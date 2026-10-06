# Younger Sibling Simulator

**Your sibling runs. You decide when to help.**

A pixel-art platformer about being the helpful hand above somebody else’s adventure. The runner moves on its own, jumps ordinary obstacles, and calls for help when it reaches a problem it cannot solve. You choose the item, position the hand, and time the drop.

The catch: a useful item delivered at the wrong moment can trip the runner and get you both in trouble. Bedtime keeps counting down while you decide.

**Status:** in development. This repository contains the Godot source and recorded showcase media; it does not currently provide a downloadable release or verified browser-play link.

[Controls](#controls) · [Timing matters](#help-is-a-timing-problem) · [Rooms and unlocks](#five-rooms-then-night-shift) · [Run the source](#run-the-source) · [Development footage](docs/devlog/README.md)

![The helper hand places a trampoline and launches the runner over an obstacle](docs/devlog/media/002-trampoline.gif)

*Recorded bot-driven showcase footage from the repository. Showcase mode replenishes bedtime; this clip demonstrates the mechanic rather than unmodified manual-play difficulty.*

## How a run works

1. **Read the course.** The AI-controlled runner moves through the room and handles ordinary jumps.
2. **Watch for the need.** A NEEDS bubble tells you when the runner is waiting for help.
3. **Choose and place an item.** Move your floating hand above the course, select a tool, and drop it at the useful moment.
4. **Manage the consequences.** Good help clears hazards. Bad timing can cause a trip and add trouble.
5. **Reach the next room before bedtime.** Stage clears reduce trouble and unlock more tools.

This is **one human controlling the helper hand**, with an AI-controlled runner. The P1/P2 labels in the code describe those roles; they are not an implemented two-human co-op mode.

## Controls

| Action | Input |
| --- | --- |
| Move the hand horizontally | Mouse, A/D, or Left/Right arrows |
| Drop the selected item | Left mouse button or Space |
| Cycle items | Q/E or mouse wheel |
| Select one of the first nine item positions | Number keys 1–9 |
| Restart the run | R |

Drops have a one-second cooldown. The item bar shows eight slots at a time and scrolls with selection; Q/E and the wheel reach items beyond the first nine shortcuts. The current scripts do not implement a pause control or input-remapping menu.

## Help is a timing problem

Tools are not interchangeable bonuses. Their usefulness depends on what the runner is doing and where the item lands.

| Item | Useful moment | Risk |
| --- | --- | --- |
| **Boots** | Prepare the runner for a wide gap | Collecting them mid-air causes a trip |
| **Feather** | Deliver while the runner is waiting at a tall obstacle | It trips the runner unless the runner is waiting |
| **Umbrella** | Glide or protect against supported hazards | It trips a grounded, running runner |
| **Slippers** | Give them to a grounded runner already moving | They trip the runner when waiting or airborne |
| **Trampoline / ramp** | Place just before a roller lane on suitable flat ground | Landing the gadget on the runner’s head trips it |
| **Flashlight** | Reveal the dark Basement | It cannot be safely received while holding feather or umbrella |
| **Tape** | Pin applicable traps or loose boards | Placement matters; it is not a universal hazard remover |
| **Cookie** | Recover one trouble point and add ten seconds | It briefly stops the runner; carried stock is capped at three and replenished on stage clears |

There are **16 item definitions: 15 non-coin power-ups plus coin**. The collection includes timed buffs, placed gadgets, and instant effects. They are run tools and unlocks, not persistent upgrades between sessions.

![Kitchen showcase frame with the slippery course and helper hand](docs/devlog/media/003-slip.png)

![Kitchen showcase frame with the slipper item and buff visible](docs/devlog/media/003-slippers.png)

*Two recorded showcase frames highlighting the Kitchen hazard and slipper-tool context.*

## Five rooms, then Night Shift

| Room | Newly available tools | Base bedtime budget |
| --- | --- | --- |
| **Bedroom** | Boots, feather, coin | 75 seconds |
| **Kitchen** | Umbrella, stopwatch, slippers | 85 seconds |
| **Backyard** | Bridge, trampoline, cookie, fan | 95 seconds |
| **Basement** | Ramp, sugar rush, flashlight, tape, bubble wrap | 100 seconds |
| **Attic** | Gloves | 105 seconds |
| **Night Shift** | Previously unlocked tools remain available | 100 seconds |

Room hazards include burners, sprinklers, mousetraps, dripping pipes, rolling marbles and paint cans, puddles, mud, gusts, cobwebs, spiders, dust, and collapsing boards. The Basement adds darkness and flashlight illumination.

![Basement showcase frame with the flashlight illuminating the dark course](docs/devlog/media/004-darkness.png)

After the five rooms, Night Shift continues at maximum difficulty and cycles the room themes. Stage progression carries forward half the remaining bedtime, capped at a quarter of the next room’s base budget.

Three trouble points produce **grounded**. Running out of bedtime also ends the run. Restarting resets progress and unlocks; there is no gameplay save/load or persistent high-score system in the inspected build.

## Built around readable cause and effect

The game combines procedural course generation with visible feedback: needs bubbles, pixel animation, parallax room layers, particles, screen shake, and hit-stop. A reactive cat and room props add character around the central timing decisions.

Generation draws from 28 chunk patterns, builds ahead of the camera, and removes old course sections behind it. A supplied seed reproduces the generated course for debugging and capture. The repository includes a bot for checking generated runs, but that is not a guarantee that every seed has been independently verified solvable.

## Stack

| Layer | Implementation | Responsibility |
| --- | --- | --- |
| Engine | Godot 4.7, GL Compatibility | Scenes, 2D physics, rendering, and input |
| Game logic | GDScript | Runner AI, helper controls, items, hazards, and progression |
| Procedural course | Seeded chunk generator and builder | Assemble room paths, spawn ahead, and cull behind |
| Pixel presentation | 960×540 viewport, integer scaling, nearest-neighbor filtering, pixel snapping | Keep the pixel-art presentation consistent |
| Feedback | Shared juice/animation systems | Particles, hit-stop, camera effects, and reactions |
| Art tooling | Python and Pillow | Generate and verify art assets |
| Large assets | Git LFS | Store artwork, fonts, and recorded media |

The project configuration also enables a bundled Godot AI editor plugin/runtime helper. Its integration requirements are separate from the gameplay code; consult [the add-on](addons/godot_ai) if you intend to use that editor integration.

## Run the source

Use Git with Git LFS and a compatible **Godot 4.7** build. Install those prerequisites from their official sources before cloning.

```sh
git clone https://github.com/Arrangedgodly/ys-sim.git
cd ys-sim
git lfs pull
```

Import `project.godot` into Godot and run the main project. With a matching Godot executable on PATH:

```sh
godot --path .
```

Downloading the small Git LFS pointer files is not enough: the actual artwork/fonts/media must be present. There are currently no export presets or packaged-release instructions to substitute for the source workflow.

## Development checks and deterministic capture

The supplied bot can run a fixed seed through multiple stages:

```sh
godot --headless --fixed-fps 60 --path . -- --bot --seed=7 --stages=8 --max=900
```

The sweep script accepts a Godot path override:

```sh
GODOT=/absolute/path/to/godot tools/sweep_bot.sh 1 24 8
```

The shell tools use zsh and otherwise default to the author’s macOS Steam installation path. Set `GODOT` for your environment instead of copying that machine-specific default. With Pillow installed and LFS assets available, the art check is:

```sh
python3 tools/verify_art_v2.py
```

Read the actual report output. Bot failures such as `GAME_OVER`, `TIMEOUT`, or `STUCK` do not reliably produce a failing process exit code, and the art verifier’s result is not wired to its exit status. A zero shell exit alone is not proof that a check passed.

These are supplied development tools, not newly executed test results from this README update.

## Development footage and limits

The [devlog](docs/devlog/README.md) includes room captures and demonstrations of item/hazard interactions. Existing capture scripts use bot-driven **showcase mode**, which replenishes bedtime below 25 seconds. These clips demonstrate mechanics and presentation; they should not be read as unmodified manual-play difficulty tests.

Current development limits:

- No audio, title screen, or menu flow in the inspected game build
- No persistent run progress or high-score saving
- No downloadable release, export presets, or verified hosted play URL
- Difficulty and bedtime balance remain development work
- Bosses, set pieces, and wall-cling are ideas rather than implemented features

No root project license is provided. A bundled add-on’s license does not apply automatically to the entire game.

## Explore the implementation

- [Main game controller](scripts/main.gd): input, timers, progression, and bot arguments
- [Runner AI](scripts/player1.gd): automatic movement and help requests
- [Item definitions](scripts/data/powerups.gd): effects and wrong-moment rules
- [Stages](scripts/data/stages.gd): room budgets and unlocks
- [Level generator](scripts/level/level_gen.gd): seeded course assembly
- [Development journal](docs/devlog/README.md): mechanics, captures, and iteration history
