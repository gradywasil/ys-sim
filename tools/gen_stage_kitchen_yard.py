"""Younger Sibling Simulator - Kitchen & Backyard Stage Assets Generator v3.

Generates all Stage Assets for Kitchen and Backyard, plus ui_stage_card.png,
into art/v2/ according to docs/art-brief-v2.md and v3:
- Full 64-color shared palette plus stage 16-color accents.
- True pixel art: no blur, crisp outlines, hard-banded alphas.
- Floor level at y=400 in 960x540 backgrounds.
- *_bg_near.png 100% transparent above y=400 with 1px warm rim light.
- Seamless mid backgrounds (1280x540).
- Fully grounded characters and floor clutter with matching 1-bit shadows.
- Registers all created assets in art/v2/manifest.json.
"""

import os
import sys
import math
import json
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE, VOID_BLACK,
    SHADOW_PURPLE_DARK, SHADOW_PURPLE_DEEP, SHADOW_PURPLE_MID, SHADOW_DEEP, SHADOW_MID,
    PURPLE_DARK, PURPLE_MID, PURPLE_RICH, PURPLE_LIGHT,
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
from stage_palettes import STAGE_RGBA

RGBA = Tuple[int, int, int, int]

# Stage Accents (strictly from stage_palettes.py)
K_CREAM_LIGHT     = STAGE_RGBA["kitchen"][0]   # #f7f0df: cream tile light
K_CREAM_SHADOW    = STAGE_RGBA["kitchen"][1]   # #dfd4be: cream tile shadow
K_TEAL_DEEP       = STAGE_RGBA["kitchen"][2]   # #2a4b49: checkerboard dark teal deep
K_TEAL_MID        = STAGE_RGBA["kitchen"][3]   # #3b6b68: checkerboard dark teal mid
K_TEAL_LIGHT      = STAGE_RGBA["kitchen"][4]   # #528f8b: checkerboard dark teal light
K_MINT_HIGHLIGHT  = STAGE_RGBA["kitchen"][5]   # #a8ded9: mint tile highlight
K_TERRACOTTA      = STAGE_RGBA["kitchen"][6]   # #d1663b: warm terracotta / toaster orange
K_TOAST_GLOW      = STAGE_RGBA["kitchen"][7]   # #fa9352: warm toast glow
K_EGG_YELLOW      = STAGE_RGBA["kitchen"][8]   # #fedc82: egg yolk yellow
K_FLOUR_PALE      = STAGE_RGBA["kitchen"][9]   # #fff2b8: flour pale yellow
K_JAM_RED         = STAGE_RGBA["kitchen"][10]  # #8b2f3e: cherry / jam red
K_CAST_IRON       = STAGE_RGBA["kitchen"][11]  # #45505e: stove cast iron dark
K_STEEL_MID       = STAGE_RGBA["kitchen"][12]  # #6b788a: stainless steel mid
K_STEEL_SPECULAR  = STAGE_RGBA["kitchen"][13]  # #a2b0c2: stainless steel specular
K_COFFEE_DARK     = STAGE_RGBA["kitchen"][14]  # #5a3825: coffee / toast crust dark
K_OLIVE_GREEN     = STAGE_RGBA["kitchen"][15]  # #7a9150: grape / olive kitchen green

Y_TURF_SHADOW     = STAGE_RGBA["yard"][0]      # #0d2b18: deep turf shadow
Y_GRASS_SHADOW    = STAGE_RGBA["yard"][1]      # #194d27: lush grass shadow
Y_GRASS_MID       = STAGE_RGBA["yard"][2]      # #2a7a3b: grass blade mid
Y_GRASS_LIGHT     = STAGE_RGBA["yard"][3]      # #46ad59: grass blade highlight
Y_SPROUT_BRIGHT   = STAGE_RGBA["yard"][4]      # #7eed8f: fresh sprout bright green
Y_SOIL_DARK       = STAGE_RGBA["yard"][5]      # #302213: garden soil loam dark
Y_SOIL_MID        = STAGE_RGBA["yard"][6]      # #593f24: garden soil loam mid
Y_DIRT_DRY        = STAGE_RGBA["yard"][7]      # #8c6840: garden dirt dry
Y_POT_DARK        = STAGE_RGBA["yard"][8]      # #c4562d: flowerpot terracotta dark
Y_POT_LIGHT       = STAGE_RGBA["yard"][9]      # #eb7844: flowerpot terracotta light
Y_LIGHT_GOLD      = STAGE_RGBA["yard"][10]     # #f5b338: string light warm gold
Y_LIGHT_FILAMENT  = STAGE_RGBA["yard"][11]     # #ffeb80: string light filament glow
Y_FENCE_SHADOW    = STAGE_RGBA["yard"][12]     # #203b57: dusk fence shadow
Y_FENCE_MID       = STAGE_RGBA["yard"][13]     # #3a638c: dusk fence blue-gray
Y_FLOWER_MAGENTA  = STAGE_RGBA["yard"][14]     # #d43b68: garden flower magenta
Y_WATER_CYAN      = STAGE_RGBA["yard"][15]     # #8fedf7: water droplet / dragonfly cyan


def make_shadow(w: int, h: int, cx: int, cy: int, rx: int, ry: int) -> PixelCanvas:
    """Creates matching 1-bit hard-banded shadow sprite in OUTLINE color."""
    c = PixelCanvas(w, h, TRANSPARENT)
    for y in range(max(0, cy - ry), min(h, cy + ry + 1)):
        for x in range(max(0, cx - rx), min(w, cx + rx + 1)):
            dx = (x - cx) / float(rx) if rx > 0 else 0
            dy = (y - cy) / float(ry) if ry > 0 else 0
            if dx * dx + dy * dy <= 1.0:
                c.set_pixel(x, y, OUTLINE)
    return c


def save_single(canvas: PixelCanvas, output_path: str):
    canvas.to_image().save(output_path, "PNG")
    print(f"Saved {output_path} ({canvas.width}x{canvas.height}, 1 frame)")


# ==============================================================================
# UI STAGE CARD: ui_stage_card.png (2400x144, 5 frames 480x144, base palette only!)
# ==============================================================================

def generate_ui_stage_card() -> List[PixelCanvas]:
    """
    Decorative banner frames for:
    (0) Bedroom, (1) Kitchen, (2) Backyard, (3) Basement, (4) Attic.
    Frame size 480x144. Strictly uses base palette (palette.py)!
    """
    frames = []

    stage_themes = [
        # 0: Bedroom
        {
            "name": "bedroom",
            "outer_rim": WOOD_HIGHLIGHT,
            "ribbon": DUSK_LILAC,
            "plate_bg": SHADOW_PURPLE_DEEP,
            "plate_stripe": PURPLE_MID,
            "corner_icon": "star",
            "icon_color": YELLOW_MID,
            "left_crest": "moon",
            "right_crest": "plane",
        },
        # 1: Kitchen
        {
            "name": "kitchen",
            "outer_rim": WOOD_LIT,
            "ribbon": ORANGE_MID,
            "plate_bg": DUSK_CREAM,
            "plate_stripe": DUSK_BLUSH,
            "corner_icon": "check",
            "icon_color": TEAL_MID,
            "left_crest": "utensils",
            "right_crest": "chef_hat",
        },
        # 2: Backyard
        {
            "name": "yard",
            "outer_rim": GREEN_LIGHT,
            "ribbon": GREEN_MID,
            "plate_bg": GREEN_DEEP,
            "plate_stripe": GREEN_SHADOW,
            "corner_icon": "flower",
            "icon_color": RED_MID,
            "left_crest": "sunflower",
            "right_crest": "trowel",
        },
        # 3: Basement
        {
            "name": "basement",
            "outer_rim": WHITE_SHADOW,
            "ribbon": METAL_SHADOW,
            "plate_bg": VOID_BLACK,
            "plate_stripe": SHADOW_PURPLE_DARK,
            "corner_icon": "bolt",
            "icon_color": METAL_MID,
            "left_crest": "gear",
            "right_crest": "gauge",
        },
        # 4: Attic
        {
            "name": "attic",
            "outer_rim": WOOD_HIGHLIGHT,
            "ribbon": BROWN_MID,
            "plate_bg": BROWN_DARKEST,
            "plate_stripe": BROWN_DARK,
            "corner_icon": "brass",
            "icon_color": YELLOW_MID,
            "left_crest": "key",
            "right_crest": "candle",
        },
    ]

    for f_idx, theme in enumerate(stage_themes):
        c = PixelCanvas(480, 144, TRANSPARENT)

        # Main frame bounds: x=12..467, y=10..133 (width 456, height 124)
        fx, fy, fw, fh = 12, 10, 456, 124

        # Drop shadow behind entire frame
        c.rect(fx + 3, fy + 4, fw, fh, VOID_BLACK)

        # Outer Dark Border (2px)
        c.rect(fx, fy, fw, fh, OUTLINE)

        # Bevel highlight top/left
        c.line(fx + 1, fy + 1, fx + fw - 2, fy + 1, theme["outer_rim"])
        c.line(fx + 1, fy + 1, fx + 1, fy + fh - 2, theme["outer_rim"])
        # Bevel shadow bottom/right
        c.line(fx + 1, fy + fh - 2, fx + fw - 2, fy + fh - 2, OUTLINE)
        c.line(fx + fw - 2, fy + 1, fx + fw - 2, fy + fh - 2, OUTLINE)

        # Ribbon Inlay (width 5px) around perimeter
        c.rect(fx + 3, fy + 3, fw - 6, fh - 6, theme["ribbon"], outline=OUTLINE)

        # Inner Filigree Bevel & Frame
        ix, iy, iw, ih = fx + 9, fy + 9, fw - 18, fh - 18
        c.rect(ix, iy, iw, ih, OUTLINE)
        c.line(ix + 1, iy + 1, ix + iw - 2, iy + 1, theme["outer_rim"])

        # Interior Plate Field
        px, py, pw, ph = ix + 2, iy + 2, iw - 4, ih - 4
        c.rect(px, py, pw, ph, theme["plate_bg"])

        # Textured pinstripe / grain pattern across plate
        for y_scan in range(py + 2, py + ph - 2, 4):
            c.line(px + 10, y_scan, px + pw - 10, y_scan, theme["plate_stripe"])

        # Chamfered Corner Medallions (4 corners)
        corner_coords = [
            (fx + 4, fy + 4),
            (fx + fw - 14, fy + 4),
            (fx + 4, fy + fh - 14),
            (fx + fw - 14, fy + fh - 14),
        ]
        for cx_c, cy_c in corner_coords:
            c.rect(cx_c, cy_c, 10, 10, theme["icon_color"], outline=OUTLINE)
            c.set_pixel(cx_c + 2, cy_c + 2, PURE_WHITE)
            c.set_pixel(cx_c + 7, cy_c + 7, OUTLINE)

        # Left Themed Crest (x=24..68, cy=72)
        lcx, lcy = 46, 72
        c.circle(lcx, lcy, 18, theme["ribbon"], outline=OUTLINE)
        c.circle(lcx, lcy, 15, theme["plate_bg"], outline=OUTLINE)

        # Right Themed Crest (x=412..456, cy=72)
        rcx, rcy = 434, 72
        c.circle(rcx, rcy, 18, theme["ribbon"], outline=OUTLINE)
        c.circle(rcx, rcy, 15, theme["plate_bg"], outline=OUTLINE)

        # Draw Theme Crest Icons
        if theme["left_crest"] == "moon":
            # Crescent Moon
            c.circle(lcx - 1, lcy, 10, YELLOW_MID, outline=OUTLINE)
            c.circle(lcx + 4, lcy - 2, 8, theme["plate_bg"], outline=None)
            c.set_pixel(lcx + 6, lcy - 5, YELLOW_LIGHT)
        elif theme["left_crest"] == "utensils":
            # Crossed Knife & Spoon
            c.line(lcx - 7, lcy - 7, lcx + 7, lcy + 7, METAL_MID)
            c.circle(lcx + 7, lcy + 7, 3, METAL_MID, outline=OUTLINE)
            c.line(lcx + 7, lcy - 7, lcx - 7, lcy + 7, WOOD_HIGHLIGHT)
            c.circle(lcx - 7, lcy + 7, 3, BROWN_MID, outline=OUTLINE)
        elif theme["left_crest"] == "sunflower":
            # Sunflower
            for deg in range(0, 360, 45):
                rad = math.radians(deg)
                px_p = int(lcx + math.cos(rad) * 9)
                py_p = int(lcy + math.sin(rad) * 9)
                c.set_pixel(px_p, py_p, YELLOW_LIGHT)
            c.circle(lcx, lcy, 5, BROWN_DARK, outline=OUTLINE)
        elif theme["left_crest"] == "gear":
            # Gear Cog
            c.circle(lcx, lcy, 9, METAL_MID, outline=OUTLINE)
            c.circle(lcx, lcy, 4, theme["plate_bg"], outline=OUTLINE)
            for dx_g, dy_g in [(-9, 0), (9, 0), (0, -9), (0, 9), (-6, -6), (6, 6), (-6, 6), (6, -6)]:
                c.rect(lcx + dx_g - 1, lcy + dy_g - 1, 3, 3, METAL_SHADOW, outline=OUTLINE)
        elif theme["left_crest"] == "key":
            # Vintage Key
            c.circle(lcx, lcy - 5, 5, YELLOW_MID, outline=OUTLINE)
            c.circle(lcx, lcy - 5, 2, theme["plate_bg"], outline=None)
            c.line(lcx, lcy, lcx, lcy + 9, YELLOW_MID)
            c.line(lcx, lcy + 5, lcx + 4, lcy + 5, YELLOW_MID)
            c.line(lcx, lcy + 8, lcx + 4, lcy + 8, YELLOW_MID)

        if theme["right_crest"] == "plane":
            # Paper Airplane
            c.polygon([(rcx + 8, rcy), (rcx - 8, rcy - 7), (rcx - 4, rcy), (rcx - 8, rcy + 7)], PURE_WHITE, outline=OUTLINE)
            c.line(rcx - 4, rcy, rcx + 8, rcy, BLUE_LIGHT)
        elif theme["right_crest"] == "chef_hat":
            # Chef Hat
            c.rect(rcx - 6, rcy + 2, 12, 6, PURE_WHITE, outline=OUTLINE)
            c.circle(rcx, rcy - 4, 7, PURE_WHITE, outline=OUTLINE)
            c.circle(rcx - 6, rcy - 2, 5, PURE_WHITE, outline=OUTLINE)
            c.circle(rcx + 6, rcy - 2, 5, PURE_WHITE, outline=OUTLINE)
        elif theme["right_crest"] == "trowel":
            # Garden Trowel
            c.polygon([(rcx + 6, rcy + 6), (rcx + 8, rcy - 2), (rcx, rcy - 7), (rcx - 4, rcy)], METAL_MID, outline=OUTLINE)
            c.line(rcx - 4, rcy, rcx - 9, rcy + 5, BROWN_MID)
        elif theme["right_crest"] == "gauge":
            # Pressure Gauge
            c.circle(rcx, rcy, 8, WHITE_MID, outline=OUTLINE)
            c.line(rcx, rcy, rcx + 5, rcy - 3, RED_MID)
            c.circle(rcx, rcy, 2, OUTLINE)
        elif theme["right_crest"] == "candle":
            # Candle
            c.rect(rcx - 3, rcy - 2, 6, 12, WHITE_MID, outline=OUTLINE)
            c.line(rcx, rcy - 5, rcx, rcy - 2, OUTLINE)
            c.circle(rcx, rcy - 7, 3, YELLOW_MID, outline=OUTLINE)
            c.set_pixel(rcx, rcy - 8, PURE_WHITE)

        # Header Ribbon Tab (Center top)
        c.rect(200, fy + 1, 80, 8, theme["ribbon"], outline=OUTLINE)
        c.line(201, fy + 2, 278, fy + 2, theme["outer_rim"])
        # Footer Ribbon Tab (Center bottom)
        c.rect(200, fy + fh - 9, 80, 8, theme["ribbon"], outline=OUTLINE)

        frames.append(c)

    return frames

# ==============================================================================
# KITCHEN PARALLAX & FOREGROUND LAYERS
# ==============================================================================

def generate_kitchen_sky_gradient() -> PixelCanvas:
    """1x540 px: 8 hard color bands of warm kitchen ambient light."""
    c = PixelCanvas(1, 540)
    bands = [
        (0, 68, K_FLOUR_PALE),     # Band 0: Ceiling light core
        (68, 136, YELLOW_LIGHT),   # Band 1: Warm ambient yellow
        (136, 203, YELLOW_MID),    # Band 2: Golden kitchen light
        (203, 270, K_EGG_YELLOW),  # Band 3: Rich yolk tone
        (270, 338, K_TOAST_GLOW),  # Band 4: Warm toast glow
        (338, 406, K_TERRACOTTA),  # Band 5: Warm terracotta
        (406, 473, K_COFFEE_DARK), # Band 6: Deep coffee brown
        (473, 540, OUTLINE),       # Band 7: Deepest shadow floor
    ]
    for y_start, y_end, col in bands:
        for y in range(y_start, y_end):
            c.set_pixel(0, y, col)
    return c


def generate_kitchen_bg_far() -> PixelCanvas:
    """
    960x540 px: Far background kitchen wall.
    - Cream tile pattern with grout lines
    - Ceiling moulding and pendant lamp
    - Upper wooden cabinets
    - Stainless stove hood
    - Wall calendar & chalkboard
    - Archway door
    - Large double-door fridge with kid drawings and alphabet magnets
    """
    c = PixelCanvas(960, 540, K_CREAM_LIGHT)

    # 1. Seamless 24x24 Cream Tile Pattern across wall (y=16..470)
    for y in range(16, 470):
        for x in range(960):
            gx = x % 24
            gy = (y - 16) % 24
            if gx == 0 or gy == 0:
                c.set_pixel(x, y, K_CREAM_SHADOW)
            elif (x // 24 + (y - 16) // 24) % 2 == 1:
                if (gx + gy) % 6 == 0:
                    c.set_pixel(x, y, DUSK_CREAM)

    # 2. Ceiling Crown Moulding (y=0..16)
    c.rect(0, 0, 960, 2, OUTLINE)
    c.rect(0, 2, 960, 3, K_COFFEE_DARK)
    c.rect(0, 5, 960, 3, BROWN_MID)
    c.rect(0, 8, 960, 3, WOOD_HIGHLIGHT)
    c.rect(0, 11, 960, 3, BROWN_LIGHT)
    c.rect(0, 14, 960, 2, OUTLINE)

    # 3. Upper Kitchen Cabinets
    # Left bank (x=60..400, y=20..140)
    c.rect(60, 20, 340, 120, BROWN_MID, outline=OUTLINE)
    c.line(61, 21, 399, 21, WOOD_HIGHLIGHT)
    c.line(61, 21, 61, 139, WOOD_HIGHLIGHT)
    # 4 Cabinet doors (each 80px wide)
    for i in range(4):
        dx = 65 + i * 82
        c.rect(dx, 25, 76, 110, BROWN_LIGHT, outline=OUTLINE)
        c.rect(dx + 6, 31, 64, 98, BROWN_MID, outline=BROWN_DARKEST)
        c.line(dx + 7, 32, dx + 69, 32, WOOD_HIGHLIGHT)
        # Brass knob handle
        kx = dx + 68 if i % 2 == 0 else dx + 8
        c.circle(kx, 85, 3, K_EGG_YELLOW, outline=OUTLINE)
        c.set_pixel(kx, 84, PURE_WHITE)

    # Right bank (x=620..900, y=20..140)
    c.rect(620, 20, 280, 120, BROWN_MID, outline=OUTLINE)
    c.line(621, 21, 899, 21, WOOD_HIGHLIGHT)
    c.line(621, 21, 621, 139, WOOD_HIGHLIGHT)
    for i in range(3):
        dx = 628 + i * 88
        c.rect(dx, 25, 80, 110, BROWN_LIGHT, outline=OUTLINE)
        c.rect(dx + 6, 31, 68, 98, BROWN_MID, outline=BROWN_DARKEST)
        c.line(dx + 7, 32, dx + 73, 32, WOOD_HIGHLIGHT)
        kx = dx + 72 if i % 2 == 0 else dx + 8
        c.circle(kx, 85, 3, K_EGG_YELLOW, outline=OUTLINE)
        c.set_pixel(kx, 84, PURE_WHITE)

    # 4. Stove Exhaust Hood (x=450..580, y=40..150)
    c.polygon([(475, 40), (555, 40), (580, 140), (450, 140)], K_STEEL_MID, outline=OUTLINE)
    c.line(476, 41, 554, 41, K_STEEL_SPECULAR)
    c.line(476, 42, 451, 139, K_STEEL_SPECULAR)
    # Bottom grease filter grates
    c.rect(452, 140, 126, 10, K_CAST_IRON, outline=OUTLINE)
    for fx in range(460, 570, 8):
        c.line(fx, 142, fx, 148, OUTLINE)
    # Control panel on front
    c.rect(480, 120, 70, 12, OUTLINE)
    for bx in range(488, 545, 14):
        c.circle(bx, 126, 2, K_STEEL_SPECULAR, outline=OUTLINE)
    c.set_pixel(542, 126, RED_MID) # power LED

    # 5. Hanging Pendant Ceiling Light (x=495..535, y=0..85)
    c.line(515, 14, 515, 60, OUTLINE)
    c.line(516, 14, 516, 60, K_CAST_IRON)
    # Brass cap & glass dome
    c.circle(515, 62, 5, K_EGG_YELLOW, outline=OUTLINE)
    c.polygon([(495, 80), (535, 80), (525, 65), (505, 65)], K_EGG_YELLOW, outline=OUTLINE)
    c.line(496, 79, 534, 79, K_FLOUR_PALE)
    c.circle(515, 83, 6, PURE_WHITE, outline=K_TOAST_GLOW)

    # 6. Wall Calendar (x=160..245, y=165..255)
    c.rect(160, 165, 85, 90, PURE_WHITE, outline=OUTLINE)
    c.rect(160, 165, 85, 18, RED_MID, outline=OUTLINE)
    # Red header text line
    c.line(175, 174, 230, 174, PURE_WHITE)
    # Calendar date grid
    for row in range(4):
        for col in range(6):
            cx_d = 168 + col * 12
            cy_d = 192 + row * 14
            c.set_pixel(cx_d, cy_d, OUTLINE)
    # Red circled important date!
    c.circle(192, 206, 5, RED_LIGHT, outline=RED_MID)

    # 7. Framed Chalkboard / Grocery List (x=275..395, y=165..275)
    c.rect(275, 165, 120, 110, BROWN_MID, outline=BROWN_DARKEST)
    c.line(275, 165, 394, 165, WOOD_HIGHLIGHT)
    c.line(275, 165, 275, 274, WOOD_HIGHLIGHT)
    c.rect(281, 171, 108, 98, GREEN_DEEP, outline=OUTLINE)
    # White chalk text lines & checkboxes
    for cy_l in range(182, 255, 12):
        c.rect(287, cy_l, 6, 6, PURE_WHITE, outline=OUTLINE)
        c.set_pixel(289, cy_l + 2, K_MINT_HIGHLIGHT) # checkmark
        c.line(297, cy_l + 3, 350, cy_l + 3, PURE_WHITE)
    # Chalk doodle cookie
    c.circle(368, 240, 10, K_FLOUR_PALE, outline=PURE_WHITE)
    c.set_pixel(366, 238, BROWN_DARK)
    c.set_pixel(370, 239, BROWN_DARK)
    c.set_pixel(368, 243, BROWN_DARK)

    # 8. Archway Doorway (x=20..115, y=120..470)
    c.rect(20, 120, 95, 350, BROWN_MID, outline=OUTLINE)
    c.line(21, 121, 114, 121, WOOD_HIGHLIGHT)
    c.rect(28, 128, 79, 342, SHADOW_PURPLE_DARK, outline=OUTLINE)
    c.rect(34, 134, 67, 336, PURPLE_MID) # warm dining room interior glow

    # 9. Large Retro Refrigerator (x=680..910, y=95..470)
    c.rect(680, 95, 230, 375, K_CREAM_LIGHT, outline=OUTLINE)
    c.line(681, 96, 909, 96, PURE_WHITE)
    c.line(681, 96, 681, 469, PURE_WHITE)
    c.line(909, 96, 909, 469, K_CREAM_SHADOW)
    # Door separation gap (Freezer top y=95..210, Fridge bottom y=216..470)
    c.line(680, 212, 910, 212, OUTLINE)
    c.line(680, 213, 910, 213, K_CREAM_SHADOW)
    c.line(680, 215, 910, 215, OUTLINE)
    # Chrome Handles
    c.rect(692, 160, 8, 45, K_STEEL_MID, outline=OUTLINE)
    c.line(693, 161, 693, 204, K_STEEL_SPECULAR)
    c.rect(692, 225, 8, 80, K_STEEL_MID, outline=OUTLINE)
    c.line(693, 226, 693, 304, K_STEEL_SPECULAR)

    # Kid Drawing 1: Crayon House (x=725..785, y=240..300)
    c.rect(725, 240, 60, 60, PURE_WHITE, outline=WHITE_SHADOW)
    # Magnet pin at top
    c.circle(755, 242, 3, RED_MID, outline=OUTLINE)
    # Crayon house drawing
    c.polygon([(740, 265), (770, 265), (755, 250)], RED_MID, outline=OUTLINE)
    c.rect(743, 265, 24, 25, YELLOW_MID, outline=OUTLINE)
    c.rect(751, 275, 8, 15, BROWN_MID) # door
    c.circle(775, 250, 5, K_EGG_YELLOW) # yellow sun

    # Kid Drawing 2: Crayon Dinosaur (x=805..875, y=250..315)
    c.rect(805, 250, 70, 65, PURE_WHITE, outline=WHITE_SHADOW)
    c.circle(840, 252, 3, BLUE_MID, outline=OUTLINE)
    # Green Dino
    c.circle(840, 285, 12, GREEN_MID, outline=GREEN_SHADOW)
    c.circle(852, 276, 8, GREEN_MID, outline=GREEN_SHADOW)
    c.line(828, 288, 818, 295, GREEN_MID) # tail
    # Orange back spikes
    c.set_pixel(836, 272, ORANGE_MID)
    c.set_pixel(842, 272, ORANGE_MID)
    c.set_pixel(848, 274, ORANGE_MID)

    # Colorful Alphabet Fridge Magnets
    # "Y" (Yellow)
    c.rect(720, 130, 8, 12, K_EGG_YELLOW, outline=OUTLINE)
    # "S" (Teal)
    c.rect(734, 130, 8, 12, TEAL_MID, outline=OUTLINE)
    # "1" (Red)
    c.rect(760, 140, 6, 12, RED_MID, outline=OUTLINE)
    # "2" (Blue)
    c.rect(772, 140, 8, 12, BLUE_MID, outline=OUTLINE)
    # "3" (Green)
    c.rect(786, 140, 8, 12, GREEN_MID, outline=OUTLINE)
    # Star magnet
    c.circle(830, 145, 5, K_TOAST_GLOW, outline=OUTLINE)

    # 10. Baseboard Moulding (y=470..540)
    c.rect(0, 470, 960, 8, BROWN_DARK, outline=OUTLINE)
    c.line(0, 471, 959, 471, WOOD_HIGHLIGHT)
    c.rect(0, 478, 960, 62, BROWN_MID)
    for x in range(0, 960, 32):
        c.line(x, 478, x, 539, BROWN_DARK)

    return c


def generate_kitchen_bg_far_anim() -> List[PixelCanvas]:
    """
    3840x540 px (4 frames of 960x540 @ 3 fps):
    Ambient motion overlay:
    - Pilot light flicker under stove hood
    - Gentle steam wisps rising from stove
    - Ceiling pendant light gentle ambient glow pulse
    """
    frames = []

    for f in range(4):
        c = PixelCanvas(960, 540, TRANSPARENT)

        # 1. Pilot Light Flicker (x=515, y=148)
        flame_colors = [BLUE_LIGHT, YELLOW_LIGHT, K_EGG_YELLOW, PURE_WHITE]
        c.circle(515, 147, 2 + (f % 2), flame_colors[f])
        c.set_pixel(515, 146 - (f % 2), PURE_WHITE)

        # 2. Gentle Steam Wisps (x=505..535, y=70..140)
        # Rising wisps with drift offset per frame
        for i in range(3):
            base_x = 510 + i * 8
            wisp_y = 135 - f * 8 - i * 16
            if 60 <= wisp_y <= 140:
                curl_x = base_x + int(math.sin((wisp_y + f * 10) * 0.1) * 6)
                c.circle(curl_x, wisp_y, 3 + (i % 2), K_FLOUR_PALE)
                c.set_pixel(curl_x, wisp_y, PURE_WHITE)

        # 3. Pendant Lamp Ambient Glow Pulse
        # 1px warm halo expanding/contracting
        glow_r = 10 + f
        c.circle(515, 83, glow_r, K_FLOUR_PALE)
        c.circle(515, 83, glow_r - 2, TRANSPARENT) # ring only

        frames.append(c)

    return frames


def generate_kitchen_bg_mid() -> PixelCanvas:
    """
    1280x540 px: Mid-ground kitchen scene.
    - Seamless horizontal tiling at floor level y=400 (x=0 matches x=1279).
    - Pantry shelves (x=50..220, y=100..400)
    - Refrigerator (x=260..450, y=110..400)
    - Counter with bread box & cutting board (x=490..690, y=220..400)
    - Range stove & oven (x=730..930, y=220..400)
    - Sink counter with dish drying rack (x=970..1130, y=220..400)
    - Rolling butcher block cart (x=1160..1230, y=260..400)
    """
    c = PixelCanvas(1280, 540, TRANSPARENT)

    # 1. TALL PANTRY SHELVES (x=50..220, y=100..400)
    # Wooden frame uprights
    c.rect(50, 100, 12, 300, BROWN_MID, outline=OUTLINE)
    c.line(51, 101, 51, 399, WOOD_HIGHLIGHT)
    c.rect(208, 100, 12, 300, BROWN_MID, outline=OUTLINE)
    c.line(209, 101, 209, 399, WOOD_HIGHLIGHT)
    # Dark shadow backing
    c.rect(62, 100, 146, 300, SHADOW_PURPLE_DEEP)

    # 4 Shelves (y=160, y=230, y=300, y=390)
    for sy in [160, 230, 300, 390]:
        c.rect(50, sy, 170, 10, BROWN_MID, outline=OUTLINE)
        c.line(51, sy + 1, 219, sy + 1, WOOD_HIGHLIGHT)
        c.line(51, sy + 9, 219, sy + 9, BROWN_DARKEST)

    # Shelf 1: Colorful cereal boxes (x=70..195, y=120..160)
    c.rect(70, 120, 24, 40, RED_MID, outline=OUTLINE)
    c.line(72, 122, 72, 158, RED_LIGHT)
    c.rect(100, 115, 26, 45, YELLOW_MID, outline=OUTLINE)
    c.line(102, 117, 102, 158, YELLOW_LIGHT)
    c.rect(132, 125, 22, 35, BLUE_MID, outline=OUTLINE)
    c.rect(160, 118, 28, 42, GREEN_MID, outline=OUTLINE)

    # Shelf 2: Glass pasta & sauce jars (x=68..200, y=190..230)
    # Jar 1: Yellow pasta spirals
    c.rect(72, 195, 26, 35, WHITE_SHADOW, outline=OUTLINE)
    c.rect(74, 200, 22, 28, YELLOW_MID)
    c.rect(76, 190, 18, 5, BROWN_MID, outline=OUTLINE) # wooden lid
    # Jar 2: Red tomato sauce
    c.rect(112, 198, 24, 32, WHITE_SHADOW, outline=OUTLINE)
    c.rect(114, 202, 20, 26, K_JAM_RED)
    c.rect(115, 193, 18, 5, K_EGG_YELLOW, outline=OUTLINE)
    # Jar 3: Olive oil
    c.rect(150, 185, 20, 45, WHITE_SHADOW, outline=OUTLINE)
    c.rect(152, 192, 16, 36, K_OLIVE_GREEN)
    c.rect(154, 180, 12, 5, BROWN_MID, outline=OUTLINE)

    # Shelf 3: Canned goods (x=68..200, y=265..300)
    for idx, (col_m, col_l) in enumerate([(RED_MID, RED_LIGHT), (GREEN_MID, GREEN_LIGHT), (K_EGG_YELLOW, YELLOW_LIGHT), (BLUE_MID, BLUE_LIGHT)]):
        can_x = 72 + idx * 32
        c.rect(can_x, 270, 26, 30, col_m, outline=OUTLINE)
        c.line(can_x + 2, 272, can_x + 24, 272, col_l)
        c.rect(can_x, 266, 26, 4, K_STEEL_MID, outline=OUTLINE) # silver top

    # Shelf 4: Sack of flour & spice jars (x=68..200, y=340..390)
    # Flour sack
    c.polygon([(75, 390), (120, 390), (115, 345), (80, 345)], K_FLOUR_PALE, outline=OUTLINE)
    c.line(82, 346, 113, 346, PURE_WHITE)
    c.line(85, 365, 110, 365, RED_MID) # label
    # Spice rack
    c.rect(135, 355, 65, 35, BROWN_LIGHT, outline=OUTLINE)
    for sp_x in range(140, 195, 12):
        c.rect(sp_x, 348, 8, 18, K_STEEL_SPECULAR, outline=OUTLINE)
        c.rect(sp_x + 1, 343, 6, 5, BROWN_MID, outline=OUTLINE)

    # 2. RETRO REFRIGERATOR (x=260..450, y=110..400)
    c.rect(260, 110, 190, 290, K_CREAM_LIGHT, outline=OUTLINE)
    c.line(261, 111, 449, 111, PURE_WHITE)
    c.line(261, 111, 261, 399, PURE_WHITE)
    c.line(449, 111, 449, 399, K_CREAM_SHADOW)
    # Door seam
    c.line(260, 210, 450, 210, OUTLINE)
    c.line(260, 212, 450, 212, OUTLINE)
    # Chrome pull bars
    c.rect(275, 150, 8, 45, K_STEEL_MID, outline=OUTLINE)
    c.line(276, 151, 276, 194, K_STEEL_SPECULAR)
    c.rect(275, 230, 8, 90, K_STEEL_MID, outline=OUTLINE)
    c.line(276, 231, 276, 319, K_STEEL_SPECULAR)
    # Timer & magnetic note
    c.circle(350, 160, 12, RED_MID, outline=OUTLINE)
    c.circle(350, 160, 9, PURE_WHITE)
    c.line(350, 160, 355, 157, OUTLINE)
    c.rect(385, 145, 30, 35, K_EGG_YELLOW, outline=OUTLINE)

    # 3. KITCHEN COUNTER WITH PREP STATION (x=490..690, y=220..400)
    # Countertop (marble laminate)
    c.rect(486, 220, 208, 14, PURE_WHITE, outline=OUTLINE)
    c.line(487, 221, 693, 221, K_CREAM_LIGHT)
    c.line(487, 233, 693, 233, WHITE_SHADOW)
    # Wooden drawers below
    c.rect(490, 234, 200, 166, BROWN_MID, outline=OUTLINE)
    # 4 Drawers
    for dry in range(240, 380, 40):
        c.rect(498, dry, 184, 34, BROWN_LIGHT, outline=OUTLINE)
        c.line(499, dry + 1, 681, dry + 1, WOOD_HIGHLIGHT)
        # Brass cup pull
        c.rect(580, dry + 14, 20, 6, K_EGG_YELLOW, outline=OUTLINE)
        c.set_pixel(582, dry + 15, PURE_WHITE)

    # Countertop Items:
    # Stainless bread box (x=505..565, y=185..220)
    c.rect(505, 185, 60, 35, K_STEEL_MID, outline=OUTLINE)
    c.line(506, 186, 564, 186, K_STEEL_SPECULAR)
    c.rect(512, 195, 46, 20, K_STEEL_SPECULAR, outline=OUTLINE) # roll-top slats
    c.line(512, 204, 558, 204, K_CAST_IRON) # handle

    # Wooden cutting board with bread & cheese (x=580..645, y=210..220)
    c.rect(580, 214, 65, 6, WOOD_LIT, outline=OUTLINE)
    # Crusty sliced loaf
    c.circle(595, 210, 10, K_COFFEE_DARK, outline=OUTLINE)
    c.circle(593, 210, 8, WOOD_LIT)
    # Cheese wedge
    c.polygon([(620, 214), (642, 214), (635, 200)], K_EGG_YELLOW, outline=OUTLINE)
    c.circle(628, 208, 2, K_TOAST_GLOW) # hole

    # Knife block (x=655..680, y=185..220)
    c.polygon([(655, 220), (680, 220), (675, 190), (660, 195)], BROWN_DARK, outline=OUTLINE)
    for k_off in range(3):
        c.line(662 + k_off * 4, 193 - k_off * 2, 658 + k_off * 4, 182 - k_off * 2, K_CAST_IRON) # handles

    # 4. RANGE STOVE & OVEN (x=730..930, y=220..400)
    c.rect(730, 220, 200, 180, K_STEEL_MID, outline=OUTLINE)
    c.line(731, 221, 929, 221, K_STEEL_SPECULAR)
    # Cooktop surface
    c.rect(730, 220, 200, 12, K_CAST_IRON, outline=OUTLINE)
    # 4 burner grates
    for bx in [755, 805, 855, 905]:
        c.circle(bx, 226, 6, OUTLINE)
        c.circle(bx, 226, 3, K_CAST_IRON)

    # Stovetop Stockpot (x=790..830, y=190..220)
    c.rect(792, 198, 36, 22, K_TERRACOTTA, outline=OUTLINE)
    c.line(793, 199, 827, 199, K_TOAST_GLOW)
    c.rect(788, 204, 5, 8, K_STEEL_MID, outline=OUTLINE) # loop handle left
    c.rect(827, 204, 5, 8, K_STEEL_MID, outline=OUTLINE) # loop handle right
    c.circle(810, 196, 4, K_STEEL_SPECULAR, outline=OUTLINE) # lid knob

    # Control dials strip
    c.rect(734, 234, 192, 18, K_CAST_IRON, outline=OUTLINE)
    for dx in range(745, 920, 32):
        c.circle(dx, 243, 5, K_STEEL_SPECULAR, outline=OUTLINE)
        c.set_pixel(dx, 240, RED_MID)

    # Glass Oven Door
    c.rect(744, 260, 172, 110, K_CAST_IRON, outline=OUTLINE)
    c.rect(756, 272, 148, 86, OUTLINE)
    c.rect(760, 276, 140, 78, SHADOW_PURPLE_DARK) # inner dark cavity
    # Warm glowing oven rack inside
    c.line(764, 315, 896, 315, K_TOAST_GLOW)
    c.line(764, 316, 896, 316, K_EGG_YELLOW)
    # Oven door handle
    c.rect(760, 264, 140, 6, K_STEEL_SPECULAR, outline=OUTLINE)

    # 5. SINK COUNTER WITH DISH DRYING RACK (x=970..1130, y=220..400)
    c.rect(970, 220, 160, 180, BROWN_MID, outline=OUTLINE)
    c.rect(966, 220, 168, 14, PURE_WHITE, outline=OUTLINE) # counter rim
    # Stainless double sink basin
    c.rect(980, 224, 70, 10, K_CAST_IRON, outline=OUTLINE)
    # Tall gooseneck faucet (x=1010..1025, y=175..220)
    for fy in range(185, 220):
        c.set_pixel(1015, fy, K_STEEL_SPECULAR)
        c.set_pixel(1016, fy, K_STEEL_MID)
    c.circle(1012, 185, 6, K_STEEL_SPECULAR, outline=OUTLINE)
    c.line(1008, 185, 1008, 195, K_STEEL_SPECULAR) # spout nozzle

    # Dish drying rack (x=1055..1125, y=190..220)
    c.rect(1055, 212, 70, 8, K_STEEL_MID, outline=OUTLINE)
    # Stacked colorful plates
    plate_colors = [RED_MID, BLUE_MID, YELLOW_MID, K_MINT_HIGHLIGHT]
    for p_idx, p_col in enumerate(plate_colors):
        c.rect(1060 + p_idx * 10, 192, 4, 20, p_col, outline=OUTLINE)
    # Mug on rack
    c.rect(1105, 200, 16, 14, TEAL_MID, outline=OUTLINE)
    c.rect(1121, 204, 4, 8, TEAL_MID, outline=OUTLINE) # handle

    # 6. ROLLING BUTCHER BLOCK CART (x=1160..1235, y=250..400)
    # Thick butcher block top
    c.rect(1160, 250, 75, 16, WOOD_LIT, outline=OUTLINE)
    c.line(1161, 251, 1234, 251, WOOD_HIGHLIGHT)
    # Legs
    c.rect(1164, 266, 8, 126, BROWN_MID, outline=OUTLINE)
    c.rect(1223, 266, 8, 126, BROWN_MID, outline=OUTLINE)
    # Lower wire shelf
    c.rect(1164, 340, 67, 6, K_STEEL_MID, outline=OUTLINE)
    # Fruit bowl on top (x=1175..1220, y=230..250)
    c.circle(1197, 245, 18, WHITE_MID, outline=OUTLINE)
    # Oranges & apples in bowl
    c.circle(1190, 240, 6, ORANGE_MID, outline=OUTLINE)
    c.circle(1202, 239, 6, RED_MID, outline=OUTLINE)
    c.circle(1196, 235, 5, K_EGG_YELLOW, outline=OUTLINE)
    # Caster wheels at y=400
    c.circle(1168, 396, 4, K_CAST_IRON, outline=OUTLINE)
    c.circle(1227, 396, 4, K_CAST_IRON, outline=OUTLINE)

    # Floor Contact Drop Shadows across all furniture at y=400
    for x in range(50, 1240):
        c.set_pixel(x, 400, OUTLINE)
        c.set_pixel(x, 401, SHADOW_PURPLE_DARK)

    return c


def generate_kitchen_bg_near() -> PixelCanvas:
    """
    960x540 px: Foreground silhouettes layer.
    - STRICT: Transparent above floor line y=400 (y=0..399 is 100% transparent!).
    - Dark silhouettes of kitchen chairs, trash can, stool with 1px warm rim light.
    """
    c = PixelCanvas(960, 540, TRANSPARENT)
    SIL = VOID_BLACK
    RIM = K_TOAST_GLOW

    # 1. Dining Chair 1 (x=50..160, y=410..535)
    # Seat profile
    c.rect(60, 430, 90, 16, SIL)
    c.line(60, 430, 150, 430, RIM)
    # Backrest spindles
    for sx in range(65, 145, 16):
        c.rect(sx, 405, 8, 30, SIL)
        c.line(sx, 405, sx, 435, RIM)
    # Turned legs
    for lx in [65, 135]:
        for ly in range(446, 535):
            hw = 6 + int(math.sin((ly - 446) * 0.15) * 3)
            c.line(lx - hw, ly, lx + hw, ly, SIL)
            c.set_pixel(lx - hw, ly, RIM)

    # 2. Kitchen Step Trash Can (x=230..320, y=415..535)
    # Cylindrical body
    c.polygon([(240, 435), (310, 435), (305, 530), (245, 530)], SIL)
    c.line(240, 435, 245, 530, RIM)
    # Dome Lid
    c.circle(275, 430, 32, SIL)
    # Erase below 430 for dome top
    for ey in range(431, 465):
        for ex in range(240, 310):
            pass # keep dome
    c.line(245, 420, 275, 402, RIM) # dome top rim
    # Foot pedal on right
    c.rect(305, 520, 15, 8, SIL)
    c.line(305, 520, 320, 520, RIM)

    # 3. Wooden Two-Step Kitchen Stool (x=410..520, y=410..535)
    # Step 1 (top tread)
    c.rect(420, 415, 85, 14, SIL)
    c.line(420, 415, 505, 415, RIM)
    # Step 2 (middle tread)
    c.rect(400, 465, 105, 14, SIL)
    c.line(400, 465, 505, 465, RIM)
    # Stool legs & side uprights
    c.polygon([(425, 429), (410, 535), (430, 535), (440, 429)], SIL)
    c.line(425, 429, 410, 535, RIM)
    c.polygon([(480, 429), (495, 535), (515, 535), (495, 429)], SIL)
    c.line(480, 429, 495, 535, RIM)

    # 4. Dining Chair 2 (tilted slightly, x=620..740, y=410..535)
    c.rect(630, 435, 95, 16, SIL)
    c.line(630, 435, 725, 435, RIM)
    for sx in range(635, 720, 18):
        c.rect(sx, 408, 8, 30, SIL)
        c.line(sx, 408, sx, 438, RIM)
    for lx in [640, 710]:
        for ly in range(451, 535):
            c.rect(lx - 4, ly, 8, 1, SIL)
            c.set_pixel(lx - 4, ly, RIM)

    # 5. Recycling Bin with Jug Silhouette (x=800..915, y=420..535)
    c.polygon([(810, 450), (905, 450), (895, 532), (820, 532)], SIL)
    c.line(810, 450, 905, 450, RIM)
    c.line(810, 450, 820, 532, RIM)
    # Milk jug neck & handle peeking out of bin
    c.rect(830, 425, 20, 26, SIL)
    c.line(830, 425, 850, 425, RIM)
    c.line(830, 425, 830, 451, RIM)
    c.rect(845, 430, 8, 16, SIL) # jug handle loop

    # STRICT RULE CHECK: Wipe any pixels above y=400 just in case
    for y in range(0, 400):
        for x in range(960):
            c.set_pixel(x, y, TRANSPARENT)

    return c


def generate_kitchen_fg_legs() -> PixelCanvas:
    """960x540 px: Foreground silhouettes of table legs and stool legs."""
    c = PixelCanvas(960, 540, TRANSPARENT)
    SIL = VOID_BLACK
    RIM = K_TOAST_GLOW

    # 1. Dining Table Turned Leg (x=10..90, y=280..540)
    c.rect(0, 280, 110, 22, SIL)
    c.line(0, 280, 110, 280, RIM)
    for ly in range(302, 540):
        if ly < 350:
            hw = 16 + int(math.sin((ly - 302) * 0.14) * 6)
        elif ly < 420:
            hw = 24 + int(math.sin((ly - 350) * 0.09) * 8)
        elif ly < 490:
            hw = 15 + int(math.sin((ly - 420) * 0.12) * 5)
        else:
            hw = 22 + int(math.sin((ly - 490) * 0.08) * 7)
        c.line(45 - hw, ly, 45 + hw, ly, SIL)
        c.set_pixel(45 - hw, ly, RIM)

    # 2. Slanted Chair Leg (x=170..220, y=360..540)
    for ly in range(360, 540):
        lx = int(175 + (ly - 360) * 0.2)
        c.line(lx, ly, lx + 14, ly, SIL)
        c.set_pixel(lx, ly, RIM)

    # 3. Bar Stool Leg with Rung (x=490..560, y=320..540)
    for ly in range(320, 540):
        c.rect(518, ly, 12, 1, SIL)
        c.set_pixel(518, ly, RIM)
    # Round Footrest Rung
    c.rect(485, 460, 75, 10, SIL)
    c.line(485, 460, 560, 460, RIM)

    # 4. Island Table Leg & Apron (x=800..930, y=290..540)
    c.rect(800, 290, 160, 20, SIL)
    c.line(800, 290, 960, 290, RIM)
    for ly in range(310, 540):
        hw = 18 + int(math.sin((ly - 310) * 0.1) * 6)
        c.line(870 - hw, ly, 870 + hw, ly, SIL)
        c.set_pixel(870 - hw, ly, RIM)

    return c


def generate_kitchen_fg_dust() -> PixelCanvas:
    """960x540 px: Foreground flour dust particles & drifting steam wisps (hard-banded alpha)."""
    c = PixelCanvas(960, 540, TRANSPARENT)
    rgb_flour = K_FLOUR_PALE[:3] # (255, 242, 184)
    rgb_cream = K_CREAM_LIGHT[:3] # (247, 240, 223)

    # Round flour dust particles with hard-banded alpha (alphas: 40, 80, 140, 210)
    orbs = [
        (90, 120, 22, rgb_flour), (220, 360, 25, rgb_cream),
        (380, 160, 20, rgb_flour), (520, 410, 26, rgb_cream),
        (670, 140, 24, rgb_flour), (820, 340, 22, rgb_cream),
        (150, 240, 12, rgb_flour), (310, 190, 14, rgb_cream),
        (460, 280, 13, rgb_flour), (600, 220, 12, rgb_cream),
        (740, 270, 14, rgb_flour), (890, 180, 11, rgb_cream),
        (60, 450, 6, rgb_flour),   (180, 90, 5, rgb_cream),
        (420, 50, 6, rgb_flour),   (700, 480, 5, rgb_cream),
        (850, 70, 6, rgb_flour),   (920, 460, 5, rgb_cream),
    ]

    for cx, cy, r, rgb in orbs:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if 0 <= x < 960 and 0 <= y < 540:
                    d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    if d <= r:
                        if d > r * 0.75:
                            a = 40
                        elif d > r * 0.50:
                            a = 80
                        elif d > r * 0.25:
                            a = 140
                        else:
                            a = 210
                        if a > c.get_pixel(x, y)[3]:
                            c.set_pixel(x, y, (rgb[0], rgb[1], rgb[2], a))

    return c

# ==============================================================================
# KITCHEN TILESET & OBSTACLES
# ==============================================================================

def generate_kitchen_tileset_floor() -> PixelCanvas:
    """
    256x96 px (32x32 tiles, 8 cols x 3 rows).
    Row 0: Surface Tiles (Checkerboard tile with grout lines)
      Col 0: Standard checkerboard (cream & dark teal)
      Col 1: Alternate phase with circular floor drain
      Col 2: Left cliff edge facing a pit
      Col 3: Right cliff edge facing a pit
      Col 4: Scuffed tile with dropped fork scratch
      Col 5: Spilled jam stain
      Col 6: Cracked tile corner
      Col 7: Pristine tile with bright star glint
    Row 1: Subfloor joists, copper plumbing pipes, dropped macaroni
    Row 2: Deep gloom fade to void
    """
    c = PixelCanvas(256, 96, VOID_BLACK)

    # Helper: draw 32x32 checkerboard quadrant tile
    def draw_checker_quad(tx: int, ty: int, cream_first: bool = True):
        c1_main = K_CREAM_LIGHT if cream_first else K_TEAL_MID
        c1_sh = K_CREAM_SHADOW if cream_first else K_TEAL_DEEP
        c2_main = K_TEAL_MID if cream_first else K_CREAM_LIGHT
        c2_sh = K_TEAL_DEEP if cream_first else K_CREAM_SHADOW

        # Top-left quadrant (16x16)
        c.rect(tx, ty, 16, 16, c1_main)
        c.rect(tx + 1, ty + 15, 14, 1, c1_sh)
        c.rect(tx + 15, ty + 1, 1, 14, c1_sh)

        # Top-right quadrant (16x16)
        c.rect(tx + 16, ty, 16, 16, c2_main)
        c.rect(tx + 17, ty + 15, 14, 1, c2_sh)
        c.rect(tx + 31, ty + 1, 1, 14, c2_sh)

        # Bottom-left quadrant (16x16)
        c.rect(tx, ty + 16, 16, 16, c2_main)
        c.rect(tx + 1, ty + 31, 14, 1, c2_sh)
        c.rect(tx + 15, ty + 17, 1, 14, c2_sh)

        # Bottom-right quadrant (16x16)
        c.rect(tx + 16, ty + 16, 16, 16, c1_main)
        c.rect(tx + 17, ty + 31, 14, 1, c1_sh)
        c.rect(tx + 31, ty + 17, 1, 14, c1_sh)

        # Grout lines (1px OUTLINE)
        c.line(tx, ty, tx + 31, ty, OUTLINE)
        c.line(tx, ty + 16, tx + 31, ty + 16, OUTLINE)
        c.line(tx, ty, tx, ty + 31, OUTLINE)
        c.line(tx + 16, ty, tx + 16, ty + 31, OUTLINE)

        # Wax shine top 2px lip (y=0..1)
        for x in range(tx, tx + 32):
            if x % 4 in [0, 1]:
                c.set_pixel(x, ty, PURE_WHITE)
                c.set_pixel(x, ty + 1, K_MINT_HIGHLIGHT if (x % 3 == 0) else K_CREAM_LIGHT)

    # --- ROW 0: SURFACE TILES (y=0..31) ---
    # Col 0: Standard
    draw_checker_quad(0, 0, True)

    # Col 1: Alternate phase with circular floor drain
    draw_checker_quad(32, 0, False)
    # Circular drain insert
    c.circle(48, 16, 7, K_CAST_IRON, outline=OUTLINE)
    c.circle(48, 16, 4, OUTLINE)
    for dx_d in [-3, 0, 3]:
        c.line(48 + dx_d, 13, 48 + dx_d, 19, OUTLINE)

    # Col 2: Left cliff edge
    draw_checker_quad(64, 0, True)
    # Exposed cliff bevel on left (x=64..66)
    c.rect(64, 0, 3, 32, OUTLINE)
    c.line(65, 0, 65, 31, K_STEEL_MID)
    c.line(66, 0, 66, 31, BROWN_DARK)

    # Col 3: Right cliff edge
    draw_checker_quad(96, 0, True)
    # Exposed cliff bevel on right (x=125..127)
    c.rect(125, 0, 3, 32, OUTLINE)
    c.line(126, 0, 126, 31, K_STEEL_MID)
    c.line(125, 0, 125, 31, BROWN_DARK)

    # Col 4: Scuffed tile
    draw_checker_quad(128, 0, True)
    # Scratch gouges
    c.line(135, 10, 148, 22, K_STEEL_MID)
    c.line(136, 11, 149, 23, OUTLINE)
    c.line(142, 8, 152, 18, K_STEEL_MID)

    # Col 5: Spilled jam stain
    draw_checker_quad(160, 0, False)
    c.circle(176, 18, 6, K_JAM_RED, outline=OUTLINE)
    c.circle(174, 16, 2, RED_LIGHT)
    c.circle(184, 23, 2, K_JAM_RED, outline=OUTLINE)

    # Col 6: Cracked tile corner
    draw_checker_quad(192, 0, True)
    # Jagged crack line
    crack_pts = [(192, 22), (200, 24), (206, 18), (214, 20), (220, 14)]
    for i in range(len(crack_pts) - 1):
        c.line(crack_pts[i][0], crack_pts[i][1], crack_pts[i+1][0], crack_pts[i+1][1], OUTLINE)

    # Col 7: Pristine tile with bright star glint
    draw_checker_quad(224, 0, True)
    # 4-point star glint at (240, 12)
    c.line(240, 8, 240, 16, PURE_WHITE)
    c.line(236, 12, 244, 12, PURE_WHITE)
    c.circle(240, 12, 2, PURE_WHITE)
    c.set_pixel(239, 11, K_MINT_HIGHLIGHT)

    # --- ROW 1: MID-FILL SUBFLOOR JOISTS & PIPES (y=32..63) ---
    for col in range(8):
        tx = col * 32
        # Plywood subfloor underlayment (y=32..37)
        c.rect(tx, 32, 32, 6, BROWN_MID, outline=OUTLINE)
        c.line(tx, 33, tx + 31, 33, WOOD_HIGHLIGHT)

        # Vertical wooden joists / studs (y=38..63)
        c.rect(tx + 4, 38, 10, 26, BROWN_DARK, outline=OUTLINE)
        c.line(tx + 5, 38, tx + 5, 63, BROWN_LIGHT)
        c.rect(tx + 18, 38, 10, 26, BROWN_DARK, outline=OUTLINE)
        c.line(tx + 19, 38, tx + 19, 63, BROWN_LIGHT)

        # Horizontal copper water pipe running through joists (y=48..53)
        c.rect(tx, 48, 32, 6, K_TERRACOTTA, outline=OUTLINE)
        c.line(tx, 49, tx + 31, 49, K_TOAST_GLOW)
        c.line(tx, 52, tx + 31, 52, K_COFFEE_DARK)

    # Dropped macaroni noodle on pipe in Col 3
    c.circle(112, 46, 3, K_EGG_YELLOW, outline=OUTLINE)

    # --- ROW 2: DEEP GLOOM VOID (y=64..95) ---
    for col in range(8):
        tx = col * 32
        c.rect(tx, 64, 32, 32, SHADOW_PURPLE_DARK)
        # Deep joist fade
        c.rect(tx + 5, 64, 8, 20, SHADOW_PURPLE_DEEP)
        # Cobweb in corners
        if col in [0, 4, 7]:
            c.line(tx, 64, tx + 10, 74, SHADOW_PURPLE_MID)
            c.line(tx + 10, 64, tx, 74, SHADOW_PURPLE_MID)
        # Fade to VOID_BLACK at bottom
        c.rect(tx, 84, 32, 12, VOID_BLACK)

    return c


def generate_kitchen_pit_bg() -> PixelCanvas:
    """32x128 px: Inside of a pit, tiles horizontally, dark plumbing pipes & floor joists."""
    c = PixelCanvas(32, 128, SHADOW_PURPLE_DARK)

    # Vertical wooden stud on left & right
    c.rect(0, 0, 6, 128, BROWN_DARK, outline=OUTLINE)
    c.line(1, 0, 1, 127, BROWN_MID)
    c.rect(26, 0, 6, 128, BROWN_DARK, outline=OUTLINE)
    c.line(27, 0, 27, 127, BROWN_MID)

    # Central dark brick / joist cavity
    c.rect(6, 0, 20, 128, SHADOW_PURPLE_DEEP)

    # Vertical Copper Pipe (x=12..18, y=0..128)
    c.rect(12, 0, 6, 128, K_TERRACOTTA, outline=OUTLINE)
    c.line(13, 0, 13, 127, K_TOAST_GLOW)
    c.line(16, 0, 16, 127, K_COFFEE_DARK)

    # Horizontal Pipe Elbow & Brass Valve Joint (y=48..60)
    c.rect(6, 50, 20, 8, K_TERRACOTTA, outline=OUTLINE)
    c.circle(15, 54, 5, K_EGG_YELLOW, outline=OUTLINE)
    c.circle(15, 54, 2, RED_MID)

    # Cast Iron Drain Pipe Section (y=85..110)
    c.rect(8, 88, 16, 20, K_CAST_IRON, outline=OUTLINE)
    c.line(9, 89, 23, 89, K_STEEL_MID)

    # Hanging water drop at y=118
    c.circle(15, 118, 2, K_MINT_HIGHLIGHT, outline=OUTLINE)
    c.set_pixel(15, 117, PURE_WHITE)

    return c


def generate_kitchen_obstacles() -> List[PixelCanvas]:
    """128x32 px (4 frames 32x32): 4 stackable obstacle block skins."""
    frames = []

    # Frame 0: Stacked cereal boxes
    c0 = PixelCanvas(32, 32, TRANSPARENT)
    # Box 1 (Bottom, y=16..31)
    c0.rect(2, 16, 28, 16, RED_MID, outline=OUTLINE)
    c0.line(3, 17, 29, 17, RED_LIGHT)
    c0.line(3, 17, 3, 30, RED_LIGHT)
    c0.rect(6, 20, 12, 8, YELLOW_MID, outline=OUTLINE) # mascot circle
    c0.circle(12, 24, 3, K_EGG_YELLOW)
    # Nutrition stripe
    c0.line(22, 19, 22, 28, PURE_WHITE)
    c0.line(24, 19, 24, 28, PURE_WHITE)

    # Box 2 (Top, y=0..15)
    c0.rect(4, 0, 26, 16, YELLOW_MID, outline=OUTLINE)
    c0.line(5, 1, 28, 1, YELLOW_LIGHT)
    c0.line(5, 1, 5, 14, YELLOW_LIGHT)
    c0.rect(8, 4, 10, 8, BLUE_MID, outline=OUTLINE)
    c0.line(21, 3, 21, 12, RED_MID)
    frames.append(c0)

    # Frame 1: Stacked pizza boxes
    c1 = PixelCanvas(32, 32, TRANSPARENT)
    for i in range(3):
        py = 22 - i * 10
        c1.rect(2, py, 28, 9, PURE_WHITE, outline=OUTLINE)
        c1.line(3, py + 1, 29, py + 1, K_CREAM_LIGHT)
        # Red chef logo & steam vent holes
        c1.circle(16, py + 4, 3, RED_MID)
        c1.set_pixel(16, py + 4, PURE_WHITE)
        c1.set_pixel(8, py + 4, OUTLINE) # vent hole
        c1.set_pixel(24, py + 4, OUTLINE)
    frames.append(c1)

    # Frame 2: Soup/Bean Cans stack
    c2 = PixelCanvas(32, 32, TRANSPARENT)
    # Can 1 (Left, 14x30)
    c2.rect(2, 2, 13, 29, K_JAM_RED, outline=OUTLINE)
    c2.line(3, 3, 3, 30, RED_LIGHT)
    c2.rect(2, 2, 13, 3, K_STEEL_MID, outline=OUTLINE) # silver rim
    c2.rect(2, 28, 13, 3, K_STEEL_MID, outline=OUTLINE)
    # White label center
    c2.rect(4, 10, 9, 12, PURE_WHITE)
    c2.line(5, 16, 11, 16, K_JAM_RED)

    # Can 2 (Right, 14x30)
    c2.rect(17, 2, 13, 29, K_OLIVE_GREEN, outline=OUTLINE)
    c2.line(18, 3, 18, 30, GREEN_LIGHT)
    c2.rect(17, 2, 13, 3, K_STEEL_MID, outline=OUTLINE)
    c2.rect(17, 28, 13, 3, K_STEEL_MID, outline=OUTLINE)
    c2.rect(19, 10, 9, 12, K_EGG_YELLOW)
    c2.line(20, 16, 26, 16, K_COFFEE_DARK)
    frames.append(c2)

    # Frame 3: Milk Crate
    c3 = PixelCanvas(32, 32, TRANSPARENT)
    c3.rect(2, 2, 28, 29, TEAL_MID, outline=OUTLINE)
    c3.line(3, 3, 29, 3, TEAL_LIGHT)
    c3.line(3, 3, 3, 29, TEAL_LIGHT)
    # Diamond cutout holes grid
    for cy_m in [10, 18, 24]:
        for cx_m in [8, 16, 24]:
            c3.rect(cx_m - 2, cy_m - 2, 4, 4, OUTLINE)
            c3.set_pixel(cx_m, cy_m, SHADOW_PURPLE_DARK)
    # Handle cutout at top
    c3.rect(10, 6, 12, 4, OUTLINE)
    frames.append(c3)

    return frames


def generate_kitchen_obstacles_tall() -> List[PixelCanvas]:
    """128x32 px (4 frames 32x32): 4 cap variants for tall stack."""
    frames = []

    # Frame 0: Open cereal top with spilling cereal loops
    c0 = PixelCanvas(32, 32, TRANSPARENT)
    # Lower box portion
    c0.rect(4, 16, 24, 16, YELLOW_MID, outline=OUTLINE)
    c0.line(5, 17, 5, 31, YELLOW_LIGHT)
    # Left flap folded out
    c0.polygon([(4, 16), (0, 8), (6, 8), (8, 16)], YELLOW_LIGHT, outline=OUTLINE)
    # Right flap folded out
    c0.polygon([(27, 16), (31, 8), (25, 8), (23, 16)], YELLOW_LIGHT, outline=OUTLINE)
    # Cereal loops spilling over
    c0.circle(12, 13, 3, RED_MID, outline=OUTLINE)
    c0.circle(17, 10, 3, BLUE_MID, outline=OUTLINE)
    c0.circle(21, 14, 3, K_EGG_YELLOW, outline=OUTLINE)
    c0.circle(15, 15, 2, GREEN_MID, outline=OUTLINE)
    frames.append(c0)

    # Frame 1: Pizza box flap with pizza slice
    c1 = PixelCanvas(32, 32, TRANSPARENT)
    c1.rect(2, 18, 28, 14, PURE_WHITE, outline=OUTLINE)
    # Half-open top lid (slanted)
    c1.polygon([(2, 18), (28, 10), (30, 13), (2, 21)], PURE_WHITE, outline=OUTLINE)
    c1.line(3, 19, 28, 11, K_CREAM_LIGHT)
    # Cheesy pizza slice peeking out
    c1.polygon([(10, 17), (24, 14), (20, 22)], K_EGG_YELLOW, outline=OUTLINE)
    c1.circle(15, 17, 2, K_JAM_RED) # pepperoni
    c1.circle(19, 16, 2, K_JAM_RED)
    frames.append(c1)

    # Frame 2: Pyramid can cap
    c2 = PixelCanvas(32, 32, TRANSPARENT)
    # Single tuna/soup can centered on top
    c2.rect(8, 10, 16, 21, K_JAM_RED, outline=OUTLINE)
    c2.line(9, 11, 9, 30, RED_LIGHT)
    c2.rect(8, 10, 16, 3, K_STEEL_MID, outline=OUTLINE)
    # Pull tab on lid
    c2.circle(16, 10, 3, K_STEEL_SPECULAR, outline=OUTLINE)
    c2.set_pixel(16, 10, OUTLINE)
    frames.append(c2)

    # Frame 3: Milk bottle in crate
    c3 = PixelCanvas(32, 32, TRANSPARENT)
    # Crate lower section
    c3.rect(2, 20, 28, 12, TEAL_MID, outline=OUTLINE)
    # Glass bottle neck & cap sticking out
    c3.rect(10, 8, 12, 16, WHITE_SHADOW, outline=OUTLINE)
    c3.line(11, 9, 11, 23, PURE_WHITE)
    c3.rect(12, 2, 8, 7, WHITE_SHADOW, outline=OUTLINE) # neck
    # Red foil cap
    c3.rect(11, 0, 10, 4, RED_MID, outline=OUTLINE)
    c3.line(12, 1, 19, 1, RED_LIGHT)
    frames.append(c3)

    return frames


# ==============================================================================
# KITCHEN GOAL GATE: kitchen_goal.png (384x128, 6 frames 64x128 @ 10 fps)
# ==============================================================================

def generate_kitchen_goal() -> List[PixelCanvas]:
    """
    384x128 px (6 frames of 64x128 @ 10 fps):
    Oven-mitt-shaped flag on a wooden spoon pole with waving motion.
    Pole at x=20..26, y=10..127.
    Oven mitt flag waving at x=24..60, y=16..68.
    """
    frames = []

    # Waving wave offsets across the 6 frames
    wave_offsets = [0, 2, 3, 2, -1, -2]

    for f in range(6):
        c = PixelCanvas(64, 128, TRANSPARENT)

        # 1. Wooden Cooking Spoon Pole (x=20..26, y=10..127)
        # Carved handle & shaft
        for py in range(25, 128):
            c.rect(21, py, 5, 1, BROWN_MID)
            c.set_pixel(21, py, WOOD_HIGHLIGHT)
            c.set_pixel(25, py, BROWN_DARK)
            c.set_pixel(20, py, OUTLINE)
            c.set_pixel(26, py, OUTLINE)

        # Spoon bowl / finial at top (y=8..25)
        c.circle(23, 16, 7, BROWN_MID, outline=OUTLINE)
        c.circle(23, 16, 5, BROWN_LIGHT)
        c.set_pixel(22, 14, WOOD_HIGHLIGHT)

        # Floor mounting base (y=122..127)
        c.rect(17, 124, 13, 4, BROWN_DARK, outline=OUTLINE)
        c.line(18, 124, 28, 124, WOOD_HIGHLIGHT)

        # 2. Oven-Mitt Flag (x=24..60, y=20..70)
        # Undulating horizontal wave offset
        woff = wave_offsets[f]

        # Mitt Cuff (attached to pole at x=26..32, y=22..38)
        c.rect(26, 24 + woff, 6, 16, PURE_WHITE, outline=OUTLINE)
        c.line(27, 25 + woff, 27, 38 + woff, K_CREAM_LIGHT)

        # Main Mitt Body (x=32..56, y=20..64)
        mitt_poly = [
            (32, 24 + woff),
            (52 + woff, 22 + woff),
            (58 + woff, 28 + woff), # mitt tip
            (56 + woff, 48 + woff),
            (46, 56 + woff // 2),   # thumb crotch
            (42, 64 + woff // 2),   # thumb tip
            (36, 60 + woff // 2),
            (38, 48 + woff),
            (32, 40 + woff),
        ]
        c.polygon(mitt_poly, RED_MID, outline=OUTLINE)

        # Quilted Diamond Pattern on Mitt Body
        for qy in range(26 + woff, 52 + woff, 6):
            c.line(34, qy, 52 + woff, qy + 6, K_FLOUR_PALE)
            c.line(34, qy + 6, 52 + woff, qy, K_FLOUR_PALE)

        # Thumb highlight
        c.circle(41, 60 + woff // 2, 3, RED_LIGHT)

        # Hanging ribbon loop at cuff
        c.line(26, 38 + woff, 23, 43 + woff, RED_MID)
        c.line(23, 43 + woff, 26, 45 + woff, RED_MID)

        frames.append(c)

    return frames

# ==============================================================================
# KITCHEN FLOOR CLUTTER (10 ITEMS + 10 SHADOWS)
# ==============================================================================

def generate_kitchen_clutter() -> Dict[str, PixelCanvas]:
    """Generates all 10 Kitchen floor clutter items and their 10 matching shadows."""
    res = {}

    # 1. Cereal Loops (32x20)
    c1 = PixelCanvas(32, 20, TRANSPARENT)
    loops = [
        (8, 10, RED_MID), (15, 7, YELLOW_MID), (22, 11, BLUE_MID),
        (13, 14, GREEN_MID), (26, 13, K_TOAST_GLOW), (19, 15, RED_MID)
    ]
    for lx, ly, col in loops:
        c1.circle(lx, ly, 4, col, outline=OUTLINE)
        c1.circle(lx, ly, 1, TRANSPARENT)
    # crunchy flakes
    c1.rect(5, 14, 3, 2, K_EGG_YELLOW, outline=OUTLINE)
    c1.rect(24, 7, 2, 2, K_EGG_YELLOW, outline=OUTLINE)
    res["kitchen_deco_cereal.png"] = c1
    res["kitchen_deco_cereal_shadow.png"] = make_shadow(32, 20, 16, 12, 13, 6)

    # 2. Spilled Sugar & Fallen Teaspoon (40x22)
    c2 = PixelCanvas(40, 22, TRANSPARENT)
    # White sugar pile
    c2.circle(20, 13, 8, PURE_WHITE, outline=WHITE_SHADOW)
    c2.circle(26, 14, 6, PURE_WHITE, outline=WHITE_SHADOW)
    c2.circle(14, 15, 5, PURE_WHITE, outline=WHITE_SHADOW)
    # fallen teaspoon
    c2.line(6, 16, 26, 8, K_STEEL_MID)
    c2.line(7, 17, 27, 9, K_STEEL_SPECULAR)
    c2.circle(30, 8, 4, K_STEEL_MID, outline=OUTLINE)
    c2.circle(29, 8, 2, K_STEEL_SPECULAR)
    res["kitchen_deco_spilled_sugar.png"] = c2
    res["kitchen_deco_spilled_sugar_shadow.png"] = make_shadow(40, 22, 20, 14, 16, 6)

    # 3. Dinner Fork (36x16)
    c3 = PixelCanvas(36, 16, TRANSPARENT)
    # Handle
    c3.line(4, 9, 22, 9, K_STEEL_MID)
    c3.line(4, 8, 22, 8, K_STEEL_SPECULAR)
    c3.set_pixel(3, 8, OUTLINE)
    c3.set_pixel(3, 9, OUTLINE)
    # 4 tines
    c3.line(22, 6, 22, 11, K_STEEL_MID)
    for ty in [6, 8, 9, 11]:
        c3.line(23, ty, 32, ty, K_STEEL_SPECULAR)
        c3.set_pixel(33, ty, OUTLINE)
    res["kitchen_deco_fork.png"] = c3
    res["kitchen_deco_fork_shadow.png"] = make_shadow(36, 16, 18, 10, 15, 4)

    # 4. Dessert Spoon (36x16)
    c4 = PixelCanvas(36, 16, TRANSPARENT)
    # Handle
    c4.line(4, 9, 22, 9, K_STEEL_MID)
    c4.line(4, 8, 22, 8, K_STEEL_SPECULAR)
    # Spoon bowl
    c4.circle(28, 8, 5, K_STEEL_MID, outline=OUTLINE)
    c4.circle(28, 8, 3, K_STEEL_SPECULAR)
    res["kitchen_deco_spoon.png"] = c4
    res["kitchen_deco_spoon_shadow.png"] = make_shadow(36, 16, 18, 10, 15, 4)

    # 5. Crimped Bottle Cap (24x16)
    c5 = PixelCanvas(24, 16, TRANSPARENT)
    c5.circle(12, 8, 6, RED_MID, outline=OUTLINE)
    c5.circle(12, 8, 4, RED_LIGHT)
    # Crimped fluted teeth
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        tx = int(12 + math.cos(rad) * 6)
        ty = int(8 + math.sin(rad) * 6)
        c5.set_pixel(tx, ty, K_STEEL_SPECULAR)
    res["kitchen_deco_bottle_cap.png"] = c5
    res["kitchen_deco_bottle_cap_shadow.png"] = make_shadow(24, 16, 12, 9, 8, 5)

    # 6. Crushed Juice Box (36x24)
    c6 = PixelCanvas(36, 24, TRANSPARENT)
    # Squashed rectangular body
    c6.polygon([(8, 8), (28, 6), (30, 20), (6, 21)], ORANGE_MID, outline=OUTLINE)
    c6.line(9, 9, 27, 7, ORANGE_LIGHT)
    # Crinkled foil seam
    c6.line(16, 8, 18, 20, K_STEEL_SPECULAR)
    # Striped straw sticking out
    c6.line(24, 8, 30, 2, RED_MID)
    c6.line(25, 8, 31, 2, PURE_WHITE)
    res["kitchen_deco_crushed_juice_box.png"] = c6
    res["kitchen_deco_crushed_juice_box_shadow.png"] = make_shadow(36, 24, 18, 15, 14, 7)

    # 7. Bowtie & Macaroni Pasta (32x18)
    c7 = PixelCanvas(32, 18, TRANSPARENT)
    # Bowtie 1 (Farfalle)
    c7.polygon([(6, 6), (16, 10), (6, 14)], K_EGG_YELLOW, outline=OUTLINE)
    c7.polygon([(20, 6), (10, 10), (20, 14)], K_EGG_YELLOW, outline=OUTLINE)
    c7.rect(12, 8, 3, 4, K_TOAST_GLOW)
    # Curved macaroni noodle
    c7.circle(24, 9, 5, K_EGG_YELLOW, outline=OUTLINE)
    c7.circle(24, 9, 2, TRANSPARENT)
    res["kitchen_deco_pasta.png"] = c7
    res["kitchen_deco_pasta_shadow.png"] = make_shadow(32, 18, 16, 11, 13, 5)

    # 8. Banana Peel (38x20)
    c8 = PixelCanvas(38, 20, TRANSPARENT)
    # Brown stem at center
    c8.circle(19, 10, 3, BROWN_DARK, outline=OUTLINE)
    # 3 Flaps
    # Flap 1 (left)
    c8.polygon([(18, 10), (6, 7), (2, 12), (17, 12)], YELLOW_MID, outline=OUTLINE)
    c8.line(6, 7, 17, 11, YELLOW_LIGHT)
    # Flap 2 (right)
    c8.polygon([(20, 10), (32, 8), (36, 14), (21, 13)], YELLOW_MID, outline=OUTLINE)
    c8.line(20, 11, 33, 9, YELLOW_LIGHT)
    # Flap 3 (center forward)
    c8.polygon([(17, 12), (21, 12), (20, 18), (18, 18)], YELLOW_MID, outline=OUTLINE)
    c8.set_pixel(19, 18, BROWN_DARK)
    res["kitchen_deco_banana_peel.png"] = c8
    res["kitchen_deco_banana_peel_shadow.png"] = make_shadow(38, 20, 19, 13, 16, 5)

    # 9. Flour Handprint (34x26)
    c9 = PixelCanvas(34, 26, TRANSPARENT)
    # Palm print
    c9.circle(17, 16, 7, K_FLOUR_PALE, outline=WHITE_SHADOW)
    # 5 Fingers
    fingers = [(9, 11), (13, 7), (17, 5), (22, 6), (26, 10)]
    for fx, fy in fingers:
        c9.circle(fx, fy, 3, K_FLOUR_PALE, outline=WHITE_SHADOW)
        c9.set_pixel(fx, fy, PURE_WHITE)
    res["kitchen_deco_flour_handprint.png"] = c9
    res["kitchen_deco_flour_handprint_shadow.png"] = make_shadow(34, 26, 17, 17, 12, 6)

    # 10. Grape with Stem (20x16)
    c10 = PixelCanvas(20, 16, TRANSPARENT)
    # Plump grape
    c10.circle(10, 9, 6, PURPLE_DARK, outline=OUTLINE)
    c10.circle(8, 7, 3, PURPLE_RICH)
    c10.set_pixel(8, 6, PURE_WHITE) # skin shine
    # Green/brown vine stem
    c10.line(10, 3, 14, 1, K_OLIVE_GREEN)
    c10.set_pixel(14, 1, BROWN_MID)
    res["kitchen_deco_grape.png"] = c10
    res["kitchen_deco_grape_shadow.png"] = make_shadow(20, 16, 10, 11, 7, 4)

    return res


# ==============================================================================
# KITCHEN ANIMATED PROPS (6 PROPS)
# ==============================================================================

def generate_kitchen_prop_fridge_light() -> List[PixelCanvas]:
    """576x128 px (6 frames 96x128 @ 6 fps): Refrigerator door cracked open with pulsing light."""
    frames = []
    for f in range(6):
        c = PixelCanvas(96, 128, TRANSPARENT)
        # Fridge Body (x=8..88, y=10..126)
        c.rect(8, 10, 80, 116, K_CREAM_LIGHT, outline=OUTLINE)
        c.line(9, 11, 87, 11, PURE_WHITE)
        c.line(9, 11, 9, 125, PURE_WHITE)

        # Door cracked open on left
        crack_w = 12 + (f % 3) * 2
        # Dark interior cavity
        c.rect(12, 16, crack_w, 104, SHADOW_PURPLE_DARK)
        # Shelves inside fridge
        c.line(12, 45, 12 + crack_w, 45, K_STEEL_SPECULAR)
        c.line(12, 75, 12 + crack_w, 75, K_STEEL_SPECULAR)
        # Colorful glowing jars on interior shelves
        c.rect(14, 33, 4, 10, K_JAM_RED)
        c.rect(14, 63, 5, 10, K_EGG_YELLOW)

        # Light fan spill across floor (pulsing glow)
        glow_alpha = 150 + f * 15
        fan_poly = [
            (12 + crack_w, 30),
            (90, 20),
            (95, 120),
            (12 + crack_w, 120),
        ]
        c.polygon(fan_poly, K_FLOUR_PALE)

        # Front Fridge Door edge (slanted slightly open)
        c.rect(12 + crack_w, 12, 74 - crack_w, 112, K_CREAM_LIGHT, outline=OUTLINE)
        # Chrome handle
        c.rect(16 + crack_w, 55, 6, 30, K_STEEL_MID, outline=OUTLINE)
        c.line(17 + crack_w, 56, 17 + crack_w, 84, K_STEEL_SPECULAR)

        frames.append(c)
    return frames


def generate_kitchen_prop_kettle() -> List[PixelCanvas]:
    """512x64 px (8 frames 64x64 @ 8 fps): Stovetop kettle with looping steam puff."""
    frames = []
    for f in range(8):
        c = PixelCanvas(64, 64, TRANSPARENT)

        # Burner ring (y=56..62)
        c.rect(10, 56, 38, 6, K_CAST_IRON, outline=OUTLINE)

        # Kettle Body (cx=26, cy=44, r=14)
        c.circle(26, 44, 14, RED_MID, outline=OUTLINE)
        c.circle(24, 42, 10, RED_LIGHT)
        c.line(15, 34, 37, 34, K_STEEL_SPECULAR) # lid rim
        c.circle(26, 32, 3, K_CAST_IRON, outline=OUTLINE) # lid knob

        # Arched Black Handle over top
        for deg in range(180, 360, 15):
            rad = math.radians(deg)
            hx = int(26 + math.cos(rad) * 12)
            hy = int(32 + math.sin(rad) * 10)
            c.rect(hx - 1, hy - 1, 3, 3, K_CAST_IRON)

        # Spout on right (x=38..48, y=36..42)
        c.polygon([(36, 42), (48, 36), (46, 33), (35, 38)], RED_MID, outline=OUTLINE)
        c.rect(46, 33, 4, 5, K_STEEL_SPECULAR, outline=OUTLINE) # whistle cap

        # Looping Billowing Steam from Whistle Tip (x=48, y=34)
        for puff_i in range(3):
            phase = (f + puff_i * 3) % 8
            sx = int(50 + phase * 1.8)
            sy = int(32 - phase * 3.5)
            sr = 2 + phase // 2
            if 0 <= sx < 64 and 0 <= sy < 64:
                c.circle(sx, sy, sr, K_FLOUR_PALE, outline=OUTLINE)
                c.circle(sx, sy, sr - 1, PURE_WHITE)

        frames.append(c)
    return frames


def generate_kitchen_prop_clock() -> List[PixelCanvas]:
    """512x64 px (8 frames 64x64 @ 4 fps): Rooster clock with moving eyes & swinging pendulum."""
    frames = []
    # Eye pupil positions: left, center, right, center
    eye_offsets = [-2, -1, 0, 1, 2, 1, 0, -1]
    # Pendulum angles
    pend_angles = [-12, -8, -3, 3, 8, 12, 6, -6]

    for f in range(8):
        c = PixelCanvas(64, 64, TRANSPARENT)

        # 1. Pendulum Tail Feather (cx=32, cy=44 swinging to y=62)
        ang = math.radians(pend_angles[f])
        pend_x = int(32 + math.sin(ang) * 16)
        pend_y = int(44 + math.cos(ang) * 16)
        c.line(32, 44, pend_x, pend_y, BROWN_MID)
        c.circle(pend_x, pend_y, 4, K_EGG_YELLOW, outline=OUTLINE)

        # 2. Clock Body (cx=32, cy=28, r=15)
        c.circle(32, 28, 15, BROWN_MID, outline=OUTLINE)
        c.circle(32, 28, 12, PURE_WHITE, outline=OUTLINE)

        # Clock Hands
        c.line(32, 28, 32, 20, OUTLINE) # minute hand
        c.line(32, 28, 37, 28, OUTLINE) # hour hand
        c.circle(32, 28, 2, K_CAST_IRON)

        # 3. Rooster Head & Comb (top of clock)
        # Red comb
        c.circle(30, 8, 4, RED_MID, outline=OUTLINE)
        c.circle(35, 7, 4, RED_MID, outline=OUTLINE)
        c.circle(26, 10, 3, RED_MID, outline=OUTLINE)
        # Yellow Beak
        c.polygon([(40, 16), (46, 18), (40, 20)], K_EGG_YELLOW, outline=OUTLINE)
        # Red wattle below beak
        c.circle(40, 22, 3, RED_MID, outline=OUTLINE)

        # 4. Moving Eyes at (27, 15) and (35, 15)
        e_off = eye_offsets[f]
        for ex in [28, 36]:
            c.circle(ex, 15, 3, PURE_WHITE, outline=OUTLINE)
            c.set_pixel(ex + e_off, 15, OUTLINE)

        frames.append(c)
    return frames


def generate_kitchen_prop_toaster() -> List[PixelCanvas]:
    """640x64 px (10 frames 64x64 @ 8 fps): Toaster popping toast into air and landing."""
    frames = []

    # Toast vertical offsets across 10 frames
    # Frames 0..2: inside toaster (y_off=0)
    # Frame 3: pop! (y_off=-8)
    # Frames 4..6: peak flight (y_off=-22, -26, -22)
    # Frames 7..9: falling back (y_off=-14, -6, 0)
    toast_y_offsets = [0, 0, 0, -8, -22, -26, -22, -14, -6, 0]
    lever_y_offsets = [12, 12, 12, 2, 2, 2, 2, 6, 10, 12]

    for f in range(10):
        c = PixelCanvas(64, 64, TRANSPARENT)

        ty_off = toast_y_offsets[f]
        ly_off = lever_y_offsets[f]

        # 1. Toast Slices (cx=26 and cx=38)
        # Drawn first so toaster front covers bottom when inside
        toast_y = 30 + ty_off
        for tx in [24, 36]:
            # Toast slice (10x14)
            c.rect(tx, toast_y, 10, 14, K_TOAST_GLOW, outline=OUTLINE)
            c.line(tx + 1, toast_y + 1, tx + 8, toast_y + 1, K_EGG_YELLOW)
            # Golden crust
            c.line(tx, toast_y, tx + 9, toast_y, K_COFFEE_DARK)

        # 2. Toaster Body (x=14..50, y=34..58)
        c.rect(14, 34, 36, 24, K_STEEL_MID, outline=OUTLINE)
        c.line(15, 35, 49, 35, K_STEEL_SPECULAR)
        c.line(15, 35, 15, 57, K_STEEL_SPECULAR)
        # Front grill band
        c.line(16, 46, 48, 46, K_CAST_IRON)

        # Toaster Slots on top (y=34)
        c.rect(22, 33, 12, 2, OUTLINE)
        c.rect(34, 33, 12, 2, OUTLINE)

        # Heating Coil Glow inside slots when down (f < 3)
        if f < 3:
            c.line(23, 34, 33, 34, RED_LIGHT)
            c.line(35, 34, 45, 34, RED_LIGHT)

        # Side Lever (x=10..14, y=36..52)
        c.line(14, 38, 14, 50, OUTLINE)
        c.rect(9, 38 + ly_off, 5, 4, K_CAST_IRON, outline=OUTLINE)

        # Flying crumbs during peak pop (frames 4..6)
        if 4 <= f <= 6:
            c.set_pixel(20, 20, K_TOAST_GLOW)
            c.set_pixel(44, 18, K_TOAST_GLOW)
            c.set_pixel(32, 12, K_EGG_YELLOW)

        # Feet (y=58..61)
        c.rect(17, 58, 4, 3, K_CAST_IRON, outline=OUTLINE)
        c.rect(43, 58, 4, 3, K_CAST_IRON, outline=OUTLINE)

        frames.append(c)
    return frames


def generate_kitchen_prop_dripping_tap() -> List[PixelCanvas]:
    """480x80 px (10 frames 48x80 @ 10 fps): Faucet dripping and splashing into basin."""
    frames = []

    # Drop Y positions across 10 frames
    # 0..2: forming at nozzle (y=28)
    # 3: detach (y=34)
    # 4: falling (y=44)
    # 5: falling (y=56)
    # 6: impact (y=68)
    # 7..9: ripple & splash (y=72)
    drop_y = [28, 29, 30, 36, 46, 58, 68, 72, 72, 72]

    for f in range(10):
        c = PixelCanvas(48, 80, TRANSPARENT)

        # Faucet Gooseneck Pipe (x=10..24, y=6..30)
        c.line(10, 6, 10, 30, K_STEEL_MID)
        c.line(11, 6, 11, 30, K_STEEL_SPECULAR)
        c.circle(16, 10, 6, K_STEEL_SPECULAR, outline=OUTLINE)
        c.rect(20, 10, 4, 18, K_STEEL_MID, outline=OUTLINE)
        c.line(21, 10, 21, 28, K_STEEL_SPECULAR)
        # Spout Nozzle (x=19..23, y=28)
        c.rect(19, 26, 5, 3, K_CAST_IRON, outline=OUTLINE)

        # Basin Water Surface at y=72
        c.line(6, 72, 42, 72, K_MINT_HIGHLIGHT)
        c.rect(6, 73, 36, 7, K_TEAL_DEEP)

        dy = drop_y[f]

        if f <= 2:
            # Drop forming at spout
            dr = 1 + f
            c.circle(21, dy, dr, K_MINT_HIGHLIGHT, outline=OUTLINE)
            c.set_pixel(21, dy, PURE_WHITE)
        elif 3 <= f <= 6:
            # Falling teardrop
            c.circle(21, dy, 2, K_MINT_HIGHLIGHT, outline=OUTLINE)
            c.set_pixel(21, dy - 1, PURE_WHITE)
            c.set_pixel(21, dy - 2, K_MINT_HIGHLIGHT)
        else:
            # Splash & Concentric Ripples at basin surface
            splash_frame = f - 7
            ripple_r = 5 + splash_frame * 4
            c.line(max(6, 21 - ripple_r), 72, min(42, 21 + ripple_r), 72, PURE_WHITE)
            # Splash droplets bouncing up
            if splash_frame == 0:
                c.set_pixel(18, 68, PURE_WHITE)
                c.set_pixel(24, 67, PURE_WHITE)
            elif splash_frame == 1:
                c.set_pixel(16, 65, K_MINT_HIGHLIGHT)
                c.set_pixel(26, 64, K_MINT_HIGHLIGHT)
                c.set_pixel(21, 63, PURE_WHITE)

        frames.append(c)
    return frames


def generate_kitchen_prop_fruit_fly() -> List[PixelCanvas]:
    """384x48 px (8 frames 48x48 @ 10 fps): Fruit fly flying in 3D figure-8 loop."""
    frames = []

    for f in range(8):
        c = PixelCanvas(48, 48, TRANSPARENT)

        # 3D Figure-8 orbital path centered at (24, 24)
        t = 2.0 * math.pi * f / 8.0
        fx = int(24 + 14 * math.sin(t))
        fy = int(24 + 7 * math.sin(2 * t))

        # Tiny Fly Body (3x2 px, brown/red)
        c.set_pixel(fx, fy, BROWN_DARK)
        c.set_pixel(fx + 1, fy, K_JAM_RED)
        c.set_pixel(fx - 1, fy, OUTLINE)

        # Shimmering Translucent Wings (flapping up/down)
        wing_phase = f % 3
        if wing_phase == 0:
            # Wings spread up
            c.line(fx - 2, fy - 3, fx, fy - 1, K_MINT_HIGHLIGHT)
            c.line(fx + 2, fy - 3, fx, fy - 1, PURE_WHITE)
        elif wing_phase == 1:
            # Wings flat
            c.line(fx - 3, fy, fx - 1, fy, K_MINT_HIGHLIGHT)
            c.line(fx + 1, fy, fx + 3, fy, PURE_WHITE)
        else:
            # Wings dipped down
            c.line(fx - 2, fy + 2, fx, fy + 1, K_MINT_HIGHLIGHT)
            c.line(fx + 2, fy + 2, fx, fy + 1, PURE_WHITE)

        frames.append(c)
    return frames

# ==============================================================================
# BACKYARD PARALLAX & FOREGROUND LAYERS
# ==============================================================================

def generate_yard_sky_gradient() -> PixelCanvas:
    """1x540 px: 8 hard color bands of dusk garden ambient light."""
    c = PixelCanvas(1, 540)
    bands = [
        (0, 68, VOID_BLACK),          # Band 0: Deep night zenith
        (68, 136, BLUE_DEEP),         # Band 1: Midnight navy
        (136, 203, BLUE_SHADOW),      # Band 2: Deep twilight blue
        (203, 270, Y_FENCE_SHADOW),   # Band 3: Dusk fence shadow
        (270, 338, Y_FENCE_MID),      # Band 4: Dusk fence blue-gray
        (338, 406, Y_FLOWER_MAGENTA), # Band 5: Twilight magenta horizon
        (406, 473, Y_POT_DARK),       # Band 6: Sunset terracotta dark
        (473, 540, Y_POT_LIGHT),      # Band 7: Warm glowing twilight horizon
    ]
    for y_start, y_end, col in bands:
        for y in range(y_start, y_end):
            c.set_pixel(0, y, col)
    return c


def generate_yard_bg_far() -> PixelCanvas:
    """
    960x540 px: Far background backyard scene.
    - Deep twilight garden sky
    - Glowing crescent moon & stars
    - Distant tree line silhouettes
    - Garden shed roof silhouette with rooster weathervane
    - Cedar dog-ear picket fence
    - Base lawn ground
    """
    c = PixelCanvas(960, 540, BLUE_DEEP)

    # 1. Sky Gradient Fill (y=0..340)
    for y in range(0, 340):
        if y < 80:
            col = VOID_BLACK
        elif y < 160:
            col = BLUE_DEEP
        elif y < 240:
            col = BLUE_SHADOW
        elif y < 300:
            col = Y_FENCE_SHADOW
        else:
            col = Y_FLOWER_MAGENTA
        for x in range(960):
            c.set_pixel(x, y, col)

    # 2. Glowing Crescent Moon (x=710..770, y=60..120)
    c.circle(740, 90, 22, Y_LIGHT_FILAMENT, outline=OUTLINE)
    c.circle(748, 86, 18, BLUE_DEEP) # inner bite
    c.set_pixel(732, 92, PURE_WHITE)

    # 3. Scattered Garden Stars across upper sky
    star_coords = [
        (40, 30), (120, 70), (180, 25), (260, 85), (340, 40),
        (420, 65), (510, 20), (590, 75), (660, 35), (820, 50),
        (880, 25), (930, 80), (150, 120), (380, 110), (620, 130), (850, 115)
    ]
    for sx, sy in star_coords:
        c.set_pixel(sx, sy, Y_LIGHT_FILAMENT)
        c.set_pixel(sx + 1, sy, Y_LIGHT_GOLD)
        c.set_pixel(sx - 1, sy, Y_LIGHT_GOLD)
        c.set_pixel(sx, sy + 1, Y_LIGHT_GOLD)
        c.set_pixel(sx, sy - 1, Y_LIGHT_GOLD)

    # 4. Distant Tree Silhouettes (y=160..340)
    # Background forest silhouette
    for x in range(960):
        tree_top = 220 + int(math.sin(x * 0.02) * 25 + math.sin(x * 0.05) * 15)
        for y in range(tree_top, 340):
            c.set_pixel(x, y, Y_TURF_SHADOW)

    # Tall Pine Tree Silhouettes
    for px_t in [80, 220, 480, 650, 890]:
        c.polygon([(px_t - 25, 340), (px_t + 25, 340), (px_t, 160)], Y_TURF_SHADOW, outline=OUTLINE)

    # 5. Shed Roof Silhouette with Rooster Weathervane (x=160..300, y=240..340)
    c.polygon([(160, 340), (300, 340), (230, 260)], Y_TURF_SHADOW, outline=OUTLINE)
    # Weathervane spire
    c.line(230, 260, 230, 230, OUTLINE)
    c.line(220, 240, 240, 240, OUTLINE) # compass cross
    # Tiny rooster silhouette
    c.circle(230, 226, 4, OUTLINE)
    c.set_pixel(226, 224, OUTLINE) # beak
    c.set_pixel(234, 223, OUTLINE) # tail

    # 6. Cedar Dog-Ear Picket Fence (x=0..960, y=340..460)
    # Horizontal fence rails
    c.rect(0, 370, 960, 10, Y_FENCE_SHADOW, outline=OUTLINE)
    c.line(0, 371, 959, 371, Y_FENCE_MID)
    c.rect(0, 430, 960, 10, Y_FENCE_SHADOW, outline=OUTLINE)
    c.line(0, 431, 959, 431, Y_FENCE_MID)

    # Dog-ear pickets (width 20px, spacing 4px)
    for px in range(0, 960, 24):
        # Dog-ear top chamfer
        c.polygon([(px + 4, 340), (px + 16, 340), (px + 20, 346), (px + 20, 460), (px, 460), (px, 346)], Y_FENCE_MID, outline=OUTLINE)
        c.line(px + 2, 347, px + 2, 458, Y_SOIL_MID) # wood grain line
        c.line(px + 6, 350, px + 6, 458, Y_DIRT_DRY)
        # Screw nails on rails
        c.set_pixel(px + 10, 375, OUTLINE)
        c.set_pixel(px + 10, 435, OUTLINE)

    # 7. Base Lawn Ground (y=460..540)
    c.rect(0, 460, 960, 80, Y_TURF_SHADOW)
    # Grass tuft fringe at y=460
    for x in range(0, 960, 6):
        c.line(x, 460, x + 2, 454, Y_GRASS_SHADOW)
        c.line(x + 2, 454, x + 4, 460, Y_GRASS_SHADOW)

    return c


def generate_yard_bg_far_anim() -> List[PixelCanvas]:
    """
    3840x540 px (4 frames 960x540 @ 3 fps):
    Ambient motion overlay:
    - Drifting wisps of dusk clouds across moon
    - Twinkling garden stars pulsating
    """
    frames = []
    star_coords = [
        (40, 30), (120, 70), (180, 25), (260, 85), (340, 40),
        (420, 65), (510, 20), (590, 75), (660, 35), (820, 50),
        (880, 25), (930, 80), (150, 120), (380, 110), (620, 130), (850, 115)
    ]

    for f in range(4):
        c = PixelCanvas(960, 540, TRANSPARENT)

        # 1. Drifting Night Clouds across Moon (x=700..790, y=70..110)
        c_off = f * 8
        c.rect(700 + c_off, 85, 45, 8, Y_FENCE_SHADOW)
        c.rect(715 + c_off, 95, 55, 6, Y_FENCE_SHADOW)

        # 2. Twinkling Garden Stars
        for i, (sx, sy) in enumerate(star_coords):
            phase = (f + i) % 4
            if phase == 0:
                c.set_pixel(sx, sy, Y_LIGHT_GOLD)
            elif phase == 1:
                c.circle(sx, sy, 2, Y_LIGHT_GOLD)
                c.set_pixel(sx, sy, Y_LIGHT_FILAMENT)
            elif phase == 2:
                # Starburst
                c.line(sx - 2, sy, sx + 2, sy, Y_LIGHT_FILAMENT)
                c.line(sx, sy - 2, sx, sy + 2, Y_LIGHT_FILAMENT)
                c.set_pixel(sx, sy, PURE_WHITE)
            else:
                c.circle(sx, sy, 1, Y_LIGHT_GOLD)

        frames.append(c)
    return frames


def generate_yard_bg_mid() -> PixelCanvas:
    """
    1280x540 px: Mid-ground backyard scene.
    - Seamless horizontal tiling at floor level y=400 (x=0 matches x=1279).
    - Patio fence with climbing roses (x=50..220, y=140..400)
    - Garden tool shed (x=260..420, y=140..400) with glowing window
    - Potting bench with flowerpots & stone gnome (x=460..580, y=200..400)
    - Big backyard oak tree with tire swing (x=620..920, y=80..400)
    - Berry bushes with fireflies (x=960..1120, y=240..400)
    - Stone birdbath with perched robin (x=1150..1240, y=260..400)
    """
    c = PixelCanvas(1280, 540, TRANSPARENT)

    # 1. PATIO FENCE WITH CLIMBING ROSES (x=50..220, y=140..400)
    # Trellis Lattice Framework
    for x in range(50, 220, 20):
        c.line(x, 140, x, 400, Y_FENCE_SHADOW)
    for y in range(150, 400, 25):
        c.line(50, y, 220, y, Y_FENCE_SHADOW)
    # Vine Stems curling over lattice
    for x in range(60, 210, 4):
        vy = int(220 + math.sin(x * 0.1) * 35)
        c.circle(x, vy, 4, Y_GRASS_MID)
        c.circle(x, vy - 2, 2, Y_SPROUT_BRIGHT)
        # Pink blooming rose blossoms
        if x % 24 == 0:
            c.circle(x, vy, 6, Y_FLOWER_MAGENTA, outline=OUTLINE)
            c.circle(x, vy, 3, RED_LIGHT)
            c.set_pixel(x, vy, Y_LIGHT_GOLD) # center

    # 2. GARDEN TOOL SHED (x=260..420, y=140..400)
    # Shed walls (cedar shakes)
    c.rect(260, 180, 160, 220, Y_SOIL_MID, outline=OUTLINE)
    for y in range(180, 400, 14):
        c.line(260, y, 420, y, Y_SOIL_DARK)
        c.line(260, y + 1, 420, y + 1, Y_DIRT_DRY)
    # Gable Roof
    c.polygon([(245, 180), (435, 180), (340, 130)], Y_FENCE_SHADOW, outline=OUTLINE)
    c.line(246, 179, 340, 131, Y_FENCE_MID)

    # Shed Window with warm candlelight glow (x=290..340, y=210..270)
    c.rect(290, 210, 50, 60, BROWN_DARK, outline=OUTLINE)
    c.rect(294, 214, 42, 52, Y_LIGHT_GOLD, outline=OUTLINE)
    c.circle(315, 240, 15, Y_LIGHT_FILAMENT) # interior candle glow
    # 4 Window panes
    c.line(315, 214, 315, 265, BROWN_DARK)
    c.line(294, 240, 335, 240, BROWN_DARK)

    # Shed Door on right (x=355..410, y=220..400)
    c.rect(355, 220, 55, 180, Y_SOIL_DARK, outline=OUTLINE)
    c.line(356, 221, 409, 221, Y_DIRT_DRY)
    c.rect(362, 230, 41, 70, Y_SOIL_MID, outline=OUTLINE)
    c.rect(362, 310, 41, 80, Y_SOIL_MID, outline=OUTLINE)
    c.circle(365, 310, 3, Y_LIGHT_GOLD, outline=OUTLINE) # brass doorknob

    # Galvanized watering can on porch step
    c.rect(270, 370, 18, 28, METAL_SHADOW, outline=OUTLINE)
    c.line(271, 371, 287, 371, WHITE_SHADOW)
    c.line(288, 375, 298, 365, METAL_SHADOW) # spout

    # 3. POTTING BENCH WITH FLOWERPOTS (x=460..580, y=200..400)
    # Sturdy wooden workbench
    c.rect(460, 250, 120, 14, Y_DIRT_DRY, outline=OUTLINE)
    c.line(461, 251, 579, 251, WOOD_HIGHLIGHT)
    c.rect(465, 264, 10, 136, Y_SOIL_MID, outline=OUTLINE)
    c.rect(565, 264, 10, 136, Y_SOIL_MID, outline=OUTLINE)
    c.rect(465, 340, 110, 8, Y_SOIL_DARK, outline=OUTLINE) # bottom shelf

    # Terracotta Flowerpots on bench
    for p_idx, px_pot in enumerate([475, 505, 535]):
        c.polygon([(px_pot, 250), (px_pot + 22, 250), (px_pot + 19, 226), (px_pot + 3, 226)], Y_POT_DARK, outline=OUTLINE)
        c.rect(px_pot + 2, 223, 18, 4, Y_POT_LIGHT, outline=OUTLINE)
        # Green plant sprout in pot
        c.circle(px_pot + 11, 218, 5, Y_GRASS_LIGHT, outline=OUTLINE)
        c.set_pixel(px_pot + 11, 216, Y_SPROUT_BRIGHT)

    # Stone garden gnome holding lantern on bench right (x=560..578, y=210..250)
    c.polygon([(564, 230), (576, 230), (570, 210)], RED_MID, outline=OUTLINE) # hat
    c.circle(570, 234, 4, PURE_WHITE, outline=OUTLINE) # beard
    c.rect(565, 236, 10, 14, BLUE_MID, outline=OUTLINE) # body
    # Tiny lantern
    c.rect(577, 234, 6, 8, Y_LIGHT_GOLD, outline=OUTLINE)
    c.set_pixel(579, 237, PURE_WHITE)

    # 4. MAJESTIC BACKYARD OAK TREE WITH TIRE SWING (x=620..920, y=80..400)
    # Massive Trunk (x=680..760, y=140..400)
    c.polygon([(670, 400), (770, 400), (745, 160), (695, 160)], Y_SOIL_DARK, outline=OUTLINE)
    for ty_tk in range(160, 400, 6):
        c.line(700, ty_tk, 740, ty_tk, Y_SOIL_MID)
        c.line(715, ty_tk, 725, ty_tk, Y_DIRT_DRY)

    # Heavy Horizontal Branch (x=640..900, y=130..170)
    c.polygon([(695, 160), (900, 135), (900, 155), (745, 180)], Y_SOIL_DARK, outline=OUTLINE)
    c.line(700, 161, 899, 136, Y_SOIL_MID)

    # Leafy Canopy Foliage Clouds (x=620..920, y=60..180)
    canopy_orbs = [
        (660, 110, 42), (720, 85, 48), (780, 90, 45), (840, 110, 40),
        (890, 130, 32), (640, 140, 35), (750, 130, 38)
    ]
    for co_x, co_y, co_r in canopy_orbs:
        c.circle(co_x, co_y, co_r, Y_TURF_SHADOW, outline=OUTLINE)
        c.circle(co_x - 3, co_y - 4, co_r - 6, Y_GRASS_SHADOW)
        c.circle(co_x - 6, co_y - 8, co_r - 12, Y_GRASS_MID)
        c.set_pixel(co_x - 8, co_y - 12, Y_GRASS_LIGHT)

    # Tire Swing hanging from branch (x=830..860, y=145..400)
    # Twin Ropes
    c.line(838, 145, 838, 340, Y_DIRT_DRY)
    c.line(848, 145, 848, 340, Y_DIRT_DRY)
    # Black Rubber Tire resting on lawn
    c.circle(843, 365, 24, VOID_BLACK, outline=OUTLINE)
    c.circle(843, 365, 13, Y_TURF_SHADOW, outline=OUTLINE)
    c.circle(841, 363, 22, METAL_SHADOW) # tire rubber bevel

    # 5. BERRY BUSHES WITH FIREFLIES (x=960..1120, y=240..400)
    bush_orbs = [(990, 320, 36), (1040, 300, 42), (1090, 330, 34)]
    for bx, by, br in bush_orbs:
        c.circle(bx, by, br, Y_TURF_SHADOW, outline=OUTLINE)
        c.circle(bx - 2, by - 3, br - 5, Y_GRASS_SHADOW)
        c.circle(bx - 4, by - 6, br - 10, Y_GRASS_MID)

    # Ripe red berries scattered on bushes
    berry_coords = [(980, 310), (1010, 330), (1035, 285), (1055, 315), (1075, 295), (1100, 325)]
    for b_x, b_y in berry_coords:
        c.circle(b_x, b_y, 3, Y_FLOWER_MAGENTA, outline=OUTLINE)
        c.set_pixel(b_x, b_y, RED_LIGHT)

    # Resting glowing fireflies
    c.circle(1020, 305, 2, Y_LIGHT_FILAMENT)
    c.set_pixel(1020, 305, PURE_WHITE)
    c.circle(1070, 340, 2, Y_LIGHT_FILAMENT)

    # 6. STONE BIRDBATH WITH PERCHED ROBIN (x=1150..1240, y=260..400)
    # Turned Stone Pedestal
    c.rect(1185, 310, 16, 85, WHITE_SHADOW, outline=OUTLINE)
    c.line(1186, 311, 1186, 394, PURE_WHITE)
    c.rect(1175, 388, 36, 12, WHITE_SHADOW, outline=OUTLINE) # base
    # Stone Basin at top
    c.circle(1193, 305, 32, WHITE_SHADOW, outline=OUTLINE)
    c.rect(1160, 290, 66, 18, WHITE_SHADOW, outline=OUTLINE)
    # Water surface inside basin
    c.line(1166, 294, 1220, 294, Y_WATER_CYAN)
    c.line(1167, 295, 1219, 295, BLUE_LIGHT)

    # Cute perched robin bird silhouette on basin rim (x=1215, y=282)
    c.circle(1218, 284, 5, BROWN_DARK, outline=OUTLINE) # body
    c.circle(1222, 280, 3, BROWN_DARK, outline=OUTLINE) # head
    c.set_pixel(1226, 280, Y_LIGHT_GOLD) # beak
    c.circle(1217, 285, 2, RED_MID) # red breast

    # Floor Contact Line at y=400 across entire mid-ground
    for x in range(50, 1240):
        c.set_pixel(x, 400, OUTLINE)
        c.set_pixel(x, 401, Y_TURF_SHADOW)

    return c


def generate_yard_bg_near() -> PixelCanvas:
    """
    960x540 px: Foreground silhouettes layer.
    - STRICT: Transparent above floor line y=400 (y=0..399 is 100% transparent!).
    - Dark silhouettes of wheelbarrow, hose reel, planter box, watering can & boots, sundial.
    - 1px warm rim light in Y_SPROUT_BRIGHT.
    """
    c = PixelCanvas(960, 540, TRANSPARENT)
    SIL = VOID_BLACK
    RIM = Y_SPROUT_BRIGHT

    # 1. Wheelbarrow (x=50..180, y=410..535)
    # Slanted metal tray
    c.polygon([(55, 420), (145, 420), (130, 480), (70, 480)], SIL)
    c.line(55, 420, 145, 420, RIM)
    c.line(55, 420, 70, 480, RIM)
    # Front wheel
    c.circle(148, 500, 20, SIL)
    c.circle(148, 500, 12, TRANSPARENT)
    c.circle(148, 500, 20, SIL, outline=RIM)
    # Rear resting leg & wooden handles
    c.line(75, 480, 70, 532, SIL)
    c.line(76, 480, 71, 532, RIM)
    c.line(70, 450, 45, 425, SIL) # handle
    c.line(70, 449, 45, 424, RIM)

    # 2. Garden Hose Reel Cart (x=240..370, y=415..535)
    # Wheeled tubular frame
    c.circle(300, 470, 36, SIL)
    c.circle(300, 470, 36, SIL, outline=RIM)
    # Coiled ribbed hose lines
    for hr in range(16, 34, 5):
        c.circle(300, 470, hr, SIL, outline=RIM)
    # Cart wheels at bottom
    c.circle(270, 515, 12, SIL, outline=RIM)
    c.circle(330, 515, 12, SIL, outline=RIM)
    # Hose nozzle sticking up
    c.polygon([(335, 435), (355, 420), (360, 425), (340, 440)], SIL)
    c.line(335, 435, 355, 420, RIM)

    # 3. Wooden Flower Planter Box with Blooming Tulips (x=430..600, y=415..535)
    # Planter Box (x=440..590, y=460..530)
    c.rect(440, 460, 150, 70, SIL)
    c.line(440, 460, 590, 460, RIM)
    c.line(440, 460, 440, 530, RIM)
    # Blooming Tulip silhouettes peeking over rim (y=410..460)
    for tx in range(455, 580, 24):
        # Stalk
        c.line(tx, 460, tx, 430, SIL)
        c.line(tx - 1, 460, tx - 1, 430, RIM)
        # Tulip cup blossom
        c.polygon([(tx - 6, 430), (tx + 6, 430), (tx + 8, 415), (tx, 420), (tx - 8, 415)], SIL)
        c.line(tx - 8, 415, tx - 6, 430, RIM)
        c.line(tx - 8, 415, tx, 420, RIM)

    # 4. Watering Can & Pair of Mud Boots (x=660..780, y=420..535)
    # Watering can on left
    c.rect(665, 450, 36, 45, SIL)
    c.line(665, 450, 701, 450, RIM)
    c.line(665, 450, 665, 495, RIM)
    # Can Spout
    c.line(701, 480, 725, 445, SIL)
    c.line(701, 479, 725, 444, RIM)
    # Tall rubber boots standing side by side (x=730..775, y=435..535)
    for bx in [735, 755]:
        c.polygon([(bx, 440), (bx + 18, 440), (bx + 16, 515), (bx + 26, 532), (bx, 532), (bx, 515)], SIL)
        c.line(bx, 440, bx + 18, 440, RIM)
        c.line(bx, 440, bx, 532, RIM)

    # 5. Stone Sundial on Pedestal (x=820..920, y=415..535)
    # Dial plate on top
    c.polygon([(830, 440), (910, 440), (895, 455), (845, 455)], SIL)
    c.line(830, 440, 910, 440, RIM)
    # Gnomon blade sticking up
    c.polygon([(870, 440), (870, 415), (860, 440)], SIL)
    c.line(860, 440, 870, 415, RIM)
    # Turned pedestal
    c.polygon([(855, 455), (885, 455), (875, 532), (865, 532)], SIL)
    c.line(855, 455, 865, 532, RIM)

    # STRICT: Clear any pixels above y=400
    for y in range(0, 400):
        for x in range(960):
            c.set_pixel(x, y, TRANSPARENT)

    return c


def generate_yard_fg_legs() -> PixelCanvas:
    """960x540 px: Foreground silhouettes of patio table legs, trellis post, and pergola."""
    c = PixelCanvas(960, 540, TRANSPARENT)
    SIL = VOID_BLACK
    RIM = Y_SPROUT_BRIGHT

    # 1. Wrought-Iron Patio Dining Table Leg (x=0..120, y=260..540)
    c.rect(0, 260, 110, 18, SIL)
    c.line(0, 260, 110, 260, RIM)
    # Scrollwork leg
    for ly in range(278, 540):
        hw = 12 + int(math.sin((ly - 278) * 0.08) * 6)
        c.line(50 - hw, ly, 50 + hw, ly, SIL)
        c.set_pixel(50 - hw, ly, RIM)
    # Scrollwork foot at bottom
    c.circle(50, 525, 20, SIL)
    c.circle(50, 525, 20, SIL, outline=RIM)

    # 2. Garden Trellis Post with Honeysuckle Vines (x=180..240, y=80..540)
    c.rect(195, 80, 14, 460, SIL)
    c.line(195, 80, 195, 539, RIM)
    # Vine tendrils wrapping around
    for vy in range(90, 530, 25):
        c.circle(202, vy, 12, SIL)
        c.set_pixel(192, vy, RIM)
        c.set_pixel(212, vy, RIM)

    # 3. Heavy Patio Umbrella Pole & Base (x=520..580, y=280..540)
    c.rect(544, 280, 12, 230, SIL)
    c.line(544, 280, 544, 510, RIM)
    # Cast iron dome weighted base on lawn (y=505..535)
    c.circle(550, 520, 28, SIL)
    c.line(522, 520, 550, 505, RIM)

    # 4. Wooden Pergola Post with Climbing Ivy (x=820..940, y=180..540)
    c.rect(860, 180, 24, 360, SIL)
    c.line(860, 180, 860, 539, RIM)
    c.line(883, 180, 883, 539, RIM)
    # Ivy leaf clusters
    for iy in range(200, 520, 30):
        c.circle(872, iy, 14, SIL)
        c.circle(872, iy, 14, SIL, outline=RIM)

    return c


def generate_yard_fg_dust() -> PixelCanvas:
    """960x540 px: Foreground firefly spores, floating dandelion seeds, evening pollen (hard-banded alpha)."""
    c = PixelCanvas(960, 540, TRANSPARENT)
    rgb_gold = Y_LIGHT_GOLD[:3]         # (245, 179, 56)
    rgb_filament = Y_LIGHT_FILAMENT[:3] # (255, 235, 128)
    rgb_sprout = Y_SPROUT_BRIGHT[:3]    # (126, 237, 143)

    orbs = [
        (100, 140, 24, rgb_gold),     (240, 380, 26, rgb_filament),
        (390, 180, 22, rgb_sprout),   (540, 420, 28, rgb_gold),
        (690, 160, 25, rgb_filament), (840, 350, 24, rgb_sprout),
        (160, 260, 14, rgb_gold),     (320, 210, 15, rgb_filament),
        (480, 300, 14, rgb_sprout),   (620, 240, 13, rgb_gold),
        (760, 290, 15, rgb_filament), (910, 200, 12, rgb_sprout),
        (70, 470, 7, rgb_gold),       (200, 100, 6, rgb_filament),
        (440, 60, 7, rgb_sprout),     (720, 490, 6, rgb_gold),
        (870, 80, 7, rgb_filament),   (940, 470, 6, rgb_sprout),
    ]

    for cx, cy, r, rgb in orbs:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if 0 <= x < 960 and 0 <= y < 540:
                    d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    if d <= r:
                        if d > r * 0.75:
                            a = 40
                        elif d > r * 0.50:
                            a = 80
                        elif d > r * 0.25:
                            a = 150
                        else:
                            a = 220
                        if a > c.get_pixel(x, y)[3]:
                            c.set_pixel(x, y, (rgb[0], rgb[1], rgb[2], a))

    return c

# ==============================================================================
# BACKYARD TILESET & OBSTACLES
# ==============================================================================

def generate_yard_tileset_floor() -> PixelCanvas:
    """
    256x96 px (32x32 tiles, 8 cols x 3 rows).
    Row 0: Surface Tiles (Grass blades over dark garden soil)
      Col 0: Standard lush grass
      Col 1: Pink clover blossom in grass
      Col 2: Left cliff edge facing a pit
      Col 3: Right cliff edge facing a pit
      Col 4: Smooth garden stone in turf
      Col 5: Cluster of 3 red garden mushrooms
      Col 6: Earthworm burrow hole
      Col 7: Fallen golden autumn leaf
    Row 1: Dark loam soil with roots and embedded stones
    Row 2: Deep subterranean bedrock
    """
    c = PixelCanvas(256, 96, VOID_BLACK)

    def draw_grass_surface(tx: int, ty: int):
        # Soil base (y=4..31)
        c.rect(tx, ty + 4, 32, 28, Y_SOIL_DARK)
        for y in range(ty + 5, ty + 32, 3):
            for x in range(tx, tx + 32, 4):
                if (x + y) % 5 == 0:
                    c.set_pixel(x, y, Y_SOIL_MID)
                elif (x + y) % 7 == 0:
                    c.set_pixel(x, y, Y_DIRT_DRY)
        # Grass blade layer (y=0..4)
        c.rect(tx, ty + 2, 32, 3, Y_GRASS_SHADOW)
        for x in range(tx, tx + 32):
            b_h = 2 + (x % 3)
            c.line(x, ty + 4 - b_h, x, ty + 4, Y_GRASS_MID)
            c.set_pixel(x, ty + 4 - b_h, Y_SPROUT_BRIGHT if (x % 2 == 0) else Y_GRASS_LIGHT)

    # --- ROW 0: SURFACE TILES (y=0..31) ---
    # Col 0: Standard
    draw_grass_surface(0, 0)

    # Col 1: Pink clover blossom
    draw_grass_surface(32, 0)
    c.circle(48, 4, 3, Y_FLOWER_MAGENTA, outline=OUTLINE)
    c.set_pixel(48, 4, Y_LIGHT_GOLD)
    c.line(48, 6, 48, 10, Y_SPROUT_BRIGHT)

    # Col 2: Left cliff edge
    draw_grass_surface(64, 0)
    # Exposed root strands & cut soil
    c.rect(64, 0, 4, 32, OUTLINE)
    c.line(65, 0, 65, 31, Y_SOIL_MID)
    c.line(64, 12, 67, 18, Y_DIRT_DRY) # hanging root

    # Col 3: Right cliff edge
    draw_grass_surface(96, 0)
    c.rect(124, 0, 4, 32, OUTLINE)
    c.line(126, 0, 126, 31, Y_SOIL_MID)
    c.line(125, 14, 128, 20, Y_DIRT_DRY)

    # Col 4: Smooth garden stone
    draw_grass_surface(128, 0)
    c.circle(144, 12, 6, WHITE_SHADOW, outline=OUTLINE)
    c.circle(142, 10, 3, METAL_MID)
    c.set_pixel(142, 9, PURE_WHITE)

    # Col 5: Red garden mushrooms
    draw_grass_surface(160, 0)
    # Shroom 1
    c.circle(170, 6, 4, RED_MID, outline=OUTLINE)
    c.set_pixel(169, 5, PURE_WHITE)
    c.rect(169, 9, 2, 4, PURE_WHITE)
    # Shroom 2
    c.circle(178, 8, 3, RED_MID, outline=OUTLINE)
    c.set_pixel(178, 7, PURE_WHITE)
    c.rect(177, 10, 2, 3, PURE_WHITE)

    # Col 6: Earthworm burrow hole
    draw_grass_surface(192, 0)
    c.circle(208, 10, 5, VOID_BLACK, outline=Y_SOIL_DARK)
    c.circle(208, 7, 2, DUSK_ROSE) # worm head peeking
    c.set_pixel(208, 6, OUTLINE)

    # Col 7: Fallen golden autumn leaf
    draw_grass_surface(224, 0)
    c.polygon([(236, 6), (246, 4), (248, 10), (238, 11)], Y_LIGHT_GOLD, outline=OUTLINE)
    c.line(237, 7, 245, 6, ORANGE_MID) # vein

    # --- ROW 1: MID-FILL SOIL & ROOTS (y=32..63) ---
    for col in range(8):
        tx = col * 32
        c.rect(tx, 32, 32, 32, Y_SOIL_DARK)
        # Horizontal soil strata
        c.line(tx, 42, tx + 31, 42, Y_SOIL_MID)
        c.line(tx, 54, tx + 31, 54, Y_SOIL_MID)

        # Tangled tree roots branching across
        rx_start = tx + (col * 7) % 24
        c.line(rx_start, 32, rx_start + 6, 48, Y_DIRT_DRY)
        c.line(rx_start + 6, 48, rx_start + 12, 63, Y_DIRT_DRY)
        c.line(rx_start + 6, 48, rx_start - 4, 60, Y_DIRT_DRY)

        # Embedded pebbles
        if col % 2 == 0:
            c.circle(tx + 18, 48, 2, WHITE_SHADOW, outline=OUTLINE)

    # Buried bone fragment in Col 3
    c.line(106, 52, 118, 52, PURE_WHITE)
    c.circle(105, 52, 2, PURE_WHITE, outline=OUTLINE)
    c.circle(119, 52, 2, PURE_WHITE, outline=OUTLINE)

    # --- ROW 2: DEEP BEDROCK (y=64..95) ---
    for col in range(8):
        tx = col * 32
        c.rect(tx, 64, 32, 32, SHADOW_PURPLE_DARK)
        # Deep stone fractures & mineral veins
        c.line(tx + 4, 68, tx + 28, 80, OUTLINE)
        c.line(tx + 12, 80, tx + 20, 92, OUTLINE)
        # Deep root tapering out
        c.line(tx + 16, 64, tx + 14, 76, Y_SOIL_MID)
        # Void black at bottom
        c.rect(tx, 86, 32, 10, VOID_BLACK)

    return c


def generate_yard_pit_bg() -> PixelCanvas:
    """32x128 px: Inside of a pit, tiles horizontally, dark soil, twisted tree roots, earthworm."""
    c = PixelCanvas(32, 128, Y_SOIL_DARK)

    # Vertical earthen walls on sides
    c.rect(0, 0, 6, 128, Y_TURF_SHADOW, outline=OUTLINE)
    c.rect(26, 0, 6, 128, Y_TURF_SHADOW, outline=OUTLINE)

    # Layered soil strata
    for y in range(0, 128, 16):
        c.line(6, y, 26, y, Y_SOIL_MID)

    # Twisted Tree Roots crawling down
    c.line(10, 0, 14, 40, Y_DIRT_DRY)
    c.line(14, 40, 22, 80, Y_DIRT_DRY)
    c.line(22, 80, 16, 127, Y_DIRT_DRY)
    # Secondary root branch
    c.line(14, 40, 8, 70, Y_DIRT_DRY)

    # Embedded quartz pebbles
    c.circle(20, 30, 3, WHITE_SHADOW, outline=OUTLINE)
    c.circle(12, 95, 2, WHITE_SHADOW, outline=OUTLINE)

    # Segmented earthworm poking out of soil pocket at y=68
    c.circle(18, 66, 3, DUSK_ROSE, outline=OUTLINE)
    c.circle(22, 68, 3, DUSK_ROSE, outline=OUTLINE)
    c.circle(25, 66, 2, DUSK_ROSE, outline=OUTLINE)
    c.set_pixel(25, 65, OUTLINE) # eye

    return c


def generate_yard_obstacles() -> List[PixelCanvas]:
    """128x32 px (4 frames 32x32): 4 stackable obstacle block skins."""
    frames = []

    # Frame 0: Stacked Terracotta Flowerpots
    c0 = PixelCanvas(32, 32, TRANSPARENT)
    # Pot 1 (Bottom, y=14..31)
    c0.polygon([(4, 31), (28, 31), (25, 18), (7, 18)], Y_POT_DARK, outline=OUTLINE)
    c0.line(5, 30, 27, 30, Y_POT_LIGHT)
    c0.rect(6, 15, 20, 4, Y_POT_LIGHT, outline=OUTLINE) # rim
    # Pot 2 (Top, y=0..15)
    c0.polygon([(6, 15), (26, 15), (23, 3), (9, 3)], Y_POT_DARK, outline=OUTLINE)
    c0.rect(8, 0, 16, 4, Y_POT_LIGHT, outline=OUTLINE) # rim
    frames.append(c0)

    # Frame 1: Garden Gnome
    c1 = PixelCanvas(32, 32, TRANSPARENT)
    # Red pointed hat (y=2..14)
    c1.polygon([(8, 14), (24, 14), (16, 2)], RED_MID, outline=OUTLINE)
    c1.line(9, 13, 23, 13, RED_LIGHT)
    # Round nose & white beard (y=13..23)
    c1.circle(16, 18, 7, PURE_WHITE, outline=OUTLINE)
    c1.circle(16, 15, 3, SKIN_LIGHT, outline=OUTLINE) # nose
    # Blue smock body (y=22..31)
    c1.rect(10, 22, 12, 9, BLUE_MID, outline=OUTLINE)
    c1.rect(10, 26, 12, 2, OUTLINE) # black belt
    c1.set_pixel(16, 27, Y_LIGHT_GOLD) # buckle
    frames.append(c1)

    # Frame 2: Watering Can
    c2 = PixelCanvas(32, 32, TRANSPARENT)
    # Galvanized green body (y=10..31)
    c2.rect(6, 12, 18, 19, Y_GRASS_SHADOW, outline=OUTLINE)
    c2.line(7, 13, 23, 13, Y_GRASS_LIGHT)
    # Arched handle over top (y=2..12)
    c2.line(8, 12, 8, 4, OUTLINE)
    c2.line(8, 4, 22, 4, OUTLINE)
    c2.line(22, 4, 22, 12, OUTLINE)
    # Angled spout on right (x=24..30, y=14..24)
    c2.polygon([(24, 24), (30, 14), (28, 12), (24, 20)], Y_GRASS_SHADOW, outline=OUTLINE)
    frames.append(c2)

    # Frame 3: Stack of Red Masonry Bricks
    c3 = PixelCanvas(32, 32, TRANSPARENT)
    for i in range(3):
        by = 22 - i * 10
        c3.rect(2, by, 28, 9, Y_POT_DARK, outline=OUTLINE)
        c3.line(3, by + 1, 29, by + 1, Y_POT_LIGHT)
        # Mortar joint line
        c3.line(2, by + 9, 30, by + 9, WHITE_SHADOW)
    frames.append(c3)

    return frames


def generate_yard_obstacles_tall() -> List[PixelCanvas]:
    """128x32 px (4 frames 32x32): 4 cap variants for tall stack."""
    frames = []

    # Frame 0: Blooming magenta tulip in flowerpot
    c0 = PixelCanvas(32, 32, TRANSPARENT)
    # Soil rim of pot
    c0.rect(6, 26, 20, 6, Y_SOIL_DARK, outline=OUTLINE)
    # Green stalk & leaves
    c0.line(16, 12, 16, 26, Y_GRASS_LIGHT)
    c0.polygon([(16, 22), (10, 18), (16, 20)], Y_SPROUT_BRIGHT, outline=OUTLINE)
    c0.polygon([(16, 20), (22, 16), (16, 18)], Y_SPROUT_BRIGHT, outline=OUTLINE)
    # Blooming Tulip blossom
    c0.polygon([(12, 12), (20, 12), (22, 2), (16, 6), (10, 2)], Y_FLOWER_MAGENTA, outline=OUTLINE)
    c0.set_pixel(16, 8, RED_LIGHT)
    frames.append(c0)

    # Frame 1: Pointed gnome hat cap with gold star
    c1 = PixelCanvas(32, 32, TRANSPARENT)
    # Conical red hat
    c1.polygon([(10, 28), (22, 28), (16, 8)], RED_MID, outline=OUTLINE)
    c1.line(11, 27, 21, 27, RED_LIGHT)
    # Gold star on top tip
    c1.circle(16, 6, 3, Y_LIGHT_GOLD, outline=OUTLINE)
    c1.set_pixel(16, 6, Y_LIGHT_FILAMENT)
    frames.append(c1)

    # Frame 2: Brass sprinkler rosette nozzle
    c2 = PixelCanvas(32, 32, TRANSPARENT)
    # Angled spout tube
    c2.line(8, 28, 18, 14, Y_GRASS_SHADOW)
    c2.line(9, 29, 19, 15, Y_GRASS_LIGHT)
    # Perforated circular brass rosette
    c2.circle(22, 10, 8, Y_LIGHT_GOLD, outline=OUTLINE)
    c2.circle(22, 10, 5, Y_LIGHT_FILAMENT)
    # Spray hole dots
    for dx_n, dy_n in [(-3, 0), (3, 0), (0, -3), (0, 3), (0, 0)]:
        c2.set_pixel(22 + dx_n, 10 + dy_n, OUTLINE)
    frames.append(c2)

    # Frame 3: Top brick with velvet moss patch & white pebble
    c3 = PixelCanvas(32, 32, TRANSPARENT)
    c3.rect(2, 20, 28, 12, Y_POT_DARK, outline=OUTLINE)
    c3.line(3, 21, 29, 21, Y_POT_LIGHT)
    # Velvet green moss patch on top
    c3.rect(6, 17, 16, 4, Y_GRASS_LIGHT, outline=OUTLINE)
    c3.set_pixel(8, 16, Y_SPROUT_BRIGHT)
    c3.set_pixel(14, 16, Y_SPROUT_BRIGHT)
    # White pebble
    c3.circle(24, 18, 3, PURE_WHITE, outline=OUTLINE)
    frames.append(c3)

    return frames


# ==============================================================================
# BACKYARD GOAL GATE: yard_goal.png (384x128, 6 frames 64x128 @ 10 fps)
# ==============================================================================

def generate_yard_goal() -> List[PixelCanvas]:
    """
    384x128 px (6 frames of 64x128 @ 10 fps):
    Spinning four-blade pinwheel on wooden garden stake.
    Pole at x=28..36, y=20..127.
    Pinwheel at cx=32, cy=36 rotating 360 degrees.
    """
    frames = []

    # 4 Blade colors: Magenta, Cyan, Gold, Green
    blade_colors = [Y_FLOWER_MAGENTA, Y_WATER_CYAN, Y_LIGHT_GOLD, Y_SPROUT_BRIGHT]

    for f in range(6):
        c = PixelCanvas(64, 128, TRANSPARENT)

        # 1. Wooden Garden Stake (x=29..35, y=30..127)
        for py in range(35, 124):
            c.rect(30, py, 4, 1, Y_SOIL_MID)
            c.set_pixel(30, py, Y_DIRT_DRY)
            c.set_pixel(33, py, Y_SOIL_DARK)
            c.set_pixel(29, py, OUTLINE)
            c.set_pixel(34, py, OUTLINE)

        # Sharpened point driven into ground at y=124..127
        c.polygon([(29, 124), (34, 124), (32, 127)], Y_SOIL_DARK, outline=OUTLINE)
        # Grass tufts at base
        c.line(26, 126, 28, 120, Y_SPROUT_BRIGHT)
        c.line(35, 126, 37, 120, Y_SPROUT_BRIGHT)

        # 2. Spinning Pinwheel (cx=32, cy=34)
        cx, cy = 32, 34
        base_angle = f * 60 # 0, 60, 120, 180, 240, 300 deg

        for b_idx in range(4):
            b_ang = math.radians(base_angle + b_idx * 90)
            col = blade_colors[b_idx]

            # Blade tip & folded wing
            tip_x = int(cx + math.cos(b_ang) * 20)
            tip_y = int(cy + math.sin(b_ang) * 20)
            wing_x = int(cx + math.cos(b_ang + 0.4) * 16)
            wing_y = int(cy + math.sin(b_ang + 0.4) * 16)

            c.polygon([(cx, cy), (tip_x, tip_y), (wing_x, wing_y)], col, outline=OUTLINE)
            c.line(cx, cy, tip_x, tip_y, PURE_WHITE) # crease shine

        # Center Brass Pin (cx=32, cy=34)
        c.circle(cx, cy, 4, Y_LIGHT_GOLD, outline=OUTLINE)
        c.set_pixel(cx, cy, PURE_WHITE)

        frames.append(c)

    return frames

# ==============================================================================
# BACKYARD FLOOR CLUTTER (10 ITEMS + 10 SHADOWS)
# ==============================================================================

def generate_yard_clutter() -> Dict[str, PixelCanvas]:
    """Generates all 10 Backyard floor clutter items and their 10 matching shadows."""
    res = {}

    # 1. Fallen Cosmos Flower (28x20)
    c1 = PixelCanvas(28, 20, TRANSPARENT)
    # 5 Magenta petals
    for deg in range(0, 360, 72):
        rad = math.radians(deg)
        px_f = int(14 + math.cos(rad) * 7)
        py_f = int(10 + math.sin(rad) * 6)
        c1.circle(px_f, py_f, 4, Y_FLOWER_MAGENTA, outline=OUTLINE)
        c1.set_pixel(px_f, py_f, RED_LIGHT)
    # Yellow pistil center
    c1.circle(14, 10, 3, Y_LIGHT_GOLD, outline=OUTLINE)
    c1.set_pixel(14, 10, Y_LIGHT_FILAMENT)
    res["yard_deco_flower.png"] = c1
    res["yard_deco_flower_shadow.png"] = make_shadow(28, 20, 14, 12, 11, 5)

    # 2. Forked Twig with Leaf Bud (40x16)
    c2 = PixelCanvas(40, 16, TRANSPARENT)
    # Main branch
    c2.line(4, 10, 34, 7, Y_SOIL_MID)
    c2.line(4, 9, 34, 6, Y_DIRT_DRY)
    c2.set_pixel(3, 9, OUTLINE)
    c2.set_pixel(3, 10, OUTLINE)
    # Fork branch
    c2.line(18, 9, 30, 13, Y_SOIL_MID)
    c2.line(19, 8, 31, 12, Y_DIRT_DRY)
    # Fresh green leaf bud
    c2.polygon([(34, 6), (38, 3), (35, 2)], Y_SPROUT_BRIGHT, outline=OUTLINE)
    res["yard_deco_stick.png"] = c2
    res["yard_deco_stick_shadow.png"] = make_shadow(40, 16, 20, 11, 16, 4)

    # 3. Toy Sand Shovel (38x20)
    c3 = PixelCanvas(38, 20, TRANSPARENT)
    # Red spade blade (x=4..18, y=5..15)
    c3.polygon([(4, 5), (16, 5), (18, 15), (4, 15)], RED_MID, outline=OUTLINE)
    c3.line(5, 6, 15, 6, RED_LIGHT)
    # Yellow handle shaft & D-grip
    c3.line(17, 10, 30, 10, Y_LIGHT_GOLD)
    c3.line(17, 9, 30, 9, Y_LIGHT_FILAMENT)
    # D-Grip at end
    c3.circle(33, 10, 4, Y_LIGHT_GOLD, outline=OUTLINE)
    c3.circle(33, 10, 2, TRANSPARENT)
    res["yard_deco_toy_shovel.png"] = c3
    res["yard_deco_toy_shovel_shadow.png"] = make_shadow(38, 20, 19, 13, 15, 5)

    # 4. Plump Acorn with Cap (22x18)
    c4 = PixelCanvas(22, 18, TRANSPARENT)
    # Nut body (cx=11, cy=10, r=6)
    c4.polygon([(6, 8), (16, 8), (13, 16), (9, 16)], Y_DIRT_DRY, outline=OUTLINE)
    c4.line(7, 9, 15, 9, WOOD_HIGHLIGHT)
    # Crosshatch textured cap
    c4.circle(11, 6, 6, Y_SOIL_DARK, outline=OUTLINE)
    c4.line(7, 6, 15, 6, Y_SOIL_MID)
    # Stem
    c4.line(11, 2, 14, 0, Y_SOIL_DARK)
    res["yard_deco_acorn.png"] = c4
    res["yard_deco_acorn_shadow.png"] = make_shadow(22, 18, 11, 12, 8, 4)

    # 5. Ladybug Beetle (20x16)
    c5 = PixelCanvas(20, 16, TRANSPARENT)
    # Shiny red domed shell
    c5.circle(11, 8, 6, RED_MID, outline=OUTLINE)
    c5.circle(10, 6, 3, RED_LIGHT)
    # Black center split line
    c5.line(7, 8, 17, 8, OUTLINE)
    # Black spots
    c5.set_pixel(10, 5, OUTLINE)
    c5.set_pixel(13, 5, OUTLINE)
    c5.set_pixel(10, 11, OUTLINE)
    c5.set_pixel(13, 11, OUTLINE)
    # Head & antennae
    c5.circle(5, 8, 3, OUTLINE)
    c5.set_pixel(2, 6, OUTLINE)
    c5.set_pixel(2, 10, OUTLINE)
    res["yard_deco_ladybug.png"] = c5
    res["yard_deco_ladybug_shadow.png"] = make_shadow(20, 16, 10, 10, 7, 4)

    # 6. Dandelion Flower Bloom (26x22)
    c6 = PixelCanvas(26, 22, TRANSPARENT)
    # Green sepals & stem
    c6.line(13, 14, 13, 20, Y_GRASS_MID)
    c6.polygon([(8, 14), (18, 14), (13, 11)], Y_GRASS_LIGHT, outline=OUTLINE)
    # Yellow fluffy petals
    c6.circle(13, 9, 8, Y_LIGHT_GOLD, outline=OUTLINE)
    c6.circle(13, 8, 5, Y_LIGHT_FILAMENT)
    for deg in range(0, 360, 40):
        rad = math.radians(deg)
        px_d = int(13 + math.cos(rad) * 7)
        py_d = int(9 + math.sin(rad) * 6)
        c6.set_pixel(px_d, py_d, PURE_WHITE)
    res["yard_deco_dandelion.png"] = c6
    res["yard_deco_dandelion_shadow.png"] = make_shadow(26, 22, 13, 15, 10, 5)

    # 7. Chewed Dog Bone (36x18)
    c7 = PixelCanvas(36, 18, TRANSPARENT)
    # Bone shaft
    c7.rect(10, 7, 16, 5, PURE_WHITE, outline=OUTLINE)
    c7.line(11, 8, 25, 8, WHITE_SHADOW)
    # Knobby chewed ends
    # Left knobs
    c7.circle(9, 6, 3, PURE_WHITE, outline=OUTLINE)
    c7.circle(9, 12, 3, PURE_WHITE, outline=OUTLINE)
    # Right knobs
    c7.circle(27, 6, 3, PURE_WHITE, outline=OUTLINE)
    c7.circle(27, 12, 3, PURE_WHITE, outline=OUTLINE)
    # Gnawed texture scratches
    c7.set_pixel(14, 9, WHITE_SHADOW)
    c7.set_pixel(22, 9, WHITE_SHADOW)
    res["yard_deco_chewed_bone.png"] = c7
    res["yard_deco_chewed_bone_shadow.png"] = make_shadow(36, 18, 18, 11, 14, 5)

    # 8. Muddy Sneaker (40x24)
    c8 = PixelCanvas(40, 24, TRANSPARENT)
    # Blue sneaker upper
    c8.polygon([(6, 16), (12, 8), (28, 8), (34, 16)], BLUE_MID, outline=OUTLINE)
    c8.line(13, 9, 27, 9, BLUE_LIGHT)
    # White laces
    for lx in [16, 20, 24]:
        c8.line(lx, 10, lx + 2, 13, PURE_WHITE)
    # White rubber toe & sole
    c8.rect(4, 16, 33, 4, PURE_WHITE, outline=OUTLINE)
    # Dark garden mud splatters on toe & heel
    c8.polygon([(4, 16), (12, 16), (8, 20)], Y_SOIL_DARK)
    c8.circle(30, 18, 3, Y_SOIL_DARK)
    c8.set_pixel(18, 17, Y_DIRT_DRY)
    res["yard_deco_muddy_sneaker.png"] = c8
    res["yard_deco_muddy_sneaker_shadow.png"] = make_shadow(40, 24, 20, 17, 16, 6)

    # 9. Kite String Spool (36x22)
    c9 = PixelCanvas(36, 22, TRANSPARENT)
    # Wooden cross frame
    c9.rect(6, 9, 24, 4, Y_SOIL_MID, outline=OUTLINE)
    c9.rect(16, 3, 4, 16, Y_SOIL_MID, outline=OUTLINE)
    # Bright orange wound kite string
    c9.rect(12, 6, 12, 10, ORANGE_MID, outline=OUTLINE)
    c9.line(13, 7, 23, 7, ORANGE_LIGHT)
    # Trailing loose string tail
    c9.line(24, 14, 32, 18, ORANGE_MID)
    res["yard_deco_kite_string_spool.png"] = c9
    res["yard_deco_kite_string_spool_shadow.png"] = make_shadow(36, 22, 18, 14, 14, 5)

    # 10. Plastic Frisbee (44x20)
    c10 = PixelCanvas(44, 20, TRANSPARENT)
    # Aerodynamic curved disc profile
    c10.circle(22, 10, 18, RED_MID, outline=OUTLINE)
    # Tilted oval mask
    c10.circle(22, 8, 15, RED_LIGHT)
    # Concentric aerodynamic ridges
    c10.circle(22, 8, 11, RED_MID)
    c10.circle(22, 8, 8, RED_LIGHT)
    c10.set_pixel(22, 6, PURE_WHITE) # glint
    res["yard_deco_frisbee.png"] = c10
    res["yard_deco_frisbee_shadow.png"] = make_shadow(44, 20, 22, 13, 17, 5)

    return res


# ==============================================================================
# BACKYARD ANIMATED PROPS (6 PROPS)
# ==============================================================================

def generate_yard_prop_swing() -> List[PixelCanvas]:
    """960x128 px (10 frames 96x128 @ 6 fps): Tire swing swaying back and forth."""
    frames = []

    # Pendulum angles across 10 frames
    swing_angles = [-8, -6, -2, 3, 7, 8, 5, 0, -4, -7]

    for f in range(10):
        c = PixelCanvas(96, 128, TRANSPARENT)

        ang = math.radians(swing_angles[f])

        # Top anchor branch at (48, 8)
        c.rect(36, 6, 24, 6, Y_SOIL_DARK, outline=OUTLINE)
        c.line(37, 7, 59, 7, Y_SOIL_MID)

        # Tire center coordinates
        tire_len = 80
        tc_x = int(48 + math.sin(ang) * tire_len)
        tc_y = int(8 + math.cos(ang) * tire_len)

        # Twin ropes hanging from branch
        c.line(45, 12, tc_x - 5, tc_y - 18, Y_DIRT_DRY)
        c.line(51, 12, tc_x + 5, tc_y - 18, Y_DIRT_DRY)

        # Black Rubber Tire (cx=tc_x, cy=tc_y, r=20)
        c.circle(tc_x, tc_y, 20, VOID_BLACK, outline=OUTLINE)
        c.circle(tc_x, tc_y, 11, TRANSPARENT)
        c.circle(tc_x, tc_y, 20, VOID_BLACK, outline=OUTLINE)
        c.circle(tc_x, tc_y, 11, VOID_BLACK, outline=OUTLINE)

        # Rubber highlight rim
        c.circle(tc_x - 2, tc_y - 2, 18, METAL_SHADOW)
        c.circle(tc_x - 2, tc_y - 2, 13, VOID_BLACK)

        frames.append(c)
    return frames


def generate_yard_prop_string_lights() -> List[PixelCanvas]:
    """1024x48 px (8 frames 128x48 @ 4 fps): String garland with 5 glowing Edison bulbs."""
    frames = []

    # 5 Bulbs at x=14, 38, 64, 90, 114
    bulb_x = [14, 38, 64, 90, 114]

    for f in range(8):
        c = PixelCanvas(128, 48, TRANSPARENT)

        # Drooping Dark Wire Cable across top (y=10..20)
        for x in range(128):
            wy = int(10 + math.sin(x * 0.05) * 6)
            c.set_pixel(x, wy, OUTLINE)

        # 5 Edison Bulbs
        for b_idx, bx in enumerate(bulb_x):
            wy = int(10 + math.sin(bx * 0.05) * 6)

            # Bulb Socket
            c.rect(bx - 2, wy, 5, 4, METAL_SHADOW, outline=OUTLINE)

            # Glass Bulb Body (cy=wy + 10, r=6)
            by = wy + 9
            b_phase = (f + b_idx * 2) % 8

            # Filament & Halo Breathing Cycle
            if b_phase in [0, 1]:
                # Bright Starburst
                c.circle(bx, by, 7, Y_LIGHT_GOLD)
                c.circle(bx, by, 4, Y_LIGHT_FILAMENT)
                c.set_pixel(bx, by, PURE_WHITE)
            elif b_phase in [2, 7]:
                # Medium Glow
                c.circle(bx, by, 5, Y_LIGHT_GOLD)
                c.circle(bx, by, 3, Y_LIGHT_FILAMENT)
            else:
                # Dim Filament
                c.circle(bx, by, 4, Y_FENCE_MID, outline=OUTLINE)
                c.set_pixel(bx, by, Y_LIGHT_GOLD)

        frames.append(c)
    return frames


def generate_yard_prop_windmill() -> List[PixelCanvas]:
    """512x96 px (8 frames 64x96 @ 12 fps): Garden windmill ornament with 6 spinning rainbow blades."""
    frames = []

    # 6 Rainbow blade colors
    rainbow_cols = [RED_MID, Y_LIGHT_GOLD, Y_SPROUT_BRIGHT, Y_WATER_CYAN, BLUE_MID, Y_FLOWER_MAGENTA]

    for f in range(8):
        c = PixelCanvas(64, 96, TRANSPARENT)

        # Green Metal Pole (x=30..33, y=36..95)
        c.rect(31, 36, 3, 58, Y_GRASS_MID, outline=OUTLINE)
        c.line(32, 36, 32, 94, Y_SPROUT_BRIGHT)

        # Windmill Hub at (32, 36)
        cx, cy = 32, 36
        base_angle = f * 45 # 0, 45, 90, 135, 180, 225, 270, 315 deg

        # 6 Blades spinning
        for b_idx in range(6):
            b_ang = math.radians(base_angle + b_idx * 60)
            col = rainbow_cols[b_idx]

            tip_x = int(cx + math.cos(b_ang) * 22)
            tip_y = int(cy + math.sin(b_ang) * 22)
            wing_x = int(cx + math.cos(b_ang + 0.3) * 16)
            wing_y = int(cy + math.sin(b_ang + 0.3) * 16)

            c.polygon([(cx, cy), (tip_x, tip_y), (wing_x, wing_y)], col, outline=OUTLINE)
            c.set_pixel(tip_x, tip_y, PURE_WHITE)

        # Center Brass Hub Nut
        c.circle(cx, cy, 4, Y_LIGHT_GOLD, outline=OUTLINE)
        c.set_pixel(cx, cy, PURE_WHITE)

        frames.append(c)
    return frames


def generate_yard_prop_sprinkler_idle() -> List[PixelCanvas]:
    """288x48 px (6 frames 48x48 @ 6 fps): Brass oscillating sprinkler rocking back and forth."""
    frames = []

    # Pivot angles across 6 frames
    tube_angles = [-25, -15, 0, 15, 25, 10]

    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)

        # Heavy Metal Sled Base (x=8..40, y=38..46)
        c.rect(8, 42, 32, 4, Y_FENCE_SHADOW, outline=OUTLINE)
        c.line(8, 42, 40, 42, Y_FENCE_MID)
        # Sled runner curved tips
        c.line(8, 42, 5, 39, Y_FENCE_SHADOW)
        c.line(40, 42, 43, 39, Y_FENCE_SHADOW)

        # Center Brass Water Motor Housing (x=20..28, y=34..42)
        c.rect(20, 34, 8, 8, Y_LIGHT_GOLD, outline=OUTLINE)
        c.line(21, 35, 21, 41, Y_LIGHT_FILAMENT)

        # Oscillating Curved Brass Spray Bar
        ang = math.radians(tube_angles[f])
        for step in range(-12, 13, 2):
            bx = int(24 + step * math.cos(ang))
            by = int(32 + step * math.sin(ang) - (12 - abs(step)) * 0.3)
            c.rect(bx - 1, by - 1, 2, 2, Y_LIGHT_GOLD, outline=OUTLINE)
            # Tiny spray jet nozzles
            if step % 4 == 0:
                c.set_pixel(bx, by - 2, Y_LIGHT_FILAMENT)

        frames.append(c)
    return frames


def generate_yard_prop_gnome() -> List[PixelCanvas]:
    """384x64 px (8 frames 48x64 @ 4 fps): Garden gnome with playful wink on frames 5-6."""
    frames = []

    for f in range(8):
        c = PixelCanvas(48, 64, TRANSPARENT)

        # Red Pointed Hat (y=6..26)
        c.polygon([(14, 26), (34, 26), (24, 6)], RED_MID, outline=OUTLINE)
        c.line(15, 25, 33, 25, RED_LIGHT)

        # Round Nose & Bushy Beard (y=24..44)
        c.circle(24, 36, 12, PURE_WHITE, outline=OUTLINE)
        c.circle(24, 30, 4, SKIN_LIGHT, outline=OUTLINE) # round bulbous nose

        # Blue Smock Body & Black Belt (y=40..58)
        c.rect(14, 40, 20, 18, BLUE_MID, outline=OUTLINE)
        c.line(15, 41, 15, 57, BLUE_LIGHT)
        c.rect(14, 48, 20, 3, OUTLINE) # belt
        c.set_pixel(24, 49, Y_LIGHT_GOLD) # buckle

        # Brown Boots (y=58..62)
        c.rect(15, 58, 8, 4, Y_SOIL_DARK, outline=OUTLINE)
        c.rect(25, 58, 8, 4, Y_SOIL_DARK, outline=OUTLINE)

        # Eyes at (20, 26) and (28, 26)
        # Right eye always open
        c.circle(28, 26, 2, OUTLINE)
        c.set_pixel(28, 25, PURE_WHITE)

        # Left eye: wink on frames 5-6!
        if f == 5:
            # Squinting
            c.line(18, 26, 22, 26, OUTLINE)
        elif f == 6:
            # Full playful wink (curved happy slit)
            c.line(18, 27, 20, 25, OUTLINE)
            c.line(20, 25, 22, 27, OUTLINE)
            c.line(18, 22, 22, 21, RED_MID) # raised eyebrow!
        else:
            # Open eye
            c.circle(20, 26, 2, OUTLINE)
            c.set_pixel(20, 25, PURE_WHITE)

        frames.append(c)
    return frames


def generate_yard_prop_butterflies() -> List[PixelCanvas]:
    """640x64 px (10 frames 64x64 @ 8 fps): Two butterflies dancing in figure-8 flight."""
    frames = []

    for f in range(10):
        c = PixelCanvas(64, 64, TRANSPARENT)

        # Butterfly 1 (Cyan): Clockwise orbit
        t1 = 2.0 * math.pi * f / 10.0
        b1_x = int(32 + 16 * math.cos(t1))
        b1_y = int(28 + 10 * math.sin(t1))

        # Butterfly 2 (Magenta): Counter-clockwise orbit
        t2 = 2.0 * math.pi * (f + 5) / 10.0
        b2_x = int(32 + 14 * math.cos(-t2))
        b2_y = int(36 + 10 * math.sin(-t2))

        # Helper to draw butterfly with flapping wings
        def draw_butterfly(bx: int, by: int, col: RGBA, phase: int):
            c.set_pixel(bx, by, OUTLINE) # body
            w_flap = phase % 3
            if w_flap == 0:
                # Wings open wide
                c.polygon([(bx - 1, by), (bx - 6, by - 5), (bx - 5, by + 3)], col, outline=OUTLINE)
                c.polygon([(bx + 1, by), (bx + 6, by - 5), (bx + 5, by + 3)], col, outline=OUTLINE)
                c.set_pixel(bx - 3, by - 2, PURE_WHITE)
                c.set_pixel(bx + 3, by - 2, PURE_WHITE)
            elif w_flap == 1:
                # Wings 45 deg
                c.line(bx - 1, by, bx - 4, by - 4, col)
                c.line(bx + 1, by, bx + 4, by - 4, col)
            else:
                # Wings folded up
                c.line(bx, by - 1, bx, by - 6, col)
                c.set_pixel(bx, by - 6, PURE_WHITE)

        draw_butterfly(b1_x, b1_y, Y_WATER_CYAN, f)
        draw_butterfly(b2_x, b2_y, Y_FLOWER_MAGENTA, f + 1)

        frames.append(c)
    return frames

# ==============================================================================
# MANIFEST ENTRIES & MAIN EXPORT PIPELINE
# ==============================================================================

MANIFEST_ENTRIES = {
    # UI
    "ui_stage_card.png": {"frame_w": 480, "frame_h": 144, "frames": 5, "fps": 0, "loop": False},

    # Kitchen Parallax & Foreground
    "kitchen_sky_gradient.png": {"frame_w": 1, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "kitchen_bg_far.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "kitchen_bg_far_anim.png": {"frame_w": 960, "frame_h": 540, "frames": 4, "fps": 3, "loop": True},
    "kitchen_bg_mid.png": {"frame_w": 1280, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "kitchen_bg_near.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "kitchen_fg_legs.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "kitchen_fg_dust.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},

    # Kitchen Tileset & Obstacles
    "kitchen_tileset_floor.png": {"frame_w": 256, "frame_h": 96, "frames": 1, "fps": 0, "loop": False, "tile_w": 32, "tile_h": 32, "columns": 8, "rows": 3},
    "kitchen_pit_bg.png": {"frame_w": 32, "frame_h": 128, "frames": 1, "fps": 0, "loop": False},
    "kitchen_obstacles.png": {"frame_w": 32, "frame_h": 32, "frames": 4, "fps": 0, "loop": False},
    "kitchen_obstacles_tall.png": {"frame_w": 32, "frame_h": 32, "frames": 4, "fps": 0, "loop": False},

    # Kitchen Goal
    "kitchen_goal.png": {"frame_w": 64, "frame_h": 128, "frames": 6, "fps": 10, "loop": True},

    # Kitchen Clutter (10 items + 10 shadows)
    "kitchen_deco_cereal.png": {"frame_w": 32, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_cereal_shadow.png": {"frame_w": 32, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_spilled_sugar.png": {"frame_w": 40, "frame_h": 22, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_spilled_sugar_shadow.png": {"frame_w": 40, "frame_h": 22, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_fork.png": {"frame_w": 36, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_fork_shadow.png": {"frame_w": 36, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_spoon.png": {"frame_w": 36, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_spoon_shadow.png": {"frame_w": 36, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_bottle_cap.png": {"frame_w": 24, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_bottle_cap_shadow.png": {"frame_w": 24, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_crushed_juice_box.png": {"frame_w": 36, "frame_h": 24, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_crushed_juice_box_shadow.png": {"frame_w": 36, "frame_h": 24, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_pasta.png": {"frame_w": 32, "frame_h": 18, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_pasta_shadow.png": {"frame_w": 32, "frame_h": 18, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_banana_peel.png": {"frame_w": 38, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_banana_peel_shadow.png": {"frame_w": 38, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_flour_handprint.png": {"frame_w": 34, "frame_h": 26, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_flour_handprint_shadow.png": {"frame_w": 34, "frame_h": 26, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_grape.png": {"frame_w": 20, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "kitchen_deco_grape_shadow.png": {"frame_w": 20, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},

    # Kitchen Animated Props
    "kitchen_prop_fridge_light.png": {"frame_w": 96, "frame_h": 128, "frames": 6, "fps": 6, "loop": True},
    "kitchen_prop_kettle.png": {"frame_w": 64, "frame_h": 64, "frames": 8, "fps": 8, "loop": True},
    "kitchen_prop_clock.png": {"frame_w": 64, "frame_h": 64, "frames": 8, "fps": 4, "loop": True},
    "kitchen_prop_toaster.png": {"frame_w": 64, "frame_h": 64, "frames": 10, "fps": 8, "loop": True},
    "kitchen_prop_dripping_tap.png": {"frame_w": 48, "frame_h": 80, "frames": 10, "fps": 10, "loop": True},
    "kitchen_prop_fruit_fly.png": {"frame_w": 48, "frame_h": 48, "frames": 8, "fps": 10, "loop": True},

    # Backyard Parallax & Foreground
    "yard_sky_gradient.png": {"frame_w": 1, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "yard_bg_far.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "yard_bg_far_anim.png": {"frame_w": 960, "frame_h": 540, "frames": 4, "fps": 3, "loop": True},
    "yard_bg_mid.png": {"frame_w": 1280, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "yard_bg_near.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "yard_fg_legs.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "yard_fg_dust.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},

    # Backyard Tileset & Obstacles
    "yard_tileset_floor.png": {"frame_w": 256, "frame_h": 96, "frames": 1, "fps": 0, "loop": False, "tile_w": 32, "tile_h": 32, "columns": 8, "rows": 3},
    "yard_pit_bg.png": {"frame_w": 32, "frame_h": 128, "frames": 1, "fps": 0, "loop": False},
    "yard_obstacles.png": {"frame_w": 32, "frame_h": 32, "frames": 4, "fps": 0, "loop": False},
    "yard_obstacles_tall.png": {"frame_w": 32, "frame_h": 32, "frames": 4, "fps": 0, "loop": False},

    # Backyard Goal
    "yard_goal.png": {"frame_w": 64, "frame_h": 128, "frames": 6, "fps": 10, "loop": True},

    # Backyard Clutter (10 items + 10 shadows)
    "yard_deco_flower.png": {"frame_w": 28, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_flower_shadow.png": {"frame_w": 28, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_stick.png": {"frame_w": 40, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_stick_shadow.png": {"frame_w": 40, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_toy_shovel.png": {"frame_w": 38, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_toy_shovel_shadow.png": {"frame_w": 38, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_acorn.png": {"frame_w": 22, "frame_h": 18, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_acorn_shadow.png": {"frame_w": 22, "frame_h": 18, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_ladybug.png": {"frame_w": 20, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_ladybug_shadow.png": {"frame_w": 20, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_dandelion.png": {"frame_w": 26, "frame_h": 22, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_dandelion_shadow.png": {"frame_w": 26, "frame_h": 22, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_chewed_bone.png": {"frame_w": 36, "frame_h": 18, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_chewed_bone_shadow.png": {"frame_w": 36, "frame_h": 18, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_muddy_sneaker.png": {"frame_w": 40, "frame_h": 24, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_muddy_sneaker_shadow.png": {"frame_w": 40, "frame_h": 24, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_kite_string_spool.png": {"frame_w": 36, "frame_h": 22, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_kite_string_spool_shadow.png": {"frame_w": 36, "frame_h": 22, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_frisbee.png": {"frame_w": 44, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "yard_deco_frisbee_shadow.png": {"frame_w": 44, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},

    # Backyard Animated Props
    "yard_prop_swing.png": {"frame_w": 96, "frame_h": 128, "frames": 10, "fps": 6, "loop": True},
    "yard_prop_string_lights.png": {"frame_w": 128, "frame_h": 48, "frames": 8, "fps": 4, "loop": True},
    "yard_prop_windmill.png": {"frame_w": 64, "frame_h": 96, "frames": 8, "fps": 12, "loop": True},
    "yard_prop_sprinkler_idle.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 6, "loop": True},
    "yard_prop_gnome.png": {"frame_w": 48, "frame_h": 64, "frames": 8, "fps": 4, "loop": True},
    "yard_prop_butterflies.png": {"frame_w": 64, "frame_h": 64, "frames": 10, "fps": 8, "loop": True},
}


def main():
    art_dir = Path("art/v2")
    art_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = art_dir / "manifest.json"

    print("=================================================================")
    print("Generating Kitchen & Backyard Stage Assets + UI Stage Card")
    print("=================================================================")

    # 1. UI Stage Card (5 frames 480x144)
    print("Generating ui_stage_card.png...")
    assemble_strip(generate_ui_stage_card(), str(art_dir / "ui_stage_card.png"))

    # 2. Kitchen Parallax & Foreground
    print("Generating Kitchen Parallax & Foreground...")
    save_single(generate_kitchen_sky_gradient(), str(art_dir / "kitchen_sky_gradient.png"))
    save_single(generate_kitchen_bg_far(), str(art_dir / "kitchen_bg_far.png"))
    assemble_strip(generate_kitchen_bg_far_anim(), str(art_dir / "kitchen_bg_far_anim.png"))
    save_single(generate_kitchen_bg_mid(), str(art_dir / "kitchen_bg_mid.png"))
    save_single(generate_kitchen_bg_near(), str(art_dir / "kitchen_bg_near.png"))
    save_single(generate_kitchen_fg_legs(), str(art_dir / "kitchen_fg_legs.png"))
    save_single(generate_kitchen_fg_dust(), str(art_dir / "kitchen_fg_dust.png"))

    # 3. Kitchen Tileset & Obstacles
    print("Generating Kitchen Tileset & Obstacles...")
    save_single(generate_kitchen_tileset_floor(), str(art_dir / "kitchen_tileset_floor.png"))
    save_single(generate_kitchen_pit_bg(), str(art_dir / "kitchen_pit_bg.png"))
    assemble_strip(generate_kitchen_obstacles(), str(art_dir / "kitchen_obstacles.png"))
    assemble_strip(generate_kitchen_obstacles_tall(), str(art_dir / "kitchen_obstacles_tall.png"))

    # 4. Kitchen Goal
    print("Generating kitchen_goal.png...")
    assemble_strip(generate_kitchen_goal(), str(art_dir / "kitchen_goal.png"))

    # 5. Kitchen Clutter (10 items + 10 shadows)
    print("Generating Kitchen Clutter...")
    k_clutter = generate_kitchen_clutter()
    for filename, canvas in k_clutter.items():
        save_single(canvas, str(art_dir / filename))

    # 6. Kitchen Animated Props
    print("Generating Kitchen Animated Props...")
    assemble_strip(generate_kitchen_prop_fridge_light(), str(art_dir / "kitchen_prop_fridge_light.png"))
    assemble_strip(generate_kitchen_prop_kettle(), str(art_dir / "kitchen_prop_kettle.png"))
    assemble_strip(generate_kitchen_prop_clock(), str(art_dir / "kitchen_prop_clock.png"))
    assemble_strip(generate_kitchen_prop_toaster(), str(art_dir / "kitchen_prop_toaster.png"))
    assemble_strip(generate_kitchen_prop_dripping_tap(), str(art_dir / "kitchen_prop_dripping_tap.png"))
    assemble_strip(generate_kitchen_prop_fruit_fly(), str(art_dir / "kitchen_prop_fruit_fly.png"))

    # 7. Backyard Parallax & Foreground
    print("Generating Backyard Parallax & Foreground...")
    save_single(generate_yard_sky_gradient(), str(art_dir / "yard_sky_gradient.png"))
    save_single(generate_yard_bg_far(), str(art_dir / "yard_bg_far.png"))
    assemble_strip(generate_yard_bg_far_anim(), str(art_dir / "yard_bg_far_anim.png"))
    save_single(generate_yard_bg_mid(), str(art_dir / "yard_bg_mid.png"))
    save_single(generate_yard_bg_near(), str(art_dir / "yard_bg_near.png"))
    save_single(generate_yard_fg_legs(), str(art_dir / "yard_fg_legs.png"))
    save_single(generate_yard_fg_dust(), str(art_dir / "yard_fg_dust.png"))

    # 8. Backyard Tileset & Obstacles
    print("Generating Backyard Tileset & Obstacles...")
    save_single(generate_yard_tileset_floor(), str(art_dir / "yard_tileset_floor.png"))
    save_single(generate_yard_pit_bg(), str(art_dir / "yard_pit_bg.png"))
    assemble_strip(generate_yard_obstacles(), str(art_dir / "yard_obstacles.png"))
    assemble_strip(generate_yard_obstacles_tall(), str(art_dir / "yard_obstacles_tall.png"))

    # 9. Backyard Goal
    print("Generating yard_goal.png...")
    assemble_strip(generate_yard_goal(), str(art_dir / "yard_goal.png"))

    # 10. Backyard Clutter (10 items + 10 shadows)
    print("Generating Backyard Clutter...")
    y_clutter = generate_yard_clutter()
    for filename, canvas in y_clutter.items():
        save_single(canvas, str(art_dir / filename))

    # 11. Backyard Animated Props
    print("Generating Backyard Animated Props...")
    assemble_strip(generate_yard_prop_swing(), str(art_dir / "yard_prop_swing.png"))
    assemble_strip(generate_yard_prop_string_lights(), str(art_dir / "yard_prop_string_lights.png"))
    assemble_strip(generate_yard_prop_windmill(), str(art_dir / "yard_prop_windmill.png"))
    assemble_strip(generate_yard_prop_sprinkler_idle(), str(art_dir / "yard_prop_sprinkler_idle.png"))
    assemble_strip(generate_yard_prop_gnome(), str(art_dir / "yard_prop_gnome.png"))
    assemble_strip(generate_yard_prop_butterflies(), str(art_dir / "yard_prop_butterflies.png"))

    # Update manifest.json
    print("Updating art/v2/manifest.json...")
    manifest = {}
    if manifest_path.exists():
        with open(manifest_path, "r") as f:
            manifest = json.load(f)

    for k, v in MANIFEST_ENTRIES.items():
        manifest[k] = v

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)

    print(f"Successfully generated all {len(MANIFEST_ENTRIES)} assets and updated manifest.json!")


if __name__ == "__main__":
    main()
