"""Younger Sibling Simulator - Environment Tiles Generator.

Elevated, high-fidelity pixel art for all environment assets:
- tileset_floor.png: Warm wood-grain floor planks, 2px lit top lip, pit edge cliff dropoffs,
                     butt joints, nail heads, wood knots, toy scratch gouges, dropped penny glint.
                     Mid-fill timber joists, dropped red crayon, blue LEGO stud, coin, iron nails.
                     Deep-fill subfloor void fading into purple-black darkness with cobwebs.
- toy_blocks.png:    3D tactile toy alphabet blocks (Red, Blue, Yellow, Green) x (A, B, Star).
                     Bright bevels on top-left, dark bevels on bottom-right, recessed face with
                     crisp embossed lettering and dimensional drop shadows.
- goal_flag.png:     Classic #2 yellow hexagonal pencil pole with silver metal ferrule and pink eraser,
                     waving pennant flag with cloth ripple physics, cloth wave shading, and star emblem.
- pit_bg.png:        Atmospheric 16x64 subfloor pit background, horizontally seamless, dust bunnies,
                     dangling lost kid's striped tube sock, glowing eyes in the void.
"""

import math
from typing import List, Tuple
from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE,
    SHADOW_DEEP, SHADOW_MID, PURPLE_MID, PURPLE_LIGHT, DUSK_PINK, DUSK_PEACH,
    BROWN_DARKEST, BROWN_DARK, BROWN_MID, BROWN_LIGHT, WOOD_HIGHLIGHT,
    RED_SHADOW, RED_MID, RED_LIGHT,
    BLUE_SHADOW, BLUE_MID, BLUE_LIGHT,
    YELLOW_SHADOW, YELLOW_MID, YELLOW_LIGHT,
    GREEN_SHADOW, GREEN_MID, GREEN_LIGHT,
    WHITE_SHADOW, PURE_WHITE,
    VOID_BLACK
)

def _generate_surface_base() -> PixelCanvas:
    """Creates the base seamless 16x16 surface wood floor tile."""
    t = PixelCanvas(16, 16)

    # 1. 2px Lit top lip
    # y=0: Warm golden specular highlight catching upper-left window light
    for x in range(16):
        # Subtle rhythm in the highlight sheen
        if x in [0, 1, 6, 7, 12, 13]:
            t.set_pixel(x, 0, YELLOW_LIGHT)
        else:
            t.set_pixel(x, 0, WOOD_HIGHLIGHT)

    # y=1: Bevel transition
    for x in range(16):
        if x % 4 == 0:
            t.set_pixel(x, 1, WOOD_HIGHLIGHT)
        else:
            t.set_pixel(x, 1, BROWN_LIGHT)

    # 2. Plank body (y=2..14) with natural horizontal wood grain waves
    # Base fill
    t.rect(0, 2, 16, 13, BROWN_MID)

    # Upper grain wave around y=4..5 (seamless horizontal wrap)
    for x in range(16):
        dy = int(0.7 * math.sin(x * 2.0 * math.pi / 16.0))
        t.set_pixel(x, 4 + dy, BROWN_DARK)
        if dy == 0:
            t.set_pixel(x, 3, BROWN_LIGHT)

    # Middle grain wave around y=8..9 (seamless horizontal wrap)
    for x in range(16):
        dy = int(0.8 * math.cos(x * 2.0 * math.pi / 16.0))
        t.set_pixel(x, 8 + dy, BROWN_DARK)
        t.set_pixel((x + 8) % 16, 7 + dy, BROWN_LIGHT)

    # Lower grain wave around y=12..13 (seamless horizontal wrap)
    for x in range(16):
        dy = int(0.6 * math.sin((x + 4) * 2.0 * math.pi / 16.0))
        t.set_pixel(x, 12 + dy, BROWN_DARK)
        if dy > 0:
            t.set_pixel(x, 11, BROWN_LIGHT)

    # 3. Plank bottom seam at y=15 (meeting subfloor)
    t.line(0, 15, 15, 15, BROWN_DARKEST)
    for x in range(16):
        if x % 3 == 0:
            t.set_pixel(x, 15, OUTLINE)
        if x % 2 == 1:
            t.set_pixel(x, 14, BROWN_DARK)

    return t

def _generate_joist_base() -> PixelCanvas:
    """Creates the base seamless 16x16 subfloor timber joist tile."""
    m = PixelCanvas(16, 16)

    # Dark horizontal seam separating surface planks from joists
    m.line(0, 0, 15, 0, OUTLINE)
    m.line(0, 1, 15, 1, BROWN_DARKEST)

    # Timber body fill: deep rich aged wood
    m.rect(0, 2, 16, 14, BROWN_DARK)

    # Central vertical stud beam structure (x=3..12)
    # Left facet catches ambient bounce (x=3..5)
    for y in range(2, 16):
        m.set_pixel(3, y, BROWN_MID)
        m.set_pixel(4, y, BROWN_LIGHT if (y % 4 in [1, 2]) else BROWN_MID)
        m.set_pixel(5, y, BROWN_MID)

    # Center vertical wood fibers (x=6..9)
    for y in range(2, 16):
        m.set_pixel(7, y, BROWN_DARKEST if (y % 3 != 0) else BROWN_DARK)
        m.set_pixel(8, y, BROWN_MID if (y % 5 == 0) else BROWN_DARK)
        m.set_pixel(9, y, BROWN_DARKEST if (y % 4 == 1) else BROWN_DARK)

    # Right facet in shadow (x=10..12)
    for y in range(2, 16):
        m.set_pixel(10, y, BROWN_DARK)
        m.set_pixel(11, y, BROWN_DARKEST)
        m.set_pixel(12, y, OUTLINE if (y % 2 == 0) else BROWN_DARKEST)

    # Recessed gap edges on sides (x=0..2 and x=13..15)
    for y in range(2, 16):
        m.set_pixel(0, y, SHADOW_DEEP)
        m.set_pixel(1, y, BROWN_DARKEST)
        m.set_pixel(14, y, BROWN_DARKEST)
        m.set_pixel(15, y, SHADOW_DEEP)

    return m

def generate_tileset_floor() -> PixelCanvas:
    """
    128x48 px (8 tiles wide x 3 tiles tall, 16x16 grid).
    Row 0: Surface tiles with 2px lit top lip, edge dropoffs, seams, nail heads, knot, scratches, penny.
    Row 1: Mid fill timber joists with red crayon, blue LEGO stud, dropped penny, iron nail.
    Row 2: Deep fill subfloor void fading into darkness with cobweb strands.
    """
    sheet = PixelCanvas(128, 48, TRANSPARENT)

    # ================== ROW 0: SURFACE TILES ==================
    t0 = _generate_surface_base()
    sheet.blit(t0, 0, 0)

    # Tile 1: Surface plank with vertical butt-joint seam at x=9
    t1 = t0.clone()
    # Vertical cut joint where two floorboards meet
    for y in range(2, 15):
        t1.set_pixel(8, y, BROWN_DARK)       # Shadow on left board edge
        t1.set_pixel(9, y, OUTLINE if y % 2 == 0 else BROWN_DARKEST)  # Deep seam
        t1.set_pixel(10, y, WOOD_HIGHLIGHT)  # Lit bevel on right board edge
    # Two countersunk finishing nails near board ends
    for nx, ny in [(6, 5), (12, 10)]:
        t1.set_pixel(nx, ny, PURE_WHITE)
        t1.set_pixel(nx + 1, ny, WHITE_SHADOW)
        t1.set_pixel(nx, ny + 1, WHITE_SHADOW)
        t1.set_pixel(nx + 1, ny + 1, BROWN_DARKEST)
    sheet.blit(t1, 16, 0)

    # Tile 2: Left cliff edge facing a pit! (Plank thickness & shadow on left)
    t2 = t0.clone()
    # Crisp outer outline along the pit edge
    t2.line(0, 1, 0, 15, OUTLINE)
    # Beveled rounded corner at (0, 0)
    t2.set_pixel(0, 0, OUTLINE)
    t2.set_pixel(1, 0, YELLOW_LIGHT)
    # Cut plank cross-section showing plank depth
    for y in range(1, 16):
        t2.set_pixel(1, y, BROWN_DARKEST if y > 1 else WOOD_HIGHLIGHT)
        t2.set_pixel(2, y, BROWN_DARK)
        t2.set_pixel(3, y, BROWN_MID)
    # Shadow cast downward into pit
    t2.set_pixel(0, 15, OUTLINE)
    t2.set_pixel(1, 15, SHADOW_DEEP)
    sheet.blit(t2, 32, 0)

    # Tile 3: Right cliff edge facing a pit! (Plank thickness & shadow on right)
    t3 = t0.clone()
    # Crisp outer outline along right pit edge
    t3.line(15, 1, 15, 15, OUTLINE)
    # Beveled rounded corner at (15, 0)
    t3.set_pixel(15, 0, OUTLINE)
    t3.set_pixel(14, 0, WOOD_HIGHLIGHT)
    # Vertical shadow on right edge
    for y in range(1, 16):
        t3.set_pixel(14, y, SHADOW_DEEP if y > 1 else WOOD_HIGHLIGHT)
        t3.set_pixel(13, y, BROWN_DARKEST)
        t3.set_pixel(12, y, BROWN_DARK)
    sheet.blit(t3, 48, 0)

    # Tile 4: Surface plank with shiny nail heads
    t4 = t0.clone()
    # Two distinct pairs of nail heads
    nails = [(4, 6), (12, 10)]
    for nx, ny in nails:
        t4.set_pixel(nx - 1, ny, BROWN_DARK)       # Indentation
        t4.set_pixel(nx, ny, PURE_WHITE)           # Specular glint
        t4.set_pixel(nx + 1, ny, WHITE_SHADOW)
        t4.set_pixel(nx, ny + 1, WHITE_SHADOW)
        t4.set_pixel(nx + 1, ny + 1, OUTLINE)      # Recessed shadow
        t4.set_pixel(nx, ny + 2, BROWN_DARKEST)
    sheet.blit(t4, 64, 0)

    # Tile 5: Surface plank with wood knot
    t5 = t0.clone()
    # Wood knot core at (8, 8)
    t5.set_pixel(8, 8, BROWN_DARKEST)
    t5.set_pixel(9, 8, OUTLINE)
    t5.set_pixel(8, 7, BROWN_DARKEST)
    t5.set_pixel(9, 7, BROWN_DARK)
    # Swirling inner ring
    for kx, ky in [(7, 7), (7, 8), (7, 9), (8, 9), (9, 9), (10, 8), (10, 7)]:
        t5.set_pixel(kx, ky, BROWN_DARK)
    # Highlight rim curling on top-left of knot
    t5.set_pixel(6, 6, WOOD_HIGHLIGHT)
    t5.set_pixel(7, 6, WOOD_HIGHLIGHT)
    t5.set_pixel(8, 6, WOOD_HIGHLIGHT)
    t5.set_pixel(6, 7, WOOD_HIGHLIGHT)
    t5.set_pixel(6, 8, BROWN_LIGHT)
    # Outer grain flow
    t5.line(5, 5, 11, 5, BROWN_DARK)
    t5.line(5, 10, 11, 10, BROWN_DARK)
    sheet.blit(t5, 80, 0)

    # Tile 6: Surface plank with toy car scratch marks
    t6 = t0.clone()
    # Scratch track 1 (gouged wood revealing lighter raw grain + shadow groove)
    scratch1 = [(3, 4), (4, 4), (5, 5), (6, 5), (7, 6), (8, 6), (9, 7), (10, 7), (11, 8)]
    for sx, sy in scratch1:
        t6.set_pixel(sx, sy, YELLOW_LIGHT if (sx + sy) % 3 == 0 else WOOD_HIGHLIGHT)
        t6.set_pixel(sx, sy + 1, BROWN_DARKEST)
    # Parallel scratch track 2 (from other wheel of toy car)
    scratch2 = [(4, 8), (5, 8), (6, 9), (7, 9), (8, 10), (9, 10), (10, 11), (11, 11), (12, 12)]
    for sx, sy in scratch2:
        t6.set_pixel(sx, sy, WOOD_HIGHLIGHT)
        t6.set_pixel(sx, sy + 1, BROWN_DARKEST)
    sheet.blit(t6, 96, 0)

    # Tile 7: Surface plank with dropped penny glint
    t7 = t0.clone()
    # 4x4 circular coin silhouette centered at (8, 8)
    coin_pts = [
                 (7, 6), (8, 6), (9, 6),
         (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),
         (6, 8), (7, 8), (8, 8), (9, 8), (10, 8),
                 (7, 9), (8, 9), (9, 9)
    ]
    for cx, cy in coin_pts:
        t7.set_pixel(cx, cy, YELLOW_MID)
    # Metallic shading & rim
    t7.set_pixel(6, 7, YELLOW_SHADOW)
    t7.set_pixel(6, 8, YELLOW_SHADOW)
    t7.set_pixel(10, 7, YELLOW_SHADOW)
    t7.set_pixel(10, 8, YELLOW_SHADOW)
    t7.set_pixel(7, 9, BROWN_DARKEST)
    t7.set_pixel(8, 9, BROWN_DARKEST)
    t7.set_pixel(9, 9, BROWN_DARKEST)
    # Shiny gleam on upper-left rim
    t7.set_pixel(7, 6, PURE_WHITE)
    t7.set_pixel(8, 6, YELLOW_LIGHT)
    t7.set_pixel(7, 7, YELLOW_LIGHT)
    # Cast shadow beneath coin on plank
    t7.line(6, 10, 10, 10, BROWN_DARKEST)
    sheet.blit(t7, 112, 0)

    # ================== ROW 1: MIDDLE FILL TILES ==================
    m0 = _generate_joist_base()
    sheet.blit(m0, 0, 16)

    # Tile 1: Rich dark wood grain stud variant
    m1 = m0.clone()
    # Wood grain knot in stud
    m1.set_pixel(8, 7, BROWN_DARKEST)
    m1.set_pixel(7, 7, OUTLINE)
    m1.circle(8, 7, 2, BROWN_DARK, outline=BROWN_DARKEST)
    m1.set_pixel(7, 6, BROWN_LIGHT)
    m1.line(6, 12, 10, 12, BROWN_DARKEST)
    sheet.blit(m1, 16, 16)

    # Tile 2: Left cliff edge facing pit
    m2 = m0.clone()
    m2.line(0, 0, 0, 15, OUTLINE)
    m2.line(1, 0, 1, 15, SHADOW_DEEP)
    m2.line(2, 0, 2, 15, BROWN_DARKEST)
    sheet.blit(m2, 32, 16)

    # Tile 3: Right cliff edge facing pit
    m3 = m0.clone()
    m3.line(15, 0, 15, 15, OUTLINE)
    m3.line(14, 0, 14, 15, SHADOW_DEEP)
    m3.line(13, 0, 13, 15, BROWN_DARKEST)
    sheet.blit(m3, 48, 16)

    # Tile 4: Wood fill with dropped RED CRAYON jammed in seam!
    m4 = m0.clone()
    # Recessed shadow groove behind crayon
    m4.rect(1, 6, 14, 7, BROWN_DARKEST)
    m4.line(1, 12, 14, 12, OUTLINE)

    # Sharpened conical wax tip (x=2..3)
    m4.set_pixel(2, 9, OUTLINE)
    m4.set_pixel(3, 8, RED_LIGHT)
    m4.set_pixel(3, 9, RED_MID)
    m4.set_pixel(3, 10, RED_SHADOW)

    # Crayon wax body (x=4..13, y=7..11)
    for cx in range(4, 14):
        m4.set_pixel(cx, 7, RED_LIGHT)   # Top cylinder highlight
        m4.set_pixel(cx, 8, RED_MID)     # Body
        m4.set_pixel(cx, 9, RED_MID)
        m4.set_pixel(cx, 10, RED_SHADOW) # Bottom cylinder shadow
        m4.set_pixel(cx, 11, OUTLINE)    # Outline

    # Paper label wrapper around middle (x=6..11)
    for px in range(6, 12):
        m4.set_pixel(px, 7, PURE_WHITE)
        m4.set_pixel(px, 8, WHITE_SHADOW)
        m4.set_pixel(px, 9, WHITE_SHADOW)
        m4.set_pixel(px, 10, PURPLE_MID)
    # Crayon logo wavy oval band
    m4.set_pixel(8, 8, PURPLE_MID)
    m4.set_pixel(9, 8, PURPLE_MID)
    m4.set_pixel(8, 9, PURPLE_MID)
    m4.set_pixel(9, 9, PURPLE_MID)
    sheet.blit(m4, 64, 16)

    # Tile 5: Wood fill with stray BLUE LEGO BRICK / STUD!
    m5 = m0.clone()
    # Shadow under LEGO brick
    m5.line(3, 13, 13, 13, OUTLINE)
    m5.line(4, 14, 12, 14, SHADOW_DEEP)

    # 2x2 LEGO brick body (x=4..12, y=8..12)
    # Outline
    m5.rect(4, 8, 9, 5, BLUE_MID, outline=OUTLINE)
    # 3D bevels
    m5.line(5, 8, 11, 8, BLUE_LIGHT)    # Top edge
    m5.line(5, 9, 5, 11, BLUE_LIGHT)    # Left edge
    m5.line(11, 9, 11, 11, BLUE_SHADOW) # Right edge
    m5.line(5, 12, 11, 12, BLUE_SHADOW) # Bottom edge

    # 2 Studs on top of brick (x=5..7 and x=9..11, y=5..7)
    # Stud 1 (left)
    m5.rect(5, 5, 3, 3, BLUE_MID, outline=OUTLINE)
    m5.set_pixel(6, 5, BLUE_LIGHT)
    m5.set_pixel(5, 6, BLUE_LIGHT)
    m5.set_pixel(6, 6, PURE_WHITE)      # Specular gleam!
    m5.set_pixel(7, 6, BLUE_SHADOW)

    # Stud 2 (right)
    m5.rect(9, 5, 3, 3, BLUE_MID, outline=OUTLINE)
    m5.set_pixel(10, 5, BLUE_LIGHT)
    m5.set_pixel(9, 6, BLUE_LIGHT)
    m5.set_pixel(10, 6, PURE_WHITE)     # Specular gleam!
    m5.set_pixel(11, 6, BLUE_SHADOW)

    sheet.blit(m5, 80, 16)

    # Tile 6: Wood fill with dropped vintage penny wedged in seam
    m6 = m0.clone()
    # Recessed shadow crack
    m6.circle(8, 8, 3, BROWN_DARKEST)
    m6.line(6, 11, 10, 11, OUTLINE)
    # Penny
    coin_pts_m = [
        (7, 6), (8, 6), (9, 6),
        (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),
        (6, 8), (7, 8), (8, 8), (9, 8), (10, 8),
        (7, 9), (8, 9), (9, 9)
    ]
    for cx, cy in coin_pts_m:
        m6.set_pixel(cx, cy, YELLOW_MID)
    m6.set_pixel(7, 6, PURE_WHITE)
    m6.set_pixel(8, 6, YELLOW_LIGHT)
    m6.set_pixel(6, 7, YELLOW_LIGHT)
    m6.set_pixel(10, 8, YELLOW_SHADOW)
    m6.set_pixel(8, 9, BROWN_DARKEST)
    m6.set_pixel(9, 9, BROWN_DARKEST)
    sheet.blit(m6, 96, 16)

    # Tile 7: Wood fill with rustic iron framing nails
    m7 = m0.clone()
    # Large heavy nail at (8, 6)
    m7.rect(7, 5, 3, 3, WHITE_SHADOW, outline=OUTLINE)
    m7.set_pixel(7, 5, PURE_WHITE)
    m7.set_pixel(9, 7, SHADOW_DEEP)
    # Second nail at (11, 11)
    m7.rect(10, 10, 2, 2, WHITE_SHADOW, outline=OUTLINE)
    m7.set_pixel(10, 10, PURE_WHITE)
    sheet.blit(m7, 112, 16)

    # ================== ROW 2: DEEP FILL TILES ==================
    for col in range(8):
        b = PixelCanvas(16, 16)
        # Background gradient fading into subfloor void
        b.rect(0, 0, 16, 2, BROWN_DARKEST)
        b.rect(0, 2, 16, 3, SHADOW_DEEP)
        b.rect(0, 5, 16, 3, SHADOW_MID)
        b.rect(0, 8, 16, 4, OUTLINE)
        b.rect(0, 12, 16, 4, VOID_BLACK)

        # Fading vertical timber joist silhouettes
        for y in range(0, 8):
            b.set_pixel(3, y, BROWN_DARKEST if y < 4 else SHADOW_DEEP)
            b.set_pixel(4, y, BROWN_DARK if y < 3 else SHADOW_DEEP)
            b.set_pixel(11, y, BROWN_DARKEST if y < 4 else SHADOW_DEEP)
            b.set_pixel(12, y, OUTLINE)

        # Pit border edge shadows (col 2, 3)
        if col == 2:
            b.line(0, 0, 0, 15, VOID_BLACK)
            b.line(1, 0, 1, 15, VOID_BLACK)
            b.line(2, 0, 2, 15, OUTLINE)
        elif col == 3:
            b.line(15, 0, 15, 15, VOID_BLACK)
            b.line(14, 0, 14, 15, VOID_BLACK)
            b.line(13, 0, 13, 15, OUTLINE)
        elif col == 4:
            # Subtle hanging dust / cobweb strand
            b.line(15, 0, 12, 5, PURPLE_MID)
            b.line(12, 5, 10, 8, PURPLE_LIGHT)
            b.set_pixel(10, 8, WHITE_SHADOW)  # Caught dust speck
        elif col == 5:
            # Intricate corner cobweb spun in void
            # Primary anchor arc
            for wx, wy in [(0, 1), (1, 2), (2, 4), (4, 6), (6, 7), (8, 6), (11, 4), (13, 2), (15, 1)]:
                b.set_pixel(wx, wy, PURPLE_MID)
            # Secondary inner arc
            for wx, wy in [(0, 0), (2, 1), (4, 3), (6, 4), (8, 3), (10, 1), (12, 0)]:
                b.set_pixel(wx, wy, PURPLE_LIGHT)
            # Radial web spokes
            b.line(0, 0, 6, 7, PURPLE_MID)
            b.line(15, 0, 6, 7, PURPLE_MID)
            b.line(6, 0, 6, 7, PURPLE_LIGHT)
            # Caught dust motes in web
            b.set_pixel(6, 7, PURE_WHITE)
            b.set_pixel(4, 6, WHITE_SHADOW)
        elif col == 6:
            # Stray cobweb strand
            b.line(0, 1, 4, 5, PURPLE_MID)
            b.set_pixel(4, 5, WHITE_SHADOW)

        sheet.blit(b, col * 16, 32)

    return sheet

def generate_toy_blocks() -> PixelCanvas:
    """
    16x16 stackable alphabet toy blocks.
    4 vibrant colors (Red, Blue, Yellow, Green), 3 variants (Letter A, Letter B, Star).
    4 columns x 3 rows -> 64x48 px.
    Detailed 3D look: 1-2px bright bevel on top-left, dark bevel on bottom-right,
    selective outline, inset block face with crisp embossed letter & drop shadow.
    """
    sheet = PixelCanvas(64, 48, TRANSPARENT)

    colors = [
        # (fill, highlight, shadow, text_color, text_shadow, text_hi)
        (RED_MID, RED_LIGHT, RED_SHADOW, PURE_WHITE, RED_SHADOW, PURE_WHITE),
        (BLUE_MID, BLUE_LIGHT, BLUE_SHADOW, PURE_WHITE, BLUE_SHADOW, PURE_WHITE),
        # Yellow block: iconic red embossed lettering!
        (YELLOW_MID, YELLOW_LIGHT, YELLOW_SHADOW, RED_MID, YELLOW_SHADOW, RED_LIGHT),
        (GREEN_MID, GREEN_LIGHT, GREEN_SHADOW, PURE_WHITE, GREEN_SHADOW, PURE_WHITE),
    ]

    for col_idx, (c_fill, c_hi, c_sh, c_txt, c_tsh, c_thi) in enumerate(colors):
        for row_idx in range(3):
            b = PixelCanvas(16, 16, TRANSPARENT)

            # 1. Outer boundary with rounded friendly toy corners
            # Fill block body
            b.rect(1, 1, 14, 14, c_fill)

            # Perimeter selective outline
            b.line(1, 0, 14, 0, OUTLINE)    # Top
            b.line(1, 15, 14, 15, OUTLINE)  # Bottom
            b.line(0, 1, 0, 14, OUTLINE)    # Left
            b.line(15, 1, 15, 14, OUTLINE)  # Right
            # 1px clipped corners for rounded tactile feel
            b.set_pixel(1, 1, c_hi)
            b.set_pixel(14, 1, c_hi)
            b.set_pixel(1, 14, c_sh)
            b.set_pixel(14, 14, c_sh)

            # 2. Outer 3D Bevel (Light from upper-left)
            # Top-left bright bevel
            b.line(2, 1, 13, 1, c_hi)
            b.line(1, 2, 13, 2, c_hi)
            b.line(1, 2, 1, 13, c_hi)
            b.line(2, 2, 2, 13, c_hi)
            # Specular gleam at top-left corner
            b.set_pixel(2, 2, PURE_WHITE)

            # Bottom-right dark bevel
            b.line(1, 14, 14, 14, c_sh)
            b.line(2, 13, 14, 13, c_sh)
            b.line(14, 1, 14, 14, c_sh)
            b.line(13, 2, 13, 14, c_sh)

            # 3. Inset / Recessed block face (x=3..12, y=3..12)
            # Inner shadow at top and left of recess
            b.line(3, 3, 12, 3, c_sh)
            b.line(3, 3, 3, 12, c_sh)
            # Inner highlight at bottom and right of recess
            b.line(3, 12, 12, 12, c_hi)
            b.line(12, 3, 12, 12, c_hi)

            # Recessed field (x=4..11, y=4..11)
            b.rect(4, 4, 8, 8, c_fill)

            # 4. Embossed Symbol with 3D Drop Shadow
            # Coordinate center is at (7.5, 7.5)
            if row_idx == 0:
                # ================= Letter 'A' =================
                # Pattern coordinates:
                a_pts = [
                            (7, 4), (8, 4),
                    (6, 5),                 (9, 5),
                    (5, 6),                 (10, 6),
                    (5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),  # Crossbar
                    (5, 8),                 (10, 8),
                    (5, 9),                 (10, 9),
                    (4, 10), (5, 10),       (10, 10), (11, 10),       # Flared feet
                ]
                # Drop shadow (+1, +1)
                for sx, sy in a_pts:
                    if sx + 1 <= 11 and sy + 1 <= 11:
                        b.set_pixel(sx + 1, sy + 1, c_tsh)
                # Symbol body
                for sx, sy in a_pts:
                    b.set_pixel(sx, sy, c_txt)
                # Highlight on top edge of letter
                b.set_pixel(7, 4, c_thi)
                b.set_pixel(8, 4, c_thi)
                b.set_pixel(6, 5, c_thi)
                b.set_pixel(5, 6, c_thi)

            elif row_idx == 1:
                # ================= Letter 'B' =================
                b_pts = [
                    (5, 4), (6, 4), (7, 4), (8, 4), (9, 4),
                    (5, 5),                         (10, 5),
                    (5, 6),                         (10, 6),
                    (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
                    (5, 8),                         (10, 8),
                    (5, 9),                         (10, 9),
                    (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10),
                ]
                # Drop shadow (+1, +1)
                for sx, sy in b_pts:
                    if sx + 1 <= 11 and sy + 1 <= 11:
                        b.set_pixel(sx + 1, sy + 1, c_tsh)
                # Symbol body
                for sx, sy in b_pts:
                    b.set_pixel(sx, sy, c_txt)
                # Highlight on top edge
                b.set_pixel(5, 4, c_thi)
                b.set_pixel(6, 4, c_thi)
                b.set_pixel(7, 4, c_thi)
                b.set_pixel(8, 4, c_thi)
                b.set_pixel(5, 5, c_thi)
                b.set_pixel(5, 6, c_thi)

            else:
                # ================= Star '★' =================
                star_pts = [
                                    (7, 4), (8, 4),
                                    (7, 5), (8, 5),
                    (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (11, 6),
                            (5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),
                                    (6, 8), (7, 8), (8, 8), (9, 8),
                            (5, 9), (6, 9),         (9, 9), (10, 9),
                    (4, 10), (5, 10),                       (10, 10), (11, 10),
                ]
                # Drop shadow (+1, +1)
                for sx, sy in star_pts:
                    if sx + 1 <= 11 and sy + 1 <= 11:
                        b.set_pixel(sx + 1, sy + 1, c_tsh)
                # Symbol body
                for sx, sy in star_pts:
                    b.set_pixel(sx, sy, c_txt)
                # Center glint
                b.set_pixel(7, 4, c_thi)
                b.set_pixel(8, 4, c_thi)
                b.set_pixel(7, 7, c_thi)

            sheet.blit(b, col_idx * 16, row_idx * 16)

    return sheet

def generate_goal_flag() -> List[PixelCanvas]:
    """
    32x64 toy pennant flag on a classic #2 pencil pole.
    6 frames of flapping, 10 fps -> 192x64 px.
    Pencil pole at x=5..10, y=4..63.
    Pennant flag extends across x=11..30, flapping with continuous sinusoidal cloth wave physics.
    """
    frames = []

    for frame_idx in range(6):
        c = PixelCanvas(32, 64, TRANSPARENT)

        # ------------------ 1. PENCIL POLE ------------------
        # Eraser Top (y=4..9)
        # Rounded crown (y=4)
        c.line(6, 4, 8, 4, OUTLINE)
        c.line(6, 5, 8, 5, DUSK_PEACH)
        # Eraser body (y=5..9)
        for y in range(5, 10):
            c.set_pixel(5, y, OUTLINE)
            c.set_pixel(6, y, DUSK_PEACH)   # Lit facet
            c.set_pixel(7, y, DUSK_PINK)    # Mid facet
            c.set_pixel(8, y, DUSK_PINK)
            c.set_pixel(9, y, PURPLE_LIGHT) # Shadow facet
            c.set_pixel(10, y, OUTLINE)

        # Silver Metal Ferrule (y=10..14)
        for y in range(10, 15):
            c.set_pixel(5, y, OUTLINE)
            c.set_pixel(6, y, PURE_WHITE)    # Specular shine
            c.set_pixel(7, y, WHITE_SHADOW)  # Metal face
            c.set_pixel(8, y, WHITE_SHADOW)
            c.set_pixel(9, y, SHADOW_MID)    # Metal shadow
            c.set_pixel(10, y, OUTLINE)
        # Horizontal crimp bands indented across ferrule
        c.line(6, 11, 9, 11, SHADOW_DEEP)
        c.set_pixel(6, 11, PURE_WHITE)
        c.line(6, 13, 9, 13, SHADOW_DEEP)
        c.set_pixel(6, 13, PURE_WHITE)

        # Hexagonal Yellow Pencil Shaft (y=15..61)
        for y in range(15, 62):
            c.set_pixel(5, y, OUTLINE)
            c.set_pixel(6, y, YELLOW_LIGHT)   # Facet 1: Lit face
            c.set_pixel(7, y, YELLOW_MID)     # Facet 2: Center
            c.set_pixel(8, y, YELLOW_MID)
            c.set_pixel(9, y, YELLOW_SHADOW)  # Facet 3: Shadow face
            c.set_pixel(10, y, OUTLINE)

        # Green brand stamp imprint on pencil (y=34..38)
        for y in range(34, 39):
            c.set_pixel(7, y, GREEN_SHADOW)
            c.set_pixel(8, y, GREEN_SHADOW)

        # Sturdy Base Mount on floor (y=62..63)
        # Wooden collar
        c.line(4, 62, 11, 62, BROWN_MID)
        c.set_pixel(4, 62, OUTLINE)
        c.set_pixel(11, 62, OUTLINE)
        c.set_pixel(5, 62, BROWN_LIGHT)
        # Floor plate
        c.line(3, 63, 12, 63, BROWN_DARKEST)
        c.set_pixel(3, 63, OUTLINE)
        c.set_pixel(12, 63, OUTLINE)
        c.set_pixel(4, 63, BROWN_MID)

        # ------------------ 2. PENNANT FLAG ------------------
        # Dynamic sinusoidal wave animation
        phase = (frame_idx / 6.0) * 2.0 * math.pi
        xs = list(range(11, 31))
        y_tops = {}
        y_bots = {}
        slopes = {}
        y_centers = {}

        for x in xs:
            dist = x - 10
            norm_dist = dist / 20.0
            # Amplitude increases gently from 0.6px at pole to 2.8px at tip
            amp = 0.6 + 2.4 * norm_dist
            wave = math.sin(phase - dist * 0.35)
            slope = math.cos(phase - dist * 0.35)
            yc = 26.0 + amp * wave
            # Taper pennant height smoothly from 25px at pole down to 2px at tip
            h = max(2.0, 25.0 * (1.0 - norm_dist))
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
                is_edge = (y == span_top or y == span_bot or x == 30 or x == 11)
                if is_edge:
                    c.set_pixel(x, y, OUTLINE)
                else:
                    is_stripe = (abs(y - int(round(yc))) <= 1)
                    is_trim = (y == span_top + 1 or y == span_bot - 1)
                    if is_stripe or is_trim:
                        if slope > 0.2:
                            c.set_pixel(x, y, YELLOW_LIGHT)
                        elif slope < -0.2:
                            c.set_pixel(x, y, YELLOW_SHADOW)
                        else:
                            c.set_pixel(x, y, YELLOW_MID)
                    else:
                        if slope > 0.2:
                            c.set_pixel(x, y, RED_LIGHT)
                        elif slope < -0.2:
                            c.set_pixel(x, y, RED_SHADOW)
                        else:
                            c.set_pixel(x, y, RED_MID)

        # Star Insignia on flag (riding the wave near pole at x=16)
        star_cx = 16
        star_cy = int(round(y_centers[16]))
        c.set_pixel(star_cx, star_cy, PURE_WHITE)
        c.set_pixel(star_cx, star_cy - 1, YELLOW_LIGHT)
        c.set_pixel(star_cx, star_cy + 1, YELLOW_LIGHT)
        c.set_pixel(star_cx - 1, star_cy, YELLOW_LIGHT)
        c.set_pixel(star_cx + 1, star_cy, YELLOW_LIGHT)
        c.set_pixel(star_cx + 1, star_cy + 1, RED_SHADOW)
        c.set_pixel(star_cx, star_cy + 2, RED_SHADOW)

        # Flag hoist attachment rings to the pencil pole
        c.rect(10, 14, 2, 2, WHITE_SHADOW, outline=OUTLINE)
        c.rect(10, 37, 2, 2, WHITE_SHADOW, outline=OUTLINE)

        frames.append(c)

    return frames

def generate_pit_bg() -> PixelCanvas:
    """
    16x64 px strip that tiles horizontally.
    Deep subfloor pit background:
    - Upper subfloor gloom fading from floorboards.
    - Fluffy dust bunnies nestled under the joists.
    - Dangling lost kid's striped tube sock.
    - Faint yellow glowing eyes peering out of the deep void.
    - Seamless horizontal wrap and 100% fade to VOID_BLACK at bottom.
    """
    c = PixelCanvas(16, 64, VOID_BLACK)

    # 1. Background gradient into deep purple-black gloom
    for y in range(64):
        for x in range(16):
            if y < 4:
                c.set_pixel(x, y, OUTLINE if y == 0 else SHADOW_DEEP)
            elif y < 10:
                c.set_pixel(x, y, SHADOW_DEEP if (x + y) % 2 == 0 else SHADOW_MID)
            elif y < 22:
                c.set_pixel(x, y, SHADOW_MID if (x * 3 + y) % 4 == 0 else SHADOW_DEEP)
            elif y < 48:
                c.set_pixel(x, y, SHADOW_DEEP if (x * 5 + y) % 7 == 0 else OUTLINE)
            elif y < 58:
                c.set_pixel(x, y, OUTLINE if (x + y) % 5 == 0 else VOID_BLACK)
            else:
                c.set_pixel(x, y, VOID_BLACK)

    # 2. Dust bunnies accumulation (y=11..19)
    # Main fluffy clump centered at (8, 14)
    dust_pts = [
                 (7, 11), (8, 11), (9, 11),
         (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12), (11, 12),
         (4, 13), (5, 13), (6, 13), (7, 13), (8, 13), (9, 13), (10, 13), (11, 13),
         (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14),
                 (5, 15), (6, 15), (7, 15), (8, 15), (9, 15),
                          (6, 16), (7, 16), (8, 16)
    ]
    for dx, dy in dust_pts:
        c.set_pixel(dx, dy, SHADOW_DEEP)

    # Dust bunny soft highlight lobes
    for hx, hy in [(7, 12), (8, 12), (6, 13), (7, 13), (8, 13)]:
        c.set_pixel(hx, hy, SHADOW_MID)
    c.set_pixel(7, 12, PURPLE_MID)
    c.set_pixel(8, 12, PURPLE_MID)

    # Floating dust motes / hair fibers
    c.set_pixel(2, 10, PURPLE_LIGHT)
    c.set_pixel(3, 11, PURPLE_MID)
    c.set_pixel(13, 15, PURPLE_MID)
    c.set_pixel(14, 16, PURPLE_LIGHT)

    # 3. Dangling lost kid's striped tube sock (y=23..45)
    # Snag thread hanging from crack above
    c.set_pixel(7, 23, WHITE_SHADOW)

    # Sock ribbed cuff (y=24..26, x=5..9)
    for cx in range(5, 10):
        c.set_pixel(cx, 24, WHITE_SHADOW if cx % 2 == 0 else SHADOW_MID)
        c.set_pixel(cx, 25, PURE_WHITE if cx % 2 == 0 else WHITE_SHADOW)
        c.set_pixel(cx, 26, WHITE_SHADOW)

    # Sock leg body with bold retro stripes (y=27..36, x=5..10)
    for y in range(27, 37):
        # Determine stripe color
        if y in [27, 28, 31, 32, 35, 36]:
            # Blue stripe
            fill_c = BLUE_MID
            hi_c = BLUE_LIGHT
            sh_c = BLUE_SHADOW
        else:
            # White stripe
            fill_c = WHITE_SHADOW
            hi_c = PURE_WHITE
            sh_c = SHADOW_MID

        # Left outline / shadow
        c.set_pixel(5, y, sh_c)
        # Highlight facet
        c.set_pixel(6, y, hi_c)
        # Body
        c.set_pixel(7, y, fill_c)
        c.set_pixel(8, y, fill_c)
        # Right shadow
        c.set_pixel(9, y, sh_c)

    # Sock Heel (y=37..39): Red heel patch curving leftward (x=3..8)
    for y in range(37, 40):
        c.set_pixel(4, y, RED_SHADOW)
        c.set_pixel(5, y, RED_MID)
        c.set_pixel(6, y, RED_LIGHT if y == 37 else RED_MID)
        c.set_pixel(7, y, RED_MID)
        c.set_pixel(8, y, RED_SHADOW)
    c.set_pixel(3, 38, RED_SHADOW)

    # Sock Foot & Toe (y=40..45) drooping to the right
    # Foot arch (y=40..42, x=5..10)
    for y in range(40, 43):
        c.set_pixel(5, y, SHADOW_MID)
        c.set_pixel(6, y, WHITE_SHADOW)
        c.set_pixel(7, y, WHITE_SHADOW)
        c.set_pixel(8, y, WHITE_SHADOW)
        c.set_pixel(9, y, SHADOW_MID)

    # Red Toe Cap (y=43..45, x=6..10)
    c.set_pixel(6, 43, RED_SHADOW)
    c.set_pixel(7, 43, RED_LIGHT)
    c.set_pixel(8, 43, RED_MID)
    c.set_pixel(9, 43, RED_SHADOW)

    c.set_pixel(7, 44, RED_MID)
    c.set_pixel(8, 44, RED_MID)
    c.set_pixel(9, 44, RED_SHADOW)

    c.set_pixel(8, 45, RED_SHADOW)

    # 4. Faint glowing yellow eyes peering from the darkness (y=50..53)
    # Left eye at (4, 51..52), Right eye at (9, 51..52)
    # Eye glow aura
    for ex in [3, 4, 5, 8, 9, 10]:
        for ey in [50, 51, 52, 53]:
            if c.get_pixel(ex, ey) == VOID_BLACK:
                c.set_pixel(ex, ey, SHADOW_DEEP)

    # Left eye
    c.set_pixel(4, 51, PURE_WHITE)     # Glistening pupil/glint
    c.set_pixel(5, 51, YELLOW_MID)
    c.set_pixel(4, 52, YELLOW_MID)
    c.set_pixel(5, 52, YELLOW_SHADOW)

    # Right eye
    c.set_pixel(9, 51, PURE_WHITE)     # Glistening pupil/glint
    c.set_pixel(10, 51, YELLOW_MID)
    c.set_pixel(9, 52, YELLOW_MID)
    c.set_pixel(10, 52, YELLOW_SHADOW)

    # 5. Seamless horizontal border wrap check
    # Ensure pixels at x=0 and x=15 have zero abrupt edges
    for y in range(64):
        p0 = c.get_pixel(0, y)
        p15 = c.get_pixel(15, y)
        if y < 48 and p0 != p15:
            # Harmonize background border
            avg_color = SHADOW_DEEP if y < 22 else OUTLINE
            c.set_pixel(0, y, avg_color)
            c.set_pixel(15, y, avg_color)

    # Absolute fade to VOID_BLACK for y >= 57
    for y in range(57, 64):
        for x in range(16):
            c.set_pixel(x, y, VOID_BLACK)

    return c

def generate_all_environment_tiles():
    # tileset_floor.png
    floor = generate_tileset_floor()
    floor.to_image().save("art/incoming/tileset_floor.png", "PNG")
    print(f"Saved art/incoming/tileset_floor.png ({floor.width}x{floor.height})")

    # toy_blocks.png
    blocks = generate_toy_blocks()
    blocks.to_image().save("art/incoming/toy_blocks.png", "PNG")
    print(f"Saved art/incoming/toy_blocks.png ({blocks.width}x{blocks.height})")

    # goal_flag.png
    flag_frames = generate_goal_flag()
    assemble_strip(flag_frames, "art/incoming/goal_flag.png")

    # pit_bg.png
    pit = generate_pit_bg()
    pit.to_image().save("art/incoming/pit_bg.png", "PNG")
    print(f"Saved art/incoming/pit_bg.png ({pit.width}x{pit.height})")

if __name__ == "__main__":
    generate_all_environment_tiles()
