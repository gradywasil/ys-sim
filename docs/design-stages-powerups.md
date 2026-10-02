# Stages, generation, and powerups

## How the level system works

- `scripts/data/stages.gd`: stage definitions (name, chunk count, difficulty ramp `d0..d1`, powerups unlocked on entry, tint). Past the last stage the game loops a harder "NIGHT SHIFT" forever.
- `scripts/level/level_gen.gd`: a seeded chunk library. Each chunk is a list of primitives (`flat`, `block`, `gap`, `coins`) plus the powerups that solve it. Weights shift toward harder chunks as difficulty rises, and breathing room between hazards shrinks.
- `scripts/level/level_builder.gd`: builds chunks ahead of the camera and frees what falls behind, so levels are endless. Floor collision is one body per unbroken run. Stage gates (the pennant flag) fire `_on_stage_cleared` in `main.gd`.
- `scripts/data/powerups.gd`: powerup definitions and the "wrong moment" rule for each buff.
- Seeds: every run has a seed (`run_seed`), so any run can be reproduced.

### Verifying generated levels

A headless bot plays P2 and hands P1 whatever it asks for. If any seed gets stuck, the sweep finds it:

```
tools/sweep_bot.sh 1 24 8     # seeds 1-24, clear 8 stages each; prints one line per seed
```

Run it after changing chunk shapes, hazards, or powerups. It uses `--fixed-fps 60`, **not** `Engine.time_scale`: a scaled time step makes falling items tunnel through P1.

### Adding things

- **A chunk:** add an entry to `LIB` and a `match` arm in `build()`. Keep all sizes multiples of 16, keep 64+ units of flat floor between hazards, and list in `needs` what solves it. Then run the sweep.
- **A stage:** add a dictionary to `STAGES`. `unlock` lists powerups added on entry.
- **A hazard:** add a type to `TYPES` in `hazard.gd` (width, danger height, cycle timing, which powerups skip the wait) and a visual in `_build_art`/`_process`, then a chunk in `level_gen.gd` with a `stage` gate. The P1 AI picks it up automatically through the `hazard` group.
- **A powerup:** add to `DEFS` and `ORDER` in `powerups.gd`, give it an icon sheet `item_<id>` (and `item_<id>_pop`) in `art/v2` plus a manifest entry, add its "wrong moment" rule to `trips()`, and handle its effect in `player1.gd` `collect()`.

## Powerup families

| Family | You decide | Examples |
|---|---|---|
| Buff | **When** P1 gets it | Boots, Feather, Umbrella |
| Placeable | **Where** it lands | Bridge |
| Instant | Nothing (score or relief) | Coin |

Every buff has a different "wrong moment", so each item teaches its own timing:

| Item | Solves | Trips P1 if collected while... |
|---|---|---|
| Boots | wide gap | P1 is mid-air |
| Feather | tall tower | P1 is not waiting |
| Umbrella | wide gap (glide) | P1 is running on the ground |
| Bridge | wide gap | (placeable) it lands on P1's head |

The wide gap has three answers (boots, umbrella, bridge) so players can pick the item that fits their situation and what they have unlocked.

## Bedtime, cookies, and hazards (built)

- **Bedtime:** each stage has a lights-out budget (`bedtime` in `stages.gd`, 75-105s). The bar drains, the room darkens over the last 25s and the edges pulse red in the last 12s. A trip costs 5s, a hazard hurt costs 4s, and clearing a stage resets the budget plus a quarter of it as a carry-over bonus. Hitting zero ends the run ("Mom turned the lights off").
- **Cookie:** limited stock (1 when Kitchen unlocks it, +1 per stage cleared, max 3). P1 stops for 1.2s to eat it, but it removes one trouble and adds 10s. Unlimited items have no stock; limited ones show `xN` on the slot and grey out at zero.
- **Cycling hazards** (`scripts/level/hazard.gd`): idle, warning, dangerous. P1 reads the phase and waits for a safe window long enough to cross; it only shows the "NEEDS" bubble after waiting about 0.8s. Waiting is always safe but burns bedtime, so powerups are time-savers:
  - Stove burner (Kitchen+): the stopwatch skips the wait.
  - Sprinkler (Backyard+): the stopwatch or the umbrella (shield) skips the wait.
- **Stopwatch:** freezes every cycling hazard for 5s (they tint blue). It dizzies P1 if boots are active, which gives it its own wrong moment. Hazards use the position-derived phase, so a seed always produces the same hazard timing.
- Hazards that were built with polygon placeholders: the burner and sprinkler visuals. Phase C of `docs/art-brief-v3.md` replaces them.

### Powerups now

| Item | Solves | Trips P1 if collected while... |
|---|---|---|
| Boots | wide gap, speed, loose boards | P1 is mid-air |
| Feather | tall tower | P1 is not waiting |
| Umbrella | wide gap (glide), sprinkler, drip | P1 is running on the ground |
| Bridge (placeable) | wide gap, fallen board | it lands on P1's head |
| Trampoline (placeable) | roller lanes | it lands on P1's head |
| Ramp (placeable) | roller lanes | it lands on P1's head |
| Stopwatch | burner, sprinkler, drip, mousetrap, roller lanes | boots are active |
| Slippers | juice puddles, mud | P1 is standing still or mid-air |
| Sugar rush | wide gap, mud, wind (but P1 won't stop for anything, then crashes) | P1 is mid-air |
| Flashlight | Basement darkness, spiders | P1 holds an umbrella or feather |
| Bubble wrap | absorbs one hit, slip, web or scare | boots or sugar are active |
| Gloves | cobwebs, spiders | P1 is in mud or on a puddle |
| Fan (placeable) | wind gusts | it lands on P1's head |
| Tape (placeable) | pins burner, sprinkler, drip, mousetrap, loose board | it lands on P1's head |
| Cookie | trouble and bedtime | (never trips; limited stock) |
| Coin | score | (never) |

Hazards and floor zones: stove burner, sprinkler, mousetrap and drip (cycling, in `hazard.gd`), marble and paint-can lanes (rollers), juice puddle, mud, wind, cobweb, spider and dust (`zone.gd`), loose board (`board.gd`). Basement darkness is a room modifier.

## Roadmap (not built yet)

Every art drop so far is built. Open ideas: sticky gloves' wall-cling, stage bosses and set pieces, audio, and a title screen (the logo and button art is delivered).

## Art status

All briefs (v2 and v3, phases A-C) have been delivered and `art/v2/manifest.json` lists 390 sheets. Everything delivered for gameplay is wired in.

**Delivered but not used yet:** the logo and buttons, `ui_banner_clear`, P1's `blown` reaction, and the flashlight cone and darkness-mask images (the darkness is a shader with hard light bands).

Notes:
- The v2 `font_pixel` bitmap is unusable (glyph cells touch); the game uses Silkscreen.
- `tools/gen_placeholder_items.py` never overwrites files that already exist.
- Per-stage palettes (`palette_<stage>.png`) are delivered but not yet enforced by `tools/verify_art.py`.
