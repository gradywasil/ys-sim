"""Younger Sibling Simulator - Power-up Items & Glow Generator v2.

Elevated pixel art for Power-up Items & Pops at v2 resolution:
- All items in 48x48 frames, centered, rich lighting and rim highlights.
- item_boots.png (48x48, 6 frames, 8 fps, loop: true) - chunky winged orange sneaker, Hermes wings, yellow lightning bolt, rubber sole tread, bobbing float, glint sweep.
- item_boots_pop.png (48x48, 3 frames, 24 fps, loop: false) - starburst pop with flying wing feathers and rubber fragments.
- item_feather.png (48x48, 6 frames, 8 fps, loop: true) - curved cyan-white plume with golden quill nib and slit, individual barb notches, glint sweep.
- item_feather_pop.png (48x48, 3 frames, 24 fps, loop: false) - plume dissolving into starry sparkle burst.
- item_coin.png (48x48, 6 frames, 8 fps, loop: true) - 3D spinning gold coin (full face -> 3/4 -> 1/4 -> edge-on with milled reeded ridges -> reverse), embossed star.
- item_coin_pop.png (48x48, 3 frames, 24 fps, loop: false) - golden coin flash with exploding starburst shards.
- item_glow.png (64x64, 1 frame) - concentric soft circular glow using 4 discrete hard alpha bands (255, 192, 115, 45).
- Strictly follows 64-color palette from tools/palette.py.
"""

import math
from typing import List, Tuple
from PIL import Image
from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE, VOID_BLACK,
    SHADOW_PURPLE_DARK, SHADOW_PURPLE_DEEP, SHADOW_PURPLE_MID,
    PURPLE_DARK, PURPLE_MID, PURPLE_LIGHT,
    ORANGE_DEEP, ORANGE_SHADOW, ORANGE_MID, ORANGE_LIGHT,
    YELLOW_DEEP, YELLOW_SHADOW, YELLOW_RICH, YELLOW_MID, YELLOW_LIGHT, YELLOW_HIGHLIGHT,
    BROWN_DARKEST, BROWN_DARK, BROWN_MID, BROWN_LIGHT, WOOD_BLACK, WOOD_HIGHLIGHT, WOOD_LIT,
    BLUE_DEEP, BLUE_SHADOW, BLUE_RICH, BLUE_MID, BLUE_LIGHT, BLUE_HIGHLIGHT,
    TEAL_SHADOW, TEAL_MID, TEAL_LIGHT, TEAL_HIGHLIGHT,
    METAL_SHADOW, METAL_MID, WHITE_SHADOW, WHITE_MID, PURE_WHITE
)

def create_item_canvas() -> PixelCanvas:
    return PixelCanvas(48, 48, TRANSPARENT)


# ==============================================================================
# 1. BOOTS (SPEED POWER-UP) & POP (48x48)
# ==============================================================================

def generate_item_boots() -> List[PixelCanvas]:
    """
    6 frames, 8 fps.
    Chunky winged orange sneaker, Hermes wings, yellow lightning bolt,
    rubber sole tread, bobbing float, glint sweep.
    Centered at cx=24, cy=24.
    """
    frames = []
    bobs = [0, -1, -2, -2, -1, 0]

    for f_idx in range(6):
        c = create_item_canvas()
        by = bobs[f_idx]
        cx = 24
        cy = 24 + by

        # ----------------------------------------------------------------------
        # 1. HERMES WINGS (Attached to heel on left, x: cx-18..cx-6, y: cy-14..cy+1)
        # 3 layered feather plumes flaring up and back
        # ----------------------------------------------------------------------
        # Top Plume (x: cx-17..cx-7, y: cy-13..cy-6)
        c.polygon([
            (cx - 16, cy - 11), (cx - 14, cy - 13), (cx - 7, cy - 8),
            (cx - 7, cy - 5), (cx - 12, cy - 7)
        ], fill=PURE_WHITE, outline=OUTLINE)
        c.line(cx - 14, cy - 12, cx - 8, cy - 7, PURE_WHITE)
        c.line(cx - 12, cy - 7, cx - 8, cy - 5, BLUE_LIGHT)

        # Mid Plume (x: cx-18..cx-6, y: cy-7..cy-1)
        c.polygon([
            (cx - 18, cy - 6), (cx - 16, cy - 8), (cx - 6, cy - 2),
            (cx - 6, cy + 1), (cx - 12, cy - 1)
        ], fill=BLUE_LIGHT, outline=OUTLINE)
        c.line(cx - 15, cy - 6, cx - 7, cy - 1, PURE_WHITE)
        c.line(cx - 14, cy - 2, cx - 7, cy + 1, BLUE_SHADOW)

        # Bottom Plume (x: cx-15..cx-5, y: cy-2..cy+4)
        c.polygon([
            (cx - 15, cy - 1), (cx - 13, cy - 3), (cx - 5, cy + 2),
            (cx - 5, cy + 5), (cx - 11, cy + 4)
        ], fill=BLUE_SHADOW, outline=OUTLINE)
        c.line(cx - 12, cy - 1, cx - 6, cy + 3, BLUE_LIGHT)

        # Wing base / quill junction
        c.line(cx - 7, cy - 4, cx - 5, cy + 3, WHITE_SHADOW)

        # ----------------------------------------------------------------------
        # 2. PADDED HIGH-TOP ANKLE COLLAR & TONGUE
        # ----------------------------------------------------------------------
        # Padded collar rim (x: cx-8..cx+3, y: cy-9..cy-6)
        c.polygon([
            (cx - 8, cy - 9), (cx + 2, cy - 9),
            (cx + 4, cy - 6), (cx - 8, cy - 6)
        ], fill=PURE_WHITE, outline=OUTLINE)
        c.line(cx - 7, cy - 8, cx + 1, cy - 8, PURE_WHITE)
        c.line(cx - 7, cy - 6, cx + 3, cy - 6, WHITE_SHADOW)

        # Dark collar interior / sock opening (x: cx-7..cx-1, y: cy-6..cy-4)
        for y_int in range(cy - 6, cy - 3):
            c.line(cx - 6, y_int, cx - 1, y_int, SHADOW_PURPLE_DARK)

        # Tongue protruding forward (x: cx..cx+5, y: cy-7..cy-2)
        c.polygon([
            (cx, cy - 7), (cx + 5, cy - 7),
            (cx + 6, cy - 3), (cx + 1, cy - 3)
        ], fill=ORANGE_MID, outline=OUTLINE)
        c.line(cx + 1, cy - 6, cx + 4, cy - 6, ORANGE_LIGHT)

        # White criss-cross laces & eyelets (y: cy-4..cy+2)
        # Lace 1
        c.line(cx + 1, cy - 4, cx + 5, cy - 3, PURE_WHITE)
        c.set_pixel(cx, cy - 4, METAL_SHADOW); c.set_pixel(cx + 6, cy - 3, METAL_SHADOW)
        # Lace 2
        c.line(cx + 2, cy - 2, cx + 6, cy - 1, PURE_WHITE)
        c.set_pixel(cx + 1, cy - 2, METAL_SHADOW); c.set_pixel(cx + 7, cy - 1, METAL_SHADOW)
        # Lace 3
        c.line(cx + 3, cy, cx + 7, cy + 1, PURE_WHITE)
        c.set_pixel(cx + 2, cy, METAL_SHADOW); c.set_pixel(cx + 8, cy + 1, METAL_SHADOW)

        # ----------------------------------------------------------------------
        # 3. ORANGE LEATHER SNEAKER UPPER
        # Heel counter, side quarter, and vamp
        # ----------------------------------------------------------------------
        # Upper body polygon
        upper_points = [
            (cx - 9, cy - 5),   # Heel top
            (cx - 9, cy + 7),   # Heel bottom
            (cx + 10, cy + 7),  # Ball of foot bottom
            (cx + 15, cy + 5),  # Vamp front
            (cx + 15, cy + 1),  # Toe cap junction
            (cx + 8, cy - 1),   # Instep
            (cx + 5, cy - 5),   # Collar front
            (cx - 8, cy - 5),   # Collar rear
        ]
        c.polygon(upper_points, fill=ORANGE_MID, outline=OUTLINE)

        # Volumetric shading across orange leather
        # Lit top edge & highlights
        c.line(cx - 8, cy - 4, cx - 2, cy - 4, WOOD_LIT)
        c.line(cx - 8, cy - 3, cx + 4, cy - 3, ORANGE_LIGHT)
        c.line(cx - 8, cy - 2, cx + 6, cy - 2, ORANGE_LIGHT)
        c.line(cx + 6, cy - 1, cx + 12, cy + 1, ORANGE_LIGHT)

        # Shaded lower panels & heel cup
        for y_sh in range(cy + 4, cy + 7):
            c.line(cx - 8, y_sh, cx - 4, y_sh, ORANGE_DEEP)
            c.line(cx - 3, y_sh, cx + 8, y_sh, ORANGE_SHADOW)

        # ----------------------------------------------------------------------
        # 4. YELLOW LIGHTNING BOLT SIDE STRIPE
        # Dynamic zigzag chevron bolt across the side quarter
        # ----------------------------------------------------------------------
        bolt_points = [
            (cx - 5, cy + 3),   # Tail
            (cx + 1, cy + 4),
            (cx + 3, cy),       # Upper notch
            (cx + 8, cy - 2),   # Apex forward
            (cx + 4, cy + 2),   # Recess notch
            (cx + 9, cy + 4),   # Front tip
            (cx + 2, cy + 6),
            (cx, cy + 3),
        ]
        c.polygon(bolt_points, fill=YELLOW_LIGHT, outline=OUTLINE)
        # Bolt specular highlights and depth
        c.line(cx - 4, cy + 3, cx + 1, cy + 4, PURE_WHITE if f_idx in (2, 3) else YELLOW_HIGHLIGHT)
        c.line(cx + 4, cy, cx + 7, cy - 1, PURE_WHITE if f_idx in (2, 3) else YELLOW_HIGHLIGHT)
        c.line(cx + 1, cy + 5, cx + 7, cy + 5, YELLOW_MID)
        c.line(cx + 2, cy + 6, cx + 8, cy + 5, YELLOW_SHADOW)

        # ----------------------------------------------------------------------
        # 5. WHITE RUBBER SHELL TOE CAP
        # Distinct bulbous shell toe cap at front (x: cx+9..cx+17, y: cy+1..cy+7)
        # ----------------------------------------------------------------------
        toe_points = [
            (cx + 9, cy + 1), (cx + 13, cy + 1),
            (cx + 16, cy + 3), (cx + 17, cy + 6),
            (cx + 16, cy + 7), (cx + 9, cy + 7)
        ]
        c.polygon(toe_points, fill=PURE_WHITE, outline=OUTLINE)
        # Shell toe contour ribbing & shading
        c.line(cx + 11, cy + 2, cx + 15, cy + 4, PURE_WHITE)
        c.line(cx + 10, cy + 6, cx + 16, cy + 6, WHITE_SHADOW)
        c.set_pixel(cx + 12, cy + 3, WHITE_SHADOW)  # Shell groove 1
        c.set_pixel(cx + 14, cy + 4, WHITE_SHADOW)  # Shell groove 2

        # ----------------------------------------------------------------------
        # 6. CHUNKY RUBBER MIDSOLE & LUGGED OUTSOLE TREAD
        # ----------------------------------------------------------------------
        # Midsole: thick white rubber band (y: cy+8..cy+10)
        for my in range(cy + 8, cy + 11):
            c.set_pixel(cx - 10, my, OUTLINE)
            c.set_pixel(cx + 17, my, OUTLINE)
            for mx in range(cx - 9, cx + 17):
                if my == cy + 8:
                    c.set_pixel(mx, my, PURE_WHITE if mx >= cx - 4 else WHITE_MID)
                elif my == cy + 9:
                    c.set_pixel(mx, my, WHITE_MID if mx % 2 == 0 else PURE_WHITE)
                else:
                    c.set_pixel(mx, my, WHITE_SHADOW)

        # Midsole foxing stripe (horizontal detail)
        c.line(cx - 9, cy + 9, cx + 16, cy + 9, WHITE_MID)

        # Outsole Tread (y: cy+11..cy+13): dark waffle lug grooves
        for ty in range(cy + 11, cy + 14):
            c.set_pixel(cx - 10, ty, OUTLINE)
            c.set_pixel(cx + 16, ty, OUTLINE)
            for tx in range(cx - 9, cx + 16):
                is_lug = ((tx - (cx - 9)) % 3 == 0)
                if ty == cy + 11:
                    c.set_pixel(tx, ty, OUTLINE if is_lug else WOOD_BLACK)
                elif ty == cy + 12:
                    c.set_pixel(tx, ty, SHADOW_PURPLE_DARK if is_lug else OUTLINE)
                else:
                    c.set_pixel(tx, ty, OUTLINE)

        # ----------------------------------------------------------------------
        # 7. GLINT SWEEP & STAR SPARKLES
        # Sweeping shine across wing -> collar -> bolt -> toe
        # ----------------------------------------------------------------------
        if f_idx == 0:
            # Star glint on Hermes wing top plume
            c.set_pixel(cx - 15, cy - 14, YELLOW_LIGHT)
            c.set_pixel(cx - 15, cy - 13, PURE_WHITE)
            c.set_pixel(cx - 16, cy - 13, YELLOW_LIGHT); c.set_pixel(cx - 14, cy - 13, YELLOW_LIGHT)
            c.set_pixel(cx - 15, cy - 12, YELLOW_LIGHT)
        elif f_idx == 1:
            # Glint on collar rim
            c.set_pixel(cx - 2, cy - 10, YELLOW_LIGHT)
            c.set_pixel(cx - 2, cy - 9, PURE_WHITE)
            c.set_pixel(cx - 3, cy - 9, YELLOW_LIGHT); c.set_pixel(cx - 1, cy - 9, YELLOW_LIGHT)
            c.set_pixel(cx - 2, cy - 8, YELLOW_LIGHT)
        elif f_idx == 2:
            # Glint flash on lightning bolt apex
            c.set_pixel(cx + 8, cy - 3, YELLOW_LIGHT)
            c.set_pixel(cx + 8, cy - 2, PURE_WHITE)
            c.set_pixel(cx + 7, cy - 2, PURE_WHITE); c.set_pixel(cx + 9, cy - 2, YELLOW_LIGHT)
            c.set_pixel(cx + 8, cy - 1, YELLOW_LIGHT)
        elif f_idx == 3:
            # Glint on shell toe cap
            c.set_pixel(cx + 14, cy + 1, YELLOW_LIGHT)
            c.set_pixel(cx + 14, cy + 2, PURE_WHITE)
            c.set_pixel(cx + 13, cy + 2, YELLOW_LIGHT); c.set_pixel(cx + 15, cy + 2, YELLOW_LIGHT)
            c.set_pixel(cx + 14, cy + 3, YELLOW_LIGHT)
        elif f_idx == 4:
            # Star sparkle flaring off front toe tip
            c.set_pixel(cx + 18, cy + 4, YELLOW_LIGHT)
            c.set_pixel(cx + 18, cy + 5, PURE_WHITE)
            c.set_pixel(cx + 17, cy + 5, YELLOW_LIGHT); c.set_pixel(cx + 19, cy + 5, YELLOW_LIGHT)
            c.set_pixel(cx + 18, cy + 6, YELLOW_LIGHT)
        elif f_idx == 5:
            # Soft rim shine on wing and outsole
            c.set_pixel(cx - 17, cy - 6, PURE_WHITE)
            c.set_pixel(cx + 15, cy + 8, PURE_WHITE)

        frames.append(c)
    return frames


def generate_item_boots_pop() -> List[PixelCanvas]:
    """
    3 frames, 24 fps.
    Starburst pop with flying wing feathers and rubber fragments.
    """
    frames = []
    cx, cy = 24, 24

    # --------------------------------------------------------------------------
    # Frame 0: Core flash & starburst rays
    # --------------------------------------------------------------------------
    c0 = create_item_canvas()
    c0.circle(cx, cy, 10, PURE_WHITE, outline=YELLOW_LIGHT)
    c0.line(cx - 16, cy, cx + 16, cy, PURE_WHITE)
    c0.line(cx, cy - 16, cx, cy + 16, PURE_WHITE)
    c0.line(cx - 11, cy - 11, cx + 11, cy + 11, YELLOW_LIGHT)
    c0.line(cx - 11, cy + 11, cx + 11, cy - 11, YELLOW_LIGHT)
    for dx, dy in [(-7, -7), (7, -7), (-7, 7), (7, 7)]:
        c0.set_pixel(cx + dx, cy + dy, BLUE_LIGHT)
        c0.set_pixel(cx + dx // 2, cy + dy // 2, PURE_WHITE)
    frames.append(c0)

    # --------------------------------------------------------------------------
    # Frame 1: Exploding starburst with flying wing feathers & rubber fragments
    # --------------------------------------------------------------------------
    c1 = create_item_canvas()
    # Radial starburst spikes
    spikes = [
        (-18, 0), (18, 0), (0, -18), (0, 18),
        (-13, -13), (13, -13), (-13, 13), (13, 13),
        (-16, -6), (16, -6), (-16, 6), (16, 6),
        (-6, -16), (6, -16), (-6, 16), (6, 16)
    ]
    for sx, sy in spikes:
        c1.set_pixel(cx + sx, cy + sy, YELLOW_LIGHT)
        c1.set_pixel(cx + sx * 3 // 4, cy + sy * 3 // 4, PURE_WHITE)

    # Hermes wing feather 1 flying up-left
    c1.polygon([
        (cx - 16, cy - 14), (cx - 12, cy - 16),
        (cx - 8, cy - 10), (cx - 12, cy - 9)
    ], fill=PURE_WHITE, outline=OUTLINE)
    c1.line(cx - 14, cy - 13, cx - 10, cy - 11, BLUE_LIGHT)

    # Hermes wing feather 2 flying left
    c1.polygon([
        (cx - 18, cy - 2), (cx - 14, cy - 4),
        (cx - 10, cy), (cx - 14, cy + 2)
    ], fill=BLUE_LIGHT, outline=OUTLINE)
    c1.line(cx - 16, cy - 1, cx - 12, cy, BLUE_SHADOW)

    # Chunky white rubber sole fragment flying down-left
    c1.polygon([
        (cx - 14, cy + 10), (cx - 8, cy + 8),
        (cx - 6, cy + 14), (cx - 12, cy + 16)
    ], fill=PURE_WHITE, outline=OUTLINE)
    c1.line(cx - 11, cy + 13, cx - 8, cy + 11, WHITE_SHADOW)

    # Rubber tread chunk flying down-right
    c1.polygon([
        (cx + 8, cy + 10), (cx + 14, cy + 12),
        (cx + 12, cy + 16), (cx + 6, cy + 14)
    ], fill=WOOD_BLACK, outline=OUTLINE)

    # Orange leather collar shard flying up-right
    c1.polygon([
        (cx + 10, cy - 14), (cx + 16, cy - 10),
        (cx + 12, cy - 6), (cx + 8, cy - 10)
    ], fill=ORANGE_MID, outline=OUTLINE)
    c1.line(cx + 11, cy - 12, cx + 14, cy - 9, ORANGE_LIGHT)

    # Yellow lightning sparks flying outward
    c1.line(cx + 12, cy - 1, cx + 16, cy + 1, YELLOW_LIGHT)
    c1.line(cx + 15, cy + 2, cx + 18, cy + 3, YELLOW_MID)
    c1.line(cx - 2, cy - 14, cx, cy - 18, YELLOW_LIGHT)
    frames.append(c1)

    # --------------------------------------------------------------------------
    # Frame 2: Outer sparkling dust ring dispersing
    # --------------------------------------------------------------------------
    c2 = create_item_canvas()
    outer_sparks = [
        (-18, -14), (-14, -18), (14, -18), (18, -14),
        (18, 14), (14, 18), (-14, 18), (-18, 14),
        (0, -20), (0, 20), (-20, 0), (20, 0),
        (-10, -10), (10, -10), (-10, 10), (10, 10),
        (-15, 0), (15, 0), (0, -15), (0, 15)
    ]
    for ox, oy in outer_sparks:
        color = YELLOW_LIGHT if (ox + oy) % 3 == 0 else (BLUE_LIGHT if (ox + oy) % 3 == 1 else WHITE_SHADOW)
        c2.set_pixel(cx + ox, cy + oy, color)
    frames.append(c2)

    return frames


# ==============================================================================
# 2. FEATHER (LIGHTWEIGHT POWER-UP) & POP (48x48)
# ==============================================================================

def generate_item_feather() -> List[PixelCanvas]:
    """
    6 frames, 8 fps.
    Curved cyan-white plume with golden quill nib and slit, individual barb notches, glint sweep.
    Diagonal orientation from bottom-left (cx-14, cy+14) to top-right (cx+14, cy-14).
    """
    frames = []
    bobs = [0, -1, -2, -2, -1, 0]

    # Vane definition along feather shaft
    # Each slice: (t_prog, rachis_x, rachis_y, left_span, right_span, notch_left, notch_right)
    vane_slices = [
        # (prog, rx_off, ry_off, l_span, r_span, notch_l, notch_r)
        (0.00, -14,  14, 1, 1, False, False),  # Nib base
        (0.08, -12,  12, 3, 2, False, False),
        (0.15, -10,  10, 5, 4, False, False),
        (0.22,  -8,   8, 8, 6, True,  False),  # Barb notch 1
        (0.30,  -6,   6, 11, 8, False, True),
        (0.38,  -4,   4, 13, 9, False, False),
        (0.45,  -2,   2, 14, 10, True, False), # Barb notch 2
        (0.53,   0,   0, 14, 10, False, True),
        (0.60,   2,  -2, 14, 10, False, False),
        (0.68,   4,  -4, 13, 9, True,  False), # Barb notch 3
        (0.75,   6,  -6, 11, 8, False, True),
        (0.82,   8,  -8, 9, 7, False, False),
        (0.90,  10, -10, 7, 5, True,  False),  # Barb notch 4
        (0.95,  12, -12, 4, 3, False, False),
        (1.00,  14, -14, 2, 1, False, False),  # Tip
    ]

    for f_idx in range(6):
        c = create_item_canvas()
        by = bobs[f_idx]
        cx = 24
        cy = 24 + by

        # ----------------------------------------------------------------------
        # 1. GOLDEN QUILL NIB AT BOTTOM-LEFT (x: cx-16..cx-11, y: cy+12..cy+17)
        # Metallic calligraphy nib with slit
        # ----------------------------------------------------------------------
        nib_poly = [
            (cx - 16, cy + 16), (cx - 13, cy + 18),
            (cx - 10, cy + 14), (cx - 13, cy + 12)
        ]
        c.polygon(nib_poly, fill=YELLOW_MID, outline=OUTLINE)
        c.line(cx - 15, cy + 15, cx - 12, cy + 13, YELLOW_LIGHT)
        c.line(cx - 14, cy + 17, cx - 11, cy + 15, YELLOW_SHADOW)
        # Nib ink slit
        c.set_pixel(cx - 14, cy + 15, OUTLINE)
        c.set_pixel(cx - 13, cy + 14, OUTLINE)

        # ----------------------------------------------------------------------
        # 2. VANES & RACHIS WITH INDIVIDUAL BARB NOTCHES
        # Upper vane: cyan-white plumage. Lower vane: cyan-blue plumage.
        # ----------------------------------------------------------------------
        for prog, rx_off, ry_off, l_span, r_span, notch_l, notch_r in vane_slices:
            rx = cx + rx_off
            ry = cy + ry_off

            # Apply notch indentations
            actual_l = l_span - (3 if notch_l else 0)
            actual_r = r_span - (3 if notch_r else 0)

            # Normal vector to feather axis (perpendicular: (-1, 1))
            # Upper vane points towards (-1, -1), lower vane towards (1, 1)
            # Scan across perpendicular width:
            # Upper vane: from (rx - actual_l, ry - actual_l) towards rachis
            for step in range(actual_l, 0, -1):
                px = rx - step
                py = ry - step // 2
                is_edge = (step == actual_l)
                if is_edge:
                    c.set_pixel(px, py, OUTLINE)
                else:
                    # Shading from outer rim (pure white) to cyan mid
                    glint_pos = (f_idx * 0.2)
                    is_glint = (abs(prog - glint_pos) <= 0.08 and step >= actual_l - 3)
                    if is_glint:
                        c.set_pixel(px, py, PURE_WHITE)
                    elif step >= actual_l - 2:
                        c.set_pixel(px, py, PURE_WHITE)
                    elif step >= actual_l - 5:
                        c.set_pixel(px, py, WHITE_MID)
                    elif step >= actual_l - 8:
                        c.set_pixel(px, py, WHITE_SHADOW)
                    else:
                        c.set_pixel(px, py, TEAL_LIGHT)

            # Lower vane: from rachis towards (rx + actual_r, ry + actual_r // 2)
            for step in range(1, actual_r + 1):
                px = rx + step
                py = ry + step // 2
                is_edge = (step == actual_r)
                if is_edge:
                    c.set_pixel(px, py, OUTLINE)
                else:
                    if step <= 2:
                        c.set_pixel(px, py, BLUE_LIGHT)
                    elif step <= 5:
                        c.set_pixel(px, py, BLUE_MID)
                    else:
                        c.set_pixel(px, py, BLUE_SHADOW)

            # Golden Rachis (central shaft)
            rachis_glint = (abs(prog - (f_idx * 0.2)) <= 0.08)
            c.set_pixel(rx, ry, PURE_WHITE if rachis_glint else YELLOW_LIGHT)
            c.set_pixel(rx + 1, ry, YELLOW_MID)

        # ----------------------------------------------------------------------
        # 3. CURLED DELICATE PLUME CREST AT TOP-RIGHT (x: cx+13..cx+17, y: cy-17..cy-13)
        # ----------------------------------------------------------------------
        c.polygon([
            (cx + 13, cy - 13), (cx + 17, cy - 15),
            (cx + 16, cy - 17), (cx + 12, cy - 15)
        ], fill=PURE_WHITE, outline=OUTLINE)
        c.set_pixel(cx + 15, cy - 16, PURE_WHITE)
        c.set_pixel(cx + 14, cy - 14, WHITE_MID)

        # ----------------------------------------------------------------------
        # 4. GLINT SWEEP & STAR SPARKLES
        # ----------------------------------------------------------------------
        if f_idx == 0:
            # Sparkle on golden quill nib
            c.set_pixel(cx - 15, cy + 14, YELLOW_LIGHT)
            c.set_pixel(cx - 15, cy + 15, PURE_WHITE)
            c.set_pixel(cx - 16, cy + 15, YELLOW_LIGHT); c.set_pixel(cx - 14, cy + 15, YELLOW_LIGHT)
            c.set_pixel(cx - 15, cy + 16, YELLOW_LIGHT)
        elif f_idx == 1:
            # Glint ascending lower rachis
            c.set_pixel(cx - 8, cy + 7, PURE_WHITE)
            c.set_pixel(cx - 9, cy + 7, YELLOW_LIGHT); c.set_pixel(cx - 7, cy + 7, YELLOW_LIGHT)
        elif f_idx == 2:
            # Glint sweeping across mid vane barbs
            c.set_pixel(cx - 4, cy - 2, PURE_WHITE)
            c.set_pixel(cx - 5, cy - 2, WHITE_MID); c.set_pixel(cx - 3, cy - 2, TEAL_LIGHT)
        elif f_idx == 3:
            # Glint reaching upper rachis
            c.set_pixel(cx + 5, cy - 7, PURE_WHITE)
            c.set_pixel(cx + 4, cy - 7, YELLOW_LIGHT); c.set_pixel(cx + 6, cy - 7, YELLOW_LIGHT)
        elif f_idx == 4:
            # Gleam on feather crest
            c.set_pixel(cx + 14, cy - 15, PURE_WHITE)
            c.set_pixel(cx + 13, cy - 15, WHITE_MID)
        elif f_idx == 5:
            # Brilliant 4-pointed sparkle star flaring off tip
            c.set_pixel(cx + 17, cy - 18, BLUE_LIGHT)
            c.set_pixel(cx + 17, cy - 17, PURE_WHITE)
            c.set_pixel(cx + 16, cy - 17, BLUE_LIGHT); c.set_pixel(cx + 18, cy - 17, BLUE_LIGHT)
            c.set_pixel(cx + 17, cy - 16, BLUE_LIGHT)

        frames.append(c)
    return frames


def generate_item_feather_pop() -> List[PixelCanvas]:
    """
    3 frames, 24 fps.
    Plume dissolving into starry sparkle burst.
    """
    frames = []
    cx, cy = 24, 24

    # --------------------------------------------------------------------------
    # Frame 0: Radiant cyan-white flash along plume axis
    # --------------------------------------------------------------------------
    c0 = create_item_canvas()
    c0.circle(cx, cy, 10, PURE_WHITE, outline=BLUE_LIGHT)
    c0.line(cx - 16, cy + 16, cx + 16, cy - 16, PURE_WHITE)
    c0.line(cx - 12, cy - 12, cx + 12, cy + 12, BLUE_LIGHT)
    c0.line(cx - 16, cy, cx + 16, cy, BLUE_LIGHT)
    c0.line(cx, cy - 16, cx, cy + 16, BLUE_LIGHT)
    frames.append(c0)

    # --------------------------------------------------------------------------
    # Frame 1: Plume dissolving into floating down wisps & golden sparks
    # --------------------------------------------------------------------------
    c1 = create_item_canvas()
    # Floating feather down wisps
    wisps = [
        (-14, -10, PURE_WHITE, BLUE_LIGHT),
        (-8, -16, PURE_WHITE, WHITE_SHADOW),
        (10, -14, PURE_WHITE, BLUE_LIGHT),
        (16, -6, BLUE_LIGHT, BLUE_SHADOW),
        (12, 10, PURE_WHITE, BLUE_LIGHT),
        (4, 16, BLUE_LIGHT, BLUE_SHADOW),
        (-10, 14, PURE_WHITE, WHITE_SHADOW),
        (-16, 4, BLUE_LIGHT, BLUE_SHADOW),
    ]
    for wx, wy, col_main, col_sh in wisps:
        c1.polygon([
            (cx + wx - 2, cy + wy), (cx + wx, cy + wy - 2),
            (cx + wx + 2, cy + wy), (cx + wx, cy + wy + 2)
        ], fill=col_main, outline=OUTLINE)
        c1.set_pixel(cx + wx + 1, cy + wy + 1, col_sh)

    # Golden quill nib fragments tumbling
    c1.line(cx - 6, cy + 6, cx - 3, cy + 8, YELLOW_LIGHT)
    c1.line(cx - 5, cy + 7, cx - 2, cy + 9, YELLOW_MID)
    c1.set_pixel(cx - 6, cy + 7, OUTLINE)

    # Diamond sparkles
    for dx, dy in [(-6, -6), (6, -6), (-6, 6), (6, 6), (0, -12), (0, 12), (-12, 0), (12, 0)]:
        c1.set_pixel(cx + dx, cy + dy, PURE_WHITE)
    frames.append(c1)

    # --------------------------------------------------------------------------
    # Frame 2: Outer starry sparkle burst dispersing
    # --------------------------------------------------------------------------
    c2 = create_item_canvas()
    dust = [
        (-18, -16), (-16, -18), (16, -18), (18, -16),
        (18, 16), (16, 18), (-16, 18), (-18, 16),
        (-20, 0), (20, 0), (0, -20), (0, 20),
        (-12, -12), (12, -12), (-12, 12), (12, 12),
        (-7, -7), (7, -7), (-7, 7), (7, 7)
    ]
    for dx, dy in dust:
        color = PURE_WHITE if (dx + dy) % 3 == 0 else (BLUE_LIGHT if (dx + dy) % 3 == 1 else WHITE_SHADOW)
        c2.set_pixel(cx + dx, cy + dy, color)
    frames.append(c2)

    return frames


# ==============================================================================
# 3. COIN (SCORE POWER-UP) & POP (48x48)
# ==============================================================================

def generate_item_coin() -> List[PixelCanvas]:
    """
    6 frames, 8 fps.
    3D spinning gold coin with embossed star.
    Frame 0: Full face circular view with 3D faceted 5-point star.
    Frame 1: 3/4 perspective view with 3D edge rim on right.
    Frame 2: 1/4 steep perspective view with compressed diamond star gleam.
    Frame 3: Pure edge-on view with milled reeded ridges!
    Frame 4: Reverse 1/4 view with edge rim on left.
    Frame 5: Reverse 3/4 view with edge rim on left.
    """
    frames = []
    bobs = [0, -1, -2, -2, -1, 0]
    R = 14.5  # Coin radius in 48x48 frame
    hw_map = [14.5, 10.5, 4.5, 0.0, 4.5, 10.5]

    for f_idx in range(6):
        c = create_item_canvas()
        by = bobs[f_idx]
        cx = 24
        cy = 24 + by
        hw = hw_map[f_idx]

        # ----------------------------------------------------------------------
        # FRAME 3: PURE EDGE-ON VIEW WITH MILLED REEDED RIDGES!
        # ----------------------------------------------------------------------
        if f_idx == 3:
            edge_w = 7
            ex0 = cx - edge_w // 2  # cx - 3 = 21
            ex1 = ex0 + edge_w - 1  # 27
            ey0 = int(round(cy - R))
            ey1 = int(round(cy + R))

            for y in range(ey0, ey1 + 1):
                # Milled reeded alternating horizontal/vertical ridges
                is_ridge = (y % 2 == 0)
                # Outer borders
                c.set_pixel(ex0, y, OUTLINE)
                c.set_pixel(ex1, y, OUTLINE)

                # Ridge shading across edge
                for x in range(ex0 + 1, ex1):
                    if x == ex0 + 1:
                        c.set_pixel(x, y, YELLOW_LIGHT if is_ridge else YELLOW_MID)
                    elif x <= ex0 + 3:
                        c.set_pixel(x, y, YELLOW_HIGHLIGHT if is_ridge else YELLOW_SHADOW)
                    elif x == ex0 + 4:
                        c.set_pixel(x, y, YELLOW_MID if is_ridge else BROWN_DARK)
                    else:
                        c.set_pixel(x, y, YELLOW_SHADOW if is_ridge else BROWN_DARKEST)

            # Top and bottom rounded coin rim caps
            for x in range(ex0 + 1, ex1):
                c.set_pixel(x, ey0 - 1, OUTLINE)
                c.set_pixel(x, ey1 + 1, OUTLINE)
                c.set_pixel(x, ey0, YELLOW_LIGHT)
                c.set_pixel(x, ey1, YELLOW_SHADOW)

            frames.append(c)
            continue

        # ----------------------------------------------------------------------
        # FRAMES 0, 1, 2, 4, 5: 3D CYLINDRICAL EDGE & ELLIPTICAL FACE
        # ----------------------------------------------------------------------
        has_edge_right = (f_idx in (1, 2))
        has_edge_left = (f_idx in (4, 5))
        edge_thickness = 4 if f_idx in (1, 5) else 6

        # Draw 3D cylindrical side edge
        if has_edge_right or has_edge_left:
            for y in range(int(round(cy - R)), int(round(cy + R)) + 1):
                dy = (y - cy) / R
                if abs(dy) > 0.98:
                    continue
                cur_hw = math.sqrt(max(0.0, 1.0 - dy * dy)) * hw
                if has_edge_right:
                    x_face = int(round(cx + cur_hw))
                    for ex in range(x_face, x_face + edge_thickness):
                        if y <= cy - 5:
                            c.set_pixel(ex, y, YELLOW_LIGHT)
                        elif y >= cy + 4:
                            c.set_pixel(ex, y, YELLOW_SHADOW)
                        else:
                            c.set_pixel(ex, y, YELLOW_MID)
                    c.set_pixel(x_face + edge_thickness, y, OUTLINE)
                elif has_edge_left:
                    x_face = int(round(cx - cur_hw))
                    for ex in range(x_face - edge_thickness + 1, x_face + 1):
                        if y <= cy - 5:
                            c.set_pixel(ex, y, YELLOW_LIGHT)
                        elif y >= cy + 4:
                            c.set_pixel(ex, y, YELLOW_SHADOW)
                        else:
                            c.set_pixel(ex, y, YELLOW_MID)
                    c.set_pixel(x_face - edge_thickness, y, OUTLINE)

        # Draw Elliptical Coin Face
        for y in range(int(round(cy - R)) - 1, int(round(cy + R)) + 2):
            dy = (y - cy) / R
            if abs(dy) > 1.0:
                continue
            cur_hw = math.sqrt(max(0.0, 1.0 - dy * dy)) * hw
            x_left = int(round(cx - cur_hw))
            x_right = int(round(cx + cur_hw))

            if not has_edge_left:
                c.set_pixel(x_left - 1, y, OUTLINE)
            if not has_edge_right:
                c.set_pixel(x_right + 1, y, OUTLINE)
            if abs(dy) >= 0.95:
                c.set_pixel(cx, int(round(cy - R)) - 1 if y < cy else int(round(cy + R)) + 1, OUTLINE)

            for x in range(x_left, x_right + 1):
                # Distance ratio from center of face:
                r_ratio = math.sqrt(((x - cx) / max(0.1, hw)) ** 2 + dy * dy)
                is_outer_rim = (r_ratio >= 0.78)

                if is_outer_rim:
                    # Raised outer bevel rim
                    if y <= cy and x <= cx:
                        c.set_pixel(x, y, YELLOW_HIGHLIGHT if r_ratio >= 0.9 else YELLOW_LIGHT)
                    elif y >= cy and x >= cx:
                        c.set_pixel(x, y, YELLOW_DEEP if r_ratio >= 0.9 else YELLOW_SHADOW)
                    else:
                        c.set_pixel(x, y, YELLOW_MID)
                else:
                    # Recessed inner coin field
                    c.set_pixel(x, y, YELLOW_RICH if y >= cy else YELLOW_MID)

        # ----------------------------------------------------------------------
        # EMBOSSED 5-POINT STAR
        # ----------------------------------------------------------------------
        if f_idx == 0:
            # Full Face 3D Faceted 5-point Star (outer r=7.5, inner r=3.5)
            # 5 Star points:
            star_pts = [
                (0, -7.5),     # Top
                (7.1, -2.3),   # Top-right
                (4.4, 6.1),    # Bottom-right
                (-4.4, 6.1),   # Bottom-left
                (-7.1, -2.3),  # Top-left
            ]
            inner_pts = [
                (2.1, -2.9),
                (3.3, 1.1),
                (0, 3.5),
                (-3.3, 1.1),
                (-2.1, -2.9)
            ]
            # Draw faceted 3D star polygons
            for pt_idx in range(5):
                outer = star_pts[pt_idx]
                in_prev = inner_pts[pt_idx - 1]
                in_curr = inner_pts[pt_idx]

                # Lit facet (facing left/top)
                c.polygon([
                    (cx, cy),
                    (int(round(cx + in_prev[0])), int(round(cy + in_prev[1]))),
                    (int(round(cx + outer[0])), int(round(cy + outer[1]))),
                ], fill=PURE_WHITE if pt_idx in (0, 4) else YELLOW_LIGHT)

                # Shaded facet (facing right/bottom)
                c.polygon([
                    (cx, cy),
                    (int(round(cx + outer[0])), int(round(cy + outer[1]))),
                    (int(round(cx + in_curr[0])), int(round(cy + in_curr[1]))),
                ], fill=YELLOW_MID if pt_idx in (0, 1) else YELLOW_SHADOW)

            # Central specular gleam
            c.set_pixel(cx, cy, PURE_WHITE)
            c.set_pixel(cx - 1, cy, YELLOW_HIGHLIGHT)
            c.set_pixel(cx, cy - 1, YELLOW_HIGHLIGHT)

        elif f_idx in (1, 5):
            # 3/4 perspective compressed star
            scale_x = hw / R
            c.polygon([
                (cx, int(round(cy - 6))),
                (int(round(cx + 5 * scale_x)), int(round(cy - 2))),
                (int(round(cx + 3 * scale_x)), int(round(cy + 5))),
                (int(round(cx - 3 * scale_x)), int(round(cy + 5))),
                (int(round(cx - 5 * scale_x)), int(round(cy - 2))),
            ], fill=YELLOW_LIGHT, outline=OUTLINE)
            c.line(cx, int(round(cy - 5)), cx, int(round(cy + 4)), PURE_WHITE)
            c.line(int(round(cx - 2 * scale_x)), cy, int(round(cx + 2 * scale_x)), cy, YELLOW_LIGHT)

        elif f_idx in (2, 4):
            # 1/4 view diamond star gleam
            c.polygon([
                (cx, int(round(cy - 5))),
                (cx + 1, cy),
                (cx, int(round(cy + 5))),
                (cx - 1, cy)
            ], fill=PURE_WHITE, outline=OUTLINE)
            c.set_pixel(cx, cy, PURE_WHITE)

        frames.append(c)
    return frames


def generate_item_coin_pop() -> List[PixelCanvas]:
    """
    3 frames, 24 fps.
    Golden coin flash with exploding starburst shards.
    """
    frames = []
    cx, cy = 24, 24

    # --------------------------------------------------------------------------
    # Frame 0: Blinding golden core flash
    # --------------------------------------------------------------------------
    c0 = create_item_canvas()
    c0.circle(cx, cy, 10, PURE_WHITE, outline=YELLOW_LIGHT)
    c0.line(cx - 16, cy, cx + 16, cy, PURE_WHITE)
    c0.line(cx, cy - 16, cx, cy + 16, PURE_WHITE)
    c0.line(cx - 11, cy - 11, cx + 11, cy + 11, YELLOW_LIGHT)
    c0.line(cx - 11, cy + 11, cx + 11, cy - 11, YELLOW_LIGHT)
    for dx, dy in [(-8, -8), (8, -8), (-8, 8), (8, 8)]:
        c0.set_pixel(cx + dx, cy + dy, YELLOW_HIGHLIGHT)
    frames.append(c0)

    # --------------------------------------------------------------------------
    # Frame 1: Exploding golden coin shards & starburst points
    # --------------------------------------------------------------------------
    c1 = create_item_canvas()
    # 4 curved coin rim shards flying out to corners
    c1.polygon([
        (cx - 16, cy - 14), (cx - 10, cy - 16),
        (cx - 8, cy - 12), (cx - 14, cy - 10)
    ], fill=YELLOW_LIGHT, outline=OUTLINE)
    c1.line(cx - 14, cy - 13, cx - 10, cy - 14, YELLOW_HIGHLIGHT)

    c1.polygon([
        (cx + 10, cy - 16), (cx + 16, cy - 14),
        (cx + 14, cy - 10), (cx + 8, cy - 12)
    ], fill=YELLOW_LIGHT, outline=OUTLINE)
    c1.line(cx + 11, cy - 14, cx + 15, cy - 12, PURE_WHITE)

    c1.polygon([
        (cx - 16, cy + 14), (cx - 14, cy + 10),
        (cx - 8, cy + 12), (cx - 10, cy + 16)
    ], fill=YELLOW_MID, outline=OUTLINE)
    c1.line(cx - 14, cy + 12, cx - 10, cy + 14, YELLOW_SHADOW)

    c1.polygon([
        (cx + 14, cy + 10), (cx + 16, cy + 14),
        (cx + 10, cy + 16), (cx + 8, cy + 12)
    ], fill=YELLOW_MID, outline=OUTLINE)
    c1.line(cx + 12, cy + 12, cx + 14, cy + 14, YELLOW_SHADOW)

    # Star points flying out along cardinal directions
    c1.polygon([(cx, cy - 18), (cx - 2, cy - 12), (cx + 2, cy - 12)], fill=PURE_WHITE, outline=OUTLINE)
    c1.polygon([(cx, cy + 18), (cx - 2, cy + 12), (cx + 2, cy + 12)], fill=YELLOW_MID, outline=OUTLINE)
    c1.polygon([(cx - 18, cy), (cx - 12, cy - 2), (cx - 12, cy + 2)], fill=YELLOW_LIGHT, outline=OUTLINE)
    c1.polygon([(cx + 18, cy), (cx + 12, cy - 2), (cx + 12, cy + 2)], fill=YELLOW_LIGHT, outline=OUTLINE)

    # Central sparkling light cross
    c1.line(cx - 4, cy, cx + 4, cy, PURE_WHITE)
    c1.line(cx, cy - 4, cx, cy + 4, PURE_WHITE)
    frames.append(c1)

    # --------------------------------------------------------------------------
    # Frame 2: Outer sparkling gold dust ring dispersing
    # --------------------------------------------------------------------------
    c2 = create_item_canvas()
    dust = [
        (-18, -14), (-14, -18), (14, -18), (18, -14),
        (18, 14), (14, 18), (-14, 18), (-18, 14),
        (0, -20), (0, 20), (-20, 0), (20, 0),
        (-12, -12), (12, -12), (-12, 12), (12, 12),
        (-8, -8), (8, -8), (-8, 8), (8, 8)
    ]
    for dx, dy in dust:
        c2.set_pixel(cx + dx, cy + dy, PURE_WHITE if (dx + dy) % 2 == 0 else YELLOW_LIGHT)
    frames.append(c2)

    return frames


# ==============================================================================
# 4. ITEM GLOW (64x64, 1 frame)
# ==============================================================================

def generate_item_glow() -> PixelCanvas:
    """
    64x64 soft circular glow using 4 discrete hard alpha bands (no smooth gradient).
    Pure white on transparent (alpha bands: 255, 192, 115, 45).
    Engine tints this dynamically via modulate color.
    """
    c = PixelCanvas(64, 64, TRANSPARENT)
    cx, cy = 31.5, 31.5

    for y in range(64):
        for x in range(64):
            d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            if d <= 6.5:
                c.set_pixel(x, y, (255, 255, 255, 255))
            elif d <= 13.5:
                c.set_pixel(x, y, (255, 255, 255, 192))
            elif d <= 21.5:
                c.set_pixel(x, y, (255, 255, 255, 115))
            elif d <= 29.5:
                c.set_pixel(x, y, (255, 255, 255, 45))
            else:
                c.set_pixel(x, y, TRANSPARENT)

    return c


def generate_all_items_v2():
    animations = {
        "art/v2/item_boots.png": generate_item_boots(),
        "art/v2/item_boots_pop.png": generate_item_boots_pop(),
        "art/v2/item_feather.png": generate_item_feather(),
        "art/v2/item_feather_pop.png": generate_item_feather_pop(),
        "art/v2/item_coin.png": generate_item_coin(),
        "art/v2/item_coin_pop.png": generate_item_coin_pop(),
    }
    for path, frames in animations.items():
        assemble_strip(frames, path)

    glow = generate_item_glow()
    glow.to_image().save("art/v2/item_glow.png", "PNG")
    print("Saved art/v2/item_glow.png (64x64, 1 frame)")


if __name__ == "__main__":
    generate_all_items_v2()
