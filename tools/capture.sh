#!/bin/zsh
# Records a showcase clip of the game (the bot plays P2 on screen) as a GIF plus a still.
# Usage: tools/capture.sh NAME [STAGE_INDEX=0] [SECONDS=8] [SEED=7] [FPS=15] [WIDTH=640]
#   NAME         output basename, e.g. 2026-10-02-kitchen -> docs/devlog/media/NAME.gif, NAME.mp4 and NAME.png
#   STAGE_INDEX  0 bedroom, 1 kitchen, 2 backyard, 3 basement, 4 attic
# Extra game args: EXTRA="--first=cans,cans" tools/capture.sh ... (forces the opening chunks).
# Needs a display (it opens the game window) and ffmpeg. Extra Godot user args can go after `--` in EXTRA.
G="${GODOT:-/Users/arrangedgodly/Library/Application Support/Steam/steamapps/common/Godot Engine/Godot.app/Contents/MacOS/Godot}"
cd "$(dirname "$0")/.."
NAME=$1; STAGE=${2:-0}; SECS=${3:-8}; SEED=${4:-7}; FPS=${5:-10}; WIDTH=${6:-512}
OUT=docs/devlog/media
TMP=$(mktemp -d)
mkdir -p "$OUT"
"$G" --path . --write-movie "$TMP/f.png" --fixed-fps 30 --quit-after $((SECS * 30)) -- --showcase --seed=$SEED --start-stage=$STAGE ${=EXTRA} > "$TMP/log.txt" 2>&1
FRAMES=$(ls "$TMP"/f*.png 2>/dev/null | wc -l | tr -d ' ')
if [ "$FRAMES" -eq 0 ]; then echo "no frames captured; log:"; tail -20 "$TMP/log.txt"; exit 1; fi
ffmpeg -loglevel error -y -pattern_type glob -framerate 30 -i "$TMP/f*.png" \
  -vf "fps=$FPS,scale=$WIDTH:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=160:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle" \
  "$OUT/$NAME.gif"
ffmpeg -loglevel error -y -pattern_type glob -framerate 30 -i "$TMP/f*.png" -vf "scale=960:-1:flags=lanczos" \
  -c:v libx264 -pix_fmt yuv420p -crf 22 -preset medium "$OUT/$NAME.mp4"
MID=$(ls "$TMP"/f*.png | sed -n "$((FRAMES * 2 / 3))p")
ffmpeg -loglevel error -y -i "$MID" -vf "scale=960:-1:flags=neighbor" "$OUT/$NAME.png"
rm -rf "$TMP"
echo "wrote $OUT/$NAME.gif ($(du -h "$OUT/$NAME.gif" | cut -f1)), $OUT/$NAME.mp4 ($(du -h "$OUT/$NAME.mp4" | cut -f1)) and $OUT/$NAME.png from $FRAMES frames"
