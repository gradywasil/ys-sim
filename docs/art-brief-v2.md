# Younger Sibling Simulator: Art Brief v2 (hi-res, packed with life)

Paste this whole file to the art agent. It replaces the size specs in `docs/art-brief.md` (the game concept, tone, palette philosophy, and lighting rules there still apply). Deliver into `art/v2/`, overwriting the placeholder files of the same name. Claude then runs `python3 tools/gen_art_data.py` and wires in anything new.

## Why v2

The game now renders at **960x540** (one art pixel is one screen pixel, shown on a 1920x1080 window at an exact 2x). v1 art was drawn for 480x270, so Player 1 had only about 20px of body to work with. The files in `art/v2/` right now are just 2x nearest-neighbor copies of v1 so the pipeline could be tested. **Do not upscale. Redraw everything with real extra detail.** Extend the existing generator scripts in `tools/` (`canvas.py`, `palette.py`, `gen_*.py`) where that helps.

## Hard rules (same as v1, restated)

1. True pixel art. No anti-aliasing, no blur, no semi-transparent edges. Fully opaque or fully transparent pixels. Exceptions: the soft light overlays in section 6, which may use hard-banded alpha.
2. One shared palette, now **up to 64 colors**, delivered as `palette.png`. Hue-shifted ramps (shadows lean purple, highlights lean warm yellow).
3. Light from the upper left. 1px lighter rim on the top-left edges, 1px darker rim on the bottom-right, and a 1-2px selective outline in the darkest purple (never pure black).
4. Transparent backgrounds. Sprite sheets are horizontal strips with no padding between frames.
5. Character feet sit on the bottom edge of the frame, body centered horizontally. Never let the body drift horizontally between run frames.
6. Every file in `art/v2/manifest.json`: `frame_w`, `frame_h`, `frames`, `fps`, `loop`. Keep all existing entries (same names) and add the new ones.

## Part A: redo every existing asset at 2x, with much more detail

All frame sizes are exactly double v1. Keep the frame counts and animation intent from v1 unless a row below says otherwise.

| Group | v2 frame size | Notes |
|---|---|---|
| `p1_*` (11 sheets) | **64x64** | Body about 40px tall, 20px wide. See P1 detail list below. |
| `hand_*` (4 sheets) | **64x64** | Palm-center origin stays at frame center. |
| `item_*`, `item_*_pop` | **48x48** | `item_glow.png` is **64x64**. |
| `tileset_floor.png` | **32x32 tiles**, 8 wide by 3 tall (layout unchanged) | Same tile index roles as v1: row 0 surface (0,1 mid, 2 left edge, 3 right edge, 4-7 decor), row 1 fill, row 2 deep shade. |
| `toy_blocks.png` | **32x32**, 4 columns by 3 rows | Same 4 colors by 3 variants. |
| `goal_flag.png` | **64x128**, 6 frames | |
| `pit_bg.png` | **32x128** | Tiles horizontally. |
| `bg_far.png` | **960x540** | Wall, window, posters. |
| `bg_far_stars.png` | **960x540** per frame, 4 frames | |
| `bg_mid.png` | **1280x540** | Seamless left/right. |
| `bg_near.png` | **960x540** | Transparent above the floor line at **y=400** (was y=200). |
| `bg_sky_gradient.png` | **1x540** | |
| `fx_*` | double v1 | `fx_bubble.png` is **192x48**; same 9-slice idea. |
| `ui_*` | double v1 | `ui_trouble_pip` 24x24 per frame, `ui_slot` 104x56 per frame, `ui_cooldown_bar` 320x12 per frame, `ui_key_*` 20x20. |
| `parent_peek.png` | **128x192**, 6 frames | |

### Player 1 detail list (this is the hero, spend the pixels here)

- A readable face: eyebrows that move, a mouth with shape changes (grin while running, gritted teeth on tripping, round "o" mouth when surprised), eyes with highlights and pupils that look toward the direction of travel.
- Clothing with real form: hoodie with drawstrings, pocket, sleeve cuffs, fabric folds that shift per frame; shorts with a hem; sneakers with laces, soles, and a toe cap.
- Hair as several locks that lag the head (follow-through and secondary motion on every run and jump frame).
- Sub-pixel style motion: use smear frames and squash and stretch in the art itself.
- Run cycle: **12 frames** at 20 fps (contact, down, passing, up, both sides, with arms crossing the body). `p1_run_fast`: 10 frames at 24 fps.
- Trip: **14 frames** at 20 fps. Toe catch, arms windmill, hang time, slide-faceplant with dust, bounce, dizzy wobble, pushes up, shakes it off, stands. Two "flat on the ground" frames held.
- Idle: 8 frames, plus three one-off idle variants played occasionally: `p1_idle_yawn.png` (8 frames), `p1_idle_stretch.png` (10), `p1_idle_bounce.png` (6, bouncing on toes).
- Waiting at a hazard: `p1_wait.png` 10 frames at 10 fps (foot tap, arm cross, checks watch, sighs), plus `p1_wait_point.png` (6 frames): points up at the hand and then at the obstacle.
- Reactions, 4-8 frames each: `p1_react_cheer.png` (caught a power-up), `p1_react_shield.png` (flinches, nearly tripped), `p1_react_scared.png` (looks down a pit), `p1_react_angry.png` (shakes a fist at the hand after a trip).
- Portraits for the HUD, **64x64** single frames: `portrait_p1_happy.png`, `portrait_p1_worried.png`, `portrait_p1_tripped.png`, `portrait_p1_angry.png`.

### Environment detail list

- **Floor**: 16 plank variations with visible grain, nail heads, scuffs, knots, wax shine on the top lip. Add a `tileset_floor_rug.png` (same 8x3 layout) for a rug section with fringe, plus a `tileset_floor_carpet.png` for a fluffy carpet stretch with tiny pixel fibers.
- **Toy block tower variants** (`toy_blocks.png` stays as is): add `obstacle_books.png` (stack of books, 32x32 slices, 4 variants), `obstacle_box.png` (cardboard box with tape and a "FRAGILE" stamp), `obstacle_jenga.png` (wobbly Jenga tower, 3 heights in 32px steps), `obstacle_lego.png` (LEGO bricks, 4 colors, studs on top). All in a 32px grid so they stack.
- **Backgrounds**: a lot more stuff on the walls. `bg_far`: wallpaper with subtle pattern, framed family photos, a pennant, height chart marks on the door frame, a clock, a corkboard of doodles. `bg_mid`: bookshelves with uneven book heights, a desk with a glowing monitor, a bed with rumpled blankets and plush toys, a toy chest spilling toys, a beanbag, a guitar on a stand, a globe. `bg_near`: dark silhouettes of a teddy bear, toy train, block towers, rocking horse, a soccer ball, a stuffed giraffe, each with a 1px warm rim light.
- **Foreground parallax** (new): `fg_legs.png` (960x540, transparent, dark silhouettes of table and chair legs, a hanging cable, bed-skirt fringe, all at the very front, which the game scrolls faster than the main layer), `fg_dust.png` (soft round dust bokeh in 3 sizes, hard-banded alpha).

## Part B: new assets that make the world feel alive

### 1. Ambient animated background props (each is an animated sheet, loops, placed in parallax layers)

| File | Frame size | Frames | fps | What it is |
|---|---|---|---|---|
| `prop_curtain.png` | 96x192 | 8 | 6 | Curtain sways in a draft by the window. |
| `prop_fan.png` | 128x64 | 8 | 12 | Ceiling fan rotating with slight wobble. |
| `prop_clock.png` | 64x64 | 8 | 4 | Wall clock with swinging pendulum and ticking second hand. |
| `prop_lamp.png` | 96x128 | 6 | 8 | Desk lamp with a subtly flickering bulb and glow. |
| `prop_lavalamp.png` | 48x96 | 10 | 6 | Lava lamp, blobs rise and fall. |
| `prop_fishbowl.png` | 96x96 | 10 | 8 | A goldfish swimming in a bowl, bubbles rising. |
| `prop_tv.png` | 128x96 | 6 | 10 | Old TV with cartoon flicker, color bars, static. |
| `prop_mobile.png` | 96x96 | 10 | 6 | A baby mobile of stars and moons, rotating. |
| `prop_poster_flap.png` | 64x96 | 6 | 6 | A poster corner fluttering. |
| `prop_plant.png` | 64x96 | 8 | 6 | Potted plant leaves swaying. |
| `prop_windup_robot.png` | 48x64 | 8 | 10 | A wind-up tin robot that walks across the background (game moves it slowly). |
| `prop_train.png` | 192x48 | 8 | 10 | Toy train puffing steam along a track (track segment included). |
| `prop_snowglobe.png` | 64x64 | 10 | 8 | Snow globe with sparkle glitter swirling. |

### 2. The family cat, a living character

`cat_*` sheets, **96x64**, feet or belly on the bottom edge. The cat sits on the bed or bookshelf and reacts to gameplay:
- `cat_sleep.png` (8 frames, 4 fps): curled up breathing, a tail twitch at the end.
- `cat_wake.png` (6 frames, 12 fps, once): opens eyes, lifts head, ears swivel.
- `cat_watch.png` (8 frames, 6 fps): sitting upright, head tracking left to right.
- `cat_startle.png` (8 frames, 20 fps, once): big puff-up jump when P1 trips.
- `cat_lick.png` (8 frames, 8 fps), `cat_yawn.png` (8 frames, 8 fps).
- `cat_zoomies.png` (8 frames, 20 fps): runs across the background when P1 clears a big gap.

### 3. The parent

- `parent_peek.png` (see the table above), plus `parent_point.png` (128x192, 8 frames, 12 fps, once): giant pointing finger wagging, and `parent_sigh.png` (128x192, 8 frames, 8 fps, once), a face-palm.
- `parent_speech_yell.png`, `parent_speech_sigh.png`: 192x96 speech bubbles with a jagged shout tail. Leave the text area empty (the game writes text).

### 4. Floor clutter (static sprites, placed at random on top of the floor, bottom-anchored)

Deliver `deco_*.png` as individual files or one sheet with a manifest of rects. Sizes 24-96px wide: a sock, a cereal bowl with spilled cereal, a toy car, a game controller with a cord, a single sneaker, a juice box, a crayon pile, a marble, a pizza slice on a paper plate, a slime puddle, a pencil, a bouncy ball, and coins (non-interactive, decor only). At least **20 distinct pieces.** Each has a matching `_shadow.png` (hard-banded 1-bit ellipse, 2 px offset).

### 5. Ambient particle sprites (white or light tint, the game recolors them)

| File | Frame size | Frames | fps |
|---|---|---|---|
| `fx_mote.png` | 8x8 | 6 | 8 (dust mote drifting in light) |
| `fx_fluff.png` | 16x16 | 6 | 8 (floating fluff/feather) |
| `fx_firefly.png` | 12x12 | 8 | 10 (soft blink) |
| `fx_steam.png` | 24x24 | 8 | 10 |
| `fx_sweat.png` | 12x12 | 4 | 14 (sweat drop) |
| `fx_heart.png` | 16x16 | 6 | 12 |
| `fx_sleepz.png` | 16x16 | 8 | 6 (Zzz rising from the cat) |
| `fx_shockwave.png` | 128x64 | 6 | 24 (ground ring on hard landings) |
| `fx_confetti.png` | 16x16 | 10 | 16 (level clear) |
| `fx_text_oof.png`, `fx_text_yikes.png`, `fx_text_nice.png`, `fx_text_whoops.png` | 96x48 | 6 each | 18 (comic text pop, hard outline) |

### 6. Light overlays (the game draws these additive/screen over the scene; hard-banded alpha, no smooth gradients)

- `light_window.png`: 384x540, a slanted moonlight shaft from the window, three alpha bands, soft-edged by banding.
- `light_lamp.png`: 256x256, round lamp glow, four bands.
- `light_vignette.png`: 960x540 corner darkening, six bands.
- `light_godray_anim.png`: 384x540 per frame, 6 frames, 4 fps, the shaft with slowly drifting dust pockets.
- **Normal maps** (optional but very valuable, Godot 2D lights use them): `tileset_floor_n.png`, `toy_blocks_n.png`, and `p1_idle_n.png`, `p1_run_n.png` with the same frame layout as their color sheets. Standard OpenGL-style tangent-space normal maps, generated from a height map of the pixel art.

### 7. UI life

- `ui_*` redone at 2x with bevels and wood/toy-box materials (see the table).
- `ui_logo.png`: 384x144, the title "YOUNGER SIBLING SIMULATOR" in a chunky toy-block letter style with a small hand poking in.
- `ui_button.png`: 192x48, 3 frames (idle, hover, pressed).
- `ui_banner_clear.png`, `ui_banner_grounded.png`: 384x96 banners, 6 frames each at 12 fps, for the end screens (confetti burst and a stern grounded stamp).
- `font_pixel.png`: a 10x14 bitmap font, ASCII 32-126 in a 16x6 grid, with the width of each glyph in `font_pixel.json`. Include a second `font_pixel_small.png` at 6x9.

## Delivery checklist

- [ ] Every v1 file name is present in `art/v2/` at the new size, redrawn (not upscaled).
- [ ] New files from Part B are present and listed in `manifest.json`.
- [ ] `palette.png` has at most 64 colors and every pixel in every file comes from it (run `tools/verify_art.py`, updated for the v2 sizes).
- [ ] Zoom to 800% on a run frame, a trip frame, and a tile: no blurred pixels, no stray single-pixel noise, feet on the bottom edge.
- [ ] Sheet width equals frames times frame width, for every file.
- [ ] Spot check P1 at 1x on a bright and a dark background. The silhouette must read instantly.
- [ ] Finish by telling Claude the list of new filenames so the game can be wired for them.
