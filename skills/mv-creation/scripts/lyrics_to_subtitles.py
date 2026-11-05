#!/usr/bin/env python3
"""Export JSON or a literal PDoomVideo LY array as UTF-8 SRT/VTT."""
import argparse
import json
import math
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


def milliseconds(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("timestamps must be numbers in seconds")
    if not math.isfinite(value) or value < 0:
        raise ValueError("timestamps must be finite and non-negative")
    return int((Decimal(str(value)) * 1000).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def load_rows(path):
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".js":
        # Only strip full-line comments; preserve // inside quoted lyric text.
        text = re.sub(r"(?m)^\s*//[^\n]*(?:\n|$)", "", text).strip()
        match = re.fullmatch(r"const\s+LY\s*=\s*(\[.*\])\s*;?\s*", text, re.S)
        if not match:
            raise ValueError("JS input must contain only const LY = a JSON-compatible array")
        text = match.group(1)
    data = json.loads(text)
    if not isinstance(data, list) or not data:
        raise ValueError("input must be a non-empty array")
    rows = []
    previous_start = -1
    for index, row in enumerate(data, 1):
        if not isinstance(row, list) or len(row) not in (3, 4):
            raise ValueError(f"row {index}: expected [start, end, text, optional metadata]")
        start, end = milliseconds(row[0]), milliseconds(row[1])
        if end <= start:
            raise ValueError(f"row {index}: end must follow start after millisecond rounding")
        if start < previous_start:
            raise ValueError(f"row {index}: rows must be ordered by start time")
        if not isinstance(row[2], str) or not row[2].strip():
            raise ValueError(f"row {index}: lyric text must be a non-empty string")
        lyric = row[2].strip().replace("\r\n", "\n").replace("\r", "\n")
        if "\n\n" in lyric or "\x00" in lyric or "-->" in lyric:
            raise ValueError(f"row {index}: text contains an invalid subtitle delimiter")
        rows.append((start, end, lyric))
        previous_start = start
    return rows


def timestamp(value, separator):
    seconds, ms = divmod(value, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}{separator}{ms:03}"


def render(rows, format_name):
    separator = "," if format_name == "srt" else "."
    blocks = []
    for index, (start, end, lyric) in enumerate(rows, 1):
        if format_name == "vtt":
            lyric = lyric.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        blocks.append(f"{index}\n{timestamp(start, separator)} --> {timestamp(end, separator)}\n{lyric}")
    return ("WEBVTT\n\n" if format_name == "vtt" else "") + "\n\n".join(blocks) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--format", choices=("srt", "vtt"))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    format_name = args.format or args.out.suffix.lower().lstrip(".")
    if format_name not in ("srt", "vtt"):
        parser.error("output must end in .srt/.vtt or specify --format")
    try:
        rows = load_rows(args.input)
        content = render(rows, format_name)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w" if args.overwrite else "x", encoding="utf-8", newline="\n") as file:
            file.write(content)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"Wrote {len(rows)} cues: {args.out}")


if __name__ == "__main__":
    main()
