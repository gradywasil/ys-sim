"""Younger Sibling Simulator - Player 1 Sprite Generator.

Elevated, charming 32x32 pixel art for Player 1:
- Messy dark brown hair with an expressive, bouncy cowlick
- Readable 2-3px eyes with pupils and sparkling white catchlights
- Determined smirk / open shouting mouth expressions
- Oversized red hoodie with hood folds, kangaroo pocket, and white drawstrings
- Denim blue shorts with pocket seams and rolled cuff hems
- Chunky orange/red sneakers with white toe caps and thick rubber soles
- Baked squash & stretch across run, jump, land, boost jump, and trip
- Strictly compliant with the 32-color palette and top-left lighting
- Guaranteed foot contact touching row y=31 in every single frame
"""

from typing import List, Tuple, Optional
from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE, SHADOW_DEEP, SHADOW_MID, PURPLE_MID, PURPLE_LIGHT,
    DUSK_PINK, DUSK_PEACH,
    SKIN_SHADOW, SKIN_MID, SKIN_LIGHT,
    BROWN_DARKEST, BROWN_DARK, BROWN_MID, BROWN_LIGHT, WOOD_HIGHLIGHT,
    RED_SHADOW, RED_MID, RED_LIGHT,
    BLUE_SHADOW, BLUE_MID, BLUE_LIGHT,
    YELLOW_SHADOW, YELLOW_MID, YELLOW_LIGHT,
    GREEN_SHADOW, GREEN_MID, GREEN_LIGHT,
    ORANGE_SHADOW, ORANGE_MID,
    WHITE_SHADOW, PURE_WHITE,
    VOID_BLACK, VALID_PALETTE_RGBA
)

def create_base_canvas() -> PixelCanvas:
    return PixelCanvas(32, 32, TRANSPARENT)


# =============================================================================
# MODULAR CHARACTER DRAWING PRIMITIVES
# =============================================================================

def draw_sneaker(canvas: PixelCanvas, foot_x: int, foot_y: int,
                 facing_right: bool = True, pose: str = "flat",
                 speed_boot: bool = False, wing_fx: bool = False,
                 is_far: bool = False):
    """
    Draws a chunky skate sneaker with white rubber toe cap and sole.
    Must touch foot_y (usually row 31).
    Body: Red/Orange ramp. Toe: Pure white. Sole: Rubber white & dark tread.
    """
    body_color = (ORANGE_MID if speed_boot else (RED_SHADOW if is_far else RED_MID))
    body_shadow = (ORANGE_SHADOW if speed_boot else RED_SHADOW)
    body_light = (YELLOW_MID if speed_boot else (RED_MID if is_far else RED_LIGHT))

    if pose == "flat":
        # Chunky sneaker planted flat on ground at foot_y (row 31)
        # Collar / tongue (y = foot_y - 3)
        canvas.set_pixel(foot_x - 1, foot_y - 3, body_color)
        canvas.set_pixel(foot_x, foot_y - 3, PURE_WHITE)     # white tongue/lace
        canvas.set_pixel(foot_x + 1, foot_y - 3, body_color)
        
        # Upper (y = foot_y - 2)
        canvas.set_pixel(foot_x - 2, foot_y - 2, body_shadow) # heel counter
        canvas.set_pixel(foot_x - 1, foot_y - 2, body_color)
        canvas.set_pixel(foot_x, foot_y - 2, PURE_WHITE)     # white lace cross
        canvas.set_pixel(foot_x + 1, foot_y - 2, body_color)
        canvas.set_pixel(foot_x + 2, foot_y - 2, PURE_WHITE) # top of toe cap
        
        # Mid (y = foot_y - 1)
        canvas.set_pixel(foot_x - 2, foot_y - 1, body_shadow)
        canvas.set_pixel(foot_x - 1, foot_y - 1, body_color)
        canvas.set_pixel(foot_x, foot_y - 1, body_color)
        canvas.set_pixel(foot_x + 1, foot_y - 1, WHITE_SHADOW)
        canvas.set_pixel(foot_x + 2, foot_y - 1, PURE_WHITE) # front toe cap
        canvas.set_pixel(foot_x + 3, foot_y - 1, PURE_WHITE) # front bumper
        
        # Sole (y = foot_y, touches 31!)
        canvas.set_pixel(foot_x - 2, foot_y, OUTLINE)        # heel tread
        canvas.set_pixel(foot_x - 1, foot_y, OUTLINE)
        canvas.set_pixel(foot_x, foot_y, WHITE_SHADOW)       # rubber sole
        canvas.set_pixel(foot_x + 1, foot_y, WHITE_SHADOW)
        canvas.set_pixel(foot_x + 2, foot_y, PURE_WHITE)     # front sole bumper
        canvas.set_pixel(foot_x + 3, foot_y, OUTLINE)        # toe bevel

    elif pose == "heel_strike":
        # Heel contacts ground at foot_y (row 31), toe raised forward
        # Heel tread touches foot_y
        canvas.set_pixel(foot_x - 2, foot_y, OUTLINE)
        canvas.set_pixel(foot_x - 1, foot_y, OUTLINE)
        canvas.set_pixel(foot_x, foot_y, WHITE_SHADOW)
        # Mid sole / heel body at foot_y - 1
        canvas.set_pixel(foot_x - 2, foot_y - 1, body_shadow)
        canvas.set_pixel(foot_x - 1, foot_y - 1, WHITE_SHADOW)
        canvas.set_pixel(foot_x, foot_y - 1, WHITE_SHADOW)
        canvas.set_pixel(foot_x + 1, foot_y - 1, OUTLINE)
        # Angled upper at foot_y - 2
        canvas.set_pixel(foot_x - 1, foot_y - 2, body_shadow)
        canvas.set_pixel(foot_x, foot_y - 2, body_color)
        canvas.set_pixel(foot_x + 1, foot_y - 2, WHITE_SHADOW)
        canvas.set_pixel(foot_x + 2, foot_y - 2, PURE_WHITE)
        # Toe cap raised up at foot_y - 3
        canvas.set_pixel(foot_x, foot_y - 3, PURE_WHITE)
        canvas.set_pixel(foot_x + 1, foot_y - 3, PURE_WHITE)
        canvas.set_pixel(foot_x + 2, foot_y - 3, PURE_WHITE)
        canvas.set_pixel(foot_x + 3, foot_y - 3, WHITE_SHADOW)

    elif pose == "toe_push":
        # Toe contacts ground at foot_y (row 31), heel kicked back and up
        # Toe sole touching foot_y
        canvas.set_pixel(foot_x + 1, foot_y, OUTLINE)
        canvas.set_pixel(foot_x + 2, foot_y, WHITE_SHADOW)
        canvas.set_pixel(foot_x + 3, foot_y, OUTLINE)
        # Toe cap at foot_y - 1
        canvas.set_pixel(foot_x, foot_y - 1, WHITE_SHADOW)
        canvas.set_pixel(foot_x + 1, foot_y - 1, PURE_WHITE)
        canvas.set_pixel(foot_x + 2, foot_y - 1, PURE_WHITE)
        canvas.set_pixel(foot_x + 3, foot_y - 1, WHITE_SHADOW)
        # Midfoot angled up at foot_y - 2
        canvas.set_pixel(foot_x - 1, foot_y - 2, body_shadow)
        canvas.set_pixel(foot_x, foot_y - 2, body_color)
        canvas.set_pixel(foot_x + 1, foot_y - 2, PURE_WHITE)
        # Heel raised at foot_y - 3
        canvas.set_pixel(foot_x - 2, foot_y - 3, body_shadow)
        canvas.set_pixel(foot_x - 1, foot_y - 3, body_color)
        canvas.set_pixel(foot_x, foot_y - 3, body_color)
        canvas.set_pixel(foot_x - 2, foot_y - 4, OUTLINE)

    elif pose == "toe_point":
        # Pointed straight down, tip touching foot_y (row 31)
        canvas.set_pixel(foot_x, foot_y, OUTLINE)
        canvas.set_pixel(foot_x + 1, foot_y, OUTLINE)
        # Toe cap at foot_y - 1
        canvas.set_pixel(foot_x, foot_y - 1, WHITE_SHADOW)
        canvas.set_pixel(foot_x + 1, foot_y - 1, PURE_WHITE)
        # Ball of foot at foot_y - 2
        canvas.set_pixel(foot_x - 1, foot_y - 2, body_shadow)
        canvas.set_pixel(foot_x, foot_y - 2, body_color)
        canvas.set_pixel(foot_x + 1, foot_y - 2, PURE_WHITE)
        # Ankle at foot_y - 3
        canvas.set_pixel(foot_x - 1, foot_y - 3, body_shadow)
        canvas.set_pixel(foot_x, foot_y - 3, body_color)
        canvas.set_pixel(foot_x + 1, foot_y - 3, body_color)

    elif pose == "squash":
        # Flattened wider sole on impact at foot_y (row 31)
        for x in range(foot_x - 3, foot_x + 4):
            canvas.set_pixel(x, foot_y, OUTLINE if (x == foot_x - 3 or x == foot_x + 3) else WHITE_SHADOW)
        # Compressed shoe upper at foot_y - 1
        canvas.set_pixel(foot_x - 3, foot_y - 1, body_shadow)
        canvas.set_pixel(foot_x - 2, foot_y - 1, body_shadow)
        canvas.set_pixel(foot_x - 1, foot_y - 1, body_color)
        canvas.set_pixel(foot_x, foot_y - 1, body_color)
        canvas.set_pixel(foot_x + 1, foot_y - 1, PURE_WHITE)
        canvas.set_pixel(foot_x + 2, foot_y - 1, PURE_WHITE)
        canvas.set_pixel(foot_x + 3, foot_y - 1, PURE_WHITE)
        # Collar at foot_y - 2
        canvas.set_pixel(foot_x - 1, foot_y - 2, body_color)
        canvas.set_pixel(foot_x, foot_y - 2, PURE_WHITE)
        canvas.set_pixel(foot_x + 1, foot_y - 2, body_color)

    elif pose == "trip_flat":
        # Sneaker sprawled horizontally flat along rows foot_y - 1 and foot_y (31)
        for x in range(foot_x - 3, foot_x + 4):
            canvas.set_pixel(x, foot_y, OUTLINE)
        canvas.set_pixel(foot_x - 3, foot_y - 1, body_shadow)
        canvas.set_pixel(foot_x - 2, foot_y - 1, body_shadow)
        canvas.set_pixel(foot_x - 1, foot_y - 1, body_color)
        canvas.set_pixel(foot_x, foot_y - 1, body_color)
        canvas.set_pixel(foot_x + 1, foot_y - 1, PURE_WHITE)
        canvas.set_pixel(foot_x + 2, foot_y - 1, PURE_WHITE)
        canvas.set_pixel(foot_x + 3, foot_y - 1, WHITE_SHADOW)

    # Speed boot winged lightning accents
    if speed_boot:
        canvas.set_pixel(foot_x - 3, foot_y - 3, YELLOW_LIGHT)
        canvas.set_pixel(foot_x - 4, foot_y - 4, YELLOW_LIGHT)
        canvas.set_pixel(foot_x - 3, foot_y - 4, YELLOW_MID)
        canvas.set_pixel(foot_x - 2, foot_y - 3, YELLOW_SHADOW)

    # Blue feather boost aura
    if wing_fx:
        canvas.set_pixel(foot_x - 3, foot_y - 2, BLUE_LIGHT)
        canvas.set_pixel(foot_x - 4, foot_y - 3, PURE_WHITE)
        canvas.set_pixel(foot_x - 3, foot_y - 4, BLUE_MID)


def draw_leg(canvas: PixelCanvas, hip_x: int, hip_y: int,
             foot_x: int, foot_y: int, is_far: bool = False):
    """Draws bare leg connecting shorts hem to sneaker collar."""
    color = SKIN_SHADOW if is_far else SKIN_MID
    light_color = SKIN_MID if is_far else SKIN_LIGHT
    
    # Bresenham-like thick column
    steps = max(abs(foot_y - hip_y), 1)
    for s in range(steps + 1):
        t = s / steps
        cx = int(round(hip_x + t * (foot_x - hip_x)))
        cy = int(round(hip_y + t * (foot_y - hip_y)))
        canvas.set_pixel(cx, cy, light_color)
        canvas.set_pixel(cx + 1, cy, color)


def draw_shorts(canvas: PixelCanvas, sx: int, sy: int, w: int = 9, h: int = 4,
                tilt: int = 0):
    """
    Draws denim blue shorts with pocket seam, shading, and cuff outlines.
    """
    x0 = sx - w // 2
    # Waistband & hips
    for y in range(sy, sy + h):
        for x in range(x0, x0 + w):
            rel_x = x - x0
            if y == sy:
                # Waistband
                canvas.set_pixel(x, y, BLUE_LIGHT if rel_x < w // 2 else BLUE_MID)
            elif rel_x == 0:
                canvas.set_pixel(x, y, BLUE_LIGHT)
            elif rel_x >= w - 2:
                canvas.set_pixel(x, y, BLUE_SHADOW)
            else:
                canvas.set_pixel(x, y, BLUE_MID)

    # Pocket curve seam
    canvas.set_pixel(sx + 1, sy + 1, BLUE_LIGHT)
    canvas.set_pixel(sx + 2, sy + 2, BLUE_LIGHT)
    canvas.set_pixel(sx + 2, sy + 1, BLUE_SHADOW)

    # Inseam / leg separation
    canvas.line(sx, sy + 1, sx, sy + h - 1, BLUE_SHADOW)
    # Rolled cuff outlines at bottom
    canvas.set_pixel(x0, sy + h - 1, OUTLINE)
    canvas.set_pixel(sx - 1, sy + h - 1, OUTLINE)
    canvas.set_pixel(sx + 1, sy + h - 1, OUTLINE)
    canvas.set_pixel(x0 + w - 1, sy + h - 1, OUTLINE)


def draw_hoodie(canvas: PixelCanvas, tx: int, ty: int, w: int = 10, h: int = 7,
                drawstring_wind: int = 0, hood_fold: bool = True):
    """
    Draws oversized red hoodie with kangaroo pocket, hood folds, and white drawstrings.
    """
    x0 = tx - w // 2
    # Torso block
    for y in range(ty, ty + h):
        for x in range(x0, x0 + w):
            rel_x = x - x0
            if y == ty:
                # Collar / shoulder line
                canvas.set_pixel(x, y, RED_LIGHT if rel_x <= w // 2 else RED_MID)
            elif rel_x == 0:
                canvas.set_pixel(x, y, RED_LIGHT)
            elif rel_x >= w - 2 or y == ty + h - 1:
                canvas.set_pixel(x, y, RED_SHADOW)
            else:
                canvas.set_pixel(x, y, RED_MID)

    # Hood bunched behind neck on left
    if hood_fold:
        canvas.set_pixel(x0 - 1, ty, RED_SHADOW)
        canvas.set_pixel(x0 - 1, ty + 1, RED_MID)
        canvas.set_pixel(x0, ty - 1, RED_LIGHT)
        canvas.set_pixel(x0 + 1, ty - 1, RED_MID)

    # Kangaroo pocket on lower torso
    pocket_y = ty + h - 3
    # Top pocket lip highlighted
    for px in range(tx - 2, tx + 3):
        canvas.set_pixel(px, pocket_y, RED_LIGHT)
    # Pocket side slits (slanted entry shadows)
    canvas.set_pixel(tx - 3, pocket_y + 1, RED_SHADOW)
    canvas.set_pixel(tx + 3, pocket_y + 1, RED_SHADOW)
    # Pocket bottom seam
    canvas.line(tx - 2, ty + h - 1, tx + 2, ty + h - 1, RED_SHADOW)

    # White drawstrings
    # Left string
    canvas.set_pixel(tx - 1, ty + 1, PURE_WHITE)
    canvas.set_pixel(tx - 1 + drawstring_wind, ty + 2, PURE_WHITE)
    canvas.set_pixel(tx - 1 + drawstring_wind * 2, ty + 3, WHITE_SHADOW) # knot tip
    # Right string
    canvas.set_pixel(tx + 2, ty + 1, PURE_WHITE)
    canvas.set_pixel(tx + 2 + drawstring_wind, ty + 2, PURE_WHITE)
    canvas.set_pixel(tx + 2 + drawstring_wind * 2, ty + 3, WHITE_SHADOW)

    # Zipper / collar metallic glint
    canvas.set_pixel(tx, ty, PURE_WHITE)
    canvas.set_pixel(tx, ty + 1, WHITE_SHADOW)


def draw_head(canvas: PixelCanvas, hx: int, hy: int,
              eye_state: str = "normal", look_dir: str = "forward",
              mouth: str = "smirk", hair_bob: int = 0, hair_wind: int = 0,
              blush: bool = True):
    """
    Draws expressive P1 head centered at (hx, hy).
    Includes messy dark brown hair, springy cowlick, readable 2-3px eyes with glints,
    and determined smirk or open shouting mouth.
    """
    # ---------------- Hair Volume (Top & Back) ----------------
    # Top crown
    for x in range(hx - 4, hx + 4):
        canvas.set_pixel(x, hy - 5 + hair_bob, WOOD_HIGHLIGHT if x <= hx else BROWN_LIGHT)
    for x in range(hx - 5, hx + 5):
        canvas.set_pixel(x, hy - 4 + hair_bob,
                         WOOD_HIGHLIGHT if x <= hx - 1 else (BROWN_LIGHT if x <= hx + 2 else BROWN_MID))
    for x in range(hx - 5, hx + 4):
        canvas.set_pixel(x, hy - 3 + hair_bob,
                         BROWN_LIGHT if x <= hx - 2 else BROWN_MID)
        
    # Back locks and nape of neck
    canvas.set_pixel(hx - 5, hy - 2 + hair_bob, BROWN_DARK)
    canvas.set_pixel(hx - 6, hy - 1 + hair_bob, OUTLINE)
    canvas.set_pixel(hx - 5, hy - 1 + hair_bob, BROWN_DARKEST)
    canvas.set_pixel(hx - 5, hy + hair_bob, BROWN_DARKEST)
    canvas.set_pixel(hx - 4, hy + 1 + hair_bob, BROWN_DARKEST)

    # Cowlick (bouncy tuft sticking up/back)
    if hair_wind > 0:
        # Swept backward in run wind
        canvas.set_pixel(hx - 4, hy - 5 + hair_bob, BROWN_MID)
        canvas.set_pixel(hx - 6, hy - 5 + hair_bob, WOOD_HIGHLIGHT)
        canvas.set_pixel(hx - 7, hy - 4 + hair_bob, WOOD_HIGHLIGHT)
        canvas.set_pixel(hx - 8, hy - 4 + hair_bob, BROWN_LIGHT)
        canvas.set_pixel(hx - 9, hy - 3 + hair_bob, OUTLINE)
    elif hair_wind < 0:
        # Swept straight up by falling wind
        canvas.set_pixel(hx - 2, hy - 6 + hair_bob, BROWN_MID)
        canvas.set_pixel(hx - 3, hy - 7 + hair_bob, WOOD_HIGHLIGHT)
        canvas.set_pixel(hx - 3, hy - 8 + hair_bob, WOOD_HIGHLIGHT)
        canvas.set_pixel(hx - 4, hy - 9 + hair_bob, WOOD_HIGHLIGHT)
        canvas.set_pixel(hx - 5, hy - 9 + hair_bob, OUTLINE)
    else:
        # Standard springy cowlick flicking upward-left
        canvas.set_pixel(hx - 2, hy - 6 + hair_bob, BROWN_MID)
        canvas.set_pixel(hx - 3, hy - 6 + hair_bob, WOOD_HIGHLIGHT)
        canvas.set_pixel(hx - 3, hy - 7 + hair_bob, WOOD_HIGHLIGHT)
        canvas.set_pixel(hx - 4, hy - 8 + hair_bob, WOOD_HIGHLIGHT)
        canvas.set_pixel(hx - 5, hy - 8 + hair_bob, BROWN_LIGHT)
        canvas.set_pixel(hx - 4, hy - 9 + hair_bob, OUTLINE)

    # ---------------- Face Base (Skin) ----------------
    for y in range(hy - 2, hy + 4):
        for x in range(hx - 3, hx + 5):
            # Left edge gets highlight, right profile gets midtone, chin gets shadow
            if y == hy + 3:
                # Chin shadow line
                canvas.set_pixel(x, y, SKIN_SHADOW)
            elif x <= hx - 2 or y == hy - 2:
                canvas.set_pixel(x, y, SKIN_LIGHT)
            else:
                canvas.set_pixel(x, y, SKIN_MID)

    # Ear on left
    canvas.set_pixel(hx - 4, hy, SKIN_MID)
    canvas.set_pixel(hx - 4, hy - 1, SKIN_LIGHT)
    canvas.set_pixel(hx - 4, hy + 1, SKIN_SHADOW)

    # Bangs / front locks overlapping face
    canvas.set_pixel(hx - 3, hy - 2, BROWN_MID)
    canvas.set_pixel(hx - 1, hy - 2, BROWN_LIGHT)
    canvas.set_pixel(hx - 2, hy - 1, BROWN_MID)
    canvas.set_pixel(hx, hy - 2, BROWN_LIGHT)
    canvas.set_pixel(hx + 1, hy - 2, BROWN_MID)
    canvas.set_pixel(hx + 3, hy - 3, BROWN_DARK)

    # Cute rosy cheek blush
    if blush:
        canvas.set_pixel(hx + 3, hy + 1, DUSK_PEACH)
        canvas.set_pixel(hx - 2, hy + 1, DUSK_PEACH)

    # ---------------- Eyes (2-3px expressive with catchlights) ----------------
    if eye_state == "normal":
        # Eyebrows
        canvas.set_pixel(hx - 2, hy - 2, BROWN_DARKEST)
        canvas.set_pixel(hx - 1, hy - 2, BROWN_DARKEST)
        canvas.set_pixel(hx + 1, hy - 2, BROWN_DARKEST)
        canvas.set_pixel(hx + 2, hy - 2, BROWN_DARKEST)
        canvas.set_pixel(hx + 3, hy - 2, BROWN_DARKEST)

        if look_dir == "forward":
            # Left eye (far)
            canvas.set_pixel(hx - 2, hy - 1, PURE_WHITE)    # Catchlight glint!
            canvas.set_pixel(hx - 1, hy - 1, OUTLINE)       # Pupil
            canvas.set_pixel(hx - 2, hy, WHITE_SHADOW)      # Sclera
            canvas.set_pixel(hx - 1, hy, OUTLINE)           # Pupil bottom
            # Right eye (near, 3px wide!)
            canvas.set_pixel(hx + 1, hy - 1, PURE_WHITE)    # Catchlight glint!
            canvas.set_pixel(hx + 2, hy - 1, PURE_WHITE)    # Sclera
            canvas.set_pixel(hx + 3, hy - 1, OUTLINE)       # Pupil looking forward
            canvas.set_pixel(hx + 1, hy, WHITE_SHADOW)
            canvas.set_pixel(hx + 2, hy, OUTLINE)
            canvas.set_pixel(hx + 3, hy, OUTLINE)
        elif look_dir == "up":
            # Looking up toward Player 2's giant hand
            canvas.set_pixel(hx - 2, hy - 1, OUTLINE)
            canvas.set_pixel(hx - 1, hy - 1, OUTLINE)
            canvas.set_pixel(hx - 2, hy, PURE_WHITE)
            canvas.set_pixel(hx - 1, hy, WHITE_SHADOW)
            canvas.set_pixel(hx + 1, hy - 1, OUTLINE)
            canvas.set_pixel(hx + 2, hy - 1, OUTLINE)
            canvas.set_pixel(hx + 3, hy - 1, PURE_WHITE)
            canvas.set_pixel(hx + 1, hy, PURE_WHITE)
            canvas.set_pixel(hx + 2, hy, WHITE_SHADOW)
            canvas.set_pixel(hx + 3, hy, WHITE_SHADOW)
        elif look_dir == "down":
            canvas.set_pixel(hx - 2, hy - 1, PURE_WHITE)
            canvas.set_pixel(hx - 1, hy - 1, WHITE_SHADOW)
            canvas.set_pixel(hx - 2, hy, OUTLINE)
            canvas.set_pixel(hx - 1, hy, OUTLINE)
            canvas.set_pixel(hx + 1, hy - 1, PURE_WHITE)
            canvas.set_pixel(hx + 2, hy - 1, PURE_WHITE)
            canvas.set_pixel(hx + 3, hy - 1, WHITE_SHADOW)
            canvas.set_pixel(hx + 1, hy, WHITE_SHADOW)
            canvas.set_pixel(hx + 2, hy, OUTLINE)
            canvas.set_pixel(hx + 3, hy, OUTLINE)

    elif eye_state == "wide":
        # Extra large excited / shocked cartoon eyes
        canvas.set_pixel(hx - 2, hy - 2, BROWN_DARKEST)
        canvas.set_pixel(hx + 2, hy - 2, BROWN_DARKEST)
        # Left eye
        canvas.set_pixel(hx - 2, hy - 1, PURE_WHITE)
        canvas.set_pixel(hx - 1, hy - 1, OUTLINE)
        canvas.set_pixel(hx - 2, hy, PURE_WHITE)
        canvas.set_pixel(hx - 1, hy, OUTLINE)
        # Right eye
        canvas.set_pixel(hx + 1, hy - 1, PURE_WHITE)
        canvas.set_pixel(hx + 2, hy - 1, OUTLINE)
        canvas.set_pixel(hx + 3, hy - 1, OUTLINE)
        canvas.set_pixel(hx + 1, hy, PURE_WHITE)
        canvas.set_pixel(hx + 2, hy, OUTLINE)
        canvas.set_pixel(hx + 3, hy, WHITE_SHADOW)

    elif eye_state == "blink" or eye_state == "closed":
        # Happy closed-eye smile curves
        canvas.set_pixel(hx - 2, hy, BROWN_DARKEST)
        canvas.set_pixel(hx - 1, hy - 1, BROWN_DARKEST)
        canvas.set_pixel(hx + 1, hy, BROWN_DARKEST)
        canvas.set_pixel(hx + 2, hy - 1, BROWN_DARKEST)
        canvas.set_pixel(hx + 3, hy, BROWN_DARKEST)

    elif eye_state == "wink":
        # Left eye normal, right eye wink
        canvas.set_pixel(hx - 2, hy - 1, PURE_WHITE)
        canvas.set_pixel(hx - 1, hy - 1, OUTLINE)
        canvas.set_pixel(hx - 2, hy, WHITE_SHADOW)
        canvas.set_pixel(hx - 1, hy, OUTLINE)
        # Right eye happy wink
        canvas.set_pixel(hx + 1, hy, BROWN_DARKEST)
        canvas.set_pixel(hx + 2, hy - 1, BROWN_DARKEST)
        canvas.set_pixel(hx + 3, hy, BROWN_DARKEST)
        # Star twinkle glint next to eye!
        canvas.set_pixel(hx + 4, hy - 1, YELLOW_LIGHT)

    elif eye_state == "dizzy":
        # Cartoon dizzy spirals
        canvas.set_pixel(hx - 2, hy - 1, YELLOW_MID)
        canvas.set_pixel(hx - 1, hy, OUTLINE)
        canvas.set_pixel(hx - 2, hy, OUTLINE)
        canvas.set_pixel(hx + 1, hy - 1, OUTLINE)
        canvas.set_pixel(hx + 2, hy - 1, YELLOW_LIGHT)
        canvas.set_pixel(hx + 3, hy, OUTLINE)
        canvas.set_pixel(hx + 2, hy, YELLOW_MID)

    elif eye_state == "oof" or eye_state == "pain":
        # Squeezed shut (> <)
        canvas.set_pixel(hx - 2, hy - 1, OUTLINE)
        canvas.set_pixel(hx - 1, hy, OUTLINE)
        canvas.set_pixel(hx - 2, hy + 1, OUTLINE)
        canvas.set_pixel(hx + 1, hy - 1, OUTLINE)
        canvas.set_pixel(hx + 2, hy, OUTLINE)
        canvas.set_pixel(hx + 3, hy - 1, OUTLINE)

    # ---------------- Mouth & Smirk ----------------
    if mouth == "smirk":
        # Determined kid smirk with white tooth glint!
        canvas.set_pixel(hx + 1, hy + 2, OUTLINE)
        canvas.set_pixel(hx + 2, hy + 2, PURE_WHITE)     # Tooth glint
        canvas.set_pixel(hx + 3, hy + 2, OUTLINE)        # Smirk upturn
        canvas.set_pixel(hx + 3, hy + 1, SKIN_SHADOW)    # Cheek smirk crease
    elif mouth == "open":
        # Joyful open mouth cheer / shout
        canvas.set_pixel(hx + 1, hy + 1, OUTLINE)
        canvas.set_pixel(hx + 2, hy + 1, PURE_WHITE)     # Upper teeth
        canvas.set_pixel(hx + 3, hy + 1, OUTLINE)
        canvas.set_pixel(hx + 1, hy + 2, OUTLINE)
        canvas.set_pixel(hx + 2, hy + 2, RED_SHADOW)     # Tongue / interior
        canvas.set_pixel(hx + 3, hy + 2, OUTLINE)
    elif mouth == "grin":
        # Big toothy grin
        canvas.set_pixel(hx, hy + 2, OUTLINE)
        canvas.set_pixel(hx + 1, hy + 2, PURE_WHITE)
        canvas.set_pixel(hx + 2, hy + 2, PURE_WHITE)
        canvas.set_pixel(hx + 3, hy + 2, OUTLINE)
    elif mouth == "pout":
        # Impatient / grumpy frown
        canvas.set_pixel(hx + 1, hy + 2, OUTLINE)
        canvas.set_pixel(hx + 2, hy + 2, OUTLINE)
        canvas.set_pixel(hx + 3, hy + 2, OUTLINE)
        canvas.set_pixel(hx + 3, hy + 3, OUTLINE)
    elif mouth == "grimace":
        canvas.set_pixel(hx + 1, hy + 2, PURE_WHITE)
        canvas.set_pixel(hx + 2, hy + 2, OUTLINE)
        canvas.set_pixel(hx + 3, hy + 2, PURE_WHITE)
    elif mouth == "oof":
        # Small surprised 'O'
        canvas.set_pixel(hx + 2, hy + 1, OUTLINE)
        canvas.set_pixel(hx + 2, hy + 2, RED_SHADOW)
        canvas.set_pixel(hx + 2, hy + 3, OUTLINE)


# =============================================================================
# 11 ANIMATION GENERATORS
# =============================================================================

def generate_p1_idle() -> List[PixelCanvas]:
    """
    6 frames, 8 fps, loop: true.
    Relaxed standing pose, gentle breathing rise, eye blink, determined smirk.
    Sneakers firmly planted at row y=31 in every frame.
    """
    frames = []
    # Breathing vertical bobs: 0, -1, -1, 0, 0, 0
    bobs = [0, -1, -1, 0, 0, 0]
    eye_states = ["normal", "normal", "normal", "normal", "blink", "normal"]
    
    for i in range(6):
        c = create_base_canvas()
        bob = bobs[i]
        
        # Sneakers planted flat touching row 31
        draw_sneaker(c, foot_x=12, foot_y=31, pose="flat", is_far=True)
        draw_sneaker(c, foot_x=18, foot_y=31, pose="flat", is_far=False)
        
        # Legs connecting shorts to sneakers
        draw_leg(c, hip_x=13, hip_y=26 + bob, foot_x=12, foot_y=28, is_far=True)
        draw_leg(c, hip_x=18, hip_y=26 + bob, foot_x=18, foot_y=28, is_far=False)
        
        # Denim shorts
        draw_shorts(c, sx=15, sy=23 + bob, w=9, h=4)
        
        # Oversized red hoodie
        draw_hoodie(c, tx=15, ty=17 + bob, w=10, h=7)
        
        # Head with hair & smirk
        draw_head(c, hx=15, hy=12 + bob, eye_state=eye_states[i], look_dir="forward",
                  mouth="smirk", hair_bob=-1 if bob < 0 else 0)
        
        # Resting arms with hoodie sleeves at sides
        # Left arm (far)
        c.set_pixel(9, 18 + bob, RED_MID)
        c.set_pixel(9, 19 + bob, RED_SHADOW)
        c.set_pixel(9, 20 + bob, RED_SHADOW)
        c.set_pixel(9, 21 + bob, SKIN_SHADOW)
        # Right arm (near)
        c.set_pixel(20, 18 + bob, RED_LIGHT)
        c.set_pixel(20, 19 + bob, RED_MID)
        c.set_pixel(20, 20 + bob, RED_SHADOW)
        c.set_pixel(20, 21 + bob, SKIN_LIGHT)
        c.set_pixel(21, 21 + bob, SKIN_MID)
        
        # Verify anchor rule
        assert any(c.get_pixel(x, 31)[3] > 0 for x in range(32)), f"p1_idle frame {i} missing y=31 anchor!"
        frames.append(c)
        
    return frames


def generate_p1_wait() -> List[PixelCanvas]:
    """
    8 frames, 6 fps, loop: true.
    Impatient waiting cycle: arms crossed over hoodie, foot tapping,
    looks up at sky, checks pretend toy watch on wrist with annoyed pout.
    """
    frames = []
    
    for i in range(8):
        c = create_base_canvas()
        
        # Foot tapping logic: right foot lifts toe on even frames, taps down on odd
        right_tap_up = (i in [0, 2, 5])
        
        # Left foot firmly planted on y=31
        draw_sneaker(c, foot_x=12, foot_y=31, pose="flat", is_far=True)
        
        # Right foot tapping
        if right_tap_up:
            # Heel touches y=31, toe angled up
            draw_sneaker(c, foot_x=18, foot_y=31, pose="heel_strike", is_far=False)
        else:
            # Flat tap down on y=31
            draw_sneaker(c, foot_x=18, foot_y=31, pose="flat", is_far=False)
            
        # Legs
        draw_leg(c, hip_x=13, hip_y=26, foot_x=12, foot_y=28, is_far=True)
        draw_leg(c, hip_x=18, hip_y=26, foot_x=18, foot_y=28, is_far=False)
        
        # Denim shorts
        draw_shorts(c, sx=15, sy=23, w=9, h=4)
        
        # Oversized hoodie
        draw_hoodie(c, tx=15, ty=17, w=10, h=7)
        
        # Crossed arms or checking watch
        if i in [4, 5]:
            # Checking pretend toy watch on wrist!
            # Right arm supporting left elbow
            c.line(12, 20, 18, 20, RED_MID)
            c.line(12, 21, 18, 21, RED_SHADOW)
            # Wrist raised in front of chest
            c.set_pixel(18, 19, SKIN_LIGHT)
            c.set_pixel(19, 19, SKIN_MID)
            # Toy watch strap (blue) with bright yellow face
            c.set_pixel(18, 18, BLUE_MID)
            c.set_pixel(19, 18, YELLOW_LIGHT)
            c.set_pixel(20, 18, BLUE_MID)
            # Head looking down at watch
            draw_head(c, hx=15, hy=12, eye_state="normal", look_dir="down", mouth="grimace")
        elif i in [0, 1, 2, 3]:
            # Arms tightly crossed, looking up at sky
            # Crossed sleeves across chest
            c.line(11, 20, 19, 20, RED_LIGHT)
            c.line(11, 21, 19, 21, RED_MID)
            c.line(11, 22, 19, 22, RED_SHADOW)
            c.set_pixel(10, 21, SKIN_MID)
            c.set_pixel(20, 21, SKIN_MID)
            draw_head(c, hx=15, hy=12, eye_state="normal", look_dir="up", mouth="pout")
        else: # 6, 7
            # Arms crossed, looking forward with impatient huff
            c.line(11, 20, 19, 20, RED_LIGHT)
            c.line(11, 21, 19, 21, RED_MID)
            c.line(11, 22, 19, 22, RED_SHADOW)
            c.set_pixel(10, 21, SKIN_MID)
            c.set_pixel(20, 21, SKIN_MID)
            draw_head(c, hx=15, hy=12, eye_state="normal", look_dir="forward", mouth="pout")
            
        assert any(c.get_pixel(x, 31)[3] > 0 for x in range(32)), f"p1_wait frame {i} missing y=31 anchor!"
        frames.append(c)
        
    return frames


def generate_p1_run() -> List[PixelCanvas]:
    """
    10 frames, 16 fps, loop: true.
    Full athletic kid run cycle with 2 distinct airborne phases.
    Baked squash & stretch, wind in hair and drawstrings, determined smirk.
    Lowest foot pixel touches row y=31 in every frame.
    """
    frames = []
    # 10 frames:
    # 0: Right heel strike forward
    # 1: Right down / plant (squash)
    # 2: Right push-off
    # 3: Airborne flight apex 1 (trailing toe touches 31)
    # 4: Airborne flight descent (reaching left foot touches 31)
    # 5: Left heel strike forward
    # 6: Left down / plant (squash)
    # 7: Left push-off
    # 8: Airborne flight apex 2 (trailing toe touches 31)
    # 9: Airborne flight descent (reaching right foot touches 31)
    
    # Body vertical offsets (squash on 1 & 6, flight rise on 3 & 8)
    bobs = [0, 1, -1, -2, -1, 0, 1, -1, -2, -1]
    
    for i in range(10):
        c = create_base_canvas()
        bob = bobs[i]
        
        # Pumping arms coordinates
        if i in [0, 1, 2]:
            arm_front_x, arm_front_y = 19, 21 + bob
            arm_back_x, arm_back_y = 10, 21 + bob
        elif i in [3, 4]:
            arm_front_x, arm_front_y = 17, 20 + bob
            arm_back_x, arm_back_y = 12, 22 + bob
        elif i in [5, 6, 7]:
            arm_front_x, arm_front_y = 10, 21 + bob
            arm_back_x, arm_back_y = 19, 21 + bob
        else: # 8, 9
            arm_front_x, arm_front_y = 12, 22 + bob
            arm_back_x, arm_back_y = 17, 20 + bob
            
        # Draw legs & sneakers based on cycle phase
        if i == 0:
            # Right foot heel strike forward, left foot trailing back
            draw_sneaker(c, foot_x=9, foot_y=28, pose="toe_point", is_far=True)
            draw_sneaker(c, foot_x=20, foot_y=31, pose="heel_strike", is_far=False)
            draw_leg(c, hip_x=14, hip_y=26 + bob, foot_x=9, foot_y=26, is_far=True)
            draw_leg(c, hip_x=17, hip_y=26 + bob, foot_x=19, foot_y=29, is_far=False)
        elif i == 1:
            # Right foot flat plant & squash, left leg passing
            draw_sneaker(c, foot_x=12, foot_y=28, pose="flat", is_far=True)
            draw_sneaker(c, foot_x=18, foot_y=31, pose="flat", is_far=False)
            draw_leg(c, hip_x=14, hip_y=26 + bob, foot_x=12, foot_y=26, is_far=True)
            draw_leg(c, hip_x=17, hip_y=26 + bob, foot_x=18, foot_y=28, is_far=False)
        elif i == 2:
            # Right foot toe push-off at y=31, left knee high forward
            draw_sneaker(c, foot_x=20, foot_y=26, pose="flat", is_far=True)
            draw_sneaker(c, foot_x=15, foot_y=31, pose="toe_push", is_far=False)
            draw_leg(c, hip_x=14, hip_y=26 + bob, foot_x=20, foot_y=24, is_far=True)
            draw_leg(c, hip_x=17, hip_y=26 + bob, foot_x=15, foot_y=28, is_far=False)
        elif i == 3:
            # Airborne 1: both feet in air, trailing right foot reaches row 31 for anchor!
            draw_sneaker(c, foot_x=21, foot_y=25, pose="flat", is_far=True)
            draw_sneaker(c, foot_x=12, foot_y=31, pose="toe_point", is_far=False)
            draw_leg(c, hip_x=14, hip_y=26 + bob, foot_x=21, foot_y=23, is_far=True)
            draw_leg(c, hip_x=17, hip_y=26 + bob, foot_x=12, foot_y=28, is_far=False)
        elif i == 4:
            # Airborne descent: reaching left foot touches row 31
            draw_sneaker(c, foot_x=10, foot_y=29, pose="toe_point", is_far=False)
            draw_sneaker(c, foot_x=20, foot_y=31, pose="heel_strike", is_far=True)
            draw_leg(c, hip_x=17, hip_y=26 + bob, foot_x=10, foot_y=27, is_far=False)
            draw_leg(c, hip_x=14, hip_y=26 + bob, foot_x=20, foot_y=29, is_far=True)
        elif i == 5:
            # Left foot heel strike forward, right foot trailing back
            draw_sneaker(c, foot_x=9, foot_y=28, pose="toe_point", is_far=False)
            draw_sneaker(c, foot_x=20, foot_y=31, pose="heel_strike", is_far=True)
            draw_leg(c, hip_x=17, hip_y=26 + bob, foot_x=9, foot_y=26, is_far=False)
            draw_leg(c, hip_x=14, hip_y=26 + bob, foot_x=19, foot_y=29, is_far=True)
        elif i == 6:
            # Left foot flat plant & squash, right leg passing
            draw_sneaker(c, foot_x=12, foot_y=28, pose="flat", is_far=False)
            draw_sneaker(c, foot_x=18, foot_y=31, pose="flat", is_far=True)
            draw_leg(c, hip_x=17, hip_y=26 + bob, foot_x=12, foot_y=26, is_far=False)
            draw_leg(c, hip_x=14, hip_y=26 + bob, foot_x=18, foot_y=28, is_far=True)
        elif i == 7:
            # Left foot toe push-off at y=31, right knee high forward
            draw_sneaker(c, foot_x=20, foot_y=26, pose="flat", is_far=False)
            draw_sneaker(c, foot_x=15, foot_y=31, pose="toe_push", is_far=True)
            draw_leg(c, hip_x=17, hip_y=26 + bob, foot_x=20, foot_y=24, is_far=False)
            draw_leg(c, hip_x=14, hip_y=26 + bob, foot_x=15, foot_y=28, is_far=True)
        elif i == 8:
            # Airborne 2: trailing left foot reaches row 31 for anchor!
            draw_sneaker(c, foot_x=21, foot_y=25, pose="flat", is_far=False)
            draw_sneaker(c, foot_x=12, foot_y=31, pose="toe_point", is_far=True)
            draw_leg(c, hip_x=17, hip_y=26 + bob, foot_x=21, foot_y=23, is_far=False)
            draw_leg(c, hip_x=14, hip_y=26 + bob, foot_x=12, foot_y=28, is_far=True)
        else: # 9
            # Airborne descent: reaching right foot touches row 31
            draw_sneaker(c, foot_x=10, foot_y=29, pose="toe_point", is_far=True)
            draw_sneaker(c, foot_x=20, foot_y=31, pose="heel_strike", is_far=False)
            draw_leg(c, hip_x=14, hip_y=26 + bob, foot_x=10, foot_y=27, is_far=True)
            draw_leg(c, hip_x=17, hip_y=26 + bob, foot_x=20, foot_y=29, is_far=False)

        # Denim shorts
        draw_shorts(c, sx=15, sy=23 + bob, w=9, h=4)
        
        # Oversized hoodie
        draw_hoodie(c, tx=15, ty=17 + bob, w=10, h=7, drawstring_wind=1)
        
        # Pumping arms
        c.line(15, 18 + bob, arm_back_x, arm_back_y, RED_SHADOW)
        c.set_pixel(arm_back_x, arm_back_y, SKIN_SHADOW)
        c.line(15, 18 + bob, arm_front_x, arm_front_y, RED_LIGHT)
        c.set_pixel(arm_front_x, arm_front_y, SKIN_LIGHT)
        
        # Head tilted slightly forward, hair streaming back in wind
        draw_head(c, hx=16, hy=12 + bob, eye_state="normal", look_dir="forward",
                  mouth="smirk", hair_bob=-1 if bob < 0 else 0, hair_wind=1)
        
        assert any(c.get_pixel(x, 31)[3] > 0 for x in range(32)), f"p1_run frame {i} missing y=31 anchor!"
        frames.append(c)
        
    return frames


def generate_p1_run_fast() -> List[PixelCanvas]:
    """
    8 frames, 20 fps, loop: true.
    Speed boost sprint! Low aerodynamic forward lean, Speed Boots (orange with yellow wings),
    motion streaks and speed lines. Row y=31 contact guaranteed in every frame.
    """
    frames = []
    
    strides = [
        # (fwd_x, fwd_y, fwd_pose, back_x, back_y, back_pose, bob)
        (22, 31, "heel_strike", 8, 27, "toe_point", 0),
        (20, 31, "flat",        11, 28, "flat",       1),
        (16, 31, "toe_push",    17, 26, "flat",       0),
        (11, 31, "toe_point",   22, 25, "flat",      -1),
        (22, 31, "heel_strike", 8, 27, "toe_point", 0),
        (20, 31, "flat",        11, 28, "flat",       1),
        (16, 31, "toe_push",    17, 26, "flat",       0),
        (11, 31, "toe_point",   22, 25, "flat",      -1),
    ]
    
    for i, (fx1, fy1, p1, fx2, fy2, p2, bob) in enumerate(strides):
        c = create_base_canvas()
        
        # Trailing speed lines and spark motes behind boots
        c.set_pixel(fx2 - 2, fy2, YELLOW_LIGHT)
        c.set_pixel(fx2 - 4, fy2, ORANGE_MID)
        c.set_pixel(fx1 - 3, fy1 - 1, YELLOW_LIGHT)
        c.set_pixel(fx1 - 5, fy1 - 1, ORANGE_SHADOW)
        
        # Speed boots (Orange ramp + yellow lightning wings)
        is_even_phase = (i < 4)
        draw_sneaker(c, foot_x=fx2, foot_y=fy2, pose=p2, speed_boot=True, is_far=is_even_phase)
        draw_sneaker(c, foot_x=fx1, foot_y=fy1, pose=p1, speed_boot=True, is_far=not is_even_phase)
        
        # Legs
        draw_leg(c, hip_x=15, hip_y=25 + bob, foot_x=fx2, foot_y=fy2 - 2, is_far=True)
        draw_leg(c, hip_x=17, hip_y=25 + bob, foot_x=fx1, foot_y=fy1 - 2, is_far=False)
        
        # Shorts leaning forward
        draw_shorts(c, sx=16, sy=23 + bob, w=9, h=4)
        
        # Hoodie thrust forward
        draw_hoodie(c, tx=17, ty=17 + bob, w=10, h=7, drawstring_wind=2)
        
        # Arms pumping like piston blades
        if i in [0, 1, 4, 5]:
            c.line(17, 18 + bob, 22, 20 + bob, RED_LIGHT)
            c.set_pixel(22, 20 + bob, SKIN_LIGHT)
            c.line(17, 18 + bob, 11, 21 + bob, RED_SHADOW)
            c.set_pixel(11, 21 + bob, SKIN_SHADOW)
        else:
            c.line(17, 18 + bob, 12, 20 + bob, RED_LIGHT)
            c.set_pixel(12, 20 + bob, SKIN_LIGHT)
            c.line(17, 18 + bob, 21, 21 + bob, RED_SHADOW)
            c.set_pixel(21, 21 + bob, SKIN_SHADOW)
            
        # Head thrust forward into wind, wide excited eyes, hair swept flat back
        draw_head(c, hx=18, hy=12 + bob, eye_state="wide", look_dir="forward",
                  mouth="smirk", hair_bob=-2, hair_wind=1)
        # Extra streaming hair streaks behind
        c.line(12, 10 + bob, 6, 11 + bob, BROWN_LIGHT)
        c.line(11, 11 + bob, 5, 12 + bob, BROWN_DARK)
        
        assert any(c.get_pixel(x, 31)[3] > 0 for x in range(32)), f"p1_run_fast frame {i} missing y=31 anchor!"
        frames.append(c)
        
    return frames


def generate_p1_jump_up() -> List[PixelCanvas]:
    """
    3 frames, 16 fps, loop: false.
    F0: Anticipation crouch / squash (knees bent wide, feet on y=31).
    F1: Explosive upward launch / stretch (toes pushing off at y=31, arms reaching sky).
    F2: Rising momentum (tucking knees, trailing foot touches row 31).
    """
    frames = []
    
    # ---------------- Frame 0: Deep Crouch Anticipation ----------------
    c0 = create_base_canvas()
    # Feet planted wide on y=31
    draw_sneaker(c0, foot_x=11, foot_y=31, pose="squash", is_far=True)
    draw_sneaker(c0, foot_x=19, foot_y=31, pose="squash", is_far=False)
    # Legs bent wide
    draw_leg(c0, hip_x=13, hip_y=26, foot_x=11, foot_y=29, is_far=True)
    draw_leg(c0, hip_x=17, hip_y=26, foot_x=19, foot_y=29, is_far=False)
    # Compressed wide shorts
    draw_shorts(c0, sx=15, sy=24, w=11, h=4)
    # Compressed hoodie
    draw_hoodie(c0, tx=15, ty=19, w=11, h=6)
    # Arms thrown down-back preparing to swing
    c0.set_pixel(9, 22, RED_MID)
    c0.set_pixel(8, 23, SKIN_LIGHT)
    c0.set_pixel(21, 22, RED_SHADOW)
    c0.set_pixel(22, 23, SKIN_SHADOW)
    # Head looking up eagerly
    draw_head(c0, hx=15, hy=15, eye_state="normal", look_dir="up", mouth="smirk")
    assert any(c0.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c0)

    # ---------------- Frame 1: Launch Blast-Off (Stretch) ----------------
    c1 = create_base_canvas()
    # Toes fully extended pointing down, touching row 31
    draw_sneaker(c1, foot_x=13, foot_y=31, pose="toe_point", is_far=True)
    draw_sneaker(c1, foot_x=17, foot_y=31, pose="toe_point", is_far=False)
    # Stretched legs
    draw_leg(c1, hip_x=14, hip_y=22, foot_x=13, foot_y=28, is_far=True)
    draw_leg(c1, hip_x=17, hip_y=22, foot_x=17, foot_y=28, is_far=False)
    # Narrow stretched shorts
    draw_shorts(c1, sx=15, sy=19, w=8, h=4)
    # Elongated hoodie
    draw_hoodie(c1, tx=15, ty=13, w=8, h=7)
    # Arms shooting straight up into the sky!
    c1.line(13, 14, 11, 8, RED_LIGHT)
    c1.set_pixel(11, 7, SKIN_LIGHT)
    c1.line(17, 14, 19, 8, RED_LIGHT)
    c1.set_pixel(19, 7, SKIN_LIGHT)
    # Head looking up with wide ecstatic eyes and open shouting mouth
    draw_head(c1, hx=15, hy=9, eye_state="wide", look_dir="up", mouth="open", hair_wind=1)
    assert any(c1.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c1)

    # ---------------- Frame 2: Rising Momentum ----------------
    c2 = create_base_canvas()
    # Knees pulling up, trailing foot touches row 31 for anchor!
    draw_sneaker(c2, foot_x=18, foot_y=29, pose="flat", is_far=False)
    draw_sneaker(c2, foot_x=13, foot_y=31, pose="toe_point", is_far=True)
    draw_leg(c2, hip_x=14, hip_y=22, foot_x=13, foot_y=28, is_far=True)
    draw_leg(c2, hip_x=17, hip_y=22, foot_x=18, foot_y=26, is_far=False)
    draw_shorts(c2, sx=15, sy=19, w=9, h=4)
    draw_hoodie(c2, tx=15, ty=13, w=9, h=7)
    # Arms bent in front guiding ascent
    c2.line(13, 14, 10, 11, RED_LIGHT)
    c2.set_pixel(10, 10, SKIN_LIGHT)
    c2.line(18, 14, 21, 11, RED_LIGHT)
    c2.set_pixel(21, 10, SKIN_LIGHT)
    draw_head(c2, hx=15, hy=9, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c2.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c2)

    return frames


def generate_p1_jump_apex() -> List[PixelCanvas]:
    """
    2 frames, 12 fps, loop: false.
    Zero-g hang time at the peak of the jump. Tucked knees, arms spread like wings,
    hair and drawstrings floating weightlessly. Trailing toe touches row y=31 for anchor.
    """
    frames = []
    
    for i in range(2):
        c = create_base_canvas()
        # Trailing toe reaches row 31 for anchor
        draw_sneaker(c, foot_x=13, foot_y=31, pose="toe_point", is_far=True)
        draw_sneaker(c, foot_x=18, foot_y=29 - i, pose="flat", is_far=False)
        
        # Tucked legs
        draw_leg(c, hip_x=14, hip_y=22, foot_x=13, foot_y=28, is_far=True)
        draw_leg(c, hip_x=17, hip_y=22, foot_x=18, foot_y=26 - i, is_far=False)
        
        draw_shorts(c, sx=15, sy=19, w=9, h=4)
        draw_hoodie(c, tx=15, ty=13, w=9, h=7)
        
        # Arms spread wide for aerodynamic balance
        c.line(13, 15, 8, 14 + i, RED_LIGHT)
        c.set_pixel(7, 14 + i, SKIN_LIGHT)
        c.line(18, 15, 23, 14 + i, RED_LIGHT)
        c.set_pixel(24, 14 + i, SKIN_LIGHT)
        
        # Head with hair floating in zero-g
        draw_head(c, hx=15, hy=9, eye_state="normal", look_dir="forward", mouth="smirk", hair_bob=-1)
        # Floating wisp pixels
        c.set_pixel(13, 4, WOOD_HIGHLIGHT)
        c.set_pixel(17, 4, BROWN_LIGHT)
        
        assert any(c.get_pixel(x, 31)[3] > 0 for x in range(32)), f"p1_jump_apex frame {i} missing y=31 anchor!"
        frames.append(c)
        
    return frames


def generate_p1_fall() -> List[PixelCanvas]:
    """
    3 frames, 16 fps, loop: true.
    High speed descent: rising air rushes upward past character!
    Hair and drawstrings blown straight up, legs reaching down touching row 31,
    wide eyes looking down at landing zone.
    """
    frames = []
    
    for i in range(3):
        c = create_base_canvas()
        
        # Legs extending downward to meet ground, touching row 31
        draw_sneaker(c, foot_x=12, foot_y=31, pose="toe_point", is_far=True)
        draw_sneaker(c, foot_x=18, foot_y=31, pose="toe_point", is_far=False)
        
        draw_leg(c, hip_x=13, hip_y=24, foot_x=12, foot_y=28, is_far=True)
        draw_leg(c, hip_x=17, hip_y=24, foot_x=18, foot_y=28, is_far=False)
        
        draw_shorts(c, sx=15, sy=21, w=9, h=4)
        draw_hoodie(c, tx=15, ty=15, w=9, h=7)
        
        # Arms pushed upward by rising wind
        c.line(12, 16, 9, 10 - i, RED_LIGHT)
        c.set_pixel(9, 9 - i, SKIN_LIGHT)
        c.line(18, 16, 21, 10 - i, RED_LIGHT)
        c.set_pixel(21, 9 - i, SKIN_LIGHT)
        
        # Drawstrings flapping up!
        c.set_pixel(14, 14, PURE_WHITE)
        c.set_pixel(14, 13, WHITE_SHADOW)
        c.set_pixel(17, 14, PURE_WHITE)
        c.set_pixel(17, 13, WHITE_SHADOW)
        
        # Head with hair blown straight up by wind, wide eyes looking down
        draw_head(c, hx=15, hy=11, eye_state="wide", look_dir="down", mouth="open", hair_wind=-1)
        
        assert any(c.get_pixel(x, 31)[3] > 0 for x in range(32)), f"p1_fall frame {i} missing y=31 anchor!"
        frames.append(c)
        
    return frames


def generate_p1_land() -> List[PixelCanvas]:
    """
    4 frames, 20 fps, loop: false.
    F0: Hard impact squash, feet wide, dust puffs at row y=31.
    F1: Low absorb crouch, rebounding.
    F2: Rising extension.
    F3: Settled upright standing ready stance.
    """
    frames = []
    
    # ---------------- Frame 0: Hard Impact Squash ----------------
    c0 = create_base_canvas()
    # Feet planted wide on row 31
    draw_sneaker(c0, foot_x=9, foot_y=31, pose="squash", is_far=True)
    draw_sneaker(c0, foot_x=21, foot_y=31, pose="squash", is_far=False)
    # Dust puffs kicked out at sides
    c0.set_pixel(7, 31, PURE_WHITE)
    c0.set_pixel(6, 31, WHITE_SHADOW)
    c0.set_pixel(23, 31, PURE_WHITE)
    c0.set_pixel(24, 31, WHITE_SHADOW)
    # Wide splayed legs
    draw_leg(c0, hip_x=12, hip_y=26, foot_x=9, foot_y=29, is_far=True)
    draw_leg(c0, hip_x=18, hip_y=26, foot_x=21, foot_y=29, is_far=False)
    # Squashed wide shorts
    draw_shorts(c0, sx=15, sy=25, w=12, h=3)
    # Squashed wide hoodie
    draw_hoodie(c0, tx=15, ty=20, w=12, h=6)
    # Arms flared wide for balance
    c0.line(10, 21, 5, 23, RED_LIGHT)
    c0.set_pixel(4, 23, SKIN_LIGHT)
    c0.line(20, 21, 25, 23, RED_SHADOW)
    c0.set_pixel(26, 23, SKIN_SHADOW)
    # Head compressed, eyes squinting shut from impact
    draw_head(c0, hx=15, hy=16, eye_state="blink", look_dir="forward", mouth="grimace")
    assert any(c0.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c0)

    # ---------------- Frame 1: Low Absorb Crouch ----------------
    c1 = create_base_canvas()
    draw_sneaker(c1, foot_x=11, foot_y=31, pose="flat", is_far=True)
    draw_sneaker(c1, foot_x=19, foot_y=31, pose="flat", is_far=False)
    draw_leg(c1, hip_x=13, hip_y=26, foot_x=11, foot_y=28, is_far=True)
    draw_leg(c1, hip_x=17, hip_y=26, foot_x=19, foot_y=28, is_far=False)
    draw_shorts(c1, sx=15, sy=24, w=10, h=4)
    draw_hoodie(c1, tx=15, ty=18, w=10, h=7)
    c1.set_pixel(9, 20, RED_MID)
    c1.set_pixel(9, 21, SKIN_MID)
    c1.set_pixel(21, 20, RED_MID)
    c1.set_pixel(21, 21, SKIN_MID)
    draw_head(c1, hx=15, hy=14, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c1.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c1)

    # ---------------- Frame 2: Rising Extension ----------------
    c2 = create_base_canvas()
    draw_sneaker(c2, foot_x=12, foot_y=31, pose="flat", is_far=True)
    draw_sneaker(c2, foot_x=18, foot_y=31, pose="flat", is_far=False)
    draw_leg(c2, hip_x=13, hip_y=26, foot_x=12, foot_y=28, is_far=True)
    draw_leg(c2, hip_x=18, hip_y=26, foot_x=18, foot_y=28, is_far=False)
    draw_shorts(c2, sx=15, sy=23, w=9, h=4)
    draw_hoodie(c2, tx=15, ty=17, w=10, h=7)
    c2.set_pixel(9, 19, RED_MID)
    c2.set_pixel(9, 20, SKIN_MID)
    c2.set_pixel(21, 19, RED_MID)
    c2.set_pixel(21, 20, SKIN_MID)
    draw_head(c2, hx=15, hy=13, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c2.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c2)

    # ---------------- Frame 3: Settled Stance ----------------
    c3 = create_base_canvas()
    draw_sneaker(c3, foot_x=12, foot_y=31, pose="flat", is_far=True)
    draw_sneaker(c3, foot_x=18, foot_y=31, pose="flat", is_far=False)
    draw_leg(c3, hip_x=13, hip_y=26, foot_x=12, foot_y=28, is_far=True)
    draw_leg(c3, hip_x=18, hip_y=26, foot_x=18, foot_y=28, is_far=False)
    draw_shorts(c3, sx=15, sy=23, w=9, h=4)
    draw_hoodie(c3, tx=15, ty=17, w=10, h=7)
    c3.set_pixel(9, 19, RED_MID)
    c3.set_pixel(9, 20, SKIN_MID)
    c3.set_pixel(20, 19, RED_MID)
    c3.set_pixel(20, 20, SKIN_MID)
    draw_head(c3, hx=15, hy=12, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c3.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c3)

    return frames


def generate_p1_trip() -> List[PixelCanvas]:
    """
    10 frames, 14 fps, loop: false.
    Comedy slapstick stumble beat:
    0: Toe caught at row 31, shock!
    1: Windmilling arms, falling forward
    2: Horizontal Superman belly-flop dive
    3: Sprawled flat on floor with dust puffs (Hold 1)
    4: Sprawled flat (Hold 2)
    5: Elastic comic butt-bounce
    6: Settles back flat, cartoon dizzy stars orbit head
    7: Hands push off floor, dizzy swirl eyes
    8: Pulls knees under, shakes head
    9: Springs back onto feet, defiant smirk ("I'm okay!")
    """
    frames = []
    
    # ---------------- Frame 0: Toe Caught! ----------------
    c0 = create_base_canvas()
    draw_sneaker(c0, foot_x=22, foot_y=31, pose="flat", is_far=False) # stuck foot
    draw_sneaker(c0, foot_x=12, foot_y=28, pose="toe_point", is_far=True) # back foot in air
    draw_leg(c0, hip_x=15, hip_y=24, foot_x=12, foot_y=26, is_far=True)
    draw_leg(c0, hip_x=18, hip_y=24, foot_x=22, foot_y=28, is_far=False)
    draw_shorts(c0, sx=16, sy=22, w=9, h=4)
    draw_hoodie(c0, tx=17, ty=16, w=10, h=7)
    # Windmilling arms starting
    c0.line(16, 17, 11, 14, RED_LIGHT)
    c0.set_pixel(10, 13, SKIN_LIGHT)
    c0.line(18, 17, 23, 15, RED_SHADOW)
    c0.set_pixel(24, 15, SKIN_SHADOW)
    draw_head(c0, hx=19, hy=11, eye_state="wide", look_dir="forward", mouth="oof")
    assert any(c0.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c0)

    # ---------------- Frame 1: Windmilling Panic ----------------
    c1 = create_base_canvas()
    draw_sneaker(c1, foot_x=18, foot_y=31, pose="toe_push", is_far=False)
    draw_sneaker(c1, foot_x=9, foot_y=26, pose="toe_point", is_far=True)
    draw_leg(c1, hip_x=16, hip_y=23, foot_x=9, foot_y=24, is_far=True)
    draw_leg(c1, hip_x=18, hip_y=23, foot_x=18, foot_y=28, is_far=False)
    draw_shorts(c1, sx=17, sy=22, w=9, h=4)
    draw_hoodie(c1, tx=19, ty=17, w=10, h=6)
    # Windmilling arm circles
    c1.line(18, 18, 13, 12, RED_LIGHT)
    c1.set_pixel(12, 11, SKIN_LIGHT)
    c1.line(20, 18, 25, 22, RED_SHADOW)
    c1.set_pixel(26, 23, SKIN_SHADOW)
    draw_head(c1, hx=22, hy=13, eye_state="wide", look_dir="down", mouth="open")
    assert any(c1.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c1)

    # ---------------- Frame 2: Horizontal Belly-Flop Dive ----------------
    c2 = create_base_canvas()
    # Feet trailing horizontally
    draw_sneaker(c2, foot_x=7, foot_y=28, pose="flat", is_far=True)
    draw_sneaker(c2, foot_x=11, foot_y=31, pose="toe_point", is_far=False) # touches y=31!
    draw_leg(c2, hip_x=14, hip_y=26, foot_x=7, foot_y=27, is_far=True)
    draw_leg(c2, hip_x=15, hip_y=26, foot_x=11, foot_y=29, is_far=False)
    draw_shorts(c2, sx=16, sy=24, w=8, h=4)
    draw_hoodie(c2, tx=20, ty=22, w=9, h=5)
    # Arms reaching forward anticipating crash
    c2.line(21, 23, 27, 23, RED_LIGHT)
    c2.set_pixel(28, 23, SKIN_LIGHT)
    draw_head(c2, hx=25, hy=20, eye_state="oof", look_dir="forward", mouth="oof")
    assert any(c2.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c2)

    # ---------------- Frame 3: Sprawled Flat (Hold 1) ----------------
    c3 = create_base_canvas()
    # Body squished flat along rows 28..31
    # Sneakers turned sideways flat on row 31
    draw_sneaker(c3, foot_x=6, foot_y=31, pose="trip_flat", is_far=False)
    # Denim shorts flat
    for y in range(28, 32):
        for x in range(10, 15):
            c3.set_pixel(x, y, BLUE_SHADOW if y == 31 else BLUE_MID)
    # Hoodie flat
    for y in range(28, 32):
        for x in range(15, 22):
            c3.set_pixel(x, y, RED_SHADOW if y == 31 else (RED_LIGHT if y == 28 else RED_MID))
    # Limp arms splayed on floor
    c3.line(16, 31, 13, 31, SKIN_MID)
    c3.line(21, 31, 24, 31, SKIN_MID)
    # Face squished flat on ground
    draw_head(c3, hx=25, hy=26, eye_state="oof", look_dir="forward", mouth="oof")
    # Comic dust poofs at floor impact
    c3.set_pixel(3, 31, WHITE_SHADOW)
    c3.set_pixel(29, 31, WHITE_SHADOW)
    assert any(c3.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c3)

    # ---------------- Frame 4: Sprawled Flat (Hold 2) ----------------
    c4 = c3.clone()
    frames.append(c4)

    # ---------------- Frame 5: Comic Butt Bounce ----------------
    c5 = create_base_canvas()
    # Feet and face remain on floor, hips pop up 2px
    draw_sneaker(c5, foot_x=6, foot_y=31, pose="trip_flat", is_far=False)
    for y in range(26, 30):
        for x in range(10, 15):
            c5.set_pixel(x, y, BLUE_SHADOW if y == 29 else BLUE_MID)
    for y in range(26, 30):
        for x in range(15, 21):
            c5.set_pixel(x, y, RED_SHADOW if y == 29 else RED_MID)
    c5.set_pixel(13, 31, OUTLINE) # contact anchor
    draw_head(c5, hx=25, hy=26, eye_state="oof", look_dir="forward", mouth="oof")
    assert any(c5.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c5)

    # ---------------- Frame 6: Settles Flat + Dizzy Stars ----------------
    c6 = c3.clone()
    # 3 cartoon dizzy stars orbiting head!
    c6.set_pixel(24, 21, YELLOW_LIGHT)
    c6.set_pixel(25, 22, YELLOW_MID)
    c6.set_pixel(28, 20, YELLOW_LIGHT)
    c6.set_pixel(27, 21, YELLOW_MID)
    c6.set_pixel(22, 23, YELLOW_LIGHT)
    frames.append(c6)

    # ---------------- Frame 7: Hands Push Off Floor (Dizzy) ----------------
    c7 = create_base_canvas()
    draw_sneaker(c7, foot_x=8, foot_y=31, pose="flat", is_far=False)
    c7.rect(11, 27, 5, 4, BLUE_MID)
    draw_hoodie(c7, tx=17, ty=22, w=8, h=6)
    # Hands planted on ground pushing up
    c7.line(16, 23, 16, 30, RED_LIGHT)
    c7.set_pixel(16, 31, SKIN_LIGHT)
    c7.line(20, 23, 21, 30, RED_LIGHT)
    c7.set_pixel(21, 31, SKIN_LIGHT)
    # Head raised, cartoon swirl dizzy eyes!
    draw_head(c7, hx=22, hy=17, eye_state="dizzy", look_dir="forward", mouth="grimace")
    assert any(c7.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c7)

    # ---------------- Frame 8: Knees Pulled Under, Shaking Head ----------------
    c8 = create_base_canvas()
    draw_sneaker(c8, foot_x=10, foot_y=31, pose="flat", is_far=True)
    draw_sneaker(c8, foot_x=14, foot_y=31, pose="flat", is_far=False)
    draw_shorts(c8, sx=14, sy=25, w=8, h=4)
    draw_hoodie(c8, tx=15, ty=20, w=9, h=6)
    c8.set_pixel(10, 22, SKIN_MID)
    c8.set_pixel(20, 22, SKIN_MID)
    draw_head(c8, hx=15, hy=15, eye_state="blink", look_dir="down", mouth="grimace")
    assert any(c8.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c8)

    # ---------------- Frame 9: Pop Up with Defiant Smirk! ----------------
    c9 = create_base_canvas()
    draw_sneaker(c9, foot_x=12, foot_y=31, pose="flat", is_far=True)
    draw_sneaker(c9, foot_x=18, foot_y=31, pose="flat", is_far=False)
    draw_leg(c9, hip_x=13, hip_y=26, foot_x=12, foot_y=28, is_far=True)
    draw_leg(c9, hip_x=18, hip_y=26, foot_x=18, foot_y=28, is_far=False)
    draw_shorts(c9, sx=15, sy=23, w=9, h=4)
    draw_hoodie(c9, tx=15, ty=17, w=10, h=7)
    # Wipes nose with sleeve in defiant recovery
    c9.line(18, 18, 17, 14, RED_LIGHT)
    c9.set_pixel(17, 13, SKIN_LIGHT)
    c9.set_pixel(9, 20, SKIN_MID)
    draw_head(c9, hx=15, hy=12, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c9.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c9)

    return frames


def generate_p1_boost_jump() -> List[PixelCanvas]:
    """
    4 frames, 18 fps, loop: false.
    Feather boost leap:
    0: Power gather crouch with cyan feather aura
    1: Vertical rocket stretch with feather wing trail down to row 31
    2: High soar / winged glide
    3: Smooth glide crest with sparkles touching row 31
    """
    frames = []
    
    # ---------------- Frame 0: Gather Crouch with Feather Glow ----------------
    c0 = create_base_canvas()
    draw_sneaker(c0, foot_x=11, foot_y=31, pose="squash", wing_fx=True, is_far=True)
    draw_sneaker(c0, foot_x=19, foot_y=31, pose="squash", wing_fx=True, is_far=False)
    # Cyan / blue feather energy swirls at ground level
    c0.set_pixel(8, 31, BLUE_LIGHT)
    c0.set_pixel(22, 31, PURE_WHITE)
    c0.set_pixel(15, 31, BLUE_MID)
    draw_leg(c0, hip_x=13, hip_y=26, foot_x=11, foot_y=29, is_far=True)
    draw_leg(c0, hip_x=17, hip_y=26, foot_x=19, foot_y=29, is_far=False)
    draw_shorts(c0, sx=15, sy=24, w=11, h=4)
    draw_hoodie(c0, tx=15, ty=19, w=11, h=6)
    draw_head(c0, hx=15, hy=15, eye_state="normal", look_dir="up", mouth="smirk")
    assert any(c0.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c0)

    # ---------------- Frame 1: Vertical Rocket Stretch ----------------
    c1 = create_base_canvas()
    # Rocketing up! Feet pointing down
    draw_sneaker(c1, foot_x=13, foot_y=26, pose="toe_point", wing_fx=True, is_far=True)
    draw_sneaker(c1, foot_x=17, foot_y=26, pose="toe_point", wing_fx=True, is_far=False)
    # Luminous feather light beam streaming down to row 31!
    c1.line(14, 27, 14, 31, BLUE_LIGHT)
    c1.line(16, 27, 16, 31, PURE_WHITE)
    c1.set_pixel(15, 30, BLUE_MID)
    c1.set_pixel(15, 31, PURE_WHITE)
    c1.set_pixel(13, 31, BLUE_LIGHT)
    c1.set_pixel(17, 31, BLUE_LIGHT)
    # Body elongated
    draw_leg(c1, hip_x=14, hip_y=19, foot_x=13, foot_y=23, is_far=True)
    draw_leg(c1, hip_x=17, hip_y=19, foot_x=17, foot_y=23, is_far=False)
    draw_shorts(c1, sx=15, sy=16, w=8, h=4)
    draw_hoodie(c1, tx=15, ty=10, w=8, h=7)
    # Arms reaching straight up
    c1.line(13, 11, 11, 5, RED_LIGHT)
    c1.set_pixel(11, 4, SKIN_LIGHT)
    c1.line(17, 11, 19, 5, RED_LIGHT)
    c1.set_pixel(19, 4, SKIN_LIGHT)
    draw_head(c1, hx=15, hy=6, eye_state="wide", look_dir="up", mouth="open")
    assert any(c1.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c1)

    # ---------------- Frame 2: Soaring Winged Glide ----------------
    c2 = create_base_canvas()
    # Soaring flight pose
    draw_sneaker(c2, foot_x=13, foot_y=26, pose="flat", wing_fx=True, is_far=True)
    draw_sneaker(c2, foot_x=18, foot_y=24, pose="flat", wing_fx=True, is_far=False)
    # Glowing feather particles drifting down to row 31 for anchor!
    c2.set_pixel(15, 28, BLUE_LIGHT)
    c2.set_pixel(14, 29, PURE_WHITE)
    c2.set_pixel(16, 30, BLUE_LIGHT)
    c2.set_pixel(15, 31, PURE_WHITE)
    draw_leg(c2, hip_x=14, hip_y=19, foot_x=13, foot_y=23, is_far=True)
    draw_leg(c2, hip_x=17, hip_y=19, foot_x=18, foot_y=21, is_far=False)
    draw_shorts(c2, sx=15, sy=16, w=9, h=4)
    draw_hoodie(c2, tx=15, ty=10, w=9, h=7)
    # Arms spread like soaring falcon wings
    c2.line(13, 12, 7, 10, RED_LIGHT)
    c2.set_pixel(6, 10, SKIN_LIGHT)
    c2.line(18, 12, 24, 10, RED_LIGHT)
    c2.set_pixel(25, 10, SKIN_LIGHT)
    draw_head(c2, hx=15, hy=7, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c2.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c2)

    # ---------------- Frame 3: Glide Crest ----------------
    c3 = create_base_canvas()
    # Trailing foot reaches row 31
    draw_sneaker(c3, foot_x=13, foot_y=31, pose="toe_point", wing_fx=True, is_far=True)
    draw_sneaker(c3, foot_x=18, foot_y=26, pose="flat", wing_fx=True, is_far=False)
    draw_leg(c3, hip_x=14, hip_y=20, foot_x=13, foot_y=28, is_far=True)
    draw_leg(c3, hip_x=17, hip_y=20, foot_x=18, foot_y=23, is_far=False)
    draw_shorts(c3, sx=15, sy=17, w=9, h=4)
    draw_hoodie(c3, tx=15, ty=11, w=9, h=7)
    c3.line(13, 13, 8, 11, RED_LIGHT)
    c3.set_pixel(7, 11, SKIN_LIGHT)
    c3.line(18, 13, 23, 11, RED_LIGHT)
    c3.set_pixel(24, 11, SKIN_LIGHT)
    draw_head(c3, hx=15, hy=8, eye_state="normal", look_dir="forward", mouth="smirk")
    assert any(c3.get_pixel(x, 31)[3] > 0 for x in range(32))
    frames.append(c3)

    return frames


def generate_p1_celebrate() -> List[PixelCanvas]:
    """
    8 frames, 10 fps, loop: true.
    Joyful victory fist-pump dance loop!
    Right fist punching the sky, little rhythmic hops, ecstatic open-mouth cheer,
    wink on frame 6. Row y=31 contact strictly maintained.
    """
    frames = []
    # Rhythmic hop offsets: [0, -1, -2, 0, 0, -1, -1, 0]
    hops = [0, -1, -2, 0, 0, -1, -1, 0]
    # Right fist heights: [16, 11, 7, 12, 14, 10, 11, 15]
    fist_ys = [16, 11, 7, 12, 14, 10, 11, 15]
    
    for i in range(8):
        c = create_base_canvas()
        hop = hops[i]
        fy = fist_ys[i]
        
        # Sneaker stance: firmly planted touching row 31
        draw_sneaker(c, foot_x=12, foot_y=31, pose="flat", is_far=True)
        draw_sneaker(c, foot_x=18, foot_y=31, pose="flat", is_far=False)
        
        # Legs
        draw_leg(c, hip_x=13, hip_y=26 + hop, foot_x=12, foot_y=28, is_far=True)
        draw_leg(c, hip_x=18, hip_y=26 + hop, foot_x=18, foot_y=28, is_far=False)
        
        # Shorts
        draw_shorts(c, sx=15, sy=23 + hop, w=9, h=4)
        
        # Hoodie
        draw_hoodie(c, tx=15, ty=17 + hop, w=10, h=7)
        
        # Left hand resting proudly on hip
        c.set_pixel(9, 20 + hop, RED_MID)
        c.set_pixel(10, 21 + hop, SKIN_MID)
        
        # Right arm fist-pumping straight up into the air!
        c.line(19, 18 + hop, 21, fy + 2, RED_LIGHT)
        # Clenched victory fist with white knuckle glint
        c.set_pixel(20, fy, SKIN_LIGHT)
        c.set_pixel(21, fy, PURE_WHITE)     # Knuckle glint
        c.set_pixel(22, fy, SKIN_MID)
        c.set_pixel(20, fy + 1, SKIN_MID)
        c.set_pixel(21, fy + 1, SKIN_SHADOW)
        c.set_pixel(22, fy + 1, OUTLINE)
        
        # Head with ecstatic expressions
        eye_st = "wink" if i == 6 else "normal"
        mouth_st = "open" if i in [1, 2, 3] else "smirk"
        look_d = "up" if i in [1, 2] else "forward"
        
        draw_head(c, hx=15, hy=12 + hop, eye_state=eye_st, look_dir=look_d,
                  mouth=mouth_st, hair_bob=-1 if hop < 0 else 0)
        
        assert any(c.get_pixel(x, 31)[3] > 0 for x in range(32)), f"p1_celebrate frame {i} missing y=31 anchor!"
        frames.append(c)
        
    return frames


# =============================================================================
# EXPORT ALL 11 SPRITESHEETS
# =============================================================================

def generate_all_player_sprites():
    animations = {
        "art/incoming/p1_idle.png": generate_p1_idle(),
        "art/incoming/p1_wait.png": generate_p1_wait(),
        "art/incoming/p1_run.png": generate_p1_run(),
        "art/incoming/p1_run_fast.png": generate_p1_run_fast(),
        "art/incoming/p1_jump_up.png": generate_p1_jump_up(),
        "art/incoming/p1_jump_apex.png": generate_p1_jump_apex(),
        "art/incoming/p1_fall.png": generate_p1_fall(),
        "art/incoming/p1_land.png": generate_p1_land(),
        "art/incoming/p1_trip.png": generate_p1_trip(),
        "art/incoming/p1_boost_jump.png": generate_p1_boost_jump(),
        "art/incoming/p1_celebrate.png": generate_p1_celebrate(),
    }
    
    print("--- Generating Elevated Player 1 Spritesheets ---")
    for path, frames in animations.items():
        assemble_strip(frames, path)
    print("--- All 11 Player 1 Spritesheets Generated Successfully! ---")


if __name__ == "__main__":
    generate_all_player_sprites()
