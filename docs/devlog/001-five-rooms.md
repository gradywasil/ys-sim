# 001: Five rooms, bedtime, hazards

You play Player 2: a hand that drops power-ups onto Player 1, a sibling auto-running a platformer. Hand an item at the wrong moment and P1 trips and you're in trouble.

## Where things stand

- **Hi-res pixel art** at 960x540 (an exact 2x window), with animated props, a cat that reacts to the action, and parallax with a foreground depth layer.
- **Endless generated stages.** A seeded chunk generator streams the level ahead of the camera, so every run is different but every level is solvable (a headless bot plays P2 across hundreds of seeds as a regression test).
- **Five themed rooms**, each with its own sky, parallax layers, floor, obstacles, clutter and props: Bedroom, Kitchen, Backyard, Basement, Attic. The endless mode cycles through them.
- **Power-ups with different "wrong moments":** boots (not mid-air), feather (only when P1 is waiting), umbrella (not while running), bridge (a placeable: where you drop it matters), stopwatch (freezes hazards, but dizzies P1 if boots are active), cookie (calms Mom; limited stock).
- **Bedtime:** a lights-out timer drains while P1 waits, so power-ups save time but risk a trip. The room darkens and pulses red as it runs out.
- **Cycling hazards** (stove burner, sprinkler) that P1 waits out unless you skip the wait.

## Bedroom
![Bedroom](media/001-bedroom.gif)

## Kitchen
![Kitchen](media/001-kitchen.gif)

## Backyard
![Backyard](media/001-backyard.gif)

## Basement
![Basement](media/001-basement.gif)

## Attic
![Attic](media/001-attic.gif)

(Sharper versions: `media/001-*.mp4`. Stills: `media/001-*.png`.)

## Next

Moving hazards (rolling marbles and paint cans) with a trampoline and a ramp as ways over them; then slippery and slow zones; then darkness in the basement with a flashlight.
