"""Younger Sibling Simulator - Player 2 Hand Generator v2.

Elevated pixel art for Player 2 Hand at 64x64 resolution:
- 64x64 frames, palm-center origin at frame center (x=31..32, y=31..32).
- Pale ribbed sleeve cuff at top edge (y=0..8).
- Warm skin tones, distinct knuckle mounds, palm creases (life line, head/heart lines), and fingernails.
- Full 5-7px volumetric finger anatomy (no stick fingers), joint creases (PIP/DIP).
- Strictly follows 64-color palette from tools/palette.py.

Animations:
- hand_idle.png (64x64, 6 frames, 8 fps, loop: true)
- hand_hold.png (64x64, 4 frames, 10 fps, loop: true)
- hand_drop.png (64x64, 5 frames, 24 fps, loop: false)
- hand_cooldown.png (64x64, 4 frames, 6 fps, loop: true)
"""

import math
from typing import List, Tuple
from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE, VOID_BLACK,
    SHADOW_PURPLE_DARK, SHADOW_PURPLE_DEEP, SHADOW_PURPLE_MID,
    PURPLE_DARK, PURPLE_MID, PURPLE_LIGHT,
    DUSK_LILAC, DUSK_PINK, DUSK_ROSE, DUSK_PEACH,
    SKIN_DEEP, SKIN_SHADOW, SKIN_MID, SKIN_LIGHT, SKIN_HIGHLIGHT,
    WHITE_SHADOW, WHITE_MID, PURE_WHITE,
    YELLOW_LIGHT, YELLOW_MID, YELLOW_SHADOW,
    BLUE_LIGHT, BLUE_MID, BLUE_SHADOW
)

def create_base_canvas() -> PixelCanvas:
    return PixelCanvas(64, 64, TRANSPARENT)

def draw_cuff(c: PixelCanvas, cx: int = 32, cy: int = 0, w: int = 28):
    """
    Pale sleeve cuff at the top edge of the frame (y=0..8).
    Ribbed sweater knit texture (y=0..4) with a rolled hem band (y=5..8).
    """
    x0 = cx - w // 2
    x1 = x0 + w - 1

    # Ribbed knit fabric (y = cy .. cy + 4)
    for y in range(cy, cy + 5):
        if not (0 <= y < 64):
            continue
        c.set_pixel(x0, y, OUTLINE)
        c.set_pixel(x1, y, OUTLINE)
        for x in range(x0 + 1, x1):
            pattern = (x - x0) % 3
            if pattern == 0:
                c.set_pixel(x, y, WHITE_SHADOW)
            elif pattern == 1:
                c.set_pixel(x, y, PURE_WHITE)
            else:
                c.set_pixel(x, y, WHITE_MID)

    # Soften top corners
    if 0 <= cy < 64:
        c.set_pixel(x0, cy, TRANSPARENT)
        c.set_pixel(x1, cy, TRANSPARENT)
        c.set_pixel(x0 + 1, cy, OUTLINE)
        c.set_pixel(x1 - 1, cy, OUTLINE)

    # Rolled cuff hem band (y = cy + 5 .. cy + 8)
    # Hem bulges outward slightly
    hw = w + 4
    hx0 = cx - hw // 2
    hx1 = hx0 + hw - 1

    for y in range(cy + 5, cy + 9):
        if not (0 <= y < 64):
            continue
        c.set_pixel(hx0, y, OUTLINE)
        c.set_pixel(hx1, y, OUTLINE)
        for x in range(hx0 + 1, hx1):
            if y == cy + 5:
                # Top edge of roll
                if x <= cx + 2:
                    c.set_pixel(x, y, PURE_WHITE)
                else:
                    c.set_pixel(x, y, WHITE_MID)
            elif y in (cy + 6, cy + 7):
                # Volumetric roll body
                if x <= cx - 6:
                    c.set_pixel(x, y, PURE_WHITE)
                elif x <= cx + 4:
                    c.set_pixel(x, y, WHITE_MID)
                else:
                    c.set_pixel(x, y, WHITE_SHADOW)
            elif y == cy + 8:
                # Underside of roll casting shadow
                if x <= cx - 8:
                    c.set_pixel(x, y, WHITE_MID)
                else:
                    c.set_pixel(x, y, WHITE_SHADOW)

    # Soften rolled hem outer corners
    if 0 <= cy + 5 < 64:
        c.set_pixel(hx0, cy + 5, TRANSPARENT)
        c.set_pixel(hx1, cy + 5, TRANSPARENT)
        c.set_pixel(hx0 + 1, cy + 5, OUTLINE)
        c.set_pixel(hx1 - 1, cy + 5, OUTLINE)
    if 0 <= cy + 8 < 64:
        c.set_pixel(hx0, cy + 8, TRANSPARENT)
        c.set_pixel(hx1, cy + 8, TRANSPARENT)
        c.set_pixel(hx0 + 1, cy + 8, OUTLINE)
        c.set_pixel(hx1 - 1, cy + 8, OUTLINE)


def draw_wrist(c: PixelCanvas, cx: int = 32, cy: int = 9, w: int = 20, h: int = 10):
    """
    Chubby kid wrist emerging from underneath the sleeve cuff roll.
    """
    x0 = cx - w // 2
    x1 = x0 + w - 1

    for y in range(cy, cy + h):
        if not (0 <= y < 64):
            continue
        c.set_pixel(x0, y, OUTLINE)
        c.set_pixel(x1, y, OUTLINE)
        for x in range(x0 + 1, x1):
            if y == cy:
                c.set_pixel(x, y, SKIN_DEEP)  # Deep cast shadow from rolled hem
            elif y == cy + 1:
                c.set_pixel(x, y, SKIN_SHADOW)
            else:
                if x <= x0 + 4:
                    c.set_pixel(x, y, SKIN_LIGHT if y > cy + 3 else SKIN_MID)
                elif x <= cx + 2:
                    c.set_pixel(x, y, SKIN_MID)
                else:
                    c.set_pixel(x, y, SKIN_SHADOW)

    # Tendon / wrist bone highlight
    if 0 <= cy + 4 < 64:
        c.set_pixel(x0 + 3, cy + 4, SKIN_HIGHLIGHT)
        c.set_pixel(x0 + 3, cy + 5, SKIN_HIGHLIGHT)


def draw_palm(c: PixelCanvas, cx: int = 32, cy: int = 19,
              palm_crease: bool = True, knuckles: bool = True,
              cooldown: bool = False):
    """
    Volumetric chubby cartoon palm centered at (cx=32, cy+12 ~ 31..32).
    Includes thenar eminence (thumb pad), hypothenar eminence,
    life line, head/heart transverse creases, and 4 knuckle mounds.
    """
    # Scanline rows for the palm contour: (dy, left_x, right_x)
    # Spans from cy + 0 to cy + 22 (y=19..41)
    palm_rows = [
        (0,  cx - 10, cx + 9),   # y=19
        (1,  cx - 11, cx + 10),  # y=20
        (2,  cx - 12, cx + 11),  # y=21
        (3,  cx - 13, cx + 12),  # y=22
        (4,  cx - 14, cx + 13),  # y=23
        (5,  cx - 15, cx + 14),  # y=24 - thenar pad flaring
        (6,  cx - 16, cx + 14),  # y=25
        (7,  cx - 17, cx + 15),  # y=26
        (8,  cx - 17, cx + 15),  # y=27
        (9,  cx - 17, cx + 15),  # y=28 - thumb base cleft
        (10, cx - 16, cx + 15),  # y=29
        (11, cx - 16, cx + 15),  # y=30
        (12, cx - 15, cx + 15),  # y=31 - palm center!
        (13, cx - 14, cx + 15),  # y=32
        (14, cx - 13, cx + 14),  # y=33
        (15, cx - 13, cx + 14),  # y=34
        (16, cx - 12, cx + 14),  # y=35
        (17, cx - 12, cx + 13),  # y=36
        (18, cx - 11, cx + 13),  # y=37
        (19, cx - 11, cx + 12),  # y=38
        (20, cx - 10, cx + 12),  # y=39
        (21, cx - 9,  cx + 11),  # y=40
        (22, cx - 8,  cx + 10),  # y=41
    ]

    for dy, lx, rx in palm_rows:
        y = cy + dy
        if not (0 <= y < 64):
            continue
        c.set_pixel(lx, y, OUTLINE)
        c.set_pixel(rx, y, OUTLINE)
        for x in range(lx + 1, rx):
            # Volumetric shading across the palm
            if x <= cx - 7:
                c.set_pixel(x, y, SKIN_HIGHLIGHT if dy in (6, 7, 8) else SKIN_LIGHT)
            elif x <= cx - 2:
                c.set_pixel(x, y, SKIN_LIGHT)
            elif x <= cx + 4:
                c.set_pixel(x, y, SKIN_MID)
            elif x <= rx - 2:
                c.set_pixel(x, y, SKIN_SHADOW)
            else:
                c.set_pixel(x, y, SKIN_DEEP)

    if cooldown:
        # Dusk fatigue bruise / shadow in palm center
        for fdy in range(10, 15):
            for fdx in range(-3, 3):
                fy = cy + fdy
                fx = cx + fdx
                if (fdx * fdx + (fdy - 12) * (fdy - 12)) <= 6:
                    c.set_pixel(fx, fy, PURPLE_LIGHT if abs(fdx) <= 1 else DUSK_ROSE)

    if palm_crease:
        # Life line / thenar crease: curves gracefully around the thumb mound
        life_crease = [
            (cx - 5, cy + 6),
            (cx - 6, cy + 7),
            (cx - 7, cy + 8),
            (cx - 8, cy + 9),
            (cx - 9, cy + 10),
            (cx - 9, cy + 11),
            (cx - 8, cy + 12),
            (cx - 8, cy + 13),
            (cx - 7, cy + 14),
            (cx - 6, cy + 15),
        ]
        for px, py in life_crease:
            if 0 <= py < 64:
                c.set_pixel(px, py, SKIN_SHADOW)
                # Bevel highlight right next to crease
                c.set_pixel(px - 1, py, SKIN_LIGHT)

        # Transverse creases (Head & Heart lines)
        head_crease = [
            (cx - 4, cy + 10), (cx - 3, cy + 10), (cx - 2, cy + 11),
            (cx - 1, cy + 11), (cx, cy + 11), (cx + 1, cy + 12),
            (cx + 2, cy + 12), (cx + 3, cy + 12), (cx + 4, cy + 13)
        ]
        for px, py in head_crease:
            if 0 <= py < 64:
                c.set_pixel(px, py, SKIN_SHADOW)

        heart_crease = [
            (cx - 2, cy + 6), (cx - 1, cy + 6), (cx, cy + 7),
            (cx + 1, cy + 7), (cx + 2, cy + 7), (cx + 3, cy + 8),
            (cx + 4, cy + 8), (cx + 5, cy + 8), (cx + 6, cy + 9)
        ]
        for px, py in heart_crease:
            if 0 <= py < 64:
                c.set_pixel(px, py, SKIN_SHADOW)

    if knuckles:
        # 4 distinct knuckle mounds across y = cy + 19 .. cy + 22 (y = 38..41)
        # 1. Index knuckle (cx - 8 .. cx - 3)
        c.rect(cx - 7, cy + 19, 4, 2, SKIN_LIGHT)
        c.set_pixel(cx - 6, cy + 19, SKIN_HIGHLIGHT)
        c.line(cx - 7, cy + 21, cx - 4, cy + 21, SKIN_MID)

        # 2. Middle knuckle (cx - 2 .. cx + 3)
        c.rect(cx - 1, cy + 19, 4, 2, SKIN_LIGHT)
        c.set_pixel(cx, cy + 19, SKIN_HIGHLIGHT)
        c.set_pixel(cx + 1, cy + 19, SKIN_HIGHLIGHT)
        c.line(cx - 1, cy + 21, cx + 2, cy + 21, SKIN_MID)

        # 3. Ring knuckle (cx + 4 .. cx + 8)
        c.rect(cx + 4, cy + 19, 4, 2, SKIN_MID)
        c.set_pixel(cx + 5, cy + 19, SKIN_LIGHT)
        c.line(cx + 4, cy + 21, cx + 7, cy + 21, SKIN_SHADOW)

        # 4. Pinky knuckle (cx + 9 .. cx + 12)
        c.rect(cx + 9, cy + 18, 3, 2, SKIN_MID)
        c.set_pixel(cx + 10, cy + 18, SKIN_LIGHT)
        c.line(cx + 9, cy + 20, cx + 11, cy + 20, SKIN_SHADOW)

        # Interdigital notches / shadow clefts between knuckles
        c.set_pixel(cx - 3, cy + 20, SKIN_DEEP)
        c.set_pixel(cx - 3, cy + 21, OUTLINE)
        c.set_pixel(cx + 3, cy + 20, SKIN_DEEP)
        c.set_pixel(cx + 3, cy + 21, OUTLINE)
        c.set_pixel(cx + 8, cy + 19, SKIN_DEEP)
        c.set_pixel(cx + 8, cy + 20, OUTLINE)


# ==============================================================================
# 1. HAND IDLE (64x64, 6 frames, 8 fps, loop: true)
# ==============================================================================

def generate_hand_idle() -> List[PixelCanvas]:
    """
    6 frames, 8 fps.
    Hovering open hand with gentle finger waves.
    Full 5-7px volumetric finger anatomy, knuckles, palm creases, fingernails.
    """
    frames = []
    bobs = [0, -1, -2, -1, 0, 1]
    t_wiggles = [0, 1, 0, -1, -1, 0]
    i_wiggles = [0, 1, 2, 1, 0, -1]
    m_wiggles = [-1, 0, 1, 2, 1, 0]
    r_wiggles = [0, -1, 0, 1, 2, 1]
    p_wiggles = [1, 0, -1, -1, 0, 1]

    for f_idx in range(6):
        c = create_base_canvas()
        by = bobs[f_idx]
        cx = 32
        cy = by

        draw_cuff(c, cx=cx, cy=max(0, cy))
        draw_wrist(c, cx=cx, cy=9 + cy)
        draw_palm(c, cx=cx, cy=19 + cy, palm_crease=True, knuckles=True)

        # ----------------------------------------------------------------------
        # 1. THUMB (on the left side)
        # ----------------------------------------------------------------------
        two = t_wiggles[f_idx]
        # Thumb projects from thenar eminence (cx - 16, cy + 26)
        # MCP joint around cy + 34, IP joint around cy + 41, tip at cy + 47 + two
        t_tip_y = cy + 47 + two
        # Draw thumb body
        for ty in range(cy + 27, t_tip_y):
            # Width ~ 6 px: lx moves from cx-16 to cx-18, rx moves from cx-11 to cx-13
            lx = cx - 18 if ty >= cy + 35 else cx - 16
            rx = cx - 13 if ty >= cy + 35 else cx - 11
            c.set_pixel(lx, ty, OUTLINE)
            c.set_pixel(rx, ty, OUTLINE)
            for tx in range(lx + 1, rx):
                if tx <= lx + 2:
                    c.set_pixel(tx, ty, SKIN_LIGHT)
                else:
                    c.set_pixel(tx, ty, SKIN_MID)

        # Thumb joint creases
        c.line(cx - 17, cy + 35, cx - 14, cy + 35, SKIN_SHADOW)
        c.line(cx - 17, cy + 41, cx - 14, cy + 41, SKIN_SHADOW)

        # Thumb tip & nail
        c.set_pixel(cx - 18, t_tip_y, OUTLINE)
        c.set_pixel(cx - 13, t_tip_y, OUTLINE)
        c.set_pixel(cx - 17, t_tip_y, PURE_WHITE)    # Thumbnail highlight
        c.set_pixel(cx - 16, t_tip_y, PURE_WHITE)
        c.set_pixel(cx - 15, t_tip_y, WHITE_SHADOW)
        c.set_pixel(cx - 14, t_tip_y, SKIN_LIGHT)
        # Rounded tip cap
        for tx in range(cx - 17, cx - 13):
            c.set_pixel(tx, t_tip_y + 1, OUTLINE)

        # ----------------------------------------------------------------------
        # 2. INDEX FINGER (cx - 8 .. cx - 3, width 6 px)
        # ----------------------------------------------------------------------
        iwo = i_wiggles[f_idx]
        i_tip_y = cy + 54 + iwo
        ilx = cx - 8
        irx = cx - 3

        for iy in range(cy + 41, i_tip_y):
            c.set_pixel(ilx, iy, OUTLINE)
            c.set_pixel(irx, iy, OUTLINE)
            for ix in range(ilx + 1, irx):
                if ix <= ilx + 2:
                    c.set_pixel(ix, iy, SKIN_LIGHT)
                else:
                    c.set_pixel(ix, iy, SKIN_MID)

        # PIP and DIP joint creases
        c.line(ilx + 1, cy + 45, irx - 1, cy + 45, SKIN_SHADOW)
        c.line(ilx + 1, cy + 49, irx - 1, cy + 49, SKIN_SHADOW)

        # Index fingernail & tip
        c.set_pixel(ilx, i_tip_y, OUTLINE)
        c.set_pixel(irx, i_tip_y, OUTLINE)
        c.set_pixel(ilx + 1, i_tip_y, PURE_WHITE)
        c.set_pixel(ilx + 2, i_tip_y, PURE_WHITE)
        c.set_pixel(ilx + 3, i_tip_y, WHITE_SHADOW)
        for ix in range(ilx + 1, irx):
            c.set_pixel(ix, i_tip_y + 1, OUTLINE)

        # ----------------------------------------------------------------------
        # 3. MIDDLE FINGER (cx - 2 .. cx + 4, width 7 px - Longest)
        # ----------------------------------------------------------------------
        mwo = m_wiggles[f_idx]
        m_tip_y = cy + 58 + mwo
        mlx = cx - 2
        mrx = cx + 4

        for my in range(cy + 41, m_tip_y):
            c.set_pixel(mlx, my, OUTLINE)
            c.set_pixel(mrx, my, OUTLINE)
            for mx in range(mlx + 1, mrx):
                if mx <= mlx + 2:
                    c.set_pixel(mx, my, SKIN_LIGHT)
                elif mx <= mlx + 4:
                    c.set_pixel(mx, my, SKIN_MID)
                else:
                    c.set_pixel(mx, my, SKIN_SHADOW)

        # PIP and DIP creases
        c.line(mlx + 1, cy + 46, mrx - 1, cy + 46, SKIN_SHADOW)
        c.line(mlx + 1, cy + 51, mrx - 1, cy + 51, SKIN_SHADOW)

        # Middle fingernail & tip
        c.set_pixel(mlx, m_tip_y, OUTLINE)
        c.set_pixel(mrx, m_tip_y, OUTLINE)
        c.set_pixel(mlx + 1, m_tip_y, PURE_WHITE)
        c.set_pixel(mlx + 2, m_tip_y, PURE_WHITE)
        c.set_pixel(mlx + 3, m_tip_y, WHITE_SHADOW)
        c.set_pixel(mlx + 4, m_tip_y, SKIN_SHADOW)
        for mx in range(mlx + 1, mrx):
            c.set_pixel(mx, m_tip_y + 1, OUTLINE)

        # ----------------------------------------------------------------------
        # 4. RING FINGER (cx + 5 .. cx + 10, width 6 px)
        # ----------------------------------------------------------------------
        rwo = r_wiggles[f_idx]
        r_tip_y = cy + 53 + rwo
        rlx = cx + 5
        rrx = cx + 10

        for ry in range(cy + 41, r_tip_y):
            c.set_pixel(rlx, ry, OUTLINE)
            c.set_pixel(rrx, ry, OUTLINE)
            for rx in range(rlx + 1, rrx):
                if rx <= rlx + 2:
                    c.set_pixel(rx, ry, SKIN_MID)
                else:
                    c.set_pixel(rx, ry, SKIN_SHADOW)

        # Creases
        c.line(rlx + 1, cy + 45, rrx - 1, cy + 45, SKIN_SHADOW)
        c.line(rlx + 1, cy + 49, rrx - 1, cy + 49, SKIN_SHADOW)

        # Ring fingernail & tip
        c.set_pixel(rlx, r_tip_y, OUTLINE)
        c.set_pixel(rrx, r_tip_y, OUTLINE)
        c.set_pixel(rlx + 1, r_tip_y, WHITE_MID)
        c.set_pixel(rlx + 2, r_tip_y, WHITE_SHADOW)
        c.set_pixel(rlx + 3, r_tip_y, SKIN_SHADOW)
        for rx in range(rlx + 1, rrx):
            c.set_pixel(rx, r_tip_y + 1, OUTLINE)

        # ----------------------------------------------------------------------
        # 5. PINKY FINGER (cx + 11 .. cx + 15, width 5 px)
        # ----------------------------------------------------------------------
        pwo = p_wiggles[f_idx]
        p_tip_y = cy + 47 + pwo
        plx = cx + 11
        prx = cx + 15

        for py in range(cy + 40, p_tip_y):
            c.set_pixel(plx, py, OUTLINE)
            c.set_pixel(prx, py, OUTLINE)
            for px in range(plx + 1, prx):
                c.set_pixel(px, py, SKIN_SHADOW)

        # Crease
        c.line(plx + 1, cy + 43, prx - 1, cy + 43, SKIN_DEEP)

        # Pinky fingernail & tip
        c.set_pixel(plx, p_tip_y, OUTLINE)
        c.set_pixel(prx, p_tip_y, OUTLINE)
        c.set_pixel(plx + 1, p_tip_y, WHITE_SHADOW)
        c.set_pixel(plx + 2, p_tip_y, SKIN_SHADOW)
        for px in range(plx + 1, prx):
            c.set_pixel(px, p_tip_y + 1, OUTLINE)

        frames.append(c)
    return frames


# ==============================================================================
# 2. HAND HOLD (64x64, 4 frames, 10 fps, loop: true)
# ==============================================================================

def generate_hand_hold() -> List[PixelCanvas]:
    """
    4 frames, 10 fps.
    Pinching grip with clear open socket beneath fingers.
    Thumb curves in from left, index/middle fingers curve in from right.
    Open socket beneath fingers (x ~ 27..37, y >= 47) is completely clear!
    Looping pulse creates alive grip tension.
    """
    frames = []
    squeezes = [0, 1, 1, 0]

    for f_idx in range(4):
        c = create_base_canvas()
        sq = squeezes[f_idx]
        cx = 32
        cy = 0

        draw_cuff(c, cx=cx, cy=0)
        draw_wrist(c, cx=cx, cy=9)
        draw_palm(c, cx=cx, cy=19, palm_crease=True, knuckles=True)

        # Grasping tension highlight across tendons in back of hand
        if sq:
            c.set_pixel(cx - 4, cy + 25, SKIN_HIGHLIGHT)
            c.set_pixel(cx - 3, cy + 26, SKIN_LIGHT)
            c.set_pixel(cx + 2, cy + 25, SKIN_LIGHT)
            c.set_pixel(cx + 3, cy + 26, SKIN_MID)

        # ----------------------------------------------------------------------
        # THUMB: Curving inward from left to cradle left side of socket
        # Base from cx - 16 .. cx - 11, curving down-right to tip at (cx - 5 + sq, cy + 44)
        # ----------------------------------------------------------------------
        tx_tip = cx - 5 + sq
        ty_tip = cy + 44

        # Thumb proximal segment (cy + 26 .. cy + 34)
        for ty in range(cy + 26, cy + 35):
            lx = cx - 17 + (ty - cy - 26) // 3
            rx = cx - 11 + (ty - cy - 26) // 2
            c.set_pixel(lx, ty, OUTLINE)
            c.set_pixel(rx, ty, OUTLINE)
            for tx in range(lx + 1, rx):
                c.set_pixel(tx, ty, SKIN_LIGHT if tx <= lx + 2 else SKIN_MID)

        # Thumb mid segment angling rightward (cy + 35 .. cy + 41)
        for ty in range(cy + 35, cy + 42):
            prog = ty - (cy + 35)
            lx = cx - 14 + prog
            rx = cx - 8 + prog
            c.set_pixel(lx, ty, OUTLINE)
            c.set_pixel(rx, ty, OUTLINE)
            for tx in range(lx + 1, rx):
                c.set_pixel(tx, ty, SKIN_LIGHT if tx <= lx + 2 else SKIN_MID)

        # Thumb distal pad & nail cradling left socket wall (cy + 42 .. ty_tip)
        for ty in range(cy + 42, ty_tip + 1):
            lx = tx_tip - 5
            rx = tx_tip
            c.set_pixel(lx, ty, OUTLINE)
            c.set_pixel(rx, ty, OUTLINE)
            for tx in range(lx + 1, rx):
                if ty == ty_tip - 1:
                    c.set_pixel(tx, ty, PURE_WHITE if tx == lx + 2 else WHITE_SHADOW)  # Thumbnail
                else:
                    c.set_pixel(tx, ty, SKIN_LIGHT if tx <= lx + 2 else SKIN_MID)

        # Bottom contour of thumb tip
        for tx in range(tx_tip - 4, tx_tip):
            c.set_pixel(tx, ty_tip + 1, OUTLINE)

        # ----------------------------------------------------------------------
        # INDEX & MIDDLE FINGERS: Curving inward from right to pinch socket
        # Tips meet socket at (cx + 5 - sq, cy + 44)
        # ----------------------------------------------------------------------
        ix_tip = cx + 5 - sq
        iy_tip = cy + 44

        # Index knuckle & proximal segment curving down-left (cy + 36 .. cy + 41)
        for iy in range(cy + 36, cy + 42):
            prog = iy - (cy + 36)
            lx = cx + 4 - prog
            rx = cx + 11 - prog
            c.set_pixel(lx, iy, OUTLINE)
            c.set_pixel(rx, iy, OUTLINE)
            for ix in range(lx + 1, rx):
                c.set_pixel(ix, iy, SKIN_MID if ix <= lx + 3 else SKIN_SHADOW)

        # Index distal pad & nail pinching right socket wall (cy + 42 .. iy_tip)
        for iy in range(cy + 42, iy_tip + 1):
            lx = ix_tip
            rx = ix_tip + 5
            c.set_pixel(lx, iy, OUTLINE)
            c.set_pixel(rx, iy, OUTLINE)
            for ix in range(lx + 1, rx):
                if iy == iy_tip - 1:
                    c.set_pixel(ix, iy, PURE_WHITE if ix == lx + 2 else WHITE_MID)  # Index nail
                else:
                    c.set_pixel(ix, iy, SKIN_LIGHT if ix <= lx + 2 else SKIN_MID)

        # Bottom contour of index tip
        for ix in range(ix_tip + 1, ix_tip + 5):
            c.set_pixel(ix, iy_tip + 1, OUTLINE)

        # Curled Ring & Pinky tucked behind into palm (x = cx + 8 .. cx + 15, y = cy + 34 .. cy + 42)
        for cy_f in range(cy + 34, cy + 42):
            c.set_pixel(cx + 12, cy_f, OUTLINE)
            c.set_pixel(cx + 15, cy_f, OUTLINE)
            for cx_f in range(cx + 13, cx + 15):
                c.set_pixel(cx_f, cy_f, SKIN_SHADOW)
        c.line(cx + 12, cy + 42, cx + 15, cy + 42, OUTLINE)

        # Clear socket beneath fingers (x ~ 27..37, y >= 46) is preserved completely empty!
        frames.append(c)
    return frames


# ==============================================================================
# 3. HAND DROP (64x64, 5 frames, 24 fps, loop: false)
# ==============================================================================

def generate_hand_drop() -> List[PixelCanvas]:
    """
    5 frames, 24 fps.
    Release sequence: squeeze -> explosive open splay -> recoil -> drop streaks -> restore.
    """
    frames = []
    cx = 32

    # --------------------------------------------------------------------------
    # Frame 0: Squeeze anticipation (dip down 2px, fingers clamped tight)
    # --------------------------------------------------------------------------
    c0 = create_base_canvas()
    cy0 = 2
    draw_cuff(c0, cx=cx, cy=cy0)
    draw_wrist(c0, cx=cx, cy=9 + cy0)
    draw_palm(c0, cx=cx, cy=19 + cy0, palm_crease=True, knuckles=True)
    # Clenched fingers pinched together tightly
    c0.line(cx - 10, cy0 + 36, cx - 2, cy0 + 44, OUTLINE)
    c0.line(cx - 9, cy0 + 36, cx - 1, cy0 + 44, SKIN_LIGHT)
    c0.line(cx - 8, cy0 + 36, cx, cy0 + 44, SKIN_MID)
    c0.set_pixel(cx - 1, cy0 + 44, PURE_WHITE)  # Thumb nail
    c0.line(cx + 10, cy0 + 36, cx + 2, cy0 + 44, OUTLINE)
    c0.line(cx + 9, cy0 + 36, cx + 1, cy0 + 44, SKIN_SHADOW)
    c0.line(cx + 8, cy0 + 36, cx, cy0 + 44, SKIN_MID)
    c0.set_pixel(cx + 1, cy0 + 44, WHITE_SHADOW)  # Finger nail
    c0.line(cx - 2, cy0 + 45, cx + 2, cy0 + 45, OUTLINE)
    frames.append(c0)

    # --------------------------------------------------------------------------
    # Frame 1: EXPLOSIVE SNAP OPEN! Radial splay + starburst release flash
    # --------------------------------------------------------------------------
    c1 = create_base_canvas()
    cy1 = 0
    draw_cuff(c1, cx=cx, cy=cy1)
    draw_wrist(c1, cx=cx, cy=9 + cy1)
    draw_palm(c1, cx=cx, cy=19 + cy1, palm_crease=False, knuckles=True)

    # Thumb flung hard left (x = 8..18, y = 30..36)
    for ty in range(30, 37):
        c1.line(cx - 14, ty, cx - 22, ty, SKIN_LIGHT if ty <= 33 else SKIN_MID)
    c1.set_pixel(cx - 23, 33, PURE_WHITE)  # Thumb nail flash
    c1.line(cx - 24, 32, cx - 24, 34, OUTLINE)
    c1.line(cx - 23, 30, cx - 14, 30, OUTLINE)
    c1.line(cx - 23, 37, cx - 14, 37, OUTLINE)

    # Index finger splayed diagonally left-down (x = 14..22, y = 44..56)
    for iy in range(43, 56):
        c1.line(cx - 14, iy, cx - 10, iy, SKIN_LIGHT)
    c1.set_pixel(cx - 12, 56, PURE_WHITE)
    c1.line(cx - 15, 43, cx - 15, 56, OUTLINE)
    c1.line(cx - 9, 43, cx - 9, 56, OUTLINE)
    c1.line(cx - 14, 57, cx - 10, 57, OUTLINE)

    # Middle finger shot straight down (x = 29..35, y = 43..61)
    for my in range(43, 61):
        c1.line(cx - 3, my, cx + 3, my, SKIN_LIGHT if my % 2 == 0 else SKIN_MID)
    c1.set_pixel(cx - 1, 61, PURE_WHITE)
    c1.set_pixel(cx, 61, PURE_WHITE)
    c1.line(cx - 4, 43, cx - 4, 61, OUTLINE)
    c1.line(cx + 4, 43, cx + 4, 61, OUTLINE)
    c1.line(cx - 3, 62, cx + 3, 62, OUTLINE)

    # Ring finger splayed diagonally right-down (x = 42..49, y = 44..56)
    for ry in range(43, 56):
        c1.line(cx + 10, ry, cx + 14, ry, SKIN_MID)
    c1.set_pixel(cx + 12, 56, WHITE_MID)
    c1.line(cx + 9, 43, cx + 9, 56, OUTLINE)
    c1.line(cx + 15, 43, cx + 15, 56, OUTLINE)
    c1.line(cx + 10, 57, cx + 14, 57, OUTLINE)

    # Pinky finger splayed up and right (x = 48..56, y = 32..38)
    for py in range(32, 38):
        c1.line(cx + 16, py, cx + 22, py, SKIN_SHADOW)
    c1.set_pixel(cx + 23, 34, WHITE_SHADOW)
    c1.line(cx + 16, 31, cx + 23, 31, OUTLINE)
    c1.line(cx + 16, 38, cx + 23, 38, OUTLINE)
    c1.line(cx + 24, 33, cx + 24, 36, OUTLINE)

    # Starburst pop at socket release point (cx, 46)
    c1.circle(cx, 46, 3, PURE_WHITE)
    c1.line(cx - 6, 46, cx + 6, 46, YELLOW_LIGHT)
    c1.line(cx, 40, cx, 52, YELLOW_LIGHT)
    for dxy in [(-4, -4), (4, -4), (-4, 4), (4, 4)]:
        c1.set_pixel(cx + dxy[0], 46 + dxy[1], YELLOW_LIGHT)
    frames.append(c1)

    # --------------------------------------------------------------------------
    # Frame 2: Max Recoil (-6px up) + Bold Vertical Drop Motion Streaks
    # --------------------------------------------------------------------------
    c2 = create_base_canvas()
    cy2 = -6
    draw_cuff(c2, cx=cx, cy=0)
    draw_wrist(c2, cx=cx, cy=max(0, 9 + cy2), h=12)
    draw_palm(c2, cx=cx, cy=19 + cy2, palm_crease=True, knuckles=True)

    # Recoiling fingers curved back upward with snap inertia
    c2.line(cx - 16, 19 + cy2 + 15, cx - 18, 19 + cy2 + 25, SKIN_LIGHT)
    c2.set_pixel(cx - 18, 19 + cy2 + 26, PURE_WHITE)
    c2.line(cx - 7, 19 + cy2 + 20, cx - 8, 19 + cy2 + 32, SKIN_LIGHT)
    c2.set_pixel(cx - 8, 19 + cy2 + 33, PURE_WHITE)
    c2.line(cx, 19 + cy2 + 22, cx, 19 + cy2 + 36, SKIN_MID)
    c2.set_pixel(cx, 19 + cy2 + 37, PURE_WHITE)
    c2.line(cx + 7, 19 + cy2 + 20, cx + 8, 19 + cy2 + 32, SKIN_MID)
    c2.set_pixel(cx + 8, 19 + cy2 + 33, WHITE_SHADOW)
    c2.line(cx + 14, 19 + cy2 + 16, cx + 16, 19 + cy2 + 26, SKIN_SHADOW)

    # Bold vertical drop motion lines rushing downward through y = 36 .. 63
    for sy in range(36, 62):
        c2.set_pixel(cx, sy, PURE_WHITE)
        if sy % 2 == 0:
            c2.set_pixel(cx - 1, sy, YELLOW_LIGHT)
            c2.set_pixel(cx + 1, sy, YELLOW_LIGHT)
    c2.set_pixel(cx, 62, YELLOW_LIGHT); c2.set_pixel(cx, 63, YELLOW_MID)

    # Flanking drop speedlines
    for sy in range(40, 60):
        c2.set_pixel(cx - 6, sy, PURE_WHITE)
        c2.set_pixel(cx + 6, sy, PURE_WHITE)
    c2.set_pixel(cx - 6, 60, YELLOW_LIGHT); c2.set_pixel(cx + 6, 60, YELLOW_LIGHT)

    for sy in range(45, 57):
        c2.set_pixel(cx - 12, sy, WHITE_MID)
        c2.set_pixel(cx + 12, sy, WHITE_MID)
    c2.set_pixel(cx - 12, 57, WHITE_SHADOW); c2.set_pixel(cx + 12, 57, WHITE_SHADOW)
    frames.append(c2)

    # --------------------------------------------------------------------------
    # Frame 3: Settling (-2px) + Motion Streaks Dissipating
    # --------------------------------------------------------------------------
    c3 = create_base_canvas()
    cy3 = -2
    draw_cuff(c3, cx=cx, cy=0)
    draw_wrist(c3, cx=cx, cy=9 + cy3)
    draw_palm(c3, cx=cx, cy=19 + cy3, palm_crease=True, knuckles=True)

    # Relaxing fingers extending back down
    for iy in range(cy3 + 41, cy3 + 52):
        c3.line(cx - 8, iy, cx - 4, iy, SKIN_LIGHT)
    c3.set_pixel(cx - 6, cy3 + 52, PURE_WHITE)
    for my in range(cy3 + 41, cy3 + 56):
        c3.line(cx - 2, my, cx + 3, my, SKIN_MID)
    c3.set_pixel(cx, cy3 + 56, PURE_WHITE)
    for ry in range(cy3 + 41, cy3 + 51):
        c3.line(cx + 5, ry, cx + 9, ry, SKIN_MID)
    c3.set_pixel(cx + 7, cy3 + 51, WHITE_SHADOW)

    # Fading dashed drop streaks
    for sy in [46, 49, 52, 55, 58, 61]:
        c3.set_pixel(cx, sy, WHITE_SHADOW)
        c3.set_pixel(cx - 6, sy, WHITE_SHADOW)
        c3.set_pixel(cx + 6, sy, WHITE_SHADOW)
    frames.append(c3)

    # --------------------------------------------------------------------------
    # Frame 4: Restored open hand settling into neutral position
    # --------------------------------------------------------------------------
    c4 = create_base_canvas()
    draw_cuff(c4, cx=cx, cy=0)
    draw_wrist(c4, cx=cx, cy=9)
    draw_palm(c4, cx=cx, cy=19, palm_crease=True, knuckles=True)

    # Fingers restored to rest positions
    # Thumb
    for ty in range(27, 47):
        c4.line(cx - 16, ty, cx - 12, ty, SKIN_LIGHT)
    c4.set_pixel(cx - 14, 47, PURE_WHITE)
    # Index
    for iy in range(41, 54):
        c4.line(cx - 8, iy, cx - 3, iy, SKIN_LIGHT)
    c4.set_pixel(cx - 5, 54, PURE_WHITE)
    # Middle
    for my in range(41, 58):
        c4.line(cx - 2, my, cx + 4, my, SKIN_MID)
    c4.set_pixel(cx + 1, 58, PURE_WHITE)
    # Ring
    for ry in range(41, 53):
        c4.line(cx + 5, ry, cx + 10, ry, SKIN_MID)
    c4.set_pixel(cx + 7, 53, WHITE_SHADOW)
    # Pinky
    for py in range(40, 47):
        c4.line(cx + 11, py, cx + 15, py, SKIN_SHADOW)
    c4.set_pixel(cx + 13, 47, WHITE_SHADOW)
    frames.append(c4)

    return frames


# ==============================================================================
# 4. HAND COOLDOWN (64x64, 4 frames, 6 fps, loop: true)
# ==============================================================================

def generate_hand_cooldown() -> List[PixelCanvas]:
    """
    4 frames, 6 fps.
    Tired limp hand shaking out fingers while cooldown recharges.
    Limp floppy fingers with inertia and animated sweat drops.
    """
    frames = []
    shakes = [-2, 2, -1, 1]
    tip_sways = [3, -3, 2, -2]

    for f_idx in range(4):
        c = create_base_canvas()
        s = shakes[f_idx]
        ts = tip_sways[f_idx]
        cx = 32 + s
        cy = 0

        draw_cuff(c, cx=32, cy=0)
        draw_wrist(c, cx=cx, cy=9)
        draw_palm(c, cx=cx, cy=19, palm_crease=True, knuckles=True, cooldown=True)

        # Limp floppy fingers with inertia tip sway (ts)
        # 1. Thumb limp
        for ty in range(cy + 27, cy + 46):
            c.line(cx - 16, ty, cx - 12, ty, SKIN_LIGHT)
        c.set_pixel(cx - 14 + ts // 2, cy + 46, PURE_WHITE)
        c.set_pixel(cx - 14 + ts // 2, cy + 47, OUTLINE)

        # 2. Index limp
        for iy in range(cy + 41, cy + 53):
            c.line(cx - 8, iy, cx - 3, iy, SKIN_LIGHT)
        c.set_pixel(cx - 5 + ts, cy + 53, PURE_WHITE)
        c.set_pixel(cx - 5 + ts, cy + 54, OUTLINE)

        # 3. Middle limp
        for my in range(cy + 41, cy + 57):
            c.line(cx - 2, my, cx + 4, my, SKIN_MID)
        c.set_pixel(cx + 1 + ts, cy + 57, PURE_WHITE)
        c.set_pixel(cx + 1 + ts, cy + 58, OUTLINE)

        # 4. Ring limp
        for ry in range(cy + 41, cy + 52):
            c.line(cx + 5, ry, cx + 10, ry, SKIN_MID)
        c.set_pixel(cx + 7 + ts, cy + 52, WHITE_SHADOW)
        c.set_pixel(cx + 7 + ts, cy + 53, OUTLINE)

        # 5. Pinky limp
        for py in range(cy + 40, cy + 46):
            c.line(cx + 11, py, cx + 15, py, SKIN_SHADOW)
        c.set_pixel(cx + 13 + ts // 2, cy + 46, WHITE_SHADOW)
        c.set_pixel(cx + 13 + ts // 2, cy + 47, OUTLINE)

        # Animated sweat droplets flying off tired hand
        if f_idx == 0:
            # Drop forming on left wrist
            c.circle(cx - 12, 16, 2, BLUE_LIGHT)
            c.set_pixel(cx - 12, 15, PURE_WHITE)
        elif f_idx == 1:
            # Drop flying off to left with teardrop motion
            c.circle(cx - 18, 14, 2, BLUE_LIGHT)
            c.set_pixel(cx - 18, 13, PURE_WHITE)
            c.set_pixel(cx - 16, 15, BLUE_SHADOW)
            c.set_pixel(cx - 15, 16, WHITE_SHADOW)
        elif f_idx == 2:
            # Drop forming on right knuckles
            c.circle(cx + 14, 22, 2, BLUE_LIGHT)
            c.set_pixel(cx + 14, 21, PURE_WHITE)
        elif f_idx == 3:
            # Drop flying off to right
            c.circle(cx + 20, 18, 2, BLUE_LIGHT)
            c.set_pixel(cx + 20, 17, PURE_WHITE)
            c.set_pixel(cx + 18, 19, BLUE_SHADOW)
            c.set_pixel(cx + 17, 20, WHITE_SHADOW)

        frames.append(c)
    return frames


def generate_all_hand_v2():
    animations = {
        "art/v2/hand_idle.png": generate_hand_idle(),
        "art/v2/hand_hold.png": generate_hand_hold(),
        "art/v2/hand_drop.png": generate_hand_drop(),
        "art/v2/hand_cooldown.png": generate_hand_cooldown(),
    }
    for path, frames in animations.items():
        assemble_strip(frames, path)


if __name__ == "__main__":
    generate_all_hand_v2()
