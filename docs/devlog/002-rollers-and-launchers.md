# 002: Rolling hazards, trampoline and ramp

Two new kinds of obstacle that you can't just wait for P1 to jump, and two new placeable power-ups that vault P1 over them.

## What's new

- **Roller lanes.** Kitchen marbles and Basement paint cans stream across a stretch of floor once P1 gets close. P1 waits for the stream to finish, which burns bedtime. The stopwatch freezes the rollers so P1 can walk through them.
- **Trampoline and ramp** (placeables). Drop one just before a lane and it snaps into place so P1 launches over the rollers: the trampoline pops P1 straight up, the ramp gives a lower, faster launch. A preview strip under the hand turns green when it will snap to a lane. Drop one on P1's head and P1 trips.
- Unlocks: trampoline from the Backyard, ramp from the Basement. The stopwatch (Kitchen) is the answer until then.
- The generator knows about lanes (`marbles`, `cans`), the AI waits for them, and the headless bot sweeps (hundreds of seeds, all 5 rooms and beyond) clear them with the stopwatch, trampoline and ramp.

## Marbles in the Kitchen: wait, then the stopwatch freezes them
![Marbles](media/002-marbles.gif)

## Trampoline over a lane in the Backyard
![Trampoline](media/002-trampoline.gif)

## Ramp over paint cans in the Basement
![Ramp](media/002-ramp-cans.gif)

(Sharper versions: `media/002-*.mp4`.)

## Next

Slippery and slow zones: juice puddles and mud, with slippers and sugar rush; then darkness in the Basement with a flashlight.
