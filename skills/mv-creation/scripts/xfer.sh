#!/bin/bash
# 仅适用于 Claude 桌面版 / 云端会话；其他环境直接写本地文件。
# xfer.sh — move a big file (master MP4) to the user's computer byte-exact, through a channel that rewrites MP4/PNG
# files and refuses single files above ~25 MB.
#
#   bash xfer.sh split FILE OUTDIR [SIZE]   # in the cloud: OUTDIR/<name>.xNNN chunks + <name>.manifest (default 15m)
#   bash xfer.sh join  DIR [OUTFILE]        # on the user's computer (macOS or Linux): rebuild + verify md5
#
# Every chunk starts with a 16-byte marker (XFERCHUNK0000000) so no chunk looks like an MP4 header and gets rewritten
# in transit; join strips it, checks each chunk's md5, concatenates in order and checks the whole-file md5.
# Put chunks in <歌名>_MV/_传输分片_可删除/ and delete them afterwards (needs the user's delete permission).
# Audio decode hashes can differ between ffmpeg builds; compare the file md5, not a decode hash.
set -euo pipefail
MARK='XFERCHUNK0000000'

md5of() { if command -v md5sum >/dev/null; then md5sum "$1" | cut -d' ' -f1; else md5 -q "$1"; fi; }

case "${1:-}" in
split)
  f=$2; out=$3; size=${4:-15m}
  name=$(basename "$f"); mkdir -p "$out"
  tmp=$(mktemp -d)
  split -b "$size" -a 3 -d "$f" "$tmp/$name.x"
  : > "$out/$name.manifest"
  printf 'file\t%s\t%s\t%s\n' "$name" "$(wc -c < "$f" | tr -d ' ')" "$(md5of "$f")" >> "$out/$name.manifest"
  for p in "$tmp/$name".x*; do
    q="$out/$(basename "$p")"
    { printf '%s' "$MARK"; cat "$p"; } > "$q"
    printf 'chunk\t%s\t%s\n' "$(basename "$q")" "$(md5of "$q")" >> "$out/$name.manifest"
  done
  rm -rf "$tmp"
  echo "split $name into $(grep -c '^chunk' "$out/$name.manifest") chunks in $out"
  ;;
join)
  dir=$2
  man=$(ls "$dir"/*.manifest | head -1)
  name=$(awk -F'\t' '$1=="file"{print $2}' "$man")
  want=$(awk -F'\t' '$1=="file"{print $4}' "$man")
  out=${3:-$dir/../$name}
  : > "$out.part"
  while IFS=$'\t' read -r kind c sum; do
    [ "$kind" = chunk ] || continue
    [ -f "$dir/$c" ] || { echo "missing chunk $c"; exit 1; }
    [ "$(md5of "$dir/$c")" = "$sum" ] || { echo "chunk $c md5 mismatch — transfer it again"; exit 1; }
    [ "$(head -c 16 "$dir/$c")" = "$MARK" ] || { echo "chunk $c lost its marker"; exit 1; }
    tail -c +17 "$dir/$c" >> "$out.part"
  done < "$man"
  got=$(md5of "$out.part")
  if [ "$got" = "$want" ]; then mv "$out.part" "$out"; echo "OK $out md5 $got"; else echo "md5 mismatch: $got != $want"; exit 1; fi
  ;;
*) sed -n '2,12p' "$0"; exit 2 ;;
esac
