"""Younger Sibling Simulator - Power-up Items & Glow Generator.

Elevated pixel art for Power-up Items & Pops:
- All items in 24x24 frames, centered, rich lighting and rim highlights.
- item_boots.png (24x24, 6f, 8fps, loop: true) - chunky winged orange sneaker, lightning bolt stripe, bobbing float, glint sweep.
- item_boots_pop.png (24x24, 3f, 24fps, loop: false) - starburst pop with sneaker wing and sole fragments.
- item_feather.png (24x24, 6f, 8fps, loop: true) - cyan-white plume with golden quill, barb details, glint sweep.
- item_feather_pop.png (24x24, 3f, 24fps, loop: false) - feather dissolving into glowing plume sparkles.
- item_coin.png (24x24, 6f, 8fps, loop: true) - 3D spinning gold coin (full face -> 3/4 -> 1/4 -> edge-on with milled ridges -> reverse), embossed star.
- item_coin_pop.png (24x24, 3f, 24fps, loop: false) - sparkling coin pop.
- item_glow.png (32x32, 1 frame) - concentric soft circular glow using 4 discrete hard bands.
- Strictly follows 32-color palette from tools/palette.py.
"""

import math
from typing import List
from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE,
    ORANGE_SHADOW, ORANGE_MID,
    YELLOW_SHADOW, YELLOW_MID, YELLOW_LIGHT,
    BLUE_SHADOW, BLUE_LIGHT,
    WHITE_SHADOW, PURE_WHITE,
    WOOD_HIGHLIGHT, BROWN_DARK, SHADOW_DEEP
)


def create_item_canvas() -> PixelCanvas:
    return PixelCanvas(24, 24, TRANSPARENT)


# ==============================================================================
# 1. BOOTS (SPEED POWER-UP) & POP
# ==============================================================================

def generate_item_boots() -> List[PixelCanvas]:
    """
    6 frames, 8 fps.
    Chunky winged orange high-top sneaker with lightning bolt side stripe.
    Bobbing float and sweeping glint across wing, collar, bolt, and toe.
    """
    frames = []
    bobs = [0, -1, -2, -2, -1, 0]

    for f_idx in range(6):
        c = create_item_canvas()
        by = bobs[f_idx]
        cx = 12
        cy = 12 + by

        # 1. Hermes Wing at Heel (x: cx-10..cx-4, y: cy-7..cy-1)
        # Top feather plume
        c.set_pixel(cx - 9, cy - 6, OUTLINE)
        c.set_pixel(cx - 8, cy - 6, PURE_WHITE)
        c.set_pixel(cx - 7, cy - 6, PURE_WHITE)
        c.set_pixel(cx - 6, cy - 6, OUTLINE)

        c.set_pixel(cx - 10, cy - 5, OUTLINE)
        c.set_pixel(cx - 9, cy - 5, PURE_WHITE)
        c.set_pixel(cx - 8, cy - 5, PURE_WHITE)
        c.set_pixel(cx - 7, cy - 5, BLUE_LIGHT)
        c.set_pixel(cx - 6, cy - 5, OUTLINE)

        # Mid feather plume
        c.set_pixel(cx - 9, cy - 4, OUTLINE)
        c.set_pixel(cx - 8, cy - 4, BLUE_LIGHT)
        c.set_pixel(cx - 7, cy - 4, PURE_WHITE)
        c.set_pixel(cx - 6, cy - 4, BLUE_LIGHT)
        c.set_pixel(cx - 5, cy - 4, OUTLINE)

        # Low feather plume
        c.set_pixel(cx - 8, cy - 3, OUTLINE)
        c.set_pixel(cx - 7, cy - 3, BLUE_LIGHT)
        c.set_pixel(cx - 6, cy - 3, BLUE_SHADOW)
        c.set_pixel(cx - 5, cy - 3, OUTLINE)

        c.set_pixel(cx - 7, cy - 2, OUTLINE)
        c.set_pixel(cx - 6, cy - 2, BLUE_SHADOW)
        c.set_pixel(cx - 5, cy - 2, OUTLINE)

        # 2. High-top Collar & Tongue
        c.set_pixel(cx - 4, cy - 5, OUTLINE)
        c.set_pixel(cx - 3, cy - 5, PURE_WHITE)
        c.set_pixel(cx - 2, cy - 5, PURE_WHITE)
        c.set_pixel(cx - 1, cy - 5, PURE_WHITE)
        c.set_pixel(cx, cy - 5, OUTLINE)
        c.set_pixel(cx - 3, cy - 4, OUTLINE)
        c.set_pixel(cx - 2, cy - 4, SHADOW_DEEP)
        c.set_pixel(cx - 1, cy - 4, OUTLINE)

        # Tongue & Criss-cross Laces
        c.set_pixel(cx, cy - 4, ORANGE_MID)
        c.set_pixel(cx + 1, cy - 4, OUTLINE)
        c.set_pixel(cx - 1, cy - 3, PURE_WHITE)  # Lace 1
        c.set_pixel(cx, cy - 3, ORANGE_MID)
        c.set_pixel(cx + 1, cy - 3, PURE_WHITE)  # Lace 1
        c.set_pixel(cx + 2, cy - 3, OUTLINE)
        c.set_pixel(cx, cy - 2, PURE_WHITE)      # Lace 2
        c.set_pixel(cx + 1, cy - 2, ORANGE_MID)
        c.set_pixel(cx + 2, cy - 2, PURE_WHITE)  # Lace 2
        c.set_pixel(cx + 3, cy - 2, OUTLINE)

        # 3. Orange Upper Body
        for y in range(cy - 4, cy + 3):
            c.set_pixel(cx - 5, y, OUTLINE)
            c.set_pixel(cx - 4, y, ORANGE_MID if y < cy else ORANGE_SHADOW)
        for y in range(cy - 2, cy + 3):
            for x in range(cx - 3, cx + 6):
                if y == cy - 2 and x > cx + 2:
                    continue
                if y == cy - 1 and x > cx + 4:
                    continue
                if y <= cy - 1:
                    c.set_pixel(x, y, WOOD_HIGHLIGHT if x == cx else ORANGE_MID)
                elif y >= cy + 1:
                    c.set_pixel(x, y, ORANGE_SHADOW)
                else:
                    c.set_pixel(x, y, ORANGE_MID)

        # 4. Bold Lightning Bolt Side Stripe
        c.set_pixel(cx - 3, cy + 1, YELLOW_LIGHT)
        c.set_pixel(cx - 2, cy + 1, YELLOW_LIGHT)
        c.set_pixel(cx - 1, cy, YELLOW_LIGHT)
        c.set_pixel(cx, cy - 1, PURE_WHITE if f_idx == 2 else YELLOW_LIGHT)  # Bolt apex
        c.set_pixel(cx + 1, cy - 1, YELLOW_MID)
        c.set_pixel(cx, cy, YELLOW_MID)
        c.set_pixel(cx + 1, cy, YELLOW_LIGHT)
        c.set_pixel(cx + 2, cy, PURE_WHITE if f_idx == 3 else YELLOW_LIGHT)
        c.set_pixel(cx + 3, cy + 1, YELLOW_MID)
        c.set_pixel(cx + 4, cy + 1, YELLOW_LIGHT)

        # 5. White Shell Toe Cap
        c.set_pixel(cx + 5, cy, OUTLINE)
        c.set_pixel(cx + 6, cy, OUTLINE)
        c.set_pixel(cx + 5, cy + 1, PURE_WHITE)
        c.set_pixel(cx + 6, cy + 1, PURE_WHITE)
        c.set_pixel(cx + 7, cy + 1, OUTLINE)
        c.set_pixel(cx + 5, cy + 2, WHITE_SHADOW)
        c.set_pixel(cx + 6, cy + 2, WHITE_SHADOW)
        c.set_pixel(cx + 7, cy + 2, OUTLINE)

        # 6. Chunky White Rubber Midsole & Outsole
        for x in range(cx - 5, cx + 7):
            c.set_pixel(x, cy + 3, PURE_WHITE if x >= cx - 2 else WHITE_SHADOW)
            c.set_pixel(x, cy + 4, WHITE_SHADOW if x % 2 == 0 else PURE_WHITE)
            c.set_pixel(x, cy + 5, OUTLINE)  # Dark bottom tread
        c.set_pixel(cx - 6, cy + 3, OUTLINE)
        c.set_pixel(cx - 6, cy + 4, OUTLINE)
        c.set_pixel(cx + 7, cy + 3, OUTLINE)
        c.set_pixel(cx + 7, cy + 4, OUTLINE)

        # 7. Glint Sweep
        if f_idx == 0:
            c.set_pixel(cx - 8, cy - 7, PURE_WHITE)  # Star glint on wing
            c.set_pixel(cx - 8, cy - 8, YELLOW_LIGHT)
            c.set_pixel(cx - 9, cy - 7, YELLOW_LIGHT)
            c.set_pixel(cx - 7, cy - 7, YELLOW_LIGHT)
        elif f_idx == 1:
            c.set_pixel(cx - 2, cy - 6, PURE_WHITE)  # Collar rim flash
        elif f_idx == 4:
            c.set_pixel(cx + 6, cy, PURE_WHITE)      # Toe cap shine
        elif f_idx == 5:
            c.set_pixel(cx + 8, cy + 1, PURE_WHITE)  # Star sparkle off toe tip
            c.set_pixel(cx + 8, cy, YELLOW_LIGHT)
            c.set_pixel(cx + 9, cy + 1, YELLOW_LIGHT)
            c.set_pixel(cx + 8, cy + 2, YELLOW_LIGHT)

        frames.append(c)
    return frames


def generate_item_boots_pop() -> List[PixelCanvas]:
    """
    3 frames, 24 fps.
    Starburst pop with sneaker wing/sole fragments and dissolving glitter.
    """
    frames = []
    cx, cy = 12, 12

    # Frame 0: Flash and expand
    c0 = create_item_canvas()
    c0.circle(cx, cy, 6, PURE_WHITE, outline=YELLOW_LIGHT)
    c0.line(cx - 9, cy, cx + 9, cy, PURE_WHITE)
    c0.line(cx, cy - 9, cx, cy + 9, PURE_WHITE)
    for dx, dy in [(-5, -5), (5, -5), (-5, 5), (5, 5)]:
        c0.set_pixel(cx + dx, cy + dy, YELLOW_LIGHT)
        c0.set_pixel(cx + dx // 2, cy + dy // 2, PURE_WHITE)
    frames.append(c0)

    # Frame 1: Exploding starburst with sneaker wing and sole fragments
    c1 = create_item_canvas()
    spikes = [(-10, 0), (10, 0), (0, -10), (0, 10), (-7, -7), (7, -7), (-7, 7), (7, 7)]
    for sx, sy in spikes:
        c1.set_pixel(cx + sx, cy + sy, YELLOW_LIGHT)
        c1.set_pixel(cx + sx * 2 // 3, cy + sy * 2 // 3, PURE_WHITE)
    # Wing fragment (up-left)
    c1.set_pixel(cx - 7, cy - 6, PURE_WHITE)
    c1.set_pixel(cx - 8, cy - 5, BLUE_LIGHT)
    c1.set_pixel(cx - 7, cy - 5, BLUE_SHADOW)
    # Sole chunk (down-left)
    c1.set_pixel(cx - 6, cy + 7, PURE_WHITE)
    c1.set_pixel(cx - 5, cy + 7, WHITE_SHADOW)
    c1.set_pixel(cx - 6, cy + 8, OUTLINE)
    # Orange leather collar shard (up-right)
    c1.set_pixel(cx + 6, cy - 6, ORANGE_MID)
    c1.set_pixel(cx + 7, cy - 5, ORANGE_SHADOW)
    # Lightning spark (right)
    c1.set_pixel(cx + 8, cy + 1, YELLOW_LIGHT)
    c1.set_pixel(cx + 7, cy + 2, YELLOW_MID)
    frames.append(c1)

    # Frame 2: Outer sparkles dispersing
    c2 = create_item_canvas()
    outer_sparks = [
        (-10, -8), (-8, -10), (8, -10), (10, -8),
        (10, 8), (8, 10), (-8, 10), (-10, 8),
        (0, -11), (0, 11), (-11, 0), (11, 0)
    ]
    for ox, oy in outer_sparks:
        c2.set_pixel(cx + ox, cy + oy, YELLOW_LIGHT if (ox + oy) % 2 == 0 else WHITE_SHADOW)
    frames.append(c2)

    return frames


# ==============================================================================
# 2. FEATHER (LIGHTWEIGHT POWER-UP) & POP
# ==============================================================================

def generate_item_feather() -> List[PixelCanvas]:
    """
    6 frames, 8 fps.
    Cyan-white plume with golden quill nib and shaft, realistic barb notches, and glint sweep.
    """
    frames = []
    bobs = [0, -1, -2, -2, -1, 0]

    vane_data = [
        # (dy, sx, lx, rx, notch_l, notch_r)
        (7, -6, -6, -5, False, False),
        (6, -5, -6, -4, False, False),
        (5, -4, -7, -2, False, False),
        (4, -3, -8, 0, True, False),
        (3, -2, -9, 2, False, True),
        (2, -1, -9, 3, False, False),
        (1, 0, -9, 4, True, False),
        (0, 1, -8, 5, False, True),
        (-1, 2, -7, 5, False, False),
        (-2, 3, -5, 6, True, False),
        (-3, 3, -4, 6, False, True),
        (-4, 4, -2, 6, False, False),
        (-5, 4, -1, 6, True, False),
        (-6, 5, 1, 6, False, False),
        (-7, 5, 3, 6, False, False),
    ]

    for f_idx in range(6):
        c = create_item_canvas()
        by = bobs[f_idx]
        cx = 12
        cy = 12 + by

        # 1. Golden Quill Nib at bottom-left
        c.set_pixel(cx - 7, cy + 9, OUTLINE)
        c.set_pixel(cx - 6, cy + 9, YELLOW_LIGHT)
        c.set_pixel(cx - 6, cy + 8, YELLOW_MID)
        c.set_pixel(cx - 5, cy + 8, YELLOW_SHADOW)
        c.set_pixel(cx - 6, cy + 7, OUTLINE)  # Nib slit

        # 2. Vanes & Golden Rachis
        for dy, dsx, dlx, drx, notch_l, notch_r in vane_data:
            y = cy + dy
            sx = cx + dsx
            lx = cx + dlx + (1 if notch_l else 0)
            rx = cx + drx - (1 if notch_r else 0)

            c.set_pixel(lx - 1, y, OUTLINE)
            c.set_pixel(rx + 1, y, OUTLINE)

            # Upper vane (lit cyan-white)
            for x in range(lx, sx):
                dist_from_cx = x - cx
                glint_target = (f_idx * 3 - 7)
                is_glint = (abs(dist_from_cx - glint_target) <= 1)

                if is_glint:
                    c.set_pixel(x, y, PURE_WHITE)
                elif x >= sx - 2:
                    c.set_pixel(x, y, WHITE_SHADOW)
                elif x >= sx - 5:
                    c.set_pixel(x, y, PURE_WHITE)
                else:
                    c.set_pixel(x, y, BLUE_LIGHT)

            # Golden spine (rachis)
            is_spine_glint = (f_idx in [1, 2] and abs(dy) <= 2)
            c.set_pixel(sx, y, PURE_WHITE if is_spine_glint else YELLOW_MID)

            # Lower vane (shadow blue)
            for x in range(sx + 1, rx + 1):
                if x <= sx + 2:
                    c.set_pixel(x, y, BLUE_LIGHT)
                else:
                    c.set_pixel(x, y, BLUE_SHADOW)

        # 3. Curled Tip
        c.set_pixel(cx + 5, cy - 8, PURE_WHITE)
        c.set_pixel(cx + 6, cy - 8, PURE_WHITE)
        c.set_pixel(cx + 7, cy - 8, OUTLINE)
        c.set_pixel(cx + 6, cy - 9, PURE_WHITE)
        c.set_pixel(cx + 5, cy - 9, OUTLINE)
        c.set_pixel(cx + 7, cy - 9, OUTLINE)

        # 4. Glint Sparkles
        if f_idx == 0:
            c.set_pixel(cx - 7, cy + 9, PURE_WHITE)
            c.set_pixel(cx - 8, cy + 9, YELLOW_LIGHT)
        elif f_idx == 5:
            c.set_pixel(cx + 7, cy - 10, PURE_WHITE)
            c.set_pixel(cx + 6, cy - 10, BLUE_LIGHT)
            c.set_pixel(cx + 8, cy - 10, BLUE_LIGHT)

        frames.append(c)
    return frames


def generate_item_feather_pop() -> List[PixelCanvas]:
    """
    3 frames, 24 fps.
    Feather dissolving into glowing plume sparkles and floating down wisps.
    """
    frames = []
    cx, cy = 12, 12

    # Frame 0: Flash and radiant cyan beams
    c0 = create_item_canvas()
    c0.circle(cx, cy, 6, PURE_WHITE, outline=BLUE_LIGHT)
    c0.line(cx - 9, cy, cx + 9, cy, BLUE_LIGHT)
    c0.line(cx, cy - 9, cx, cy + 9, BLUE_LIGHT)
    c0.line(cx - 6, cy - 6, cx + 6, cy + 6, PURE_WHITE)
    frames.append(c0)

    # Frame 1: Feather dissolving into floating plume down & golden quill sparks
    c1 = create_item_canvas()
    wisps = [
        (-6, -6, PURE_WHITE), (-7, -3, BLUE_LIGHT),
        (5, -6, PURE_WHITE), (6, -4, BLUE_LIGHT),
        (-4, 6, BLUE_LIGHT), (-5, 7, BLUE_SHADOW),
        (4, 5, PURE_WHITE), (6, 6, BLUE_LIGHT),
        (0, -8, PURE_WHITE), (0, 8, BLUE_LIGHT)
    ]
    for wx, wy, col in wisps:
        c1.set_pixel(cx + wx, cy + wy, col)
        c1.set_pixel(cx + wx + (1 if wx < 0 else -1), cy + wy, WHITE_SHADOW)
    c1.set_pixel(cx - 2, cy + 2, YELLOW_LIGHT)
    c1.set_pixel(cx - 3, cy + 3, YELLOW_MID)
    c1.set_pixel(cx + 2, cy - 2, YELLOW_LIGHT)
    frames.append(c1)

    # Frame 2: Dispersing glowing plume dust
    c2 = create_item_canvas()
    dust = [
        (-9, -8), (9, -8), (-8, 9), (8, 9),
        (-10, 0), (10, 0), (0, -10), (0, 10),
        (-6, -6), (6, -6), (-6, 6), (6, 6)
    ]
    for dx, dy in dust:
        c2.set_pixel(cx + dx, cy + dy, BLUE_LIGHT if (dx + dy) % 2 == 0 else WHITE_SHADOW)
    frames.append(c2)

    return frames


# ==============================================================================
# 3. COIN (SCORE POWER-UP) & POP
# ==============================================================================

def generate_item_coin() -> List[PixelCanvas]:
    """
    6 frames, 8 fps.
    3D spinning gold coin with embossed star.
    Frame 0: Full circular face with faceted 5-point star.
    Frame 1: 3/4 view with 3D edge rim.
    Frame 2: 1/4 view with compressed diamond star gleam.
    Frame 3: Edge-on view with milled reeded edge ridges!
    Frame 4: Reverse 1/4 view.
    Frame 5: Reverse 3/4 view.
    """
    frames = []
    bobs = [0, -1, -2, -2, -1, 0]
    hh = 6.8
    hw_map = [6.8, 4.8, 2.4, 0.0, 2.4, 4.8]

    for f_idx in range(6):
        c = create_item_canvas()
        by = bobs[f_idx]
        cx = 12
        cy = 12 + by
        hw = hw_map[f_idx]

        if f_idx == 3:
            # FRAME 3: EDGE-ON VIEW WITH MILLED RIDGES!
            for y in range(cy - 6, cy + 7):
                is_ridge = (y % 2 == 0)
                c.set_pixel(cx - 2, y, YELLOW_LIGHT)
                if is_ridge:
                    c.set_pixel(cx - 1, y, YELLOW_LIGHT)
                    c.set_pixel(cx, y, YELLOW_MID)
                else:
                    c.set_pixel(cx - 1, y, YELLOW_SHADOW)
                    c.set_pixel(cx, y, BROWN_DARK)
                c.set_pixel(cx + 1, y, YELLOW_SHADOW)
                c.set_pixel(cx + 2, y, OUTLINE)

            c.set_pixel(cx - 1, cy - 7, OUTLINE)
            c.set_pixel(cx, cy - 7, OUTLINE)
            c.set_pixel(cx - 1, cy + 7, OUTLINE)
            c.set_pixel(cx, cy + 7, OUTLINE)
            c.set_pixel(cx - 3, cy, OUTLINE)
            frames.append(c)
            continue

        has_edge_right = (f_idx in [1, 2])
        has_edge_left = (f_idx in [4, 5])
        edge_thickness = 2 if f_idx in [1, 5] else 3

        # 3D cylindrical edge
        if has_edge_right:
            for y in range(cy - 6, cy + 7):
                dy = (y - cy) / hh
                if abs(dy) > 0.95:
                    continue
                cur_hw = math.sqrt(max(0.0, 1.0 - dy * dy)) * hw
                x_face_right = int(round(cx + cur_hw))
                for ex in range(x_face_right, x_face_right + edge_thickness):
                    if y <= cy - 3:
                        c.set_pixel(ex, y, YELLOW_LIGHT)
                    elif y >= cy + 2:
                        c.set_pixel(ex, y, YELLOW_SHADOW)
                    else:
                        c.set_pixel(ex, y, YELLOW_MID)
                c.set_pixel(x_face_right + edge_thickness, y, OUTLINE)
        elif has_edge_left:
            for y in range(cy - 6, cy + 7):
                dy = (y - cy) / hh
                if abs(dy) > 0.95:
                    continue
                cur_hw = math.sqrt(max(0.0, 1.0 - dy * dy)) * hw
                x_face_left = int(round(cx - cur_hw))
                for ex in range(x_face_left - edge_thickness + 1, x_face_left + 1):
                    if y <= cy - 3:
                        c.set_pixel(ex, y, YELLOW_LIGHT)
                    elif y >= cy + 2:
                        c.set_pixel(ex, y, YELLOW_SHADOW)
                    else:
                        c.set_pixel(ex, y, YELLOW_MID)
            c.set_pixel(x_face_left - edge_thickness, y, OUTLINE)

        # Elliptical coin face
        for y in range(cy - 7, cy + 8):
            dy = (y - cy) / hh
            if abs(dy) > 1.0:
                continue
            cur_hw = math.sqrt(max(0.0, 1.0 - dy * dy)) * hw
            x_left = int(round(cx - cur_hw))
            x_right = int(round(cx + cur_hw))

            if not has_edge_left:
                c.set_pixel(x_left - 1, y, OUTLINE)
            if not has_edge_right:
                c.set_pixel(x_right + 1, y, OUTLINE)
            if y == cy - 7 or y == cy + 7:
                c.set_pixel(cx, y - 1 if y < cy else y + 1, OUTLINE)

            for x in range(x_left, x_right + 1):
                is_rim = (x == x_left or x == x_right or y == cy - 6 or y == cy + 6)
                if is_rim:
                    if y <= cy and x <= cx:
                        c.set_pixel(x, y, YELLOW_LIGHT)
                    elif y >= cy and x >= cx:
                        c.set_pixel(x, y, YELLOW_SHADOW)
                    else:
                        c.set_pixel(x, y, YELLOW_MID)
                else:
                    c.set_pixel(x, y, YELLOW_MID)

        # Embossed Star
        if f_idx == 0:
            c.set_pixel(cx, cy, PURE_WHITE)
            c.set_pixel(cx, cy - 3, YELLOW_LIGHT); c.set_pixel(cx, cy - 2, YELLOW_LIGHT); c.set_pixel(cx, cy - 1, YELLOW_LIGHT)
            c.set_pixel(cx - 3, cy - 1, YELLOW_LIGHT); c.set_pixel(cx - 2, cy - 1, YELLOW_LIGHT); c.set_pixel(cx - 1, cy - 1, YELLOW_LIGHT)
            c.set_pixel(cx + 1, cy - 1, YELLOW_LIGHT); c.set_pixel(cx + 2, cy - 1, YELLOW_MID); c.set_pixel(cx + 3, cy - 1, YELLOW_SHADOW)
            c.set_pixel(cx - 2, cy + 2, YELLOW_LIGHT); c.set_pixel(cx - 1, cy + 1, YELLOW_LIGHT)
            c.set_pixel(cx + 2, cy + 2, YELLOW_SHADOW); c.set_pixel(cx + 1, cy + 1, YELLOW_SHADOW)
            c.set_pixel(cx - 1, cy - 2, YELLOW_LIGHT); c.set_pixel(cx + 1, cy - 2, YELLOW_MID)
        elif f_idx in [1, 5]:
            c.set_pixel(cx, cy, PURE_WHITE)
            c.set_pixel(cx, cy - 2, YELLOW_LIGHT); c.set_pixel(cx, cy - 1, YELLOW_LIGHT)
            c.set_pixel(cx, cy + 1, YELLOW_SHADOW); c.set_pixel(cx, cy + 2, YELLOW_SHADOW)
            c.set_pixel(cx - 1, cy, YELLOW_LIGHT); c.set_pixel(cx + 1, cy, YELLOW_SHADOW)
        elif f_idx in [2, 4]:
            c.set_pixel(cx, cy - 1, YELLOW_LIGHT)
            c.set_pixel(cx, cy, PURE_WHITE)
            c.set_pixel(cx, cy + 1, YELLOW_LIGHT)

        frames.append(c)
    return frames


def generate_item_coin_pop() -> List[PixelCanvas]:
    """
    3 frames, 24 fps.
    Sparkling gold coin pop with exploding shards and sparkling dust ring.
    """
    frames = []
    cx, cy = 12, 12

    # Frame 0: Golden flash
    c0 = create_item_canvas()
    c0.circle(cx, cy, 6, PURE_WHITE, outline=YELLOW_LIGHT)
    c0.line(cx - 9, cy, cx + 9, cy, YELLOW_LIGHT)
    c0.line(cx, cy - 9, cx, cy + 9, YELLOW_LIGHT)
    c0.line(cx - 6, cy - 6, cx + 6, cy + 6, PURE_WHITE)
    frames.append(c0)

    # Frame 1: Exploding golden shards & sparkles
    c1 = create_item_canvas()
    sparks = [
        (-8, -8), (0, -10), (8, -8),
        (10, 0), (8, 8), (0, 10),
        (-8, 8), (-10, 0)
    ]
    for sx, sy in sparks:
        c1.set_pixel(cx + sx, cy + sy, YELLOW_LIGHT)
        c1.set_pixel(cx + sx * 2 // 3, cy + sy * 2 // 3, YELLOW_MID)
    c1.set_pixel(cx - 3, cy - 3, PURE_WHITE)
    c1.set_pixel(cx + 3, cy + 3, YELLOW_SHADOW)
    c1.set_pixel(cx - 4, cy + 2, YELLOW_LIGHT)
    c1.set_pixel(cx + 4, cy - 2, YELLOW_MID)
    frames.append(c1)

    # Frame 2: Outer sparkling gold dust ring
    c2 = create_item_canvas()
    dust = [
        (-10, -9), (10, -9), (-9, 10), (9, 10),
        (-11, 0), (11, 0), (0, -11), (0, 11),
        (-7, -7), (7, -7), (-7, 7), (7, 7)
    ]
    for dx, dy in dust:
        c2.set_pixel(cx + dx, cy + dy, PURE_WHITE if (dx + dy) % 2 == 0 else YELLOW_LIGHT)
    frames.append(c2)

    return frames


# ==============================================================================
# 4. ITEM GLOW
# ==============================================================================

def generate_item_glow() -> PixelCanvas:
    """
    32x32 soft circular glow using 4 discrete hard bands (no smooth gradient).
    Pure white on transparent, tinted dynamically by the engine.
    """
    c = PixelCanvas(32, 32, TRANSPARENT)
    cx, cy = 15.5, 15.5

    for y in range(32):
        for x in range(32):
            d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            if d <= 3.5:
                c.set_pixel(x, y, (255, 255, 255, 255))
            elif d <= 7.0:
                c.set_pixel(x, y, (255, 255, 255, 192))
            elif d <= 11.0:
                c.set_pixel(x, y, (255, 255, 255, 115))
            elif d <= 15.0:
                c.set_pixel(x, y, (255, 255, 255, 45))
            else:
                c.set_pixel(x, y, TRANSPARENT)

    return c


def generate_all_items():
    animations = {
        "art/incoming/item_boots.png": generate_item_boots(),
        "art/incoming/item_boots_pop.png": generate_item_boots_pop(),
        "art/incoming/item_feather.png": generate_item_feather(),
        "art/incoming/item_feather_pop.png": generate_item_feather_pop(),
        "art/incoming/item_coin.png": generate_item_coin(),
        "art/incoming/item_coin_pop.png": generate_item_coin_pop(),
    }
    for path, frames in animations.items():
        assemble_strip(frames, path)

    glow = generate_item_glow()
    glow.to_image().save("art/incoming/item_glow.png", "PNG")
    print("Saved art/incoming/item_glow.png (32x32, 1 frame)")


if __name__ == "__main__":
    generate_all_items()
