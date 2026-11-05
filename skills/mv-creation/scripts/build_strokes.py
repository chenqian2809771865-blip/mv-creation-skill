#!/usr/bin/env python3
"""Build strokes.json (real stroke order for hanzi.py / handwriting effects) for just the characters a song needs.

usage: python3 build_strokes.py SOURCE [SOURCE ...] --out code/strokes.json [--merge] [--graphics graphics.txt]

SOURCE: lyrics.json ([[start, end, text, ...], ...]), a .lrc, or any UTF-8 text file; every CJK character in it is
collected. Data comes from Make Me a Hanzi graphics.txt (Arphic Public License; keep that notice if you ship the
data). It is downloaded once from raw.githubusercontent.com to ~/.cache/mv-creation/ (github.com/.../raw/ links can
get 403 behind the proxy). --merge keeps the characters already in --out. Missing characters are listed: write
those with a font instead, or pick other wording for on-screen text.
Output format: {char: {"m": medians, "s": stroke outline paths}} as hanzi.py expects.
"""
import argparse
import json
import os
import re
import sys
import urllib.request

URL = 'https://raw.githubusercontent.com/skishore/makemeahanzi/master/graphics.txt'
CACHE = os.path.expanduser('~/.cache/mv-creation/graphics.txt')
CJK = re.compile(r'[㐀-鿿豈-﫿]')


def chars_from(path):
    text = open(path, encoding='utf-8-sig').read()
    if path.endswith('.json'):
        try:
            text = ''.join(r[2] for r in json.loads(text) if isinstance(r, list) and len(r) > 2)
        except (ValueError, TypeError, IndexError):
            pass
    elif path.endswith('.lrc'):
        text = re.sub(r'\[[^\]]*\]', '', text)
    return set(CJK.findall(text))


def graphics(path):
    if path:
        return path
    if not os.path.exists(CACHE):
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        print('downloading', URL, file=sys.stderr)
        try:
            urllib.request.urlretrieve(URL, CACHE + '.part')
        except OSError as e:
            sys.exit('download failed (%s); attach graphics.txt and pass --graphics' % e)
        os.replace(CACHE + '.part', CACHE)
    return CACHE


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('sources', nargs='+')
    ap.add_argument('--out', required=True)
    ap.add_argument('--merge', action='store_true')
    ap.add_argument('--graphics')
    a = ap.parse_args()
    want = set().union(*(chars_from(s) for s in a.sources))
    data = json.load(open(a.out, encoding='utf-8')) if a.merge and os.path.exists(a.out) else {}
    need = want - set(data)
    with open(graphics(a.graphics), encoding='utf-8') as fh:
        for line in fh:
            if not need:
                break
            row = json.loads(line)
            if row['character'] in need:
                data[row['character']] = {'m': row['medians'], 's': row['strokes']}
                need.discard(row['character'])
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(data, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('%s: %d characters (%d requested)' % (a.out, len(data), len(want)))
    if need:
        print('not in Make Me a Hanzi:', ''.join(sorted(need)))


if __name__ == '__main__':
    main()
