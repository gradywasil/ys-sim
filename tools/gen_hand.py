"""Younger Sibling Simulator - Player 2 Hand Generator.

Elevated pixel art for Player 2 Hand:
- 32x32 frames, origin at palm.
- Pale ribbed sleeve cuff at top edge (y=0..4).
- Warm skin tones, distinct knuckle mounds, palm creases (life line), and fingernails.
- Full 2-3px volumetric finger anatomy (no 1px stick fingers).
- Strictly follows 32-color palette from tools/palette.py.
"""

from typing import List
from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE,
    SKIN_SHADOW, SKIN_MID, SKIN_LIGHT,
    WHITE_SHADOW, PURE_WHITE,
    YELLOW_LIGHT, YELLOW_MID,
    BLUE_LIGHT, PURPLE_LIGHT
)

def create_base_canvas() -> PixelCanvas:
    return PixelCanvas(32, 32, TRANSPARENT)

def draw_cuff(c: PixelCanvas, cx: int = 16, cy: int = 0, w: int = 14):
    """
    Pale sleeve cuff at the top edge of the frame (y=0..4).
    Ribbed sweater knit texture with a rolled hem band.
    """
    x0 = cx - w // 2
    x1 = x0 + w - 1

    # Ribbed knit fabric (y = cy .. cy + 2)
    for y in range(cy, cy + 3):
        for x in range(x0, x1 + 1):
            if x == x0 or x == x1:
                c.set_pixel(x, y, OUTLINE)
            elif (x - x0) % 2 == 1:
                c.set_pixel(x, y, PURE_WHITE)
            else:
                c.set_pixel(x, y, WHITE_SHADOW)
    # Rounded top corners
    c.set_pixel(x0, cy, TRANSPARENT)
    c.set_pixel(x1, cy, TRANSPARENT)
    c.set_pixel(x0 + 1, cy, OUTLINE)
    c.set_pixel(x1 - 1, cy, OUTLINE)

    # Rolled cuff hem band (y = cy + 3, cy + 4)
    for x in range(x0, x1 + 1):
        if x == x0 or x == x1:
            c.set_pixel(x, cy + 3, OUTLINE)
            c.set_pixel(x, cy + 4, OUTLINE)
        elif x <= cx:
            c.set_pixel(x, cy + 3, PURE_WHITE)
            c.set_pixel(x, cy + 4, WHITE_SHADOW)
        else:
            c.set_pixel(x, cy + 3, WHITE_SHADOW)
            c.set_pixel(x, cy + 4, WHITE_SHADOW)
    c.set_pixel(x0, cy + 4, TRANSPARENT)
    c.set_pixel(x1, cy + 4, TRANSPARENT)
    c.set_pixel(x0 + 1, cy + 4, OUTLINE)
    c.set_pixel(x1 - 1, cy + 4, OUTLINE)

def draw_wrist(c: PixelCanvas, cx: int = 16, cy: int = 5, w: int = 10, h: int = 3):
    """Kid wrist emerging from underneath the sleeve cuff."""
    x0 = cx - w // 2
    x1 = x0 + w - 1
    for y in range(cy, cy + h):
        c.set_pixel(x0, y, OUTLINE)
        c.set_pixel(x1, y, OUTLINE)
        for x in range(x0 + 1, x1):
            if y == cy:
                c.set_pixel(x, y, SKIN_SHADOW)  # Cast shadow from cuff hem
            elif x <= cx - 2:
                c.set_pixel(x, y, SKIN_LIGHT)
            elif x <= cx + 2:
                c.set_pixel(x, y, SKIN_MID)
            else:
                c.set_pixel(x, y, SKIN_SHADOW)

def draw_palm(c: PixelCanvas, cx: int = 16, cy: int = 8, palm_crease: bool = True, knuckles: bool = True):
    """
    Volumetric chubby cartoon palm with thenar eminence, palm creases, and knuckle mounds.
    """
    palm_rows = [
        (cy + 0, cx - 6, cx + 5),
        (cy + 1, cx - 7, cx + 6),
        (cy + 2, cx - 8, cx + 6),
        (cy + 3, cx - 8, cx + 6),
        (cy + 4, cx - 8, cx + 6),
        (cy + 5, cx - 8, cx + 6),
        (cy + 6, cx - 7, cx + 6),
        (cy + 7, cx - 7, cx + 5),
    ]
    for y, lx, rx in palm_rows:
        if 0 <= y < 32:
            c.set_pixel(lx, y, OUTLINE)
            c.set_pixel(rx, y, OUTLINE)
            for x in range(lx + 1, rx):
                if x <= cx - 3:
                    c.set_pixel(x, y, SKIN_LIGHT)
                elif x <= cx + 2:
                    c.set_pixel(x, y, SKIN_MID)
                else:
                    c.set_pixel(x, y, SKIN_SHADOW)

    if palm_crease:
        # Life line / thenar crease
        c.set_pixel(cx - 3, cy + 2, SKIN_SHADOW)
        c.set_pixel(cx - 3, cy + 3, SKIN_SHADOW)
        c.set_pixel(cx - 2, cy + 4, SKIN_SHADOW)
        c.set_pixel(cx - 2, cy + 5, SKIN_SHADOW)
        c.set_pixel(cx - 1, cy + 6, SKIN_SHADOW)

    if knuckles:
        # 4 Knuckle mounds across y = cy + 6 .. cy + 7
        # Index knuckle
        c.set_pixel(cx - 4, cy + 6, SKIN_LIGHT)
        c.set_pixel(cx - 5, cy + 6, SKIN_LIGHT)
        # Middle knuckle
        c.set_pixel(cx - 1, cy + 6, SKIN_LIGHT)
        c.set_pixel(cx - 2, cy + 6, SKIN_LIGHT)
        # Ring knuckle
        c.set_pixel(cx + 1, cy + 6, SKIN_MID)
        c.set_pixel(cx + 2, cy + 6, SKIN_MID)
        # Pinky knuckle
        c.set_pixel(cx + 4, cy + 6, SKIN_SHADOW)
        c.set_pixel(cx + 5, cy + 6, SKIN_SHADOW)


def generate_hand_idle() -> List[PixelCanvas]:
    """
    6 frames, 8 fps.
    Open hovering hand with gentle finger wiggle wave.
    Thumb, index, middle, ring, and pinky have distinct widths, joints, and fingernails.
    """
    frames = []
    bobs = [0, -1, -1, 0, 1, 0]
    t_wiggles = [0, 1, 0, -1, -1, 0]
    i_wiggles = [0, 1, 1, 0, -1, -1]
    m_wiggles = [-1, 0, 1, 1, 0, -1]
    r_wiggles = [0, -1, 0, 1, 1, 0]
    p_wiggles = [1, 0, -1, -1, 0, 1]

    for f_idx in range(6):
        c = create_base_canvas()
        by = bobs[f_idx]
        cx = 16
        cy = by

        draw_cuff(c, cx=cx, cy=max(0, cy))
        draw_wrist(c, cx=cx, cy=5 + cy)
        draw_palm(c, cx=cx, cy=8 + cy, palm_crease=True, knuckles=True)

        # 1. Thumb (on the left)
        two = t_wiggles[f_idx]
        c.set_pixel(cx - 9, cy + 14, OUTLINE)
        c.set_pixel(cx - 8, cy + 14, SKIN_LIGHT)
        c.set_pixel(cx - 7, cy + 14, SKIN_MID)
        c.set_pixel(cx - 6, cy + 14, SKIN_SHADOW)

        t_tip_y = cy + 19 + two
        for ty in range(cy + 15, t_tip_y):
            c.set_pixel(cx - 9, ty, OUTLINE)
            c.set_pixel(cx - 8, ty, SKIN_LIGHT)
            c.set_pixel(cx - 7, ty, SKIN_MID)
            c.set_pixel(cx - 6, ty, OUTLINE if ty >= cy + 17 else SKIN_SHADOW)
        c.set_pixel(cx - 7, cy + 16, SKIN_SHADOW)  # Thumb joint crease
        c.set_pixel(cx - 9, t_tip_y, OUTLINE)
        c.set_pixel(cx - 8, t_tip_y, PURE_WHITE)  # Thumb fingernail
        c.set_pixel(cx - 7, t_tip_y, SKIN_LIGHT)
        c.set_pixel(cx - 6, t_tip_y, OUTLINE)
        c.set_pixel(cx - 8, t_tip_y + 1, OUTLINE)
        c.set_pixel(cx - 7, t_tip_y + 1, OUTLINE)

        # 2. Index finger (x = cx - 5 .. cx - 3)
        iwo = i_wiggles[f_idx]
        i_tip_y = cy + 23 + iwo
        for iy in range(cy + 16, i_tip_y):
            c.set_pixel(cx - 6, iy, OUTLINE)
            c.set_pixel(cx - 5, iy, SKIN_LIGHT)
            c.set_pixel(cx - 4, iy, SKIN_MID)
            c.set_pixel(cx - 3, iy, SKIN_SHADOW)
        c.set_pixel(cx - 4, cy + 19, SKIN_SHADOW)  # Knuckle joint crease
        c.set_pixel(cx - 6, i_tip_y, OUTLINE)
        c.set_pixel(cx - 5, i_tip_y, PURE_WHITE)  # Index fingernail
        c.set_pixel(cx - 4, i_tip_y, SKIN_LIGHT)
        c.set_pixel(cx - 3, i_tip_y, OUTLINE)
        c.set_pixel(cx - 5, i_tip_y + 1, OUTLINE)
        c.set_pixel(cx - 4, i_tip_y + 1, OUTLINE)

        # 3. Middle finger (x = cx - 2 .. cx) - longest finger
        mwo = m_wiggles[f_idx]
        m_tip_y = cy + 25 + mwo
        for my in range(cy + 16, m_tip_y):
            c.set_pixel(cx - 2, my, SKIN_LIGHT)
            c.set_pixel(cx - 1, my, SKIN_MID)
            c.set_pixel(cx, my, SKIN_SHADOW)
        c.set_pixel(cx - 1, cy + 19, SKIN_SHADOW)  # PIP crease
        c.set_pixel(cx - 1, cy + 22, SKIN_SHADOW)  # DIP crease
        c.set_pixel(cx - 3, m_tip_y, OUTLINE)
        c.set_pixel(cx - 2, m_tip_y, PURE_WHITE)  # Middle fingernail
        c.set_pixel(cx - 1, m_tip_y, PURE_WHITE)
        c.set_pixel(cx, m_tip_y, SKIN_SHADOW)
        c.set_pixel(cx + 1, m_tip_y, OUTLINE)
        c.set_pixel(cx - 2, m_tip_y + 1, OUTLINE)
        c.set_pixel(cx - 1, m_tip_y + 1, OUTLINE)
        c.set_pixel(cx, m_tip_y + 1, OUTLINE)

        # 4. Ring finger (x = cx + 1 .. cx + 3)
        rwo = r_wiggles[f_idx]
        r_tip_y = cy + 23 + rwo
        for ry in range(cy + 16, r_tip_y):
            c.set_pixel(cx + 1, ry, SKIN_MID)
            c.set_pixel(cx + 2, ry, SKIN_MID)
            c.set_pixel(cx + 3, ry, SKIN_SHADOW)
        c.set_pixel(cx + 2, cy + 19, SKIN_SHADOW)  # Crease
        c.set_pixel(cx + 1, r_tip_y, WHITE_SHADOW)  # Ring fingernail
        c.set_pixel(cx + 2, r_tip_y, SKIN_SHADOW)
        c.set_pixel(cx + 3, r_tip_y, OUTLINE)
        c.set_pixel(cx + 1, r_tip_y + 1, OUTLINE)
        c.set_pixel(cx + 2, r_tip_y + 1, OUTLINE)

        # 5. Pinky finger (x = cx + 4 .. cx + 5)
        pwo = p_wiggles[f_idx]
        p_tip_y = cy + 20 + pwo
        for py in range(cy + 16, p_tip_y):
            c.set_pixel(cx + 4, py, SKIN_MID if py <= cy + 17 else SKIN_SHADOW)
            c.set_pixel(cx + 5, py, SKIN_SHADOW)
            c.set_pixel(cx + 6, py, OUTLINE)
        c.set_pixel(cx + 4, p_tip_y, WHITE_SHADOW)  # Pinky fingernail
        c.set_pixel(cx + 5, p_tip_y, SKIN_SHADOW)
        c.set_pixel(cx + 6, p_tip_y, OUTLINE)
        c.set_pixel(cx + 4, p_tip_y + 1, OUTLINE)
        c.set_pixel(cx + 5, p_tip_y + 1, OUTLINE)

        frames.append(c)
    return frames


def generate_hand_hold() -> List[PixelCanvas]:
    """
    4 frames, 10 fps.
    Pinching grip with clear socket for held item below palm.
    Thumb curves in from left, fingers curve in from right, leaving (cx-1..cx+1, y>=21) open.
    Looping pulse creates an alive grip tension.
    """
    frames = []
    squeezes = [0, 1, 1, 0]

    for f_idx in range(4):
        c = create_base_canvas()
        sq = squeezes[f_idx]
        cx = 16

        draw_cuff(c, cx=cx, cy=0)
        draw_wrist(c, cx=cx, cy=5)
        draw_palm(c, cx=cx, cy=8, palm_crease=True, knuckles=True)

        # Grasping tension highlight across palm/tendons
        c.set_pixel(cx - 2, 12, PURE_WHITE if sq else SKIN_LIGHT)
        c.set_pixel(cx + 1, 13, SKIN_LIGHT if sq else SKIN_MID)

        # Thumb reaching inward to cradle left side of socket
        tx = cx - 3 + sq
        c.set_pixel(cx - 7, 15, OUTLINE); c.set_pixel(cx - 6, 15, SKIN_LIGHT); c.set_pixel(cx - 5, 15, SKIN_MID)
        c.set_pixel(cx - 7, 16, OUTLINE); c.set_pixel(cx - 6, 16, SKIN_LIGHT); c.set_pixel(cx - 5, 16, SKIN_MID); c.set_pixel(cx - 4, 16, OUTLINE)
        c.set_pixel(cx - 6, 17, OUTLINE); c.set_pixel(cx - 5, 17, SKIN_LIGHT); c.set_pixel(cx - 4, 17, SKIN_MID); c.set_pixel(cx - 3, 17, OUTLINE)
        c.set_pixel(cx - 5, 18, OUTLINE); c.set_pixel(cx - 4, 18, SKIN_LIGHT); c.set_pixel(cx - 3, 18, SKIN_MID); c.set_pixel(cx - 2, 18, OUTLINE)
        # Thumb lower pad and nail
        c.set_pixel(tx - 2, 19, OUTLINE); c.set_pixel(tx - 1, 19, SKIN_LIGHT); c.set_pixel(tx, 19, SKIN_MID); c.set_pixel(tx + 1, 19, OUTLINE)
        c.set_pixel(tx - 2, 20, OUTLINE); c.set_pixel(tx - 1, 20, PURE_WHITE); c.set_pixel(tx, 20, SKIN_LIGHT); c.set_pixel(tx + 1, 20, OUTLINE)  # Nail
        c.set_pixel(tx - 2, 21, OUTLINE); c.set_pixel(tx - 1, 21, SKIN_LIGHT); c.set_pixel(tx, 21, SKIN_MID); c.set_pixel(tx + 1, 21, OUTLINE)  # Pad
        c.set_pixel(tx - 1, 22, OUTLINE); c.set_pixel(tx, 22, OUTLINE)

        # Index & Middle fingers curling from right to pinch socket
        ix = cx + 2 - sq
        c.set_pixel(cx + 4, 16, OUTLINE); c.set_pixel(cx + 3, 16, SKIN_MID); c.set_pixel(cx + 2, 16, SKIN_LIGHT)
        c.set_pixel(cx + 4, 17, OUTLINE); c.set_pixel(cx + 3, 17, SKIN_MID); c.set_pixel(cx + 2, 17, SKIN_LIGHT); c.set_pixel(cx + 1, 17, OUTLINE)
        c.set_pixel(ix + 2, 18, OUTLINE); c.set_pixel(ix + 1, 18, SKIN_MID); c.set_pixel(ix, 18, SKIN_LIGHT); c.set_pixel(ix - 1, 18, OUTLINE)
        c.set_pixel(ix + 2, 19, OUTLINE); c.set_pixel(ix + 1, 19, SKIN_MID); c.set_pixel(ix, 19, SKIN_LIGHT); c.set_pixel(ix - 1, 19, OUTLINE)
        c.set_pixel(ix + 2, 20, OUTLINE); c.set_pixel(ix + 1, 20, WHITE_SHADOW); c.set_pixel(ix, 20, SKIN_LIGHT); c.set_pixel(ix - 1, 20, OUTLINE)  # Nail
        c.set_pixel(ix + 1, 21, OUTLINE); c.set_pixel(ix, 21, SKIN_MID); c.set_pixel(ix - 1, 21, OUTLINE)  # Pad
        c.set_pixel(ix, 22, OUTLINE)

        # Curled ring & pinky fingers tucked in on the right
        c.set_pixel(cx + 5, 17, OUTLINE); c.set_pixel(cx + 6, 17, OUTLINE)
        c.set_pixel(cx + 5, 18, SKIN_SHADOW); c.set_pixel(cx + 6, 18, OUTLINE)
        c.set_pixel(cx + 5, 19, SKIN_SHADOW); c.set_pixel(cx + 6, 19, OUTLINE)
        c.set_pixel(cx + 4, 20, SKIN_SHADOW); c.set_pixel(cx + 5, 20, OUTLINE)
        c.set_pixel(cx + 4, 21, OUTLINE)

        # Item socket (cx-1 .. cx+1) at y >= 21 is kept clear for the held item
        frames.append(c)
    return frames


def generate_hand_drop() -> List[PixelCanvas]:
    """
    5 frames, 24 fps.
    Release sequence: squeeze -> explosive snap open -> recoil -> drop lines -> restore.
    Plays once.
    """
    frames = []
    cx = 16

    # Frame 0: Squeeze anticipation (dip down 1px, fingers clamped tight)
    c0 = create_base_canvas()
    draw_cuff(c0, cx=cx, cy=1)
    draw_wrist(c0, cx=cx, cy=6)
    draw_palm(c0, cx=cx, cy=9, palm_crease=True, knuckles=True)
    c0.line(cx - 6, 17, cx - 2, 21, SKIN_LIGHT)
    c0.line(cx - 5, 17, cx - 1, 21, SKIN_MID)
    c0.set_pixel(cx - 2, 21, PURE_WHITE)  # Thumb nail
    c0.set_pixel(cx - 1, 22, OUTLINE)
    c0.line(cx + 4, 17, cx, 21, SKIN_MID)
    c0.line(cx + 3, 17, cx - 1, 21, SKIN_LIGHT)
    c0.set_pixel(cx, 21, WHITE_SHADOW)  # Index nail
    c0.set_pixel(cx, 22, OUTLINE)
    frames.append(c0)

    # Frame 1: SNAP OPEN! Explosive radial splay + release starburst
    c1 = create_base_canvas()
    draw_cuff(c1, cx=cx, cy=0)
    draw_wrist(c1, cx=cx, cy=5)
    draw_palm(c1, cx=cx, cy=8, palm_crease=False, knuckles=True)
    # Thumb flung left
    c1.line(cx - 7, 14, cx - 11, 15, SKIN_LIGHT)
    c1.line(cx - 7, 15, cx - 11, 16, SKIN_MID)
    c1.set_pixel(cx - 12, 15, PURE_WHITE)
    c1.set_pixel(cx - 12, 16, OUTLINE); c1.set_pixel(cx - 11, 17, OUTLINE)
    # Index finger splayed left-down
    c1.line(cx - 5, 16, cx - 7, 24, SKIN_LIGHT)
    c1.line(cx - 4, 16, cx - 6, 24, SKIN_MID)
    c1.set_pixel(cx - 7, 25, PURE_WHITE)
    c1.set_pixel(cx - 7, 26, OUTLINE); c1.set_pixel(cx - 6, 26, OUTLINE)
    # Middle finger splayed center-down
    c1.line(cx - 1, 16, cx - 1, 26, SKIN_LIGHT)
    c1.line(cx, 16, cx, 26, SKIN_MID)
    c1.set_pixel(cx - 1, 27, PURE_WHITE)
    c1.set_pixel(cx, 27, PURE_WHITE)
    c1.set_pixel(cx - 1, 28, OUTLINE); c1.set_pixel(cx, 28, OUTLINE)
    # Ring finger splayed right-down
    c1.line(cx + 2, 16, cx + 5, 25, SKIN_MID)
    c1.line(cx + 3, 16, cx + 6, 25, SKIN_SHADOW)
    c1.set_pixel(cx + 5, 26, WHITE_SHADOW)
    c1.set_pixel(cx + 5, 27, OUTLINE); c1.set_pixel(cx + 6, 27, OUTLINE)
    # Pinky finger splayed up-right
    c1.line(cx + 5, 15, cx + 9, 18, SKIN_SHADOW)
    c1.set_pixel(cx + 10, 18, WHITE_SHADOW)
    c1.set_pixel(cx + 10, 19, OUTLINE)
    # Release starburst at socket point (cx, 22)
    c1.set_pixel(cx, 22, PURE_WHITE)
    c1.set_pixel(cx - 1, 22, YELLOW_LIGHT); c1.set_pixel(cx + 1, 22, YELLOW_LIGHT)
    c1.set_pixel(cx, 21, YELLOW_LIGHT); c1.set_pixel(cx, 23, YELLOW_LIGHT)
    frames.append(c1)

    # Frame 2: Max Recoil (-3px up) + Downward Drop Lines
    c2 = create_base_canvas()
    draw_cuff(c2, cx=cx, cy=0)
    draw_wrist(c2, cx=cx, cy=2, h=4)
    draw_palm(c2, cx=cx, cy=5, palm_crease=True, knuckles=True)
    # Recoiling fingers flung upward
    c2.line(cx - 7, 11, cx - 10, 13, SKIN_LIGHT)
    c2.set_pixel(cx - 11, 13, PURE_WHITE)
    c2.line(cx - 5, 13, cx - 6, 20, SKIN_LIGHT)
    c2.set_pixel(cx - 6, 21, PURE_WHITE)
    c2.line(cx - 1, 13, cx - 1, 21, SKIN_MID)
    c2.set_pixel(cx - 1, 22, PURE_WHITE)
    c2.line(cx + 2, 13, cx + 4, 20, SKIN_MID)
    c2.set_pixel(cx + 4, 21, WHITE_SHADOW)
    c2.line(cx + 5, 12, cx + 8, 15, SKIN_SHADOW)

    # Bold downward drop motion lines rushing through y=20..31
    c2.line(cx, 20, cx, 30, PURE_WHITE)
    c2.set_pixel(cx, 31, YELLOW_LIGHT)
    c2.line(cx - 3, 23, cx - 3, 29, PURE_WHITE)
    c2.set_pixel(cx - 3, 30, YELLOW_LIGHT)
    c2.line(cx + 3, 23, cx + 3, 29, PURE_WHITE)
    c2.set_pixel(cx + 3, 30, YELLOW_LIGHT)
    frames.append(c2)

    # Frame 3: Settling (-1px) + Drop Lines Dissipating
    c3 = create_base_canvas()
    draw_cuff(c3, cx=cx, cy=0)
    draw_wrist(c3, cx=cx, cy=4, h=3)
    draw_palm(c3, cx=cx, cy=7, palm_crease=True, knuckles=True)
    c3.line(cx - 7, 13, cx - 9, 17, SKIN_LIGHT)
    c3.set_pixel(cx - 9, 18, PURE_WHITE)
    c3.line(cx - 5, 15, cx - 5, 22, SKIN_LIGHT)
    c3.set_pixel(cx - 5, 23, PURE_WHITE)
    c3.line(cx - 1, 15, cx - 1, 23, SKIN_MID)
    c3.set_pixel(cx - 1, 24, PURE_WHITE)
    c3.line(cx + 2, 15, cx + 2, 22, SKIN_MID)
    c3.set_pixel(cx + 2, 23, WHITE_SHADOW)
    c3.line(cx + 5, 14, cx + 6, 18, SKIN_SHADOW)
    # Fading dashed drop lines
    c3.set_pixel(cx - 3, 28, WHITE_SHADOW); c3.set_pixel(cx - 3, 30, WHITE_SHADOW)
    c3.set_pixel(cx, 27, WHITE_SHADOW); c3.set_pixel(cx, 29, WHITE_SHADOW); c3.set_pixel(cx, 31, WHITE_SHADOW)
    c3.set_pixel(cx + 3, 28, WHITE_SHADOW); c3.set_pixel(cx + 3, 30, WHITE_SHADOW)
    frames.append(c3)

    # Frame 4: Restored open hand settling into place
    c4 = create_base_canvas()
    draw_cuff(c4, cx=cx, cy=0)
    draw_wrist(c4, cx=cx, cy=5)
    draw_palm(c4, cx=cx, cy=8, palm_crease=True, knuckles=True)
    c4.line(cx - 7, 14, cx - 8, 19, SKIN_LIGHT)
    c4.set_pixel(cx - 8, 20, PURE_WHITE)
    c4.line(cx - 5, 16, cx - 5, 23, SKIN_LIGHT)
    c4.set_pixel(cx - 5, 24, PURE_WHITE)
    c4.line(cx - 1, 16, cx - 1, 25, SKIN_MID)
    c4.set_pixel(cx - 1, 26, PURE_WHITE)
    c4.line(cx + 2, 16, cx + 2, 23, SKIN_MID)
    c4.set_pixel(cx + 2, 24, WHITE_SHADOW)
    c4.line(cx + 5, 15, cx + 5, 20, SKIN_SHADOW)
    c4.set_pixel(cx + 5, 21, WHITE_SHADOW)
    frames.append(c4)

    return frames


def generate_hand_cooldown() -> List[PixelCanvas]:
    """
    4 frames, 6 fps.
    Tired limp hand shaking out fingers while cooldown recharges.
    Limp floppy fingers with inertia and animated sweat drops.
    """
    frames = []
    shakes = [-1, 1, -1, 0]
    finger_flips = [1, -1, 1, -1]

    for f_idx in range(4):
        c = create_base_canvas()
        s = shakes[f_idx]
        ff = finger_flips[f_idx]
        cx = 16 + s

        draw_cuff(c, cx=16, cy=0)
        draw_wrist(c, cx=cx, cy=5)
        draw_palm(c, cx=cx, cy=8, palm_crease=True, knuckles=True)

        # Fatigue dusky crease in palm center
        c.set_pixel(cx - 2, 11, PURPLE_LIGHT)
        c.set_pixel(cx - 1, 12, PURPLE_LIGHT)

        # Limp floppy fingers shaking with inertia (ff)
        # Thumb limp
        c.line(cx - 7, 14, cx - 8 + ff, 18, SKIN_LIGHT)
        c.set_pixel(cx - 8 + ff, 19, PURE_WHITE)
        c.set_pixel(cx - 8 + ff, 20, OUTLINE)

        # Index limp
        c.line(cx - 5, 16, cx - 5 + ff, 22, SKIN_LIGHT)
        c.line(cx - 4, 16, cx - 4 + ff, 22, SKIN_MID)
        c.set_pixel(cx - 5 + ff, 23, PURE_WHITE)
        c.set_pixel(cx - 5 + ff, 24, OUTLINE)

        # Middle limp
        c.line(cx - 1, 16, cx - 1 + ff, 24, SKIN_LIGHT)
        c.line(cx, 16, cx + ff, 24, SKIN_MID)
        c.set_pixel(cx - 1 + ff, 25, PURE_WHITE)
        c.set_pixel(cx + ff, 25, PURE_WHITE)
        c.set_pixel(cx - 1 + ff, 26, OUTLINE)

        # Ring limp
        c.line(cx + 2, 16, cx + 2 + ff, 22, SKIN_MID)
        c.line(cx + 3, 16, cx + 3 + ff, 22, SKIN_SHADOW)
        c.set_pixel(cx + 2 + ff, 23, WHITE_SHADOW)
        c.set_pixel(cx + 2 + ff, 24, OUTLINE)

        # Pinky limp
        c.line(cx + 5, 15, cx + 5 + ff, 19, SKIN_SHADOW)
        c.set_pixel(cx + 5 + ff, 20, WHITE_SHADOW)
        c.set_pixel(cx + 5 + ff, 21, OUTLINE)

        # Sweat droplets flicking off tired hand
        if f_idx == 0:
            c.set_pixel(cx - 8, 12, BLUE_LIGHT)
            c.set_pixel(cx - 9, 13, WHITE_SHADOW)
        elif f_idx == 1:
            c.set_pixel(cx - 11, 10, PURE_WHITE)
            c.set_pixel(cx - 12, 11, BLUE_LIGHT)
            c.set_pixel(cx - 11, 11, BLUE_LIGHT)
            c.set_pixel(cx - 12, 12, OUTLINE)
        elif f_idx == 2:
            c.set_pixel(cx + 7, 13, BLUE_LIGHT)
            c.set_pixel(cx + 8, 14, WHITE_SHADOW)
        elif f_idx == 3:
            c.set_pixel(cx + 10, 11, PURE_WHITE)
            c.set_pixel(cx + 11, 12, BLUE_LIGHT)
            c.set_pixel(cx + 10, 12, BLUE_LIGHT)
            c.set_pixel(cx + 11, 13, OUTLINE)

        frames.append(c)
    return frames


def generate_all_hand_sprites():
    animations = {
        "art/incoming/hand_idle.png": generate_hand_idle(),
        "art/incoming/hand_hold.png": generate_hand_hold(),
        "art/incoming/hand_drop.png": generate_hand_drop(),
        "art/incoming/hand_cooldown.png": generate_hand_cooldown(),
    }
    for path, frames in animations.items():
        assemble_strip(frames, path)


if __name__ == "__main__":
    generate_all_hand_sprites()
