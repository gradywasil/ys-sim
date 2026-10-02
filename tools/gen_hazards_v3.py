"""Younger Sibling Simulator - Phase C Hazards & FX Generator v3.

Generates all Phase C stage hazard sprites, flashlight items, light masks,
and shared hazard feedback particles into art/v2/ according to docs/art-brief-v2.md and v3:

Kitchen hazards:
1. hazard_juice_puddle.png (96x16, 6 frames @ 8 fps, loop: true)
2. hazard_marble.png (24x24, 8 frames @ 14 fps, loop: true)
3. hazard_stove_burner.png (64x48, 10 frames @ 10 fps, loop: true)
4. hazard_spill_trail.png (32x16, 4 frames @ 6 fps, loop: true)

Backyard hazards:
1. hazard_sprinkler.png (64x96, 10 frames @ 10 fps, loop: true)
2. hazard_water_spray.png (192x96, 8 frames @ 14 fps, loop: true)
3. hazard_mud.png (96x16, 6 frames @ 6 fps, loop: true)
4. hazard_wind_gust.png (192x64, 8 frames @ 14 fps, loop: true)
5. fx_leaf.png (16x16, 8 frames @ 12 fps, loop: true)
6. fx_leaf_b.png (16x16, 8 frames @ 12 fps, loop: true)

Basement hazards:
1. hazard_paint_can.png (40x40, 8 frames @ 12 fps, loop: true)
2. hazard_drip.png (16x48, 10 frames @ 12 fps, loop: true)
3. hazard_mousetrap.png (48x24, 8 frames @ 14 fps, loop: false)
4. light_flashlight_cone.png (256x128, 1 frame @ 0 fps)
5. light_dark_mask.png (512x512, 1 frame @ 0 fps)
6. item_flashlight.png (48x48, 6 frames @ 8 fps, loop: true)
7. item_flashlight_pop.png (48x48, 3 frames @ 24 fps, loop: false)

Attic hazards:
1. hazard_cobweb.png (96x64, 6 frames @ 6 fps, loop: true)
2. hazard_loose_board.png (64x24, 8 frames @ 10 fps, loop: false)
3. hazard_dust_cloud.png (64x64, 8 frames @ 10 fps, loop: false)
4. hazard_spider_drop.png (16x64, 10 frames @ 12 fps, loop: true)

Shared hazard feedback:
1. fx_warning_exclaim.png (16x24, 6 frames @ 12 fps, loop: true)
2. fx_slip_swirl.png (32x16, 6 frames @ 16 fps, loop: true)
3. fx_splat.png (32x32, 5 frames @ 20 fps, loop: false)
4. fx_shield_bubble.png (64x64, 8 frames @ 12 fps, loop: false)
5. fx_sugar_blur.png (64x32, 6 frames @ 24 fps, loop: true)
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
    SHADOW_PURPLE_DARK, SHADOW_PURPLE_DEEP, SHADOW_PURPLE_MID,
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

# Stage-specific accent constants
# Kitchen accents
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
K_OLIVE           = STAGE_RGBA["kitchen"][15]  # #7a9150: grape / olive kitchen green

# Backyard accents
Y_TURF_SHADOW     = STAGE_RGBA["yard"][0]      # #0d2b18: deep turf shadow
Y_GRASS_SHADOW    = STAGE_RGBA["yard"][1]      # #194d27: lush grass shadow
Y_GRASS_MID       = STAGE_RGBA["yard"][2]      # #2a7a3b: grass blade mid
Y_GRASS_HL        = STAGE_RGBA["yard"][3]      # #46ad59: grass blade highlight
Y_SPROUT_BRIGHT   = STAGE_RGBA["yard"][4]      # #7eed8f: fresh sprout bright green
Y_SOIL_DARK       = STAGE_RGBA["yard"][5]      # #302213: garden soil loam dark
Y_SOIL_MID        = STAGE_RGBA["yard"][6]      # #593f24: garden soil loam mid
Y_DIRT_DRY        = STAGE_RGBA["yard"][7]      # #8c6840: garden dirt dry
Y_TERRACOTTA_DARK = STAGE_RGBA["yard"][8]      # #c4562d: flowerpot terracotta dark
Y_TERRACOTTA_LIGHT= STAGE_RGBA["yard"][9]      # #eb7844: flowerpot terracotta light
Y_STRING_GOLD     = STAGE_RGBA["yard"][10]     # #f5b338: string light warm gold
Y_STRING_FILAMENT = STAGE_RGBA["yard"][11]     # #ffeb80: string light filament glow
Y_FENCE_SHADOW    = STAGE_RGBA["yard"][12]     # #203b57: dusk fence shadow
Y_FENCE_BLUE      = STAGE_RGBA["yard"][13]     # #3a638c: dusk fence blue-gray
Y_FLOWER_MAGENTA  = STAGE_RGBA["yard"][14]     # #d43b68: garden flower magenta
Y_WATER_CYAN      = STAGE_RGBA["yard"][15]     # #8fedf7: water droplet / dragonfly cyan

# Basement accents
B_CONCRETE_SHADOW = STAGE_RGBA["basement"][0]  # #1e2530: concrete deep shadow
B_CONCRETE_DARK   = STAGE_RGBA["basement"][1]  # #2f3b4c: concrete slab dark
B_CONCRETE_MID    = STAGE_RGBA["basement"][2]  # #4a5a70: concrete mid
B_CONCRETE_LIGHT  = STAGE_RGBA["basement"][3]  # #6e8099: concrete light
B_CONCRETE_HL     = STAGE_RGBA["basement"][4]  # #94a6bd: concrete highlight
B_DRAIN_GRATE     = STAGE_RGBA["basement"][5]  # #151b24: cast iron drain grate
B_RUST_DARK       = STAGE_RGBA["basement"][6]  # #693521: pipe rust dark
B_RUST_MID        = STAGE_RGBA["basement"][7]  # #994e2b: pipe rust mid
B_EMBER_ORANGE    = STAGE_RGBA["basement"][8]  # #c46e37: pipe rust / furnace ember orange
B_FIRE_YELLOW     = STAGE_RGBA["basement"][9]  # #f79434: furnace fire flame yellow-orange
B_FIRE_CORE       = STAGE_RGBA["basement"][10] # #fed147: furnace fire bright core
B_SLATE_DARK      = STAGE_RGBA["basement"][11] # #2b4859: industrial slate dark
B_WATER_PUDDLE    = STAGE_RGBA["basement"][12] # #3f6c85: water puddle blue-gray
B_RIPPLE_HL       = STAGE_RGBA["basement"][13] # #5fa2b8: drip ripple highlight
B_OIL_PURPLE      = STAGE_RGBA["basement"][14] # #3e2a47: oil stain iridescent purple
B_SAWDUST_TAN     = STAGE_RGBA["basement"][15] # #80705a: dry sawdust amber-tan

# Attic accents
A_TIMBER_DEEP     = STAGE_RGBA["attic"][0]     # #241910: aged attic timber deep
A_TIMBER_DARK     = STAGE_RGBA["attic"][1]     # #3d2919: dusty oak board dark
A_FLOORBOARD_MID  = STAGE_RGBA["attic"][2]     # #5c3e24: attic floorboard mid
A_FLOORBOARD_LIGHT= STAGE_RGBA["attic"][3]     # #825832: attic floorboard light
A_WOOD_GRAIN      = STAGE_RGBA["attic"][4]     # #b37f49: warm wood grain amber
A_HONEY_BEAM      = STAGE_RGBA["attic"][5]     # #deb073: golden honey beam highlight
A_DUST_DARK       = STAGE_RGBA["attic"][6]     # #544b3c: dust layer dark olive-tan
A_DUST_MID        = STAGE_RGBA["attic"][7]     # #80735d: dust layer mid
A_COBWEB_GRAY     = STAGE_RGBA["attic"][8]     # #b5a68d: dusty cobweb gray-linen
A_PARCHMENT       = STAGE_RGBA["attic"][9]     # #e8dec8: parchment letter yellow-ivory
A_ROSE_FADED      = STAGE_RGBA["attic"][10]    # #804a5e: antique faded rose
A_DOLL_ROSE       = STAGE_RGBA["attic"][11]    # #ad6d83: antique doll dress rose
A_BRASS_DARK      = STAGE_RGBA["attic"][12]    # #69592a: tarnished trunk brass dark
A_BRASS_MID       = STAGE_RGBA["attic"][13]    # #a38e42: tarnished brass mid
A_BRASS_HL        = STAGE_RGBA["attic"][14]    # #d9c264: brass latch specular
A_MOON_DUST       = STAGE_RGBA["attic"][15]    # #697894: moonlit window dust blue-gray

BOB_6 = [0, -1, -2, -2, -1, 0]

def save_single(canvas: PixelCanvas, output_path: str):
    canvas.to_image().save(output_path, "PNG")
    print(f"Saved {output_path} ({canvas.width}x{canvas.height}, 1 frame)")


# ==============================================================================
# 1. KITCHEN HAZARDS
# ==============================================================================

def generate_hazard_juice_puddle() -> List[PixelCanvas]:
    """96x16, 6 frames @ 8 fps, loop: true.
    Flat shimmering puddle of orange juice on floor.
    Bottom-anchored at floor lip y=15.
    """
    frames = []
    for f in range(6):
        c = PixelCanvas(96, 16, TRANSPARENT)

        # Baseline puddle profile
        for x in range(8, 88):
            nx = (x - 48) / 39.0
            if abs(nx) > 1.0:
                continue
            base_top = 8 + int(5 * (nx * nx))
            wave = math.sin(x * 0.35 + f * 1.05) * 0.8
            top_y = max(6, min(14, int(base_top + wave)))

            # Floor contact bottom edge at y=15
            for y in range(top_y, 16):
                if y == 15:
                    c.set_pixel(x, y, ORANGE_DEEP)
                elif y == 14:
                    c.set_pixel(x, y, ORANGE_SHADOW)
                elif y == top_y:
                    c.set_pixel(x, y, OUTLINE)
                else:
                    c.set_pixel(x, y, ORANGE_MID)

        # Outline at extreme ends
        for x in (7, 88):
            c.set_pixel(x, 14, OUTLINE)
            c.set_pixel(x, 15, ORANGE_DEEP)

        # Satellite droplets near edges
        droplet_coords = [(4, 14), (5, 14), (5, 15), (4, 15), (90, 14), (91, 14), (91, 15), (90, 15)]
        for dx, dy in droplet_coords:
            c.set_pixel(dx, dy, ORANGE_MID if dy == 14 else ORANGE_DEEP)

        # Shimmer highlights moving across the puddle surface
        for x in range(16, 80):
            nx = (x - 48) / 32.0
            top_y = 8 + int(4 * (nx * nx))
            shimmer_phase = (x * 0.25 - f * 1.2) % (math.pi * 2)
            if math.cos(shimmer_phase) > 0.65:
                hy = top_y + 1
                if 0 <= hy < 15:
                    if math.cos(shimmer_phase) > 0.88:
                        c.set_pixel(x, hy, PURE_WHITE)
                    else:
                        c.set_pixel(x, hy, K_EGG_YELLOW)

            if math.cos(shimmer_phase + 0.5) > 0.7:
                hy2 = top_y + 2
                if 0 <= hy2 < 15:
                    c.set_pixel(x, hy2, ORANGE_LIGHT)

        # Extra glint sparkles on frames
        glint_x = 24 + ((f * 13) % 48)
        c.set_pixel(glint_x, 9, PURE_WHITE)
        c.set_pixel(glint_x - 1, 9, K_FLOUR_PALE)
        c.set_pixel(glint_x + 1, 9, K_FLOUR_PALE)

        frames.append(c)
    return frames


def generate_hazard_marble() -> List[PixelCanvas]:
    """24x24, 8 frames @ 14 fps, loop: true.
    Big glass marble with swirl, rolling leftward along floor.
    Bottom-anchored at floor lip y=23.
    """
    frames = []
    cx, cy = 12, 13
    r = 9

    for f in range(8):
        c = PixelCanvas(24, 24, TRANSPARENT)

        # Floor contact shadow at y=23
        for sx in range(7, 18):
            c.set_pixel(sx, 23, SHADOW_PURPLE_DARK)
        for sx in range(9, 16):
            c.set_pixel(sx, 23, OUTLINE)

        # Marble body
        # Rotation angle for swirl: rolling leftward -> counter-clockwise rotation
        angle = -f * (2 * math.pi / 8.0)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                dx = x - cx
                dy = y - cy
                dist_sq = dx * dx + dy * dy
                if dist_sq > r * r:
                    continue

                # Perimeter outline
                if dist_sq > (r - 1.2) ** 2:
                    c.set_pixel(x, y, OUTLINE)
                    continue

                norm_x = dx / r
                norm_y = dy / r

                # Rotated coordinates for internal swirl
                rx = dx * cos_a - dy * sin_a
                ry = dx * sin_a + dy * cos_a

                # Cat's-eye glass swirl equation (S-spiral)
                swirl_val = ry - 3.5 * math.sin(rx * 0.35)
                is_swirl = abs(swirl_val) < 2.2
                is_swirl_core = abs(swirl_val) < 1.0

                if is_swirl:
                    if is_swirl_core:
                        c.set_pixel(x, y, RED_LIGHT)
                    else:
                        c.set_pixel(x, y, K_JAM_RED if ry < 0 else RED_MID)
                else:
                    # Glass body tones
                    if norm_x < -0.3 and norm_y < -0.3:
                        c.set_pixel(x, y, WHITE_SHADOW)
                    elif norm_x > 0.4 or norm_y > 0.4:
                        c.set_pixel(x, y, BLUE_DEEP)
                    elif norm_x > 0.1 or norm_y > 0.1:
                        c.set_pixel(x, y, BLUE_SHADOW)
                    elif norm_x < 0 and norm_y < 0:
                        c.set_pixel(x, y, BLUE_LIGHT)
                    else:
                        c.set_pixel(x, y, BLUE_MID)

        # Specular glint on upper-left glass rim
        c.set_pixel(cx - 5, cy - 5, PURE_WHITE)
        c.set_pixel(cx - 4, cy - 5, PURE_WHITE)
        c.set_pixel(cx - 5, cy - 4, PURE_WHITE)
        c.set_pixel(cx - 3, cy - 5, WHITE_MID)
        c.set_pixel(cx - 5, cy - 3, WHITE_MID)

        # Subtle secondary bounce reflection at bottom-right inside rim
        c.set_pixel(cx + 4, cy + 4, BLUE_LIGHT)
        c.set_pixel(cx + 5, cy + 3, BLUE_LIGHT)

        frames.append(c)
    return frames


def generate_hazard_stove_burner() -> List[PixelCanvas]:
    """64x48, 10 frames @ 10 fps, loop: true.
    Stove burner on floor:
    - frames 0-2: cold coil (idle)
    - frames 3-4: warming red glow (telegraph)
    - frames 5-9: bright orange/yellow flame jets shooting up (dangerous)
    Bottom-anchored at floor lip y=47.
    """
    frames = []

    for f in range(10):
        c = PixelCanvas(64, 48, TRANSPARENT)

        is_telegraph = (f in (3, 4))
        is_dangerous = (f >= 5)

        # Floor shadow under burner base at y=47
        for x in range(6, 58):
            c.set_pixel(x, 47, OUTLINE)

        # Burner base pan rim (y=44..46)
        for x in range(8, 56):
            c.set_pixel(x, 46, K_CAST_IRON)
            c.set_pixel(x, 45, METAL_SHADOW)
        c.set_pixel(7, 46, OUTLINE)
        c.set_pixel(56, 46, OUTLINE)
        c.set_pixel(7, 45, OUTLINE)
        c.set_pixel(56, 45, OUTLINE)

        # Cast iron burner plate (y=38..44)
        for y in range(38, 45):
            for x in range(10, 54):
                if (x in (10, 53) and y in (38, 44)) or (x in (11, 52) and y == 38):
                    continue
                c.set_pixel(x, y, K_CAST_IRON)

        # Burner outer rim outline
        for x in range(12, 52):
            c.set_pixel(x, 38, OUTLINE)
        c.set_pixel(11, 39, OUTLINE)
        c.set_pixel(52, 39, OUTLINE)
        c.set_pixel(10, 40, OUTLINE)
        c.set_pixel(53, 40, OUTLINE)

        # 5 Gas jet / coil port centers at x=16, 24, 32, 40, 48
        ports_x = [16, 24, 32, 40, 48]

        # Draw coil rings
        for x in range(14, 50):
            dx = abs(x - 32)
            if dx in (4, 5, 12, 13):
                c.set_pixel(x, 41, OUTLINE)
                c.set_pixel(x, 42, METAL_MID)

        # Center cap
        for x in range(30, 35):
            c.set_pixel(x, 40, METAL_MID)
            c.set_pixel(x, 41, OUTLINE)

        # -------------------------------------------------------------
        # STATE 1: COLD COIL (Frames 0-2)
        # -------------------------------------------------------------
        if not is_telegraph and not is_dangerous:
            for px in ports_x:
                c.set_pixel(px, 40, METAL_MID)
                c.set_pixel(px + 1, 40, METAL_SHADOW)
                c.set_pixel(px, 41, OUTLINE)

        # -------------------------------------------------------------
        # STATE 2: WARMING RED GLOW (Frames 3-4, TELEGRAPH)
        # -------------------------------------------------------------
        elif is_telegraph:
            glow_intensity = 0 if f == 3 else 1
            glow_color = RED_SHADOW if glow_intensity == 0 else RED_MID
            hot_color = RED_MID if glow_intensity == 0 else RED_LIGHT

            for x in range(12, 52):
                if c.get_pixel(x, 40) != TRANSPARENT:
                    c.set_pixel(x, 40, glow_color)
                if c.get_pixel(x, 41) != TRANSPARENT:
                    c.set_pixel(x, 41, hot_color)

            for px in ports_x:
                c.set_pixel(px - 1, 40, hot_color)
                c.set_pixel(px, 40, RED_LIGHT if glow_intensity == 1 else RED_MID)
                c.set_pixel(px + 1, 40, hot_color)
                c.set_pixel(px, 39, RED_LIGHT if glow_intensity == 1 else RED_SHADOW)

            spark_offsets = [(-1, -4), (1, -6), (-2, -5), (2, -7), (0, -5)]
            for i, px in enumerate(ports_x):
                sx = px + spark_offsets[i][0] + (1 if f == 4 else 0)
                sy = 38 + spark_offsets[i][1]
                c.set_pixel(sx, sy, RED_LIGHT if f == 4 else RED_MID)
                c.set_pixel(sx, sy - 1, YELLOW_MID if f == 4 else RED_SHADOW)

        # -------------------------------------------------------------
        # STATE 3: BRIGHT ORANGE/YELLOW FLAME JETS (Frames 5-9, DANGEROUS)
        # -------------------------------------------------------------
        elif is_dangerous:
            for x in range(12, 52):
                if c.get_pixel(x, 40) != TRANSPARENT:
                    c.set_pixel(x, 40, RED_MID)
                if c.get_pixel(x, 41) != TRANSPARENT:
                    c.set_pixel(x, 41, ORANGE_MID)
            for px in ports_x:
                c.set_pixel(px, 40, YELLOW_LIGHT)
                c.set_pixel(px, 41, YELLOW_MID)

            jet_heights = [
                [22, 28, 34, 27, 21],
                [25, 31, 38, 30, 24],
                [21, 29, 36, 32, 23],
                [26, 33, 39, 29, 25],
                [23, 30, 35, 31, 22],
            ][f - 5]

            for i, px in enumerate(ports_x):
                jh = jet_heights[i]
                tip_y = 39 - jh
                sway = int(math.sin(f * 1.5 + i * 1.2) * 1.5)

                for y in range(tip_y, 40):
                    progress = (39 - y) / float(jh)
                    half_w = max(0, int((1.0 - progress * 0.85) * 2.8))
                    center_x = px + int(sway * progress)

                    for x in range(center_x - half_w, center_x + half_w + 1):
                        dx = abs(x - center_x)
                        if progress < 0.35 and dx == 0:
                            c.set_pixel(x, y, PURE_WHITE)
                        elif progress < 0.6 and dx <= 1:
                            c.set_pixel(x, y, YELLOW_LIGHT)
                        elif progress < 0.8:
                            c.set_pixel(x, y, YELLOW_MID if dx == 0 else ORANGE_MID)
                        elif progress < 0.95:
                            c.set_pixel(x, y, ORANGE_LIGHT if dx == 0 else RED_LIGHT)
                        else:
                            c.set_pixel(x, y, RED_MID)

                ember_y = tip_y - 2 - ((f * 3 + i * 2) % 6)
                ember_x = px + sway + ((i * 3) % 5) - 2
                if 0 <= ember_y < 48 and 0 <= ember_x < 64:
                    c.set_pixel(ember_x, ember_y, YELLOW_LIGHT)
                    c.set_pixel(ember_x, ember_y + 1, ORANGE_MID)

        frames.append(c)
    return frames


def generate_hazard_spill_trail() -> List[PixelCanvas]:
    """32x16, 4 frames @ 6 fps, loop: true.
    Small drip trail leading into a puddle (decor preview).
    Bottom-anchored at floor lip y=15.
    """
    frames = []
    for f in range(4):
        c = PixelCanvas(32, 16, TRANSPARENT)

        # Floor contact at y=15
        for x in range(2, 30):
            if x in range(3, 7) or x in range(10, 16) or x in range(19, 25) or x in range(27, 30):
                c.set_pixel(x, 15, ORANGE_DEEP)
            elif x in (7, 8, 9, 16, 17, 18, 25, 26):
                c.set_pixel(x, 15, ORANGE_SHADOW)

        # Spot 1: x=3..6, y=13..14
        for x in range(3, 7):
            c.set_pixel(x, 14, ORANGE_MID)
        for x in range(4, 6):
            c.set_pixel(x, 13, ORANGE_LIGHT if f % 2 == 0 else ORANGE_MID)
        c.set_pixel(2, 14, OUTLINE)
        c.set_pixel(7, 14, OUTLINE)

        # Spot 2: x=10..15, y=12..14
        for x in range(10, 16):
            c.set_pixel(x, 14, ORANGE_MID)
        for x in range(11, 15):
            c.set_pixel(x, 13, ORANGE_MID)
        for x in range(12, 14):
            c.set_pixel(x, 12, K_TOAST_GLOW if (f + 1) % 4 < 2 else ORANGE_LIGHT)

        # Spot 3: x=19..24, y=11..14
        for x in range(19, 25):
            c.set_pixel(x, 14, ORANGE_MID)
        for x in range(20, 24):
            c.set_pixel(x, 13, ORANGE_MID)
        for x in range(21, 23):
            c.set_pixel(x, 12, ORANGE_LIGHT)
        c.set_pixel(21, 11, K_EGG_YELLOW if f == 2 else ORANGE_LIGHT)

        # Spot 4: x=27..29, y=13..14
        for x in range(27, 30):
            c.set_pixel(x, 14, ORANGE_MID)
        c.set_pixel(28, 13, ORANGE_LIGHT)

        # Thin seep trail between puddles
        for x in (8, 9, 17, 18, 26):
            c.set_pixel(x, 14, ORANGE_SHADOW)

        # Shimmer highlights shifting along drops
        glint_pos = [(4, 13), (12, 12), (21, 12), (28, 13)][f]
        c.set_pixel(glint_pos[0], glint_pos[1], PURE_WHITE)

        frames.append(c)
    return frames


# ==============================================================================
# 2. BACKYARD HAZARDS
# ==============================================================================

def generate_hazard_sprinkler() -> List[PixelCanvas]:
    """64x96, 10 frames @ 10 fps, loop: true.
    Short stake sprinkler:
    - frames 0-2: idle
    - frames 3-4: wobble telegraph
    - frames 5-9: spraying water streams
    Bottom-anchored at floor lip y=95.
    """
    frames = []

    for f in range(10):
        c = PixelCanvas(64, 96, TRANSPARENT)

        is_telegraph = (f in (3, 4))
        is_spraying = (f >= 5)

        # Ground stake driven into soil/turf at y=95
        for sx in range(26, 39):
            c.set_pixel(sx, 95, Y_SOIL_DARK)
        for sx in range(28, 37):
            c.set_pixel(sx, 94, Y_SOIL_MID)

        # Metal stake spike (y=74..94)
        for y in range(74, 94):
            c.set_pixel(31, y, OUTLINE)
            c.set_pixel(32, y, METAL_MID)
            c.set_pixel(33, y, METAL_SHADOW)
            c.set_pixel(34, y, OUTLINE)

        # Hose fitting collar at y=70..74
        for x in range(28, 37):
            c.set_pixel(x, 70, Y_TERRACOTTA_LIGHT)
            c.set_pixel(x, 71, Y_TERRACOTTA_DARK)
            c.set_pixel(x, 72, BROWN_DARK)
            c.set_pixel(x, 73, OUTLINE)

        # Sprinkler pipe riser (y=52..70)
        for y in range(52, 70):
            c.set_pixel(30, y, OUTLINE)
            c.set_pixel(31, y, Y_GRASS_HL)
            c.set_pixel(32, y, Y_GRASS_MID)
            c.set_pixel(33, y, Y_GRASS_SHADOW)
            c.set_pixel(34, y, OUTLINE)

        # Wobble displacement for telegraph and spraying
        wobble_dx = 0
        if is_telegraph:
            wobble_dx = -2 if f == 3 else 2
        elif is_spraying:
            wobble_dx = [-1, 1, -1, 1, 0][f - 5]

        hx = 32 + wobble_dx

        # Sprinkler head base block (y=46..52)
        for y in range(46, 52):
            for x in range(hx - 5, hx + 6):
                c.set_pixel(x, y, Y_STRING_GOLD if y < 49 else BROWN_MID)
        for x in range(hx - 5, hx + 6):
            c.set_pixel(x, 46, OUTLINE)
            c.set_pixel(x, 52, OUTLINE)
        for y in range(46, 53):
            c.set_pixel(hx - 5, y, OUTLINE)
            c.set_pixel(hx + 5, y, OUTLINE)

        # Nozzle cylinder pointing left (x=hx-12..hx-4, y=41..45)
        for y in range(41, 46):
            for x in range(hx - 12, hx - 4):
                c.set_pixel(x, y, Y_STRING_GOLD)
        for x in range(hx - 12, hx - 4):
            c.set_pixel(x, 41, OUTLINE)
            c.set_pixel(x, 45, OUTLINE)
        for y in range(41, 46):
            c.set_pixel(hx - 12, y, OUTLINE)

        # Nozzle orifice at x=hx-12, y=42..44
        for y in range(42, 45):
            c.set_pixel(hx - 13, y, OUTLINE)
            c.set_pixel(hx - 12, y, VOID_BLACK)

        # Impulse arm (brass clicker rocker on top)
        arm_angle = 0.0
        if is_telegraph:
            arm_angle = 0.4 if f == 3 else -0.3
        elif is_spraying:
            arm_angle = [0.6, -0.5, 0.7, -0.4, 0.5][f - 5]

        arm_end_x = hx + int(math.cos(arm_angle) * 10)
        arm_end_y = 38 + int(math.sin(arm_angle) * 6)
        c.line(hx, 43, arm_end_x, arm_end_y, Y_STRING_GOLD)
        c.line(hx, 42, arm_end_x, arm_end_y - 1, Y_STRING_FILAMENT)
        c.circle(arm_end_x, arm_end_y, 2, Y_STRING_GOLD, outline=OUTLINE)

        # -------------------------------------------------------------
        # TELEGRAPH FX: wobble and small hissing droplets
        # -------------------------------------------------------------
        if is_telegraph:
            d_x = hx - 16 if f == 3 else hx - 19
            c.set_pixel(d_x, 43, Y_WATER_CYAN)
            c.set_pixel(d_x - 1, 43, PURE_WHITE)
            c.set_pixel(d_x, 42, PURE_WHITE)
            c.set_pixel(hx + 8, 44, WHITE_SHADOW)
            c.set_pixel(hx + 9, 44, PURE_WHITE)
            c.set_pixel(hx - 8, 40, WHITE_SHADOW)

        # -------------------------------------------------------------
        # SPRAYING FX: violent water jets shooting from nozzle
        # -------------------------------------------------------------
        elif is_spraying:
            for x in range(hx - 28, hx - 12):
                jy = 43 + int(math.sin((x - hx) * 0.4 + f * 1.5) * 2.5)
                c.set_pixel(x, jy, PURE_WHITE)
                c.set_pixel(x, jy + 1, Y_WATER_CYAN)
                c.set_pixel(x, jy - 1, WHITE_SHADOW)

            spray_drops = [
                (hx - 22, 38), (hx - 25, 47), (hx - 30, 41), (hx - 32, 45), (hx - 20, 36)
            ]
            for sx, sy in spray_drops:
                if 0 <= sx < 64 and 0 <= sy < 96:
                    c.set_pixel(sx, sy, PURE_WHITE)
                    c.set_pixel(sx - 1, sy, Y_WATER_CYAN)

        frames.append(c)
    return frames


def generate_hazard_water_spray() -> List[PixelCanvas]:
    """192x96, 8 frames @ 14 fps, loop: true.
    Arcs of spraying water (white-blue, hard-banded alpha),
    anchored to left of sprinkler head (right side at x=185, y=44).
    Hard-banded discrete alpha bands: 255, 180, 100, 40.
    """
    frames = []
    x0, y0 = 185, 44

    for f in range(8):
        c = PixelCanvas(192, 96, TRANSPARENT)

        for stream_idx in range(3):
            apex_y = 12 + stream_idx * 8 + int(math.sin(f * 1.2 + stream_idx * 1.5) * 4)
            land_x = 12 + stream_idx * 30 + int(math.cos(f * 1.1 + stream_idx) * 8)

            for x in range(land_x, x0 + 1):
                t = (x0 - x) / float(x0 - land_x)
                y_center = (y0 * (1.0 - t) + 88 * t) - (4.0 * (y0 - apex_y) * t * (1.0 - t))
                yc = int(round(y_center))

                stream_w = 1 + int(t * 3.5)

                for dy in range(-stream_w, stream_w + 1):
                    py = yc + dy
                    if not (0 <= py < 96 and 0 <= x < 192):
                        continue

                    dist = abs(dy) / float(stream_w)
                    if dist < 0.35 and t < 0.7:
                        c.set_pixel(x, py, (245, 248, 252, 255))
                    elif dist < 0.6:
                        c.set_pixel(x, py, (143, 237, 247, 180))
                    elif dist < 0.85:
                        c.set_pixel(x, py, (130, 203, 250, 100))
                    else:
                        c.set_pixel(x, py, (194, 210, 227, 40))

            num_droplets = 12
            for di in range(num_droplets):
                dt = (di / float(num_droplets) + f * 0.125) % 1.0
                dx = int(x0 - dt * (x0 - land_x))
                base_y = (y0 * (1.0 - dt) + 88 * dt) - (4.0 * (y0 - apex_y) * dt * (1.0 - dt))
                dy_scatter = int(math.sin(di * 2.7 + f * 1.4) * (3 + dt * 8))
                drop_y = int(base_y + dy_scatter)

                if 0 <= dx < 192 and 0 <= drop_y < 96:
                    c.set_pixel(dx, drop_y, (245, 248, 252, 255))
                    if 0 <= dx - 1 < 192:
                        c.set_pixel(dx - 1, drop_y, (143, 237, 247, 180))

        frames.append(c)
    return frames


def generate_hazard_mud() -> List[PixelCanvas]:
    """96x16, 6 frames @ 6 fps, loop: true.
    Pool of thick brown mud with popping bubbles.
    Bottom-anchored at floor lip y=15.
    """
    frames = []

    for f in range(6):
        c = PixelCanvas(96, 16, TRANSPARENT)

        for x in range(6, 90):
            nx = (x - 48) / 41.0
            if abs(nx) > 1.0:
                continue
            base_top = 7 + int(6 * (nx * nx))
            top_y = max(6, min(14, base_top))

            for y in range(top_y, 16):
                if y == 15:
                    c.set_pixel(x, y, Y_SOIL_DARK)
                elif y == 14:
                    c.set_pixel(x, y, BROWN_DARKEST)
                elif y == top_y:
                    c.set_pixel(x, y, OUTLINE)
                elif y == top_y + 1:
                    c.set_pixel(x, y, BROWN_MID)
                else:
                    c.set_pixel(x, y, Y_SOIL_MID)

        for sx, sy in [(3, 14), (4, 14), (4, 15), (3, 15), (91, 14), (92, 14), (91, 15), (92, 15)]:
            c.set_pixel(sx, sy, BROWN_MID if sy == 14 else Y_SOIL_DARK)

        for x in range(16, 80, 4):
            c.set_pixel(x, 10, BROWN_LIGHT)
            c.set_pixel(x + 1, 10, WOOD_HIGHLIGHT)

        # Bubble A at x=28, y=7
        bx_a = 28
        if f == 0:
            c.circle(bx_a, 9, 2, BROWN_MID, outline=OUTLINE)
            c.set_pixel(bx_a - 1, 8, BROWN_LIGHT)
        elif f == 1:
            c.circle(bx_a, 8, 3, BROWN_MID, outline=OUTLINE)
            c.set_pixel(bx_a - 1, 7, WOOD_HIGHLIGHT)
            c.set_pixel(bx_a, 7, PURE_WHITE)
        elif f == 2:
            c.circle(bx_a, 7, 4, BROWN_MID, outline=OUTLINE)
            c.set_pixel(bx_a - 1, 5, PURE_WHITE)
            c.set_pixel(bx_a, 5, WOOD_HIGHLIGHT)
        elif f == 3:
            c.circle(bx_a, 7, 4, BROWN_LIGHT, outline=OUTLINE)
            c.set_pixel(bx_a - 1, 5, PURE_WHITE)
            c.set_pixel(bx_a + 2, 7, BROWN_DARK)
        elif f == 4:
            c.circle(bx_a, 9, 3, Y_SOIL_DARK, outline=OUTLINE)
            c.set_pixel(bx_a - 4, 4, BROWN_MID)
            c.set_pixel(bx_a + 4, 3, BROWN_MID)
            c.set_pixel(bx_a, 2, BROWN_LIGHT)
        elif f == 5:
            c.circle(bx_a, 9, 2, BROWN_DARKEST, outline=BROWN_MID)

        # Bubble B at x=64, y=8
        bx_b = 64
        f_b = (f + 3) % 6
        if f_b == 0:
            c.circle(bx_b, 9, 2, BROWN_MID, outline=OUTLINE)
            c.set_pixel(bx_b - 1, 8, BROWN_LIGHT)
        elif f_b == 1:
            c.circle(bx_b, 8, 3, BROWN_MID, outline=OUTLINE)
            c.set_pixel(bx_b - 1, 7, WOOD_HIGHLIGHT)
            c.set_pixel(bx_b, 7, PURE_WHITE)
        elif f_b == 2:
            c.circle(bx_b, 7, 4, BROWN_MID, outline=OUTLINE)
            c.set_pixel(bx_b - 1, 5, PURE_WHITE)
            c.set_pixel(bx_b, 5, WOOD_HIGHLIGHT)
        elif f_b == 3:
            c.circle(bx_b, 7, 4, BROWN_LIGHT, outline=OUTLINE)
            c.set_pixel(bx_b - 1, 5, PURE_WHITE)
        elif f_b == 4:
            c.circle(bx_b, 9, 3, Y_SOIL_DARK, outline=OUTLINE)
            c.set_pixel(bx_b - 3, 3, BROWN_MID)
            c.set_pixel(bx_b + 3, 4, BROWN_MID)
            c.set_pixel(bx_b - 1, 2, BROWN_LIGHT)
        elif f_b == 5:
            c.circle(bx_b, 9, 2, BROWN_DARKEST, outline=BROWN_MID)

        frames.append(c)
    return frames


def generate_hazard_wind_gust() -> List[PixelCanvas]:
    """192x64, 8 frames @ 14 fps, loop: true.
    Swirl of white wind lines and leaves crossing screen.
    Frames 0-1 subtle breeze telegraph.
    """
    frames = []

    for f in range(8):
        c = PixelCanvas(192, 64, TRANSPARENT)

        is_telegraph = (f in (0, 1))

        if is_telegraph:
            wisps = [
                (110 + f * 12, 24, 45),
                (140 + f * 10, 42, 38),
            ]
            for wx, wy, wlen in wisps:
                for lx in range(wlen):
                    px = wx + lx
                    if not (0 <= px < 192):
                        continue
                    py = wy + int(math.sin(lx * 0.15) * 3)
                    c.set_pixel(px, py, WHITE_SHADOW if lx < 8 or lx > wlen - 8 else PURE_WHITE)

            lx, ly = 135 + f * 10, 32 + f * 3
            c.set_pixel(lx, ly, Y_GRASS_HL)
            c.set_pixel(lx + 1, ly, Y_GRASS_MID)
            c.set_pixel(lx, ly + 1, OUTLINE)

        else:
            stream_offsets = [
                (12, 1.2), (28, 1.6), (42, 1.4), (54, 1.8)
            ]
            for base_y, speed in stream_offsets:
                for x in range(0, 192, 2):
                    phase = (x * 0.08 - f * speed) % (math.pi * 2)
                    y = int(base_y + math.sin(phase) * 6)

                    if 40 < x < 70 and base_y == 28:
                        y -= int(math.sin((x - 40) * 0.2) * 8)
                    elif 120 < x < 155 and base_y == 42:
                        y += int(math.sin((x - 120) * 0.18) * 8)

                    if 0 <= y < 64:
                        if math.sin(phase) > 0.4:
                            c.set_pixel(x, y, PURE_WHITE)
                            c.set_pixel(x + 1, y, WHITE_SHADOW)
                        else:
                            c.set_pixel(x, y, WHITE_SHADOW)

            for y_line in (16, 26, 36, 48):
                lx_start = ((f * 42 + y_line * 11) % 150)
                for x in range(lx_start, lx_start + 32):
                    if 0 <= x < 192:
                        c.set_pixel(x, y_line, PURE_WHITE if (x - lx_start) % 4 != 0 else WHITE_SHADOW)

            leaf_data = [
                (Y_GRASS_HL, Y_GRASS_MID, 20, 20, 24, 2),
                (RED_LIGHT, RED_MID, 60, 38, 26, -3),
                (ORANGE_LIGHT, ORANGE_MID, 110, 18, 28, 3),
                (Y_GRASS_MID, Y_GRASS_SHADOW, 150, 46, 22, -2),
            ]
            for col_hl, col_mid, sx, sy, vx, vy in leaf_data:
                leaf_x = (sx + f * vx) % 184
                leaf_y = int(sy + math.sin(f * 1.5 + sx) * 6)
                if 0 <= leaf_x < 190 and 0 <= leaf_y < 62:
                    flip = (f + sx) % 4
                    if flip == 0:
                        c.set_pixel(leaf_x, leaf_y, col_hl)
                        c.set_pixel(leaf_x + 1, leaf_y, col_mid)
                        c.set_pixel(leaf_x, leaf_y + 1, col_mid)
                        c.set_pixel(leaf_x + 1, leaf_y + 1, OUTLINE)
                    elif flip == 1:
                        c.set_pixel(leaf_x, leaf_y, col_hl)
                        c.set_pixel(leaf_x + 1, leaf_y, col_mid)
                        c.set_pixel(leaf_x + 2, leaf_y, OUTLINE)
                    elif flip == 2:
                        c.set_pixel(leaf_x, leaf_y, col_mid)
                        c.set_pixel(leaf_x, leaf_y + 1, col_hl)
                        c.set_pixel(leaf_x, leaf_y + 2, OUTLINE)
                    else:
                        c.set_pixel(leaf_x + 1, leaf_y, col_hl)
                        c.set_pixel(leaf_x, leaf_y + 1, col_mid)
                        c.set_pixel(leaf_x + 1, leaf_y + 1, OUTLINE)

        frames.append(c)
    return frames


def generate_fx_leaf() -> List[PixelCanvas]:
    """16x16, 8 frames @ 12 fps, loop: true.
    Tumbling green/brown leaf.
    """
    frames = []

    for f in range(8):
        c = PixelCanvas(16, 16, TRANSPARENT)

        if f == 0:
            pts = [(5, 4), (10, 4), (12, 7), (11, 10), (7, 12), (4, 9)]
            c.polygon(pts, GREEN_MID, outline=OUTLINE)
            c.line(5, 5, 10, 10, GREEN_LIGHT)
            c.set_pixel(4, 3, BROWN_MID)
        elif f == 1:
            pts = [(6, 5), (10, 5), (11, 8), (9, 11), (6, 9)]
            c.polygon(pts, GREEN_MID, outline=OUTLINE)
            c.line(6, 6, 9, 9, GREEN_LIGHT)
            c.set_pixel(5, 4, BROWN_MID)
        elif f == 2:
            c.line(7, 4, 9, 12, OUTLINE)
            c.line(8, 5, 8, 11, GREEN_LIGHT)
            c.set_pixel(6, 3, BROWN_MID)
        elif f == 3:
            pts = [(6, 6), (9, 4), (11, 7), (9, 11), (7, 10)]
            c.polygon(pts, GREEN_RICH, outline=OUTLINE)
            c.line(7, 6, 9, 9, GREEN_SHADOW)
            c.set_pixel(5, 6, BROWN_DARK)
        elif f == 4:
            pts = [(5, 5), (9, 3), (12, 6), (11, 11), (7, 12), (4, 8)]
            c.polygon(pts, GREEN_DEEP, outline=OUTLINE)
            c.line(6, 6, 10, 10, GREEN_RICH)
            c.set_pixel(4, 4, BROWN_DARK)
        elif f == 5:
            pts = [(6, 6), (9, 4), (11, 7), (8, 10), (6, 9)]
            c.polygon(pts, GREEN_RICH, outline=OUTLINE)
            c.line(7, 6, 9, 8, GREEN_SHADOW)
            c.set_pixel(5, 6, BROWN_MID)
        elif f == 6:
            c.line(9, 4, 7, 12, OUTLINE)
            c.line(8, 5, 8, 11, GREEN_MID)
            c.set_pixel(9, 3, BROWN_MID)
        elif f == 7:
            pts = [(5, 5), (9, 4), (12, 7), (10, 11), (6, 11), (4, 8)]
            c.polygon(pts, GREEN_MID, outline=OUTLINE)
            c.line(6, 6, 9, 9, GREEN_LIGHT)
            c.set_pixel(4, 4, BROWN_MID)

        frames.append(c)
    return frames


def generate_fx_leaf_b() -> List[PixelCanvas]:
    """16x16, 8 frames @ 12 fps, loop: true.
    Tumbling orange/red leaf variant.
    """
    frames = []

    for f in range(8):
        c = PixelCanvas(16, 16, TRANSPARENT)

        if f == 0:
            pts = [(4, 5), (9, 3), (12, 6), (11, 11), (7, 12), (4, 9)]
            c.polygon(pts, RED_MID, outline=OUTLINE)
            c.line(5, 5, 10, 10, RED_LIGHT)
            c.set_pixel(3, 4, RED_SHADOW)
        elif f == 1:
            pts = [(5, 6), (10, 4), (11, 8), (9, 11), (6, 10)]
            c.polygon(pts, ORANGE_MID, outline=OUTLINE)
            c.line(6, 6, 9, 9, ORANGE_LIGHT)
            c.set_pixel(4, 5, RED_SHADOW)
        elif f == 2:
            c.line(8, 4, 8, 12, OUTLINE)
            c.line(8, 5, 8, 11, RED_LIGHT)
            c.set_pixel(7, 3, RED_SHADOW)
        elif f == 3:
            pts = [(6, 5), (10, 5), (11, 8), (8, 11), (6, 9)]
            c.polygon(pts, RED_SHADOW, outline=OUTLINE)
            c.line(7, 6, 9, 9, RED_DEEP)
            c.set_pixel(5, 4, WOOD_BLACK)
        elif f == 4:
            pts = [(5, 4), (10, 3), (12, 7), (10, 11), (6, 12), (4, 8)]
            c.polygon(pts, RED_SHADOW, outline=OUTLINE)
            c.line(6, 5, 10, 9, RED_MID)
            c.set_pixel(4, 3, WOOD_BLACK)
        elif f == 5:
            pts = [(6, 6), (9, 4), (11, 7), (9, 11), (6, 9)]
            c.polygon(pts, RED_MID, outline=OUTLINE)
            c.line(7, 6, 9, 8, RED_LIGHT)
            c.set_pixel(5, 5, RED_SHADOW)
        elif f == 6:
            c.line(7, 4, 9, 12, OUTLINE)
            c.line(8, 5, 8, 11, ORANGE_LIGHT)
            c.set_pixel(6, 3, RED_SHADOW)
        elif f == 7:
            pts = [(5, 5), (9, 4), (12, 7), (11, 10), (7, 12), (4, 8)]
            c.polygon(pts, ORANGE_MID, outline=OUTLINE)
            c.line(6, 6, 10, 9, ORANGE_LIGHT)
            c.set_pixel(4, 4, RED_SHADOW)

        frames.append(c)
    return frames


# ==============================================================================
# 3. BASEMENT HAZARDS
# ==============================================================================

def generate_hazard_paint_can() -> List[PixelCanvas]:
    """40x40, 8 frames @ 12 fps, loop: true.
    Rolling paint can with drip of bright paint trailing, rolling leftward.
    Bottom-anchored at floor lip y=39.
    """
    frames = []

    for f in range(8):
        c = PixelCanvas(40, 40, TRANSPARENT)

        # Floor contact shadow at y=39
        for sx in range(8, 36):
            c.set_pixel(sx, 39, B_CONCRETE_SHADOW)
        for sx in range(12, 32):
            c.set_pixel(sx, 39, OUTLINE)

        angle = -f * (2 * math.pi / 8.0)

        for y in range(17, 39):
            for x in range(14, 33):
                ny = (y - 28) / 11.0
                if ny < -0.7:
                    c.set_pixel(x, y, WHITE_SHADOW)
                elif ny < 0:
                    c.set_pixel(x, y, METAL_MID)
                elif ny < 0.7:
                    c.set_pixel(x, y, METAL_SHADOW)
                else:
                    c.set_pixel(x, y, B_CONCRETE_DARK)

        for y in range(17, 39):
            cyl_y = (y - 28) / 11.0
            if abs(cyl_y) <= 1.0:
                theta = math.asin(cyl_y) + angle
                if math.sin(theta * 2.0) > 0.4:
                    for x in range(16, 31):
                        c.set_pixel(x, y, B_EMBER_ORANGE)

        for x in range(14, 33):
            c.set_pixel(x, 16, OUTLINE)
            c.set_pixel(x, 38, OUTLINE)
        for y in range(17, 39):
            c.set_pixel(32, y, METAL_SHADOW)
            c.set_pixel(33, y, OUTLINE)

        cx_rim, cy_rim = 14, 28
        rx, ry = 5, 11
        for y in range(cy_rim - ry, cy_rim + ry + 1):
            for x in range(cx_rim - rx, cx_rim + rx + 1):
                dx = (x - cx_rim) / float(rx)
                dy = (y - cy_rim) / float(ry)
                dist_sq = dx * dx + dy * dy
                if dist_sq <= 1.0:
                    if dist_sq > 0.7:
                        c.set_pixel(x, y, OUTLINE if dx < 0 else METAL_MID)
                    else:
                        c.set_pixel(x, y, TEAL_LIGHT if dy < 0 else TEAL_MID)

        c.set_pixel(cx_rim - 4, cy_rim + 6, TEAL_HIGHLIGHT)
        c.set_pixel(cx_rim - 3, cy_rim + 7, TEAL_LIGHT)
        c.set_pixel(cx_rim - 2, cy_rim + 8, TEAL_MID)

        drip_phase = (f * 3) % 8
        drip_x = 30 + drip_phase
        if drip_x < 39:
            c.set_pixel(drip_x, 38, TEAL_LIGHT)
            c.set_pixel(drip_x + 1, 38, TEAL_HIGHLIGHT)
            c.set_pixel(drip_x, 39, TEAL_SHADOW)

        splat_x = 24 + ((f * 5) % 12)
        c.set_pixel(splat_x, 37, TEAL_HIGHLIGHT)
        c.set_pixel(splat_x, 38, TEAL_LIGHT)

        frames.append(c)
    return frames


def generate_hazard_drip() -> List[PixelCanvas]:
    """16x48, 10 frames @ 12 fps, loop: true.
    Droplet forming on ceiling (frames 0-3 telegraph),
    falling (4-6), and splashing on floor (7-9).
    """
    frames = []

    for f in range(10):
        c = PixelCanvas(16, 48, TRANSPARENT)

        for y in range(0, 3):
            for x in range(4, 13):
                c.set_pixel(x, y, B_RUST_MID if y == 1 else B_DRAIN_GRATE)
        c.line(4, 3, 12, 3, OUTLINE)

        if f == 0:
            c.set_pixel(8, 4, B_WATER_PUDDLE)
            c.set_pixel(9, 4, PURE_WHITE)
        elif f == 1:
            c.set_pixel(8, 4, B_WATER_PUDDLE)
            c.set_pixel(9, 4, B_RIPPLE_HL)
            c.set_pixel(8, 5, BLUE_LIGHT)
            c.set_pixel(9, 5, PURE_WHITE)
            c.set_pixel(8, 6, OUTLINE)
        elif f == 2:
            c.circle(8, 6, 2, BLUE_LIGHT, outline=OUTLINE)
            c.set_pixel(8, 5, PURE_WHITE)
            c.set_pixel(9, 6, B_WATER_PUDDLE)
        elif f == 3:
            c.line(8, 4, 8, 6, BLUE_LIGHT)
            c.circle(8, 8, 2, BLUE_LIGHT, outline=OUTLINE)
            c.set_pixel(8, 7, PURE_WHITE)
            c.set_pixel(8, 10, OUTLINE)
        elif f == 4:
            c.line(8, 15, 8, 19, BLUE_LIGHT)
            c.set_pixel(8, 16, PURE_WHITE)
            c.set_pixel(8, 14, OUTLINE)
            c.set_pixel(8, 20, OUTLINE)
        elif f == 5:
            c.line(8, 26, 8, 32, BLUE_LIGHT)
            c.set_pixel(8, 27, PURE_WHITE)
            c.set_pixel(8, 28, PURE_WHITE)
            c.set_pixel(8, 25, OUTLINE)
            c.set_pixel(8, 33, OUTLINE)
        elif f == 6:
            c.line(8, 37, 8, 44, BLUE_LIGHT)
            c.set_pixel(8, 39, PURE_WHITE)
            c.set_pixel(8, 40, PURE_WHITE)
            c.set_pixel(8, 36, OUTLINE)
            c.set_pixel(8, 45, OUTLINE)
        elif f == 7:
            for x in range(4, 13):
                c.set_pixel(x, 47, B_WATER_PUDDLE)
            for x in range(5, 12):
                c.set_pixel(x, 46, BLUE_LIGHT)
            c.set_pixel(8, 46, PURE_WHITE)
            c.set_pixel(4, 46, OUTLINE)
            c.set_pixel(12, 46, OUTLINE)
        elif f == 8:
            for x in range(3, 14):
                c.set_pixel(x, 47, B_WATER_PUDDLE)
            c.line(4, 45, 12, 45, B_RIPPLE_HL)
            c.set_pixel(4, 43, BLUE_LIGHT)
            c.set_pixel(4, 42, PURE_WHITE)
            c.set_pixel(12, 43, BLUE_LIGHT)
            c.set_pixel(12, 42, PURE_WHITE)
            c.set_pixel(8, 44, PURE_WHITE)
            c.set_pixel(2, 40, PURE_WHITE)
            c.set_pixel(14, 41, PURE_WHITE)
        elif f == 9:
            for x in range(2, 15):
                c.set_pixel(x, 47, B_WATER_PUDDLE)
            for x in range(4, 13):
                c.set_pixel(x, 46, B_RIPPLE_HL)
            c.set_pixel(8, 46, PURE_WHITE)

        frames.append(c)
    return frames


def generate_hazard_mousetrap() -> List[PixelCanvas]:
    """48x24, 8 frames @ 14 fps, loop: false.
    Wooden mouse trap on floor:
    - frames 0-2: set with cheese & glint (telegraph)
    - frames 3-4: snapping shut
    - frames 5-7: sprung
    Bottom-anchored at floor lip y=23.
    """
    frames = []

    for f in range(8):
        c = PixelCanvas(48, 24, TRANSPARENT)

        # Wooden pine board base: x=4..43, y=17..23
        for y in range(17, 24):
            for x in range(4, 44):
                if y == 23:
                    c.set_pixel(x, y, OUTLINE)
                elif y == 22:
                    c.set_pixel(x, y, BROWN_DARK)
                elif y == 17:
                    c.set_pixel(x, y, WOOD_LIT)
                else:
                    c.set_pixel(x, y, WOOD_HIGHLIGHT if x % 7 == 0 else BROWN_MID)
        c.line(4, 17, 4, 23, OUTLINE)
        c.line(43, 17, 43, 23, OUTLINE)

        # Spring coil in center: x=22..26, y=15..18
        for x in range(22, 27):
            c.set_pixel(x, 16, METAL_MID)
            c.set_pixel(x, 17, METAL_SHADOW)
        c.set_pixel(24, 15, OUTLINE)

        if f <= 2:
            for x in range(24, 41):
                c.set_pixel(x, 16, METAL_SHADOW)
                c.set_pixel(x, 15, METAL_MID)
            c.set_pixel(41, 16, OUTLINE)
            c.set_pixel(41, 17, OUTLINE)

            c.line(24, 15, 18, 15, OUTLINE)

            pts_cheese = [(11, 17), (18, 17), (18, 12)]
            c.polygon(pts_cheese, YELLOW_MID, outline=OUTLINE)
            c.set_pixel(14, 15, YELLOW_LIGHT)
            c.set_pixel(16, 14, YELLOW_LIGHT)
            c.set_pixel(15, 16, YELLOW_SHADOW)

            glint_x, glint_y = 17, 12
            if f == 1:
                c.set_pixel(glint_x, glint_y, PURE_WHITE)
                c.set_pixel(glint_x - 1, glint_y, WHITE_SHADOW)
                c.set_pixel(glint_x + 1, glint_y, WHITE_SHADOW)
                c.set_pixel(glint_x, glint_y - 1, WHITE_SHADOW)
                c.set_pixel(glint_x, glint_y + 1, WHITE_SHADOW)
            elif f == 2:
                c.set_pixel(glint_x, glint_y, PURE_WHITE)

        elif f == 3:
            for y in range(4, 16):
                c.set_pixel(23, y, METAL_MID)
                c.set_pixel(24, y, METAL_SHADOW)
                c.set_pixel(25, y, OUTLINE)
            c.line(26, 7, 34, 12, WHITE_SHADOW)
            c.line(27, 9, 36, 14, WHITE_MID)

            c.polygon([(10, 15), (15, 15), (14, 12)], YELLOW_MID, outline=OUTLINE)
            c.set_pixel(12, 9, YELLOW_LIGHT)
            c.set_pixel(16, 8, YELLOW_MID)

        elif f == 4:
            for x in range(6, 24):
                c.set_pixel(x, 16, METAL_SHADOW)
                c.set_pixel(x, 15, METAL_MID)
            c.set_pixel(6, 16, OUTLINE)
            c.set_pixel(6, 17, OUTLINE)

            spark_pts = [(5, 14), (4, 12), (7, 13), (6, 11), (9, 13)]
            for sx, sy in spark_pts:
                c.set_pixel(sx, sy, PURE_WHITE)
                c.set_pixel(sx, sy + 1, YELLOW_LIGHT)

            c.set_pixel(11, 16, YELLOW_MID)
            c.set_pixel(12, 16, YELLOW_LIGHT)
            c.set_pixel(13, 16, YELLOW_SHADOW)

        else:
            shudder = (1 if f == 5 else 0)
            for x in range(6, 24):
                c.set_pixel(x, 16 - shudder, METAL_SHADOW)
                c.set_pixel(x, 15 - shudder, METAL_MID)
            c.set_pixel(6, 16 - shudder, OUTLINE)
            c.set_pixel(6, 17 - shudder, OUTLINE)

            crumbs = [(10, 16), (14, 16), (8, 16), (17, 16)]
            for cx_crumb, cy_crumb in crumbs:
                c.set_pixel(cx_crumb, cy_crumb, YELLOW_MID)

        frames.append(c)
    return frames


def generate_light_flashlight_cone() -> PixelCanvas:
    """256x128, 1 frame @ 0 fps.
    Hard-banded warm light cone pointing right (4 discrete alpha bands: 200, 120, 60, 20).
    Color: warm light (253, 240, 126).
    """
    c = PixelCanvas(256, 128, TRANSPARENT)
    y0 = 64.0
    r_val, g_val, b_val = 253, 240, 126

    for x in range(256):
        half_h = 8.0 + (x / 255.0) * 54.0

        for y in range(128):
            dy = abs(y - y0)
            if dy > half_h:
                continue

            rel_d = dy / half_h
            if rel_d <= 0.35 and x > 2:
                alpha = 200
            elif rel_d <= 0.65:
                alpha = 120
            elif rel_d <= 0.88:
                alpha = 60
            else:
                alpha = 20

            c.set_pixel(x, y, (r_val, g_val, b_val, alpha))

    return c


def generate_light_dark_mask() -> PixelCanvas:
    """512x512, 1 frame @ 0 fps.
    Hard-banded radial gradient: transparent middle, dark edges in 6 bands
    (alphas: 0, 40, 90, 150, 210, 255).
    Color: VOID_BLACK (10, 7, 16).
    """
    c = PixelCanvas(512, 512, TRANSPARENT)
    cx, cy = 256.0, 256.0
    r_val, g_val, b_val = 10, 7, 16

    for y in range(512):
        for x in range(512):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < 65:
                alpha = 0
            elif dist < 115:
                alpha = 40
            elif dist < 175:
                alpha = 90
            elif dist < 235:
                alpha = 150
            elif dist < 295:
                alpha = 210
            else:
                alpha = 255

            if alpha > 0:
                c.set_pixel(x, y, (r_val, g_val, b_val, alpha))

    return c


def generate_item_flashlight() -> List[PixelCanvas]:
    """48x48, 6 frames @ 8 fps, loop: true.
    Dropped yellow chunky flashlight with beam glint.
    """
    frames = []

    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        by = BOB_6[f]
        cx, cy = 24, 24 + by

        for y in range(cy - 2, cy + 9):
            for x in range(14, 29):
                c.set_pixel(x, y, YELLOW_MID)
        for rx in (18, 23):
            for y in range(cy - 2, cy + 9):
                c.set_pixel(rx, y, WOOD_BLACK)

        for x in range(14, 29):
            c.set_pixel(x, cy - 2, YELLOW_LIGHT)
            c.set_pixel(x, cy + 8, YELLOW_DEEP)

        for y in range(cy - 5, cy - 2):
            for x in range(19, 23):
                c.set_pixel(x, y, RED_MID)
        c.set_pixel(20, cy - 5, RED_LIGHT)
        c.set_pixel(21, cy - 5, RED_LIGHT)

        for y in range(cy - 6, cy + 13):
            half_w = 4 + int(abs(y - (cy + 3)) * 0.4)
            for x in range(29, 29 + half_w):
                if x == 29:
                    c.set_pixel(x, y, METAL_SHADOW)
                elif x == 29 + half_w - 1:
                    c.set_pixel(x, y, BLUE_LIGHT)
                else:
                    c.set_pixel(x, y, METAL_MID)

        for y in range(cy - 5, cy + 12):
            c.set_pixel(36, y, PURE_WHITE if y < cy + 3 else BLUE_LIGHT)

        c.apply_selective_outline(OUTLINE, light_rim=YELLOW_LIGHT, dark_rim=WOOD_BLACK)

        glint_phase = f % 6
        glint_y = cy - 4 + glint_phase * 2
        gx = 37
        if 0 <= glint_y < 48:
            c.set_pixel(gx, glint_y, PURE_WHITE)
            c.set_pixel(gx - 1, glint_y, WHITE_MID)
            c.set_pixel(gx + 1, glint_y, WHITE_MID)
            c.set_pixel(gx, glint_y - 1, WHITE_MID)
            c.set_pixel(gx, glint_y + 1, WHITE_MID)

        frames.append(c)
    return frames


def generate_item_flashlight_pop() -> List[PixelCanvas]:
    """48x48, 3 frames @ 24 fps, loop: false.
    Battery/spark pop pickup effect.
    """
    frames = []

    for f in range(3):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cx, cy = 24, 24

        if f == 0:
            c.circle(cx, cy, 5, YELLOW_LIGHT, outline=PURE_WHITE)
            c.rect(cx - 2, cy - 14, 4, 8, METAL_MID, outline=OUTLINE)
            c.rect(cx - 1, cy - 16, 2, 2, METAL_MID, outline=OUTLINE)
            c.line(cx - 2, cy - 11, cx + 1, cy - 11, RED_MID)
        elif f == 1:
            c.circle(cx, cy, 3, PURE_WHITE)
            spark_dists = [10, 14, 18, 14, 10, 14, 18, 14]
            for i, d in enumerate(spark_dists):
                ang = i * (math.pi / 4.0)
                sx = int(cx + math.cos(ang) * d)
                sy = int(cy + math.sin(ang) * d)
                c.set_pixel(sx, sy, PURE_WHITE)
                c.set_pixel(sx + 1, sy, YELLOW_LIGHT)
            c.rect(cx + 6, cy - 16, 8, 4, METAL_MID, outline=OUTLINE)
        elif f == 2:
            for i in range(8):
                ang = i * (math.pi / 4.0) + 0.2
                d = 20
                sx = int(cx + math.cos(ang) * d)
                sy = int(cy + math.sin(ang) * d)
                if 0 <= sx < 48 and 0 <= sy < 48:
                    c.set_pixel(sx, sy, YELLOW_LIGHT)

        frames.append(c)
    return frames


# ==============================================================================
# 4. ATTIC HAZARDS
# ==============================================================================

def generate_hazard_cobweb() -> List[PixelCanvas]:
    """96x64, 6 frames @ 6 fps, loop: true.
    Dense trembling cobweb hung across path at jump height.
    """
    frames = []
    cx, cy = 52, 24

    spoke_ends = [
        (4, 6), (28, 4), (64, 4), (91, 8), (91, 36),
        (84, 56), (56, 58), (24, 54), (6, 42), (4, 22)
    ]

    for f in range(6):
        c = PixelCanvas(96, 64, TRANSPARENT)

        shiver_dx = int(math.sin(f * 1.05) * 1.5)
        shiver_dy = int(math.cos(f * 1.05) * 1.2)
        cur_cx = cx + shiver_dx
        cur_cy = cy + shiver_dy

        for sx, sy in spoke_ends:
            c.line(cur_cx, cur_cy, sx, sy, A_COBWEB_GRAY)

        for ring_idx in range(1, 7):
            t = ring_idx / 7.0
            ring_pts = []
            for i, (sx, sy) in enumerate(spoke_ends):
                pt_x = int(cur_cx + (sx - cur_cx) * t)
                pt_y = int(cur_cy + (sy - cur_cy) * t)
                sag = int(math.sin(i * 1.5 + f * 1.05) * 1.2)
                ring_pts.append((pt_x, pt_y + sag))

            for i in range(len(ring_pts)):
                p1 = ring_pts[i]
                p2 = ring_pts[(i + 1) % len(ring_pts)]
                c.line(p1[0], p1[1], p2[0], p2[1], A_COBWEB_GRAY)

        clump_coords = [
            (cur_cx - 8, cur_cy + 4), (cur_cx + 12, cur_cy - 6),
            (cur_cx - 18, cur_cy + 14), (cur_cx + 22, cur_cy + 16),
            (cur_cx + 4, cur_cy + 22)
        ]
        for clx, cly in clump_coords:
            c.set_pixel(clx, cly, DUSK_CREAM)
            c.set_pixel(clx + 1, cly, A_DUST_MID)
            c.set_pixel(clx, cly + 1, A_COBWEB_GRAY)

        c.set_pixel(cur_cx, cur_cy, WHITE_SHADOW)
        c.set_pixel(cur_cx + 1, cur_cy, PURE_WHITE)

        frames.append(c)
    return frames


def generate_hazard_loose_board() -> List[PixelCanvas]:
    """64x24, 8 frames @ 10 fps, loop: false.
    Floorboard that creaks (frames 0-2), tilts (3-4),
    and drops away into darkness (5-7).
    Bottom-anchored / flush with floor lip at y=23.
    """
    frames = []

    for f in range(8):
        c = PixelCanvas(64, 24, TRANSPARENT)

        # Permanent floor joists / ledge on left (x=0..5) and right (x=58..63)
        for y in range(16, 24):
            for x in range(0, 6):
                c.set_pixel(x, y, A_TIMBER_DARK if y > 18 else A_FLOORBOARD_MID)
            for x in range(58, 64):
                c.set_pixel(x, y, A_TIMBER_DARK if y > 18 else A_FLOORBOARD_MID)
        c.line(0, 23, 5, 23, OUTLINE)
        c.line(58, 23, 63, 23, OUTLINE)
        c.line(5, 16, 5, 23, OUTLINE)
        c.line(58, 16, 58, 23, OUTLINE)

        if f <= 2:
            lift_left = f
            for x in range(6, 58):
                t = (x - 6) / 51.0
                board_top = int(16 - lift_left * (1.0 - t))
                for y in range(board_top, 24):
                    if y == 23:
                        c.set_pixel(x, y, OUTLINE)
                    elif y == board_top:
                        c.set_pixel(x, y, A_HONEY_BEAM if x % 8 < 4 else A_FLOORBOARD_LIGHT)
                    else:
                        c.set_pixel(x, y, A_FLOORBOARD_MID if (x + y) % 5 != 0 else A_WOOD_GRAIN)

            nail_y = 16 - lift_left - (f * 2)
            c.line(10, nail_y, 10, 16 - lift_left, OUTLINE)
            c.set_pixel(9, nail_y, A_BRASS_HL)
            c.set_pixel(10, nail_y, A_BRASS_MID)

            c.set_pixel(54, 16, OUTLINE)
            c.set_pixel(54, 17, A_BRASS_DARK)

            if f >= 1:
                c.set_pixel(8, nail_y - 2, WHITE_SHADOW)
                c.set_pixel(12, nail_y - 3, WHITE_SHADOW)
                if f == 2:
                    c.set_pixel(9, nail_y - 4, PURE_WHITE)

        elif f in (3, 4):
            for y in range(16, 24):
                for x in range(6, 58):
                    c.set_pixel(x, y, VOID_BLACK)

            left_y = 10 if f == 3 else 14
            right_y = 20 if f == 3 else 23

            for step in range(50):
                t = step / 49.0
                bx = int(8 + t * 46)
                by = int(left_y * (1.0 - t) + right_y * t)
                if 0 <= by < 24 and 0 <= bx < 64:
                    c.set_pixel(bx, by, A_FLOORBOARD_LIGHT)
                    if by + 1 < 24:
                        c.set_pixel(bx, by + 1, A_TIMBER_DARK)
                    if by + 2 < 24:
                        c.set_pixel(bx, by + 2, OUTLINE)

            c.set_pixel(56, 17, A_DUST_MID)
            c.set_pixel(57, 18, A_COBWEB_GRAY)

        else:
            for y in range(16, 24):
                for x in range(6, 58):
                    c.set_pixel(x, y, VOID_BLACK)

            if f == 5:
                for x in range(20, 48):
                    c.set_pixel(x, 22, A_TIMBER_DARK)
                    c.set_pixel(x, 23, OUTLINE)
                c.set_pixel(16, 19, A_DUST_MID)
                c.set_pixel(42, 20, A_COBWEB_GRAY)
            elif f == 6:
                c.set_pixel(24, 20, A_DUST_MID)
                c.set_pixel(38, 22, A_DUST_DARK)

        frames.append(c)
    return frames


def generate_hazard_dust_cloud() -> List[PixelCanvas]:
    """64x64, 8 frames @ 10 fps, loop: false.
    Cloud of dust puffing up from a floorboard.
    Bottom-anchored at floor lip y=63.
    """
    frames = []

    for f in range(8):
        c = PixelCanvas(64, 64, TRANSPARENT)

        # Ground anchor particles on floorboard at y=63 across all frames
        for x in range(24, 41, 4):
            c.set_pixel(x, 63, A_DUST_MID)
            c.set_pixel(x + 1, 63, A_COBWEB_GRAY)

        # Frame 0: Compact initial compression burst at floor (y=54..63)
        if f == 0:
            for x in range(20, 45):
                c.set_pixel(x, 63, OUTLINE)
            c.polygon([(20, 63), (24, 54), (40, 54), (44, 63)], A_DUST_MID, outline=OUTLINE)
            c.circle(32, 57, 4, A_COBWEB_GRAY)
            c.set_pixel(32, 55, WHITE_SHADOW)

        # Frame 1: Rapid expanding puff (y=36..63)
        elif f == 1:
            for x in range(14, 51):
                c.set_pixel(x, 63, OUTLINE)
            c.circle(24, 48, 8, A_DUST_MID, outline=OUTLINE)
            c.circle(40, 48, 8, A_DUST_MID, outline=OUTLINE)
            c.circle(32, 42, 10, A_COBWEB_GRAY, outline=OUTLINE)
            c.set_pixel(32, 38, WHITE_SHADOW)
            c.set_pixel(31, 37, PURE_WHITE)

        # Frame 2: Max plume volume (y=16..63)
        elif f == 2:
            for x in range(10, 55):
                c.set_pixel(x, 63, OUTLINE)
            c.circle(20, 42, 12, A_TIMBER_DARK, outline=OUTLINE)
            c.circle(44, 42, 12, A_TIMBER_DARK, outline=OUTLINE)
            c.circle(26, 30, 14, A_DUST_MID, outline=OUTLINE)
            c.circle(38, 28, 14, A_COBWEB_GRAY, outline=OUTLINE)
            c.circle(32, 22, 12, A_COBWEB_GRAY, outline=OUTLINE)
            c.line(26, 16, 38, 16, WHITE_SHADOW)
            c.set_pixel(32, 16, PURE_WHITE)

        # Frame 3: Plume billows higher (y=8..56)
        elif f == 3:
            c.circle(22, 32, 13, A_TIMBER_DARK, outline=OUTLINE)
            c.circle(42, 30, 13, A_TIMBER_DARK, outline=OUTLINE)
            c.circle(28, 20, 13, A_DUST_MID, outline=OUTLINE)
            c.circle(36, 16, 12, A_COBWEB_GRAY, outline=OUTLINE)
            c.line(30, 10, 40, 10, WHITE_SHADOW)

        # Frame 4: Dispersing into 3 floating puffs (y=6..50)
        elif f == 4:
            c.circle(18, 26, 10, A_DUST_MID, outline=OUTLINE)
            c.circle(44, 22, 10, A_DUST_MID, outline=OUTLINE)
            c.circle(30, 14, 9, A_COBWEB_GRAY, outline=OUTLINE)
            c.set_pixel(12, 14, WHITE_SHADOW)
            c.set_pixel(52, 16, WHITE_SHADOW)

        # Frame 5: Thinning wisps & scattered motes
        elif f == 5:
            c.circle(16, 22, 7, A_COBWEB_GRAY, outline=OUTLINE)
            c.circle(46, 18, 7, A_COBWEB_GRAY, outline=OUTLINE)
            c.circle(32, 12, 6, A_DUST_MID)
            for mx, my in [(8, 18), (24, 8), (40, 6), (54, 22), (28, 30)]:
                c.set_pixel(mx, my, WHITE_SHADOW)

        # Frame 6: Wisps drifting apart
        elif f == 6:
            c.circle(14, 18, 4, A_COBWEB_GRAY)
            c.circle(48, 14, 4, A_COBWEB_GRAY)
            for mx, my in [(6, 14), (20, 6), (36, 4), (56, 18)]:
                c.set_pixel(mx, my, WHITE_SHADOW)

        # Frame 7: Faint lingering particles
        elif f == 7:
            for mx, my in [(10, 12), (32, 4), (52, 14)]:
                c.set_pixel(mx, my, WHITE_SHADOW)

        frames.append(c)
    return frames


def generate_hazard_spider_drop() -> List[PixelCanvas]:
    """16x64, 10 frames @ 12 fps, loop: true.
    Spider dropping down on thread from above and retracting.
    """
    frames = []

    drop_ys = [4, 4, 16, 28, 40, 48, 48, 46, 28, 10]

    for f in range(10):
        c = PixelCanvas(16, 64, TRANSPARENT)
        sy = drop_ys[f]
        cx = 8

        for y in range(0, sy):
            c.set_pixel(cx, y, WHITE_SHADOW if y % 4 != 0 else PURE_WHITE)

        for y in range(sy, sy + 5):
            for x in range(6, 11):
                c.set_pixel(x, y, VOID_BLACK)
        c.set_pixel(cx, sy + 1, PURPLE_DARK)
        c.set_pixel(cx, sy + 2, PURPLE_DARK)

        for y in range(sy + 5, sy + 8):
            for x in range(7, 10):
                c.set_pixel(x, y, OUTLINE)

        eye_color = RED_LIGHT if f in (5, 6, 7) else RED_SHADOW
        c.set_pixel(cx - 1, sy + 7, eye_color)
        c.set_pixel(cx + 1, sy + 7, eye_color)

        leg_flare = 3 if f in (5, 6) else (1 if f in (0, 1) else 2)

        c.line(6, sy + 2, 6 - leg_flare - 1, sy - 1, OUTLINE)
        c.line(6, sy + 3, 6 - leg_flare - 2, sy + 2, OUTLINE)
        c.line(6, sy + 4, 6 - leg_flare - 2, sy + 6, OUTLINE)
        c.line(6, sy + 5, 6 - leg_flare - 1, sy + 9, OUTLINE)

        c.line(10, sy + 2, 10 + leg_flare + 1, sy - 1, OUTLINE)
        c.line(10, sy + 3, 10 + leg_flare + 2, sy + 2, OUTLINE)
        c.line(10, sy + 4, 10 + leg_flare + 2, sy + 6, OUTLINE)
        c.line(10, sy + 5, 10 + leg_flare + 1, sy + 9, OUTLINE)

        frames.append(c)
    return frames


# ==============================================================================
# 5. SHARED HAZARD FEEDBACK
# ==============================================================================

def generate_fx_warning_exclaim() -> List[PixelCanvas]:
    """16x24, 6 frames @ 12 fps, loop: true.
    Bouncing red exclamation mark popping above telegraphing hazard.
    """
    frames = []
    bounce_dy = [6, 1, 0, 1, 3, 5]

    for f in range(6):
        c = PixelCanvas(16, 24, TRANSPARENT)
        dy = bounce_dy[f]
        cx = 8

        for y in range(2 + dy, 13 + dy):
            half_w = 2 if y < 9 + dy else 1
            for x in range(cx - half_w, cx + half_w + 1):
                if x == cx - half_w or x == cx + half_w or y == 2 + dy or y == 12 + dy:
                    c.set_pixel(x, y, OUTLINE)
                elif y < 5 + dy and x == cx:
                    c.set_pixel(x, y, RED_LIGHT)
                else:
                    c.set_pixel(x, y, RED_MID)

        for y in range(15 + dy, 18 + dy):
            for x in range(cx - 1, cx + 2):
                if x in (cx - 1, cx + 1) and y in (15 + dy, 17 + dy):
                    c.set_pixel(x, y, OUTLINE)
                elif y == 15 + dy and x == cx:
                    c.set_pixel(x, y, RED_LIGHT)
                else:
                    c.set_pixel(x, y, RED_MID)

        if f in (1, 2, 3):
            c.set_pixel(cx - 5, 4 + dy, RED_LIGHT)
            c.set_pixel(cx + 5, 4 + dy, RED_LIGHT)
            if f == 2:
                c.set_pixel(cx - 6, 3 + dy, YELLOW_LIGHT)
                c.set_pixel(cx + 6, 3 + dy, YELLOW_LIGHT)

        frames.append(c)
    return frames


def generate_fx_slip_swirl() -> List[PixelCanvas]:
    """32x16, 6 frames @ 16 fps, loop: true.
    Swirl lines under P1 feet while slipping.
    """
    frames = []

    for f in range(6):
        c = PixelCanvas(32, 16, TRANSPARENT)
        cx, cy = 16, 9
        angle = f * (2 * math.pi / 6.0)

        for arc in (0, math.pi):
            base_a = angle + arc
            for step in range(16):
                t = step / 15.0
                rad = 3.0 + t * 9.0
                a = base_a + t * 2.2
                px = int(cx + math.cos(a) * rad * 1.3)
                py = int(cy + math.sin(a) * rad * 0.5)

                if 0 <= px < 32 and 0 <= py < 16:
                    if t > 0.8:
                        c.set_pixel(px, py, WHITE_SHADOW)
                    elif t > 0.3:
                        c.set_pixel(px, py, PURE_WHITE)
                    else:
                        c.set_pixel(px, py, YELLOW_LIGHT)

        streak_x = (f * 7) % 20
        c.line(streak_x, 14, min(31, streak_x + 8), 14, PURE_WHITE)
        c.line(31 - streak_x - 6, 15, 31 - streak_x, 15, WHITE_SHADOW)

        frames.append(c)
    return frames


def generate_fx_splat() -> List[PixelCanvas]:
    """32x32, 5 frames @ 20 fps, loop: false.
    Comic splash / splatter.
    """
    frames = []
    cx, cy = 16, 16

    for f in range(5):
        c = PixelCanvas(32, 32, TRANSPARENT)

        if f == 0:
            c.circle(cx, cy, 4, RED_MID, outline=OUTLINE)
            c.set_pixel(cx - 1, cy - 1, PURE_WHITE)
            c.set_pixel(cx, cy - 1, RED_LIGHT)
        elif f == 1:
            c.circle(cx, cy, 7, RED_MID, outline=OUTLINE)
            c.set_pixel(cx - 2, cy - 2, PURE_WHITE)
            lobe_angles = [0.2, 1.2, 2.3, 3.4, 4.5, 5.6]
            for a in lobe_angles:
                lx = int(cx + math.cos(a) * 11)
                ly = int(cy + math.sin(a) * 11)
                c.circle(lx, ly, 2, RED_MID, outline=OUTLINE)
        elif f == 2:
            c.circle(cx, cy, 5, RED_SHADOW, outline=OUTLINE)
            c.set_pixel(cx, cy, RED_MID)
            for a in [0.1, 0.9, 1.8, 2.7, 3.6, 4.5, 5.4]:
                lx = int(cx + math.cos(a) * 13)
                ly = int(cy + math.sin(a) * 13)
                if 0 <= lx < 32 and 0 <= ly < 32:
                    c.set_pixel(lx, ly, RED_MID)
                    c.set_pixel(lx, ly - 1, RED_LIGHT)
        elif f == 3:
            c.circle(cx, cy, 3, RED_SHADOW, outline=OUTLINE)
            for a in [0.2, 1.5, 3.0, 4.2, 5.3]:
                lx = int(cx + math.cos(a) * 14)
                ly = int(cy + math.sin(a) * 14)
                if 0 <= lx < 32 and 0 <= ly < 32:
                    c.set_pixel(lx, ly, RED_MID)
        elif f == 4:
            for a in [0.5, 2.0, 3.8, 5.0]:
                lx = int(cx + math.cos(a) * 15)
                ly = int(cy + math.sin(a) * 15)
                if 0 <= lx < 32 and 0 <= ly < 32:
                    c.set_pixel(lx, ly, RED_SHADOW)

        frames.append(c)
    return frames


def generate_fx_shield_bubble() -> List[PixelCanvas]:
    """64x64, 8 frames @ 12 fps, loop: false.
    Bubble-wrap shield around P1 with hard-banded alpha,
    pop animation in last 3 frames (5-7).
    """
    frames = []
    cx, cy = 32, 32

    for f in range(8):
        c = PixelCanvas(64, 64, TRANSPARENT)

        if f <= 4:
            base_r = 25.0 + (0.8 if f in (1, 2) else 0.0)

            for y in range(64):
                for x in range(64):
                    dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    if dist > base_r + 1.2:
                        continue

                    if dist > base_r - 1.5:
                        if x < cx and y < cy:
                            c.set_pixel(x, y, (245, 248, 252, 220))
                        else:
                            c.set_pixel(x, y, (77, 153, 242, 180))
                    elif dist > base_r - 3.5:
                        c.set_pixel(x, y, (130, 203, 250, 70))
                    else:
                        c.set_pixel(x, y, (188, 228, 252, 30))

            cell_centers = [
                (cx, cy), (cx - 10, cy - 8), (cx + 10, cy - 8),
                (cx - 10, cy + 8), (cx + 10, cy + 8), (cx - 18, cy),
                (cx + 18, cy), (cx, cy - 16), (cx, cy + 16)
            ]
            for ccx, ccy in cell_centers:
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        d_cell = math.sqrt(dx * dx + dy * dy)
                        if 1.8 < d_cell <= 3.2:
                            px, py = ccx + dx, ccy + dy
                            if 0 <= px < 64 and 0 <= py < 64:
                                c.set_pixel(px, py, (245, 248, 252, 140))
                        elif d_cell <= 1.8:
                            px, py = ccx + dx, ccy + dy
                            if 0 <= px < 64 and 0 <= py < 64:
                                c.set_pixel(px, py, (130, 203, 250, 60))

            for x in range(cx - 20, cx - 6):
                sy = cy - int(math.sqrt(max(0, 22 ** 2 - (x - cx) ** 2)))
                c.set_pixel(x, sy, (245, 248, 252, 255))
                c.set_pixel(x, sy + 1, (245, 248, 252, 180))

        elif f == 5:
            for y in range(64):
                for x in range(64):
                    dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    if 23.0 < dist <= 26.0:
                        c.set_pixel(x, y, (130, 203, 250, 140))

            crack_pts = [(cx - 20, cy), (cx - 10, cy - 4), (cx, cy + 2), (cx + 12, cy - 6), (cx + 22, cy)]
            for i in range(len(crack_pts) - 1):
                c.line(crack_pts[i][0], crack_pts[i][1], crack_pts[i+1][0], crack_pts[i+1][1], (245, 248, 252, 255))

            for sx, sy in [(cx - 14, cy - 14), (cx + 14, cy - 14), (cx - 14, cy + 14), (cx + 14, cy + 14)]:
                c.circle(sx, sy, 2, (245, 248, 252, 220))

        elif f == 6:
            for i in range(12):
                ang = i * (math.pi / 6.0)
                d = 28.0
                fx = int(cx + math.cos(ang) * d)
                fy = int(cy + math.sin(ang) * d)
                c.circle(fx, fy, 2, (130, 203, 250, 100))
                c.set_pixel(fx, fy, (245, 248, 252, 200))

        elif f == 7:
            for i in range(12):
                ang = i * (math.pi / 6.0) + 0.2
                d = 31.0
                fx = int(cx + math.cos(ang) * d)
                fy = int(cy + math.sin(ang) * d)
                if 0 <= fx < 64 and 0 <= fy < 64:
                    c.set_pixel(fx, fy, (130, 203, 250, 60))

        frames.append(c)
    return frames


def generate_fx_sugar_blur() -> List[PixelCanvas]:
    """64x32, 6 frames @ 24 fps, loop: true.
    Rainbow speed smear trail trailing behind P1.
    """
    frames = []

    rainbow_colors = [
        RED_MID, ORANGE_MID, YELLOW_MID, GREEN_MID, TEAL_LIGHT, PURPLE_LIGHT
    ]

    for f in range(6):
        c = PixelCanvas(64, 32, TRANSPARENT)

        for band_idx, col in enumerate(rainbow_colors):
            y_base = 4 + band_idx * 4

            for y in range(y_base, y_base + 4):
                shift = int(math.sin(f * 1.5 + band_idx) * 4)
                start_x = max(0, 10 + shift + (y % 2) * 6)

                for x in range(start_x, 64):
                    dash_mod = (x + f * 5) % 10
                    if x < 28 and dash_mod < 4:
                        continue

                    if x > 48 and y in (y_base + 1, y_base + 2):
                        if (x + f * 3) % 6 == 0:
                            c.set_pixel(x, y, PURE_WHITE)
                        else:
                            c.set_pixel(x, y, col)
                    else:
                        c.set_pixel(x, y, col)

        needle_y = [7, 13, 19, 25][f % 4]
        c.line(16, needle_y, 56, needle_y, PURE_WHITE)

        frames.append(c)
    return frames


# ==============================================================================
# MAIN RUNNER & MANIFEST UPDATER
# ==============================================================================

def main():
    art_dir = Path("art/v2")
    art_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = art_dir / "manifest.json"
    if manifest_path.exists():
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    else:
        manifest = {}

    print("Generating Phase C Hazards & FX...")

    tasks = {
        # Kitchen
        "hazard_juice_puddle.png": (generate_hazard_juice_puddle, {"frame_w": 96, "frame_h": 16, "frames": 6, "fps": 8, "loop": True}),
        "hazard_marble.png": (generate_hazard_marble, {"frame_w": 24, "frame_h": 24, "frames": 8, "fps": 14, "loop": True}),
        "hazard_stove_burner.png": (generate_hazard_stove_burner, {"frame_w": 64, "frame_h": 48, "frames": 10, "fps": 10, "loop": True}),
        "hazard_spill_trail.png": (generate_hazard_spill_trail, {"frame_w": 32, "frame_h": 16, "frames": 4, "fps": 6, "loop": True}),

        # Backyard
        "hazard_sprinkler.png": (generate_hazard_sprinkler, {"frame_w": 64, "frame_h": 96, "frames": 10, "fps": 10, "loop": True}),
        "hazard_water_spray.png": (generate_hazard_water_spray, {"frame_w": 192, "frame_h": 96, "frames": 8, "fps": 14, "loop": True}),
        "hazard_mud.png": (generate_hazard_mud, {"frame_w": 96, "frame_h": 16, "frames": 6, "fps": 6, "loop": True}),
        "hazard_wind_gust.png": (generate_hazard_wind_gust, {"frame_w": 192, "frame_h": 64, "frames": 8, "fps": 14, "loop": True}),
        "fx_leaf.png": (generate_fx_leaf, {"frame_w": 16, "frame_h": 16, "frames": 8, "fps": 12, "loop": True}),
        "fx_leaf_b.png": (generate_fx_leaf_b, {"frame_w": 16, "frame_h": 16, "frames": 8, "fps": 12, "loop": True}),

        # Basement
        "hazard_paint_can.png": (generate_hazard_paint_can, {"frame_w": 40, "frame_h": 40, "frames": 8, "fps": 12, "loop": True}),
        "hazard_drip.png": (generate_hazard_drip, {"frame_w": 16, "frame_h": 48, "frames": 10, "fps": 12, "loop": True}),
        "hazard_mousetrap.png": (generate_hazard_mousetrap, {"frame_w": 48, "frame_h": 24, "frames": 8, "fps": 14, "loop": False}),
        "light_flashlight_cone.png": (generate_light_flashlight_cone, {"frame_w": 256, "frame_h": 128, "frames": 1, "fps": 0, "loop": False}),
        "light_dark_mask.png": (generate_light_dark_mask, {"frame_w": 512, "frame_h": 512, "frames": 1, "fps": 0, "loop": False}),
        "item_flashlight.png": (generate_item_flashlight, {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True}),
        "item_flashlight_pop.png": (generate_item_flashlight_pop, {"frame_w": 48, "frame_h": 48, "frames": 3, "fps": 24, "loop": False}),

        # Attic
        "hazard_cobweb.png": (generate_hazard_cobweb, {"frame_w": 96, "frame_h": 64, "frames": 6, "fps": 6, "loop": True}),
        "hazard_loose_board.png": (generate_hazard_loose_board, {"frame_w": 64, "frame_h": 24, "frames": 8, "fps": 10, "loop": False}),
        "hazard_dust_cloud.png": (generate_hazard_dust_cloud, {"frame_w": 64, "frame_h": 64, "frames": 8, "fps": 10, "loop": False}),
        "hazard_spider_drop.png": (generate_hazard_spider_drop, {"frame_w": 16, "frame_h": 64, "frames": 10, "fps": 12, "loop": True}),

        # Shared Feedback
        "fx_warning_exclaim.png": (generate_fx_warning_exclaim, {"frame_w": 16, "frame_h": 24, "frames": 6, "fps": 12, "loop": True}),
        "fx_slip_swirl.png": (generate_fx_slip_swirl, {"frame_w": 32, "frame_h": 16, "frames": 6, "fps": 16, "loop": True}),
        "fx_splat.png": (generate_fx_splat, {"frame_w": 32, "frame_h": 32, "frames": 5, "fps": 20, "loop": False}),
        "fx_shield_bubble.png": (generate_fx_shield_bubble, {"frame_w": 64, "frame_h": 64, "frames": 8, "fps": 12, "loop": False}),
        "fx_sugar_blur.png": (generate_fx_sugar_blur, {"frame_w": 64, "frame_h": 32, "frames": 6, "fps": 24, "loop": True}),
    }

    for filename, (gen_fn, meta) in tasks.items():
        out_file = str(art_dir / filename)
        result = gen_fn()
        if isinstance(result, list):
            assemble_strip(result, out_file)
        else:
            save_single(result, out_file)

        manifest[filename] = meta
        print(f"Delivered {filename} -> manifest updated.")

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
    print(f"Successfully updated {manifest_path} with {len(manifest)} total assets.")

if __name__ == "__main__":
    main()
