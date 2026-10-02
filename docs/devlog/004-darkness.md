# 004: Darkness in the Basement

The Basement is dark now, so Player 2 can't just read the level ahead.

## What's new

- **Darkness.** In the Basement the whole room dims to near-black. P1 carries a small circle of light, and there's a little light around your hand so you can still aim. Hazards and obstacles ahead are hidden until P1 gets close, so you can't pre-place a trampoline or slippers by sight. P1 can still see, so "NEEDS" bubbles and waiting work as usual.
- **Flashlight** (a buff, unlocked in the Basement): P1 pulls out a flashlight (new animations) and lights a long beam forward for 9 seconds, showing the next hazards. It trips P1 if its hands are full (an umbrella or feather is active).
- Darkness fades in and out as you cross a stage gate, and the shader uses hard light bands to match the pixel art.

## Hands-free demo: the bot hands over a flashlight and P1 lights up the hazards ahead
![Darkness](media/004-darkness.gif)

(Sharper version: `media/004-darkness.mp4`.)

## Where things stand

11 power-ups across three families, 10 kinds of hazard and floor zone across five rooms, a bedtime clock, and generated endless stages that a headless bot verifies are solvable. See `docs/design-stages-powerups.md`.

## Next

Left over from the art drop and not built yet: wind gusts, dripping pipes, mousetraps, cobwebs, loose boards, spiders and dust clouds, plus bubble wrap, sticky gloves, a fan and tape as power-ups.
