# Younger Sibling Simulator: Art Brief v3 (stage themes, real powerups, hazards, bedtime)

Paste this whole file to the art agent. All v2 rules still apply (`docs/art-brief-v2.md`): true pixel art, hard-edged alpha, 960x540 screen with 1 art pixel = 1 screen pixel, light from the upper left, 1px lighter top-left rim and darker bottom-right rim, selective dark-purple outline (never pure black), feet on the bottom edge of character frames, horizontal sprite strips with no padding.

Deliver into `art/v2/`, add every new file to `art/v2/manifest.json` (`frame_w`, `frame_h`, `frames`, `fps`, `loop`), and keep file names exactly as listed. Existing files with the same name (the placeholders for `item_umbrella` and `item_bridge`) get overwritten.

**Work in phases and tell Claude when each phase is done**, so the game can be wired up while you draw the next one.

## Palette

Keep the shared `palette.png` (64 colors) for everything that appears in every stage (P1, the hand, items, HUD, the parent, the cat). Each stage may add up to **16 accent colors** of its own, delivered as `palette_kitchen.png`, `palette_yard.png`, `palette_basement.png`, `palette_attic.png` (1 pixel per color). Stage backgrounds, tilesets, props and hazards may use shared plus that stage's accents. Verify with `tools/verify_art.py` (extend it to accept the per-stage palettes).

## Phase A: real powerup art, bedtime HUD, cookie, status HUD (needed first)

### A1. Replace the two placeholders and add the placed bridge

| File | Frame size | Frames | fps | Loop | Notes |
|---|---|---|---|---|---|
| `item_umbrella.png` | 48x48 | 6 | 8 | yes | A bright red-and-white kid's umbrella, bobbing, with a glint. Same silhouette and rim light rules as `item_boots`. |
| `item_umbrella_pop.png` | 48x48 | 3 | 24 | no | Pickup starburst (red tinted). |
| `item_bridge.png` | 48x48 | 6 | 8 | yes | A flat of corrugated cardboard with tape, bobbing. |
| `item_bridge_pop.png` | 48x48 | 3 | 24 | no | Cardboard confetti pop. |
| `bridge_plank.png` | 240x32 | 1 | 0 | no | The placed bridge: a long cardboard plank with tape strips, 16px of overhang on each end. Its top edge is the walking surface, flush with the floor lip. Must tile cleanly if the game scales it to other widths: keep the middle 128px free of unique details so it can be stretched. |
| `bridge_land.png` | 240x48 | 6 | 24 | no | Landing fx: a dust puff along the length, the plank settling with a small bounce. |
| `fx_umbrella_canopy.png` | 64x48 | 8 | 12 | no | Opens above P1's head (anchor: bottom-center sits on the head) in frames 1-3, then loops a gentle sway in frames 4-8. |

### A2. Bedtime timer HUD (a countdown to Mom's "lights out")

| File | Frame size | Frames | fps | Notes |
|---|---|---|---|---|
| `ui_bedtime_clock.png` | 96x96 | 12 | 0 | A cartoon alarm clock face. Each frame is a time step from "plenty of time" (frame 1) to "midnight" (frame 12), hands advancing, with the last 3 frames visibly panicking (bell shaking, a red tint on the rim). The game picks the frame from the remaining time. |
| `ui_bedtime_clock_ring.png` | 96x96 | 6 | 16 | Ringing animation (shaking clock with sound lines), played when time is nearly up. |
| `ui_bedtime_moon.png` | 48x48 | 4 | 0 | A little crescent moon with a sleepy face: awake, drowsy, yawning, asleep. |
| `ui_bedtime_warning.png` | 960x540 | 4 | 6 | A thin red-purple screen-edge pulse overlay (hard-banded, transparent in the middle) shown during the last 15 seconds. |
| `ui_banner_bedtime.png` | 384x96 | 6 | 12 | A "BEDTIME!" stamp banner for the game-over screen (like `ui_banner_grounded`). Leave the text as a shape, not font-dependent. |
| `parent_bedtime.png` | 128x192 | 8 | 10 | The parent at the bedroom door in a robe, tapping a wristwatch, then pointing at the bed. |
| `parent_speech_bedtime.png` | 192x96 | 1 | 0 | A speech bubble shape for "BEDTIME!" (text is drawn by the game). |

### A3. Cookie (a rare relief item that calms the parent)

| File | Frame size | Frames | fps | Notes |
|---|---|---|---|---|
| `item_cookie.png` | 48x48 | 6 | 8 | A big chocolate-chip cookie with a golden shimmer, a little warmer and shinier than the coin. |
| `item_cookie_pop.png` | 48x48 | 4 | 24 | Crumb burst with hearts. |
| `parent_happy.png` | 128x192 | 8 | 10 | The parent in the doorway, takes a bite, closes their eyes happily, nods. |
| `fx_crumbs.png` | 16x16 | 6 | 14 | Cookie crumbs. |
| `fx_calm_wave.png` | 128x64 | 6 | 16 | A soft ring of hearts and sparkles that spreads from the parent's door. |

### A4. Active-buff status HUD

| File | Frame size | Frames | fps | Notes |
|---|---|---|---|---|
| `ui_status_ring.png` | 48x48 | 16 | 0 | A circular timer ring: frame 1 is full, frame 16 is empty, drawn so the buff's icon (the game draws it inside) sits in the center. |
| `ui_status_bg.png` | 56x56 | 1 | 0 | The rounded badge behind the ring. |

### A5. New powerup icons (the roadmap items). All are 48x48, 6 frames, 8 fps, loop; each with a `_pop` sheet of 3 frames at 24 fps (no loop). Same style as the existing items.

- `item_slippers.png`: fluffy pink bunny slippers with floppy ears.
- `item_sugar.png`: a fizzing soda can (bright cyan and yellow) with bubbles popping off it.
- `item_stopwatch.png`: a chunky silver stopwatch with a glowing blue face.
- `item_bubblewrap.png`: a roll of bubble wrap with shimmering bubbles.
- `item_gloves.png`: a pair of sticky green gloves with a visible gooey sheen.
- `item_trampoline.png`: a tiny, red-and-blue mini trampoline (the dropped item version).
- `item_fan.png`: a small desk fan with spinning blades.
- `item_tape.png`: a roll of bright blue painter's tape.
- `item_ramp.png`: a wedge-shaped stack of books (the dropped item version).

Placed versions of the placeables, bottom-anchored (feet of the object on the bottom edge), animated:
- `placed_trampoline.png`: 96x48, 6 frames at 20 fps, one-shot bounce (squash, launch, settle) plus a still frame as the first frame.
- `placed_ramp.png`: 96x48, 1 frame, a wedge of books, low side facing left.
- `placed_fan.png`: 64x64, 8 frames at 16 fps, loop, with a blast of wind lines coming off its right side (the lines are part of the animation, white at 60% opacity using hard-banded alpha).
- `placed_tape.png`: 64x16, 1 frame, a strip of blue tape flat on the ground, slightly curled at the ends.

## Phase B: stage themes (Kitchen, Backyard, Basement, Attic)

Each stage is the same set of files with a prefix: `kitchen_`, `yard_`, `basement_`, `attic_`. The game already has the bedroom versions (no prefix) to match the layout and scale. Reuse the sizes and layout rules from v2 exactly.

### Per-stage file list (replace `<s>` with the stage prefix)

| File | Size / frames | Notes |
|---|---|---|
| `<s>_bg_far.png` | 960x540, 1 | Far wall or sky layer. |
| `<s>_bg_far_anim.png` | 960x540, 4 frames, 3 fps | An overlay layer of ambient motion (twinkling stars, a flickering bulb, steam, drifting clouds). |
| `<s>_bg_mid.png` | 1280x540, 1 | Mid layer, seamless left/right, mid-tone. Large furniture/features for this room. |
| `<s>_bg_near.png` | 960x540, 1 | Dark silhouettes, transparent above the floor line at y=400, each with a 1px warm rim light. |
| `<s>_sky_gradient.png` | 1x540, 1 | Hard-banded 8-color gradient. |
| `<s>_fg_legs.png` | 960x540, 1 | Foreground silhouettes (they scroll faster than the main layer). |
| `<s>_fg_dust.png` | 960x540, 1 | Foreground particles for this stage (leaves, steam wisps, fireflies, cobweb fibers, or dust). |
| `<s>_tileset_floor.png` | 256x96 | The same 8x3 grid of 32px tiles as `tileset_floor.png`. Row 0: surface (0,1 plain, 2 left edge, 3 right edge, 4-7 decor). Row 1: fill. Row 2: deep shade. |
| `<s>_pit_bg.png` | 32x128 | The inside of a pit, tiles horizontally. |
| `<s>_obstacles.png` | 128x32 | Four 32x32 skins for a stackable obstacle block (they stack, so every side must read as a repeating block). |
| `<s>_obstacles_tall.png` | 128x32 | A 4-frame variant sheet for the top block of a tall stack (a recognizable cap). |
| `<s>_goal.png` | 64x128, 6 frames, 10 fps | The stage-exit gate/flag for this room (the thing P1 passes to enter the next stage). |
| `<s>_deco_*.png` + `_shadow` | 24-96px | **10 floor-clutter pieces** per stage, each with its `_shadow.png` (hard-banded ellipse). |
| `<s>_prop_*.png` | listed below | **6 animated props** per stage. |

Also deliver `ui_stage_card.png` (480x144, 1 frame): a decorative banner frame that the game draws stage text over, with matching color variants as 4 frames side by side (frame size 480x144): bedroom, kitchen, yard, basement. Frame 5 is attic (so the sheet is 5 frames, 2400x144).

### Kitchen (warm cream and teal, late-night snack energy)

Look: checkerboard tile floor with grout lines, yellow ceiling light, a fridge covered in kid drawings, magnets, a stove, a dish rack, a bread box, a calendar. Obstacles: stacked cereal boxes, a stack of pizza boxes, cans, a milk crate, a pile of plates (4 skins). Floor clutter: dropped cereal, a spilled sugar bowl, a fork, a spoon, a bottle cap, a crushed juice box, pasta noodles, a banana peel, a spilled bag of flour handprint, a grape.
Props (animated): `kitchen_prop_fridge_light.png` (a fridge door cracked open, with light spilling, 6 frames), `kitchen_prop_kettle.png` (steaming kettle, 8 frames), `kitchen_prop_clock.png` (a rooster clock, 8 frames), `kitchen_prop_toaster.png` (toast pops up, 10 frames), `kitchen_prop_dripping_tap.png` (a tap with a drip, 10 frames), `kitchen_prop_fruit_fly.png` (a looping orbit, 8 frames).
Goal gate: an oven-mitt-shaped flag on a wooden spoon pole.

### Backyard (dusk green and orange, fireflies and string lights)

Look: a night garden seen from the patio: fence boards, grass tufts, a swing set silhouette, a garden gnome, string lights, a shed, a moon behind clouds. The floor tileset is grass over dirt (2px grass blades on top, dirt with pebbles below). Obstacles: stacked flowerpots, garden gnomes (4 skins), watering cans, a stack of bricks. Floor clutter: a flower, a stick, a toy shovel, an acorn, a ladybug (static), a dandelion, a chewed bone, a muddy sneaker, a kite string spool, a frisbee.
Props: `yard_prop_swing.png` (a swing set swaying, 10 frames), `yard_prop_string_lights.png` (twinkling bulbs, 8 frames), `yard_prop_windmill.png` (a pinwheel, 8 frames), `yard_prop_sprinkler_idle.png` (a decorative sprinkler head, 6 frames), `yard_prop_gnome.png` (a gnome that blinks once, 8 frames), `yard_prop_butterflies.png` (2 butterflies looping, 10 frames).
Goal gate: a pinwheel on a garden stake.

### Basement (cool blue-gray, one bare bulb)

Look: concrete floor with cracks, pipes along the ceiling, a flickering bare bulb, a furnace with a glowing window, shelves of paint cans and boxes, a workbench, a dusty old TV, a washing machine. Floor tileset: concrete with cracks, oil stains, and drain grates. Obstacles: paint cans, cardboard moving boxes (stacked, taped), cinder blocks, a stack of old tires (4 skins). Floor clutter: a screw, a nail, a bolt, a rag, a flashlight (dropped, off), a crumpled blueprint, a rusty key, a jar of nails, a mouse trap (sprung, harmless decor), a pile of sawdust.
Props: `basement_prop_bulb.png` (a swinging bare bulb with a glow, 10 frames), `basement_prop_furnace.png` (glowing furnace window with flicker, 8 frames), `basement_prop_pipe_drip.png` (pipe with a drip and a small puddle ripple, 10 frames), `basement_prop_washer.png` (a washing machine mid-cycle, rattling, 8 frames), `basement_prop_spider.png` (a spider that lowers on a thread and goes back up, 12 frames), `basement_prop_tv_static.png` (an old TV showing static, 6 frames).
Goal gate: a pull-chain light bulb that switches on.

### Attic (dusty amber, moonlight through a round window)

Look: sloped wooden roof beams, dusty floorboards, a round window with a moon, covered furniture (white sheets), trunks, boxes, an old rocking chair, a dress form, hanging strings of old photos, cobweb corners. Floor tileset: wide worn floorboards with gaps and nail heads. Obstacles: stacked suitcases, steamer trunks, hat boxes, a stack of old photo albums (4 skins). Floor clutter: a marble, a brittle comic book, a faded photo, a music box key, a tarnished spoon, a bundle of letters, a porcelain doll arm, an old teddy eye, a dust bunny, a jar of buttons.
Props: `attic_prop_rocking_chair.png` (rocking on its own, 10 frames), `attic_prop_moon_window.png` (moonlight shaft with swirling dust, 8 frames), `attic_prop_sheet_ghost.png` (a sheet-covered chair that sways, 8 frames), `attic_prop_music_box.png` (a ballerina spinning, 8 frames), `attic_prop_cobweb.png` (a swaying web with a small spider, 8 frames), `attic_prop_mobile.png` (an old mobile with faded animals, 10 frames).
Goal gate: a lantern on an old broom handle.

## Phase C: stage hazards and P1 reactions

All hazards are drawn on a 32px grid and bottom-anchored on the floor lip unless noted. For each one deliver a **telegraph** (the warning state) as the first frames so the game can show it before it becomes dangerous. If a hazard is dangerous, its dangerous frames must be unmistakable (hard red/orange accent, high contrast).

### Kitchen hazards

| File | Frame size | Frames | fps | Behavior |
|---|---|---|---|---|
| `hazard_juice_puddle.png` | 96x16 | 6 | 8 | A flat, shimmering puddle of orange juice on the floor. P1 slips on it (spins out and slides forward). |
| `hazard_marble.png` | 24x24 | 8 | 14 | A big glass marble with a swirl, rolling leftward along the floor, looping. P1 must jump or be knocked back. |
| `hazard_stove_burner.png` | 64x48 | 10 | 10 | A stove burner on the floor: frames 1-3 cold coil, 4-5 warming red glow (telegraph), 6-10 flame jets up. Loops. |
| `hazard_spill_trail.png` | 32x16 | 4 | 6 | A small drip trail that leads into a puddle (decor that previews it). |

### Backyard hazards

| File | Frame size | Frames | fps | Behavior |
|---|---|---|---|---|
| `hazard_sprinkler.png` | 64x96 | 10 | 10 | A sprinkler head on a short stake: frames 1-3 idle, 4-5 wobble (telegraph), 6-10 spraying arcs of water. Loops. |
| `hazard_water_spray.png` | 192x96 | 8 | 14 | The water arcs themselves as an overlay (white-blue, hard-banded alpha), anchored to the left of the sprinkler's head. |
| `hazard_mud.png` | 96x16 | 6 | 6 | A pool of thick brown mud with bubbles popping. P1 slows to a trudge in it. |
| `hazard_wind_gust.png` | 192x64 | 8 | 14 | A swirl of white wind lines and leaves crossing the screen (the whole thing moves in-engine; the sheet only animates the streaks). Telegraph in frames 1-2. |
| `fx_leaf.png` | 16x16 | 8 | 12 | A tumbling leaf, 2 color variants as 2 files: `fx_leaf.png` and `fx_leaf_b.png`. |

### Basement hazards

| File | Frame size | Frames | fps | Behavior |
|---|---|---|---|---|
| `hazard_paint_can.png` | 40x40 | 8 | 12 | A rolling paint can with a drip of bright paint trailing, rolling leftward. |
| `hazard_drip.png` | 16x48 | 10 | 12 | A droplet that forms on the ceiling, falls, and splashes on the floor; frames 1-4 telegraph the swell. |
| `hazard_mousetrap.png` | 48x24 | 8 | 14 | A big wooden mouse trap on the floor: set (frames 1-3, with a glint), snapping (4-5), sprung (6-8). |
| `light_flashlight_cone.png` | 256x128 | 1 | 0 | A hard-banded warm light cone, pointing right, used when the player has the flashlight item. |
| `light_dark_mask.png` | 512x512 | 1 | 0 | A hard-banded radial gradient: transparent in the middle, fully dark at the edges, in 6 bands. The game uses it as a "darkness with a hole" around P1. |
| `item_flashlight.png` + `_pop` | 48x48, 6 frames + 3 | 8/24 | | The dropped flashlight item, a yellow chunky flashlight with a beam glint. |

### Attic hazards

| File | Frame size | Frames | fps | Behavior |
|---|---|---|---|---|
| `hazard_cobweb.png` | 96x64 | 6 | 6 | A dense cobweb hung across the path at jump height. P1 gets stuck for a moment if it runs into it; the web trembles. |
| `hazard_loose_board.png` | 64x24 | 8 | 10 | A floorboard that creaks (frames 1-3), tilts (4-5), and drops away (6-8, the board falls into darkness). |
| `hazard_dust_cloud.png` | 64x64 | 8 | 10 | A cloud of dust that puffs up from a floorboard and blinds the screen edge briefly (the cloud is a silhouette the game can scale). |
| `hazard_spider_drop.png` | 16x64 | 10 | 12 | A spider dropping on a thread from above and retracting. |

### Shared hazard feedback

- `fx_warning_exclaim.png`: 16x24, 6 frames at 12 fps, a bouncing red exclamation mark that pops above a telegraphing hazard.
- `fx_slip_swirl.png`: 32x16, 6 frames at 16 fps, swirl lines under P1's feet while slipping.
- `fx_splat.png`: 32x32, 5 frames at 20 fps, a generic splatter (tint it in the game).
- `fx_shield_bubble.png`: 64x64, 8 frames at 12 fps, a soft bubble-wrap shield around P1 (hard-banded alpha, with a pop animation in the last 3 frames).
- `fx_sugar_blur.png`: 64x32, 6 frames at 24 fps, a rainbow speed smear trailing behind P1.

### P1 reactions to hazards (64x64 per frame, same style and anchor rules as the existing P1 sheets)

| File | Frames | fps | Loop | Notes |
|---|---|---|---|---|
| `p1_slip.png` | 8 | 14 | no | Feet fly out on a puddle, a skid with arms flailing, a seated landing. |
| `p1_slog.png` | 8 | 10 | yes | Trudging through mud, each leg lifting out with a sucking pull. |
| `p1_lean.png` | 6 | 12 | yes | Leaning into a strong wind, hair and hoodie blown backwards. |
| `p1_ouch.png` | 8 | 14 | no | Hopping on one foot, holding the other, wincing. |
| `p1_stuck.png` | 8 | 10 | yes | Struggling in a cobweb, wriggling. |
| `p1_sprint.png` | 8 | 28 | yes | Sugar-rush sprint: blurred legs, wide eyes, hair streaming, leaning far forward. |
| `p1_flashlight_idle.png` | 8 | 8 | yes | Standing and sweeping a flashlight, nervous eyes. |
| `p1_flashlight_run.png` | 12 | 20 | yes | Running holding a flashlight out front. |
| `p1_blown.png` | 8 | 14 | no | Knocked backwards a step by a gust, arms out. |

## Delivery checklist

- [ ] Every file in the lists above exists in `art/v2/` with the stated size, frame count, and manifest entry. Report which phases are complete.
- [ ] Each stage's files use only the shared palette plus that stage's 16 accents.
- [ ] Stage tilesets line up in the same 8x3 layout as `tileset_floor.png`, and the obstacle skins stack cleanly.
- [ ] Every hazard has a readable telegraph state, and the dangerous frames are clearly different from it.
- [ ] Everything reads at 1x on both a bright and a dark background (check P1 with each stage's background).
- [ ] The stage palettes' accent colors do not collide with the item colors (boots orange, feather white-blue, umbrella red, bridge cardboard tan, coin and cookie gold).
- [ ] Tell Claude the phase names that are finished.
