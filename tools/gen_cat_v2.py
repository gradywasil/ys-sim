"""Younger Sibling Simulator - Cat & Parent v2 Sprite Generator.

Generates:
1. The Family Cat (96x64, grounded on y=63):
   - cat_sleep.png (8 frames, 4 fps, loop: true)
   - cat_wake.png (6 frames, 12 fps, loop: false)
   - cat_watch.png (8 frames, 6 fps, loop: true)
   - cat_startle.png (8 frames, 20 fps, loop: false)
   - cat_lick.png (8 frames, 8 fps, loop: true)
   - cat_yawn.png (8 frames, 8 fps, loop: true)
   - cat_zoomies.png (8 frames, 20 fps, loop: true)

2. The Parent (128x192 sheets and 192x96 speech bubbles):
   - parent_peek.png (128x192, 6 frames, 6 fps, loop: false)
   - parent_point.png (128x192, 8 frames, 12 fps, loop: false)
   - parent_sigh.png (128x192, 8 frames, 8 fps, loop: false)
   - parent_speech_yell.png (192x96)
   - parent_speech_sigh.png (192x96)
"""

import math
from typing import List, Tuple
from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE, VOID_BLACK,
    SHADOW_DEEP, SHADOW_MID, PURPLE_DARK, PURPLE_MID, PURPLE_RICH, PURPLE_LIGHT,
    DUSK_LILAC, DUSK_PINK, DUSK_ROSE, DUSK_PEACH, DUSK_BLUSH, DUSK_CREAM,
    SKIN_DEEP, SKIN_SHADOW, SKIN_MID, SKIN_LIGHT, SKIN_HIGHLIGHT,
    WOOD_BLACK, BROWN_DARKEST, BROWN_DARK, BROWN_MID, BROWN_LIGHT, WOOD_HIGHLIGHT, WOOD_LIT,
    RED_DEEP, RED_SHADOW, RED_RICH, RED_MID, RED_LIGHT, RED_HIGHLIGHT,
    BLUE_DEEP, BLUE_SHADOW, BLUE_RICH, BLUE_MID, BLUE_LIGHT, BLUE_HIGHLIGHT,
    YELLOW_DEEP, YELLOW_SHADOW, YELLOW_RICH, YELLOW_MID, YELLOW_LIGHT, YELLOW_HIGHLIGHT,
    GREEN_DEEP, GREEN_SHADOW, GREEN_RICH, GREEN_MID, GREEN_LIGHT, GREEN_HIGHLIGHT,
    ORANGE_DEEP, ORANGE_SHADOW, ORANGE_MID, ORANGE_LIGHT,
    TEAL_SHADOW, TEAL_MID, TEAL_LIGHT, TEAL_HIGHLIGHT,
    METAL_SHADOW, METAL_MID, WHITE_SHADOW, WHITE_MID, PURE_WHITE
)

# Cat Color Scheme (Warm Marmalade Ginger Tabby)
CAT_ORANGE_DARK = ORANGE_DEEP
CAT_ORANGE = ORANGE_MID
CAT_ORANGE_LIGHT = ORANGE_LIGHT
CAT_BELLY_WHITE = PURE_WHITE
CAT_BELLY_SHADOW = WHITE_SHADOW
CAT_INNER_EAR = DUSK_ROSE
CAT_NOSE = DUSK_ROSE
CAT_EYE_GREEN = GREEN_MID
CAT_EYE_LIGHT = GREEN_LIGHT
CAT_STRIPE = BROWN_MID
CAT_OUTLINE = OUTLINE


def ensure_bottom_ground(c: PixelCanvas, start_x: int, end_x: int, color=CAT_OUTLINE, y: int = 63):
    """Ensures at least one opaque pixel touches y=63 for the ground anchor rule."""
    has_contact = False
    for x in range(c.width):
        if c.get_pixel(x, y)[3] > 0:
            has_contact = True
            break
    if not has_contact:
        for x in range(start_x, end_x):
            c.set_pixel(x, y, color)


# ==============================================================================
# 1. CAT ANIMATIONS (96x64)
# ==============================================================================

def generate_cat_sleep() -> List[PixelCanvas]:
    """8 frames, 4 fps, loop: true.
    Curled up sleeping cat with rhythmic breathing and tail twitching at the end.
    """
    frames = []
    # Breathing offset: rises slightly on frames 2..5
    breath_offsets = [0, 1, 2, 2, 1, 1, 0, 0]
    tail_twitch = [0, 0, 0, 0, 1, 3, 2, 0]

    for f in range(8):
        c = PixelCanvas(96, 64, TRANSPARENT)
        bo = breath_offsets[f]
        tt = tail_twitch[f]

        # 1. Tail wrapped around body on ground (x=60..86, y=52..63)
        tail_tip_y = 48 - tt
        c.polygon([
            (62, 58), (72, 60), (84, 58), (86, 54),
            (82, tail_tip_y), (85, tail_tip_y - 2), (88, tail_tip_y), (88, 56),
            (84, 62), (72, 63), (60, 63)
        ], CAT_ORANGE, outline=CAT_OUTLINE)
        # Tail tip white dip
        c.circle(85, tail_tip_y, 2, CAT_BELLY_WHITE, outline=CAT_OUTLINE)
        # Tail stripes
        c.line(70, 60, 72, 63, CAT_STRIPE)
        c.line(78, 59, 80, 62, CAT_STRIPE)

        # 2. Main sleeping curled body (oval: center at 46, 50 - bo//2)
        body_y = 50 - bo
        c.circle(46, body_y, 16 + bo, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(52, body_y + 2, 14, CAT_ORANGE, outline=CAT_OUTLINE)

        # Body shading & warm fur highlights
        c.circle(44, body_y - 3, 10, CAT_ORANGE_LIGHT)
        c.line(36, body_y - 8, 56, body_y - 8, CAT_ORANGE_LIGHT)

        # Tabby stripes across back
        for sx in [40, 48, 56]:
            c.polygon([(sx, body_y - 12), (sx + 2, body_y - 6), (sx - 1, body_y - 2)], CAT_STRIPE)

        # Cream belly tuck
        c.circle(38, 54, 8, CAT_BELLY_WHITE)
        c.circle(38, 56, 7, CAT_BELLY_SHADOW)

        # 3. Head tucked close to front paws (center at 26, 48 - bo//2)
        hy = 48 - (bo // 2)
        c.circle(26, hy, 12, CAT_ORANGE, outline=CAT_OUTLINE)
        # Cheeks fluff
        c.circle(21, hy + 3, 6, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(31, hy + 3, 6, CAT_ORANGE, outline=CAT_OUTLINE)

        # Cream muzzle
        c.circle(24, hy + 4, 4, CAT_BELLY_WHITE)
        c.circle(28, hy + 4, 4, CAT_BELLY_WHITE)
        c.circle(26, hy + 2, 2, CAT_NOSE)

        # Sleeping peaceful curved eyes ^ ^
        c.line(19, hy + 1, 21, hy - 1, CAT_OUTLINE)
        c.line(21, hy - 1, 23, hy + 1, CAT_OUTLINE)
        c.line(29, hy + 1, 31, hy - 1, CAT_OUTLINE)
        c.line(31, hy - 1, 33, hy + 1, CAT_OUTLINE)

        # Ears folded back peacefully
        c.polygon([(16, hy - 6), (22, hy - 14), (25, hy - 6)], CAT_ORANGE, outline=CAT_OUTLINE)
        c.polygon([(18, hy - 6), (22, hy - 12), (24, hy - 6)], CAT_INNER_EAR)

        c.polygon([(28, hy - 6), (33, hy - 14), (37, hy - 6)], CAT_ORANGE, outline=CAT_OUTLINE)
        c.polygon([(29, hy - 6), (33, hy - 12), (35, hy - 6)], CAT_INNER_EAR)

        # Whiskers
        c.line(16, hy + 4, 11, hy + 3, WHITE_SHADOW)
        c.line(16, hy + 6, 12, hy + 8, WHITE_SHADOW)
        c.line(34, hy + 4, 39, hy + 3, WHITE_SHADOW)
        c.line(34, hy + 6, 38, hy + 8, WHITE_SHADOW)

        # Tucked front white paws under chin (y=56..63)
        c.circle(24, 59, 4, CAT_BELLY_WHITE, outline=CAT_OUTLINE)
        c.circle(31, 59, 4, CAT_BELLY_WHITE, outline=CAT_OUTLINE)
        c.line(24, 60, 24, 62, CAT_OUTLINE)
        c.line(31, 60, 31, 62, CAT_OUTLINE)

        # Grounding row y=63
        ensure_bottom_ground(c, 22, 76, CAT_OUTLINE)

        frames.append(c)

    return frames


def generate_cat_wake() -> List[PixelCanvas]:
    """6 frames, 12 fps, loop: false.
    Cat wakes up: eyes crack open, lifts head, ears swivel alertly.
    """
    frames = []

    for f in range(6):
        c = PixelCanvas(96, 64, TRANSPARENT)

        # Head lift progression
        head_y = 48 - (f * 4)  # 48 down to 28
        body_spread = 52 - (f * 2)

        # Tail resting behind, lifting slightly in frame 5
        tail_y = 58 - (1 if f > 3 else 0)
        c.polygon([
            (60, 58), (72, 60), (84, 58), (88, 54 - f),
            (84, 50 - f), (86, 48 - f), (90, 52 - f), (86, 62), (60, 63)
        ], CAT_ORANGE, outline=CAT_OUTLINE)

        # Body settling into upright sitting
        c.circle(52, 48, 14, CAT_ORANGE, outline=CAT_OUTLINE)
        c.polygon([(36, 60), (44, 38), (62, 40), (68, 62)], CAT_ORANGE, outline=CAT_OUTLINE)
        # Chest cream patch
        c.polygon([(38, 48), (44, 38), (48, 48), (46, 58), (38, 58)], CAT_BELLY_WHITE)

        # Front legs planting on ground
        leg_y = 46 + (f * 2)
        c.rect(34, 46, 6, 17, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(36, 61, 3, CAT_BELLY_WHITE, outline=CAT_OUTLINE)
        c.rect(46, 46, 6, 17, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(48, 61, 3, CAT_BELLY_WHITE, outline=CAT_OUTLINE)

        # Head
        hx = 38
        hy = head_y
        c.circle(hx, hy, 12, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(hx - 5, hy + 3, 5, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(hx + 5, hy + 3, 5, CAT_ORANGE, outline=CAT_OUTLINE)

        # Muzzle
        c.circle(hx - 2, hy + 4, 3, CAT_BELLY_WHITE)
        c.circle(hx + 2, hy + 4, 3, CAT_BELLY_WHITE)
        c.circle(hx, hy + 2, 2, CAT_NOSE)

        # Eyes: progression from closed to wide open
        if f == 0:
            # Closed
            c.line(hx - 6, hy, hx - 2, hy, CAT_OUTLINE)
            c.line(hx + 2, hy, hx + 6, hy, CAT_OUTLINE)
        elif f == 1:
            # Slit open
            c.line(hx - 6, hy, hx - 2, hy, CAT_EYE_GREEN)
            c.line(hx + 2, hy, hx + 6, hy, CAT_EYE_GREEN)
            c.line(hx - 7, hy - 1, hx - 1, hy - 1, CAT_OUTLINE)
            c.line(hx + 1, hy - 1, hx + 7, hy - 1, CAT_OUTLINE)
        elif f in (2, 3):
            # Half open
            c.rect(hx - 6, hy - 2, 5, 4, CAT_EYE_GREEN, outline=CAT_OUTLINE)
            c.rect(hx + 2, hy - 2, 5, 4, CAT_EYE_GREEN, outline=CAT_OUTLINE)
            c.line(hx - 4, hy - 1, hx - 4, hy + 1, CAT_OUTLINE)
            c.line(hx + 4, hy - 1, hx + 4, hy + 1, CAT_OUTLINE)
        else:
            # Wide open
            c.circle(hx - 5, hy - 1, 3, CAT_EYE_GREEN, outline=CAT_OUTLINE)
            c.circle(hx + 5, hy - 1, 3, CAT_EYE_GREEN, outline=CAT_OUTLINE)
            c.line(hx - 5, hy - 2, hx - 5, hy, CAT_OUTLINE)
            c.line(hx + 5, hy - 2, hx + 5, hy, CAT_OUTLINE)
            c.set_pixel(hx - 6, hy - 2, PURE_WHITE)
            c.set_pixel(hx + 4, hy - 2, PURE_WHITE)

        # Ears swiveling upward
        ear_angle = f * 3  # swivels from folded back to straight up
        c.polygon([
            (hx - 8, hy - 6),
            (hx - 12 + (f // 2), hy - 14 - (f * 2)),
            (hx - 2, hy - 8)
        ], CAT_ORANGE, outline=CAT_OUTLINE)
        c.polygon([
            (hx - 7, hy - 6),
            (hx - 11 + (f // 2), hy - 12 - (f * 2)),
            (hx - 3, hy - 7)
        ], CAT_INNER_EAR)

        c.polygon([
            (hx + 2, hy - 8),
            (hx + 12 - (f // 2), hy - 14 - (f * 2)),
            (hx + 8, hy - 6)
        ], CAT_ORANGE, outline=CAT_OUTLINE)
        c.polygon([
            (hx + 3, hy - 7),
            (hx + 11 - (f // 2), hy - 12 - (f * 2)),
            (hx + 7, hy - 6)
        ], CAT_INNER_EAR)

        # Whiskers
        c.line(hx - 8, hy + 4, hx - 14, hy + 3, WHITE_SHADOW)
        c.line(hx - 8, hy + 6, hx - 14, hy + 7, WHITE_SHADOW)
        c.line(hx + 8, hy + 4, hx + 14, hy + 3, WHITE_SHADOW)
        c.line(hx + 8, hy + 6, hx + 14, hy + 7, WHITE_SHADOW)

        ensure_bottom_ground(c, 32, 70, CAT_OUTLINE)
        frames.append(c)

    return frames


def generate_cat_watch() -> List[PixelCanvas]:
    """8 frames, 6 fps, loop: true.
    Cat sitting upright, head and eyes tracking left to right and back, tail swishing slowly.
    """
    frames = []
    # Head x-offsets: tracking left (-3) to right (+3) and back
    look_offsets = [-3, -4, -2, 0, 2, 4, 3, 0]
    tail_swish = [-4, -2, 0, 3, 5, 3, 0, -2]

    for f in range(8):
        c = PixelCanvas(96, 64, TRANSPARENT)
        lx = look_offsets[f]
        ts = tail_swish[f]

        # 1. Tail swishing on ground
        c.polygon([
            (62, 58), (72, 60), (82 + ts, 56), (86 + ts, 48),
            (89 + ts, 49), (85 + ts, 58), (76, 62), (60, 63)
        ], CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(88 + ts, 48, 2, CAT_BELLY_WHITE, outline=CAT_OUTLINE)

        # 2. Upright sitting body
        c.polygon([(34, 62), (40, 32), (58, 32), (66, 62)], CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(50, 46, 14, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(48, 38, 10, CAT_ORANGE_LIGHT)

        # Tabby stripes on flanks
        c.line(56, 36, 62, 44, CAT_STRIPE)
        c.line(58, 46, 64, 52, CAT_STRIPE)

        # Cream chest / bib
        c.polygon([(42, 34), (52, 34), (54, 52), (48, 58), (40, 52)], CAT_BELLY_WHITE)
        c.polygon([(43, 36), (51, 36), (52, 50), (48, 56), (41, 50)], CAT_BELLY_SHADOW)

        # Front legs and white paws sitting side-by-side
        c.rect(38, 42, 6, 21, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(41, 61, 3, CAT_BELLY_WHITE, outline=CAT_OUTLINE)
        c.rect(48, 42, 6, 21, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(51, 61, 3, CAT_BELLY_WHITE, outline=CAT_OUTLINE)

        # 3. Head (tracking smoothly at hx = 46 + lx)
        hx = 46 + lx
        hy = 22
        c.circle(hx, hy, 12, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(hx - 5, hy + 3, 5, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(hx + 5, hy + 3, 5, CAT_ORANGE, outline=CAT_OUTLINE)

        # Forehead stripes
        c.line(hx, hy - 11, hx, hy - 6, CAT_STRIPE)
        c.line(hx - 3, hy - 10, hx - 2, hy - 6, CAT_STRIPE)
        c.line(hx + 3, hy - 10, hx + 2, hy - 6, CAT_STRIPE)

        # Muzzle
        c.circle(hx - 2, hy + 4, 3, CAT_BELLY_WHITE)
        c.circle(hx + 2, hy + 4, 3, CAT_BELLY_WHITE)
        c.circle(hx, hy + 2, 2, CAT_NOSE)

        # Big curious green eyes with pupils tracking
        eye_look = 1 if lx > 0 else (-1 if lx < 0 else 0)
        c.circle(hx - 5, hy - 1, 4, CAT_EYE_GREEN, outline=CAT_OUTLINE)
        c.circle(hx + 5, hy - 1, 4, CAT_EYE_GREEN, outline=CAT_OUTLINE)
        # Slit pupils shifting with head look direction
        c.line(hx - 5 + eye_look, hy - 3, hx - 5 + eye_look, hy + 1, CAT_OUTLINE)
        c.line(hx + 5 + eye_look, hy - 3, hx + 5 + eye_look, hy + 1, CAT_OUTLINE)
        # Specular glint
        c.set_pixel(hx - 6, hy - 2, PURE_WHITE)
        c.set_pixel(hx + 4, hy - 2, PURE_WHITE)

        # Ears upright and alert
        c.polygon([(hx - 9, hy - 6), (hx - 8, hy - 18), (hx - 1, hy - 8)], CAT_ORANGE, outline=CAT_OUTLINE)
        c.polygon([(hx - 8, hy - 7), (hx - 7, hy - 16), (hx - 2, hy - 8)], CAT_INNER_EAR)

        c.polygon([(hx + 1, hy - 8), (hx + 8, hy - 18), (hx + 9, hy - 6)], CAT_ORANGE, outline=CAT_OUTLINE)
        c.polygon([(hx + 2, hy - 8), (hx + 7, hy - 16), (hx + 8, hy - 7)], CAT_INNER_EAR)

        # Whiskers
        c.line(hx - 7, hy + 4, hx - 14, hy + 3, WHITE_SHADOW)
        c.line(hx - 7, hy + 6, hx - 14, hy + 7, WHITE_SHADOW)
        c.line(hx + 7, hy + 4, hx + 14, hy + 3, WHITE_SHADOW)
        c.line(hx + 7, hy + 6, hx + 14, hy + 7, WHITE_SHADOW)

        ensure_bottom_ground(c, 34, 68, CAT_OUTLINE)
        frames.append(c)

    return frames


def generate_cat_startle() -> List[PixelCanvas]:
    """8 frames, 20 fps, loop: false.
    Huge puff-up jump when P1 trips:
    Squash, explosive arch jump with spiky bristling fur & bottle-brush tail, land with shock.
    """
    frames = []

    # Jump heights for center of mass
    jump_y_offsets = [0, 6, -14, -20, -12, 4, 2, 0]

    for f in range(8):
        c = PixelCanvas(96, 64, TRANSPARENT)
        jy = jump_y_offsets[f]

        if f == 0:
            # Neutral alert before snap
            c.polygon([(34, 62), (40, 32), (58, 32), (66, 62)], CAT_ORANGE, outline=CAT_OUTLINE)
            c.circle(46, 22, 12, CAT_ORANGE, outline=CAT_OUTLINE)
            c.circle(41, 20, 3, CAT_EYE_GREEN, outline=CAT_OUTLINE)
            c.circle(51, 20, 3, CAT_EYE_GREEN, outline=CAT_OUTLINE)
        elif f == 1:
            # Anticipation squash: compressed flat to floor, ears flat back
            c.circle(48, 54, 18, CAT_ORANGE, outline=CAT_OUTLINE)
            c.circle(48, 48, 12, CAT_ORANGE_LIGHT)
            # Flattened head
            c.circle(38, 46, 10, CAT_ORANGE, outline=CAT_OUTLINE)
            # Giant black shock eyes
            c.circle(34, 44, 4, CAT_OUTLINE)
            c.circle(42, 44, 4, CAT_OUTLINE)
            c.set_pixel(33, 43, PURE_WHITE)
            c.set_pixel(41, 43, PURE_WHITE)
            # Airplane ears flat out
            c.polygon([(26, 48), (14, 46), (28, 44)], CAT_ORANGE, outline=CAT_OUTLINE)
            c.polygon([(46, 44), (58, 46), (48, 48)], CAT_ORANGE, outline=CAT_OUTLINE)
        elif f in (2, 3, 4):
            # AIRBORNE EXPLOSION: Arched spiky spine, bottle-brush tail, claws out!
            cy = 38 + jy
            # Bottle brush tail pointing straight up with jagged zig-zags
            c.polygon([
                (70, cy + 6), (78, cy - 8), (74, cy - 22), (80, cy - 26),
                (84, cy - 20), (82, cy - 8), (76, cy + 10)
            ], CAT_ORANGE, outline=CAT_OUTLINE)
            # Spiky tail tufts
            c.polygon([(78, cy - 14), (88, cy - 16), (80, cy - 10)], CAT_ORANGE_LIGHT, outline=CAT_OUTLINE)
            c.polygon([(76, cy - 4), (86, cy - 6), (78, cy)], CAT_ORANGE, outline=CAT_OUTLINE)

            # High arched spiky body
            c.circle(48, cy, 16, CAT_ORANGE, outline=CAT_OUTLINE)
            c.circle(48, cy - 6, 12, CAT_ORANGE_LIGHT)
            # Spiky fur tufts along the arched spine
            for sp_x in [38, 44, 50, 56]:
                c.polygon([(sp_x - 3, cy - 14), (sp_x, cy - 21), (sp_x + 3, cy - 14)], CAT_ORANGE_LIGHT, outline=CAT_OUTLINE)

            # Stiff extended splayed legs reaching downward
            c.line(36, cy + 10, 32, 60, CAT_OUTLINE)
            c.line(37, cy + 10, 33, 60, CAT_ORANGE)
            c.line(42, cy + 10, 40, 60, CAT_ORANGE)
            c.line(54, cy + 10, 56, 60, CAT_ORANGE)
            c.line(60, cy + 10, 64, 60, CAT_ORANGE)
            # Splayed needle claws at paw tips
            for px in [32, 40, 56, 64]:
                c.circle(px, 60, 3, CAT_BELLY_WHITE, outline=CAT_OUTLINE)
                c.line(px - 1, 62, px - 1, 63, WHITE_SHADOW)
                c.line(px + 1, 62, px + 1, 63, WHITE_SHADOW)

            # Startled head turned side/front
            hx, hy = 32, cy - 8
            c.circle(hx, hy, 13, CAT_ORANGE, outline=CAT_OUTLINE)
            # Spiky cheek fluff
            c.polygon([(hx - 10, hy + 2), (hx - 18, hy + 5), (hx - 10, hy + 8)], CAT_ORANGE, outline=CAT_OUTLINE)
            c.polygon([(hx + 8, hy + 2), (hx + 16, hy + 5), (hx + 8, hy + 8)], CAT_ORANGE, outline=CAT_OUTLINE)

            # Giant bugged-out eyes with pinpoint pupils
            c.circle(hx - 5, hy - 2, 5, PURE_WHITE, outline=CAT_OUTLINE)
            c.circle(hx + 5, hy - 2, 5, PURE_WHITE, outline=CAT_OUTLINE)
            c.set_pixel(hx - 5, hy - 2, CAT_OUTLINE)
            c.set_pixel(hx + 5, hy - 2, CAT_OUTLINE)

            # Open screaming/hissing mouth
            c.circle(hx, hy + 5, 3, RED_SHADOW, outline=CAT_OUTLINE)
            c.set_pixel(hx - 2, hy + 4, PURE_WHITE)  # tiny fang
            c.set_pixel(hx + 2, hy + 4, PURE_WHITE)

            # Tall alert startled ears
            c.polygon([(hx - 9, hy - 8), (hx - 12, hy - 24), (hx - 2, hy - 10)], CAT_ORANGE, outline=CAT_OUTLINE)
            c.polygon([(hx + 2, hy - 10), (hx + 12, hy - 24), (hx + 9, hy - 8)], CAT_ORANGE, outline=CAT_OUTLINE)
        else:
            # f == 5, 6, 7: Impact land & settling, fur still slightly poofed
            c.circle(48, 52, 16, CAT_ORANGE, outline=CAT_OUTLINE)
            c.circle(48, 48, 12, CAT_ORANGE_LIGHT)
            # Fur slowly settling
            c.circle(36, 44, 11, CAT_ORANGE, outline=CAT_OUTLINE)
            c.circle(32, 42, 4, PURE_WHITE, outline=CAT_OUTLINE)
            c.circle(40, 42, 4, PURE_WHITE, outline=CAT_OUTLINE)
            c.set_pixel(32, 42, CAT_EYE_GREEN)
            c.set_pixel(40, 42, CAT_EYE_GREEN)
            # Tail puffy resting behind
            c.polygon([(64, 58), (76, 52), (86, 44), (88, 52), (78, 62), (64, 63)], CAT_ORANGE, outline=CAT_OUTLINE)
            # Front paws gripping floor
            c.circle(32, 60, 4, CAT_BELLY_WHITE, outline=CAT_OUTLINE)
            c.circle(42, 60, 4, CAT_BELLY_WHITE, outline=CAT_OUTLINE)
            c.circle(58, 60, 4, CAT_BELLY_WHITE, outline=CAT_OUTLINE)

        ensure_bottom_ground(c, 24, 76, CAT_OUTLINE)
        frames.append(c)

    return frames


def generate_cat_lick() -> List[PixelCanvas]:
    """8 frames, 8 fps, loop: true.
    Cat sitting upright, lifting right paw to lick it and groom cheek/ear.
    """
    frames = []
    # Paw y & x positions across the grooming cycle
    paw_coords = [
        (38, 58), (36, 46), (34, 32), (32, 28),
        (34, 26), (36, 32), (36, 44), (38, 54)
    ]
    head_tilt = [0, 1, 2, 3, 2, 1, 0, 0]

    for f in range(8):
        c = PixelCanvas(96, 64, TRANSPARENT)
        px, py = paw_coords[f]
        ht = head_tilt[f]

        # Tail curled beside
        c.polygon([
            (62, 58), (74, 56), (84, 52), (86, 46),
            (88, 48), (86, 56), (76, 62), (60, 63)
        ], CAT_ORANGE, outline=CAT_OUTLINE)

        # Body sitting
        c.polygon([(34, 62), (40, 32), (58, 32), (66, 62)], CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(50, 46, 14, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(48, 38, 10, CAT_ORANGE_LIGHT)

        # Left leg firmly planted
        c.rect(48, 42, 6, 21, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(51, 61, 3, CAT_BELLY_WHITE, outline=CAT_OUTLINE)

        # Right leg (the grooming leg, moving with px, py)
        c.polygon([(36, 42), (px, py), (px + 6, py), (42, 42)], CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(px + 2, py + 2, 4, CAT_BELLY_WHITE, outline=CAT_OUTLINE)
        # Pink paw pad visible on paw underside
        if py < 40:
            c.circle(px + 2, py + 2, 2, DUSK_ROSE)

        # Head tilted toward the raised paw
        hx = 44 - ht
        hy = 22 + ht
        c.circle(hx, hy, 12, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(hx - 5, hy + 3, 5, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(hx + 5, hy + 3, 5, CAT_ORANGE, outline=CAT_OUTLINE)

        # Muzzle & Tongue licking
        c.circle(hx - 2, hy + 4, 3, CAT_BELLY_WHITE)
        c.circle(hx + 2, hy + 4, 3, CAT_BELLY_WHITE)
        c.circle(hx, hy + 2, 2, CAT_NOSE)

        if f in (2, 3, 4):
            # Cute pink tongue licking the paw!
            c.polygon([(hx - 3, hy + 4), (px + 4, py - 1), (hx, hy + 7)], DUSK_ROSE, outline=CAT_OUTLINE)
            c.set_pixel(px + 4, py - 1, DUSK_BLUSH)
            # Eyes closed in bliss > <
            c.line(hx - 6, hy - 1, hx - 4, hy + 1, CAT_OUTLINE)
            c.line(hx - 4, hy + 1, hx - 2, hy - 1, CAT_OUTLINE)
            c.line(hx + 2, hy - 1, hx + 4, hy + 1, CAT_OUTLINE)
            c.line(hx + 4, hy + 1, hx + 6, hy - 1, CAT_OUTLINE)
        else:
            # Eyes half open
            c.rect(hx - 6, hy - 2, 5, 3, CAT_EYE_GREEN, outline=CAT_OUTLINE)
            c.rect(hx + 2, hy - 2, 5, 3, CAT_EYE_GREEN, outline=CAT_OUTLINE)

        # Ears
        c.polygon([(hx - 9, hy - 6), (hx - 9 - ht, hy - 17), (hx - 2, hy - 8)], CAT_ORANGE, outline=CAT_OUTLINE)
        c.polygon([(hx + 1, hy - 8), (hx + 8, hy - 17), (hx + 9, hy - 6)], CAT_ORANGE, outline=CAT_OUTLINE)

        ensure_bottom_ground(c, 34, 68, CAT_OUTLINE)
        frames.append(c)

    return frames


def generate_cat_yawn() -> List[PixelCanvas]:
    """8 frames, 8 fps, loop: true.
    Cat stretch and big wide yawn:
    Reaches front paws out long, chest sinks, back arches in big bow, mouth gapes wide!
    """
    frames = []

    for f in range(8):
        c = PixelCanvas(96, 64, TRANSPARENT)

        # Tail curves upward with the big stretch
        tail_high = 38 - (f * 2 if f < 5 else (8 - f) * 2)
        c.polygon([
            (68, 50), (76, 44), (84, tail_high), (86, tail_high - 6),
            (88, tail_high - 4), (86, 48), (74, 56), (68, 62)
        ], CAT_ORANGE, outline=CAT_OUTLINE)

        # Hindquarters held up high (classic cat stretch posture)
        c.circle(60, 44, 14, CAT_ORANGE, outline=CAT_OUTLINE)
        # Hind legs planted back
        c.rect(60, 46, 7, 17, CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(63, 61, 3, CAT_BELLY_WHITE, outline=CAT_OUTLINE)

        # Front body slopes downward toward floor in stretch
        front_reach = min(36, 18 + f * 3 if f < 5 else 36 - (f - 4) * 4)
        chest_y = 50 + (f if f < 4 else (7 - f))

        c.polygon([
            (60, 36), (66, 46), (36, chest_y), (48 - front_reach, 60),
            (32, chest_y - 8)
        ], CAT_ORANGE, outline=CAT_OUTLINE)

        # Extended front legs reaching forward on floor
        paw_x = 44 - front_reach
        c.line(40, chest_y - 2, paw_x, 61, CAT_OUTLINE)
        c.line(40, chest_y - 1, paw_x, 61, CAT_ORANGE)
        c.circle(paw_x, 61, 3, CAT_BELLY_WHITE, outline=CAT_OUTLINE)
        # Claws dug in
        c.line(paw_x - 3, 62, paw_x - 1, 62, WHITE_SHADOW)

        # Head dipping low and yawning
        hx = paw_x + 12
        hy = chest_y - 10
        c.circle(hx, hy, 11, CAT_ORANGE, outline=CAT_OUTLINE)

        # Yawn opening progression
        yawn_size = [0, 2, 5, 7, 8, 6, 3, 0][f]

        if yawn_size > 2:
            # Huge yawning mouth!
            c.circle(hx, hy + 4, yawn_size, RED_DEEP, outline=CAT_OUTLINE)
            c.circle(hx, hy + 4, yawn_size - 1, RED_SHADOW)
            # Curled pink tongue
            c.circle(hx, hy + 5, max(1, yawn_size - 3), DUSK_ROSE)
            # Sharp white fangs top and bottom
            c.set_pixel(hx - 2, hy + 4 - yawn_size + 2, PURE_WHITE)
            c.set_pixel(hx + 2, hy + 4 - yawn_size + 2, PURE_WHITE)
            c.set_pixel(hx - 2, hy + 4 + yawn_size - 2, PURE_WHITE)
            c.set_pixel(hx + 2, hy + 4 + yawn_size - 2, PURE_WHITE)

            # Squinted shut eyes > <
            c.line(hx - 7, hy - 3, hx - 4, hy - 1, CAT_OUTLINE)
            c.line(hx - 7, hy + 1, hx - 4, hy - 1, CAT_OUTLINE)
            c.line(hx + 7, hy - 3, hx + 4, hy - 1, CAT_OUTLINE)
            c.line(hx + 7, hy + 1, hx + 4, hy - 1, CAT_OUTLINE)
        else:
            c.circle(hx, hy + 3, 2, CAT_NOSE)
            c.circle(hx - 4, hy - 1, 3, CAT_EYE_GREEN, outline=CAT_OUTLINE)
            c.circle(hx + 4, hy - 1, 3, CAT_EYE_GREEN, outline=CAT_OUTLINE)

        # Ears pinned back in stretch
        c.polygon([(hx - 6, hy - 6), (hx - 14, hy - 12), (hx - 4, hy - 10)], CAT_ORANGE, outline=CAT_OUTLINE)
        c.polygon([(hx + 4, hy - 10), (hx + 14, hy - 12), (hx + 6, hy - 6)], CAT_ORANGE, outline=CAT_OUTLINE)

        ensure_bottom_ground(c, paw_x - 2, 70, CAT_OUTLINE)
        frames.append(c)

    return frames


def generate_cat_zoomies() -> List[PixelCanvas]:
    """8 frames, 20 fps, loop: true.
    Wild galloping sprint across screen!
    Full 4-beat gallop with extended flight, compression, hind push, and trailing dust.
    """
    frames = []

    for f in range(8):
        c = PixelCanvas(96, 64, TRANSPARENT)

        # Horizontal bullet cat gallop positions
        # Gallop cycle phases:
        # f0: Extended airborne stretch
        # f1: Front paws contact
        # f2: Front legs compress
        # f3: Gathered airborne tuck
        # f4: Hind paws plant
        # f5: Explosive hind push
        # f6: Hind thrust airborne
        # f7: Front reaching out

        body_y = [42, 44, 46, 40, 42, 44, 40, 41][f]
        front_x = [68, 64, 58, 48, 54, 62, 70, 72][f]
        hind_x = [24, 28, 34, 40, 32, 22, 20, 22][f]

        # Horizontal elongated body
        c.polygon([
            (hind_x, body_y + 4), (hind_x + 8, body_y - 6),
            (front_x - 8, body_y - 6), (front_x, body_y + 4),
            (front_x - 6, body_y + 8), (hind_x + 6, body_y + 8)
        ], CAT_ORANGE, outline=CAT_OUTLINE)
        # Back highlight
        c.line(hind_x + 8, body_y - 6, front_x - 8, body_y - 6, CAT_ORANGE_LIGHT)

        # Comet tail streaming behind
        tail_tip_x = hind_x - 20
        tail_tip_y = body_y - 12 + (f % 4) * 3
        c.polygon([
            (hind_x + 2, body_y), (hind_x - 8, body_y - 4), (tail_tip_x, tail_tip_y),
            (tail_tip_x + 4, tail_tip_y + 2), (hind_x - 6, body_y + 4)
        ], CAT_ORANGE, outline=CAT_OUTLINE)
        c.circle(tail_tip_x, tail_tip_y, 2, CAT_BELLY_WHITE, outline=CAT_OUTLINE)

        # Front legs
        front_paw_y = 61 if f in (1, 2) else 50 - (f % 3) * 4
        c.line(front_x - 6, body_y + 4, front_x + 4, front_paw_y, CAT_ORANGE)
        c.line(front_x - 6, body_y + 5, front_x + 4, front_paw_y, CAT_OUTLINE)
        c.circle(front_x + 4, front_paw_y, 3, CAT_BELLY_WHITE, outline=CAT_OUTLINE)

        # Hind legs
        hind_paw_y = 61 if f in (4, 5) else 52 - ((f + 2) % 3) * 4
        c.line(hind_x + 4, body_y + 4, hind_x - 6, hind_paw_y, CAT_ORANGE)
        c.line(hind_x + 4, body_y + 5, hind_x - 6, hind_paw_y, CAT_OUTLINE)
        c.circle(hind_x - 6, hind_paw_y, 3, CAT_BELLY_WHITE, outline=CAT_OUTLINE)

        # Head thrust forward
        hx = front_x + 10
        hy = body_y - 4
        c.circle(hx, hy, 10, CAT_ORANGE, outline=CAT_OUTLINE)

        # Wild zoomies eyes (huge dilated black pupils, crazed look!)
        c.circle(hx - 2, hy - 2, 4, CAT_OUTLINE)
        c.set_pixel(hx - 3, hy - 3, PURE_WHITE)
        c.circle(hx + 5, hy - 2, 4, CAT_OUTLINE)
        c.set_pixel(hx + 4, hy - 3, PURE_WHITE)

        # Pinned back aerodynamic ears
        c.polygon([(hx - 6, hy - 4), (hx - 16, hy - 8), (hx - 4, hy - 8)], CAT_ORANGE, outline=CAT_OUTLINE)
        c.polygon([(hx - 4, hy - 8), (hx - 14, hy - 11), (hx - 2, hy - 8)], CAT_ORANGE, outline=CAT_OUTLINE)

        # Snout / whiskers streaming back
        c.circle(hx + 7, hy + 2, 2, CAT_NOSE)
        c.line(hx + 6, hy + 3, hx - 2, hy + 2, WHITE_SHADOW)
        c.line(hx + 6, hy + 5, hx - 1, hy + 6, WHITE_SHADOW)

        # Trailing speed dust puffs behind paws
        if f in (1, 2, 4, 5):
            puff_x = (front_x if f in (1, 2) else hind_x) - 10
            c.circle(puff_x, 60, 2, WHITE_SHADOW)
            c.set_pixel(puff_x - 3, 62, PURE_WHITE)

        ensure_bottom_ground(c, 16, 80, CAT_OUTLINE)
        frames.append(c)

    return frames


# ==============================================================================
# 2. PARENT ASSETS (128x192 sheets and 192x96 speech bubbles)
# ==============================================================================

def generate_parent_peek_v2() -> List[PixelCanvas]:
    """128x192, 6 frames, fps 6, loop: false.
    High-res v2 parent peeking through cracked door with bright hallway light beam,
    curlers, glowing red eye, and giant wagging finger with comic anger steam.
    """
    frames = []
    finger_y_offsets = [0, -4, 3, -3, 4, 0]

    for f in range(6):
        c = PixelCanvas(128, 192, TRANSPARENT)
        fy = 96 + finger_y_offsets[f]

        # 1. Door frame / wall molding on right edge (x=112..127)
        c.rect(112, 0, 16, 192, BROWN_MID, outline=OUTLINE)
        c.line(112, 0, 112, 191, WOOD_HIGHLIGHT)
        c.line(113, 0, 113, 191, BROWN_LIGHT)
        c.line(125, 0, 125, 191, BROWN_DARKEST)
        c.line(127, 0, 127, 191, VOID_BLACK)

        # 2. Cracked open wooden door slab (x=door_x..112)
        door_x = 84 + (f % 2) * 2
        c.rect(door_x, 0, 112 - door_x, 192, BROWN_DARKEST)
        # Inner vertical door edge catching bright light
        c.line(door_x, 0, door_x, 191, WOOD_HIGHLIGHT)
        c.line(door_x + 1, 0, door_x + 1, 191, PURE_WHITE)

        # Recessed wood panels on door
        for py0, py1 in [(16, 76), (108, 176)]:
            if 108 > door_x + 6:
                c.rect(door_x + 6, py0, 104 - door_x, py1 - py0, BROWN_DARK, outline=OUTLINE)

        # Brass doorknob and lockplate
        c.rect(door_x + 4, 100, 6, 10, YELLOW_MID, outline=OUTLINE)
        c.set_pixel(door_x + 6, 102, YELLOW_LIGHT)
        c.set_pixel(door_x + 6, 106, YELLOW_SHADOW)

        # 3. Hallway light beam pouring into room (x=beam_left..door_x)
        for y in range(192):
            beam_left = max(12, int(door_x - 36 - (y * 0.35)))
            for x in range(beam_left, door_x):
                dist = door_x - x
                if dist < 12:
                    c.set_pixel(x, y, YELLOW_LIGHT)
                elif dist < 28:
                    c.set_pixel(x, y, YELLOW_LIGHT if (x + y) % 2 == 0 else YELLOW_MID)
                elif dist < 44:
                    if (x + y) % 2 == 0:
                        c.set_pixel(x, y, YELLOW_MID)
                    elif (x + y) % 4 == 0:
                        c.set_pixel(x, y, YELLOW_SHADOW)
                elif (x + y) % 4 == 0:
                    c.set_pixel(x, y, YELLOW_SHADOW)

        # Floorboards illuminated
        for y in range(160, 192):
            for x in range(16, door_x):
                if (x + y) % 3 == 0 and c.get_pixel(x, y) == TRANSPARENT:
                    c.set_pixel(x, y, WOOD_HIGHLIGHT if y % 4 == 0 else BROWN_DARK)

        # 4. Imposing Parent Silhouette in doorway (x=44..92)
        # Bathrobe body
        for y in range(56, 184):
            bw = int(24 + (y - 56) * 0.28)
            bx0 = 68 - (bw // 2)
            bx1 = bx0 + bw
            c.rect(bx0, y, bw, 1, OUTLINE)
            c.rect(bx0 + 3, y, max(1, bw - 6), 1, SHADOW_DEEP)
            # Hallway rim-light on back edge
            c.line(bx1 - 2, y, bx1 - 1, y, YELLOW_LIGHT)
            c.set_pixel(bx1 - 3, y, YELLOW_MID)

        # Bathrobe sash / belt tied at waist
        c.rect(52, 104, 32, 6, SHADOW_MID, outline=OUTLINE)
        c.line(56, 110, 60, 126, PURPLE_LIGHT)
        c.line(58, 110, 62, 128, OUTLINE)

        # Head silhouette
        c.circle(64, 40, 16, OUTLINE)
        c.circle(64, 40, 13, SHADOW_DEEP)
        # Hallway rim light on hair/head
        c.line(76, 32, 78, 48, YELLOW_LIGHT)
        c.line(75, 28, 77, 44, YELLOW_MID)

        # Curlers / Rollers in hair (4 distinct curlers)
        curlers = [(52, 22), (64, 18), (76, 22), (82, 34)]
        for cx, cy in curlers:
            c.rect(cx - 4, cy - 4, 8, 6, PURPLE_LIGHT, outline=OUTLINE)
            c.rect(cx - 2, cy - 2, 4, 3, DUSK_PINK)
            c.line(cx + 2, cy - 3, cx + 3, cy + 1, YELLOW_LIGHT)

        # Glowing angry red eye at (52, 40)
        c.circle(52, 40, 3, RED_LIGHT, outline=OUTLINE)
        c.set_pixel(52, 40, RED_MID)
        c.set_pixel(51, 39, OUTLINE)  # angry brow ridge
        c.set_pixel(52, 39, OUTLINE)
        c.set_pixel(53, 39, OUTLINE)
        if f in (1, 3, 4):
            # Eye glare laser streak
            c.line(42, 40, 49, 40, RED_LIGHT)
            c.set_pixel(40, 40, RED_MID)

        # 5. GIANT ANGRY POINTING FINGER extending LEFT into bedroom
        # Sleeve
        c.rect(52, fy - 6, 16, 18, OUTLINE)
        c.rect(54, fy - 4, 12, 14, SHADOW_DEEP)
        c.line(52, fy - 6, 52, fy + 11, PURPLE_LIGHT)

        # Forearm
        c.rect(40, fy - 4, 14, 14, SHADOW_DEEP, outline=OUTLINE)

        # Clenched fist
        c.rect(32, fy - 2, 12, 16, SHADOW_DEEP, outline=OUTLINE)
        for ky in [fy + 3, fy + 7, fy + 11]:
            c.line(32, ky, 42, ky, OUTLINE)
            c.set_pixel(34, ky - 1, PURPLE_LIGHT)

        # Giant pointing index finger pointing straight at P1
        c.rect(6, fy - 4, 28, 10, SHADOW_DEEP, outline=OUTLINE)
        c.line(8, fy - 4, 32, fy - 4, PURPLE_LIGHT)
        c.line(8, fy - 2, 32, fy - 2, SKIN_MID)
        c.line(6, fy + 5, 32, fy + 5, OUTLINE)
        # Fingertip
        c.circle(8, fy + 1, 4, SHADOW_DEEP, outline=OUTLINE)
        c.set_pixel(6, fy, PURPLE_LIGHT)
        c.rect(10, fy - 2, 4, 3, WHITE_SHADOW)  # fingernail

        # 6. Anger steam puffs & cross-vein pop marks above head
        if f in (0, 5):
            c.circle(56, 12, 4, WHITE_SHADOW)
            c.circle(56, 12, 2, PURE_WHITE)
        elif f in (1, 2):
            c.circle(52, 8, 6, WHITE_SHADOW)
            c.circle(52, 8, 4, PURE_WHITE)
            c.circle(62, 6, 4, WHITE_SHADOW)
            c.set_pixel(62, 6, PURE_WHITE)
            # Red anger cross-vein pop!
            c.line(70, 6, 78, 6, RED_LIGHT)
            c.line(70, 10, 78, 10, RED_LIGHT)
            c.line(72, 4, 72, 12, RED_LIGHT)
            c.line(76, 4, 76, 12, RED_LIGHT)
            c.set_pixel(74, 8, RED_MID)
        elif f in (3, 4):
            c.circle(48, 6, 4, WHITE_SHADOW)
            c.circle(48, 6, 2, PURE_WHITE)
            c.circle(66, 4, 5, WHITE_SHADOW)
            c.circle(66, 4, 3, PURE_WHITE)
            # Sharp red tick
            c.line(40, 12, 46, 18, RED_MID)
            c.line(46, 12, 40, 18, RED_MID)

        frames.append(c)

    return frames


def generate_parent_point() -> List[PixelCanvas]:
    """128x192, 8 frames, 12 fps, loop: false.
    Giant accusatory pointing finger wagging angrily up and down!
    """
    frames = []
    # Rhythmic aggressive wagging angles
    wag_y = [0, -8, -14, -6, 4, 12, 6, 0]

    for f in range(8):
        c = PixelCanvas(128, 192, TRANSPARENT)
        wy = wag_y[f]
        fy = 100 + wy

        # Imposing bathrobe torso on right
        c.polygon([(70, 60), (120, 60), (128, 191), (60, 191)], SHADOW_DEEP, outline=OUTLINE)
        # Bathrobe sash
        c.rect(68, 116, 56, 8, SHADOW_MID, outline=OUTLINE)

        # Head leaning forward angrily
        c.circle(88, 44, 18, SHADOW_DEEP, outline=OUTLINE)
        # Curlers
        for cx, cy in [(76, 28), (88, 24), (100, 28), (106, 38)]:
            c.rect(cx - 4, cy - 4, 8, 6, PURPLE_LIGHT, outline=OUTLINE)
            c.rect(cx - 2, cy - 2, 4, 3, DUSK_PINK)

        # Blazing red eye glaring forward
        c.circle(74, 44, 4, RED_LIGHT, outline=OUTLINE)
        c.set_pixel(74, 44, RED_MID)
        c.line(70, 41, 78, 41, OUTLINE)  # deep furrowed brow
        # Laser streak
        c.line(56, 44, 70, 44, RED_LIGHT)

        # Huge sleeve extending forward
        c.polygon([(80, 88), (106, 96), (88, 128), (68, 114)], SHADOW_DEEP, outline=OUTLINE)
        c.line(70, 94, 66, 118, PURPLE_LIGHT)  # cuff rim

        # Forearm thrusting dramatically left
        c.rect(48, fy - 6, 24, 18, SHADOW_DEEP, outline=OUTLINE)

        # Fist with clenched knuckles
        c.rect(34, fy - 4, 16, 20, SHADOW_DEEP, outline=OUTLINE)
        for ky in [fy + 2, fy + 7, fy + 12]:
            c.line(34, ky, 48, ky, OUTLINE)
            c.set_pixel(36, ky - 1, PURPLE_LIGHT)

        # GIANT POINTING FINGER (30px long)
        c.polygon([
            (6, fy - 6), (36, fy - 6), (36, fy + 8), (6, fy + 6)
        ], SHADOW_DEEP, outline=OUTLINE)
        c.line(8, fy - 5, 34, fy - 5, PURPLE_LIGHT)
        c.line(8, fy - 3, 34, fy - 3, SKIN_MID)
        c.circle(6, fy + 1, 5, SHADOW_DEEP, outline=OUTLINE)
        c.rect(8, fy - 3, 5, 4, WHITE_SHADOW)  # fingernail

        # Motion speedlines around the wagging finger!
        if abs(wy) > 4:
            c.line(2, fy - 12, 14, fy - 12, WHITE_SHADOW)
            c.line(4, fy + 16, 18, fy + 16, WHITE_SHADOW)

        # Steam venting from head
        steam_x = 76 + (f % 3) * 6
        c.circle(steam_x, 14, 4 + (f % 3), WHITE_SHADOW)
        c.circle(steam_x, 14, 2, PURE_WHITE)

        frames.append(c)

    return frames


def generate_parent_sigh() -> List[PixelCanvas]:
    """128x192, 8 frames, 8 fps, loop: false.
    Exasperated face-palm: lowers finger, raises hand to face, shoulders slump, heavy sigh cloud.
    """
    frames = []
    hand_stages = [
        (30, 110), (42, 90), (54, 70), (62, 54),
        (64, 48), (64, 48), (64, 48), (64, 48)
    ]
    shoulder_slump = [0, 1, 2, 4, 6, 7, 7, 6]

    for f in range(8):
        c = PixelCanvas(128, 192, TRANSPARENT)
        hx, hy = hand_stages[f]
        slump = shoulder_slump[f]

        # Slumped torso silhouette
        c.polygon([
            (66, 68 + slump), (116, 68 + slump), (124, 191), (58, 191)
        ], SHADOW_DEEP, outline=OUTLINE)
        c.rect(64, 120 + slump, 56, 8, SHADOW_MID, outline=OUTLINE)

        # Bowed head
        head_y = 48 + slump
        c.circle(82, head_y, 18, SHADOW_DEEP, outline=OUTLINE)

        # Curlers drooping slightly
        for cx, cy in [(70, head_y - 14), (82, head_y - 18), (94, head_y - 14), (100, head_y - 4)]:
            c.rect(cx - 4, cy - 4, 8, 6, PURPLE_LIGHT, outline=OUTLINE)
            c.rect(cx - 2, cy - 2, 4, 3, DUSK_PINK)

        # Resigned closed eye
        c.line(72, head_y, 78, head_y, OUTLINE)
        c.line(72, head_y - 2, 78, head_y - 4, OUTLINE)  # furrowed tired brow

        # Arm reaching up to face-palm
        c.polygon([(84, 96 + slump), (96, 100 + slump), (hx + 8, hy + 10), (hx, hy + 8)], SHADOW_DEEP, outline=OUTLINE)
        # Hand / palm on forehead
        c.circle(hx, hy, 10, SHADOW_DEEP, outline=OUTLINE)
        # Fingers covering eyes/forehead
        for i in range(4):
            c.rect(hx - 2 + i * 3, hy - 8, 3, 10, SKIN_MID, outline=OUTLINE)

        # Big drooping sigh cloud in later frames
        if f >= 4:
            cloud_f = f - 4
            cloud_x = 44 - cloud_f * 4
            cloud_y = 70 + cloud_f * 5
            c.circle(cloud_x, cloud_y, 8 + cloud_f * 2, WHITE_SHADOW)
            c.circle(cloud_x + 4, cloud_y - 2, 6, PURE_WHITE)
            c.circle(cloud_x - 6, cloud_y + 3, 5, WHITE_SHADOW)
            # Little sigh trailing trail toward mouth
            c.circle(cloud_x + 16, cloud_y - 8, 3, WHITE_SHADOW)
            c.circle(cloud_x + 22, cloud_y - 12, 2, WHITE_SHADOW)

        frames.append(c)

    return frames


def generate_parent_speech_yell() -> PixelCanvas:
    """192x96 comic speech bubble with jagged explosive shout spikes and empty center."""
    c = PixelCanvas(192, 96, TRANSPARENT)

    # Outer jagged starburst shout bubble
    # Define contour with sharp teeth
    num_teeth = 28
    cx, cy = 96, 42
    rx, ry = 86, 34

    coords_outer = []
    coords_inner = []

    for i in range(num_teeth):
        angle = (i / num_teeth) * 2 * math.pi
        is_spike = (i % 2 == 1)
        r_mult = 1.15 if is_spike else 0.88
        ox = cx + math.cos(angle) * (rx * r_mult)
        oy = cy + math.sin(angle) * (ry * r_mult)
        coords_outer.append((ox, oy))

        # Inner fill boundary
        ix = cx + math.cos(angle) * (rx * r_mult - 4)
        iy = cy + math.sin(angle) * (ry * r_mult - 4)
        coords_inner.append((ix, iy))

    # Jagged shout tail pointing down-right toward parent (x=140..170, y=70..95)
    outer_poly = [(int(x), int(y)) for x, y in coords_outer]
    # Add tail vertices to polygon
    outer_poly.extend([(136, 70), (160, 94), (150, 68)])

    # Draw solid outline
    c.polygon(outer_poly, PURE_WHITE, outline=OUTLINE)

    # Inner hollow fill (leaving empty center for text)
    # The polygon fill already fills with PURE_WHITE. Let's ensure a crisp 2px border:
    c.apply_selective_outline(OUTLINE)

    return c


def generate_parent_speech_sigh() -> PixelCanvas:
    """192x96 speech bubble with smooth pillowy cloud contours and smooth curved sigh tail."""
    c = PixelCanvas(192, 96, TRANSPARENT)

    # Smooth cloud bubble lobes
    lobes = [
        (40, 36, 26), (72, 28, 28), (112, 26, 28), (150, 34, 26),
        (156, 52, 24), (130, 64, 26), (88, 66, 28), (44, 58, 26),
        (96, 46, 34)  # center fill
    ]

    for lx, ly, lr in lobes:
        c.circle(lx, ly, lr, PURE_WHITE, outline=OUTLINE)

    # Smooth drooping sigh tail pointing down-right
    # Series of trailing cloud puffs tapering toward parent
    tail_puffs = [
        (148, 72, 10),
        (160, 80, 7),
        (170, 86, 5),
        (178, 90, 3)
    ]
    for tx, ty, tr in tail_puffs:
        c.circle(tx, ty, tr, PURE_WHITE, outline=OUTLINE)

    # Hollow center fill
    for lx, ly, lr in lobes:
        c.circle(lx, ly, lr - 2, PURE_WHITE)
    for tx, ty, tr in tail_puffs:
        c.circle(tx, ty, tr - 1, PURE_WHITE)

    return c


# ==============================================================================
# MAIN GENERATION RUNNER
# ==============================================================================

def generate_all_cat_and_parent():
    print("--- Generating Cat Animations (art/v2/) ---")
    assemble_strip(generate_cat_sleep(), "art/v2/cat_sleep.png")
    assemble_strip(generate_cat_wake(), "art/v2/cat_wake.png")
    assemble_strip(generate_cat_watch(), "art/v2/cat_watch.png")
    assemble_strip(generate_cat_startle(), "art/v2/cat_startle.png")
    assemble_strip(generate_cat_lick(), "art/v2/cat_lick.png")
    assemble_strip(generate_cat_yawn(), "art/v2/cat_yawn.png")
    assemble_strip(generate_cat_zoomies(), "art/v2/cat_zoomies.png")

    print("\n--- Generating Parent Sheets (art/v2/) ---")
    assemble_strip(generate_parent_peek_v2(), "art/v2/parent_peek.png")
    assemble_strip(generate_parent_point(), "art/v2/parent_point.png")
    assemble_strip(generate_parent_sigh(), "art/v2/parent_sigh.png")

    bubble_yell = generate_parent_speech_yell()
    bubble_yell.to_image().save("art/v2/parent_speech_yell.png", "PNG")
    print("Saved art/v2/parent_speech_yell.png (192x96)")

    bubble_sigh = generate_parent_speech_sigh()
    bubble_sigh.to_image().save("art/v2/parent_speech_sigh.png", "PNG")
    print("Saved art/v2/parent_speech_sigh.png (192x96)")


if __name__ == "__main__":
    generate_all_cat_and_parent()
