"""Younger Sibling Simulator - Environment & Obstacles Tiles Generator v2.

Elevated, high-fidelity pixel art for all v2 environment and obstacle assets:
- tileset_floor.png: 256x96 px (32x32 tiles, 8 cols x 3 rows).
  Row 0: Surface Planks: 16 plank variations across surface and decor.
         Visible wood grain, nail heads, scuffs, knots, wax shine on 2-3px top lip.
         Col 0: Standard surface plank (seamless horizontal wrap).
         Col 1: Butt joint seam with finishing nails.
         Col 2: Left cliff edge facing a pit (plank thickness, bevel, shadow).
         Col 3: Right cliff edge facing a pit (plank thickness, bevel, shadow).
         Col 4: Floor with shiny nail heads & scuffs.
         Col 5: Wood knot with swirling concentric grain and highlight rim.
         Col 6: Toy car scratch marks (parallel gouges exposing raw wood).
         Col 7: Dropped penny glint (metallic shading and specular gleam).
  Row 1: Mid-fill Joists/Studs: Heavy timber studs, dropped red crayon, blue LEGO stud, dropped coin.
  Row 2: Deep-fill Void: Deep gloom fade with cobwebs and dust motes.
- tileset_floor_rug.png: 256x96 px (32x32 tiles, 8 cols x 3 rows).
  Decorative woven bedroom rug with ornamental border pattern and fringe on ends.
- tileset_floor_carpet.png: 256x96 px (32x32 tiles, 8 cols x 3 rows).
  Fluffy bedroom carpet with tiny pixel fibers, soft pile texture, and warm dusk tone.
- toy_blocks.png: 128x96 px (32x32 tiles, 4 cols x 3 rows).
  4 vibrant colors: red (#e64848), blue (#4d99f2), yellow (#f2cc40), green (#66cc73).
  3 face variants: letter 'A', letter 'B', star '★'.
  3D toy block look: 2px bright highlight bevel top-left, 2px dark shadow bevel bottom-right,
  rounded corners, inset face with embossed letter and drop shadow.
- obstacle_books.png: 128x32 px (32x32 slices, 4 variants).
  Stack of colorful hardcover books (Blue, Red stack, Green textbook, Dusk tome).
- obstacle_box.png: 32x32 px.
  Cardboard box with packing tape and a "FRAGILE" red stamp.
- obstacle_jenga.png: 96x96 px (3 frames of 32x96, 3 heights in 32px steps).
  Wobbly Jenga wooden block tower in 3 precarious heights.
- obstacle_lego.png: 128x32 px (32x32 slices, 4 colors).
  LEGO brick stacks (red, blue, yellow, green) with studs on top.
- goal_flag.png: 384x128 px (64x128 per frame, 6 frames, 10 fps, loop: true).
  Yellow #2 pencil pole with silver ferrule, pink eraser top, and flapping red/yellow pennant with star.
- pit_bg.png: 32x128 px (tiles horizontally).
  Deep subfloor with dust bunnies, hanging striped tube sock, and mysterious glowing yellow eyes.
- tileset_floor_n.png (256x96 px) and toy_blocks_n.png (128x96 px):
  Normal maps generated from height maps using canvas.py.
"""

import os
import sys
import math
import json
from typing import List, Tuple
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from canvas import PixelCanvas, assemble_strip, generate_normal_map
from palette import (
    TRANSPARENT, OUTLINE,
    VOID_BLACK, SHADOW_PURPLE_DARK, SHADOW_DEEP, SHADOW_MID,
    PURPLE_DARK, PURPLE_MID, PURPLE_RICH, PURPLE_LIGHT,
    DUSK_LILAC, DUSK_PINK, DUSK_ROSE, DUSK_PEACH, DUSK_BLUSH, DUSK_CREAM,
    WOOD_BLACK, BROWN_DARKEST, BROWN_DARK, BROWN_MID, BROWN_LIGHT, WOOD_HIGHLIGHT, WOOD_LIT,
    RED_DEEP, RED_SHADOW, RED_RICH, RED_MID, RED_LIGHT, RED_HIGHLIGHT,
    BLUE_DEEP, BLUE_SHADOW, BLUE_RICH, BLUE_MID, BLUE_LIGHT, BLUE_HIGHLIGHT,
    YELLOW_DEEP, YELLOW_SHADOW, YELLOW_RICH, YELLOW_MID, YELLOW_LIGHT, YELLOW_HIGHLIGHT,
    GREEN_DEEP, GREEN_SHADOW, GREEN_RICH, GREEN_MID, GREEN_LIGHT, GREEN_HIGHLIGHT,
    ORANGE_DEEP, ORANGE_SHADOW, ORANGE_MID, ORANGE_LIGHT,
    TEAL_SHADOW, TEAL_MID, TEAL_LIGHT, TEAL_HIGHLIGHT,
    METAL_SHADOW, METAL_MID, WHITE_SHADOW, WHITE_MID, PURE_WHITE
)


# ==============================================================================
# 1. FLOOR TILESET: tileset_floor.png (256x96 px, 32x32 tiles, 8x3)
# ==============================================================================

def _generate_surface_base_v2() -> PixelCanvas:
    """Creates the base seamless 32x32 surface wood floor plank tile."""
    t = PixelCanvas(32, 32)

    # 1. 3px Wax shine & lit top lip (y=0..2)
    # y=0: Golden specular sheen rhythm
    for x in range(32):
        if x in [0, 1, 2, 7, 8, 9, 15, 16, 17, 24, 25, 26]:
            t.set_pixel(x, 0, YELLOW_HIGHLIGHT)
        elif x in [3, 6, 10, 14, 18, 23, 27, 31]:
            t.set_pixel(x, 0, YELLOW_LIGHT)
        else:
            t.set_pixel(x, 0, WOOD_LIT)

    # y=1: Bevel highlight transition
    for x in range(32):
        if x % 3 == 0:
            t.set_pixel(x, 1, WOOD_LIT)
        else:
            t.set_pixel(x, 1, WOOD_HIGHLIGHT)

    # y=2: Top plank shoulder bevel
    for x in range(32):
        if x % 4 == 0:
            t.set_pixel(x, 2, WOOD_HIGHLIGHT)
        else:
            t.set_pixel(x, 2, BROWN_LIGHT)

    # 2. Plank body (y=3..29) with natural undulating horizontal wood grain
    t.rect(0, 3, 32, 27, BROWN_MID)

    # Upper grain wave around y=7..9 (seamless sine wave)
    for x in range(32):
        dy = int(1.4 * math.sin(x * 2.0 * math.pi / 32.0))
        t.set_pixel(x, 8 + dy, BROWN_DARK)
        t.set_pixel(x, 7 + dy, BROWN_LIGHT)
        if dy <= 0:
            t.set_pixel(x, 6 + dy, WOOD_HIGHLIGHT)

    # Middle grain wave around y=15..17 (seamless cosine wave)
    for x in range(32):
        dy = int(1.6 * math.cos(x * 2.0 * math.pi / 32.0))
        t.set_pixel(x, 16 + dy, BROWN_DARK)
        t.set_pixel((x + 16) % 32, 15 + dy, BROWN_LIGHT)
        if dy >= 1:
            t.set_pixel(x, 17 + dy, BROWN_DARKEST)

    # Lower grain wave around y=23..25 (seamless shifted sine wave)
    for x in range(32):
        dy = int(1.3 * math.sin((x + 8) * 2.0 * math.pi / 32.0))
        t.set_pixel(x, 24 + dy, BROWN_DARK)
        t.set_pixel(x, 23 + dy, BROWN_LIGHT)
        if dy < 0:
            t.set_pixel(x, 25 + dy, BROWN_DARKEST)

    # Organic wood pore flecks (deterministic, seamless)
    pores = [
        (4, 5), (12, 11), (20, 4), (28, 12),
        (2, 19), (10, 21), (18, 19), (26, 20),
        (6, 27), (14, 28), (22, 27), (30, 28)
    ]
    for px, py in pores:
        t.set_pixel(px, py, BROWN_DARK)
        t.set_pixel(px + 1, py, BROWN_LIGHT)

    # 3. Plank bottom seam at y=30..31 (meeting subfloor)
    t.line(0, 30, 31, 30, BROWN_DARKEST)
    for x in range(32):
        if x % 2 == 1:
            t.set_pixel(x, 30, BROWN_DARK)
    t.line(0, 31, 31, 31, OUTLINE)
    for x in range(32):
        if x % 3 == 0:
            t.set_pixel(x, 31, BROWN_DARKEST)

    return t


def _generate_joist_base_v2() -> PixelCanvas:
    """Creates the base seamless 32x32 subfloor timber joist tile."""
    m = PixelCanvas(32, 32)

    # Dark horizontal seam separating surface plank from joists
    m.line(0, 0, 31, 0, OUTLINE)
    m.line(0, 1, 31, 1, WOOD_BLACK)
    m.line(0, 2, 31, 2, BROWN_DARKEST)

    # Timber body fill
    m.rect(0, 3, 32, 29, BROWN_DARK)

    # Recessed shadow cavity on sides (x=0..5 and x=26..31)
    for y in range(3, 32):
        m.set_pixel(0, y, SHADOW_PURPLE_DARK)
        m.set_pixel(1, y, SHADOW_DEEP)
        m.set_pixel(2, y, SHADOW_MID)
        m.set_pixel(3, y, BROWN_DARKEST)
        m.set_pixel(4, y, BROWN_DARKEST)
        m.set_pixel(5, y, BROWN_DARK)

        m.set_pixel(26, y, BROWN_DARK)
        m.set_pixel(27, y, BROWN_DARKEST)
        m.set_pixel(28, y, BROWN_DARKEST)
        m.set_pixel(29, y, SHADOW_MID)
        m.set_pixel(30, y, SHADOW_DEEP)
        m.set_pixel(31, y, SHADOW_PURPLE_DARK)

    # Central heavy timber vertical stud (x=6..25)
    # Left facet catches ambient bounce (x=6..10)
    for y in range(3, 32):
        m.set_pixel(6, y, BROWN_MID)
        m.set_pixel(7, y, BROWN_LIGHT if (y % 4 in [1, 2]) else BROWN_MID)
        m.set_pixel(8, y, WOOD_HIGHLIGHT if (y % 8 == 2) else BROWN_LIGHT)
        m.set_pixel(9, y, BROWN_MID)
        m.set_pixel(10, y, BROWN_MID)

    # Center vertical wood fibers & growth rings (x=11..20)
    for y in range(3, 32):
        m.set_pixel(11, y, BROWN_DARK)
        m.set_pixel(12, y, BROWN_DARKEST if (y % 3 != 0) else BROWN_DARK)
        m.set_pixel(13, y, BROWN_DARKEST)
        m.set_pixel(14, y, BROWN_DARK if (y % 5 == 0) else BROWN_DARKEST)
        m.set_pixel(15, y, BROWN_MID if (y % 6 in [1, 2]) else BROWN_DARK)
        m.set_pixel(16, y, BROWN_LIGHT if (y % 7 == 3) else BROWN_MID)
        m.set_pixel(17, y, BROWN_DARK)
        m.set_pixel(18, y, BROWN_DARKEST if (y % 4 != 0) else BROWN_DARK)
        m.set_pixel(19, y, BROWN_DARKEST)
        m.set_pixel(20, y, BROWN_DARK)

    # Right facet in deep shadow (x=21..25)
    for y in range(3, 32):
        m.set_pixel(21, y, BROWN_DARK)
        m.set_pixel(22, y, BROWN_DARKEST)
        m.set_pixel(23, y, BROWN_DARKEST)
        m.set_pixel(24, y, OUTLINE if (y % 2 == 0) else BROWN_DARKEST)
        m.set_pixel(25, y, OUTLINE)

    return m


def generate_tileset_floor() -> PixelCanvas:
    """
    256x96 px (8 tiles wide x 3 tiles tall, 32x32 grid).
    Row 0: Surface tiles (Standard, Butt joint, Left pit edge, Right pit edge,
           Nails & Scuffs, Knot, Toy Car Scratches, Dropped Penny).
    Row 1: Mid-fill Joists/Studs (Timber joist, Knot variant, Left cliff, Right cliff,
           Dropped Red Crayon, Blue LEGO stud, Vintage Penny, Rustic Iron Nails).
    Row 2: Deep-fill Void (Deep purple-black fade with hanging cobwebs and dust motes).
    """
    sheet = PixelCanvas(256, 96, TRANSPARENT)

    # ================== ROW 0: SURFACE TILES ==================
    t0 = _generate_surface_base_v2()
    sheet.blit(t0, 0, 0)

    # Tile 1: Surface plank with vertical butt joint seam at x=16
    t1 = t0.clone()
    for y in range(3, 30):
        t1.set_pixel(15, y, BROWN_DARK)       # Shadow on left board edge
        t1.set_pixel(16, y, OUTLINE if y % 2 == 0 else BROWN_DARKEST)  # Cut seam
        t1.set_pixel(17, y, WOOD_HIGHLIGHT)  # Lit bevel on right board edge
        t1.set_pixel(18, y, WOOD_LIT if y % 3 == 0 else WOOD_HIGHLIGHT)

    # Countersunk finishing nails near board ends
    for nx, ny in [(10, 10), (22, 22)]:
        t1.rect(nx, ny, 3, 3, WHITE_SHADOW, outline=BROWN_DARKEST)
        t1.set_pixel(nx, ny, PURE_WHITE)
        t1.set_pixel(nx + 1, ny, WHITE_MID)
        t1.set_pixel(nx + 2, ny + 2, OUTLINE)
    sheet.blit(t1, 32, 0)

    # Tile 2: Left cliff edge facing a pit! (Plank thickness & shadow on left)
    t2 = t0.clone()
    # Crisp outer outline along left pit edge
    t2.line(0, 2, 0, 31, OUTLINE)
    # Beveled rounded top-left corner
    t2.set_pixel(0, 0, OUTLINE)
    t2.set_pixel(0, 1, OUTLINE)
    t2.set_pixel(1, 0, OUTLINE)
    t2.set_pixel(1, 1, YELLOW_LIGHT)
    t2.set_pixel(2, 0, YELLOW_HIGHLIGHT)
    t2.set_pixel(2, 1, WOOD_LIT)

    # Cut plank cross-section showing plank depth
    for y in range(2, 32):
        t2.set_pixel(1, y, WOOD_HIGHLIGHT if y < 4 else BROWN_DARKEST)
        t2.set_pixel(2, y, BROWN_DARK if y < 4 else BROWN_DARK)
        t2.set_pixel(3, y, BROWN_MID)
    # Shadow cast downward into pit
    t2.set_pixel(0, 30, OUTLINE)
    t2.set_pixel(0, 31, OUTLINE)
    t2.set_pixel(1, 31, SHADOW_DEEP)
    sheet.blit(t2, 64, 0)

    # Tile 3: Right cliff edge facing a pit! (Plank thickness & shadow on right)
    t3 = t0.clone()
    # Crisp outer outline along right pit edge
    t3.line(31, 2, 31, 31, OUTLINE)
    # Beveled rounded top-right corner
    t3.set_pixel(31, 0, OUTLINE)
    t3.set_pixel(31, 1, OUTLINE)
    t3.set_pixel(30, 0, OUTLINE)
    t3.set_pixel(30, 1, WOOD_HIGHLIGHT)
    t3.set_pixel(29, 0, WOOD_LIT)

    # Vertical shadow on right edge
    for y in range(2, 32):
        t3.set_pixel(30, y, SHADOW_DEEP if y > 3 else WOOD_HIGHLIGHT)
        t3.set_pixel(29, y, BROWN_DARKEST)
        t3.set_pixel(28, y, BROWN_DARK)
    sheet.blit(t3, 96, 0)

    # Tile 4: Surface plank with pairs of shiny nail heads & scuffs
    t4 = t0.clone()
    nails = [(8, 11), (23, 20)]
    for nx, ny in nails:
        # Nail indent cavity
        t4.rect(nx - 1, ny - 1, 4, 4, BROWN_DARKEST)
        # Metallic head
        t4.set_pixel(nx, ny, PURE_WHITE)
        t4.set_pixel(nx + 1, ny, WHITE_MID)
        t4.set_pixel(nx, ny + 1, WHITE_SHADOW)
        t4.set_pixel(nx + 1, ny + 1, METAL_MID)
        t4.set_pixel(nx + 2, ny + 2, OUTLINE)

    # Scuff marks (pale scratched wax)
    scuffs = [(12, 7), (13, 7), (14, 8), (15, 8), (17, 16), (18, 16), (19, 17)]
    for sx, sy in scuffs:
        t4.set_pixel(sx, sy, WOOD_HIGHLIGHT)
    sheet.blit(t4, 128, 0)

    # Tile 5: Surface plank with wood knot
    t5 = t0.clone()
    # Wood knot core at (16, 16)
    t5.circle(16, 16, 3, BROWN_DARKEST, outline=OUTLINE)
    t5.set_pixel(16, 16, WOOD_BLACK)
    t5.set_pixel(15, 16, BROWN_DARKEST)

    # Swirling inner ring
    t5.circle(16, 16, 5, BROWN_DARK, outline=BROWN_DARKEST)
    # Highlight rim curling on upper-left of knot
    for kx, ky in [(11, 13), (12, 12), (13, 11), (14, 11), (15, 11), (16, 11), (11, 14), (11, 15)]:
        t5.set_pixel(kx, ky, WOOD_HIGHLIGHT)
    t5.set_pixel(13, 12, WOOD_LIT)
    t5.set_pixel(14, 12, WOOD_LIT)

    # Outer grain flow parting around knot
    for x in range(8, 25):
        t5.set_pixel(x, 9, BROWN_DARK)
        t5.set_pixel(x, 23, BROWN_DARK)
    sheet.blit(t5, 160, 0)

    # Tile 6: Surface plank with toy car scratch marks
    t6 = t0.clone()
    # Scratch track 1 (gouged wood revealing raw inner grain + shadow groove)
    scratch1 = [
        (6, 8), (7, 8), (8, 9), (9, 9), (10, 10), (11, 10), (12, 11),
        (13, 11), (14, 12), (15, 12), (16, 13), (17, 13), (18, 14),
        (19, 14), (20, 15), (21, 15), (22, 16), (23, 16)
    ]
    for sx, sy in scratch1:
        t6.set_pixel(sx, sy, YELLOW_LIGHT if (sx + sy) % 3 == 0 else WOOD_LIT)
        t6.set_pixel(sx, sy + 1, BROWN_DARKEST)

    # Parallel scratch track 2 (from other wheel of toy car)
    scratch2 = [
        (8, 15), (9, 15), (10, 16), (11, 16), (12, 17), (13, 17), (14, 18),
        (15, 18), (16, 19), (17, 19), (18, 20), (19, 20), (20, 21),
        (21, 21), (22, 22), (23, 22), (24, 23), (25, 23)
    ]
    for sx, sy in scratch2:
        t6.set_pixel(sx, sy, WOOD_HIGHLIGHT)
        t6.set_pixel(sx, sy + 1, BROWN_DARKEST)
    sheet.blit(t6, 192, 0)

    # Tile 7: Surface plank with dropped penny glint
    t7 = t0.clone()
    # 8x8 circular coin centered at (16, 16)
    t7.circle(16, 16, 4, YELLOW_MID, outline=YELLOW_SHADOW)
    t7.set_pixel(14, 14, PURE_WHITE)     # Specular gleam!
    t7.set_pixel(15, 14, YELLOW_LIGHT)
    t7.set_pixel(14, 15, YELLOW_LIGHT)
    t7.set_pixel(15, 15, YELLOW_MID)
    t7.set_pixel(17, 17, YELLOW_RICH)
    t7.set_pixel(18, 17, YELLOW_SHADOW)
    t7.set_pixel(17, 18, YELLOW_SHADOW)
    t7.set_pixel(18, 18, BROWN_DARKEST)
    # Cast shadow beneath coin on plank
    t7.line(13, 21, 20, 21, BROWN_DARKEST)
    t7.line(14, 22, 19, 22, OUTLINE)
    sheet.blit(t7, 224, 0)

    # ================== ROW 1: MID FILL TILES ==================
    m0 = _generate_joist_base_v2()
    sheet.blit(m0, 0, 32)

    # Tile 1: Rich dark wood grain stud variant with wood knot & split crack
    m1 = m0.clone()
    m1.circle(16, 15, 4, BROWN_DARK, outline=BROWN_DARKEST)
    m1.set_pixel(16, 15, WOOD_BLACK)
    m1.set_pixel(15, 14, WOOD_HIGHLIGHT)
    # Vertical stress crack
    for cy in range(19, 29):
        m1.set_pixel(16, cy, WOOD_BLACK if cy % 2 == 0 else BROWN_DARKEST)
        m1.set_pixel(17, cy, BROWN_DARK)
    sheet.blit(m1, 32, 32)

    # Tile 2: Left cliff edge facing pit
    m2 = m0.clone()
    m2.line(0, 0, 0, 31, OUTLINE)
    m2.line(1, 0, 1, 31, SHADOW_PURPLE_DARK)
    m2.line(2, 0, 2, 31, SHADOW_DEEP)
    m2.line(3, 0, 3, 31, BROWN_DARKEST)
    sheet.blit(m2, 64, 32)

    # Tile 3: Right cliff edge facing pit
    m3 = m0.clone()
    m3.line(31, 0, 31, 31, OUTLINE)
    m3.line(30, 0, 30, 31, SHADOW_PURPLE_DARK)
    m3.line(29, 0, 29, 31, SHADOW_DEEP)
    m3.line(28, 0, 28, 31, BROWN_DARKEST)
    sheet.blit(m3, 96, 32)

    # Tile 4: Wood fill with dropped RED CRAYON jammed in seam!
    m4 = m0.clone()
    # Recessed shadow cavity behind crayon
    m4.rect(3, 11, 26, 11, BROWN_DARKEST)
    m4.line(3, 22, 28, 22, OUTLINE)

    # Sharpened conical wax tip (x=4..7)
    m4.set_pixel(4, 16, OUTLINE)
    m4.set_pixel(5, 15, RED_LIGHT)
    m4.set_pixel(5, 16, RED_MID)
    m4.set_pixel(5, 17, RED_SHADOW)
    m4.set_pixel(6, 14, RED_LIGHT)
    m4.set_pixel(6, 15, RED_LIGHT)
    m4.set_pixel(6, 16, RED_MID)
    m4.set_pixel(6, 17, RED_SHADOW)
    m4.set_pixel(6, 18, RED_DEEP)
    m4.set_pixel(7, 13, RED_LIGHT)
    m4.set_pixel(7, 14, RED_LIGHT)
    m4.set_pixel(7, 15, RED_MID)
    m4.set_pixel(7, 16, RED_MID)
    m4.set_pixel(7, 17, RED_SHADOW)
    m4.set_pixel(7, 18, RED_DEEP)

    # Crayon cylindrical wax body (x=8..27, y=13..19)
    for cx in range(8, 28):
        m4.set_pixel(cx, 13, RED_LIGHT)    # Cylinder top highlight
        m4.set_pixel(cx, 14, RED_MID)
        m4.set_pixel(cx, 15, RED_MID)
        m4.set_pixel(cx, 16, RED_MID)
        m4.set_pixel(cx, 17, RED_SHADOW)
        m4.set_pixel(cx, 18, RED_DEEP)    # Cylinder bottom shadow
        m4.set_pixel(cx, 19, OUTLINE)

    # White paper label wrapper (x=13..23)
    for px in range(13, 24):
        m4.set_pixel(px, 13, PURE_WHITE)
        m4.set_pixel(px, 14, WHITE_MID)
        m4.set_pixel(px, 15, WHITE_SHADOW)
        m4.set_pixel(px, 16, WHITE_SHADOW)
        m4.set_pixel(px, 17, PURPLE_MID)
        m4.set_pixel(px, 18, PURPLE_DARK)

    # Crayon brand wavy logo band
    for wx in range(16, 21):
        m4.set_pixel(wx, 15, PURPLE_MID)
        m4.set_pixel(wx, 16, PURPLE_RICH)
    sheet.blit(m4, 128, 32)

    # Tile 5: Wood fill with stray BLUE LEGO BRICK / STUD!
    m5 = m0.clone()
    # Shadow under LEGO brick
    m5.line(7, 26, 25, 26, OUTLINE)
    m5.line(8, 27, 24, 27, SHADOW_DEEP)

    # 2x2 LEGO brick body (x=8..24, y=16..25)
    m5.rect(8, 16, 17, 10, BLUE_MID, outline=OUTLINE)
    # 3D bevels
    m5.line(9, 17, 23, 17, BLUE_LIGHT)    # Top edge
    m5.line(9, 18, 9, 24, BLUE_LIGHT)     # Left edge
    m5.line(23, 18, 23, 24, BLUE_SHADOW)  # Right edge
    m5.line(9, 24, 23, 24, BLUE_DEEP)     # Bottom edge

    # 2 Cylindrical studs on top (Stud 1: x=10..14, Stud 2: x=18..22, y=11..15)
    for sx in [10, 18]:
        m5.rect(sx, 11, 5, 5, BLUE_MID, outline=OUTLINE)
        m5.line(sx + 1, 12, sx + 3, 12, BLUE_LIGHT)
        m5.set_pixel(sx + 1, 12, PURE_WHITE)  # Specular gleam!
        m5.set_pixel(sx + 1, 13, BLUE_LIGHT)
        m5.set_pixel(sx + 3, 13, BLUE_SHADOW)
        m5.line(sx + 1, 14, sx + 3, 14, BLUE_SHADOW)
    sheet.blit(m5, 160, 32)

    # Tile 6: Wood fill with vintage penny wedged in seam
    m6 = m0.clone()
    # Knot cavity
    m6.circle(16, 16, 6, BROWN_DARKEST, outline=OUTLINE)
    # Wedge coin
    m6.circle(16, 16, 4, YELLOW_MID, outline=YELLOW_SHADOW)
    m6.set_pixel(14, 14, PURE_WHITE)
    m6.set_pixel(15, 14, YELLOW_LIGHT)
    m6.set_pixel(17, 17, YELLOW_SHADOW)
    m6.set_pixel(18, 18, BROWN_DARKEST)
    sheet.blit(m6, 192, 32)

    # Tile 7: Wood fill with rustic iron framing nails
    m7 = m0.clone()
    # Large nail at (12, 11)
    m7.rect(10, 9, 5, 5, WHITE_SHADOW, outline=OUTLINE)
    m7.set_pixel(10, 9, PURE_WHITE)
    m7.set_pixel(11, 10, WHITE_MID)
    m7.set_pixel(13, 12, METAL_SHADOW)
    m7.set_pixel(14, 13, SHADOW_DEEP)

    # Second nail at (21, 21)
    m7.rect(19, 19, 4, 4, WHITE_SHADOW, outline=OUTLINE)
    m7.set_pixel(19, 19, PURE_WHITE)
    m7.set_pixel(21, 21, METAL_SHADOW)
    sheet.blit(m7, 224, 32)

    # ================== ROW 2: DEEP FILL TILES ==================
    for col in range(8):
        b = PixelCanvas(32, 32)
        # Deep gloom vertical fade into void
        b.rect(0, 0, 32, 4, BROWN_DARKEST)
        b.rect(0, 4, 32, 5, SHADOW_PURPLE_DARK)
        b.rect(0, 9, 32, 6, SHADOW_DEEP)
        b.rect(0, 15, 32, 6, SHADOW_MID)
        b.rect(0, 21, 32, 5, OUTLINE)
        b.rect(0, 26, 32, 6, VOID_BLACK)

        # Fading timber stud ghosts
        for y in range(0, 16):
            b.set_pixel(7, y, BROWN_DARKEST if y < 6 else SHADOW_DEEP)
            b.set_pixel(8, y, BROWN_DARK if y < 4 else SHADOW_DEEP)
            b.set_pixel(23, y, BROWN_DARKEST if y < 6 else SHADOW_DEEP)
            b.set_pixel(24, y, OUTLINE)

        # Pit border edge shadows (col 2, 3)
        if col == 2:
            b.rect(0, 0, 3, 32, VOID_BLACK)
            b.line(3, 0, 3, 31, OUTLINE)
            b.line(4, 0, 4, 31, SHADOW_PURPLE_DARK)
        elif col == 3:
            b.rect(29, 0, 3, 32, VOID_BLACK)
            b.line(28, 0, 28, 31, OUTLINE)
            b.line(27, 0, 27, 31, SHADOW_PURPLE_DARK)
        elif col == 4:
            # Subtle hanging dust / cobweb strand
            b.line(31, 0, 24, 10, PURPLE_MID)
            b.line(24, 10, 20, 16, PURPLE_LIGHT)
            b.set_pixel(20, 16, WHITE_SHADOW)  # Caught dust speck
            b.set_pixel(19, 17, PURE_WHITE)
        elif col == 5:
            # Intricate corner cobweb spun in void
            # Primary anchor arc
            web_pts = [
                (0, 2), (2, 4), (5, 8), (9, 12), (14, 14),
                (19, 14), (24, 12), (28, 8), (30, 4), (31, 2)
            ]
            for wx, wy in web_pts:
                b.set_pixel(wx, wy, PURPLE_MID)
            # Secondary inner arc
            inner_web = [
                (0, 0), (4, 3), (8, 6), (12, 8), (16, 9),
                (20, 8), (24, 6), (28, 3), (31, 0)
            ]
            for wx, wy in inner_web:
                b.set_pixel(wx, wy, PURPLE_LIGHT)
            # Radial web spokes
            b.line(0, 0, 16, 14, PURPLE_MID)
            b.line(31, 0, 16, 14, PURPLE_MID)
            b.line(16, 0, 16, 14, PURPLE_LIGHT)
            # Caught dust motes in web
            b.set_pixel(16, 14, PURE_WHITE)
            b.set_pixel(12, 8, WHITE_SHADOW)
            b.set_pixel(20, 8, WHITE_MID)
        elif col == 6:
            # Stray cobweb strand
            b.line(0, 2, 9, 11, PURPLE_MID)
            b.line(9, 11, 14, 18, PURPLE_LIGHT)
            b.set_pixel(14, 18, PURE_WHITE)
        elif col == 7:
            # Floating dust motes in void
            b.set_pixel(8, 14, PURPLE_LIGHT)
            b.set_pixel(9, 14, PURE_WHITE)
            b.set_pixel(22, 20, WHITE_SHADOW)
            b.set_pixel(23, 20, PURPLE_LIGHT)

        sheet.blit(b, col * 32, 64)

    return sheet


# ==============================================================================
# 2. RUG AND CARPET TILESETS (256x96 px each, 32x32 tiles, 8x3)
# ==============================================================================

def generate_tileset_floor_rug() -> PixelCanvas:
    """
    tileset_floor_rug.png: 256x96 px (8 columns x 3 rows of 32x32 tiles).
    Decorative woven bedroom rug with ornamental border pattern and fringe on ends.
    Teal ramp (#144747, #227878, #42b5ab, #82ebd9), Dusk Peach/Rose, Gold accents.
    """
    sheet = PixelCanvas(256, 96, TRANSPARENT)

    # Base repeating rug tile (Row 0, Col 0)
    def make_rug_base() -> PixelCanvas:
        r = PixelCanvas(32, 32)
        # Background floor plank visible at top y=0..1
        r.line(0, 0, 31, 0, BROWN_LIGHT)
        r.line(0, 1, 31, 1, BROWN_MID)

        # Rug top bound hem (y=2..3)
        r.line(0, 2, 31, 2, DUSK_CREAM)
        r.line(0, 3, 31, 3, TEAL_SHADOW)

        # Outer ornamental border band (y=4..7)
        r.rect(0, 4, 32, 4, TEAL_MID)
        for x in range(32):
            if x % 4 in [0, 1]:
                r.set_pixel(x, 5, TEAL_LIGHT)
                r.set_pixel(x, 6, DUSK_PEACH)
            else:
                r.set_pixel(x, 5, DUSK_ROSE)
                r.set_pixel(x, 6, TEAL_HIGHLIGHT)

        # Thin accent stripe (y=8)
        r.line(0, 8, 31, 8, YELLOW_MID)

        # Center woven diamond field (y=9..23)
        r.rect(0, 9, 32, 15, TEAL_SHADOW)
        for y in range(9, 24):
            for x in range(32):
                # Repeating geometric diamond grid
                dist = abs((x % 8) - 4) + abs(((y - 9) % 8) - 4)
                if dist == 4:
                    r.set_pixel(x, y, TEAL_LIGHT)
                elif dist == 3:
                    r.set_pixel(x, y, TEAL_MID)
                elif dist == 0:
                    r.set_pixel(x, y, YELLOW_LIGHT)
                elif dist == 1:
                    r.set_pixel(x, y, DUSK_PEACH)

        # Bottom accent stripe (y=24)
        r.line(0, 24, 31, 24, YELLOW_MID)

        # Bottom ornamental border band (y=25..28)
        r.rect(0, 25, 32, 4, TEAL_MID)
        for x in range(32):
            if x % 4 in [0, 1]:
                r.set_pixel(x, 26, TEAL_LIGHT)
                r.set_pixel(x, 27, DUSK_PEACH)
            else:
                r.set_pixel(x, 26, DUSK_ROSE)
                r.set_pixel(x, 27, TEAL_HIGHLIGHT)

        # Rug bottom bound hem (y=29)
        r.line(0, 29, 31, 29, DUSK_CREAM)
        # Drop shadow onto floor beneath rug (y=30..31)
        r.line(0, 30, 31, 30, BROWN_DARKEST)
        r.line(0, 31, 31, 31, BROWN_DARK)

        return r

    rug0 = make_rug_base()
    sheet.blit(rug0, 0, 0)

    # Col 1: Center medallion variant
    rug1 = rug0.clone()
    # Large 14x14 center medallion in diamond field
    med_cx, med_cy = 16, 16
    for y in range(med_cy - 6, med_cy + 7):
        for x in range(med_cx - 6, med_cx + 7):
            d = abs(x - med_cx) + abs(y - med_cy)
            if d == 6:
                rug1.set_pixel(x, y, YELLOW_MID)
            elif d == 5:
                rug1.set_pixel(x, y, DUSK_CREAM)
            elif d == 4:
                rug1.set_pixel(x, y, TEAL_HIGHLIGHT)
            elif d == 3:
                rug1.set_pixel(x, y, DUSK_ROSE)
            elif d == 2:
                rug1.set_pixel(x, y, TEAL_LIGHT)
            elif d <= 1:
                rug1.set_pixel(x, y, PURE_WHITE)
    sheet.blit(rug1, 32, 0)

    # Col 2: Left rug edge with ornamental border & fringe tassels!
    rug2 = rug0.clone()
    # Clear left side for floor + fringe tassels (x=0..9)
    for y in range(32):
        # Wood floor underneath
        rug2.set_pixel(0, y, BROWN_LIGHT if y < 4 else BROWN_MID)
        rug2.set_pixel(1, y, BROWN_MID)
        rug2.set_pixel(2, y, BROWN_MID)
        rug2.set_pixel(3, y, BROWN_MID)
        rug2.set_pixel(4, y, BROWN_MID)

    # Left vertical binding hem at x=8..9
    rug2.line(8, 2, 8, 29, TEAL_SHADOW)
    rug2.line(9, 2, 9, 29, DUSK_CREAM)

    # Ornamental left fringe tassels extending over floor (x=1..7)
    for ty in range(3, 29, 2):
        rug2.line(3, ty, 7, ty, DUSK_CREAM)
        rug2.set_pixel(2, ty, PURE_WHITE)
        rug2.set_pixel(1, ty, WHITE_SHADOW)
        rug2.set_pixel(4, ty + 1, BROWN_DARKEST)  # Tassel shadow on floor
    sheet.blit(rug2, 64, 0)

    # Col 3: Right rug edge with ornamental border & fringe tassels!
    rug3 = rug0.clone()
    for y in range(32):
        rug3.set_pixel(27, y, BROWN_MID)
        rug3.set_pixel(28, y, BROWN_MID)
        rug3.set_pixel(29, y, BROWN_MID)
        rug3.set_pixel(30, y, BROWN_MID)
        rug3.set_pixel(31, y, BROWN_LIGHT if y < 4 else BROWN_MID)

    # Right vertical binding hem at x=22..23
    rug3.line(22, 2, 22, 29, DUSK_CREAM)
    rug3.line(23, 2, 23, 29, TEAL_SHADOW)

    # Right fringe tassels extending over floor (x=24..30)
    for ty in range(3, 29, 2):
        rug3.line(24, ty, 28, ty, DUSK_CREAM)
        rug3.set_pixel(29, ty, PURE_WHITE)
        rug3.set_pixel(30, ty, WHITE_SHADOW)
        rug3.set_pixel(27, ty + 1, BROWN_DARKEST)
    sheet.blit(rug3, 96, 0)

    # Col 4: Rug with toy indentation (flattened pile dent)
    rug4 = rug0.clone()
    rug4.rect(10, 12, 12, 8, TEAL_SHADOW)
    rug4.line(10, 12, 21, 12, OUTLINE)
    rug4.line(10, 12, 10, 19, OUTLINE)
    rug4.line(10, 19, 21, 19, TEAL_MID)
    rug4.line(21, 12, 21, 19, TEAL_MID)
    sheet.blit(rug4, 128, 0)

    # Col 5: Rug with ornamental corner rosette / knot
    rug5 = rug0.clone()
    for rx, ry in [(16, 14), (16, 18), (14, 16), (18, 16)]:
        rug5.set_pixel(rx, ry, YELLOW_LIGHT)
    rug5.circle(16, 16, 2, DUSK_ROSE, outline=YELLOW_MID)
    rug5.set_pixel(16, 16, PURE_WHITE)
    sheet.blit(rug5, 160, 0)

    # Col 6: Rug with dropped shiny gold button / sequin
    rug6 = rug0.clone()
    rug6.circle(16, 16, 3, YELLOW_MID, outline=YELLOW_SHADOW)
    rug6.set_pixel(15, 15, PURE_WHITE)
    rug6.set_pixel(16, 15, YELLOW_LIGHT)
    rug6.set_pixel(17, 17, YELLOW_DEEP)
    rug6.line(14, 20, 18, 20, OUTLINE)
    sheet.blit(rug6, 192, 0)

    # Col 7: Rug with color band variation
    rug7 = rug0.clone()
    rug7.line(0, 16, 31, 16, DUSK_PEACH)
    rug7.line(0, 17, 31, 17, DUSK_ROSE)
    sheet.blit(rug7, 224, 0)

    # Row 1 & 2: Subfloor joists and void beneath rug
    floor_sheet = generate_tileset_floor()
    # Blit joists from floor_sheet Row 1 and void from Row 2
    for col in range(8):
        # Extract mid-fill
        mid = PixelCanvas(32, 32)
        for y in range(32):
            for x in range(32):
                mid.set_pixel(x, y, floor_sheet.get_pixel(col * 32 + x, 32 + y))
        sheet.blit(mid, col * 32, 32)

        # Extract deep-fill
        deep = PixelCanvas(32, 32)
        for y in range(32):
            for x in range(32):
                deep.set_pixel(x, y, floor_sheet.get_pixel(col * 32 + x, 64 + y))
        sheet.blit(deep, col * 32, 64)

    return sheet


def generate_tileset_floor_carpet() -> PixelCanvas:
    """
    tileset_floor_carpet.png: 256x96 px (8 columns x 3 rows of 32x32 tiles).
    Fluffy bedroom carpet with tiny pixel fibers, soft pile texture, and warm dusk tone.
    Palette: Dusk Lilac/Pink/Rose/Peach/Blush/Cream (#824d94..#f0c5d6), Purple Dark/Mid.
    """
    sheet = PixelCanvas(256, 96, TRANSPARENT)

    def make_carpet_base() -> PixelCanvas:
        c = PixelCanvas(32, 32)
        # Carpet body fill
        c.rect(0, 3, 32, 26, DUSK_ROSE)

        # 1. Fluffy pixel fiber top edge (y=0..3):
        # Organic tufts breaking the horizontal line
        for x in range(32):
            tuft_h = int(1.5 + 1.2 * math.sin(x * 1.7) + 0.8 * math.cos(x * 3.1))
            tuft_h = max(0, min(3, tuft_h))
            for y in range(3 - tuft_h, 4):
                if y == 3 - tuft_h:
                    c.set_pixel(x, y, DUSK_CREAM if (x % 2 == 0) else DUSK_BLUSH)
                elif y == 4 - tuft_h:
                    c.set_pixel(x, y, DUSK_PEACH)
                else:
                    c.set_pixel(x, y, DUSK_ROSE)

        # 2. Rich plush pile micro-texture (y=4..28)
        # Cluster loops and fiber curls
        for y in range(4, 29):
            for x in range(32):
                val = (x * 7 + y * 13 + ((x ^ y) * 3)) % 11
                if val == 0:
                    c.set_pixel(x, y, DUSK_CREAM)
                elif val in [1, 2]:
                    c.set_pixel(x, y, DUSK_BLUSH)
                elif val in [3, 4, 5]:
                    c.set_pixel(x, y, DUSK_PEACH)
                elif val in [6, 7]:
                    c.set_pixel(x, y, DUSK_ROSE)
                elif val in [8, 9]:
                    c.set_pixel(x, y, DUSK_PINK)
                else:
                    c.set_pixel(x, y, PURPLE_MID)  # Shadow crevice between yarn tufts

        # 3. Bottom underlay / foam padding seam (y=29..31)
        c.line(0, 29, 31, 29, DUSK_LILAC)
        c.line(0, 30, 31, 30, PURPLE_DARK)
        c.line(0, 31, 31, 31, OUTLINE)

        return c

    carp0 = make_carpet_base()
    sheet.blit(carp0, 0, 0)

    # Col 1: Vacuum track stripe / nap contrast
    carp1 = carp0.clone()
    for y in range(4, 29):
        # Diagonal brushed vacuum band (x=8..22)
        for x in range(32):
            if 8 <= (x + y // 3) % 32 <= 22:
                # Smoothed nap: catches brighter warm light
                px_color = carp1.get_pixel(x, y)
                if px_color == DUSK_ROSE:
                    carp1.set_pixel(x, y, DUSK_PEACH)
                elif px_color == DUSK_PEACH:
                    carp1.set_pixel(x, y, DUSK_BLUSH)
                elif px_color == DUSK_PINK:
                    carp1.set_pixel(x, y, DUSK_ROSE)
    sheet.blit(carp1, 32, 0)

    # Col 2: Left edge of carpet runner / transition
    carp2 = carp0.clone()
    # Left edge roll curve
    for y in range(32):
        carp2.set_pixel(0, y, OUTLINE if y > 2 else TRANSPARENT)
        carp2.set_pixel(1, y, PURPLE_MID if y > 1 else TRANSPARENT)
        carp2.set_pixel(2, y, DUSK_LILAC if y > 0 else TRANSPARENT)
        carp2.set_pixel(3, y, DUSK_ROSE)
        carp2.set_pixel(4, y, DUSK_PEACH)
        carp2.set_pixel(5, y, DUSK_BLUSH)
    sheet.blit(carp2, 64, 0)

    # Col 3: Right edge of carpet runner / transition
    carp3 = carp0.clone()
    for y in range(32):
        carp3.set_pixel(31, y, OUTLINE if y > 2 else TRANSPARENT)
        carp3.set_pixel(30, y, PURPLE_MID if y > 1 else TRANSPARENT)
        carp3.set_pixel(29, y, DUSK_LILAC if y > 0 else TRANSPARENT)
        carp3.set_pixel(28, y, DUSK_ROSE)
        carp3.set_pixel(27, y, DUSK_PEACH)
    sheet.blit(carp3, 96, 0)

    # Col 4: Flattened footprint / paw print indent
    carp4 = carp0.clone()
    # Cute little footprint indentation in plush fibers
    foot_pts = [
        (15, 14), (16, 14), (17, 14),
        (14, 15), (15, 15), (16, 15), (17, 15), (18, 15),
        (14, 16), (15, 16), (16, 16), (17, 16), (18, 16),
        (15, 17), (16, 17), (17, 17),
        (15, 18), (16, 18)
    ]
    for fx, fy in foot_pts:
        carp4.set_pixel(fx, fy, PURPLE_MID)
    # Toe indents
    for tx, ty in [(13, 12), (15, 11), (17, 11), (19, 12)]:
        carp4.set_pixel(tx, ty, PURPLE_DARK)
        carp4.set_pixel(tx, ty + 1, PURPLE_MID)
    sheet.blit(carp4, 128, 0)

    # Col 5: Dropped fuzz ball / lint tuft in carpet
    carp5 = carp0.clone()
    carp5.circle(16, 16, 3, WHITE_SHADOW, outline=DUSK_LILAC)
    carp5.set_pixel(15, 15, PURE_WHITE)
    carp5.set_pixel(16, 15, WHITE_MID)
    carp5.set_pixel(17, 17, PURPLE_MID)
    sheet.blit(carp5, 160, 0)

    # Col 6: Dropped colorful marble half-sunken in plush pile
    carp6 = carp0.clone()
    carp6.circle(16, 16, 4, BLUE_MID, outline=PURPLE_DARK)
    carp6.set_pixel(14, 14, PURE_WHITE)
    carp6.set_pixel(15, 14, BLUE_LIGHT)
    carp6.set_pixel(17, 17, BLUE_SHADOW)
    carp6.set_pixel(18, 18, BLUE_DEEP)
    sheet.blit(carp6, 192, 0)

    # Col 7: Swirled carpet pile
    carp7 = carp0.clone()
    for deg in range(0, 360, 15):
        rad = math.radians(deg)
        r = 3.0 + 4.0 * (deg / 360.0)
        sx = int(16 + r * math.cos(rad))
        sy = int(16 + r * math.sin(rad))
        if 0 <= sx < 32 and 0 <= sy < 32:
            carp7.set_pixel(sx, sy, DUSK_CREAM if deg % 30 == 0 else DUSK_BLUSH)
    sheet.blit(carp7, 224, 0)

    # Row 1 & 2: Subfloor joists and void beneath carpet
    floor_sheet = generate_tileset_floor()
    for col in range(8):
        mid = PixelCanvas(32, 32)
        for y in range(32):
            for x in range(32):
                mid.set_pixel(x, y, floor_sheet.get_pixel(col * 32 + x, 32 + y))
        sheet.blit(mid, col * 32, 32)

        deep = PixelCanvas(32, 32)
        for y in range(32):
            for x in range(32):
                deep.set_pixel(x, y, floor_sheet.get_pixel(col * 32 + x, 64 + y))
        sheet.blit(deep, col * 32, 64)

    return sheet


# ==============================================================================
# 3. TOY BLOCKS: toy_blocks.png (128x96 px, 32x32 tiles, 4x3)
# ==============================================================================

def generate_toy_blocks() -> PixelCanvas:
    """
    32x32 stackable alphabet toy blocks.
    4 vibrant colors (Red, Blue, Yellow, Green), 3 variants (Letter A, Letter B, Star ★).
    4 columns x 3 rows -> 128x96 px.
    Detailed 3D look: 2px bright bevel top-left, 2px dark bevel bottom-right,
    rounded corners, inset face with embossed letter and drop shadow.
    """
    sheet = PixelCanvas(128, 96, TRANSPARENT)

    # Color definitions:
    # (fill, highlight, shadow, deep_shadow, text_color, text_shadow, text_hi)
    colors = [
        # Red
        (RED_MID, RED_LIGHT, RED_SHADOW, RED_DEEP, PURE_WHITE, RED_DEEP, RED_HIGHLIGHT),
        # Blue
        (BLUE_MID, BLUE_LIGHT, BLUE_SHADOW, BLUE_DEEP, PURE_WHITE, BLUE_DEEP, BLUE_HIGHLIGHT),
        # Yellow: iconic RED embossed lettering!
        (YELLOW_MID, YELLOW_LIGHT, YELLOW_SHADOW, YELLOW_DEEP, RED_MID, YELLOW_DEEP, RED_LIGHT),
        # Green
        (GREEN_MID, GREEN_LIGHT, GREEN_SHADOW, GREEN_DEEP, PURE_WHITE, GREEN_DEEP, GREEN_HIGHLIGHT),
    ]

    for col_idx, (c_fill, c_hi, c_sh, c_deep, c_txt, c_tsh, c_thi) in enumerate(colors):
        for row_idx in range(3):
            b = PixelCanvas(32, 32, TRANSPARENT)

            # 1. Outer boundary with rounded friendly toy corners
            b.rect(2, 2, 28, 28, c_fill)

            # Perimeter selective outline
            b.line(2, 0, 29, 0, OUTLINE)    # Top
            b.line(2, 31, 29, 31, OUTLINE)  # Bottom
            b.line(0, 2, 0, 29, OUTLINE)    # Left
            b.line(31, 2, 31, 29, OUTLINE)  # Right

            # Clipped rounded corner outlines
            b.set_pixel(1, 1, OUTLINE)
            b.set_pixel(30, 1, OUTLINE)
            b.set_pixel(1, 30, OUTLINE)
            b.set_pixel(30, 30, OUTLINE)

            # 2. Outer 3D Bevel (Light from upper-left)
            # Top-left bright bevel (2px wide)
            b.line(3, 1, 28, 1, c_hi)
            b.line(2, 2, 28, 2, c_hi)
            b.line(1, 3, 1, 28, c_hi)
            b.line(2, 3, 2, 28, c_hi)
            # Specular gleam at top-left corner
            b.set_pixel(3, 3, PURE_WHITE)
            b.set_pixel(4, 3, PURE_WHITE)
            b.set_pixel(3, 4, PURE_WHITE)

            # Bottom-right dark bevel (2px wide)
            b.line(3, 30, 28, 30, c_deep)
            b.line(2, 29, 29, 29, c_sh)
            b.line(30, 3, 30, 28, c_deep)
            b.line(29, 2, 29, 29, c_sh)

            # 3. Inset / Recessed block face (x=5..26, y=5..26)
            # Inner shadow at top and left of recess (2px)
            b.line(5, 5, 26, 5, c_deep)
            b.line(5, 6, 25, 6, c_sh)
            b.line(5, 5, 5, 26, c_deep)
            b.line(6, 5, 6, 25, c_sh)

            # Inner highlight at bottom and right of recess (2px)
            b.line(5, 26, 26, 26, c_hi)
            b.line(6, 25, 26, 25, c_hi)
            b.line(26, 5, 26, 26, c_hi)
            b.line(25, 6, 25, 26, c_hi)

            # Recessed square field (x=7..24, y=7..24)
            b.rect(7, 7, 18, 18, c_fill)

            # 4. Embossed Symbol with 3D Drop Shadow inside the recess
            if row_idx == 0:
                # ================= Letter 'A' (High-res 32x32) =================
                a_pts = [
                    # Apex
                    (15, 9), (16, 9),
                    (14, 10), (15, 10), (16, 10), (17, 10),
                    # Upper legs
                    (13, 11), (14, 11), (17, 11), (18, 11),
                    (12, 12), (13, 12), (18, 12), (19, 12),
                    (12, 13), (13, 13), (18, 13), (19, 13),
                    (11, 14), (12, 14), (19, 14), (20, 14),
                    # Crossbar
                    (11, 15), (12, 15), (13, 15), (14, 15), (15, 15),
                    (16, 15), (17, 15), (18, 15), (19, 15), (20, 15),
                    (10, 16), (11, 16), (12, 16), (13, 16), (14, 16),
                    (15, 16), (16, 16), (17, 16), (18, 16), (19, 16), (20, 16), (21, 16),
                    # Lower legs
                    (10, 17), (11, 17), (20, 17), (21, 17),
                    (9, 18), (10, 18), (21, 18), (22, 18),
                    (9, 19), (10, 19), (21, 19), (22, 19),
                    (8, 20), (9, 20), (10, 20), (21, 20), (22, 20), (23, 20),
                    # Flared feet
                    (8, 21), (9, 21), (10, 21), (11, 21), (20, 21), (21, 21), (22, 21), (23, 21),
                    (7, 22), (8, 22), (9, 22), (10, 22), (21, 22), (22, 22), (23, 22), (24, 22),
                ]
                # Drop shadow (+1, +1)
                for sx, sy in a_pts:
                    if sx + 1 <= 24 and sy + 1 <= 24:
                        b.set_pixel(sx + 1, sy + 1, c_tsh)
                # Symbol body
                for sx, sy in a_pts:
                    b.set_pixel(sx, sy, c_txt)
                # Top-left highlight rim
                for hx, hy in [(15, 9), (16, 9), (14, 10), (13, 11), (12, 12), (11, 15), (12, 15)]:
                    b.set_pixel(hx, hy, c_thi)

            elif row_idx == 1:
                # ================= Letter 'B' (High-res 32x32) =================
                b_pts = [
                    # Vertical spine
                    (9, 9), (10, 9), (11, 9), (12, 9), (13, 9), (14, 9), (15, 9), (16, 9), (17, 9), (18, 9),
                    (9, 10), (10, 10), (11, 10), (12, 10),                                (18, 10), (19, 10),
                    (9, 11), (10, 11), (11, 11), (12, 11),                                (19, 11), (20, 11),
                    (9, 12), (10, 12), (11, 12), (12, 12),                                (19, 12), (20, 12),
                    (9, 13), (10, 13), (11, 13), (12, 13),                                (18, 13), (19, 13),
                    # Center waist bar
                    (9, 14), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14), (15, 14), (16, 14), (17, 14), (18, 14),
                    (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15),
                    # Bottom bowl
                    (9, 16), (10, 16), (11, 16), (12, 16),                                          (19, 16), (20, 16),
                    (9, 17), (10, 17), (11, 17), (12, 17),                                          (20, 17), (21, 17),
                    (9, 18), (10, 18), (11, 18), (12, 18),                                          (20, 18), (21, 18),
                    (9, 19), (10, 19), (11, 19), (12, 19),                                          (20, 19), (21, 19),
                    (9, 20), (10, 20), (11, 20), (12, 20),                                (19, 20), (20, 20),
                    (9, 21), (10, 21), (11, 21), (12, 21), (13, 21), (14, 21), (15, 21), (16, 21), (17, 21), (18, 21), (19, 21),
                    (8, 22), (9, 22), (10, 22), (11, 22), (12, 22), (13, 22), (14, 22), (15, 22), (16, 22), (17, 22), (18, 22),
                ]
                # Drop shadow (+1, +1)
                for sx, sy in b_pts:
                    if sx + 1 <= 24 and sy + 1 <= 24:
                        b.set_pixel(sx + 1, sy + 1, c_tsh)
                # Symbol body
                for sx, sy in b_pts:
                    b.set_pixel(sx, sy, c_txt)
                # Highlight on top edges
                for hx, hy in [(9, 9), (10, 9), (11, 9), (12, 9), (13, 9), (14, 9), (15, 9), (16, 9), (17, 9), (9, 10), (9, 11)]:
                    b.set_pixel(hx, hy, c_thi)

            else:
                # ================= Star '★' (High-res 32x32) =================
                star_pts = [
                    # Top point
                    (15, 8), (16, 8),
                    (15, 9), (16, 9),
                    (14, 10), (15, 10), (16, 10), (17, 10),
                    (14, 11), (15, 11), (16, 11), (17, 11),
                    (13, 12), (14, 12), (15, 12), (16, 12), (17, 12), (18, 12),
                    # Horizontal arms
                    (8, 13), (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13),
                    (15, 13), (16, 13), (17, 13), (18, 13), (19, 13), (20, 13), (21, 13), (22, 13), (23, 13),
                    (9, 14), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14),
                    (15, 14), (16, 14), (17, 14), (18, 14), (19, 14), (20, 14), (21, 14), (22, 14),
                    (10, 15), (11, 15), (12, 15), (13, 15), (14, 15),
                    (15, 15), (16, 15), (17, 15), (18, 15), (19, 15), (20, 15), (21, 15),
                    # Center & waist
                    (11, 16), (12, 16), (13, 16), (14, 16), (15, 16), (16, 16), (17, 16), (18, 16), (19, 16), (20, 16),
                    (12, 17), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (19, 17),
                    # Lower legs
                    (11, 18), (12, 18), (13, 18), (14, 18), (17, 18), (18, 18), (19, 18), (20, 18),
                    (10, 19), (11, 19), (12, 19), (13, 19), (18, 19), (19, 19), (20, 19), (21, 19),
                    (9, 20), (10, 20), (11, 20), (12, 20), (19, 20), (20, 20), (21, 20), (22, 20),
                    (9, 21), (10, 21), (11, 21), (20, 21), (21, 21), (22, 21),
                    (8, 22), (9, 22), (10, 22), (21, 22), (22, 22), (23, 22),
                ]
                # Drop shadow (+1, +1)
                for sx, sy in star_pts:
                    if sx + 1 <= 24 and sy + 1 <= 24:
                        b.set_pixel(sx + 1, sy + 1, c_tsh)
                # Symbol body
                for sx, sy in star_pts:
                    b.set_pixel(sx, sy, c_txt)
                # Center glint
                b.set_pixel(15, 8, c_thi)
                b.set_pixel(16, 8, c_thi)
                b.set_pixel(15, 14, c_thi)
                b.set_pixel(16, 14, c_thi)

            sheet.blit(b, col_idx * 32, row_idx * 32)

    return sheet


# ==============================================================================
# 4. NEW OBSTACLES (32px grid stacking)
# ==============================================================================

def generate_obstacle_books() -> PixelCanvas:
    """
    obstacle_books.png: 128x32 px (4 slices of 32x32).
    Stack of colorful hardcover books:
    - Slice 0: Navy Blue hardcover book with gold foil title and ribbon bookmark.
    - Slice 1: Crimson Red double book stack (red encyclopedia + yellow novel).
    - Slice 2: Emerald Green textbook with decorative spine bands.
    - Slice 3: Dusk/Purple grimoire with brass corner brackets.
    """
    sheet = PixelCanvas(128, 32, TRANSPARENT)

    # ---------------- Slice 0: Navy Blue Hardcover Book ----------------
    s0 = PixelCanvas(32, 32)
    # Book body (x=2..29, y=10..30)
    # Book cover outline
    s0.rect(2, 10, 28, 21, BLUE_MID, outline=OUTLINE)
    # Left spine (x=2..7)
    s0.rect(2, 10, 6, 21, BLUE_DEEP, outline=OUTLINE)
    s0.line(3, 11, 3, 29, BLUE_MID)
    # Gold foil spine bands
    for gy in [13, 14, 21, 22, 27]:
        s0.line(3, gy, 6, gy, YELLOW_MID)
        s0.set_pixel(3, gy, YELLOW_LIGHT)
    # Paper pages block (x=8..28, y=13..27)
    s0.rect(8, 13, 21, 15, WHITE_SHADOW, outline=METAL_SHADOW)
    for py in range(14, 28, 2):
        s0.line(9, py, 27, py, WHITE_MID)
    # Silk ribbon bookmark dangling out (x=18..20, y=20..31)
    s0.line(18, 20, 18, 29, RED_MID)
    s0.line(19, 21, 19, 31, RED_LIGHT)
    s0.set_pixel(18, 30, RED_SHADOW)
    s0.set_pixel(19, 31, RED_DEEP)
    # Gold star embossed on front cover
    s0.set_pixel(14, 11, YELLOW_LIGHT)
    s0.set_pixel(15, 11, YELLOW_LIGHT)
    # Bottom floor shadow
    s0.line(1, 31, 30, 31, OUTLINE)
    sheet.blit(s0, 0, 0)

    # ---------------- Slice 1: Crimson Red Double Book Stack ----------------
    s1 = PixelCanvas(32, 32)
    # Bottom book: Large Red Encyclopedia (x=2..29, y=18..30)
    s1.rect(2, 18, 28, 13, RED_MID, outline=OUTLINE)
    s1.rect(2, 18, 6, 13, RED_DEEP, outline=OUTLINE)
    s1.line(3, 19, 3, 29, RED_LIGHT)
    # Gold spine bands on bottom book
    s1.line(3, 21, 6, 21, YELLOW_MID)
    s1.line(3, 26, 6, 26, YELLOW_MID)
    # Pages of bottom book
    s1.rect(8, 21, 21, 8, WHITE_SHADOW)
    s1.line(8, 23, 28, 23, WHITE_MID)
    s1.line(8, 25, 28, 25, WHITE_MID)

    # Top book: Slim Yellow Novel (x=5..26, y=7..18)
    s1.rect(5, 7, 22, 12, YELLOW_MID, outline=OUTLINE)
    s1.rect(5, 7, 5, 12, YELLOW_DEEP, outline=OUTLINE)
    s1.line(6, 8, 6, 17, YELLOW_LIGHT)
    # Blue spine title label on yellow book
    s1.rect(6, 11, 3, 4, BLUE_MID)
    # Pages of top book
    s1.rect(10, 10, 16, 7, WHITE_SHADOW)
    s1.line(10, 12, 25, 12, PURE_WHITE)
    s1.line(10, 14, 25, 14, WHITE_MID)
    # Green ribbon bookmark
    s1.line(16, 14, 18, 22, GREEN_MID)
    s1.set_pixel(18, 22, GREEN_LIGHT)
    # Shadow between books
    s1.line(4, 18, 27, 18, RED_DEEP)
    s1.line(1, 31, 30, 31, OUTLINE)
    sheet.blit(s1, 32, 0)

    # ---------------- Slice 2: Emerald Green Textbook ----------------
    s2 = PixelCanvas(32, 32)
    # Book body (x=3..28, y=8..30)
    s2.rect(3, 8, 26, 23, GREEN_MID, outline=OUTLINE)
    # Spine (x=3..8)
    s2.rect(3, 8, 6, 23, GREEN_DEEP, outline=OUTLINE)
    s2.line(4, 9, 4, 29, GREEN_LIGHT)
    # Ornate spine ribs
    for ry in [11, 16, 21, 26]:
        s2.line(4, ry, 7, ry, GREEN_LIGHT)
        s2.line(4, ry + 1, 7, ry + 1, GREEN_DEEP)
    # Cream paper block (x=9..27, y=12..27)
    s2.rect(9, 12, 19, 16, DUSK_CREAM, outline=METAL_SHADOW)
    for py in range(13, 27, 2):
        s2.line(10, py, 26, py, WHITE_MID)
    # Thumb index notches on paper block
    s2.set_pixel(27, 16, BROWN_DARK)
    s2.set_pixel(27, 20, BROWN_DARK)
    # Front cover filigree crest
    s2.circle(18, 10, 1, YELLOW_LIGHT)
    s2.line(2, 31, 29, 31, OUTLINE)
    sheet.blit(s2, 64, 0)

    # ---------------- Slice 3: Dusk/Purple Grimoire ----------------
    s3 = PixelCanvas(32, 32)
    # Heavy violet leather tome (x=2..29, y=6..30)
    s3.rect(2, 6, 28, 25, PURPLE_MID, outline=OUTLINE)
    # Antique ribbed spine (x=2..8)
    s3.rect(2, 6, 7, 25, PURPLE_DARK, outline=OUTLINE)
    s3.line(3, 7, 3, 29, PURPLE_LIGHT)
    # Gold foil ribs
    for ry in [10, 15, 20, 25]:
        s3.line(3, ry, 7, ry, YELLOW_MID)
        s3.set_pixel(3, ry, YELLOW_LIGHT)
    # Antique aged pages (x=9..28, y=10..27)
    s3.rect(9, 10, 20, 18, DUSK_CREAM, outline=BROWN_MID)
    for py in range(11, 27, 2):
        s3.line(10, py, 27, py, DUSK_BLUSH)
    # Heavy brass corner brackets
    # Top-right bracket
    s3.rect(25, 6, 4, 4, YELLOW_MID, outline=OUTLINE)
    s3.set_pixel(26, 7, YELLOW_LIGHT)
    s3.set_pixel(27, 8, YELLOW_DEEP)
    # Bottom-right bracket
    s3.rect(25, 27, 4, 4, YELLOW_MID, outline=OUTLINE)
    s3.set_pixel(26, 28, YELLOW_LIGHT)
    s3.set_pixel(27, 29, YELLOW_DEEP)
    # Gilded center star rune
    s3.circle(18, 8, 1, YELLOW_LIGHT)
    s3.line(1, 31, 30, 31, OUTLINE)
    sheet.blit(s3, 96, 0)

    return sheet


def generate_obstacle_box() -> PixelCanvas:
    """
    obstacle_box.png: 32x32 px.
    Cardboard moving box with packing tape and a bold red "FRAGILE" stamp.
    """
    c = PixelCanvas(32, 32, TRANSPARENT)

    # Box body (x=2..29, y=4..30)
    c.rect(2, 4, 28, 27, BROWN_MID, outline=OUTLINE)

    # 3D Highlight on top-left cardboard shoulder
    c.line(3, 5, 28, 5, WOOD_HIGHLIGHT)
    c.line(3, 6, 3, 29, WOOD_HIGHLIGHT)
    # 3D Shadow on bottom-right
    c.line(4, 29, 28, 29, BROWN_DARKEST)
    c.line(28, 6, 28, 29, BROWN_DARKEST)

    # Cardboard flaps & seam on top (y=4..10)
    c.line(2, 10, 29, 10, BROWN_DARK)
    c.line(16, 4, 16, 10, BROWN_DARKEST)  # Flap split seam

    # Wide shiny clear/tan packing tape running across center (x=2..29, y=13..18)
    c.rect(2, 13, 28, 6, WOOD_LIT)
    c.line(2, 13, 29, 13, WOOD_HIGHLIGHT)
    c.line(2, 14, 29, 14, PURE_WHITE)     # Plastic tape specular shine!
    c.line(2, 18, 29, 18, BROWN_DARK)

    # Corrugated cardboard fluting texture flecks
    for cy in [8, 21, 25]:
        for cx in range(5, 27, 4):
            c.set_pixel(cx, cy, BROWN_LIGHT)
            c.set_pixel(cx + 1, cy, BROWN_DARK)

    # Red rubber stamp "FRAGILE" (x=6..25, y=20..27)
    # Stencil stamp frame box
    c.rect(6, 20, 20, 8, RED_MID, outline=RED_DEEP)
    c.rect(7, 21, 18, 6, BROWN_MID)  # Inner cutout

    # Cracked wine glass / umbrella fragile symbol + stencil letters
    # Stencil letters "FRAGILE" impression in RED_MID
    letters = [
        # F
        (8, 22), (8, 23), (8, 24), (8, 25), (9, 22), (10, 22), (9, 24),
        # R
        (11, 22), (11, 23), (11, 24), (11, 25), (12, 22), (13, 23), (12, 24), (13, 25),
        # A
        (14, 23), (14, 24), (14, 25), (15, 22), (15, 24), (16, 23), (16, 24), (16, 25),
        # G
        (17, 22), (17, 23), (17, 24), (17, 25), (18, 22), (18, 25), (19, 24), (19, 25),
        # !
        (21, 22), (21, 23), (21, 25),
    ]
    for lx, ly in letters:
        c.set_pixel(lx, ly, RED_MID)

    # Broken/cracked glass icon on right of stamp
    c.set_pixel(23, 22, RED_MID)
    c.set_pixel(24, 23, RED_LIGHT)
    c.set_pixel(23, 24, RED_DEEP)

    # Bottom ground contact shadow
    c.line(1, 31, 30, 31, OUTLINE)

    return c


def generate_obstacle_jenga() -> PixelCanvas:
    """
    obstacle_jenga.png: 96x96 px (3 frames of 32x96).
    Wobbly Jenga wooden block tower in 3 heights in 32px steps:
    - Frame 0 (x=0..31): 1 tier high (32px tall, occupies y=64..95; y=0..63 is transparent).
    - Frame 1 (x=32..63): 2 tiers high (64px tall, occupies y=32..95; y=0..31 is transparent).
    - Frame 2 (x=64..95): 3 tiers high (96px tall, full height y=0..95).
    Features alternating perpendicular wood block layers, wobbly offsets, bevels, and beech grain.
    """
    sheet = PixelCanvas(96, 96, TRANSPARENT)

    def draw_jenga_tier(canvas: PixelCanvas, ox: int, base_y: int, tier_index: int, wobble: int):
        """Draws one 32px high tier consisting of 3 alternating Jenga block layers."""
        # Layer 1 (bottom layer of tier, 10px tall): 3 block ends facing camera
        y1 = base_y + 21
        for b_idx in range(3):
            bx = ox + 4 + b_idx * 8 + (wobble if b_idx == 1 else 0)
            # 7x10 block cross section
            canvas.rect(bx, y1, 7, 10, WOOD_HIGHLIGHT, outline=OUTLINE)
            # Top-left bevel
            canvas.line(bx + 1, y1 + 1, bx + 5, y1 + 1, WOOD_LIT)
            canvas.line(bx + 1, y1 + 2, bx + 1, y1 + 8, WOOD_LIT)
            # End-grain rings
            canvas.set_pixel(bx + 3, y1 + 5, BROWN_DARK)
            canvas.set_pixel(bx + 4, y1 + 5, BROWN_MID)
            # Bottom-right shadow
            canvas.line(bx + 1, y1 + 8, bx + 5, y1 + 8, BROWN_DARKEST)
            canvas.line(bx + 5, y1 + 2, bx + 5, y1 + 8, BROWN_DARKEST)

        # Layer 2 (middle layer of tier, 10px tall): 1 horizontal block running sideways
        y2 = base_y + 11
        bx2 = ox + 3 - wobble
        canvas.rect(bx2, y2, 26, 10, WOOD_HIGHLIGHT, outline=OUTLINE)
        canvas.line(bx2 + 1, y2 + 1, bx2 + 24, y2 + 1, WOOD_LIT)
        canvas.line(bx2 + 1, y2 + 2, bx2 + 1, y2 + 8, WOOD_LIT)
        # Horizontal beech wood grain
        for gx in range(bx2 + 2, bx2 + 24):
            if (gx + y2) % 3 == 0:
                canvas.set_pixel(gx, y2 + 4, BROWN_MID)
                canvas.set_pixel(gx, y2 + 7, BROWN_DARK)
        canvas.line(bx2 + 1, y2 + 8, bx2 + 24, y2 + 8, BROWN_DARKEST)

        # Layer 3 (top layer of tier, 10px tall): 3 block ends facing camera
        y3 = base_y + 1
        for b_idx in range(3):
            # One block pushed out for precarious wobble!
            shift = wobble * 2 if b_idx == 0 else -wobble
            bx3 = ox + 4 + b_idx * 8 + shift
            canvas.rect(bx3, y3, 7, 10, WOOD_HIGHLIGHT, outline=OUTLINE)
            canvas.line(bx3 + 1, y3 + 1, bx3 + 5, y3 + 1, WOOD_LIT)
            canvas.line(bx3 + 1, y3 + 2, bx3 + 1, y3 + 8, WOOD_LIT)
            canvas.set_pixel(bx3 + 3, y3 + 5, BROWN_DARK)
            canvas.line(bx3 + 1, y3 + 8, bx3 + 5, y3 + 8, BROWN_DARKEST)
            canvas.line(bx3 + 5, y3 + 2, bx3 + 5, y3 + 8, BROWN_DARKEST)

    # Frame 0: 1 tier high (occupies y=64..95)
    draw_jenga_tier(sheet, 0, 64, tier_index=0, wobble=1)
    sheet.line(2, 95, 29, 95, OUTLINE)

    # Frame 1: 2 tiers high (occupies y=32..95)
    draw_jenga_tier(sheet, 32, 64, tier_index=0, wobble=0)
    draw_jenga_tier(sheet, 32, 32, tier_index=1, wobble=2)
    sheet.line(34, 95, 61, 95, OUTLINE)

    # Frame 2: 3 tiers high (occupies y=0..95, full height!)
    draw_jenga_tier(sheet, 64, 64, tier_index=0, wobble=1)
    draw_jenga_tier(sheet, 64, 32, tier_index=1, wobble=-2)
    draw_jenga_tier(sheet, 64, 0, tier_index=2, wobble=3)  # Maximum dramatic wobble!
    sheet.line(66, 95, 93, 95, OUTLINE)

    return sheet


def generate_obstacle_lego() -> PixelCanvas:
    """
    obstacle_lego.png: 128x32 px (4 slices of 32x32).
    LEGO brick stacks in 4 vibrant colors (Red, Blue, Yellow, Green) with cylindrical studs on top.
    """
    sheet = PixelCanvas(128, 32, TRANSPARENT)

    lego_colors = [
        # Red
        (RED_MID, RED_LIGHT, RED_SHADOW, RED_DEEP),
        # Blue
        (BLUE_MID, BLUE_LIGHT, BLUE_SHADOW, BLUE_DEEP),
        # Yellow
        (YELLOW_MID, YELLOW_LIGHT, YELLOW_SHADOW, YELLOW_DEEP),
        # Green
        (GREEN_MID, GREEN_LIGHT, GREEN_SHADOW, GREEN_DEEP),
    ]

    for col_idx, (c_mid, c_light, c_shadow, c_deep) in enumerate(lego_colors):
        b = PixelCanvas(32, 32, TRANSPARENT)

        # Bottom brick (x=4..27, y=18..30)
        b.rect(4, 18, 24, 13, c_mid, outline=OUTLINE)
        b.line(5, 19, 26, 19, c_light)
        b.line(5, 20, 5, 29, c_light)
        b.line(26, 20, 26, 29, c_shadow)
        b.line(5, 29, 26, 29, c_deep)

        # Top brick (x=4..27, y=7..18)
        b.rect(4, 7, 24, 12, c_mid, outline=OUTLINE)
        b.line(5, 8, 26, 8, c_light)
        b.line(5, 9, 5, 17, c_light)
        b.line(26, 9, 26, 17, c_shadow)
        # Seam shadow between bricks
        b.line(4, 18, 27, 18, OUTLINE)

        # 2 Raised cylindrical LEGO studs on top (x=7..13 and x=18..24, y=1..6)
        for sx in [7, 18]:
            # Stud body
            b.rect(sx, 1, 7, 6, c_mid, outline=OUTLINE)
            # Top circular face
            b.line(sx + 1, 2, sx + 5, 2, c_light)
            b.set_pixel(sx + 1, 2, PURE_WHITE)  # Specular gleam!
            b.set_pixel(sx + 2, 2, PURE_WHITE)
            b.set_pixel(sx + 1, 3, c_light)
            b.line(sx + 1, 4, sx + 5, 4, c_shadow)
            b.line(sx + 1, 5, sx + 5, 5, c_deep)

        # Floor contact outline
        b.line(3, 31, 28, 31, OUTLINE)

        sheet.blit(b, col_idx * 32, 0)

    return sheet


# ==============================================================================
# 5. GOAL FLAG & PIT BG
# ==============================================================================

def generate_goal_flag() -> List[PixelCanvas]:
    """
    goal_flag.png: 64x128 px, 6 frames (384x128 px, 10 fps, loop: true).
    Yellow #2 pencil pole with silver ferrule, pink eraser top, and flapping red/yellow pennant with star.
    """
    frames = []

    for frame_idx in range(6):
        c = PixelCanvas(64, 128, TRANSPARENT)

        # ------------------ 1. PENCIL POLE (x=10..22, y=8..125) ------------------
        # Pink Rubber Eraser Top (y=8..22)
        # Rounded crown (y=8..9)
        c.line(13, 8, 19, 8, OUTLINE)
        c.line(12, 9, 20, 9, DUSK_CREAM)
        # Eraser body (y=10..22)
        for y in range(10, 23):
            c.set_pixel(11, y, OUTLINE)
            c.set_pixel(12, y, DUSK_CREAM)   # Highlight facet
            c.set_pixel(13, y, DUSK_BLUSH)
            c.set_pixel(14, y, DUSK_PEACH)
            c.set_pixel(15, y, DUSK_PEACH)   # Mid facet
            c.set_pixel(16, y, DUSK_PINK)
            c.set_pixel(17, y, DUSK_PINK)
            c.set_pixel(18, y, PURPLE_LIGHT) # Shadow facet
            c.set_pixel(19, y, PURPLE_DARK)
            c.set_pixel(20, y, OUTLINE)

        # Silver Metal Ferrule (y=23..36)
        for y in range(23, 37):
            c.set_pixel(11, y, OUTLINE)
            c.set_pixel(12, y, PURE_WHITE)    # Specular shine
            c.set_pixel(13, y, WHITE_MID)
            c.set_pixel(14, y, WHITE_SHADOW)  # Metal face
            c.set_pixel(15, y, WHITE_SHADOW)
            c.set_pixel(16, y, METAL_MID)
            c.set_pixel(17, y, METAL_MID)
            c.set_pixel(18, y, METAL_SHADOW)  # Metal shadow
            c.set_pixel(19, y, SHADOW_DEEP)
            c.set_pixel(20, y, OUTLINE)

        # Horizontal crimp bands indented across ferrule
        for crimp_y in [26, 30, 34]:
            c.line(12, crimp_y, 19, crimp_y, SHADOW_DEEP)
            c.set_pixel(12, crimp_y, PURE_WHITE)

        # Hexagonal Yellow Pencil Shaft (y=37..122)
        for y in range(37, 123):
            c.set_pixel(11, y, OUTLINE)
            # Facet 1: Lit face (x=12..14)
            c.set_pixel(12, y, YELLOW_LIGHT)
            c.set_pixel(13, y, YELLOW_LIGHT)
            c.set_pixel(14, y, YELLOW_MID)
            # Facet 2: Center (x=15..17)
            c.set_pixel(15, y, YELLOW_MID)
            c.set_pixel(16, y, YELLOW_MID)
            c.set_pixel(17, y, YELLOW_SHADOW)
            # Facet 3: Shadow face (x=18..19)
            c.set_pixel(18, y, YELLOW_SHADOW)
            c.set_pixel(19, y, YELLOW_DEEP)
            c.set_pixel(20, y, OUTLINE)

        # Green brand stamp imprint on pencil body "#2 HB" (y=68..78)
        for y in range(68, 79):
            c.set_pixel(15, y, GREEN_SHADOW)
            c.set_pixel(16, y, GREEN_RICH)

        # Sturdy Base Mount on floor (y=123..127)
        # Wooden collar
        c.line(9, 123, 22, 123, BROWN_MID)
        c.set_pixel(9, 123, OUTLINE)
        c.set_pixel(22, 123, OUTLINE)
        c.line(10, 124, 21, 124, BROWN_LIGHT)
        # Metal floor plate
        c.line(7, 125, 24, 125, METAL_MID)
        c.line(6, 126, 25, 126, BROWN_DARKEST)
        c.line(5, 127, 26, 127, OUTLINE)

        # ------------------ 2. PENNANT FLAG (x=21..62) ------------------
        # Dynamic sinusoidal wave animation
        phase = (frame_idx / 6.0) * 2.0 * math.pi
        xs = list(range(21, 62))
        y_tops = {}
        y_bots = {}
        slopes = {}
        y_centers = {}

        for x in xs:
            dist = x - 20
            norm_dist = dist / 41.0
            # Amplitude increases gently from 1.2px at pole to 5.6px at tip
            amp = 1.2 + 4.8 * norm_dist
            wave = math.sin(phase - dist * 0.28)
            slope = math.cos(phase - dist * 0.28)
            yc = 52.0 + amp * wave
            # Taper pennant height smoothly from 48px at pole down to 4px at tip
            h = max(4.0, 48.0 * (1.0 - norm_dist))
            y_tops[x] = int(round(yc - h / 2.0))
            y_bots[x] = int(round(yc + h / 2.0))
            slopes[x] = slope
            y_centers[x] = yc

        # Fill cloth columns seamlessly
        for i, x in enumerate(xs):
            yt = y_tops[x]
            yb = y_bots[x]
            prev_yt = y_tops[xs[i - 1]] if i > 0 else yt
            next_yt = y_tops[xs[i + 1]] if i < len(xs) - 1 else yt
            prev_yb = y_bots[xs[i - 1]] if i > 0 else yb
            next_yb = y_bots[xs[i + 1]] if i < len(xs) - 1 else yb

            span_top = min(yt, prev_yt, next_yt)
            span_bot = max(yb, prev_yb, next_yb)
            slope = slopes[x]
            yc = y_centers[x]

            for y in range(span_top, span_bot + 1):
                is_edge = (y == span_top or y == span_bot or x == 61 or x == 21)
                if is_edge:
                    c.set_pixel(x, y, OUTLINE)
                else:
                    # Gold border trim on top and bottom 2-3px
                    is_trim = (y <= span_top + 2 or y >= span_bot - 2)
                    is_center_stripe = (abs(y - int(round(yc))) <= 2)

                    if is_trim or is_center_stripe:
                        if slope > 0.2:
                            c.set_pixel(x, y, YELLOW_LIGHT)
                        elif slope < -0.2:
                            c.set_pixel(x, y, YELLOW_SHADOW)
                        else:
                            c.set_pixel(x, y, YELLOW_MID)
                    else:
                        if slope > 0.25:
                            c.set_pixel(x, y, RED_LIGHT)
                        elif slope < -0.25:
                            c.set_pixel(x, y, RED_DEEP)
                        elif slope < -0.05:
                            c.set_pixel(x, y, RED_SHADOW)
                        else:
                            c.set_pixel(x, y, RED_MID)

        # Star Insignia on flag (riding the wave near pole at x=31)
        star_cx = 31
        star_cy = int(round(y_centers[31]))
        star_offsets = [
            (0, 0), (-1, 0), (1, 0), (0, -1), (0, 1),
            (-2, 0), (2, 0), (0, -2), (0, 2),
            (-1, -1), (1, -1), (-1, 1), (1, 1)
        ]
        for sox, soy in star_offsets:
            c.set_pixel(star_cx + sox, star_cy + soy, YELLOW_LIGHT)
        c.set_pixel(star_cx, star_cy, PURE_WHITE)
        # Drop shadow beneath star
        c.set_pixel(star_cx + 1, star_cy + 2, RED_DEEP)
        c.set_pixel(star_cx + 2, star_cy + 2, RED_DEEP)

        # Flag hoist attachment rings to the pencil pole
        c.rect(19, 28, 3, 3, WHITE_SHADOW, outline=OUTLINE)
        c.rect(19, 74, 3, 3, WHITE_SHADOW, outline=OUTLINE)

        frames.append(c)

    return frames


def generate_pit_bg() -> PixelCanvas:
    """
    pit_bg.png: 32x128 px (tiles horizontally).
    Deep subfloor pit background:
    - Upper subfloor gloom fading from floorboards.
    - Fluffy dust bunnies nestled under the joists.
    - Dangling lost kid's striped tube sock.
    - Mysterious glowing yellow eyes peering out of the deep void.
    - 100% fade to VOID_BLACK at bottom.
    """
    c = PixelCanvas(32, 128, VOID_BLACK)

    # 1. Background gradient into deep purple-black gloom
    for y in range(128):
        for x in range(32):
            if y < 8:
                c.set_pixel(x, y, OUTLINE if y == 0 else SHADOW_PURPLE_DARK)
            elif y < 20:
                c.set_pixel(x, y, SHADOW_PURPLE_DARK if (x + y) % 2 == 0 else SHADOW_DEEP)
            elif y < 45:
                c.set_pixel(x, y, SHADOW_DEEP if (x * 3 + y) % 4 == 0 else SHADOW_MID)
            elif y < 96:
                c.set_pixel(x, y, SHADOW_DEEP if (x * 5 + y) % 7 == 0 else OUTLINE)
            elif y < 116:
                c.set_pixel(x, y, OUTLINE if (x + y) % 5 == 0 else VOID_BLACK)
            else:
                c.set_pixel(x, y, VOID_BLACK)

    # 2. Dust bunnies accumulation (y=22..38)
    # Main fluffy clump centered at (16, 28)
    c.circle(16, 28, 8, SHADOW_DEEP)
    c.circle(11, 29, 6, SHADOW_DEEP)
    c.circle(21, 29, 6, SHADOW_DEEP)
    # Dust bunny soft highlight lobes
    for hx, hy in [(15, 25), (16, 25), (12, 26), (13, 26), (19, 26), (20, 26)]:
        c.set_pixel(hx, hy, SHADOW_MID)
    c.set_pixel(15, 24, PURPLE_MID)
    c.set_pixel(16, 24, PURPLE_MID)

    # Floating dust motes / hair fibers
    c.set_pixel(4, 20, PURPLE_LIGHT)
    c.set_pixel(5, 22, PURPLE_MID)
    c.set_pixel(26, 30, PURPLE_MID)
    c.set_pixel(28, 32, PURPLE_LIGHT)

    # 3. Dangling lost kid's striped tube sock (y=46..90)
    # Snag thread hanging from crack above
    c.line(15, 46, 15, 49, WHITE_SHADOW)

    # Sock ribbed cuff (y=50..54, x=10..19)
    for y in range(50, 55):
        for cx in range(10, 20):
            c.set_pixel(cx, y, WHITE_MID if cx % 2 == 0 else WHITE_SHADOW)
    c.line(10, 50, 19, 50, SHADOW_MID)

    # Sock leg body with retro blue & white stripes (y=55..74, x=10..20)
    for y in range(55, 75):
        # Determine stripe color
        if y in range(55, 59) or y in range(63, 67) or y in range(71, 75):
            fill_c = BLUE_MID
            hi_c = BLUE_LIGHT
            sh_c = BLUE_SHADOW
        else:
            fill_c = WHITE_SHADOW
            hi_c = PURE_WHITE
            sh_c = SHADOW_MID

        # Left outline / shadow
        c.set_pixel(10, y, sh_c)
        c.set_pixel(11, y, hi_c)
        c.set_pixel(12, y, hi_c)
        # Body
        for bx in range(13, 18):
            c.set_pixel(bx, y, fill_c)
        # Right shadow
        c.set_pixel(18, y, sh_c)
        c.set_pixel(19, y, sh_c)

    # Sock Heel (y=75..80): Red heel patch curving leftward (x=7..17)
    for y in range(75, 81):
        c.set_pixel(8, y, RED_DEEP)
        c.set_pixel(9, y, RED_SHADOW)
        c.set_pixel(10, y, RED_MID)
        c.set_pixel(11, y, RED_LIGHT if y < 78 else RED_MID)
        for rx in range(12, 17):
            c.set_pixel(rx, y, RED_MID)
        c.set_pixel(17, y, RED_SHADOW)
    c.set_pixel(7, 77, RED_SHADOW)
    c.set_pixel(7, 78, RED_SHADOW)

    # Sock Foot & Toe (y=81..90) drooping to the right
    # Foot arch (y=81..85, x=10..22)
    for y in range(81, 86):
        c.set_pixel(10, y, SHADOW_MID)
        for fx in range(11, 21):
            c.set_pixel(fx, y, WHITE_SHADOW)
        c.set_pixel(21, y, SHADOW_MID)

    # Red Toe Cap (y=86..90, x=13..23)
    for y in range(86, 91):
        c.set_pixel(13, y, RED_SHADOW)
        c.set_pixel(14, y, RED_LIGHT)
        for tx in range(15, 21):
            c.set_pixel(tx, y, RED_MID)
        c.set_pixel(21, y, RED_SHADOW)
        if y < 89:
            c.set_pixel(22, y, RED_DEEP)

    # 4. Faint glowing yellow eyes peering from the darkness (y=100..106)
    # Left eye at (8, 102..104), Right eye at (19, 102..104)
    # Soft purple eye glow corona
    for ex in [6, 7, 8, 9, 10, 17, 18, 19, 20, 21]:
        for ey in range(100, 107):
            if c.get_pixel(ex, ey) == VOID_BLACK:
                c.set_pixel(ex, ey, SHADOW_DEEP)

    # Left eye
    c.rect(7, 102, 3, 3, YELLOW_MID)
    c.set_pixel(8, 102, PURE_WHITE)     # Specular glint
    c.set_pixel(7, 102, YELLOW_LIGHT)
    c.set_pixel(9, 104, YELLOW_SHADOW)

    # Right eye
    c.rect(18, 102, 3, 3, YELLOW_MID)
    c.set_pixel(19, 102, PURE_WHITE)    # Specular glint
    c.set_pixel(18, 102, YELLOW_LIGHT)
    c.set_pixel(20, 104, YELLOW_SHADOW)

    # 5. Seamless horizontal border wrap check
    for y in range(128):
        p0 = c.get_pixel(0, y)
        p31 = c.get_pixel(31, y)
        if y < 96 and p0 != p31:
            avg_color = SHADOW_DEEP if y < 45 else OUTLINE
            c.set_pixel(0, y, avg_color)
            c.set_pixel(31, y, avg_color)

    # Absolute fade to VOID_BLACK for y >= 115
    for y in range(115, 128):
        for x in range(32):
            c.set_pixel(x, y, VOID_BLACK)

    return c


# ==============================================================================
# MAIN GENERATOR & MANIFEST UPDATER
# ==============================================================================

def generate_all_v2(output_dir: str = "art/v2"):
    os.makedirs(output_dir, exist_ok=True)

    print("Generating v2 environment tiles and obstacles...")

    # 1. tileset_floor.png (256x96 px)
    floor = generate_tileset_floor()
    floor_path = os.path.join(output_dir, "tileset_floor.png")
    floor.to_image().save(floor_path, "PNG")
    print(f"Saved {floor_path} ({floor.width}x{floor.height})")

    # 2. tileset_floor_n.png (256x96 px normal map)
    floor_n = generate_normal_map(floor, strength=2.0)
    floor_n_path = os.path.join(output_dir, "tileset_floor_n.png")
    floor_n.to_image().save(floor_n_path, "PNG")
    print(f"Saved {floor_n_path} ({floor_n.width}x{floor_n.height})")

    # 3. tileset_floor_rug.png (256x96 px)
    rug = generate_tileset_floor_rug()
    rug_path = os.path.join(output_dir, "tileset_floor_rug.png")
    rug.to_image().save(rug_path, "PNG")
    print(f"Saved {rug_path} ({rug.width}x{rug.height})")

    # 4. tileset_floor_carpet.png (256x96 px)
    carpet = generate_tileset_floor_carpet()
    carpet_path = os.path.join(output_dir, "tileset_floor_carpet.png")
    carpet.to_image().save(carpet_path, "PNG")
    print(f"Saved {carpet_path} ({carpet.width}x{carpet.height})")

    # 5. toy_blocks.png (128x96 px)
    blocks = generate_toy_blocks()
    blocks_path = os.path.join(output_dir, "toy_blocks.png")
    blocks.to_image().save(blocks_path, "PNG")
    print(f"Saved {blocks_path} ({blocks.width}x{blocks.height})")

    # 6. toy_blocks_n.png (128x96 px normal map)
    blocks_n = generate_normal_map(blocks, strength=2.0)
    blocks_n_path = os.path.join(output_dir, "toy_blocks_n.png")
    blocks_n.to_image().save(blocks_n_path, "PNG")
    print(f"Saved {blocks_n_path} ({blocks_n.width}x{blocks_n.height})")

    # 7. obstacle_books.png (128x32 px)
    books = generate_obstacle_books()
    books_path = os.path.join(output_dir, "obstacle_books.png")
    books.to_image().save(books_path, "PNG")
    print(f"Saved {books_path} ({books.width}x{books.height})")

    # 8. obstacle_box.png (32x32 px)
    box = generate_obstacle_box()
    box_path = os.path.join(output_dir, "obstacle_box.png")
    box.to_image().save(box_path, "PNG")
    print(f"Saved {box_path} ({box.width}x{box.height})")

    # 9. obstacle_jenga.png (96x96 px)
    jenga = generate_obstacle_jenga()
    jenga_path = os.path.join(output_dir, "obstacle_jenga.png")
    jenga.to_image().save(jenga_path, "PNG")
    print(f"Saved {jenga_path} ({jenga.width}x{jenga.height})")

    # 10. obstacle_lego.png (128x32 px)
    lego = generate_obstacle_lego()
    lego_path = os.path.join(output_dir, "obstacle_lego.png")
    lego.to_image().save(lego_path, "PNG")
    print(f"Saved {lego_path} ({lego.width}x{lego.height})")

    # 11. goal_flag.png (384x128 px, 6 frames of 64x128)
    flag_frames = generate_goal_flag()
    flag_path = os.path.join(output_dir, "goal_flag.png")
    assemble_strip(flag_frames, flag_path)

    # 12. pit_bg.png (32x128 px)
    pit = generate_pit_bg()
    pit_path = os.path.join(output_dir, "pit_bg.png")
    pit.to_image().save(pit_path, "PNG")
    print(f"Saved {pit_path} ({pit.width}x{pit.height})")

    # Update manifest.json in art/v2
    manifest_path = os.path.join(output_dir, "manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as f:
            manifest = json.load(f)

        manifest["tileset_floor.png"] = {
            "frame_w": 256,
            "frame_h": 96,
            "frames": 1,
            "fps": 0,
            "loop": False,
            "tile_w": 32,
            "tile_h": 32,
            "columns": 8,
            "rows": 3
        }
        manifest["tileset_floor_n.png"] = {
            "frame_w": 256,
            "frame_h": 96,
            "frames": 1,
            "fps": 0,
            "loop": False
        }
        manifest["tileset_floor_rug.png"] = {
            "frame_w": 256,
            "frame_h": 96,
            "frames": 1,
            "fps": 0,
            "loop": False,
            "tile_w": 32,
            "tile_h": 32,
            "columns": 8,
            "rows": 3
        }
        manifest["tileset_floor_carpet.png"] = {
            "frame_w": 256,
            "frame_h": 96,
            "frames": 1,
            "fps": 0,
            "loop": False,
            "tile_w": 32,
            "tile_h": 32,
            "columns": 8,
            "rows": 3
        }
        manifest["toy_blocks.png"] = {
            "frame_w": 128,
            "frame_h": 96,
            "frames": 1,
            "fps": 0,
            "loop": False,
            "tile_w": 32,
            "tile_h": 32,
            "columns": 4,
            "rows": 3
        }
        manifest["toy_blocks_n.png"] = {
            "frame_w": 128,
            "frame_h": 96,
            "frames": 1,
            "fps": 0,
            "loop": False
        }
        manifest["obstacle_books.png"] = {
            "frame_w": 32,
            "frame_h": 32,
            "frames": 4,
            "fps": 0,
            "loop": False
        }
        manifest["obstacle_box.png"] = {
            "frame_w": 32,
            "frame_h": 32,
            "frames": 1,
            "fps": 0,
            "loop": False
        }
        manifest["obstacle_jenga.png"] = {
            "frame_w": 32,
            "frame_h": 96,
            "frames": 3,
            "fps": 0,
            "loop": False
        }
        manifest["obstacle_lego.png"] = {
            "frame_w": 32,
            "frame_h": 32,
            "frames": 4,
            "fps": 0,
            "loop": False
        }
        manifest["goal_flag.png"] = {
            "frame_w": 64,
            "frame_h": 128,
            "frames": 6,
            "fps": 10,
            "loop": True
        }
        manifest["pit_bg.png"] = {
            "frame_w": 32,
            "frame_h": 128,
            "frames": 1,
            "fps": 0,
            "loop": False
        }

        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=1)
        print(f"Updated {manifest_path} with new environment and obstacle entries.")


if __name__ == "__main__":
    generate_all_v2()
