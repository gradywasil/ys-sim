#!/bin/zsh
# Usage: tools/sweep_bot.sh FIRST_SEED LAST_SEED STAGES
# Runs the headless P2 bot across seeds (4 at a time) and prints one result line per seed.
G="${GODOT:-/Users/arrangedgodly/Library/Application Support/Steam/steamapps/common/Godot Engine/Godot.app/Contents/MacOS/Godot}"
cd "$(dirname "$0")/.."
mkdir -p /tmp/botsweep
seeds=($(seq $1 $2))
for s in $seeds; do
  ( "$G" --headless --fixed-fps 60 --path . -- --bot --seed=$s --stages=$3 --max=900 > /tmp/botsweep/$s.log 2>&1 & pid=$!
    # Kill runs that hang (e.g. a script that failed to load) after 3 minutes.
    ( sleep 180; kill $pid 2>/dev/null ) & wait $pid ) &
  while [ $(jobs -r | wc -l) -ge 4 ]; do sleep 1; done
done
wait
for s in $seeds; do grep -E "^BOT|near chunk" /tmp/botsweep/$s.log || echo "NO RESULT seed=$s (see /tmp/botsweep/$s.log)"; done
