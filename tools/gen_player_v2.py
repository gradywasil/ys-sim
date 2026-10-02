"""Younger Sibling Simulator - Player 1 Sprite Generator v2 (64x64 Native Resolution).

Elevated, charming, highly detailed 64x64 pixel art for Player 1:
- Proportions: 64x64 canvas, body ~40px tall, ~20px wide, centered at x=31..32
- CRUCIAL ANCHOR: Row y=63 touches lowest foot/sole pixel in EVERY frame!
- Palette: 64-color palette strictly from tools/palette.py, selective outline OUTLINE (#120d1f)
- Lighting: Upper-left light source, 1px lighter rim on top-left, 1px darker on bottom-right
- Readable face: Animated eyebrows, changing mouth shapes (grin, shout, grimace, 'o', smirk),
  large expressive eyes with specular catchlights and directional pupils
- Form-fitting hoodie with drawstrings, kangaroo pocket, cuffs, shifting dynamic fabric folds
- Denim shorts with pocket seams, fly, and rolled cuff hems
- Chunky skate sneakers with laces, soles, toe cap, and rubber foxing sidewalls
- Messy brown hair with signature springy cowlick showing lag and follow-through
- Sub-pixel motion: squash, stretch, anticipation, and recovery baked in
"""

import math
import json
import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional

# Ensure tools directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from canvas import PixelCanvas, assemble_strip, generate_normal_map
from palette import (
    TRANSPARENT, OUTLINE, VOID_BLACK,
    SHADOW_PURPLE_DARK, SHADOW_PURPLE_DEEP, SHADOW_PURPLE_MID, PURPLE_DARK, PURPLE_MID, PURPLE_RICH, PURPLE_LIGHT,
    DUSK_LILAC, DUSK_PINK, DUSK_ROSE, DUSK_PEACH, DUSK_BLUSH, DUSK_CREAM,
    SKIN_DEEP, SKIN_SHADOW, SKIN_MID, SKIN_LIGHT, SKIN_HIGHLIGHT,
    WOOD_BLACK, BROWN_DARKEST, BROWN_DARK, BROWN_MID, BROWN_LIGHT, WOOD_HIGHLIGHT, WOOD_LIT,
    RED_DEEP, RED_SHADOW, RED_RICH, RED_MID, RED_LIGHT, RED_HIGHLIGHT,
    BLUE_DEEP, BLUE_SHADOW, BLUE_RICH, BLUE_MID, BLUE_LIGHT, BLUE_HIGHLIGHT,
    YELLOW_DEEP, YELLOW_SHADOW, YELLOW_RICH, YELLOW_MID, YELLOW_LIGHT, YELLOW_HIGHLIGHT,
    GREEN_DEEP, GREEN_SHADOW, GREEN_RICH, GREEN_MID, GREEN_LIGHT, GREEN_HIGHLIGHT,
    ORANGE_DEEP, ORANGE_SHADOW, ORANGE_MID, ORANGE_LIGHT,
    TEAL_SHADOW, TEAL_MID, TEAL_LIGHT, TEAL_HIGHLIGHT,
    METAL_SHADOW, METAL_MID, WHITE_SHADOW, WHITE_MID, PURE_WHITE,
    VALID_PALETTE_RGBA
)

RGBA = Tuple[int, int, int, int]

def create_base_canvas() -> PixelCanvas:
    return PixelCanvas(64, 64, TRANSPARENT)


# =============================================================================
# MODULAR 64x64 CHARACTER DRAWING PRIMITIVES
# =============================================================================

def draw_sneaker_v2(canvas: PixelCanvas, foot_x: int, foot_y: int = 63,
                    facing_right: bool = True, pose: str = "flat",
                    speed_boot: bool = False, wing_fx: bool = False,
                    is_far: bool = False):
    """
    Draws a chunky skate sneaker at 64x64 scale.
    Features: thick vulcanized rubber foxing sidewall, rubber toe cap bumper,
    white laces with eyelets, padded collar, heel counter, and dark tread.
    CRUCIAL: Touches foot_y (row 63) in every pose!
    """
    body_color = ORANGE_MID if speed_boot else (RED_SHADOW if is_far else RED_MID)
    body_shadow = ORANGE_SHADOW if speed_boot else (RED_DEEP if is_far else RED_SHADOW)
    body_light = YELLOW_MID if speed_boot else (RED_MID if is_far else RED_LIGHT)
    rim_light = ORANGE_LIGHT if speed_boot else (RED_LIGHT if is_far else RED_HIGHLIGHT)

    if pose == "flat":
        # Planted flat on ground. Soles span row foot_y-1 (62) to foot_y (63).
        # Length ~ 14px: from foot_x - 6 to foot_x + 7.
        
        # 1. Dark bottom tread (touches row 63!)
        for x in range(foot_x - 6, foot_x + 7):
            if x == foot_x - 6 or x == foot_x + 6:
                canvas.set_pixel(x, foot_y, OUTLINE)
            elif x in [foot_x - 5, foot_x - 4, foot_x + 4, foot_x + 5]:
                canvas.set_pixel(x, foot_y, SHADOW_PURPLE_DARK)
            else:
                canvas.set_pixel(x, foot_y, WHITE_SHADOW)

        # 2. Vulcanized rubber sidewall / foxing tape (row foot_y - 1 = 62)
        canvas.set_pixel(foot_x - 6, foot_y - 1, OUTLINE)
        for x in range(foot_x - 5, foot_x + 7):
            if x <= foot_x - 3:
                canvas.set_pixel(x, foot_y - 1, WHITE_SHADOW)
            elif x >= foot_x + 4:
                canvas.set_pixel(x, foot_y - 1, PURE_WHITE)
            else:
                canvas.set_pixel(x, foot_y - 1, WHITE_MID)
        canvas.set_pixel(foot_x + 7, foot_y - 1, OUTLINE)

        # 3. White rubber toe cap bumper (rows 59..61, front)
        for x in range(foot_x + 3, foot_x + 7):
            canvas.set_pixel(x, foot_y - 2, PURE_WHITE)
        canvas.set_pixel(foot_x + 7, foot_y - 2, WHITE_MID)
        for x in range(foot_x + 4, foot_x + 7):
            canvas.set_pixel(x, foot_y - 3, PURE_WHITE)
        canvas.set_pixel(foot_x + 5, foot_y - 4, WHITE_MID)

        # 4. Shoe Upper body (canvas / suede) & heel counter
        # Heel counter (back)
        for y in range(foot_y - 5, foot_y - 1):
            canvas.set_pixel(foot_x - 6, y, OUTLINE if y == foot_y - 5 else body_shadow)
            canvas.set_pixel(foot_x - 5, y, body_shadow)
            canvas.set_pixel(foot_x - 4, y, body_color)

        # Midfoot upper & collar
        for y in range(foot_y - 4, foot_y - 1):
            canvas.set_pixel(foot_x - 3, y, body_color)
            canvas.set_pixel(foot_x - 2, y, body_light if y == foot_y - 4 else body_color)
            canvas.set_pixel(foot_x + 2, y, body_color)
            canvas.set_pixel(foot_x + 3, y, body_shadow if y == foot_y - 2 else body_color)

        # 5. Padded tongue & white laces
        # Tongue
        canvas.set_pixel(foot_x - 1, foot_y - 5, PURE_WHITE)
        canvas.set_pixel(foot_x, foot_y - 5, PURE_WHITE)
        canvas.set_pixel(foot_x + 1, foot_y - 5, WHITE_SHADOW)
        # Laces (criss-cross)
        canvas.set_pixel(foot_x - 2, foot_y - 4, PURE_WHITE)
        canvas.set_pixel(foot_x, foot_y - 4, PURE_WHITE)
        canvas.set_pixel(foot_x + 1, foot_y - 4, PURE_WHITE)
        canvas.set_pixel(foot_x - 1, foot_y - 3, PURE_WHITE)
        canvas.set_pixel(foot_x + 1, foot_y - 3, PURE_WHITE)
        canvas.set_pixel(foot_x, foot_y - 2, PURE_WHITE)
        canvas.set_pixel(foot_x + 2, foot_y - 3, WHITE_SHADOW)

        # 6. Ankle sock cuff peek (rows foot_y - 7, foot_y - 6)
        canvas.set_pixel(foot_x - 4, foot_y - 6, PURE_WHITE)
        canvas.set_pixel(foot_x - 3, foot_y - 6, PURE_WHITE)
        canvas.set_pixel(foot_x - 2, foot_y - 6, BLUE_MID if is_far else RED_LIGHT)
        canvas.set_pixel(foot_x - 1, foot_y - 6, PURE_WHITE)
        canvas.set_pixel(foot_x, foot_y - 6, PURE_WHITE)

    elif pose == "heel_strike":
        # Heel contacts ground at foot_y (row 63). Shoe angled up ~25 deg forward.
        # Heel tread touches row 63!
        canvas.set_pixel(foot_x - 5, foot_y, OUTLINE)
        canvas.set_pixel(foot_x - 4, foot_y, SHADOW_PURPLE_DARK)
        canvas.set_pixel(foot_x - 3, foot_y, WHITE_SHADOW)

        # Angled sole & foxing
        canvas.set_pixel(foot_x - 6, foot_y - 1, OUTLINE)
        canvas.set_pixel(foot_x - 5, foot_y - 1, WHITE_SHADOW)
        canvas.set_pixel(foot_x - 4, foot_y - 1, WHITE_MID)
        canvas.set_pixel(foot_x - 3, foot_y - 1, PURE_WHITE)
        canvas.set_pixel(foot_x - 2, foot_y - 1, OUTLINE)

        canvas.set_pixel(foot_x - 2, foot_y - 2, WHITE_SHADOW)
        canvas.set_pixel(foot_x - 1, foot_y - 2, WHITE_MID)
        canvas.set_pixel(foot_x, foot_y - 2, PURE_WHITE)

        canvas.set_pixel(foot_x + 1, foot_y - 3, WHITE_MID)
        canvas.set_pixel(foot_x + 2, foot_y - 3, PURE_WHITE)
        canvas.set_pixel(foot_x + 3, foot_y - 3, PURE_WHITE)

        # Toe cap raised up
        for x in range(foot_x + 4, foot_x + 8):
            canvas.set_pixel(x, foot_y - 4, PURE_WHITE)
        for x in range(foot_x + 4, foot_x + 7):
            canvas.set_pixel(x, foot_y - 5, PURE_WHITE)
        canvas.set_pixel(foot_x + 7, foot_y - 4, WHITE_SHADOW)

        # Upper & heel counter
        for y in range(foot_y - 6, foot_y - 1):
            canvas.set_pixel(foot_x - 5, y, body_shadow)
            canvas.set_pixel(foot_x - 4, y, body_color)
        for y in range(foot_y - 6, foot_y - 2):
            canvas.set_pixel(foot_x - 3, y, body_light if y <= foot_y - 5 else body_color)
            canvas.set_pixel(foot_x - 2, y, body_color)
        for y in range(foot_y - 5, foot_y - 3):
            canvas.set_pixel(foot_x - 1, y, body_color)
            canvas.set_pixel(foot_x, y, body_color)
            canvas.set_pixel(foot_x + 1, y, body_color)

        # Laces on angle
        canvas.set_pixel(foot_x, foot_y - 5, PURE_WHITE)
        canvas.set_pixel(foot_x + 1, foot_y - 5, PURE_WHITE)
        canvas.set_pixel(foot_x + 2, foot_y - 4, PURE_WHITE)
        canvas.set_pixel(foot_x + 3, foot_y - 4, PURE_WHITE)

        # Sock
        canvas.set_pixel(foot_x - 4, foot_y - 7, PURE_WHITE)
        canvas.set_pixel(foot_x - 3, foot_y - 7, PURE_WHITE)
        canvas.set_pixel(foot_x - 2, foot_y - 7, PURE_WHITE)

    elif pose == "toe_push":
        # Toe pushes off ground at foot_y (row 63). Heel kicked up ~30 deg back.
        # Front toe bumper & tread touches row 63!
        canvas.set_pixel(foot_x + 4, foot_y, OUTLINE)
        canvas.set_pixel(foot_x + 5, foot_y, SHADOW_PURPLE_DARK)
        canvas.set_pixel(foot_x + 6, foot_y, OUTLINE)

        # Toe cap & lower foxing at row 62
        canvas.set_pixel(foot_x + 3, foot_y - 1, WHITE_SHADOW)
        canvas.set_pixel(foot_x + 4, foot_y - 1, PURE_WHITE)
        canvas.set_pixel(foot_x + 5, foot_y - 1, PURE_WHITE)
        canvas.set_pixel(foot_x + 6, foot_y - 1, WHITE_SHADOW)

        # Angled sole reaching up toward heel
        canvas.set_pixel(foot_x + 1, foot_y - 2, WHITE_SHADOW)
        canvas.set_pixel(foot_x + 2, foot_y - 2, WHITE_MID)
        canvas.set_pixel(foot_x + 3, foot_y - 2, PURE_WHITE)

        canvas.set_pixel(foot_x - 1, foot_y - 3, WHITE_SHADOW)
        canvas.set_pixel(foot_x, foot_y - 3, WHITE_MID)
        canvas.set_pixel(foot_x + 1, foot_y - 3, PURE_WHITE)

        canvas.set_pixel(foot_x - 3, foot_y - 4, OUTLINE)
        canvas.set_pixel(foot_x - 2, foot_y - 4, WHITE_SHADOW)
        canvas.set_pixel(foot_x - 1, foot_y - 4, WHITE_MID)

        # Upper angled
        for x in range(foot_x + 1, foot_x + 6):
            canvas.set_pixel(x, foot_y - 2, PURE_WHITE if x >= foot_x + 4 else body_color)
            canvas.set_pixel(x, foot_y - 3, PURE_WHITE if x >= foot_x + 4 else body_light)
        for x in range(foot_x - 2, foot_x + 3):
            canvas.set_pixel(x, foot_y - 4, body_color)
            canvas.set_pixel(x, foot_y - 5, body_color)
        canvas.set_pixel(foot_x - 3, foot_y - 5, body_shadow)
        canvas.set_pixel(foot_x - 3, foot_y - 6, body_shadow)

        # Laces
        canvas.set_pixel(foot_x + 1, foot_y - 4, PURE_WHITE)
        canvas.set_pixel(foot_x + 2, foot_y - 4, PURE_WHITE)
        canvas.set_pixel(foot_x, foot_y - 5, PURE_WHITE)
        canvas.set_pixel(foot_x + 1, foot_y - 5, PURE_WHITE)

        # Sock
        canvas.set_pixel(foot_x - 2, foot_y - 7, PURE_WHITE)
        canvas.set_pixel(foot_x - 1, foot_y - 7, PURE_WHITE)
        canvas.set_pixel(foot_x, foot_y - 7, PURE_WHITE)

    elif pose == "toe_point":
        # Pointed straight/steeply down in mid-air or launch.
        # Tip of toe cap / rubber bumper touches row 63!
        canvas.set_pixel(foot_x + 1, foot_y, OUTLINE)
        canvas.set_pixel(foot_x + 2, foot_y, SHADOW_PURPLE_DARK)
        canvas.set_pixel(foot_x + 3, foot_y, OUTLINE)

        # Toe cap at row 62
        canvas.set_pixel(foot_x, foot_y - 1, WHITE_SHADOW)
        canvas.set_pixel(foot_x + 1, foot_y - 1, PURE_WHITE)
        canvas.set_pixel(foot_x + 2, foot_y - 1, PURE_WHITE)
        canvas.set_pixel(foot_x + 3, foot_y - 1, WHITE_SHADOW)

        # Upper ascending
        for y in range(foot_y - 6, foot_y - 1):
            canvas.set_pixel(foot_x - 1, y, body_shadow)
            canvas.set_pixel(foot_x, y, body_color)
            canvas.set_pixel(foot_x + 1, y, body_light if y <= foot_y - 4 else body_color)
            canvas.set_pixel(foot_x + 2, y, body_color)
        canvas.set_pixel(foot_x - 2, foot_y - 6, body_shadow)
        canvas.set_pixel(foot_x - 2, foot_y - 5, body_shadow)

        # Laces
        canvas.set_pixel(foot_x + 1, foot_y - 3, PURE_WHITE)
        canvas.set_pixel(foot_x + 1, foot_y - 4, PURE_WHITE)
        canvas.set_pixel(foot_x + 2, foot_y - 3, PURE_WHITE)

        # Sock
        canvas.set_pixel(foot_x - 1, foot_y - 7, PURE_WHITE)
        canvas.set_pixel(foot_x, foot_y - 7, PURE_WHITE)
        canvas.set_pixel(foot_x + 1, foot_y - 7, PURE_WHITE)

    elif pose == "squash":
        # Impact landing squash! Wider flat sole along rows 62 and 63.
        # Length ~ 16px: from foot_x - 7 to foot_x + 8. Touches row 63!
        for x in range(foot_x - 7, foot_x + 9):
            if x == foot_x - 7 or x == foot_x + 8:
                canvas.set_pixel(x, foot_y, OUTLINE)
            elif x in [foot_x - 6, foot_x + 7]:
                canvas.set_pixel(x, foot_y, SHADOW_PURPLE_DARK)
            else:
                canvas.set_pixel(x, foot_y, WHITE_SHADOW)

        # Sidewall at row 62
        for x in range(foot_x - 7, foot_x + 9):
            if x <= foot_x - 5:
                canvas.set_pixel(x, foot_y - 1, WHITE_SHADOW)
            elif x >= foot_x + 5:
                canvas.set_pixel(x, foot_y - 1, PURE_WHITE)
            else:
                canvas.set_pixel(x, foot_y - 1, WHITE_MID)

        # Compressed upper (rows 59..61)
        for y in range(foot_y - 4, foot_y - 1):
            for x in range(foot_x - 6, foot_x + 8):
                if x >= foot_x + 4:
                    canvas.set_pixel(x, y, PURE_WHITE if y >= foot_y - 3 else WHITE_MID)
                elif x <= foot_x - 4:
                    canvas.set_pixel(x, y, body_shadow)
                else:
                    canvas.set_pixel(x, y, body_color)

        # Laces
        canvas.set_pixel(foot_x - 1, foot_y - 3, PURE_WHITE)
        canvas.set_pixel(foot_x, foot_y - 3, PURE_WHITE)
        canvas.set_pixel(foot_x + 1, foot_y - 3, PURE_WHITE)

        # Sock
        canvas.set_pixel(foot_x - 3, foot_y - 5, PURE_WHITE)
        canvas.set_pixel(foot_x - 2, foot_y - 5, PURE_WHITE)
        canvas.set_pixel(foot_x - 1, foot_y - 5, PURE_WHITE)

    elif pose == "trip_flat":
        # Sneaker sprawled horizontally flat along rows 62 and 63.
        for x in range(foot_x - 8, foot_x + 8):
            canvas.set_pixel(x, foot_y, OUTLINE if (x in [foot_x - 8, foot_x + 7]) else SHADOW_PURPLE_DARK)
            canvas.set_pixel(x, foot_y - 1, WHITE_SHADOW if x <= foot_x else PURE_WHITE)
        for x in range(foot_x - 6, foot_x + 6):
            canvas.set_pixel(x, foot_y - 2, body_shadow if x <= foot_x - 2 else body_color)
            canvas.set_pixel(x, foot_y - 3, body_color if x <= foot_x + 2 else PURE_WHITE)

    # ---------------- Accents: Speed Boot Wings / Blue Aura ----------------
    if speed_boot:
        # Golden-yellow lightning wings behind heel
        wing_base_x = foot_x - 6
        wing_base_y = foot_y - 4
        canvas.set_pixel(wing_base_x - 1, wing_base_y - 1, YELLOW_MID)
        canvas.set_pixel(wing_base_x - 2, wing_base_y - 2, YELLOW_LIGHT)
        canvas.set_pixel(wing_base_x - 3, wing_base_y - 3, PURE_WHITE)
        canvas.set_pixel(wing_base_x - 1, wing_base_y - 2, YELLOW_LIGHT)
        canvas.set_pixel(wing_base_x - 2, wing_base_y - 1, YELLOW_SHADOW)
        canvas.set_pixel(wing_base_x - 3, wing_base_y - 2, YELLOW_MID)
        canvas.set_pixel(wing_base_x - 4, wing_base_y - 3, YELLOW_LIGHT)
        canvas.set_pixel(wing_base_x - 5, wing_base_y - 4, PURE_WHITE)

    if wing_fx:
        # Glowing cyan/blue feather wings
        wing_base_x = foot_x - 6
        wing_base_y = foot_y - 4
        canvas.set_pixel(wing_base_x - 1, wing_base_y - 1, BLUE_LIGHT)
        canvas.set_pixel(wing_base_x - 2, wing_base_y - 2, PURE_WHITE)
        canvas.set_pixel(wing_base_x - 3, wing_base_y - 3, TEAL_LIGHT)
        canvas.set_pixel(wing_base_x - 1, wing_base_y - 2, BLUE_MID)
        canvas.set_pixel(wing_base_x - 2, wing_base_y - 3, BLUE_LIGHT)
        canvas.set_pixel(wing_base_x - 3, wing_base_y - 4, PURE_WHITE)


def draw_leg_v2(canvas: PixelCanvas, hip_x: int, hip_y: int,
                foot_x: int, foot_y: int, is_far: bool = False):
    """
    Draws bare kid leg connecting shorts leg hem down to sneaker collar.
    4-5px wide column with calf curve and rim lighting.
    """
    skin_c = SKIN_SHADOW if is_far else SKIN_MID
    skin_l = SKIN_MID if is_far else SKIN_LIGHT
    skin_hl = SKIN_LIGHT if is_far else SKIN_HIGHLIGHT
    skin_d = SKIN_DEEP if is_far else SKIN_SHADOW

    steps = max(abs(foot_y - hip_y), 1)
    for s in range(steps + 1):
        t = s / steps
        cx = int(round(hip_x + t * (foot_x - hip_x)))
        cy = int(round(hip_y + t * (foot_y - hip_y)))
        if cy >= 62: # don't overwrite sole
            continue
        # 4px column width
        canvas.set_pixel(cx - 2, cy, OUTLINE)
        canvas.set_pixel(cx - 1, cy, skin_hl if not is_far else skin_l)
        canvas.set_pixel(cx, cy, skin_l)
        canvas.set_pixel(cx + 1, cy, skin_c)
        canvas.set_pixel(cx + 2, cy, skin_d)


def draw_shorts_v2(canvas: PixelCanvas, sx: int, sy: int, w: int = 18, h: int = 9,
                   tilt: int = 0):
    """
    Draws denim blue shorts with waistband, belt loops, gold pocket seams,
    vertical fly, and rolled cuff hems.
    """
    x0 = sx - w // 2
    x1 = x0 + w

    # 1. Waistband (rows sy, sy + 1)
    for x in range(x0, x1):
        rel_x = x - x0
        if rel_x <= 3:
            canvas.set_pixel(x, sy, BLUE_LIGHT)
            canvas.set_pixel(x, sy + 1, BLUE_MID)
        elif rel_x >= w - 4:
            canvas.set_pixel(x, sy, BLUE_MID)
            canvas.set_pixel(x, sy + 1, BLUE_SHADOW)
        else:
            canvas.set_pixel(x, sy, BLUE_LIGHT)
            canvas.set_pixel(x, sy + 1, BLUE_MID)

    # Brass button & belt loops
    canvas.set_pixel(sx, sy + 1, YELLOW_LIGHT)
    canvas.set_pixel(sx - 5, sy, BLUE_HIGHLIGHT)
    canvas.set_pixel(sx - 5, sy + 1, BLUE_SHADOW)
    canvas.set_pixel(sx + 5, sy, BLUE_HIGHLIGHT)
    canvas.set_pixel(sx + 5, sy + 1, BLUE_SHADOW)

    # 2. Main Shorts Body (rows sy + 2 .. sy + h - 3)
    for y in range(sy + 2, sy + h - 2):
        for x in range(x0, x1):
            rel_x = x - x0
            if rel_x <= 2:
                canvas.set_pixel(x, y, BLUE_LIGHT)
            elif rel_x >= w - 3:
                canvas.set_pixel(x, y, BLUE_SHADOW)
            elif rel_x >= w - 1:
                canvas.set_pixel(x, y, BLUE_DEEP)
            else:
                canvas.set_pixel(x, y, BLUE_MID)

    # Golden contrast pocket seam (curved)
    canvas.set_pixel(sx + 4, sy + 2, YELLOW_LIGHT)
    canvas.set_pixel(sx + 5, sy + 3, YELLOW_MID)
    canvas.set_pixel(sx + 6, sy + 4, YELLOW_MID)
    canvas.set_pixel(sx + 6, sy + 3, BLUE_DEEP) # pocket slit shadow

    # Left pocket hint
    canvas.set_pixel(sx - 5, sy + 2, YELLOW_MID)
    canvas.set_pixel(sx - 6, sy + 3, BLUE_DEEP)

    # Vertical fly seam down center
    for y in range(sy + 2, sy + 6):
        canvas.set_pixel(sx, y, BLUE_LIGHT)
        canvas.set_pixel(sx + 1, y, BLUE_DEEP)

    # Diagonal fabric stress creases
    canvas.set_pixel(sx - 2, sy + 4, BLUE_SHADOW)
    canvas.set_pixel(sx - 3, sy + 5, BLUE_SHADOW)
    canvas.set_pixel(sx + 3, sy + 5, BLUE_SHADOW)

    # 3. Rolled cuff leg hems (rows sy + h - 2 .. sy + h)
    # Left leg opening
    for x in range(x0 + 1, sx):
        canvas.set_pixel(x, sy + h - 2, BLUE_LIGHT)
        canvas.set_pixel(x, sy + h - 1, BLUE_MID)
        canvas.set_pixel(x, sy + h, OUTLINE)

    # Right leg opening
    for x in range(sx + 2, x1 - 1):
        canvas.set_pixel(x, sy + h - 2, BLUE_MID)
        canvas.set_pixel(x, sy + h - 1, BLUE_SHADOW)
        canvas.set_pixel(x, sy + h, OUTLINE)

    # Crotch / inseam notch separation
    canvas.set_pixel(sx, sy + h - 2, BLUE_DEEP)
    canvas.set_pixel(sx + 1, sy + h - 2, BLUE_DEEP)
    canvas.set_pixel(sx, sy + h - 1, OUTLINE)
    canvas.set_pixel(sx + 1, sy + h - 1, OUTLINE)


def draw_hoodie_v2(canvas: PixelCanvas, tx: int, ty: int, w: int = 22, h: int = 15,
                   drawstring_wind: int = 0, hood_fold: bool = True, folds: int = 0):
    """
    Draws form-fitting red hoodie with kangaroo pocket, ribbed cuffs/waistband,
    bunched hood behind collar, shifting dynamic fabric folds, and white drawstrings.
    """
    x0 = tx - w // 2
    x1 = x0 + w

    # 1. Torso Volume
    for y in range(ty + 2, ty + h):
        for x in range(x0, x1):
            rel_x = x - x0
            if rel_x <= 3:
                canvas.set_pixel(x, y, RED_LIGHT)
            elif rel_x >= w - 4:
                canvas.set_pixel(x, y, RED_SHADOW)
            elif rel_x >= w - 2:
                canvas.set_pixel(x, y, RED_DEEP)
            else:
                canvas.set_pixel(x, y, RED_MID)

    # Sloping shoulders (rows ty, ty + 1)
    for x in range(x0 + 2, x1 - 2):
        rel_x = x - (x0 + 2)
        top_y = ty + (1 if (x <= x0 + 4 or x >= x1 - 5) else 0)
        canvas.set_pixel(x, top_y, RED_HIGHLIGHT if rel_x <= 5 else RED_LIGHT)
        canvas.set_pixel(x, top_y + 1, RED_LIGHT if rel_x <= 5 else RED_MID)

    # 2. Bunched Hood behind neck
    if hood_fold:
        # Bunched fabric folds around back of neck (left side)
        for y in range(ty - 3, ty + 3):
            canvas.set_pixel(x0 - 2, y, OUTLINE)
            canvas.set_pixel(x0 - 1, y, RED_HIGHLIGHT if y <= ty else RED_LIGHT)
            canvas.set_pixel(x0, y, RED_MID)
            canvas.set_pixel(x0 + 1, y, RED_SHADOW)
        canvas.set_pixel(x0 - 1, ty - 4, OUTLINE)
        canvas.set_pixel(x0, ty - 4, RED_HIGHLIGHT)
        canvas.set_pixel(x0 + 1, ty - 4, RED_LIGHT)

    # 3. Metallic zipper / neckline glint
    canvas.set_pixel(tx, ty + 1, PURE_WHITE)
    canvas.set_pixel(tx, ty + 2, METAL_MID)
    canvas.set_pixel(tx, ty + 3, RED_DEEP)

    # 4. Dynamic diagonal fabric folds
    if folds == 0:
        # Subtle relaxed creases
        canvas.set_pixel(tx - 4, ty + 4, RED_LIGHT)
        canvas.set_pixel(tx - 3, ty + 5, RED_SHADOW)
        canvas.set_pixel(tx + 4, ty + 5, RED_SHADOW)
        canvas.set_pixel(tx + 5, ty + 6, RED_DEEP)
    elif folds > 0:
        # Wind / motion stretch creases
        canvas.line(tx - 6, ty + 4, tx - 1, ty + 7, RED_LIGHT)
        canvas.line(tx - 5, ty + 5, tx, ty + 8, RED_SHADOW)
        canvas.line(tx + 2, ty + 4, tx + 7, ty + 7, RED_SHADOW)
    else:
        # Compressed / squash wrinkles
        canvas.line(tx - 5, ty + 5, tx + 5, ty + 5, RED_LIGHT)
        canvas.line(tx - 6, ty + 6, tx + 6, ty + 6, RED_SHADOW)

    # 5. Kangaroo Pocket (lower torso, rows ty + h - 7 .. ty + h - 2)
    pocket_top_y = ty + h - 7
    # Top pocket hem highlighted
    for px in range(tx - 7, tx + 8):
        canvas.set_pixel(px, pocket_top_y, RED_HIGHLIGHT if px <= tx else RED_LIGHT)
    # Side entry diagonal pocket slits (shadowed entry points)
    canvas.set_pixel(tx - 8, pocket_top_y + 1, RED_DEEP)
    canvas.set_pixel(tx - 7, pocket_top_y + 2, RED_DEEP)
    canvas.set_pixel(tx - 8, pocket_top_y + 3, OUTLINE)
    canvas.set_pixel(tx + 8, pocket_top_y + 1, RED_DEEP)
    canvas.set_pixel(tx + 7, pocket_top_y + 2, RED_DEEP)
    canvas.set_pixel(tx + 8, pocket_top_y + 3, OUTLINE)
    # Bottom seam of pocket
    for px in range(tx - 6, tx + 7):
        canvas.set_pixel(px, ty + h - 2, RED_SHADOW)

    # 6. Elastic Ribbed Waistband Hem (rows ty + h - 1 .. ty + h)
    for x in range(x0 + 1, x1 - 1):
        is_rib = (x % 2 == 0)
        canvas.set_pixel(x, ty + h - 1, RED_LIGHT if is_rib else RED_MID)
        canvas.set_pixel(x, ty + h, RED_SHADOW if is_rib else RED_DEEP)

    # 7. White Drawstrings with metal aglets
    # Left string
    lx = tx - 3
    for dy in range(2, 9):
        curve = int(round(drawstring_wind * (dy - 1) / 7.0))
        canvas.set_pixel(lx + curve, ty + dy, PURE_WHITE)
        canvas.set_pixel(lx + curve + 1, ty + dy, WHITE_SHADOW)
    # Left aglet
    laglet_x = lx + drawstring_wind
    canvas.set_pixel(laglet_x, ty + 9, METAL_MID)
    canvas.set_pixel(laglet_x, ty + 10, PURE_WHITE)

    # Right string
    rx = tx + 3
    for dy in range(2, 10):
        curve = int(round(drawstring_wind * (dy - 1) / 8.0))
        canvas.set_pixel(rx + curve, ty + dy, PURE_WHITE)
        canvas.set_pixel(rx + curve + 1, ty + dy, WHITE_SHADOW)
    # Right aglet
    raglet_x = rx + drawstring_wind
    canvas.set_pixel(raglet_x, ty + 10, METAL_MID)
    canvas.set_pixel(raglet_x, ty + 11, PURE_WHITE)


def draw_head_v2(canvas: PixelCanvas, hx: int, hy: int,
                 eye_state: str = "normal", look_dir: str = "forward",
                 mouth: str = "smirk", eyebrow: str = "normal",
                 hair_bob: int = 0, hair_wind: int = 0,
                 blush: bool = True, sweat: bool = False):
    """
    Draws expressive, highly readable P1 head centered around (hx, hy) ~ (32, 22).
    Features:
    - Messy multi-lock brown hair with springy cowlick showing momentum/secondary lag
    - Large expressive eyes with crisp pupils, white catchlights, direction tracking
    - Mobile animated eyebrows (normal, raised, worried, angry, furrowed)
    - Animated mouth shapes (smirk, grin, open shout, 'o', grimace/gritted, pout, yawn)
    - Chubby kid cheeks with soft peach blush, button nose, kid ear
    """
    # ---------------- 1. Hair Volume (Top Crown & Back) ----------------
    hb = hair_bob
    # Top crown mass
    for y in range(hy - 8 + hb, hy - 3 + hb):
        for x in range(hx - 9, hx + 8):
            dist_sq = ((x - (hx - 1)) * 1.0) ** 2 + ((y - (hy - 3 + hb)) * 1.8) ** 2
            if dist_sq <= 50:
                if y <= hy - 6 + hb and x <= hx:
                    canvas.set_pixel(x, y, WOOD_LIT if x <= hx - 3 else WOOD_HIGHLIGHT)
                elif x <= hx - 4:
                    canvas.set_pixel(x, y, BROWN_LIGHT)
                elif x >= hx + 4:
                    canvas.set_pixel(x, y, BROWN_DARK)
                else:
                    canvas.set_pixel(x, y, BROWN_MID)

    # Glossy ribbon highlight across crown (top-left)
    for x in range(hx - 7, hx + 1):
        canvas.set_pixel(x, hy - 7 + hb, WOOD_LIT)
        canvas.set_pixel(x + 1, hy - 6 + hb, WOOD_HIGHLIGHT)

    # Back hair locks (nape & behind ear)
    for y in range(hy - 3 + hb, hy + 6 + hb):
        canvas.set_pixel(hx - 10, y, OUTLINE)
        canvas.set_pixel(hx - 9, y, BROWN_DARKEST)
        canvas.set_pixel(hx - 8, y, BROWN_DARK)

    # ---------------- 2. Signature Bouncy Cowlick (Follow-through!) ----------------
    # Anchored at top-back crown: (hx - 4, hy - 7 + hb)
    cx0 = hx - 4
    cy0 = hy - 7 + hb
    if hair_wind > 0:
        # Swept backward horizontally in run wind (lags head)
        canvas.line(cx0, cy0, cx0 - 6, cy0 - 1, BROWN_MID)
        canvas.line(cx0 - 1, cy0 - 1, cx0 - 8, cy0 - 2, WOOD_HIGHLIGHT)
        canvas.set_pixel(cx0 - 9, cy0 - 3, WOOD_LIT)
        canvas.set_pixel(cx0 - 10, cy0 - 3, OUTLINE)
        canvas.line(cx0 - 2, cy0, cx0 - 7, cy0, BROWN_LIGHT)
    elif hair_wind < 0:
        # Blown straight up into the air by falling updraft!
        canvas.line(cx0, cy0, cx0, cy0 - 6, BROWN_MID)
        canvas.line(cx0 - 1, cy0 - 1, cx0 - 1, cy0 - 8, WOOD_HIGHLIGHT)
        canvas.set_pixel(cx0 - 1, cy0 - 9, WOOD_LIT)
        canvas.set_pixel(cx0 - 1, cy0 - 10, OUTLINE)
        canvas.line(cx0 + 1, cy0 - 1, cx0 + 1, cy0 - 6, BROWN_LIGHT)
    else:
        # Natural springy curl flicking upward-left
        canvas.set_pixel(cx0, cy0 - 1, BROWN_MID)
        canvas.set_pixel(cx0 - 1, cy0 - 2, BROWN_MID)
        canvas.set_pixel(cx0 - 2, cy0 - 3, WOOD_HIGHLIGHT)
        canvas.set_pixel(cx0 - 3, cy0 - 4, WOOD_HIGHLIGHT)
        canvas.set_pixel(cx0 - 4, cy0 - 5, WOOD_LIT)
        canvas.set_pixel(cx0 - 5, cy0 - 6, WOOD_LIT)
        canvas.set_pixel(cx0 - 6, cy0 - 6, OUTLINE)
        canvas.set_pixel(cx0 - 4, cy0 - 4, BROWN_LIGHT)
        canvas.set_pixel(cx0 - 3, cy0 - 3, BROWN_MID)

    # ---------------- 3. Face Geometry (Skin) ----------------
    for y in range(hy - 3, hy + 8):
        for x in range(hx - 7, hx + 8):
            # Profile bounds
            if y >= hy + 6 and x >= hx + 5: # jaw taper
                continue
            if y >= hy + 7 and (x <= hx - 3 or x >= hx + 4): # chin width
                continue
            
            # Shading
            if y == hy + 7:
                canvas.set_pixel(x, y, SKIN_SHADOW) # bottom of chin
            elif x <= hx - 4 or y == hy - 3:
                canvas.set_pixel(x, y, SKIN_HIGHLIGHT if x <= hx - 5 else SKIN_LIGHT)
            elif x >= hx + 5 or y == hy + 6:
                canvas.set_pixel(x, y, SKIN_SHADOW)
            else:
                canvas.set_pixel(x, y, SKIN_MID if x >= hx + 2 else SKIN_LIGHT)

    # Button nose
    canvas.set_pixel(hx + 7, hy + 2, SKIN_HIGHLIGHT)
    canvas.set_pixel(hx + 8, hy + 2, SKIN_LIGHT)
    canvas.set_pixel(hx + 8, hy + 3, SKIN_SHADOW)

    # Kid ear on left
    canvas.set_pixel(hx - 8, hy + 1, OUTLINE)
    canvas.set_pixel(hx - 7, hy + 1, SKIN_HIGHLIGHT)
    canvas.set_pixel(hx - 7, hy + 2, SKIN_LIGHT)
    canvas.set_pixel(hx - 6, hy + 2, SKIN_SHADOW) # inner helix
    canvas.set_pixel(hx - 7, hy + 3, SKIN_MID)
    canvas.set_pixel(hx - 8, hy + 2, OUTLINE)

    # Cheek blush
    if blush:
        # Far cheek
        canvas.set_pixel(hx - 3, hy + 3, DUSK_PEACH)
        canvas.set_pixel(hx - 2, hy + 3, DUSK_BLUSH)
        # Near cheek
        canvas.set_pixel(hx + 4, hy + 3, DUSK_PEACH)
        canvas.set_pixel(hx + 5, hy + 3, DUSK_BLUSH)
        canvas.set_pixel(hx + 6, hy + 3, DUSK_PEACH)

    # Sweat drop (if scared / nervous)
    if sweat:
        canvas.set_pixel(hx + 7, hy - 1, PURE_WHITE)
        canvas.set_pixel(hx + 7, hy, BLUE_LIGHT)
        canvas.set_pixel(hx + 8, hy, BLUE_MID)

    # ---------------- 4. Bangs / Front Hair Locks (Overlapping face) ----------------
    # Left bang
    canvas.set_pixel(hx - 6, hy - 3 + hb, BROWN_MID)
    canvas.set_pixel(hx - 5, hy - 2 + hb, BROWN_LIGHT)
    canvas.set_pixel(hx - 5, hy - 1 + hb, BROWN_DARK)
    # Center bang
    canvas.set_pixel(hx - 2, hy - 3 + hb, WOOD_HIGHLIGHT)
    canvas.set_pixel(hx - 1, hy - 2 + hb, BROWN_LIGHT)
    canvas.set_pixel(hx - 1, hy - 1 + hb, BROWN_DARK)
    canvas.set_pixel(hx, hy - 2 + hb, BROWN_MID)
    # Front sweep bang
    canvas.set_pixel(hx + 3, hy - 3 + hb, BROWN_LIGHT)
    canvas.set_pixel(hx + 4, hy - 2 + hb, BROWN_MID)
    canvas.set_pixel(hx + 5, hy - 1 + hb, BROWN_DARK)
    canvas.set_pixel(hx + 6, hy - 2 + hb, BROWN_DARKEST)

    # Sideburn in front of ear
    canvas.set_pixel(hx - 6, hy + 2 + hb, BROWN_MID)
    canvas.set_pixel(hx - 6, hy + 3 + hb, BROWN_DARK)

    # ---------------- 5. Eyebrows ----------------
    # Left brow (hx-5 .. hx-2)
    # Right brow (hx+2 .. hx+6)
    brow_color = BROWN_DARKEST
    if eyebrow == "normal":
        # Confident cocky slant
        canvas.line(hx - 5, hy - 1, hx - 2, hy - 1, brow_color)
        canvas.line(hx + 2, hy - 1, hx + 6, hy - 2, brow_color)
    elif eyebrow == "raised":
        # Surprised high arches
        canvas.line(hx - 5, hy - 3, hx - 2, hy - 2, brow_color)
        canvas.line(hx + 2, hy - 3, hx + 6, hy - 3, brow_color)
    elif eyebrow == "worried":
        # Slanted up in center (sad/scared)
        canvas.line(hx - 5, hy - 1, hx - 2, hy - 2, brow_color)
        canvas.line(hx + 2, hy - 2, hx + 6, hy - 1, brow_color)
    elif eyebrow == "angry":
        # Slanted down towards nose bridge
        canvas.line(hx - 5, hy - 2, hx - 2, hy - 1, brow_color)
        canvas.line(hx + 2, hy - 1, hx + 6, hy - 3, brow_color)
    elif eyebrow == "furrowed":
        canvas.line(hx - 4, hy, hx - 2, hy, brow_color)
        canvas.line(hx + 2, hy, hx + 5, hy, brow_color)

    # ---------------- 6. Expressive Eyes with Catchlights ----------------
    # Left eye: (hx-5 .. hx-2, hy .. hy+2)
    # Right eye: (hx+2 .. hx+6, hy .. hy+2)
    if eye_state == "normal":
        # Sclera white
        for y in range(hy, hy + 3):
            for x in range(hx - 5, hx - 1):
                canvas.set_pixel(x, y, PURE_WHITE if y <= hy + 1 else WHITE_SHADOW)
            for x in range(hx + 2, hx + 7):
                canvas.set_pixel(x, y, PURE_WHITE if y <= hy + 1 else WHITE_SHADOW)

        # Directional pupils & specular catchlights
        if look_dir == "forward":
            # Looking ahead/right
            # Left pupil
            canvas.set_pixel(hx - 3, hy, OUTLINE)
            canvas.set_pixel(hx - 3, hy + 1, SHADOW_PURPLE_DARK)
            canvas.set_pixel(hx - 4, hy, PURE_WHITE) # catchlight!
            # Right pupil
            canvas.set_pixel(hx + 5, hy, OUTLINE)
            canvas.set_pixel(hx + 5, hy + 1, SHADOW_PURPLE_DARK)
            canvas.set_pixel(hx + 6, hy, SHADOW_PURPLE_DARK)
            canvas.set_pixel(hx + 6, hy + 1, OUTLINE)
            canvas.set_pixel(hx + 4, hy, PURE_WHITE) # catchlight!
            canvas.set_pixel(hx + 4, hy + 1, WHITE_MID)
        elif look_dir == "up":
            # Looking up at giant hand!
            canvas.set_pixel(hx - 3, hy, OUTLINE)
            canvas.set_pixel(hx - 4, hy, PURE_WHITE)
            canvas.set_pixel(hx + 4, hy, PURE_WHITE)
            canvas.set_pixel(hx + 5, hy, OUTLINE)
            canvas.set_pixel(hx + 6, hy, OUTLINE)
        elif look_dir == "down":
            # Looking down at watch or pit!
            canvas.set_pixel(hx - 3, hy + 1, OUTLINE)
            canvas.set_pixel(hx - 4, hy + 1, PURE_WHITE)
            canvas.set_pixel(hx + 4, hy + 1, PURE_WHITE)
            canvas.set_pixel(hx + 5, hy + 1, OUTLINE)
            canvas.set_pixel(hx + 6, hy + 2, OUTLINE)

    elif eye_state == "wide":
        # Extra large cartoon eyes (excited or scared)
        for y in range(hy - 1, hy + 3):
            for x in range(hx - 5, hx - 1):
                canvas.set_pixel(x, y, PURE_WHITE)
            for x in range(hx + 2, hx + 7):
                canvas.set_pixel(x, y, PURE_WHITE)
        # Large dilated pupils with big catchlights
        canvas.set_pixel(hx - 3, hy, SHADOW_PURPLE_DARK)
        canvas.set_pixel(hx - 3, hy + 1, OUTLINE)
        canvas.set_pixel(hx - 4, hy, PURE_WHITE)
        canvas.set_pixel(hx + 4, hy, PURE_WHITE)
        canvas.set_pixel(hx + 5, hy, SHADOW_PURPLE_DARK)
        canvas.set_pixel(hx + 5, hy + 1, OUTLINE)

    elif eye_state in ["blink", "closed"]:
        # Happy smile curve arcs (^_^)
        canvas.set_pixel(hx - 5, hy + 1, OUTLINE)
        canvas.set_pixel(hx - 4, hy, OUTLINE)
        canvas.set_pixel(hx - 3, hy, OUTLINE)
        canvas.set_pixel(hx - 2, hy + 1, OUTLINE)

        canvas.set_pixel(hx + 2, hy + 1, OUTLINE)
        canvas.set_pixel(hx + 3, hy, OUTLINE)
        canvas.set_pixel(hx + 4, hy, OUTLINE)
        canvas.set_pixel(hx + 5, hy, OUTLINE)
        canvas.set_pixel(hx + 6, hy + 1, OUTLINE)

    elif eye_state == "wink":
        # Left eye open, right eye happy wink with star glint
        for y in range(hy, hy + 3):
            for x in range(hx - 5, hx - 1):
                canvas.set_pixel(x, y, PURE_WHITE)
        canvas.set_pixel(hx - 3, hy, OUTLINE)
        canvas.set_pixel(hx - 4, hy, PURE_WHITE)

        # Right wink arc
        canvas.set_pixel(hx + 2, hy + 1, OUTLINE)
        canvas.set_pixel(hx + 3, hy, OUTLINE)
        canvas.set_pixel(hx + 4, hy, OUTLINE)
        canvas.set_pixel(hx + 5, hy, OUTLINE)
        canvas.set_pixel(hx + 6, hy + 1, OUTLINE)
        # Sparkle glint!
        canvas.set_pixel(hx + 7, hy - 1, YELLOW_LIGHT)
        canvas.set_pixel(hx + 8, hy, YELLOW_MID)

    elif eye_state == "dizzy":
        # Cartoon dizzy spirals
        canvas.set_pixel(hx - 4, hy, YELLOW_LIGHT)
        canvas.set_pixel(hx - 3, hy + 1, OUTLINE)
        canvas.set_pixel(hx - 4, hy + 2, YELLOW_MID)
        canvas.set_pixel(hx - 5, hy + 1, OUTLINE)

        canvas.set_pixel(hx + 3, hy, YELLOW_LIGHT)
        canvas.set_pixel(hx + 4, hy, OUTLINE)
        canvas.set_pixel(hx + 5, hy + 1, YELLOW_MID)
        canvas.set_pixel(hx + 4, hy + 2, OUTLINE)
        canvas.set_pixel(hx + 3, hy + 1, YELLOW_LIGHT)

    elif eye_state in ["oof", "pain"]:
        # Clenched shut (> <)
        canvas.line(hx - 5, hy, hx - 3, hy + 1, OUTLINE)
        canvas.line(hx - 5, hy + 2, hx - 3, hy + 1, OUTLINE)
        canvas.line(hx + 2, hy + 1, hx + 5, hy, OUTLINE)
        canvas.line(hx + 2, hy + 1, hx + 5, hy + 2, OUTLINE)

    # ---------------- 7. Mouth Shapes ----------------
    if mouth == "smirk":
        # Confident cocky grin with white tooth glint & dimple crease
        canvas.set_pixel(hx + 2, hy + 5, OUTLINE)
        canvas.set_pixel(hx + 3, hy + 5, PURE_WHITE) # tooth glint
        canvas.set_pixel(hx + 4, hy + 5, PURE_WHITE)
        canvas.set_pixel(hx + 5, hy + 5, OUTLINE)
        canvas.set_pixel(hx + 6, hy + 4, OUTLINE) # upturned corner
        canvas.set_pixel(hx + 6, hy + 3, SKIN_SHADOW) # cheek crease

    elif mouth == "grin":
        # Wide toothy smile
        for x in range(hx + 1, hx + 7):
            canvas.set_pixel(x, hy + 4, PURE_WHITE) # upper teeth
            canvas.set_pixel(x, hy + 5, OUTLINE if (x in [hx + 1, hx + 6]) else RED_SHADOW)
        canvas.set_pixel(hx + 2, hy + 5, PURE_WHITE) # lower teeth
        canvas.set_pixel(hx + 3, hy + 5, PURE_WHITE)
        canvas.set_pixel(hx + 4, hy + 5, PURE_WHITE)
        canvas.set_pixel(hx + 5, hy + 5, PURE_WHITE)

    elif mouth == "open":
        # Joyful shouting / cheering mouth
        for y in range(hy + 4, hy + 7):
            for x in range(hx + 2, hx + 7):
                if y == hy + 4:
                    canvas.set_pixel(x, y, PURE_WHITE) # teeth row
                elif y == hy + 6:
                    canvas.set_pixel(x, y, RED_LIGHT if (x in [hx + 3, hx + 4]) else RED_SHADOW) # tongue
                else:
                    canvas.set_pixel(x, y, RED_DEEP) # mouth cavity
        canvas.set_pixel(hx + 1, hy + 5, OUTLINE)
        canvas.set_pixel(hx + 7, hy + 5, OUTLINE)

    elif mouth == "o":
        # Surprised round 'O' mouth
        canvas.set_pixel(hx + 3, hy + 4, OUTLINE)
        canvas.set_pixel(hx + 4, hy + 4, OUTLINE)
        canvas.set_pixel(hx + 2, hy + 5, OUTLINE)
        canvas.set_pixel(hx + 3, hy + 5, RED_DEEP)
        canvas.set_pixel(hx + 4, hy + 5, RED_DEEP)
        canvas.set_pixel(hx + 5, hy + 5, OUTLINE)
        canvas.set_pixel(hx + 3, hy + 6, OUTLINE)
        canvas.set_pixel(hx + 4, hy + 6, OUTLINE)

    elif mouth == "grimace":
        # Gritted clenched teeth
        for x in range(hx + 1, hx + 7):
            canvas.set_pixel(x, hy + 5, PURE_WHITE if (x % 2 == 0) else WHITE_SHADOW)
            canvas.set_pixel(x, hy + 4, OUTLINE)
            canvas.set_pixel(x, hy + 6, OUTLINE)
        canvas.set_pixel(hx, hy + 5, OUTLINE)
        canvas.set_pixel(hx + 7, hy + 5, OUTLINE)

    elif mouth == "pout":
        # Impatient turned-down lip
        canvas.set_pixel(hx + 2, hy + 5, OUTLINE)
        canvas.set_pixel(hx + 3, hy + 5, OUTLINE)
        canvas.set_pixel(hx + 4, hy + 5, OUTLINE)
        canvas.set_pixel(hx + 5, hy + 5, OUTLINE)
        canvas.set_pixel(hx + 5, hy + 6, OUTLINE)

    elif mouth == "yawn":
        # Wide sleepy open yawn
        for y in range(hy + 3, hy + 8):
            for x in range(hx + 2, hx + 7):
                if y == hy + 3 or y == hy + 7 or x == hx + 2 or x == hx + 6:
                    canvas.set_pixel(x, y, OUTLINE)
                elif y == hy + 6:
                    canvas.set_pixel(x, y, RED_LIGHT) # tongue
                else:
                    canvas.set_pixel(x, y, RED_DEEP)


def draw_arm_v2(canvas: PixelCanvas, shoulder_x: int, shoulder_y: int,
                hand_x: int, hand_y: int, is_far: bool = False,
                pose: str = "swing", fist: bool = False, pointing: bool = False,
                watch: bool = False):
    """
    Draws kid arm with hoodie sleeve, ribbed wrist cuff, and hand.
    """
    sleeve_c = RED_SHADOW if is_far else RED_MID
    sleeve_l = RED_MID if is_far else RED_LIGHT
    sleeve_d = RED_DEEP if is_far else RED_SHADOW

    hand_c = SKIN_SHADOW if is_far else SKIN_LIGHT
    hand_d = SKIN_DEEP if is_far else SKIN_MID

    # Draw sleeve cylinder from shoulder to wrist (hand_x, hand_y - 2)
    wrist_x = hand_x
    wrist_y = hand_y - 2 if hand_y >= shoulder_y else hand_y + 2
    steps = max(abs(wrist_x - shoulder_x), abs(wrist_y - shoulder_y), 1)

    for s in range(steps + 1):
        t = s / steps
        cx = int(round(shoulder_x + t * (wrist_x - shoulder_x)))
        cy = int(round(shoulder_y + t * (wrist_y - shoulder_y)))
        # 3-4px thick sleeve
        canvas.set_pixel(cx - 1, cy, sleeve_l)
        canvas.set_pixel(cx, cy, sleeve_c)
        canvas.set_pixel(cx + 1, cy, sleeve_d)

    # Ribbed wrist cuff
    canvas.set_pixel(wrist_x - 1, wrist_y, RED_RICH)
    canvas.set_pixel(wrist_x, wrist_y, RED_SHADOW)
    canvas.set_pixel(wrist_x + 1, wrist_y, RED_DEEP)

    # Watch on near wrist
    if watch and not is_far:
        canvas.set_pixel(wrist_x - 1, wrist_y, BLUE_MID) # strap
        canvas.set_pixel(wrist_x, wrist_y, YELLOW_LIGHT) # watch face
        canvas.set_pixel(wrist_x + 1, wrist_y, BLUE_MID)

    # Hand
    if pointing:
        # Extended index finger
        canvas.set_pixel(hand_x, hand_y, hand_c)
        canvas.set_pixel(hand_x + 1, hand_y - 1, hand_c)
        canvas.set_pixel(hand_x + 2, hand_y - 2, hand_c)
        canvas.set_pixel(hand_x + 3, hand_y - 3, hand_c)
        canvas.set_pixel(hand_x, hand_y + 1, hand_d)
    elif fist:
        # Clenched fist
        canvas.set_pixel(hand_x - 1, hand_y, hand_c)
        canvas.set_pixel(hand_x, hand_y, hand_c)
        canvas.set_pixel(hand_x + 1, hand_y, hand_c)
        canvas.set_pixel(hand_x - 1, hand_y + 1, hand_d)
        canvas.set_pixel(hand_x, hand_y + 1, hand_d)
    else:
        # Relaxed kid hand
        canvas.set_pixel(hand_x - 1, hand_y, hand_c)
        canvas.set_pixel(hand_x, hand_y, hand_c)
        canvas.set_pixel(hand_x + 1, hand_y, hand_c)
        canvas.set_pixel(hand_x, hand_y + 1, hand_d)


# =============================================================================
# 19 ANIMATION GENERATORS
# =============================================================================

def generate_p1_idle() -> List[PixelCanvas]:
    """
    8 frames, 8 fps, loop: true.
    Relaxed standing breathing cycle:
    - Subtle chest rise and fall (sub-pixel breathing)
    - Natural blinking on frames 4 and 5
    - Gentle lag on hair cowlick
    - Both sneakers firmly planted on ground touching row y=63
    """
    frames = []
    # 8-frame breathing offsets: rise on 2..4, relax on 5..7
    bobs = [0, 0, -1, -1, -1, 0, 0, 0]
    eye_states = ["normal", "normal", "normal", "normal", "blink", "blink", "normal", "normal"]

    for i in range(8):
        c = create_base_canvas()
        bob = bobs[i]

        # 1. Sneakers planted flat touching row 63
        draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="flat", is_far=True)
        draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="flat", is_far=False)

        # 2. Bare legs
        draw_leg_v2(c, hip_x=28, hip_y=52 + bob, foot_x=26, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=52 + bob, foot_x=38, foot_y=57, is_far=False)

        # 3. Denim shorts
        draw_shorts_v2(c, sx=32, sy=45 + bob, w=18, h=9)

        # 4. Far arm resting at side
        draw_arm_v2(c, shoulder_x=24, shoulder_y=33 + bob, hand_x=22, hand_y=42 + bob, is_far=True)

        # 5. Red hoodie
        draw_hoodie_v2(c, tx=32, ty=31 + bob, w=20, h=15, drawstring_wind=0)

        # 6. Near arm resting at side
        draw_arm_v2(c, shoulder_x=40, shoulder_y=33 + bob, hand_x=42, hand_y=42 + bob, is_far=False)

        # 7. Head with hair & smirk
        draw_head_v2(c, hx=32, hy=22 + bob, eye_state=eye_states[i], look_dir="forward",
                     mouth="smirk", eyebrow="normal", hair_bob=-1 if bob < 0 else 0)

        # Verify anchor rule
        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_idle frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_idle_yawn() -> List[PixelCanvas]:
    """
    8 frames, 6 fps, loop: false.
    Sleepy kid idle variant:
    Begins standing, mouth opens into a huge sleepy yawn, eyes squeeze shut,
    hand covers mouth, sighs with a gentle blink. Lowest foot touches y=63 in all frames.
    """
    frames = []
    # Mouth progression: smirk -> o -> yawn -> yawn -> yawn -> o -> smirk -> smirk
    mouths = ["smirk", "o", "yawn", "yawn", "yawn", "o", "smirk", "smirk"]
    eyes = ["normal", "normal", "closed", "closed", "closed", "blink", "normal", "normal"]
    hand_up = [False, False, True, True, True, False, False, False]

    for i in range(8):
        c = create_base_canvas()

        # Sneakers flat on y=63
        draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="flat", is_far=True)
        draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="flat", is_far=False)

        # Legs & shorts
        draw_leg_v2(c, hip_x=28, hip_y=52, foot_x=26, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=52, foot_x=38, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=32, sy=45, w=18, h=9)

        # Far arm
        draw_arm_v2(c, shoulder_x=24, shoulder_y=33, hand_x=22, hand_y=42, is_far=True)

        # Hoodie
        draw_hoodie_v2(c, tx=32, ty=31, w=20, h=15)

        # Near arm (covers mouth during yawn)
        if hand_up[i]:
            draw_arm_v2(c, shoulder_x=40, shoulder_y=33, hand_x=36, hand_y=28, is_far=False)
        else:
            draw_arm_v2(c, shoulder_x=40, shoulder_y=33, hand_x=42, hand_y=42, is_far=False)

        # Head
        draw_head_v2(c, hx=32, hy=22, eye_state=eyes[i], look_dir="forward",
                     mouth=mouths[i], eyebrow="worried" if mouths[i] == "yawn" else "normal")

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_idle_yawn frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_idle_stretch() -> List[PixelCanvas]:
    """
    10 frames, 6 fps, loop: false.
    Satisfying full-body kid stretch:
    Hands interlock, reach high above head, torso elongates (stretch),
    toes stay firmly planted touching row 63, arms lower with relief.
    """
    frames = []
    # Stretch vertical elongation: [0, -1, -2, -3, -3, -3, -2, -1, 0, 0]
    stretches = [0, -1, -2, -3, -3, -3, -2, -1, 0, 0]

    for i in range(10):
        c = create_base_canvas()
        st = stretches[i]

        # Sneakers on ground touching y=63
        if st <= -2:
            # Rises slightly on toes, toe cap touches y=63
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="toe_push", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="toe_push", is_far=False)
        else:
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="flat", is_far=False)

        # Legs & shorts stretched
        draw_leg_v2(c, hip_x=28, hip_y=52 + st, foot_x=26, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=52 + st, foot_x=38, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=32, sy=45 + st, w=17, h=9)

        # Hoodie elongated
        draw_hoodie_v2(c, tx=32, ty=31 + st, w=19, h=15, folds=1 if st < 0 else 0)

        # Arms reaching high up
        if i in [2, 3, 4, 5]:
            # Arms stretched high above head
            draw_arm_v2(c, shoulder_x=24, shoulder_y=32 + st, hand_x=28, hand_y=14 + st, is_far=True)
            draw_arm_v2(c, shoulder_x=40, shoulder_y=32 + st, hand_x=36, hand_y=14 + st, is_far=False)
            draw_head_v2(c, hx=32, hy=22 + st, eye_state="closed", look_dir="up",
                         mouth="grin", eyebrow="raised", hair_bob=-1)
        elif i in [1, 6]:
            # Reaching midway
            draw_arm_v2(c, shoulder_x=24, shoulder_y=33 + st, hand_x=25, hand_y=22 + st, is_far=True)
            draw_arm_v2(c, shoulder_x=40, shoulder_y=33 + st, hand_x=39, hand_y=22 + st, is_far=False)
            draw_head_v2(c, hx=32, hy=22 + st, eye_state="normal", look_dir="up", mouth="smirk")
        else:
            # Settled
            draw_arm_v2(c, shoulder_x=24, shoulder_y=33, hand_x=22, hand_y=42, is_far=True)
            draw_arm_v2(c, shoulder_x=40, shoulder_y=33, hand_x=42, hand_y=42, is_far=False)
            draw_head_v2(c, hx=32, hy=22, eye_state="normal", look_dir="forward", mouth="smirk")

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_idle_stretch frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_idle_bounce() -> List[PixelCanvas]:
    """
    6 frames, 10 fps, loop: true.
    Bouncing on toes idle variant:
    Energetic kid bouncing with springy knee bends and hair lag.
    Lowest foot touches row y=63 in all 6 frames!
    """
    frames = []
    # Bounce heights: [0, 1, 0, -2, -1, 0] (squash on 1, stretch on 3)
    bobs = [0, 1, 0, -2, -1, 0]

    for i in range(6):
        c = create_base_canvas()
        bob = bobs[i]

        # Sneaker poses: squash on 1, toe push on 3, flat otherwise
        if i == 1:
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="squash", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="squash", is_far=False)
        elif i in [3, 4]:
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="toe_push", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="toe_push", is_far=False)
        else:
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="flat", is_far=False)

        draw_leg_v2(c, hip_x=28, hip_y=52 + bob, foot_x=26, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=52 + bob, foot_x=38, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=32, sy=45 + bob, w=18, h=9)

        # Arms pumping slightly with rhythm
        arm_dy = 2 if i in [1, 2] else -2
        draw_arm_v2(c, shoulder_x=24, shoulder_y=33 + bob, hand_x=22, hand_y=42 + bob + arm_dy, is_far=True)
        draw_hoodie_v2(c, tx=32, ty=31 + bob, w=20, h=15, folds=-1 if bob > 0 else 1)
        draw_arm_v2(c, shoulder_x=40, shoulder_y=33 + bob, hand_x=42, hand_y=42 + bob + arm_dy, is_far=False)

        draw_head_v2(c, hx=32, hy=22 + bob, eye_state="normal", look_dir="forward",
                     mouth="grin", eyebrow="normal", hair_bob=-bob)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_idle_bounce frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_wait() -> List[PixelCanvas]:
    """
    10 frames, 10 fps, loop: true.
    Impatient hazard waiting cycle:
    - Foot tapping: right foot lifts toe and taps down rhythmically on y=63
    - Crossed arms over hoodie chest
    - Checks pretend toy watch on wrist
    - Looks up and sighs with an annoyed huff
    - Guaranteed row y=63 contact in all 10 frames!
    """
    frames = []

    for i in range(10):
        c = create_base_canvas()

        # Foot tapping on right foot: taps up on 0, 2, 4, 6
        right_tap = (i in [0, 2, 4, 6])

        # Left foot firmly planted on y=63
        draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="flat", is_far=True)

        # Right foot tapping
        if right_tap:
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="heel_strike", is_far=False)
        else:
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="flat", is_far=False)

        draw_leg_v2(c, hip_x=28, hip_y=52, foot_x=26, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=52, foot_x=38, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=32, sy=45, w=18, h=9)
        draw_hoodie_v2(c, tx=32, ty=31, w=20, h=15)

        if i in [4, 5, 6]:
            # Checking pretend toy watch on wrist!
            draw_arm_v2(c, shoulder_x=24, shoulder_y=33, hand_x=34, hand_y=38, is_far=True)
            draw_arm_v2(c, shoulder_x=40, shoulder_y=33, hand_x=34, hand_y=38, is_far=False, watch=True)
            # Head looking down at watch with grimace
            draw_head_v2(c, hx=32, hy=22, eye_state="normal", look_dir="down", mouth="grimace", eyebrow="furrowed")
        elif i in [0, 1, 2, 3]:
            # Arms tightly crossed across chest, looking up at sky/hand
            draw_arm_v2(c, shoulder_x=24, shoulder_y=33, hand_x=38, hand_y=38, is_far=True)
            draw_arm_v2(c, shoulder_x=40, shoulder_y=33, hand_x=26, hand_y=38, is_far=False)
            draw_head_v2(c, hx=32, hy=22, eye_state="normal", look_dir="up", mouth="pout", eyebrow="worried")
        else: # 7, 8, 9
            # Sighing huff forward
            draw_arm_v2(c, shoulder_x=24, shoulder_y=33, hand_x=38, hand_y=38, is_far=True)
            draw_arm_v2(c, shoulder_x=40, shoulder_y=33, hand_x=26, hand_y=38, is_far=False)
            draw_head_v2(c, hx=32, hy=22, eye_state="blink", look_dir="forward", mouth="pout", eyebrow="normal")

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_wait frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_wait_point() -> List[PixelCanvas]:
    """
    6 frames, 8 fps, loop: false.
    Hazard call for help:
    Points up at the hand ("Hey, look up!"), then points forward at the obstacle ("Help me!").
    Sneakers planted at row y=63.
    """
    frames = []

    for i in range(6):
        c = create_base_canvas()

        draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="flat", is_far=True)
        draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="flat", is_far=False)

        draw_leg_v2(c, hip_x=28, hip_y=52, foot_x=26, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=52, foot_x=38, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=32, sy=45, w=18, h=9)

        # Far arm on hip
        draw_arm_v2(c, shoulder_x=24, shoulder_y=33, hand_x=24, hand_y=42, is_far=True, fist=True)

        draw_hoodie_v2(c, tx=32, ty=31, w=20, h=15)

        if i in [0, 1, 2]:
            # Points up toward hand!
            draw_arm_v2(c, shoulder_x=40, shoulder_y=33, hand_x=44, hand_y=16, is_far=False, pointing=True)
            draw_head_v2(c, hx=32, hy=22, eye_state="wide", look_dir="up", mouth="open", eyebrow="raised")
        else: # 3, 4, 5
            # Sweeps arm down and points right toward the hazard
            draw_arm_v2(c, shoulder_x=40, shoulder_y=33, hand_x=52, hand_y=34, is_far=False, pointing=True)
            draw_head_v2(c, hx=32, hy=22, eye_state="normal", look_dir="forward", mouth="open", eyebrow="normal")

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_wait_point frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_run() -> List[PixelCanvas]:
    """
    12 frames, 20 fps, loop: true.
    Full athletic 12-frame double-step kid run cycle:
    Contact, down (squash), passing, up (push-off), flight apex, flight descent for BOTH legs!
    - Arms crossing the body with dynamic pumping
    - Drawstrings and hair streaming back with secondary follow-through
    - Determined grin with pupil tracking forward
    - CRUCIAL: Lowest foot pixel touches row y=63 in every single frame!
    """
    frames = []

    # 12-frame cycle:
    # 0: Contact Right (right heel strike forward at y=63, left toe trailing)
    # 1: Down / Squash Right (right foot flat on y=63, body squashed)
    # 2: Passing Right (right foot flat on y=63, left knee swinging forward)
    # 3: Up / Push-off Right (right toe pushing at y=63, body rising)
    # 4: Flight Apex 1 (both feet airborne, trailing left toe touches row 63)
    # 5: Flight Descent 1 (reaching left foot descending touching row 63)
    # 6: Contact Left (left heel strike forward at y=63, right toe trailing)
    # 7: Down / Squash Left (left foot flat on y=63, body squashed)
    # 8: Passing Left (left foot flat on y=63, right knee swinging forward)
    # 9: Up / Push-off Left (left toe pushing at y=63, body rising)
    # 10: Flight Apex 2 (both feet airborne, trailing right toe touches row 63)
    # 11: Flight Descent 2 (reaching right foot descending touching row 63)

    bobs = [0, 2, 0, -2, -3, -1, 0, 2, 0, -2, -3, -1]

    for i in range(12):
        c = create_base_canvas()
        bob = bobs[i]

        # Pumping arms coordinates
        if i in [0, 1, 2]:
            near_arm = (42, 42 + bob)
            far_arm = (22, 40 + bob)
        elif i in [3, 4, 5]:
            near_arm = (46, 36 + bob)
            far_arm = (18, 44 + bob)
        elif i in [6, 7, 8]:
            near_arm = (22, 40 + bob)
            far_arm = (42, 42 + bob)
        else: # 9, 10, 11
            near_arm = (18, 44 + bob)
            far_arm = (46, 36 + bob)

        # Draw legs based on phase
        if i == 0:
            draw_sneaker_v2(c, foot_x=20, foot_y=57, pose="toe_point", is_far=True)
            draw_sneaker_v2(c, foot_x=42, foot_y=63, pose="heel_strike", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=20, foot_y=53, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=42, foot_y=59, is_far=False)
        elif i == 1:
            draw_sneaker_v2(c, foot_x=26, foot_y=57, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="squash", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=26, foot_y=53, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=38, foot_y=57, is_far=False)
        elif i == 2:
            draw_sneaker_v2(c, foot_x=42, foot_y=53, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=32, foot_y=63, pose="flat", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=42, foot_y=49, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=32, foot_y=57, is_far=False)
        elif i == 3:
            draw_sneaker_v2(c, foot_x=44, foot_y=51, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="toe_push", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=44, foot_y=47, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=26, foot_y=57, is_far=False)
        elif i == 4:
            draw_sneaker_v2(c, foot_x=45, foot_y=50, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=24, foot_y=63, pose="toe_point", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=45, foot_y=46, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=24, foot_y=57, is_far=False)
        elif i == 5:
            draw_sneaker_v2(c, foot_x=44, foot_y=63, pose="heel_strike", is_far=True)
            draw_sneaker_v2(c, foot_x=22, foot_y=58, pose="toe_point", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=44, foot_y=59, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=22, foot_y=54, is_far=False)
        elif i == 6:
            draw_sneaker_v2(c, foot_x=42, foot_y=63, pose="heel_strike", is_far=True)
            draw_sneaker_v2(c, foot_x=20, foot_y=57, pose="toe_point", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=42, foot_y=59, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=20, foot_y=53, is_far=False)
        elif i == 7:
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="squash", is_far=True)
            draw_sneaker_v2(c, foot_x=26, foot_y=57, pose="flat", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=38, foot_y=57, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=26, foot_y=53, is_far=False)
        elif i == 8:
            draw_sneaker_v2(c, foot_x=32, foot_y=63, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=42, foot_y=53, pose="flat", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=32, foot_y=57, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=42, foot_y=49, is_far=False)
        elif i == 9:
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="toe_push", is_far=True)
            draw_sneaker_v2(c, foot_x=44, foot_y=51, pose="flat", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=26, foot_y=57, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=44, foot_y=47, is_far=False)
        elif i == 10:
            draw_sneaker_v2(c, foot_x=24, foot_y=63, pose="toe_point", is_far=True)
            draw_sneaker_v2(c, foot_x=45, foot_y=50, pose="flat", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=24, foot_y=57, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=45, foot_y=46, is_far=False)
        else: # 11
            draw_sneaker_v2(c, foot_x=22, foot_y=58, pose="toe_point", is_far=True)
            draw_sneaker_v2(c, foot_x=44, foot_y=63, pose="heel_strike", is_far=False)
            draw_leg_v2(c, hip_x=30, hip_y=52 + bob, foot_x=22, foot_y=54, is_far=True)
            draw_leg_v2(c, hip_x=35, hip_y=52 + bob, foot_x=44, foot_y=59, is_far=False)

        # Shorts leaning forward slightly
        draw_shorts_v2(c, sx=33, sy=45 + bob, w=18, h=9)

        # Far arm
        draw_arm_v2(c, shoulder_x=25, shoulder_y=33 + bob, hand_x=far_arm[0], hand_y=far_arm[1], is_far=True)

        # Hoodie thrust forward with wind in drawstrings
        draw_hoodie_v2(c, tx=33, ty=31 + bob, w=20, h=15, drawstring_wind=2, folds=1)

        # Near arm
        draw_arm_v2(c, shoulder_x=41, shoulder_y=33 + bob, hand_x=near_arm[0], hand_y=near_arm[1], is_far=False)

        # Head tilted slightly forward, hair streaming back in wind
        draw_head_v2(c, hx=34, hy=22 + bob, eye_state="normal", look_dir="forward",
                     mouth="smirk", eyebrow="normal", hair_bob=-1 if bob < 0 else 0, hair_wind=1)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_run frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_run_fast() -> List[PixelCanvas]:
    """
    10 frames, 24 fps, loop: true.
    High speed sprint with Speed Boots (orange with yellow wings):
    - Low aerodynamic forward lean
    - Piston-blade arm pumping
    - Streaming speed lines
    - Row y=63 contact guaranteed in every frame!
    """
    frames = []

    strides = [
        # (fwd_x, fwd_y, fwd_pose, back_x, back_y, back_pose, bob)
        (45, 63, "heel_strike", 17, 55, "toe_point", 0),
        (41, 63, "flat",        23, 56, "flat",       2),
        (33, 63, "toe_push",    35, 52, "flat",       0),
        (23, 63, "toe_point",   45, 50, "flat",      -2),
        (45, 63, "heel_strike", 17, 55, "toe_point", 0),
        (41, 63, "flat",        23, 56, "flat",       2),
        (33, 63, "toe_push",    35, 52, "flat",       0),
        (23, 63, "toe_point",   45, 50, "flat",      -2),
        (43, 63, "heel_strike", 19, 54, "toe_point", -1),
        (35, 63, "toe_push",    39, 51, "flat",       0),
    ]

    for i, (fx1, fy1, p1, fx2, fy2, p2, bob) in enumerate(strides):
        c = create_base_canvas()

        # Speed streak sparks behind feet
        c.set_pixel(fx2 - 4, fy2, YELLOW_LIGHT)
        c.set_pixel(fx2 - 8, fy2, ORANGE_MID)
        c.set_pixel(fx1 - 6, fy1 - 2, YELLOW_LIGHT)
        c.set_pixel(fx1 - 10, fy1 - 2, ORANGE_SHADOW)

        # Speed boots (Orange ramp + yellow lightning wings)
        is_even = (i < 5)
        draw_sneaker_v2(c, foot_x=fx2, foot_y=fy2, pose=p2, speed_boot=True, is_far=is_even)
        draw_sneaker_v2(c, foot_x=fx1, foot_y=fy1, pose=p1, speed_boot=True, is_far=not is_even)

        draw_leg_v2(c, hip_x=31, hip_y=51 + bob, foot_x=fx2, foot_y=fy2 - 4, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=51 + bob, foot_x=fx1, foot_y=fy1 - 4, is_far=False)

        draw_shorts_v2(c, sx=34, sy=45 + bob, w=18, h=9)

        # Arms pumping like piston blades
        if i in [0, 1, 4, 5, 8]:
            arm_front = (48, 38 + bob)
            arm_back = (20, 42 + bob)
        else:
            arm_front = (22, 42 + bob)
            arm_back = (46, 38 + bob)

        draw_arm_v2(c, shoulder_x=26, shoulder_y=33 + bob, hand_x=arm_back[0], hand_y=arm_back[1], is_far=True)
        draw_hoodie_v2(c, tx=34, ty=31 + bob, w=20, h=15, drawstring_wind=3, folds=1)
        draw_arm_v2(c, shoulder_x=42, shoulder_y=33 + bob, hand_x=arm_front[0], hand_y=arm_front[1], is_far=False)

        draw_head_v2(c, hx=36, hy=22 + bob, eye_state="wide", look_dir="forward",
                     mouth="smirk", eyebrow="normal", hair_bob=-2, hair_wind=1)

        # Speed lines streaming behind hair
        c.line(24, 18 + bob, 12, 19 + bob, BROWN_LIGHT)
        c.line(22, 20 + bob, 10, 21 + bob, BROWN_DARK)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_run_fast frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_jump_up() -> List[PixelCanvas]:
    """
    3 frames, 16 fps, loop: false.
    F0: Anticipation crouch / squash (knees bent wide, feet on y=63).
    F1: Explosive upward launch / stretch (toes driving off y=63, arms reaching sky).
    F2: Rising momentum (tucking knees up, trailing toe touches row 63).
    """
    frames = []

    # ---------------- Frame 0: Deep Anticipation Crouch ----------------
    c0 = create_base_canvas()
    draw_sneaker_v2(c0, foot_x=22, foot_y=63, pose="squash", is_far=True)
    draw_sneaker_v2(c0, foot_x=42, foot_y=63, pose="squash", is_far=False)
    draw_leg_v2(c0, hip_x=26, hip_y=54, foot_x=22, foot_y=59, is_far=True)
    draw_leg_v2(c0, hip_x=38, hip_y=54, foot_x=42, foot_y=59, is_far=False)
    draw_shorts_v2(c0, sx=32, sy=49, w=20, h=8)
    draw_hoodie_v2(c0, tx=32, ty=36, w=22, h=14, folds=-1)
    # Arms swung down-back preparing to propel up
    draw_arm_v2(c0, shoulder_x=23, shoulder_y=38, hand_x=18, hand_y=46, is_far=True)
    draw_arm_v2(c0, shoulder_x=41, shoulder_y=38, hand_x=46, hand_y=46, is_far=False)
    draw_head_v2(c0, hx=32, hy=28, eye_state="normal", look_dir="up", mouth="smirk", eyebrow="raised")
    assert any(c0.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c0)

    # ---------------- Frame 1: Launch Blast-Off (Stretch) ----------------
    c1 = create_base_canvas()
    # Toes fully extended pointing down, driving off y=63
    draw_sneaker_v2(c1, foot_x=28, foot_y=63, pose="toe_point", is_far=True)
    draw_sneaker_v2(c1, foot_x=36, foot_y=63, pose="toe_point", is_far=False)
    draw_leg_v2(c1, hip_x=29, hip_y=46, foot_x=28, foot_y=57, is_far=True)
    draw_leg_v2(c1, hip_x=35, hip_y=46, foot_x=36, foot_y=57, is_far=False)
    draw_shorts_v2(c1, sx=32, sy=39, w=16, h=9)
    draw_hoodie_v2(c1, tx=32, ty=25, w=18, h=15, folds=1)
    # Arms shooting straight skyward!
    draw_arm_v2(c1, shoulder_x=24, shoulder_y=26, hand_x=22, hand_y=12, is_far=True)
    draw_arm_v2(c1, shoulder_x=40, shoulder_y=26, hand_x=42, hand_y=12, is_far=False)
    draw_head_v2(c1, hx=32, hy=16, eye_state="wide", look_dir="up", mouth="open", eyebrow="raised", hair_wind=1)
    assert any(c1.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c1)

    # ---------------- Frame 2: Rising Momentum ----------------
    c2 = create_base_canvas()
    # Knees pulling up, trailing foot touches row 63 for anchor
    draw_sneaker_v2(c2, foot_x=28, foot_y=63, pose="toe_point", is_far=True)
    draw_sneaker_v2(c2, foot_x=38, foot_y=57, pose="flat", is_far=False)
    draw_leg_v2(c2, hip_x=29, hip_y=45, foot_x=28, foot_y=57, is_far=True)
    draw_leg_v2(c2, hip_x=35, hip_y=45, foot_x=38, foot_y=51, is_far=False)
    draw_shorts_v2(c2, sx=32, sy=38, w=18, h=9)
    draw_hoodie_v2(c2, tx=32, ty=24, w=19, h=15)
    # Arms bent in front guiding ascent
    draw_arm_v2(c2, shoulder_x=24, shoulder_y=26, hand_x=20, hand_y=18, is_far=True)
    draw_arm_v2(c2, shoulder_x=40, shoulder_y=26, hand_x=44, hand_y=18, is_far=False)
    draw_head_v2(c2, hx=32, hy=15, eye_state="normal", look_dir="forward", mouth="smirk", eyebrow="normal")
    assert any(c2.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c2)

    return frames


def generate_p1_jump_apex() -> List[PixelCanvas]:
    """
    2 frames, 12 fps, loop: false.
    Zero-g hang time at the peak of the jump:
    - Arms spread wide for aerodynamic balance
    - Hair and drawstrings floating weightlessly
    - Trailing toe touches row y=63 for anchor in both frames
    """
    frames = []

    for i in range(2):
        c = create_base_canvas()
        # Trailing toe reaches row 63
        draw_sneaker_v2(c, foot_x=28, foot_y=63, pose="toe_point", is_far=True)
        draw_sneaker_v2(c, foot_x=38, foot_y=56 - i, pose="flat", is_far=False)

        draw_leg_v2(c, hip_x=29, hip_y=44, foot_x=28, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=35, hip_y=44, foot_x=38, foot_y=50 - i, is_far=False)
        draw_shorts_v2(c, sx=32, sy=37, w=18, h=9)
        draw_hoodie_v2(c, tx=32, ty=23, w=19, h=15, drawstring_wind=1)

        # Arms spread wide like soaring wings
        draw_arm_v2(c, shoulder_x=24, shoulder_y=25, hand_x=14, hand_y=23 + i, is_far=True)
        draw_arm_v2(c, shoulder_x=40, shoulder_y=25, hand_x=50, hand_y=23 + i, is_far=False)

        draw_head_v2(c, hx=32, hy=14, eye_state="normal", look_dir="forward", mouth="smirk", hair_bob=-1)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_jump_apex frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_fall() -> List[PixelCanvas]:
    """
    3 frames, 16 fps, loop: true.
    High speed descent:
    - Updraft pushes hair and drawstrings straight up!
    - Legs reaching downward touching row y=63
    - Wide eyes looking down at landing zone
    """
    frames = []

    for i in range(3):
        c = create_base_canvas()

        # Both legs reaching downward touching row 63
        draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="toe_point", is_far=True)
        draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="toe_point", is_far=False)

        draw_leg_v2(c, hip_x=28, hip_y=48, foot_x=26, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=48, foot_x=38, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=32, sy=41, w=18, h=9)
        draw_hoodie_v2(c, tx=32, ty=27, w=19, h=15, drawstring_wind=-1)

        # Arms pushed upward by rushing air
        draw_arm_v2(c, shoulder_x=24, shoulder_y=29, hand_x=18, hand_y=16 - i, is_far=True)
        draw_arm_v2(c, shoulder_x=40, shoulder_y=29, hand_x=46, hand_y=16 - i, is_far=False)

        # Drawstrings flapping straight up
        c.line(29, 25, 28, 20, PURE_WHITE)
        c.line(35, 25, 36, 20, PURE_WHITE)

        # Hair blown straight up by wind! Wide eyes looking down
        draw_head_v2(c, hx=32, hy=18, eye_state="wide", look_dir="down", mouth="open", eyebrow="worried", hair_wind=-1)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_fall frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_land() -> List[PixelCanvas]:
    """
    4 frames, 20 fps, loop: false.
    F0: Hard impact squash, feet wide, dust puffs at row y=63.
    F1: Low absorb crouch, rebounding upward.
    F2: Rising extension.
    F3: Settled upright standing ready stance.
    Every single frame touches row y=63!
    """
    frames = []

    # ---------------- Frame 0: Hard Impact Squash ----------------
    c0 = create_base_canvas()
    draw_sneaker_v2(c0, foot_x=20, foot_y=63, pose="squash", is_far=True)
    draw_sneaker_v2(c0, foot_x=44, foot_y=63, pose="squash", is_far=False)
    # Impact dust puffs kicked out to sides
    c0.set_pixel(14, 63, PURE_WHITE)
    c0.set_pixel(13, 63, WHITE_SHADOW)
    c0.set_pixel(12, 62, WHITE_SHADOW)
    c0.set_pixel(50, 63, PURE_WHITE)
    c0.set_pixel(51, 63, WHITE_SHADOW)
    c0.set_pixel(52, 62, WHITE_SHADOW)

    draw_leg_v2(c0, hip_x=26, hip_y=54, foot_x=20, foot_y=59, is_far=True)
    draw_leg_v2(c0, hip_x=38, hip_y=54, foot_x=44, foot_y=59, is_far=False)
    draw_shorts_v2(c0, sx=32, sy=49, w=22, h=7)
    draw_hoodie_v2(c0, tx=32, ty=38, w=24, h=13, folds=-1)
    # Arms flared wide for impact balance
    draw_arm_v2(c0, shoulder_x=22, shoulder_y=40, hand_x=12, hand_y=44, is_far=True)
    draw_arm_v2(c0, shoulder_x=42, shoulder_y=40, hand_x=52, hand_y=44, is_far=False)
    # Head compressed, eyes squinting shut from impact
    draw_head_v2(c0, hx=32, hy=30, eye_state="closed", look_dir="forward", mouth="grimace", eyebrow="furrowed")
    assert any(c0.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c0)

    # ---------------- Frame 1: Low Absorb Crouch ----------------
    c1 = create_base_canvas()
    draw_sneaker_v2(c1, foot_x=24, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c1, foot_x=40, foot_y=63, pose="flat", is_far=False)
    draw_leg_v2(c1, hip_x=27, hip_y=53, foot_x=24, foot_y=57, is_far=True)
    draw_leg_v2(c1, hip_x=37, hip_y=53, foot_x=40, foot_y=57, is_far=False)
    draw_shorts_v2(c1, sx=32, sy=47, w=20, h=8)
    draw_hoodie_v2(c1, tx=32, ty=34, w=22, h=14)
    draw_arm_v2(c1, shoulder_x=23, shoulder_y=36, hand_x=18, hand_y=43, is_far=True)
    draw_arm_v2(c1, shoulder_x=41, shoulder_y=36, hand_x=46, hand_y=43, is_far=False)
    draw_head_v2(c1, hx=32, hy=26, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c1.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c1)

    # ---------------- Frame 2: Rising Extension ----------------
    c2 = create_base_canvas()
    draw_sneaker_v2(c2, foot_x=26, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c2, foot_x=38, foot_y=63, pose="flat", is_far=False)
    draw_leg_v2(c2, hip_x=28, hip_y=52, foot_x=26, foot_y=57, is_far=True)
    draw_leg_v2(c2, hip_x=36, hip_y=52, foot_x=38, foot_y=57, is_far=False)
    draw_shorts_v2(c2, sx=32, sy=45, w=18, h=9)
    draw_hoodie_v2(c2, tx=32, ty=31, w=20, h=15)
    draw_arm_v2(c2, shoulder_x=24, shoulder_y=33, hand_x=22, hand_y=42, is_far=True)
    draw_arm_v2(c2, shoulder_x=40, shoulder_y=33, hand_x=42, hand_y=42, is_far=False)
    draw_head_v2(c2, hx=32, hy=23, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c2.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c2)

    # ---------------- Frame 3: Settled Stance ----------------
    c3 = create_base_canvas()
    draw_sneaker_v2(c3, foot_x=26, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c3, foot_x=38, foot_y=63, pose="flat", is_far=False)
    draw_leg_v2(c3, hip_x=28, hip_y=52, foot_x=26, foot_y=57, is_far=True)
    draw_leg_v2(c3, hip_x=36, hip_y=52, foot_x=38, foot_y=57, is_far=False)
    draw_shorts_v2(c3, sx=32, sy=45, w=18, h=9)
    draw_hoodie_v2(c3, tx=32, ty=31, w=20, h=15)
    draw_arm_v2(c3, shoulder_x=24, shoulder_y=33, hand_x=22, hand_y=42, is_far=True)
    draw_arm_v2(c3, shoulder_x=40, shoulder_y=33, hand_x=42, hand_y=42, is_far=False)
    draw_head_v2(c3, hx=32, hy=22, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c3.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c3)

    return frames


def generate_p1_trip() -> List[PixelCanvas]:
    """
    14 frames, 20 fps, loop: false.
    Comedy slapstick stumble sequence:
    0: Toe catch at y=63
    1: Stumble forward, arms begin windmilling
    2: Windmilling panic, body tilting forward
    3: Hang time / Superman dive, trailing toe touches row 63
    4: Slide-faceplant impact with dust puffs at y=63 (Flat held 1)
    5: Sprawled flat on floor (Flat held 2)
    6: Elastic comic butt-bounce (hips pop up, feet/face stay anchored on row 63)
    7: Settles flat, cartoon dizzy stars orbit head
    8: Dizzy wobble, hands plant on floor at y=63 pushing chest up
    9: Pushes up higher on hands and knees
    10: Kneeling, shakes head vigorously to clear dizziness
    11: Shakes off last daze, pulls foot onto y=63
    12: Stands up, dusting off hoodie sleeves
    13: Upright with confident smirk ("I meant to do that!"), sneakers flat on y=63.
    """
    frames = []

    # ---------------- Frame 0: Toe Caught! ----------------
    c0 = create_base_canvas()
    draw_sneaker_v2(c0, foot_x=46, foot_y=63, pose="flat", is_far=False) # stuck foot
    draw_sneaker_v2(c0, foot_x=24, foot_y=57, pose="toe_point", is_far=True) # back foot flying
    draw_leg_v2(c0, hip_x=32, hip_y=48, foot_x=24, foot_y=53, is_far=True)
    draw_leg_v2(c0, hip_x=38, hip_y=48, foot_x=46, foot_y=57, is_far=False)
    draw_shorts_v2(c0, sx=35, sy=43, w=18, h=9)
    draw_hoodie_v2(c0, tx=36, ty=29, w=20, h=15)
    draw_arm_v2(c0, shoulder_x=28, shoulder_y=31, hand_x=20, hand_y=24, is_far=True)
    draw_arm_v2(c0, shoulder_x=44, shoulder_y=31, hand_x=52, hand_y=26, is_far=False)
    draw_head_v2(c0, hx=39, hy=20, eye_state="wide", look_dir="forward", mouth="o", eyebrow="raised")
    assert any(c0.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c0)

    # ---------------- Frame 1: Stumble Forward ----------------
    c1 = create_base_canvas()
    draw_sneaker_v2(c1, foot_x=40, foot_y=63, pose="toe_push", is_far=False)
    draw_sneaker_v2(c1, foot_x=18, foot_y=53, pose="toe_point", is_far=True)
    draw_leg_v2(c1, hip_x=33, hip_y=47, foot_x=18, foot_y=49, is_far=True)
    draw_leg_v2(c1, hip_x=38, hip_y=47, foot_x=40, foot_y=57, is_far=False)
    draw_shorts_v2(c1, sx=36, sy=43, w=18, h=8)
    draw_hoodie_v2(c1, tx=39, ty=30, w=20, h=14)
    # Windmilling arms
    draw_arm_v2(c1, shoulder_x=31, shoulder_y=32, hand_x=22, hand_y=20, is_far=True)
    draw_arm_v2(c1, shoulder_x=47, shoulder_y=32, hand_x=56, hand_y=42, is_far=False)
    draw_head_v2(c1, hx=44, hy=22, eye_state="wide", look_dir="down", mouth="open", eyebrow="worried")
    assert any(c1.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c1)

    # ---------------- Frame 2: Windmill Panic ----------------
    c2 = create_base_canvas()
    draw_sneaker_v2(c2, foot_x=34, foot_y=63, pose="toe_push", is_far=False)
    draw_sneaker_v2(c2, foot_x=14, foot_y=50, pose="toe_point", is_far=True)
    draw_leg_v2(c2, hip_x=32, hip_y=48, foot_x=14, foot_y=46, is_far=True)
    draw_leg_v2(c2, hip_x=36, hip_y=48, foot_x=34, foot_y=57, is_far=False)
    draw_shorts_v2(c2, sx=36, sy=45, w=18, h=8)
    draw_hoodie_v2(c2, tx=41, ty=34, w=20, h=13)
    draw_arm_v2(c2, shoulder_x=33, shoulder_y=36, hand_x=24, hand_y=46, is_far=True)
    draw_arm_v2(c2, shoulder_x=49, shoulder_y=36, hand_x=58, hand_y=22, is_far=False)
    draw_head_v2(c2, hx=48, hy=27, eye_state="wide", look_dir="down", mouth="open", eyebrow="worried")
    assert any(c2.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c2)

    # ---------------- Frame 3: Hang Time / Superman Dive ----------------
    c3 = create_base_canvas()
    # Body horizontal in mid-air, trailing toe brushes row 63!
    draw_sneaker_v2(c3, foot_x=12, foot_y=56, pose="flat", is_far=True)
    draw_sneaker_v2(c3, foot_x=22, foot_y=63, pose="toe_point", is_far=False)
    draw_leg_v2(c3, hip_x=28, hip_y=52, foot_x=12, foot_y=54, is_far=True)
    draw_leg_v2(c3, hip_x=30, hip_y=52, foot_x=22, foot_y=59, is_far=False)
    draw_shorts_v2(c3, sx=32, sy=48, w=16, h=8)
    draw_hoodie_v2(c3, tx=40, ty=44, w=18, h=11)
    # Arms reaching forward anticipating crash
    draw_arm_v2(c3, shoulder_x=42, shoulder_y=46, hand_x=54, hand_y=46, is_far=False)
    draw_head_v2(c3, hx=50, hy=40, eye_state="oof", look_dir="forward", mouth="oof")
    assert any(c3.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c3)

    # ---------------- Frame 4: Slide-Faceplant (Flat Held 1) ----------------
    c4 = create_base_canvas()
    # Body squished flat along rows 58..63
    draw_sneaker_v2(c4, foot_x=12, foot_y=63, pose="trip_flat", is_far=False)
    # Shorts flat
    for y in range(57, 64):
        for x in range(20, 30):
            c4.set_pixel(x, y, BLUE_SHADOW if y == 63 else BLUE_MID)
    # Hoodie flat
    for y in range(57, 64):
        for x in range(30, 44):
            c4.set_pixel(x, y, RED_SHADOW if y == 63 else (RED_LIGHT if y == 57 else RED_MID))
    # Limp arms splayed on floor
    c4.line(32, 63, 26, 63, SKIN_MID)
    c4.line(42, 63, 48, 63, SKIN_MID)
    # Face flat on floor
    draw_head_v2(c4, hx=50, hy=52, eye_state="oof", look_dir="forward", mouth="grimace")
    # Comic dust poofs at floor impact
    c4.set_pixel(6, 63, WHITE_SHADOW)
    c4.set_pixel(58, 63, WHITE_SHADOW)
    c4.set_pixel(57, 62, PURE_WHITE)
    assert any(c4.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c4)

    # ---------------- Frame 5: Sprawled Flat (Flat Held 2) ----------------
    c5 = c4.clone()
    frames.append(c5)

    # ---------------- Frame 6: Elastic Comic Butt Bounce ----------------
    c6 = create_base_canvas()
    draw_sneaker_v2(c6, foot_x=12, foot_y=63, pose="trip_flat", is_far=False)
    # Hips pop up 3px, feet & head remain on floor!
    for y in range(53, 60):
        for x in range(20, 30):
            c6.set_pixel(x, y, BLUE_SHADOW if y == 59 else BLUE_MID)
    for y in range(54, 61):
        for x in range(30, 42):
            c6.set_pixel(x, y, RED_SHADOW if y == 60 else RED_MID)
    c6.set_pixel(26, 63, OUTLINE) # anchor contact
    draw_head_v2(c6, hx=50, hy=52, eye_state="oof", look_dir="forward", mouth="grimace")
    assert any(c6.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c6)

    # ---------------- Frame 7: Settles Flat + Dizzy Stars ----------------
    c7 = c4.clone()
    # 3 cartoon dizzy stars orbiting head!
    c7.set_pixel(48, 42, YELLOW_LIGHT)
    c7.set_pixel(50, 43, YELLOW_MID)
    c7.set_pixel(56, 40, YELLOW_LIGHT)
    c7.set_pixel(54, 41, YELLOW_MID)
    c7.set_pixel(44, 45, YELLOW_LIGHT)
    frames.append(c7)

    # ---------------- Frame 8: Hands Push Off Floor (Dizzy) ----------------
    c8 = create_base_canvas()
    draw_sneaker_v2(c8, foot_x=16, foot_y=63, pose="flat", is_far=False)
    draw_shorts_v2(c8, sx=26, sy=53, w=16, h=8)
    draw_hoodie_v2(c8, tx=36, ty=43, w=18, h=13)
    # Hands planted on ground pushing up at y=63
    c8.line(34, 45, 34, 62, RED_LIGHT)
    c8.set_pixel(34, 63, SKIN_LIGHT)
    c8.line(42, 45, 44, 62, RED_LIGHT)
    c8.set_pixel(44, 63, SKIN_LIGHT)
    draw_head_v2(c8, hx=46, hy=34, eye_state="dizzy", look_dir="forward", mouth="grimace")
    assert any(c8.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c8)

    # ---------------- Frame 9: Pushes Higher on Knees ----------------
    c9 = create_base_canvas()
    draw_sneaker_v2(c9, foot_x=20, foot_y=63, pose="flat", is_far=False)
    draw_shorts_v2(c9, sx=28, sy=50, w=16, h=8)
    draw_hoodie_v2(c9, tx=34, ty=38, w=18, h=14)
    draw_arm_v2(c9, shoulder_x=28, shoulder_y=40, hand_x=28, hand_y=62, is_far=True)
    c9.set_pixel(28, 63, SKIN_LIGHT)
    draw_arm_v2(c9, shoulder_x=40, shoulder_y=40, hand_x=42, hand_y=62, is_far=False)
    c9.set_pixel(42, 63, SKIN_LIGHT)
    draw_head_v2(c9, hx=38, hy=28, eye_state="dizzy", look_dir="forward", mouth="grimace")
    assert any(c9.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c9)

    # ---------------- Frame 10: Kneeling, Shaking Head ----------------
    c10 = create_base_canvas()
    draw_sneaker_v2(c10, foot_x=22, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c10, foot_x=30, foot_y=63, pose="flat", is_far=False)
    draw_shorts_v2(c10, sx=30, sy=48, w=16, h=8)
    draw_hoodie_v2(c10, tx=32, ty=35, w=18, h=14)
    draw_arm_v2(c10, shoulder_x=24, shoulder_y=37, hand_x=22, hand_y=47, is_far=True)
    draw_arm_v2(c10, shoulder_x=40, shoulder_y=37, hand_x=42, hand_y=47, is_far=False)
    # Head shaking (eyes closed)
    draw_head_v2(c10, hx=32, hy=26, eye_state="closed", look_dir="down", mouth="grimace", hair_bob=1)
    assert any(c10.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c10)

    # ---------------- Frame 11: Shakes Off Daze, Foot Pulled Up ----------------
    c11 = create_base_canvas()
    draw_sneaker_v2(c11, foot_x=24, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c11, foot_x=36, foot_y=63, pose="flat", is_far=False)
    draw_leg_v2(c11, hip_x=27, hip_y=53, foot_x=24, foot_y=57, is_far=True)
    draw_leg_v2(c11, hip_x=35, hip_y=53, foot_x=36, foot_y=57, is_far=False)
    draw_shorts_v2(c11, sx=31, sy=46, w=18, h=9)
    draw_hoodie_v2(c11, tx=31, ty=32, w=20, h=15)
    draw_arm_v2(c11, shoulder_x=23, shoulder_y=34, hand_x=22, hand_y=43, is_far=True)
    draw_arm_v2(c11, shoulder_x=39, shoulder_y=34, hand_x=41, hand_y=43, is_far=False)
    draw_head_v2(c11, hx=31, hy=23, eye_state="blink", look_dir="forward", mouth="smirk")
    assert any(c11.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c11)

    # ---------------- Frame 12: Stands, Dusting Sleeves ----------------
    c12 = create_base_canvas()
    draw_sneaker_v2(c12, foot_x=26, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c12, foot_x=38, foot_y=63, pose="flat", is_far=False)
    draw_leg_v2(c12, hip_x=28, hip_y=52, foot_x=26, foot_y=57, is_far=True)
    draw_leg_v2(c12, hip_x=36, hip_y=52, foot_x=38, foot_y=57, is_far=False)
    draw_shorts_v2(c12, sx=32, sy=45, w=18, h=9)
    draw_hoodie_v2(c12, tx=32, ty=31, w=20, h=15)
    # Brushing sleeve
    draw_arm_v2(c12, shoulder_x=24, shoulder_y=33, hand_x=36, hand_y=36, is_far=True)
    draw_arm_v2(c12, shoulder_x=40, shoulder_y=33, hand_x=36, hand_y=38, is_far=False)
    draw_head_v2(c12, hx=32, hy=22, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c12.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c12)

    # ---------------- Frame 13: Upright Confident Smirk! ----------------
    c13 = create_base_canvas()
    draw_sneaker_v2(c13, foot_x=26, foot_y=63, pose="flat", is_far=True)
    draw_sneaker_v2(c13, foot_x=38, foot_y=63, pose="flat", is_far=False)
    draw_leg_v2(c13, hip_x=28, hip_y=52, foot_x=26, foot_y=57, is_far=True)
    draw_leg_v2(c13, hip_x=36, hip_y=52, foot_x=38, foot_y=57, is_far=False)
    draw_shorts_v2(c13, sx=32, sy=45, w=18, h=9)
    draw_hoodie_v2(c13, tx=32, ty=31, w=20, h=15)
    # Wipes nose with sleeve in cocky defiance
    draw_arm_v2(c13, shoulder_x=24, shoulder_y=33, hand_x=22, hand_y=42, is_far=True)
    draw_arm_v2(c13, shoulder_x=40, shoulder_y=33, hand_x=36, hand_y=26, is_far=False)
    draw_head_v2(c13, hx=32, hy=22, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c13.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c13)

    return frames


def generate_p1_boost_jump() -> List[PixelCanvas]:
    """
    4 frames, 18 fps, loop: false.
    Cyan Feather boost leap:
    0: Power gather crouch with cyan aura ripples touching row 63
    1: Vertical rocket stretch with feather stream touching row 63
    2: Soaring falcon glide with glowing trails touching row 63
    3: Smooth glide crest with sparkles touching row 63
    """
    frames = []

    # ---------------- Frame 0: Gather Crouch + Feather Glow ----------------
    c0 = create_base_canvas()
    draw_sneaker_v2(c0, foot_x=22, foot_y=63, pose="squash", wing_fx=True, is_far=True)
    draw_sneaker_v2(c0, foot_x=42, foot_y=63, pose="squash", wing_fx=True, is_far=False)
    # Cyan/blue feather ripples on row 63
    c0.set_pixel(16, 63, BLUE_LIGHT)
    c0.set_pixel(48, 63, PURE_WHITE)
    c0.set_pixel(32, 63, TEAL_LIGHT)
    draw_leg_v2(c0, hip_x=26, hip_y=54, foot_x=22, foot_y=59, is_far=True)
    draw_leg_v2(c0, hip_x=38, hip_y=54, foot_x=42, foot_y=59, is_far=False)
    draw_shorts_v2(c0, sx=32, sy=48, w=22, h=8)
    draw_hoodie_v2(c0, tx=32, ty=36, w=22, h=14)
    draw_head_v2(c0, hx=32, hy=28, eye_state="normal", look_dir="up", mouth="smirk")
    assert any(c0.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c0)

    # ---------------- Frame 1: Vertical Rocket Stretch ----------------
    c1 = create_base_canvas()
    draw_sneaker_v2(c1, foot_x=28, foot_y=52, pose="toe_point", wing_fx=True, is_far=True)
    draw_sneaker_v2(c1, foot_x=36, foot_y=52, pose="toe_point", wing_fx=True, is_far=False)
    # Luminous feather light beam streaming down to row 63!
    c1.line(30, 53, 30, 63, BLUE_LIGHT)
    c1.line(32, 53, 32, 63, PURE_WHITE)
    c1.line(34, 53, 34, 63, BLUE_LIGHT)
    c1.set_pixel(28, 63, TEAL_LIGHT)
    c1.set_pixel(36, 63, TEAL_LIGHT)

    draw_leg_v2(c1, hip_x=29, hip_y=38, foot_x=28, foot_y=48, is_far=True)
    draw_leg_v2(c1, hip_x=35, hip_y=38, foot_x=36, foot_y=48, is_far=False)
    draw_shorts_v2(c1, sx=32, sy=32, w=16, h=9)
    draw_hoodie_v2(c1, tx=32, ty=18, w=18, h=15, folds=1)
    draw_arm_v2(c1, shoulder_x=24, shoulder_y=19, hand_x=22, hand_y=7, is_far=True)
    draw_arm_v2(c1, shoulder_x=40, shoulder_y=19, hand_x=42, hand_y=7, is_far=False)
    draw_head_v2(c1, hx=32, hy=10, eye_state="wide", look_dir="up", mouth="open")
    assert any(c1.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c1)

    # ---------------- Frame 2: Soaring Winged Glide ----------------
    c2 = create_base_canvas()
    draw_sneaker_v2(c2, foot_x=28, foot_y=52, pose="flat", wing_fx=True, is_far=True)
    draw_sneaker_v2(c2, foot_x=38, foot_y=48, pose="flat", wing_fx=True, is_far=False)
    # Glowing feather particles drifting down touching row 63
    c2.set_pixel(31, 56, BLUE_LIGHT)
    c2.set_pixel(32, 58, PURE_WHITE)
    c2.set_pixel(33, 61, BLUE_LIGHT)
    c2.set_pixel(32, 63, PURE_WHITE)

    draw_leg_v2(c2, hip_x=29, hip_y=38, foot_x=28, foot_y=47, is_far=True)
    draw_leg_v2(c2, hip_x=35, hip_y=38, foot_x=38, foot_y=43, is_far=False)
    draw_shorts_v2(c2, sx=32, sy=32, w=18, h=9)
    draw_hoodie_v2(c2, tx=32, ty=18, w=19, h=15)
    draw_arm_v2(c2, shoulder_x=24, shoulder_y=20, hand_x=12, hand_y=16, is_far=True)
    draw_arm_v2(c2, shoulder_x=40, shoulder_y=20, hand_x=52, hand_y=16, is_far=False)
    draw_head_v2(c2, hx=32, hy=11, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c2.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c2)

    # ---------------- Frame 3: Glide Crest ----------------
    c3 = create_base_canvas()
    # Trailing foot reaches row 63
    draw_sneaker_v2(c3, foot_x=28, foot_y=63, pose="toe_point", wing_fx=True, is_far=True)
    draw_sneaker_v2(c3, foot_x=38, foot_y=53, pose="flat", wing_fx=True, is_far=False)
    draw_leg_v2(c3, hip_x=29, hip_y=40, foot_x=28, foot_y=57, is_far=True)
    draw_leg_v2(c3, hip_x=35, hip_y=40, foot_x=38, foot_y=48, is_far=False)
    draw_shorts_v2(c3, sx=32, sy=34, w=18, h=9)
    draw_hoodie_v2(c3, tx=32, ty=20, w=19, h=15)
    draw_arm_v2(c3, shoulder_x=24, shoulder_y=22, hand_x=14, hand_y=18, is_far=True)
    draw_arm_v2(c3, shoulder_x=40, shoulder_y=22, hand_x=50, hand_y=18, is_far=False)
    draw_head_v2(c3, hx=32, hy=13, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c3.get_pixel(x, 63)[3] > 0 for x in range(64))
    frames.append(c3)

    return frames


def generate_p1_celebrate() -> List[PixelCanvas]:
    """
    8 frames, 10 fps, loop: true.
    Joyful victory fist-pump dance loop!
    Right fist punching the sky, rhythmic bouncing hops, ecstatic cheering mouth,
    wink on frame 5. Lowest foot pixel touches row y=63 in every frame!
    """
    frames = []
    hops = [0, -2, -4, -1, 0, -2, -3, 0]
    fist_ys = [28, 20, 14, 22, 26, 18, 16, 26]

    for i in range(8):
        c = create_base_canvas()
        hop = hops[i]
        fist_y = fist_ys[i]

        # Sneaker touches row 63
        if hop <= -2:
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="toe_point", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=56 + hop, pose="flat", is_far=False)
        else:
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="flat", is_far=False)

        draw_leg_v2(c, hip_x=28, hip_y=52 + hop, foot_x=26, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=52 + hop, foot_x=38, foot_y=57 + (0 if hop > -2 else hop), is_far=False)
        draw_shorts_v2(c, sx=32, sy=45 + hop, w=18, h=9)

        # Far arm on hip
        draw_arm_v2(c, shoulder_x=24, shoulder_y=33 + hop, hand_x=22, hand_y=42 + hop, is_far=True, fist=True)

        draw_hoodie_v2(c, tx=32, ty=31 + hop, w=20, h=15)

        # Near arm punching the sky!
        draw_arm_v2(c, shoulder_x=40, shoulder_y=33 + hop, hand_x=44, hand_y=fist_y + hop, is_far=False, fist=True)

        # Head cheering / winking
        eye = "wink" if i == 5 else ("wide" if i in [2, 6] else "normal")
        draw_head_v2(c, hx=32, hy=22 + hop, eye_state=eye, look_dir="up",
                     mouth="open" if i in [1, 2, 6] else "grin", eyebrow="raised")

        # Confetti / sparkle motes
        if i in [2, 3]:
            c.set_pixel(46, 8, YELLOW_LIGHT)
            c.set_pixel(47, 9, YELLOW_MID)
        elif i in [6, 7]:
            c.set_pixel(20, 10, BLUE_LIGHT)
            c.set_pixel(19, 11, TEAL_LIGHT)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_celebrate frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_react_cheer() -> List[PixelCanvas]:
    """
    6 frames, 12 fps, loop: false.
    Power-up collected cheer!
    Leaps slightly in place with double fist pump ("V" victory), wide excited eyes,
    drawstrings sway, returns to eager ready stance. Feet touch row y=63.
    """
    frames = []
    hops = [0, -1, -3, -2, -1, 0]

    for i in range(6):
        c = create_base_canvas()
        hop = hops[i]

        if hop <= -2:
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="toe_point", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="toe_push", is_far=False)
        else:
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="flat", is_far=False)

        draw_leg_v2(c, hip_x=28, hip_y=52 + hop, foot_x=26, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=52 + hop, foot_x=38, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=32, sy=45 + hop, w=18, h=9)

        # Both arms raised in "V" celebration
        draw_arm_v2(c, shoulder_x=24, shoulder_y=33 + hop, hand_x=18, hand_y=16 + hop, is_far=True, fist=True)
        draw_hoodie_v2(c, tx=32, ty=31 + hop, w=20, h=15, drawstring_wind=1)
        draw_arm_v2(c, shoulder_x=40, shoulder_y=33 + hop, hand_x=46, hand_y=16 + hop, is_far=False, fist=True)

        draw_head_v2(c, hx=32, hy=22 + hop, eye_state="wide", look_dir="up",
                     mouth="open", eyebrow="raised")

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_react_cheer frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_react_shield() -> List[PixelCanvas]:
    """
    6 frames, 14 fps, loop: false.
    Flinches / nearly tripped!
    Skids back, raises both arms defensively across face/chest in shielding guard,
    knees bent, wide shocked eyes, then relaxes with relief. Sneakers on row y=63.
    """
    frames = []

    for i in range(6):
        c = create_base_canvas()

        # Skidding crouch
        draw_sneaker_v2(c, foot_x=24, foot_y=63, pose="heel_strike", is_far=True)
        draw_sneaker_v2(c, foot_x=40, foot_y=63, pose="flat", is_far=False)

        draw_leg_v2(c, hip_x=26, hip_y=53, foot_x=24, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=53, foot_x=40, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=31, sy=47, w=18, h=8)
        draw_hoodie_v2(c, tx=31, ty=33, w=20, h=14)

        # Arms crossed in front of face shielding!
        if i in [1, 2, 3]:
            draw_arm_v2(c, shoulder_x=23, shoulder_y=34, hand_x=34, hand_y=24, is_far=True, fist=True)
            draw_arm_v2(c, shoulder_x=39, shoulder_y=34, hand_x=32, hand_y=26, is_far=False, fist=True)
            draw_head_v2(c, hx=31, hy=24, eye_state="oof", look_dir="forward", mouth="grimace", eyebrow="worried")
        else:
            draw_arm_v2(c, shoulder_x=23, shoulder_y=34, hand_x=28, hand_y=36, is_far=True)
            draw_arm_v2(c, shoulder_x=39, shoulder_y=34, hand_x=36, hand_y=36, is_far=False)
            draw_head_v2(c, hx=31, hy=23, eye_state="wide", look_dir="forward", mouth="o", eyebrow="worried")

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_react_shield frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_react_scared() -> List[PixelCanvas]:
    """
    6 frames, 12 fps, loop: false.
    Looks down a pit:
    Teeters on edge, body leaning forward, windmilling arms backward for balance,
    eyes wide trembling looking straight down into abyss, sweat drop. Feet on row y=63.
    """
    frames = []

    for i in range(6):
        c = create_base_canvas()

        # Teetering on front toe
        draw_sneaker_v2(c, foot_x=22, foot_y=63, pose="toe_point", is_far=True)
        draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="heel_strike", is_far=False)

        draw_leg_v2(c, hip_x=26, hip_y=51, foot_x=22, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=35, hip_y=51, foot_x=38, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=32, sy=45, w=18, h=9)

        # Windmilling arms backward
        draw_arm_v2(c, shoulder_x=25, shoulder_y=33, hand_x=14, hand_y=28 + (i % 2) * 4, is_far=True)
        draw_hoodie_v2(c, tx=33, ty=31, w=20, h=15, folds=1)
        draw_arm_v2(c, shoulder_x=41, shoulder_y=33, hand_x=50, hand_y=32 - (i % 2) * 4, is_far=False)

        # Wide scared eyes looking down, sweat drop!
        draw_head_v2(c, hx=35, hy=22, eye_state="wide", look_dir="down",
                     mouth="o", eyebrow="worried", sweat=True)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_react_scared frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


def generate_p1_react_angry() -> List[PixelCanvas]:
    """
    8 frames, 14 fps, loop: false.
    Shakes fist at hand after trip:
    Turns upward, stomps foot on row y=63, furrows angry brows, clenches fist
    and shakes it furiously upward with red cheek flush and shouting mouth!
    """
    frames = []
    shake_ys = [14, 18, 14, 18, 14, 18, 16, 20]

    for i in range(8):
        c = create_base_canvas()
        sy = shake_ys[i]

        # Stomping foot on y=63
        if i in [1, 4]:
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="squash", is_far=False)
        else:
            draw_sneaker_v2(c, foot_x=26, foot_y=63, pose="flat", is_far=True)
            draw_sneaker_v2(c, foot_x=38, foot_y=63, pose="flat", is_far=False)

        draw_leg_v2(c, hip_x=28, hip_y=52, foot_x=26, foot_y=57, is_far=True)
        draw_leg_v2(c, hip_x=36, hip_y=52, foot_x=38, foot_y=57, is_far=False)
        draw_shorts_v2(c, sx=32, sy=45, w=18, h=9)

        # Left hand on hip clenched in fist
        draw_arm_v2(c, shoulder_x=24, shoulder_y=33, hand_x=20, hand_y=42, is_far=True, fist=True)
        draw_hoodie_v2(c, tx=32, ty=31, w=20, h=15)

        # Right fist shaking furiously upward at Player 2!
        draw_arm_v2(c, shoulder_x=40, shoulder_y=33, hand_x=44, hand_y=sy, is_far=False, fist=True)

        # Angry expression, shouting mouth, eyebrows angled down
        draw_head_v2(c, hx=32, hy=22, eye_state="normal", look_dir="up",
                     mouth="open", eyebrow="angry", blush=True)

        assert any(c.get_pixel(x, 63)[3] > 0 for x in range(64)), f"p1_react_angry frame {i} missing y=63 anchor!"
        frames.append(c)

    return frames


# =============================================================================
# 4 HUD PORTRAITS (64x64, 1 frame each)
# =============================================================================

def generate_portrait(mood: str) -> PixelCanvas:
    """
    Generates a 64x64 close-up HUD portrait of Player 1.
    Framed kid bust: hoodie collar with drawstrings, bunched hood,
    expressive head, hair, and mood-specific facial animation.
    Moods: 'happy', 'worried', 'tripped', 'angry'.
    """
    c = PixelCanvas(64, 64, TRANSPARENT)

    # 1. Subtle decorative framing / soft backdrop badge (circular)
    for y in range(6, 58):
        for x in range(6, 58):
            d_sq = (x - 32) ** 2 + (y - 32) ** 2
            if d_sq <= 25 * 25:
                # Circular portrait background
                if mood == "happy":
                    c.set_pixel(x, y, BLUE_DEEP if d_sq > 23 * 23 else SHADOW_PURPLE_DEEP)
                elif mood == "worried":
                    c.set_pixel(x, y, PURPLE_DARK if d_sq > 23 * 23 else SHADOW_PURPLE_DEEP)
                elif mood == "tripped":
                    c.set_pixel(x, y, BROWN_DARK if d_sq > 23 * 23 else SHADOW_PURPLE_DEEP)
                else: # angry
                    c.set_pixel(x, y, RED_DEEP if d_sq > 23 * 23 else SHADOW_PURPLE_DEEP)

    # 2. Hoodie Bust (lower half of portrait, y=42..63)
    for y in range(42, 64):
        for x in range(12, 53):
            rel_x = x - 32
            if y >= 45 and (x <= 14 or x >= 51):
                continue
            if rel_x <= -8:
                c.set_pixel(x, y, RED_LIGHT)
            elif rel_x >= 8:
                c.set_pixel(x, y, RED_SHADOW)
            else:
                c.set_pixel(x, y, RED_MID)

    # Collar & drawstrings
    c.line(26, 44, 26, 56, PURE_WHITE)
    c.line(27, 44, 27, 56, WHITE_SHADOW)
    c.set_pixel(26, 57, METAL_MID)
    c.line(38, 44, 38, 57, PURE_WHITE)
    c.line(39, 44, 39, 57, WHITE_SHADOW)
    c.set_pixel(38, 58, METAL_MID)

    # Bunched hood behind neck
    for y in range(36, 46):
        c.set_pixel(16, y, OUTLINE)
        c.set_pixel(17, y, RED_HIGHLIGHT)
        c.set_pixel(18, y, RED_LIGHT)
        c.set_pixel(19, y, RED_MID)

    # 3. Head & Face close-up centered around (hx=32, hy=30)
    if mood == "happy":
        draw_head_v2(c, hx=32, hy=30, eye_state="normal", look_dir="forward",
                     mouth="smirk", eyebrow="normal", blush=True)
    elif mood == "worried":
        draw_head_v2(c, hx=32, hy=30, eye_state="normal", look_dir="up",
                     mouth="pout", eyebrow="worried", sweat=True)
    elif mood == "tripped":
        draw_head_v2(c, hx=32, hy=30, eye_state="dizzy", look_dir="forward",
                     mouth="grimace", eyebrow="furrowed")
        # Band-aid on cheek!
        c.line(40, 32, 44, 34, WOOD_HIGHLIGHT)
        c.set_pixel(42, 33, PURE_WHITE) # gauze center
        # Dizzy star near temple
        c.set_pixel(46, 20, YELLOW_LIGHT)
        c.set_pixel(47, 21, YELLOW_MID)
        c.set_pixel(45, 21, YELLOW_MID)
    elif mood == "angry":
        draw_head_v2(c, hx=32, hy=30, eye_state="normal", look_dir="forward",
                     mouth="open", eyebrow="angry", blush=True)
        # Anger temple pop vein (#)
        c.set_pixel(44, 18, RED_MID)
        c.set_pixel(46, 18, RED_MID)
        c.line(43, 19, 47, 19, RED_MID)
        c.set_pixel(44, 20, RED_MID)
        c.set_pixel(46, 20, RED_MID)

    return c


# =============================================================================
# MAIN BUILDER & NORMAL MAP PIPELINE
# =============================================================================

def build_all(output_dir: str = "art/v2"):
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"=== Generating Player 1 v2 Sheets into {out_path} ===")

    # Specifications dictionary: filename -> (generator_func, frame_w, frame_h, fps, loop)
    specs = {
        "p1_idle.png": (generate_p1_idle, 64, 64, 8, True),
        "p1_idle_yawn.png": (generate_p1_idle_yawn, 64, 64, 6, False),
        "p1_idle_stretch.png": (generate_p1_idle_stretch, 64, 64, 6, False),
        "p1_idle_bounce.png": (generate_p1_idle_bounce, 64, 64, 10, True),
        "p1_wait.png": (generate_p1_wait, 64, 64, 10, True),
        "p1_wait_point.png": (generate_p1_wait_point, 64, 64, 8, False),
        "p1_run.png": (generate_p1_run, 64, 64, 20, True),
        "p1_run_fast.png": (generate_p1_run_fast, 64, 64, 24, True),
        "p1_jump_up.png": (generate_p1_jump_up, 64, 64, 16, False),
        "p1_jump_apex.png": (generate_p1_jump_apex, 64, 64, 12, False),
        "p1_fall.png": (generate_p1_fall, 64, 64, 16, True),
        "p1_land.png": (generate_p1_land, 64, 64, 20, False),
        "p1_trip.png": (generate_p1_trip, 64, 64, 20, False),
        "p1_boost_jump.png": (generate_p1_boost_jump, 64, 64, 18, False),
        "p1_celebrate.png": (generate_p1_celebrate, 64, 64, 10, True),
        "p1_react_cheer.png": (generate_p1_react_cheer, 64, 64, 12, False),
        "p1_react_shield.png": (generate_p1_react_shield, 64, 64, 14, False),
        "p1_react_scared.png": (generate_p1_react_scared, 64, 64, 12, False),
        "p1_react_angry.png": (generate_p1_react_angry, 64, 64, 14, False),
    }

    # Load existing manifest to update
    manifest_file = out_path / "manifest.json"
    manifest = {}
    if manifest_file.exists():
        with open(manifest_file, "r") as f:
            manifest = json.load(f)

    # 1. Generate Character Sprite Sheets
    cached_sheets = {}
    for filename, (gen_fn, fw, fh, fps, loop) in specs.items():
        frames = gen_fn()
        num_frames = len(frames)
        file_path = str(out_path / filename)

        # Check anchor rule on every frame
        for f_idx, fr in enumerate(frames):
            has_contact = any(fr.get_pixel(x, 63)[3] > 0 for x in range(64))
            assert has_contact, f"CRITICAL: {filename} frame {f_idx} fails y=63 foot anchor rule!"

        assemble_strip(frames, file_path)
        cached_sheets[filename] = frames

        manifest[filename] = {
            "frame_w": fw,
            "frame_h": fh,
            "frames": num_frames,
            "fps": fps,
            "loop": loop
        }

    # 2. Generate 4 HUD Portraits
    portraits = {
        "portrait_p1_happy.png": "happy",
        "portrait_p1_worried.png": "worried",
        "portrait_p1_tripped.png": "tripped",
        "portrait_p1_angry.png": "angry",
    }
    for p_filename, mood in portraits.items():
        p_frame = generate_portrait(mood)
        p_path = str(out_path / p_filename)
        assemble_strip([p_frame], p_path)
        manifest[p_filename] = {
            "frame_w": 64,
            "frame_h": 64,
            "frames": 1,
            "fps": 0,
            "loop": False
        }

    # 3. Generate Normal Maps: p1_idle_n.png and p1_run_n.png
    print("Generating tangent-space normal maps...")
    idle_frames = cached_sheets["p1_idle.png"]
    idle_n_frames = [generate_normal_map(f, strength=2.2) for f in idle_frames]
    assemble_strip(idle_n_frames, str(out_path / "p1_idle_n.png"))
    manifest["p1_idle_n.png"] = {
        "frame_w": 64,
        "frame_h": 64,
        "frames": len(idle_n_frames),
        "fps": 8,
        "loop": True
    }

    run_frames = cached_sheets["p1_run.png"]
    run_n_frames = [generate_normal_map(f, strength=2.2) for f in run_frames]
    assemble_strip(run_n_frames, str(out_path / "p1_run_n.png"))
    manifest["p1_run_n.png"] = {
        "frame_w": 64,
        "frame_h": 64,
        "frames": len(run_n_frames),
        "fps": 20,
        "loop": True
    }

    # 4. Save updated manifest.json
    with open(manifest_file, "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"Updated {manifest_file} with {len(manifest)} total entries.")

    # 5. Regenerate scripts/art_data.gd
    gen_art_script = Path("tools/gen_art_data.py")
    if gen_art_script.exists():
        import subprocess
        subprocess.run(["python3", str(gen_art_script)], check=True)
        print("Regenerated scripts/art_data.gd successfully.")


if __name__ == "__main__":
    build_all()
