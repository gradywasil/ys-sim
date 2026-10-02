# Devlog

A running record of how the game looks and plays as it's built, for sharing between dev stages.
Each entry is a short markdown file with stills and clips from `media/`.

| Entry | What it covers |
|---|---|
| [001: Five rooms, bedtime, hazards](001-five-rooms.md) | Hi-res art pass, the stage generator, five themed rooms, bedtime, first hazards |
| [002: Rolling hazards, trampoline and ramp](002-rollers-and-launchers.md) | Marble and paint-can lanes, placeable launchers |
| [003: Slippery floors, mud, slippers and sugar rush](003-slips-mud-sugar.md) | Puddles, mud, two new buffs, scrolling item bar |
| [004: Darkness in the Basement](004-darkness.md) | Dark rooms, flashlight |
| [005: The rest of the hazards, and four more power-ups](005-traps-and-gadgets.md) | Wind, traps, spider, web, loose board, dust; fan, tape, bubble wrap, gloves |

## Capturing a clip

The bot plays P2 on screen, so a clip shows the full loop (P1 asking for help, items dropping, hazards).

```
tools/capture.sh NAME [STAGE_INDEX=0] [SECONDS=8] [SEED=7] [FPS=10] [WIDTH=512]
```

- `STAGE_INDEX`: 0 Bedroom, 1 Kitchen, 2 Backyard, 3 Basement, 4 Attic.
- Writes `media/NAME.gif` (small, plays inline in markdown), `media/NAME.mp4` (sharp, ~3x smaller) and `media/NAME.png` (a still).
- It opens the game window and records with Godot's movie writer at a fixed 30 fps, so capture speed doesn't affect what you see. It needs a display and `ffmpeg`.
- Same `STAGE_INDEX` + `SEED` always produces the same level, so a feature can be re-shot the same way later.
- To show a specific moment: `EXTRA="--first=marbles,cans --prefer=trampoline" tools/capture.sh ...` forces the opening chunks (`--first`, ids from `level_gen.gd`) and makes the bot pick one item whenever it's an option (`--prefer`). Debug builds also have keys: **N** next stage, **M** skip ahead, **T** trip P1, **H**/**J** spawn a burner/sprinkler.

Naming: `NNN-topic` (entry number, then what's in it), e.g. `002-marbles`.

## Writing an entry

1. Capture 1-3 clips and stills of whatever is new.
2. Copy the structure of the latest entry: a one-line summary, what changed, what it looks like (media), what's next.
3. Add it to the table above.

Media is large (about 35 MB for entry 001). If this goes into git, use Git LFS for `docs/devlog/media/`.
`docs/.gdignore` keeps Godot from importing these files as game assets.
