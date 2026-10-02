# Younger Sibling Simulator: Art Brief

Paste this whole file to the art agent (Gemini in T3 Code). Deliver PNGs into `art/incoming/` in the project root, using the exact filenames below. Claude will wire them into Godot afterward.

## The game in one paragraph

A 2D side-scrolling platformer. Player 1 (an older sibling, about 10 years old) auto-runs through a giant kid's bedroom: floor is wood planks, obstacles are stacked toy blocks, pits are gaps in the floor. The player is Player 2, a disembodied kid's hand that drops power-ups from the top of the screen. Drop them at the wrong moment and P1 trips and the parent yells. Tone: warm, cozy, cartoony, a little chaotic. Think Celeste or Kirby's Dream Land meets a Pixar bedroom at dusk.

## Hard technical rules (do not break these)

1. **True pixel art.** No anti-aliasing, no blur, no sub-pixel gradients, no semi-transparent edge pixels. Every pixel is fully opaque or fully transparent (exception: glow sprites, noted below).
2. **Native scale.** The game renders at 480x270 and scales up by whole numbers. One art pixel is one game pixel. Do not draw big and downscale. If your image tool can't hit a pixel grid exactly, generate the sprite with a Python (Pillow) script from hand-written pixel arrays, or generate large and post-process with nearest-neighbor downscale plus palette quantization, and check that the result is crisp.
3. **Palette.** One shared palette of at most 32 colors for all assets. Deliver `palette.png` (one pixel per color, in a strip) first, and reuse it everywhere. Warm dusk tones: deep purples and indigos in shadow, warm wood browns and oranges in light, saturated toy colors (red `#e64848`, blue `#4d99f2`, yellow `#f2cc40`, green `#66cc73`) as accents. Use 3 to 5 tone ramps with hue shifting (shadows lean purple, highlights lean yellow).
4. **Lighting.** Light comes from the upper left (a window and a warm lamp). Every sprite gets a 1px darker rim on the bottom-right and a 1px lighter rim on the top-left. Add a 1px dark selective outline (not pure black; use the darkest palette purple).
5. **Transparent background** on every sprite. Spritesheets are horizontal strips with frames left to right and no padding between frames.
6. **Anchor.** For character sprites the feet touch the bottom edge of the frame and the body is centered horizontally. This matters: the game places the frame by its bottom-center.
7. **Animation feel: high fps, lots of juice.** Smooth, overlapping animation with anticipation, follow-through, and squash and stretch baked into the frames. Frame counts are listed below. The game plays them at the listed fps.

## Deliverables

### 1. Player 1: `p1_*.png` (frame size **32x32**, character is about 20px tall and 10px wide, centered)

Design: a scrappy older kid. Red hoodie or tee, blue shorts, sneakers with a bright white toe, messy brown hair with one cowlick, big readable eyes (2px), a determined grin. The silhouette must read instantly at 1x. Cape-free, no hat.

| File | Frames | FPS | Notes |
|---|---|---|---|
| `p1_idle.png` | 6 | 8 | Breathing, hair bob, looks around. Used when waiting for help. |
| `p1_wait.png` | 8 | 10 | Impatient: tapping foot, arms crossed, looks up at the hand, checks a pretend watch. The "needs an item" pose. |
| `p1_run.png` | 10 | 20 | Full run cycle with a 2-frame airborne phase, arms pumping, hair streaming, subtle body bob. Loops seamlessly. |
| `p1_run_fast.png` | 8 | 24 | Same character but leaning forward, exaggerated stride, motion smear on legs. Used with speed boots. |
| `p1_jump_up.png` | 3 | 14 | Anticipation crouch, launch stretch, rising pose. Plays once. |
| `p1_jump_apex.png` | 2 | 8 | Hang time at the top, tucked knees. Loops. |
| `p1_fall.png` | 3 | 12 | Descending, arms up, legs reaching for the ground. Loops. |
| `p1_land.png` | 4 | 24 | Squash, dust-kick pose, recover to standing. Plays once. |
| `p1_trip.png` | 10 | 20 | The big comedy beat: toe catches, arms windmill, faceplant, small bounce, stars circle the head, then peels off the ground and gets up. Plays once, about 0.5s. Include the "sprawled flat" pose held for 2 frames. |
| `p1_boost_jump.png` | 4 | 14 | Feather-powered jump: extra stretch, tiny sparkles trailing. |
| `p1_celebrate.png` | 8 | 12 | Victory: fist pump, hop, grin. Loops. |

### 2. Player 2 hand: `hand_*.png` (frame size **32x32**, origin at the center of the palm)

A kid's hand seen from the side, pointing down, cartoony and slightly oversized, with a pale sleeve cuff at the top edge. Skin tone should be neutral and warm, not tied to a specific ethnicity. The gesture must be readable at 1x.

| File | Frames | FPS | Notes |
|---|---|---|---|
| `hand_idle.png` | 6 | 8 | Open hand hovering, fingers gently wiggling. |
| `hand_hold.png` | 4 | 10 | Pinching a spot below the palm where the item sits (leave the pinch point clear, the game draws the item there). |
| `hand_drop.png` | 5 | 24 | Release: squeeze, snap open, motion lines. Plays once. |
| `hand_cooldown.png` | 4 | 6 | Hand tired or shaking out fingers while the cooldown recharges. |

### 3. Power-up items: `item_*.png` (frame size **24x24**, centered)

Each item has a 6-frame idle loop (fps 8): a bobbing float, a glint sweep across the surface, and a soft pulse. Also each gets a 3-frame pickup pop (`item_*_pop.png`, fps 24) that expands into a small starburst.

- `item_boots.png` and `item_boots_pop.png`: chunky orange running shoes with lightning-bolt stripes and little wing details.
- `item_feather.png` and `item_feather_pop.png`: a big cyan-white feather with a golden quill, a slight curl.
- `item_coin.png` and `item_coin_pop.png`: a gold coin, spins around its vertical axis (a real 6-frame spin, edge-on frame included), embossed star.

Glow: also deliver `item_glow.png`, a 32x32 soft circular glow using 4 hard-edged concentric bands (no smooth gradient, keep it pixel art), white on transparent, which the game tints.

### 4. Environment tiles: 16x16 grid

- `tileset_floor.png`: a wood-plank bedroom floor tileset, 8 tiles wide by 3 tall. Top row: floor surface tiles (flat, left edge, right edge, inner variants; a lit top lip 2px tall with wood grain below). Middle and bottom rows: fill tiles that extend downward into darkness (grain, nail heads, a couple of dropped pennies, a crayon, and a stray LEGO stud as rare decoration variants). Edges facing a pit should show the plank thickness and a dark shadow.
- `toy_blocks.png`: 16x16 stackable alphabet toy blocks. 4 colors (red, blue, yellow, green), 3 variants each (letter A, letter B, star), laid out 4 columns by 3 rows. Bright bevels, a big letter on the face.
- `goal_flag.png`: a 32x64 toy pennant flag on a pencil pole. 6 frames of flapping, fps 10.
- `pit_bg.png`: a 16x64 strip that tiles horizontally, showing the dark space under the floor (dust bunnies, a lost sock, faint glowing eyes far down). Very dark, low contrast, purple-black.

### 5. Parallax backgrounds (each tiles horizontally, height **270**)

- `bg_far.png`: **480x270**. Bedroom wall: wallpaper with a soft pattern, a large window with a crescent moon and stars (twinkle can be a second file `bg_far_stars.png`, 4 frames, fps 3), a framed crayon drawing, a poster. Cool blue-purple, lowest contrast.
- `bg_mid.png`: **640x270**. Bookshelves stuffed with colorful spines, a lamp giving a warm glow, a bed edge, a toy chest. Mid-tone. Seamless on the left and right edges.
- `bg_near.png`: **480x270**, transparent above the floor line at y=200. Dark silhouetted foreground toys: a teddy bear, a toy train, block towers, a rocking horse. The darkest layer, but keep rim-light on edges.
- `bg_sky_gradient.png`: **1x270** vertical strip, dusk purple at the top shifting to warm plum at the bottom, in 8 hard color bands (no smooth blending).

### 6. Effects (all 1-bit style white on transparent so the game can tint them)

Frame sizes and fps listed per file, each in a horizontal strip:

- `fx_dust.png`: 16x16, 6 frames, fps 20 (landing and jump puff)
- `fx_jump_puff.png`: 16x16, 5 frames, fps 24
- `fx_stars.png`: 24x24, 8 frames, fps 16 (circling stars for a trip)
- `fx_impact.png`: 32x32, 5 frames, fps 30 (comic "bang" burst for hitstop frames)
- `fx_speedline.png`: 24x8, 4 frames, fps 30
- `fx_sparkle.png`: 8x8, 5 frames, fps 16
- `fx_bubble.png`: 96x24, a speech bubble 9-slice with a tail at the bottom center, for "needs BOOTS!" (deliver as a single image, with the slice corners 6px)

### 7. UI (pixel-art skin for the HUD)

- `ui_trouble_pip.png`: 12x12, 2 frames (empty, full). The full state is a red angry-face icon.
- `ui_slot.png`: 52x28, 2 frames (idle, selected). A toy-box style slot with a bright selected border.
- `ui_cooldown_bar.png`: 160x6, 2 frames (empty track, filled).
- `ui_key_1.png`, `ui_key_2.png`, `ui_key_3.png`: 10x10 keycap icons.
- `font_pixel.png`: an optional 5x7 bitmap font sheet (ASCII 32-126), if easy. Otherwise skip and the game uses a pixel font from Google Fonts.

## Extra polish (nice to have, if time allows)

- Parent silhouette peeking through the door for the trouble screen: `parent_peek.png`, 64x96, 6 frames, fps 6, with a giant angry pointing finger.
- A second, brighter background palette variant for a later level (a backyard at golden hour): keep the same filenames with a `_yard` suffix.

## Delivery checklist (verify before you say you're done)

- [ ] All files are in `art/incoming/` with the exact names above.
- [ ] Every file is a PNG with transparency, using only palette colors.
- [ ] A spot check shows no blurred or anti-aliased pixels (zoom in at 800%).
- [ ] Frame counts and frame sizes match the tables so each sheet's width equals frames times frame width.
- [ ] Feet touch the bottom edge on every P1 frame, and the body doesn't jitter horizontally between run frames.
- [ ] Also write `art/incoming/manifest.json` listing each file with its `frame_w`, `frame_h`, `frames`, `fps`, and `loop` (true/false). Claude will read it to build the Godot `SpriteFrames` automatically.
