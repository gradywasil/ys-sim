"""Younger Sibling Simulator - Phase B Basement & Attic Art Generator v3.

Generates all Basement and Attic stage assets into art/v2/:
Basement:
  1. Parallax Layers:
     - basement_bg_far.png (960x540, 1)
     - basement_bg_far_anim.png (3840x540, 4f @ 3fps)
     - basement_bg_mid.png (1280x540, 1, floor y=400, seamless)
     - basement_bg_near.png (960x540, 1, y<400 transparent)
     - basement_sky_gradient.png (1x540, 1)
     - basement_fg_legs.png (960x540, 1)
     - basement_fg_dust.png (960x540, 1)
  2. Tileset & Obstacles:
     - basement_tileset_floor.png (256x96, 8x3 32px)
     - basement_pit_bg.png (32x128, 1)
     - basement_obstacles.png (128x32, 4f 32x32)
     - basement_obstacles_tall.png (128x32, 4f 32x32)
  3. Goal Gate:
     - basement_goal.png (384x128, 6f 64x128 @ 10fps)
  4. Floor Clutter (10 items + 10 shadows):
     - screw, nail, bolt, rag, flashlight, crumpled_blueprint, rusty_key, jar_of_nails, mouse_trap, sawdust
  5. Animated Props (6 props):
     - basement_prop_bulb.png (64x96, 10f @ 6fps)
     - basement_prop_furnace.png (96x96, 8f @ 8fps)
     - basement_prop_pipe_drip.png (48x80, 10f @ 10fps)
     - basement_prop_washer.png (80x80, 8f @ 12fps)
     - basement_prop_spider.png (32x80, 12f @ 8fps)
     - basement_prop_tv_static.png (80x64, 6f @ 12fps)

Attic:
  1. Parallax Layers:
     - attic_bg_far.png (960x540, 1)
     - attic_bg_far_anim.png (3840x540, 4f @ 3fps)
     - attic_bg_mid.png (1280x540, 1, floor y=400, seamless)
     - attic_bg_near.png (960x540, 1, y<400 transparent)
     - attic_sky_gradient.png (1x540, 1)
     - attic_fg_legs.png (960x540, 1)
     - attic_fg_dust.png (960x540, 1)
  2. Tileset & Obstacles:
     - attic_tileset_floor.png (256x96, 8x3 32px)
     - attic_pit_bg.png (32x128, 1)
     - attic_obstacles.png (128x32, 4f 32x32)
     - attic_obstacles_tall.png (128x32, 4f 32x32)
  3. Goal Gate:
     - attic_goal.png (384x128, 6f 64x128 @ 10fps)
  4. Floor Clutter (10 items + 10 shadows):
     - marble, brittle_comic, faded_photo, music_box_key, tarnished_spoon,
       bundle_of_letters, doll_arm, teddy_eye, dust_bunny, jar_of_buttons
  5. Animated Props (6 props):
     - attic_prop_rocking_chair.png (80x96, 10f @ 6fps)
     - attic_prop_moon_window.png (96x128, 8f @ 6fps)
     - attic_prop_sheet_ghost.png (80x96, 8f @ 6fps)
     - attic_prop_music_box.png (64x64, 8f @ 8fps)
     - attic_prop_cobweb.png (64x64, 8f @ 6fps)
     - attic_prop_mobile.png (80x80, 10f @ 6fps)
"""

import json
import math
import os
import sys
from pathlib import Path
from typing import List, Tuple
from PIL import Image

sys.path.append(os.path.dirname(__file__))

from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE, VOID_BLACK,
    SHADOW_PURPLE_DARK, SHADOW_PURPLE_DEEP, SHADOW_PURPLE_MID, SHADOW_DEEP, SHADOW_MID,
    PURPLE_DARK, PURPLE_MID, PURPLE_RICH, PURPLE_LIGHT,
    DUSK_LILAC, DUSK_PINK, DUSK_ROSE, DUSK_PEACH, DUSK_BLUSH, DUSK_CREAM,
    SKIN_DEEP, SKIN_SHADOW, SKIN_MID, SKIN_LIGHT, SKIN_HIGHLIGHT,
    WOOD_BLACK, BROWN_DARKEST, BROWN_DARK, BROWN_MID, BROWN_LIGHT,
    WOOD_HIGHLIGHT, WOOD_LIT,
    RED_DEEP, RED_SHADOW, RED_RICH, RED_MID, RED_LIGHT, RED_HIGHLIGHT,
    BLUE_DEEP, BLUE_SHADOW, BLUE_RICH, BLUE_MID, BLUE_LIGHT, BLUE_HIGHLIGHT,
    YELLOW_DEEP, YELLOW_SHADOW, YELLOW_RICH, YELLOW_MID, YELLOW_LIGHT, YELLOW_HIGHLIGHT,
    GREEN_DEEP, GREEN_SHADOW, GREEN_RICH, GREEN_MID, GREEN_LIGHT, GREEN_HIGHLIGHT,
    ORANGE_DEEP, ORANGE_SHADOW, ORANGE_MID, ORANGE_LIGHT,
    TEAL_SHADOW, TEAL_MID, TEAL_LIGHT, TEAL_HIGHLIGHT,
    METAL_SHADOW, METAL_MID, WHITE_SHADOW, WHITE_MID, PURE_WHITE,
)
from stage_palettes import STAGE_RGBA

RGBA = Tuple[int, int, int, int]

# Basement Accents (0..15)
B0 = STAGE_RGBA["basement"][0]   # #1e2530: concrete deep shadow
B1 = STAGE_RGBA["basement"][1]   # #2f3b4c: concrete slab dark
B2 = STAGE_RGBA["basement"][2]   # #4a5a70: concrete mid
B3 = STAGE_RGBA["basement"][3]   # #6e8099: concrete light
B4 = STAGE_RGBA["basement"][4]   # #94a6bd: concrete highlight
B5 = STAGE_RGBA["basement"][5]   # #151b24: cast iron drain grate
B6 = STAGE_RGBA["basement"][6]   # #693521: pipe rust dark
B7 = STAGE_RGBA["basement"][7]   # #994e2b: pipe rust mid
B8 = STAGE_RGBA["basement"][8]   # #c46e37: pipe rust / furnace ember orange
B9 = STAGE_RGBA["basement"][9]   # #f79434: furnace fire flame yellow-orange
B10 = STAGE_RGBA["basement"][10] # #fed147: furnace fire bright core
B11 = STAGE_RGBA["basement"][11] # #2b4859: industrial slate dark
B12 = STAGE_RGBA["basement"][12] # #3f6c85: water puddle blue-gray
B13 = STAGE_RGBA["basement"][13] # #5fa2b8: drip ripple highlight
B14 = STAGE_RGBA["basement"][14] # #3e2a47: oil stain iridescent purple
B15 = STAGE_RGBA["basement"][15] # #80705a: dry sawdust amber-tan

# Attic Accents (0..15)
A0 = STAGE_RGBA["attic"][0]   # #241910: aged attic timber deep
A1 = STAGE_RGBA["attic"][1]   # #3d2919: dusty oak board dark
A2 = STAGE_RGBA["attic"][2]   # #5c3e24: attic floorboard mid
A3 = STAGE_RGBA["attic"][3]   # #825832: attic floorboard light
A4 = STAGE_RGBA["attic"][4]   # #b37f49: warm wood grain amber
A5 = STAGE_RGBA["attic"][5]   # #deb073: golden honey beam highlight
A6 = STAGE_RGBA["attic"][6]   # #544b3c: dust layer dark olive-tan
A7 = STAGE_RGBA["attic"][7]   # #80735d: dust layer mid
A8 = STAGE_RGBA["attic"][8]   # #b5a68d: dusty cobweb gray-linen
A9 = STAGE_RGBA["attic"][9]   # #e8dec8: parchment letter yellow-ivory
A10 = STAGE_RGBA["attic"][10] # #804a5e: antique faded rose
A11 = STAGE_RGBA["attic"][11] # #ad6d83: antique doll dress rose
A12 = STAGE_RGBA["attic"][12] # #69592a: tarnished trunk brass dark
A13 = STAGE_RGBA["attic"][13] # #a38e42: tarnished brass mid
A14 = STAGE_RGBA["attic"][14] # #d9c264: brass latch specular
A15 = STAGE_RGBA["attic"][15] # #697894: moonlit window dust blue-gray


def make_shadow(w: int, h: int, cx: int, cy: int, rx: int, ry: int) -> PixelCanvas:
    """Creates matching 1-bit hard-banded shadow sprite in OUTLINE color."""
    c = PixelCanvas(w, h, TRANSPARENT)
    for y in range(max(0, cy - ry), min(h, cy + ry + 1)):
        for x in range(max(0, cx - rx), min(w, cx + rx + 1)):
            dx = (x - cx) / float(max(1, rx))
            dy = (y - cy) / float(max(1, ry))
            if dx * dx + dy * dy <= 1.0:
                c.set_pixel(x, y, OUTLINE)
    return c


def save_single(canvas: PixelCanvas, output_path: str):
    canvas.to_image().save(output_path, "PNG")
    print(f"Saved {output_path} ({canvas.width}x{canvas.height}, 1 frame)")


# ==============================================================================
# BASEMENT ASSETS
# ==============================================================================

# --- 1. Parallax Layers ---

def generate_basement_sky_gradient() -> PixelCanvas:
    """1x540 px: 8 hard color bands of cool industrial concrete dusk."""
    c = PixelCanvas(1, 540)
    bands = [
        (0, 68, VOID_BLACK),
        (68, 135, B5),
        (135, 203, B0),
        (203, 270, B1),
        (270, 338, B11),
        (338, 405, B2),
        (405, 473, B12),
        (473, 540, B3),
    ]
    for y0, y1, col in bands:
        for y in range(y0, y1):
            c.set_pixel(0, y, col)
    return c


def generate_basement_bg_far() -> PixelCanvas:
    """960x540 px: Concrete brick walls with mortar lines, hanging pipes, fuse box,
    workbench silhouette, small high window well. Floor at y=400.
    """
    c = PixelCanvas(960, 540, B0)

    # 1. Concrete block wall (y=0..400)
    # Staggered cinder blocks (60x24) with mortar lines in B5
    for row, y in enumerate(range(0, 400, 24)):
        c.line(0, y, 959, y, B5)
        offset = 30 if row % 2 == 1 else 0
        for x in range(offset, 960, 60):
            c.line(x, y, x, min(400, y + 24), B5)
            # Subtle cinder block texture
            c.set_pixel((x + 15) % 960, y + 8, B1)
            c.set_pixel((x + 35) % 960, y + 16, B2)
            c.set_pixel((x + 48) % 960, y + 12, B11)

    # Floor baseboard / slab seam at y=400
    c.rect(0, 400, 960, 6, B5)
    c.line(0, 400, 959, 400, B1)
    # Floor slab tone
    for y in range(406, 540):
        shade = B0 if y < 450 else VOID_BLACK
        c.line(0, y, 959, y, shade)

    # 2. Ceiling Pipes (y=15..65)
    # Top main steam/water pipe
    c.rect(0, 24, 960, 10, B7)
    c.line(0, 24, 959, 24, B8)
    c.line(0, 33, 959, 33, B6)
    # Pipe brackets / joints every 120px
    for px in range(60, 960, 120):
        c.rect(px - 4, 15, 8, 24, B6, outline=B5)
        c.rect(px - 6, 22, 12, 14, B8, outline=B6)
        # Small hanging valve
        if px == 300 or px == 660:
            c.rect(px - 8, 34, 16, 6, METAL_MID, outline=B5)
            c.circle(px, 46, 8, RED_MID, outline=RED_DEEP)
            c.set_pixel(px, 46, METAL_MID)

    # Lower secondary pipe (y=50..58)
    c.rect(0, 52, 960, 6, B11)
    c.line(0, 52, 959, 52, B3)
    c.line(0, 57, 959, 57, B5)

    # 3. High Basement Window Well (x=720..850, y=40..110)
    c.rect(720, 40, 130, 70, B5)
    c.rect(724, 44, 122, 62, B1)
    # Window frame
    c.rect(732, 50, 106, 50, B11, outline=B5)
    # Window panes with cool dusk light
    c.rect(736, 54, 46, 42, B12)
    c.rect(786, 54, 48, 42, B12)
    c.line(782, 50, 785, 100, B5)
    # Window well corrugated iron curve silhouette above
    for ax in range(715, 855):
        c.set_pixel(ax, 38, B3)
        c.set_pixel(ax, 39, B5)

    # 4. Electrical Breaker / Fuse Box (x=240..310, y=140..230)
    c.rect(240, 140, 70, 90, B5)
    c.rect(242, 142, 66, 86, METAL_SHADOW)
    c.rect(245, 145, 60, 80, B11, outline=B5)
    # Conduit pipe from ceiling down to fuse box
    c.rect(272, 58, 6, 82, METAL_MID, outline=B5)
    # Warning triangle on fuse box
    c.line(275, 165, 268, 178, YELLOW_MID)
    c.line(268, 178, 282, 178, YELLOW_MID)
    c.line(282, 178, 275, 165, YELLOW_MID)
    c.set_pixel(275, 172, VOID_BLACK)
    # Door latch handle
    c.rect(298, 180, 4, 12, METAL_MID, outline=B5)

    # 5. Vintage Workbench Silhouette in distance (x=400..620, y=320..400)
    c.rect(400, 320, 220, 80, B5)
    # Pegboard back
    c.rect(404, 324, 212, 40, B1)
    for pgy in range(328, 360, 6):
        for pgx in range(408, 612, 10):
            c.set_pixel(pgx, pgy, B5)
    # Hanging tool silhouettes
    # Hand saw silhouette
    c.line(420, 330, 440, 350, B5)
    c.line(422, 330, 442, 350, B5)
    # Hammer silhouette
    c.line(470, 330, 470, 352, B5)
    c.rect(466, 332, 9, 5, B5)
    # Wrench silhouette
    c.line(520, 330, 520, 350, B5)
    c.circle(520, 332, 3, B5)
    # Tabletop slab
    c.rect(396, 364, 228, 8, B1, outline=B5)
    c.line(396, 364, 623, 364, B3)

    return c


def generate_basement_bg_far_anim() -> List[PixelCanvas]:
    """3840x540 px total (4 frames of 960x540 @ 3 fps):
    Flickering ceiling light bulb filament and shadow shift on wall.
    """
    frames = []
    # Base coords of ceiling light fixture
    lx, ly = 480, 0
    cord_len = 100
    by = ly + cord_len  # bulb center y=100

    flicker_data = [
        # (halo_r, fil_col, halo_col, shadow_shift)
        (70, B10, YELLOW_MID, 0),    # F0: Steady warm glow
        (50, B9, B8, -2),            # F1: Slight dim dip
        (90, PURE_WHITE, B10, 3),    # F2: Bright flare spike
        (65, B10, YELLOW_MID, 1),    # F3: Return settling
    ]

    for halo_r, fil_col, halo_col, sshift in flicker_data:
        c = PixelCanvas(960, 540, TRANSPARENT)

        # Ceiling junction box & hanging black wire
        c.rect(lx - 10, 0, 20, 10, B5)
        c.line(lx, 10, lx, by - 12, B5)
        # Brass socket fixture
        c.rect(lx - 6, by - 12, 12, 10, B8, outline=B5)
        c.line(lx - 6, by - 12, lx + 5, by - 12, B10)

        # Light halo hard-banded rings
        for r_step, col in [(halo_r, B0), (int(halo_r * 0.7), B1), (int(halo_r * 0.4), B2), (int(halo_r * 0.2), halo_col)]:
            c.circle(lx, by, r_step, fill=col)

        # Glass bulb shape
        c.circle(lx, by, 10, B2, outline=B5)
        c.circle(lx, by - 2, 7, B3)

        # Filament loop glowing
        c.line(lx - 3, by, lx - 1, by - 4, fil_col)
        c.line(lx - 1, by - 4, lx + 1, by - 4, fil_col)
        c.line(lx + 1, by - 4, lx + 3, by, fil_col)
        c.set_pixel(lx, by - 3, PURE_WHITE if fil_col == PURE_WHITE else fil_col)

        # Dynamic wall shadow band shifting with flicker
        sy = 220 + sshift
        c.line(0, sy, 959, sy, B5)
        c.line(0, sy + 1, 959, sy + 1, B0)

        frames.append(c)

    return frames


def generate_basement_bg_mid() -> PixelCanvas:
    """1280x540 px: Seamless left/right mid layer, floor at y=400.
    Furnace with glowing grate, shelves of paint cans and toolboxes,
    workbench with vise, old washing machine.
    """
    c = PixelCanvas(1280, 540, TRANSPARENT)

    # Seamless background wall tint between items (concrete wall)
    for y in range(80, 400):
        col = B1 if y % 32 < 2 else B0
        c.line(0, y, 1279, y, col)

    # Floor baseboard and floor surface (y=400..540)
    c.rect(0, 400, 1280, 8, B5)
    c.line(0, 400, 1279, 400, B3)
    for y in range(408, 540):
        # Concrete floor with horizontal slab seams
        fcol = B1 if (y % 40 == 0) else B0
        c.line(0, y, 1279, y, fcol)
    # Vertical expansion joints every 160 px (divides 1280 cleanly!)
    for fx in range(0, 1280, 160):
        c.line(fx, 408, fx, 539, B5)

    # -------------------------------------------------------------------------
    # 1. Cast Iron Furnace with Glowing Grate (x=120..280, y=210..400)
    # -------------------------------------------------------------------------
    fx0, fy0 = 130, 210
    # Heavy exhaust stovepipe going up to ceiling
    c.rect(fx0 + 50, 40, 30, 170, B5)
    c.line(fx0 + 50, 40, fx0 + 50, 210, B3)
    c.line(fx0 + 79, 40, fx0 + 79, 210, VOID_BLACK)
    # Furnace body (heavy iron cylindrical stove)
    c.rect(fx0, fy0, 130, 190, B5, outline=VOID_BLACK)
    c.rect(fx0 + 4, fy0 + 4, 122, 182, B1)
    c.line(fx0 + 4, fy0 + 4, fx0 + 125, fy0 + 4, B3) # top rim
    # Rivet lines
    for ry in range(fy0 + 15, fy0 + 190, 30):
        for rx in [fx0 + 8, fx0 + 122]:
            c.rect(rx, ry, 3, 3, B3, outline=B5)
    # Firebox door (heavy arched door)
    c.rect(fx0 + 25, fy0 + 70, 80, 85, B5, outline=VOID_BLACK)
    c.rect(fx0 + 30, fy0 + 75, 70, 75, VOID_BLACK)
    # Iron grate bars
    for gx in range(fx0 + 35, fx0 + 95, 10):
        c.line(gx, fy0 + 75, gx, fy0 + 149, B5)
    # Glowing fire/embers behind grate
    c.rect(fx0 + 32, fy0 + 110, 66, 38, B8)
    c.rect(fx0 + 36, fy0 + 122, 58, 24, B9)
    c.rect(fx0 + 44, fy0 + 130, 42, 14, B10)
    # Door latch
    c.rect(fx0 + 106, fy0 + 105, 6, 18, METAL_MID, outline=B5)

    # -------------------------------------------------------------------------
    # 2. Industrial Shelving Unit (x=360..600, y=140..400)
    # -------------------------------------------------------------------------
    sx0, sy0 = 370, 140
    # Steel uprights
    c.rect(sx0, sy0, 8, 260, B5)
    c.rect(sx0 + 200, sy0, 8, 260, B5)
    c.line(sx0, sy0, sx0, sy0 + 259, B3)
    c.line(sx0 + 200, sy0, sx0 + 200, sy0 + 259, B3)
    # Shelves (4 horizontal shelves)
    for shy in [sy0 + 60, sy0 + 125, sy0 + 195, sy0 + 255]:
        c.rect(sx0, shy, 208, 6, B11, outline=B5)
        c.line(sx0, shy, sx0 + 207, shy, B3)
    # Shelf 1: Paint cans (1-gallon cans)
    for cx in range(sx0 + 20, sx0 + 180, 32):
        c.rect(cx, sy0 + 28, 24, 32, METAL_MID, outline=B5)
        c.line(cx, sy0 + 28, cx + 23, sy0 + 28, WHITE_MID)
        # Colored paint label bands
        lbl_col = RED_MID if cx % 64 == 20 else BLUE_MID
        c.rect(cx + 2, sy0 + 38, 20, 14, lbl_col)
    # Shelf 2: Rusty toolboxes
    c.rect(sx0 + 25, sy0 + 90, 70, 35, B6, outline=B5)
    c.line(sx0 + 25, sy0 + 90, sx0 + 94, sy0 + 90, B8)
    c.rect(sx0 + 55, sy0 + 84, 12, 6, METAL_MID, outline=B5) # handle
    c.rect(sx0 + 115, sy0 + 96, 65, 29, TEAL_SHADOW, outline=B5)
    c.line(sx0 + 115, sy0 + 96, sx0 + 179, sy0 + 96, TEAL_LIGHT)
    # Shelf 3: Glass jars with screws & nails
    for jx in range(sx0 + 20, sx0 + 180, 28):
        c.rect(jx, sy0 + 165, 18, 30, B2, outline=B5)
        c.rect(jx + 2, sy0 + 175, 14, 18, B5) # contents
        c.line(jx + 2, sy0 + 167, jx + 4, sy0 + 190, WHITE_MID) # glass glint

    # -------------------------------------------------------------------------
    # 3. Heavy Workbench with Bench Vise (x=680..940, y=260..400)
    # -------------------------------------------------------------------------
    wx0, wy0 = 700, 270
    # Pegboard back
    c.rect(wx0, wy0 - 100, 220, 100, B1, outline=B5)
    for pgy in range(wy0 - 95, wy0, 10):
        for pgx in range(wx0 + 8, wx0 + 215, 12):
            c.set_pixel(pgx, pgy, B5)
    # Workbench top thick maple/steel slab
    c.rect(wx0 - 10, wy0, 240, 20, BROWN_MID, outline=VOID_BLACK)
    c.line(wx0 - 10, wy0, wx0 + 229, wy0, WOOD_LIT)
    # Steel frame legs
    c.rect(wx0 + 10, wy0 + 20, 14, 110, B5)
    c.rect(wx0 + 196, wy0 + 20, 14, 110, B5)
    c.line(wx0 + 10, wy0 + 20, wx0 + 10, wy0 + 129, B3)
    c.line(wx0 + 196, wy0 + 20, wx0 + 196, wy0 + 129, B3)
    # Lower tool shelf
    c.rect(wx0 + 10, wy0 + 85, 200, 10, B11, outline=B5)
    # Heavy Bench Vise on left corner
    c.rect(wx0 - 6, wy0 - 24, 28, 24, B5, outline=VOID_BLACK)
    c.rect(wx0 - 2, wy0 - 20, 20, 8, METAL_MID)
    c.rect(wx0 - 14, wy0 - 18, 8, 14, METAL_MID, outline=B5)
    # Vise handle screw bar
    c.line(wx0 - 18, wy0 - 26, wx0 - 10, wy0 - 6, METAL_MID)

    # -------------------------------------------------------------------------
    # 4. Vintage Washing Machine (x=1020..1180, y=250..400)
    # -------------------------------------------------------------------------
    wash_x, wash_y = 1040, 260
    c.rect(wash_x, wash_y, 110, 140, WHITE_SHADOW, outline=B5)
    c.line(wash_x, wash_y, wash_x + 109, wash_y, PURE_WHITE)
    c.line(wash_x, wash_y, wash_x, wash_y + 139, WHITE_MID)
    # Top control console
    c.rect(wash_x, wash_y - 20, 110, 20, WHITE_MID, outline=B5)
    # Control dials
    c.circle(wash_x + 30, wash_y - 10, 6, B5)
    c.set_pixel(wash_x + 30, wash_y - 10, WHITE_MID)
    c.circle(wash_x + 60, wash_y - 10, 6, B5)
    c.circle(wash_x + 85, wash_y - 10, 4, RED_MID)
    # Front round wash drum door
    c.circle(wash_x + 55, wash_y + 65, 34, B5)
    c.circle(wash_x + 55, wash_y + 65, 30, METAL_MID)
    c.circle(wash_x + 55, wash_y + 65, 24, B12)
    # Door glint
    c.line(wash_x + 40, wash_y + 50, wash_x + 65, y_val := wash_y + 50, PURE_WHITE)
    # Rubber drain hose leading to floor
    c.line(wash_x + 105, wash_y + 80, wash_x + 120, wash_y + 130, B5)
    c.line(wash_x + 120, wash_y + 130, wash_x + 125, wash_y + 140, B5)

    return c


def generate_basement_bg_near() -> PixelCanvas:
    """960x540 px: Silhouettes layer.
    STRICT: 100% transparent above floor line y=400 (y=0..399 is transparent!).
    Dark silhouettes of stack of tires, laundry basket, heavy crate with 1px warm rim light.
    """
    c = PixelCanvas(960, 540, TRANSPARENT)
    BODY = VOID_BLACK
    RIM = B8  # Warm amber/rust 1px rim light

    # 1. Stack of car tires (x=60..190, y=410..535)
    tx, ty = 125, 415
    for tire_idx in range(3):
        cur_y = ty + tire_idx * 40
        # Oval tire profile
        rx, ry = 55, 22
        for py in range(cur_y - ry, cur_y + ry + 1):
            if py < 400:
                continue
            for px in range(tx - rx, tx + rx + 1):
                dx = (px - tx) / float(rx)
                dy = (py - cur_y) / float(ry)
                if dx * dx + dy * dy <= 1.0:
                    c.set_pixel(px, py, BODY)
        # Inner rim depression
        for py in range(cur_y - 10, cur_y + 11):
            if py < 400:
                continue
            for px in range(tx - 25, tx + 26):
                dx = (px - tx) / 25.0
                dy = (py - cur_y) / 10.0
                if dx * dx + dy * dy <= 1.0:
                    c.set_pixel(px, py, B5)
        # 1px Rim Light on top curve
        for px in range(tx - 45, tx + 10):
            r_py = int(cur_y - ry * math.sqrt(max(0.0, 1.0 - ((px - tx) / float(rx)) ** 2)))
            if r_py >= 400:
                c.set_pixel(px, r_py, RIM)

    # 2. Laundry basket with spilling clothes (x=380..510, y=415..535)
    lx0, ly0 = 400, 440
    # Plastic mesh basket silhouette
    c.rect(lx0, ly0, 90, 85, BODY)
    # Upper-left rim
    c.line(lx0, ly0, lx0 + 89, ly0, RIM)
    c.line(lx0, ly0, lx0, ly0 + 84, RIM)
    # Clothes bulging out of top
    c.circle(lx0 + 25, ly0 - 8, 18, BODY)
    c.circle(lx0 + 60, ly0 - 12, 22, BODY)
    # Spilling towel onto floor
    c.rect(lx0 - 15, ly0 + 30, 20, 60, BODY)
    c.line(lx0 + 10, ly0 - 24, lx0 + 35, ly0 - 24, RIM)
    c.line(lx0 + 45, ly0 - 32, lx0 + 75, ly0 - 32, RIM)
    c.line(lx0 - 15, ly0 + 30, lx0 - 15, ly0 + 89, RIM)

    # 3. Heavy wooden crate with diagonal braces (x=700..870, y=410..535)
    cx0, cy0 = 720, 420
    cw, ch = 130, 110
    c.rect(cx0, cy0, cw, ch, BODY)
    # Rim light on crate top and left
    c.line(cx0, cy0, cx0 + cw - 1, cy0, RIM)
    c.line(cx0, cy0, cx0, cy0 + ch - 1, RIM)
    # Diagonal brace lines (silhouette texture)
    c.line(cx0 + 10, cy0 + 10, cx0 + cw - 10, cy0 + ch - 10, B5)
    c.line(cx0 + 10, cy0 + ch - 10, cx0 + cw - 10, cy0 + 10, B5)

    return c


def generate_basement_fg_legs() -> PixelCanvas:
    """960x540 px: Heavy steel workbench legs and vertical iron support beam."""
    c = PixelCanvas(960, 540, TRANSPARENT)
    SIL = VOID_BLACK
    RIM = B3

    # Vertical iron support column (lally column) on left (x=110..150, y=0..540)
    c.rect(115, 0, 24, 540, SIL)
    c.line(115, 0, 115, 539, RIM)
    c.line(138, 0, 138, 539, OUTLINE)
    # Column top and base plates
    c.rect(105, 0, 44, 16, SIL)
    c.line(105, 15, 148, 15, RIM)
    c.rect(105, 510, 44, 30, SIL)
    c.line(105, 510, 148, 510, RIM)

    # Steel workbench legs on right (x=780..960, y=280..540)
    # Table apron
    c.rect(760, 280, 200, 24, SIL)
    c.line(760, 280, 959, 280, RIM)
    # Heavy diagonal I-beam leg
    for y in range(304, 540):
        lx = 840 + int((y - 304) * 0.15)
        c.rect(lx, y, 22, 1, SIL)
        c.set_pixel(lx, y, RIM)
        c.set_pixel(lx + 21, y, OUTLINE)
    # Base pad
    c.rect(860, 525, 45, 15, SIL)
    c.line(860, 525, 904, 525, RIM)

    return c


def generate_basement_fg_dust() -> PixelCanvas:
    """960x540 px: Cobweb filaments and floating cellar dust motes (hard-banded alpha)."""
    c = PixelCanvas(960, 540, TRANSPARENT)
    rgb_dust = B4[:3]
    rgb_slate = B3[:3]

    # Corner cobweb filaments in upper left & upper right
    web_color = (B3[0], B3[1], B3[2], 140)
    # Top-left web
    for rad in [40, 80, 130, 180, 240]:
        for ang in range(0, 91, 5):
            rad_cur = rad + int(math.sin(ang * 0.1) * 4)
            wx = int(rad_cur * math.cos(math.radians(ang)))
            wy = int(rad_cur * math.sin(math.radians(ang)))
            if 0 <= wx < 960 and 0 <= wy < 540:
                c.set_pixel(wx, wy, web_color)
    # Radial spokes
    for ang in [15, 30, 45, 60, 75]:
        c.line(0, 0, int(260 * math.cos(math.radians(ang))), int(260 * math.sin(math.radians(ang))), web_color)

    # Floating cellar dust motes (hard alpha bands: 40, 90, 160, 240)
    motes = [
        (100, 120, 14, rgb_dust), (240, 220, 18, rgb_slate),
        (380, 90, 12, rgb_dust), (510, 310, 20, rgb_slate),
        (650, 160, 16, rgb_dust), (790, 260, 14, rgb_slate),
        (880, 110, 18, rgb_dust), (300, 420, 12, rgb_dust),
        (720, 430, 16, rgb_slate), (440, 480, 14, rgb_dust),
    ]
    for cx, cy, r, rgb in motes:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if 0 <= x < 960 and 0 <= y < 540:
                    d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    if d <= r:
                        if d > r * 0.75:
                            a = 40
                        elif d > r * 0.50:
                            a = 90
                        elif d > r * 0.25:
                            a = 160
                        else:
                            a = 240
                        cur_a = c.get_pixel(x, y)[3]
                        if a > cur_a:
                            c.set_pixel(x, y, (rgb[0], rgb[1], rgb[2], a))

    return c


# --- 2. Tileset & Obstacles ---

def generate_basement_tileset_floor() -> PixelCanvas:
    """256x96 px (8x3 32px tiles): Cracked concrete slab with fractures, oil stains, drain grates.
    Row 0: Surface (plain 0,1; left pit 2; right pit 3; hairline fractures 4; oil stain 5; drain grate 6; embedded bolt 7)
    Row 1: Concrete structural fill
    Row 2: Dark subterranean void
    """
    sheet = PixelCanvas(256, 96, TRANSPARENT)

    # Base surface tile (Tile 0)
    def make_base_surface() -> PixelCanvas:
        t = PixelCanvas(32, 32, B1)
        # Top bevel lip
        t.line(0, 0, 31, 0, B4)
        t.line(0, 1, 31, 1, B3)
        t.line(0, 2, 31, 2, B2)
        # Concrete aggregate speckles
        for sx, sy in [(5, 8), (14, 19), (22, 11), (27, 25), (9, 26), (18, 6)]:
            t.set_pixel(sx, sy, B0)
            t.set_pixel((sx + 1) % 32, sy, B3)
        return t

    # Base fill tile (Row 1)
    def make_base_fill() -> PixelCanvas:
        t = PixelCanvas(32, 32, B0)
        # Gravel bits and concrete fill
        for fx, fy, col in [(6, 6, B1), (18, 12, B2), (25, 20, B1), (10, 24, B2), (20, 28, B11)]:
            t.rect(fx, fy, 3, 3, col, outline=B5)
        return t

    # Base deep void tile (Row 2)
    def make_base_void() -> PixelCanvas:
        t = PixelCanvas(32, 32, VOID_BLACK)
        t.line(0, 0, 31, 0, B5)
        t.line(0, 1, 31, 1, B0)
        return t

    # --- ROW 0: SURFACE TILES ---
    # Tile 0: Plain concrete
    t0 = make_base_surface()
    sheet.blit(t0, 0, 0)

    # Tile 1: Expansion joint seam at x=16
    t1 = t0.clone()
    t1.line(15, 0, 15, 31, B0)
    t1.line(16, 0, 16, 31, B5)
    t1.line(17, 0, 17, 31, B3)
    sheet.blit(t1, 32, 0)

    # Tile 2: Left cliff edge facing pit
    t2 = t0.clone()
    t2.line(0, 0, 0, 31, B5)
    t2.line(1, 0, 1, 31, B0)
    t2.set_pixel(0, 0, B4)
    t2.set_pixel(1, 0, B4)
    # Rebar tip sticking out into pit
    t2.rect(0, 14, 4, 3, B7, outline=B6)
    sheet.blit(t2, 64, 0)

    # Tile 3: Right cliff edge facing pit
    t3 = t0.clone()
    t3.line(31, 0, 31, 31, B5)
    t3.line(30, 0, 30, 31, B0)
    t3.set_pixel(31, 0, B4)
    sheet.blit(t3, 96, 0)

    # Tile 4: Hairline fractures
    t4 = t0.clone()
    # Spiderweb crack pattern
    t4.line(6, 2, 12, 10, B5)
    t4.line(12, 10, 18, 8, B5)
    t4.line(12, 10, 14, 22, B5)
    t4.line(14, 22, 24, 26, B5)
    # Highlight next to crack
    t4.line(7, 2, 13, 10, B4)
    sheet.blit(t4, 128, 0)

    # Tile 5: Oil stain (iridescent purple/black)
    t5 = t0.clone()
    t5.circle(16, 16, 8, B14)
    t5.circle(16, 16, 5, B0)
    t5.circle(17, 15, 2, B11)
    sheet.blit(t5, 160, 0)

    # Tile 6: Embedded cast-iron drain grate
    t6 = t0.clone()
    t6.rect(4, 4, 24, 24, B5, outline=B0)
    t6.line(4, 4, 27, 4, B3)
    # Grate slots
    for gy in range(8, 26, 4):
        t6.line(7, gy, 24, gy, VOID_BLACK)
        t6.line(7, gy + 1, 24, gy + 1, METAL_MID)
    sheet.blit(t6, 192, 0)

    # Tile 7: Embedded rusty bolt & washer
    t7 = t0.clone()
    t7.circle(16, 14, 5, B6, outline=B5)
    t7.circle(16, 14, 2, B8)
    t7.line(15, 14, 17, 14, B10)
    sheet.blit(t7, 224, 0)

    # --- ROW 1: CONCRETE FILL TILES ---
    for c_idx in range(8):
        tf = make_base_fill()
        if c_idx == 2:
            # Left pit edge fill
            tf.line(0, 0, 0, 31, B5)
        elif c_idx == 3:
            # Right pit edge fill
            tf.line(31, 0, 31, 31, B5)
        elif c_idx == 4:
            # Embedded diagonal rebar rod
            tf.line(4, 4, 28, 28, B7)
            tf.line(5, 4, 29, 28, B6)
        sheet.blit(tf, c_idx * 32, 32)

    # --- ROW 2: DEEP SUBTERRANEAN VOID TILES ---
    for c_idx in range(8):
        tv = make_base_void()
        sheet.blit(tv, c_idx * 32, 64)

    return sheet


def generate_basement_pit_bg() -> PixelCanvas:
    """32x128 px: Sub-basement pit interior, rusty rebar, sewer pipe, dripping moisture."""
    c = PixelCanvas(32, 128, B0)

    # Vertical damp stains & concrete wall seams
    c.line(0, 0, 0, 127, B5)
    c.line(31, 0, 31, 127, B5)
    c.line(10, 0, 10, 127, B1)

    # Corrugated large sewer/drain pipe crossing horizontally (y=40..70)
    c.rect(0, 42, 32, 28, B5)
    c.rect(0, 44, 32, 24, B7)
    c.line(0, 44, 31, 44, B8)
    c.line(0, 67, 31, 67, B6)
    # Corrugation ribs
    for rx in range(4, 32, 6):
        c.line(rx, 42, rx, 69, B8)
        c.line(rx + 1, 42, rx + 1, 69, B5)

    # Exposed rusty iron rebar protruding diagonally (y=15..35)
    c.line(2, 18, 22, 34, B6)
    c.line(3, 18, 23, 34, B8)
    c.line(22, 34, 26, 36, B7)

    # Dripping water trickles (y=72..120)
    c.line(16, 70, 16, 110, B12)
    c.line(17, 70, 17, 100, B13)
    c.set_pixel(16, 112, B13)

    # Deep darkness at bottom
    c.rect(0, 108, 32, 20, VOID_BLACK)

    return c


def generate_basement_obstacles() -> List[PixelCanvas]:
    """128x32 px total (4 frames 32x32): 4 stackable obstacle block skins:
    0: Paint cans
    1: Taped cardboard moving boxes
    2: Cinder blocks
    3: Stack of old tires
    """
    frames = []

    # 0: Paint cans (stacked pair)
    c0 = PixelCanvas(32, 32, TRANSPARENT)
    for cy in [0, 16]:
        c0.rect(4, cy, 24, 16, METAL_MID, outline=B5)
        c0.line(4, cy, 27, cy, WHITE_MID)
        c0.rect(6, cy + 5, 20, 6, RED_MID if cy == 0 else BLUE_MID)
        # Wire handle across can
        c0.line(4, cy + 2, 16, cy + 6, B5)
        c0.line(16, cy + 6, 27, cy + 2, B5)
    frames.append(c0)

    # 1: Taped cardboard moving box
    c1 = PixelCanvas(32, 32, TRANSPARENT)
    c1.rect(2, 2, 28, 28, BROWN_MID, outline=B5)
    c1.line(2, 2, 29, 2, WOOD_HIGHLIGHT)
    c1.line(2, 2, 2, 29, WOOD_HIGHLIGHT)
    # Heavy tan packing tape sealing across horizontal & vertical center
    c1.rect(2, 14, 28, 5, WOOD_LIT, outline=B5)
    c1.rect(13, 2, 5, 28, WOOD_LIT, outline=B5)
    # Shipping label sticker
    c1.rect(5, 5, 6, 6, WHITE_SHADOW)
    c1.line(6, 7, 9, 7, B5)
    c1.line(6, 9, 8, 9, B5)
    frames.append(c1)

    # 2: Cinder block (two rectangular cores)
    c2 = PixelCanvas(32, 32, TRANSPARENT)
    c2.rect(2, 4, 28, 24, B2, outline=B5)
    c2.line(2, 4, 29, 4, B4)
    # Two core holes
    c2.rect(6, 9, 8, 14, B5, outline=B0)
    c2.rect(18, 9, 8, 14, B5, outline=B0)
    c2.line(6, 22, 13, 22, B3)
    c2.line(18, 22, 25, 22, B3)
    frames.append(c2)

    # 3: Stack of old tires
    c3 = PixelCanvas(32, 32, TRANSPARENT)
    for ty in [2, 17]:
        c3.rect(3, ty, 26, 13, VOID_BLACK, outline=B5)
        c3.line(3, ty, 28, ty, B1)
        # Tread grooves
        for gx in range(6, 26, 4):
            c3.line(gx, ty + 1, gx, ty + 11, B5)
    frames.append(c3)

    return frames


def generate_basement_obstacles_tall() -> List[PixelCanvas]:
    """128x32 px total (4 frames 32x32): Cap variants for tall stack:
    0: Paint can handle & open lid
    1: Cardboard box with open flap
    2: Cinder block with rebar sticking up
    3: Tire with wheel rim
    """
    frames = []

    # 0: Paint can cap (top can with bail handle up & lid)
    c0 = PixelCanvas(32, 32, TRANSPARENT)
    c0.rect(4, 12, 24, 20, METAL_MID, outline=B5)
    c0.line(4, 12, 27, 12, WHITE_MID)
    c0.rect(6, 18, 20, 8, RED_MID)
    # Upright wire bail handle
    c0.line(4, 14, 16, 2, B5)
    c0.line(16, 2, 27, 14, B5)
    c0.rect(13, 1, 6, 3, WOOD_LIT, outline=B5)
    frames.append(c0)

    # 1: Box with open top flap
    c1 = PixelCanvas(32, 32, TRANSPARENT)
    c1.rect(2, 10, 28, 22, BROWN_MID, outline=B5)
    c1.line(2, 10, 29, 10, WOOD_HIGHLIGHT)
    # Open flap angling upwards on left
    c1.line(2, 10, 10, 1, WOOD_LIT)
    c1.line(10, 1, 16, 1, WOOD_LIT)
    c1.line(16, 1, 16, 10, B5)
    # Flap interior shadow
    for y in range(2, 10):
        c1.line(7, y, 15, y, BROWN_DARK)
    frames.append(c1)

    # 2: Cinder block with rebar sticking up
    c2 = PixelCanvas(32, 32, TRANSPARENT)
    c2.rect(2, 10, 28, 22, B2, outline=B5)
    c2.line(2, 10, 29, 10, B4)
    c2.rect(6, 14, 8, 14, B5, outline=B0)
    c2.rect(18, 14, 8, 14, B5, outline=B0)
    # Rebar rod extending upward out of left core
    c2.rect(9, 1, 3, 16, B7, outline=B5)
    c2.line(10, 1, 10, 16, B8)
    frames.append(c2)

    # 3: Tire with wheel rim
    c3 = PixelCanvas(32, 32, TRANSPARENT)
    c3.rect(3, 10, 26, 22, VOID_BLACK, outline=B5)
    c3.line(3, 10, 28, 10, B1)
    # Wheel hub & rim
    c3.circle(16, 21, 8, METAL_MID, outline=B5)
    c3.circle(16, 21, 3, B5)
    for ang in [0, 90, 180, 270]:
        rad = math.radians(ang)
        c3.set_pixel(int(16 + 5 * math.cos(rad)), int(21 + 5 * math.sin(rad)), WHITE_MID)
    frames.append(c3)

    return frames


# --- 3. Goal Gate ---

def generate_basement_goal() -> List[PixelCanvas]:
    """384x128 px total (6 frames of 64x128 @ 10 fps):
    Hanging pull-chain industrial light bulb on brass fixture switching on with bright radiance.
    """
    frames = []
    cx = 32

    for f_idx in range(6):
        c = PixelCanvas(64, 128, TRANSPARENT)

        # Overhead iron pipe & ceiling junction box (y=0..16)
        c.rect(0, 4, 64, 8, B5)
        c.line(0, 4, 63, 4, B3)
        c.rect(cx - 10, 0, 20, 14, B5, outline=B0)

        # Hanging electrical cord / brass conduit down to fixture (y=14..40)
        c.line(cx, 14, cx, 40, B5)
        c.line(cx + 1, 14, cx + 1, 40, B8)

        # Brass fixture socket (y=40..54)
        c.rect(cx - 8, 40, 16, 14, B8, outline=B5)
        c.line(cx - 8, 40, cx + 7, 40, B10)

        # Beaded pull-chain hanging on right side
        chain_pull = 4 if f_idx in [1, 2] else 0
        chain_bottom = 78 + chain_pull
        for cy in range(48, chain_bottom, 3):
            c.set_pixel(cx + 9, cy, B10 if f_idx >= 2 else METAL_MID)
        # Pull bell / acorn
        c.circle(cx + 9, chain_bottom + 2, 2, B8, outline=B5)

        # Bulb state
        by = 64
        if f_idx == 0:
            # Off / dark filament
            c.circle(cx, by, 12, B1, outline=B5)
            c.line(cx - 3, by, cx, by - 4, B6)
            c.line(cx, by - 4, cx + 3, by, B6)
        elif f_idx == 1:
            # Warm click / switch begins
            c.circle(cx, by, 12, B2, outline=B5)
            c.line(cx - 3, by, cx, by - 4, B8)
            c.line(cx, by - 4, cx + 3, by, B9)
        elif f_idx == 2:
            # Spark / ignition
            c.circle(cx, by, 14, B9, outline=B8)
            c.circle(cx, by, 8, B10)
            c.circle(cx, by, 4, PURE_WHITE)
        else:
            # Full brilliant glow (f_idx 3, 4, 5)
            glow_r = 26 + (f_idx - 3) * 4
            # Radiance rings
            c.circle(cx, by, glow_r, B0)
            c.circle(cx, by, int(glow_r * 0.75), B8)
            c.circle(cx, by, int(glow_r * 0.5), B9)
            c.circle(cx, by, 14, B10)
            c.circle(cx, by, 8, PURE_WHITE)
            # Radiant light rays extending outward
            for ang in range(0, 360, 45):
                rad = math.radians(ang + (f_idx * 15))
                rx1 = int(cx + 16 * math.cos(rad))
                ry1 = int(by + 16 * math.sin(rad))
                rx2 = int(cx + (glow_r + 6) * math.cos(rad))
                ry2 = int(by + (glow_r + 6) * math.sin(rad))
                c.line(rx1, ry1, rx2, ry2, B10)

        # Floor stand / baseboard silhouette at bottom (y=112..128)
        c.rect(cx - 16, 120, 32, 8, B5, outline=VOID_BLACK)
        c.line(cx - 16, 120, cx + 15, 120, B3)

        frames.append(c)

    return frames


# --- 4. Floor Clutter (10 items + shadows) ---

def generate_basement_clutter() -> List[Tuple[str, PixelCanvas, PixelCanvas]]:
    """Returns list of (item_name, item_canvas, shadow_canvas)."""
    items = []

    # 1. screw (20x16)
    c1 = PixelCanvas(20, 16, TRANSPARENT)
    # Head on left, threaded shaft to right
    c1.rect(2, 6, 4, 6, METAL_MID, outline=OUTLINE)
    c1.line(6, 8, 16, 8, METAL_SHADOW)
    # Threads
    for tx in range(7, 16, 2):
        c1.line(tx, 7, tx + 1, 10, METAL_MID)
    c1.set_pixel(17, 8, METAL_MID) # tip
    s1 = make_shadow(20, 16, 10, 12, 7, 2)
    items.append(("basement_deco_screw", c1, s1))

    # 2. nail (24x16)
    c2 = PixelCanvas(24, 16, TRANSPARENT)
    c2.rect(2, 6, 3, 5, B6, outline=OUTLINE) # flat nail head
    c2.line(5, 8, 20, 8, B7)
    c2.line(5, 7, 18, 7, B8) # top highlight
    c2.set_pixel(21, 8, B6) # point
    s2 = make_shadow(24, 16, 12, 11, 9, 2)
    items.append(("basement_deco_nail", c2, s2))

    # 3. bolt (24x20)
    c3 = PixelCanvas(24, 20, TRANSPARENT)
    # Hex head
    c3.rect(2, 5, 6, 10, METAL_MID, outline=OUTLINE)
    c3.line(2, 5, 7, 5, WHITE_MID)
    # Threaded shaft
    c3.rect(8, 7, 13, 6, METAL_SHADOW, outline=OUTLINE)
    for bx in range(9, 21, 3):
        c3.line(bx, 7, bx, 12, METAL_MID)
    s3 = make_shadow(24, 20, 12, 14, 9, 3)
    items.append(("basement_deco_bolt", c3, s3))

    # 4. rag (32x20)
    c4 = PixelCanvas(32, 20, TRANSPARENT)
    # Oily shop rag crumpled
    c4.rect(6, 6, 20, 10, RED_SHADOW, outline=OUTLINE)
    c4.circle(12, 9, 5, RED_MID)
    c4.circle(20, 11, 4, RED_DEEP)
    # Dark oil smudge on rag
    c4.rect(14, 8, 5, 4, B14)
    s4 = make_shadow(32, 20, 16, 14, 12, 4)
    items.append(("basement_deco_rag", c4, s4))

    # 5. flashlight (36x20)
    c5 = PixelCanvas(36, 20, TRANSPARENT)
    # Heavy rubberized barrel
    c5.rect(8, 6, 20, 8, YELLOW_MID, outline=OUTLINE)
    c5.line(8, 6, 27, 6, YELLOW_HIGHLIGHT)
    # Ribbed grip
    for gx in range(12, 24, 3):
        c5.line(gx, 7, gx, 13, B5)
    # Beveled lens bezel on left
    c5.rect(2, 4, 6, 12, B5, outline=OUTLINE)
    c5.line(2, 5, 2, 15, B2) # unlit lens
    # Switch on top
    c5.rect(16, 4, 5, 2, RED_MID)
    s5 = make_shadow(36, 20, 18, 14, 14, 3)
    items.append(("basement_deco_flashlight", c5, s5))

    # 6. crumpled_blueprint (36x24)
    c6 = PixelCanvas(36, 24, TRANSPARENT)
    # Blue paper folded and wrinkled
    c6.rect(4, 5, 28, 14, BLUE_MID, outline=OUTLINE)
    c6.line(4, 5, 31, 5, BLUE_LIGHT)
    c6.line(4, 5, 4, 18, BLUE_LIGHT)
    # Folds & white draft lines
    c6.line(10, 8, 26, 8, WHITE_SHADOW)
    c6.line(16, 8, 16, 15, WHITE_SHADOW)
    c6.line(6, 12, 12, 17, BLUE_SHADOW)
    c6.line(20, 10, 28, 16, BLUE_SHADOW)
    s6 = make_shadow(36, 24, 18, 17, 14, 4)
    items.append(("basement_deco_crumpled_blueprint", c6, s6))

    # 7. rusty_key (24x16)
    c7 = PixelCanvas(24, 16, TRANSPARENT)
    # Bow (handle ring) on left
    c7.circle(5, 8, 4, B8, outline=OUTLINE)
    c7.set_pixel(5, 8, TRANSPARENT)
    # Shaft to right
    c7.line(9, 8, 20, 8, B7)
    c7.line(9, 7, 19, 7, B8)
    # Bit (teeth) on right
    c7.rect(17, 9, 3, 4, B6, outline=OUTLINE)
    c7.set_pixel(18, 11, TRANSPARENT)
    s7 = make_shadow(24, 16, 12, 12, 9, 2)
    items.append(("basement_deco_rusty_key", c7, s7))

    # 8. jar_of_nails (24x32)
    c8 = PixelCanvas(24, 32, TRANSPARENT)
    # Glass jar body
    c8.rect(4, 8, 16, 22, B11, outline=OUTLINE)
    c8.rect(5, 9, 14, 20, B0)
    # Glass highlight
    c8.line(6, 10, 6, 28, WHITE_SHADOW)
    # Metal lid
    c8.rect(5, 4, 14, 4, METAL_MID, outline=OUTLINE)
    c8.line(5, 4, 18, 4, WHITE_MID)
    # Nails inside jar
    for ny in range(16, 28, 3):
        c8.line(7, ny, 16, ny + 2, METAL_MID)
        c8.set_pixel(17, ny + 2, B6)
    s8 = make_shadow(24, 32, 12, 29, 9, 3)
    items.append(("basement_deco_jar_of_nails", c8, s8))

    # 9. mouse_trap (32x20)
    c9 = PixelCanvas(32, 20, TRANSPARENT)
    # Wood base
    c9.rect(3, 8, 26, 8, WOOD_LIT, outline=OUTLINE)
    c9.line(3, 8, 28, 8, WOOD_HIGHLIGHT)
    # Copper spring coil in center
    c9.rect(13, 6, 6, 6, B8, outline=OUTLINE)
    # Sprung wire bail flat on wood
    c9.line(6, 10, 20, 10, METAL_MID)
    c9.line(20, 10, 26, 14, METAL_MID)
    s9 = make_shadow(32, 20, 16, 15, 13, 3)
    items.append(("basement_deco_mouse_trap", c9, s9))

    # 10. sawdust (32x16)
    c10 = PixelCanvas(32, 16, TRANSPARENT)
    # Small pile of sawdust
    c10.circle(16, 11, 7, B15)
    c10.circle(12, 12, 5, B15)
    c10.circle(20, 12, 5, B15)
    # Amber wood shavings
    for px, py in [(14, 7), (17, 8), (11, 10), (21, 9), (16, 11), (9, 13), (23, 12)]:
        c10.set_pixel(px, py, WOOD_LIT)
    s10 = make_shadow(32, 16, 16, 13, 11, 2)
    items.append(("basement_deco_sawdust", c10, s10))

    return items


# --- 5. Animated Props (6 props) ---

def generate_basement_prop_bulb() -> List[PixelCanvas]:
    """64x96 px, 10 frames @ 6 fps: Swinging bare incandescent bulb with swinging light cone."""
    frames = []
    # Pendulum swing angles
    angles = [-8, -6, -3, 0, 3, 6, 8, 6, 3, 0]

    for ang_deg in angles:
        c = PixelCanvas(64, 96, TRANSPARENT)
        rad = math.radians(ang_deg)

        # Hanging pivot at top center (32, 0)
        px, py = 32, 0
        arm_len = 46
        bx = int(px + arm_len * math.sin(rad))
        by = int(py + arm_len * math.cos(rad))

        # Cord
        c.line(px, py, bx, by - 8, B5)
        # Socket fixture
        c.rect(bx - 3, by - 8, 7, 6, B8, outline=B5)

        # Swinging light cone behind bulb (hard alpha or stepped tone)
        cone_left = int(bx + 40 * math.sin(rad - 0.4))
        cone_right = int(bx + 40 * math.sin(rad + 0.4))
        for ly in range(by + 8, 96):
            t = (ly - (by + 8)) / float(96 - (by + 8))
            span = int(10 + t * 24)
            x_mid = int(bx + (ly - by) * math.sin(rad))
            for x in range(x_mid - span, x_mid + span + 1):
                if 0 <= x < 64:
                    cur_col = c.get_pixel(x, ly)
                    if cur_col[3] == 0:
                        c.set_pixel(x, ly, B0 if t > 0.6 else B1)

        # Glass bulb
        c.circle(bx, by, 7, B10, outline=B5)
        c.circle(bx, by, 4, PURE_WHITE)

        frames.append(c)

    return frames


def generate_basement_prop_furnace() -> List[PixelCanvas]:
    """96x96 px, 8 frames @ 8 fps: Iron furnace with flickering fire glowing through grate."""
    frames = []

    for f_idx in range(8):
        c = PixelCanvas(96, 96, TRANSPARENT)

        # Cast iron furnace body (grounded on floor, bottom y=95)
        c.rect(14, 20, 68, 75, B5, outline=OUTLINE)
        c.rect(18, 24, 60, 68, B1)
        c.line(18, 24, 77, 24, B3)

        # Stove chimney pipe going up
        c.rect(38, 0, 20, 20, B5, outline=OUTLINE)
        c.line(38, 0, 38, 19, B3)

        # Arched door frame
        c.rect(26, 44, 44, 46, B5, outline=OUTLINE)
        c.rect(30, 48, 36, 38, VOID_BLACK)

        # Grate bars
        for gx in [38, 48, 58]:
            c.line(gx, 48, gx, 85, B5)

        # Flickering fire animation behind grate
        shift = int(math.sin(f_idx * 0.9) * 3)
        flame_h = 24 + (f_idx % 3) * 3
        c.rect(32, 85 - flame_h, 32, flame_h, B8)
        c.rect(36, 85 - int(flame_h * 0.75), 24, int(flame_h * 0.75), B9)
        c.rect(40 + shift, 85 - int(flame_h * 0.5), 16, int(flame_h * 0.5), B10)
        c.set_pixel(48 + shift, 85 - flame_h + 2, PURE_WHITE)

        # Door latch
        c.rect(70, 62, 4, 10, METAL_MID, outline=B5)

        frames.append(c)

    return frames


def generate_basement_prop_pipe_drip() -> List[PixelCanvas]:
    """48x80 px, 10 frames @ 10 fps: Copper pipe with forming drop and floor ripple puddle."""
    frames = []

    for f_idx in range(10):
        c = PixelCanvas(48, 80, TRANSPARENT)
        cx = 24

        # Overhead horizontal copper pipe at top (y=4..16)
        c.rect(0, 4, 48, 12, B7, outline=B5)
        c.line(0, 4, 47, 4, B8)
        c.line(0, 15, 47, 15, B6)
        # Pipe coupling joint in center
        c.rect(cx - 5, 2, 10, 16, B8, outline=B5)

        # Water droplet cycle:
        # F0..3: droplet forming at pipe bottom (y=18..24)
        # F4..6: droplet falling down (y=32..68)
        # F7..9: impact on floor ripple (y=72..78)
        if f_idx < 4:
            # Swelling drop
            drop_r = 1 + f_idx
            c.circle(cx, 18 + drop_r, drop_r, B13, outline=B12)
        elif f_idx < 7:
            # Falling drop
            dy = 28 + (f_idx - 4) * 16
            c.rect(cx - 1, dy, 3, 6, B13, outline=B12)
            c.set_pixel(cx, dy, PURE_WHITE)

        # Floor puddle & ripples (y=72..78)
        puddle_w = 12
        c.circle(cx, 75, puddle_w, B12, outline=B5)
        if f_idx >= 7:
            ripple_r = 4 + (f_idx - 7) * 4
            for rx in range(cx - ripple_r, cx + ripple_r + 1):
                dx = (rx - cx) / float(max(1, ripple_r))
                ry_val = int(75 + 3 * math.sqrt(max(0.0, 1.0 - dx * dx)))
                if 0 <= rx < 48 and 0 <= ry_val < 80:
                    c.set_pixel(rx, ry_val, B13)

        frames.append(c)

    return frames


def generate_basement_prop_washer() -> List[PixelCanvas]:
    """80x80 px, 8 frames @ 12 fps: Vintage washing machine rattling violently mid-spin-cycle."""
    frames = []

    for f_idx in range(8):
        c = PixelCanvas(80, 80, TRANSPARENT)

        # Vibration offset
        vx = 1 if f_idx % 2 == 0 else -1
        vy = -1 if (f_idx // 2) % 2 == 0 else 0
        wx = 10 + vx
        wy = 16 + vy

        # Motion blur shake lines on sides
        if f_idx % 2 == 0:
            c.line(wx - 3, wy + 20, wx - 3, wy + 50, B3)
            c.line(wx + 63, wy + 20, wx + 63, wy + 50, B3)

        # Machine chassis
        c.rect(wx, wy, 60, 62, WHITE_SHADOW, outline=B5)
        c.line(wx, wy, wx + 59, wy, PURE_WHITE)

        # Control panel top
        c.rect(wx, wy - 10, 60, 10, WHITE_MID, outline=B5)
        c.circle(wx + 15, wy - 5, 3, B5)
        c.circle(wx + 45, wy - 5, 3, RED_MID)

        # Rotating drum window
        rot_ang = f_idx * 45
        c.circle(wx + 30, wy + 32, 20, B5)
        c.circle(wx + 30, wy + 32, 17, METAL_MID)
        c.circle(wx + 30, wy + 32, 13, B12)
        # Clothes swirling inside
        spin_rad = math.radians(rot_ang)
        swx = int(wx + 30 + 7 * math.cos(spin_rad))
        swy = int(wy + 32 + 7 * math.sin(spin_rad))
        c.circle(swx, swy, 4, RED_MID)

        # Rubber feet on floor (grounded at y=79)
        c.rect(wx + 4, 76, 8, 4, B5)
        c.rect(wx + 48, 76, 8, 4, B5)

        frames.append(c)

    return frames


def generate_basement_prop_spider() -> List[PixelCanvas]:
    """32x80 px, 12 frames @ 8 fps: Basement spider lowering on silk thread and climbing back up."""
    frames = []
    # Drop heights
    heights = [15, 25, 38, 50, 60, 65, 65, 60, 50, 38, 25, 15]

    for f_idx, sy in enumerate(heights):
        c = PixelCanvas(32, 80, TRANSPARENT)
        cx = 16

        # Silk thread from top ceiling (y=0) to spider
        c.line(cx, 0, cx, sy - 4, WHITE_SHADOW)

        # Spider body (abdomen and cephalothorax)
        c.circle(cx, sy, 4, VOID_BLACK, outline=OUTLINE)
        c.circle(cx, sy + 4, 3, B5, outline=OUTLINE)
        # Red eyes
        c.set_pixel(cx - 1, sy + 5, RED_MID)
        c.set_pixel(cx + 1, sy + 5, RED_MID)

        # 8 Legs twitching/wiggling
        leg_wig = 1 if f_idx % 2 == 0 else -1
        # Left legs
        c.line(cx - 3, sy - 1, cx - 8, sy - 4 + leg_wig, OUTLINE)
        c.line(cx - 3, sy + 1, cx - 9, sy + 1, OUTLINE)
        c.line(cx - 3, sy + 3, cx - 8, sy + 5 - leg_wig, OUTLINE)
        c.line(cx - 2, sy + 5, cx - 6, sy + 8, OUTLINE)
        # Right legs
        c.line(cx + 3, sy - 1, cx + 8, sy - 4 - leg_wig, OUTLINE)
        c.line(cx + 3, sy + 1, cx + 9, sy + 1, OUTLINE)
        c.line(cx + 3, sy + 3, cx + 8, sy + 5 + leg_wig, OUTLINE)
        c.line(cx + 2, sy + 5, cx + 6, sy + 8, OUTLINE)

        frames.append(c)

    return frames


def generate_basement_prop_tv_static() -> List[PixelCanvas]:
    """80x64 px, 6 frames @ 12 fps: Old cathode-ray TV monitor displaying animated static snow."""
    frames = []

    for f_idx in range(6):
        c = PixelCanvas(80, 64, TRANSPARENT)

        # Wooden milk crate / stool stand (grounded at y=63)
        c.rect(16, 46, 48, 18, BROWN_DARK, outline=OUTLINE)
        c.line(16, 46, 63, 46, WOOD_LIT)

        # TV chassis (bulky retro CRT)
        c.rect(10, 8, 60, 38, B5, outline=OUTLINE)
        c.rect(12, 10, 56, 34, B0)
        c.line(10, 8, 69, 8, B3) # top rim

        # Antenna bunny ears on top
        c.line(26, 8, 18, 0, METAL_MID)
        c.line(54, 8, 62, 0, METAL_MID)

        # CRT curved glass screen
        c.rect(16, 14, 40, 26, VOID_BLACK, outline=OUTLINE)

        # Static snow pattern (animated pseudorandom pixels)
        for sy in range(15, 39):
            for sx in range(17, 55):
                # Hash function for crisp deterministic static per frame
                h = (sx * 37 + sy * 59 + f_idx * 101) % 13
                if h < 3:
                    c.set_pixel(sx, sy, PURE_WHITE)
                elif h < 6:
                    c.set_pixel(sx, sy, WHITE_MID)
                elif h < 9:
                    c.set_pixel(sx, sy, B3)
                else:
                    c.set_pixel(sx, sy, VOID_BLACK)

        # Knobs & speaker grille on right
        c.circle(62, 18, 3, METAL_MID, outline=B5)
        c.circle(62, 26, 3, METAL_MID, outline=B5)
        for gy in [33, 36, 39]:
            c.line(59, gy, 65, gy, B5)

        frames.append(c)

    return frames


# ==============================================================================
# ATTIC ASSETS
# ==============================================================================

# --- 1. Parallax Layers ---

def generate_attic_sky_gradient() -> PixelCanvas:
    """1x540 px: 8 hard color bands of dusty amber and moonlit indigo."""
    c = PixelCanvas(1, 540)
    bands = [
        (0, 68, VOID_BLACK),
        (68, 135, SHADOW_PURPLE_DARK),
        (135, 203, A15),
        (203, 270, A0),
        (270, 338, A1),
        (338, 405, A2),
        (405, 473, A3),
        (473, 540, A4),
    ]
    for y0, y1, col in bands:
        for y in range(y0, y1):
            c.set_pixel(0, y, col)
    return c


def generate_attic_bg_far() -> PixelCanvas:
    """960x540 px: Sloped wooden roof beams, round dormer window with moonlight,
    hanging clothes on wire, antique mirror. Floor at y=400.
    """
    c = PixelCanvas(960, 540, A0)

    # 1. Sloped wooden roof rafters and ceiling boards (y=0..400)
    # Horizontal lath wall boards
    for y in range(0, 400, 16):
        c.line(0, y, 959, y, A1)
        if y % 32 == 0:
            c.line(0, y + 1, 959, y + 1, A0)

    # Massive diagonal timber roof rafters peaking near top center (x=480, y=0)
    # Left slope
    for rx in range(0, 480):
        ry = int(rx * 0.7)
        if ry < 400:
            c.rect(rx, ry, 6, 20, A1, outline=A0)
            c.set_pixel(rx, ry, A4)
    # Right slope
    for rx in range(480, 960):
        ry = int((960 - rx) * 0.7)
        if ry < 400:
            c.rect(rx, ry, 6, 20, A1, outline=A0)
            c.set_pixel(rx, ry, A4)

    # Collar tie horizontal beam across center (y=120..136)
    c.rect(0, 120, 960, 16, A2, outline=A0)
    c.line(0, 120, 959, 120, A4)

    # Floor baseboard / floorboards (y=400..540)
    c.rect(0, 400, 960, 8, A0)
    c.line(0, 400, 959, 400, A3)
    for y in range(408, 540):
        c.line(0, y, 959, y, A1 if y % 28 == 0 else A0)

    # 2. Round Dormer Window with Moonlight (x=420..540, y=30..110)
    wx, wy = 480, 70
    c.circle(wx, wy, 38, A0)
    c.circle(wx, wy, 34, A4)
    c.circle(wx, wy, 30, A15) # moonlight glass
    # Window panes cross
    c.line(wx - 30, wy, wx + 30, wy, A0)
    c.line(wx, wy - 30, wx, wy + 30, A0)
    # Distant glowing crescent moon in window
    c.circle(wx + 8, wy - 8, 8, PURE_WHITE)
    c.circle(wx + 11, wy - 9, 7, A15)

    # 3. Hanging Clothesline with Old Garments on Wire (x=80..400, y=140..220)
    # Wire sagging across
    for wx_line in range(80, 400):
        t = (wx_line - 240) / 160.0
        wy_line = int(145 + t * t * 15)
        c.set_pixel(wx_line, wy_line, A8)
    # Hanging shirt (x=120..160)
    c.rect(125, 150, 30, 45, A10, outline=A0)
    c.line(125, 150, 154, 150, A11)
    # Hanging coat (x=200..260)
    c.rect(205, 155, 45, 60, A1, outline=A0)
    c.line(205, 155, 249, 155, A3)
    # Hanging dress (x=300..350)
    c.rect(305, 150, 35, 65, A8, outline=A0)

    # 4. Antique Oval Filigree Mirror (x=680..760, y=160..280)
    mx, my = 720, 220
    # Outer carved wooden frame
    for ay in range(my - 50, my + 51):
        dy = (ay - my) / 50.0
        if 1.0 - dy * dy >= 0:
            span = int(32 * math.sqrt(1.0 - dy * dy))
            c.line(mx - span - 4, ay, mx + span + 4, ay, A12)
            c.line(mx - span, ay, mx + span, ay, A15)
    # Dim reflection highlight
    c.line(mx - 15, my - 25, mx + 15, my - 25, WHITE_SHADOW)

    return c


def generate_attic_bg_far_anim() -> List[PixelCanvas]:
    """3840x540 px total (4 frames of 960x540 @ 3 fps):
    Moonlight beam shift through round window with twinkling dust specks.
    """
    frames = []
    wx, wy = 480, 70

    for f_idx in range(4):
        c = PixelCanvas(960, 540, TRANSPARENT)

        # Angled moonlight beam spreading downwards from window
        beam_shift = int(math.sin(f_idx * 1.5) * 4)
        for by in range(wy + 20, 480):
            t = (by - (wy + 20)) / 400.0
            span = int(25 + t * 90)
            bx_mid = int(wx + t * 140 + beam_shift)
            for x in range(bx_mid - span, bx_mid + span + 1):
                if 0 <= x < 960:
                    dist_center = abs(x - bx_mid) / float(span)
                    if dist_center < 0.4:
                        c.set_pixel(x, by, A15)
                    elif dist_center < 0.8:
                        c.set_pixel(x, by, A8)

        # Floating dust specks twinkling inside the beam
        specks = [
            (500, 160), (540, 220), (580, 290), (620, 360),
            (520, 240), (560, 180), (610, 310), (650, 420),
            (490, 190), (570, 340), (630, 260), (670, 390)
        ]
        for idx, (sx, sy) in enumerate(specks):
            sx_dyn = sx + beam_shift + int(math.sin((f_idx + idx) * 0.8) * 3)
            sy_dyn = sy + int(math.cos((f_idx + idx) * 0.8) * 2)
            if (f_idx + idx) % 2 == 0:
                c.set_pixel(sx_dyn, sy_dyn, PURE_WHITE)
            else:
                c.set_pixel(sx_dyn, sy_dyn, A5)

        frames.append(c)

    return frames


def generate_attic_bg_mid() -> PixelCanvas:
    """1280x540 px: Seamless left/right mid layer, floor at y=400.
    White sheet-covered furniture, steamer trunks, hat boxes,
    old dress form, rocking chair.
    """
    c = PixelCanvas(1280, 540, TRANSPARENT)

    # Seamless background timber wall between items
    for y in range(80, 400):
        col = A1 if y % 24 < 2 else A0
        c.line(0, y, 1279, y, col)

    # Floor baseboard and worn floorboards (y=400..540)
    c.rect(0, 400, 1280, 8, A0)
    c.line(0, 400, 1279, 400, A4)
    for y in range(408, 540):
        c.line(0, y, 1279, y, A2 if y % 32 == 0 else A1)
    # Board butt joints every 160 px (seamless!)
    for bx in range(0, 1280, 160):
        c.line(bx, 408, bx, 539, A0)

    # -------------------------------------------------------------------------
    # 1. White Sheet-Covered Armchair (x=90..240, y=240..400)
    # -------------------------------------------------------------------------
    cx0, cy0 = 100, 250
    # Sculpted draped sheet silhouette
    c.rect(cx0, cy0 + 30, 130, 120, WHITE_SHADOW, outline=A0)
    c.circle(cx0 + 65, cy0 + 30, 40, WHITE_SHADOW)
    # Sheet folds and highlights
    c.line(cx0, cy0 + 30, cx0 + 129, cy0 + 30, PURE_WHITE)
    for fold_x in [cx0 + 30, cx0 + 65, cx0 + 100]:
        c.line(fold_x, cy0 + 30, fold_x - 5, cy0 + 145, WHITE_MID)
        c.line(fold_x + 1, cy0 + 30, fold_x - 4, cy0 + 145, A8)

    # -------------------------------------------------------------------------
    # 2. Brass-Bound Steamer Trunks (x=330..520, y=260..400)
    # -------------------------------------------------------------------------
    tx0, ty0 = 350, 270
    # Lower large trunk
    c.rect(tx0, ty0 + 50, 150, 80, A2, outline=A0)
    c.line(tx0, ty0 + 50, tx0 + 149, ty0 + 50, A4)
    # Brass reinforcing bands
    for bx in [tx0 + 15, tx0 + 75, tx0 + 135]:
        c.rect(bx, ty0 + 50, 8, 80, A13, outline=A0)
        c.line(bx, ty0 + 50, bx + 7, ty0 + 50, A14)
    # Brass center latch & lock
    c.rect(tx0 + 70, ty0 + 75, 18, 22, A14, outline=A0)
    # Smaller trunk stacked on top
    c.rect(tx0 + 20, ty0, 110, 50, A1, outline=A0)
    c.line(tx0 + 20, ty0, tx0 + 129, ty0, A3)
    c.rect(tx0 + 68, ty0 + 18, 14, 16, A13, outline=A0)

    # -------------------------------------------------------------------------
    # 3. Stacked Round Vintage Hat Boxes (x=600..720, y=260..400)
    # -------------------------------------------------------------------------
    hx0, hy0 = 620, 270
    # Bottom large hat box
    c.rect(hx0, hy0 + 65, 80, 65, A10, outline=A0)
    c.circle(hx0 + 40, hy0 + 65, 40, A11)
    # Middle hat box (striped)
    c.rect(hx0 + 10, hy0 + 30, 60, 35, A8, outline=A0)
    for sx in range(hx0 + 15, hx0 + 65, 8):
        c.line(sx, hy0 + 30, sx, hy0 + 64, A10)
    # Top small hat box
    c.rect(hx0 + 20, hy0, 40, 30, A9, outline=A0)
    c.line(hx0 + 20, hy0, hx0 + 59, hy0, PURE_WHITE)

    # -------------------------------------------------------------------------
    # 4. Antique Dress Form on Wooden Stand (x=780..880, y=190..400)
    # -------------------------------------------------------------------------
    dx0, dy0 = 820, 200
    # Torso
    c.rect(dx0 - 15, dy0, 30, 75, A8, outline=A0)
    c.line(dx0 - 15, dy0, dx0 + 14, dy0, A9)
    # Contoured waist & hips
    c.circle(dx0, dy0 + 18, 14, A8)
    c.circle(dx0, dy0 + 55, 17, A8)
    # Turned wooden stand pole
    c.rect(dx0 - 3, dy0 + 75, 6, 115, A2, outline=A0)
    # Tripod base feet (grounded at y=400)
    c.line(dx0, dy0 + 180, dx0 - 24, 399, A1)
    c.line(dx0, dy0 + 180, dx0 + 24, 399, A1)

    # -------------------------------------------------------------------------
    # 5. Carved Antique Rocking Chair (x=960..1110, y=230..400)
    # -------------------------------------------------------------------------
    rx0, ry0 = 980, 240
    # Spindle back
    c.line(rx0 + 10, ry0, rx0 + 10, ry0 + 80, A3)
    c.line(rx0 + 40, ry0, rx0 + 40, ry0 + 80, A3)
    for sp_x in range(rx0 + 16, rx0 + 38, 5):
        c.line(sp_x, ry0 + 10, sp_x, ry0 + 80, A2)
    # Seat
    c.rect(rx0 + 5, ry0 + 80, 55, 10, A3, outline=A0)
    # Turned legs
    c.line(rx0 + 12, ry0 + 90, rx0 + 8, ry0 + 150, A2)
    c.line(rx0 + 52, ry0 + 90, rx0 + 56, ry0 + 150, A2)
    # Curved rockers touching floor (grounded at y=400)
    for rkx in range(rx0, rx0 + 75):
        t = (rkx - (rx0 + 37)) / 37.0
        rky = int(395 + t * t * 4)
        c.set_pixel(rkx, rky, A4)

    return c


def generate_attic_bg_near() -> PixelCanvas:
    """960x540 px: Silhouettes layer.
    STRICT: 100% transparent above floor line y=400 (y=0..399 is transparent!).
    Dark silhouettes of phonograph horn, spinning wheel, dress form with 1px warm rim light.
    """
    c = PixelCanvas(960, 540, TRANSPARENT)
    BODY = VOID_BLACK
    RIM = A5  # Warm golden amber 1px rim light

    # 1. Antique Phonograph / Gramophone with flared horn (x=70..210, y=405..535)
    px0, py0 = 90, 420
    # Horn flared bell silhouette
    for hy in range(py0, py0 + 75):
        t = (hy - py0) / 75.0
        hw = int(45 * (1.0 - t * 0.7))
        c.line(px0 + 50 - hw, hy, px0 + 50 + hw, hy, BODY)
        c.set_pixel(px0 + 50 - hw, hy, RIM)
    # Square wooden cabinet base
    c.rect(px0 + 30, py0 + 75, 55, 40, BODY)
    c.line(px0 + 30, py0 + 75, px0 + 84, py0 + 75, RIM)
    c.line(px0 + 30, py0 + 75, px0 + 30, py0 + 114, RIM)

    # 2. Old wooden spinning wheel (x=410..560, y=405..535)
    sx0, sy0 = 470, 450
    # Large wheel rim
    c.circle(sx0, sy0, 42, BODY, outline=BODY)
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        c.line(sx0, sy0, int(sx0 + 40 * math.cos(rad)), int(sy0 + 40 * math.sin(rad)), BODY)
    # Rim light on upper left curve of wheel
    for ang in range(120, 240, 5):
        rad = math.radians(ang)
        c.set_pixel(int(sx0 + 42 * math.cos(rad)), int(sy0 + 42 * math.sin(rad)), RIM)
    # Spindle table & slanted legs
    c.rect(sx0 - 45, sy0 + 30, 90, 12, BODY)
    c.line(sx0 - 45, sy0 + 30, sx0 + 44, sy0 + 30, RIM)

    # 3. Victorian dress form silhouette on tripod stand (x=740..870, y=402..535)
    dx0, dy0 = 800, 410
    # Silhouette torso
    c.circle(dx0, dy0 + 25, 26, BODY)
    c.circle(dx0, dy0 + 65, 32, BODY)
    # Stand pole
    c.rect(dx0 - 4, dy0 + 90, 8, 38, BODY)
    # Rim light on left contour
    c.line(dx0 - 26, dy0 + 15, dx0 - 26, dy0 + 35, RIM)
    c.line(dx0 - 32, dy0 + 55, dx0 - 32, dy0 + 75, RIM)

    return c


def generate_attic_fg_legs() -> PixelCanvas:
    """960x540 px: Diagonal attic roof rafters and hanging light cord."""
    c = PixelCanvas(960, 540, TRANSPARENT)
    SIL = VOID_BLACK
    RIM = A4

    # Heavy sloped timber rafter on top-left (x=0..220, y=0..260)
    for y in range(0, 260):
        rx = int(220 - y * 0.85)
        c.rect(0, y, rx, 1, SIL)
        c.set_pixel(rx, y, RIM)

    # Heavy sloped timber rafter on top-right (x=740..960, y=0..260)
    for y in range(0, 260):
        rx = int(740 + y * 0.85)
        c.rect(rx, y, 960 - rx, 1, SIL)
        c.set_pixel(rx, y, RIM)

    # Hanging braided pull cord with brass tassel (x=480, y=0..180)
    c.line(480, 0, 480, 170, SIL)
    c.line(479, 0, 479, 170, RIM)
    # Tassel
    c.circle(480, 175, 4, SIL)
    c.set_pixel(478, 173, A5)

    return c


def generate_attic_fg_dust() -> PixelCanvas:
    """960x540 px: Floating attic wool fibers and dust bunny specks (hard-banded alpha)."""
    c = PixelCanvas(960, 540, TRANSPARENT)
    rgb_dust = A8[:3]
    rgb_amber = A5[:3]

    # Curved wool fibers
    for fx0, fy0, length in [(120, 140, 25), (320, 280, 30), (600, 110, 20), (840, 340, 28), (450, 420, 22)]:
        fiber_col = (A8[0], A8[1], A8[2], 160)
        for i in range(length):
            fx = int(fx0 + i + math.sin(i * 0.3) * 4)
            fy = int(fy0 + i * 0.5 + math.cos(i * 0.3) * 3)
            if 0 <= fx < 960 and 0 <= fy < 540:
                c.set_pixel(fx, fy, fiber_col)

    # Soft round dust bunny motes (hard alpha bands: 40, 80, 150, 240)
    motes = [
        (80, 80, 16, rgb_dust), (220, 360, 22, rgb_amber),
        (360, 180, 14, rgb_dust), (520, 90, 18, rgb_amber),
        (680, 320, 20, rgb_dust), (820, 160, 15, rgb_amber),
        (920, 410, 18, rgb_dust), (410, 460, 12, rgb_dust),
    ]
    for cx, cy, r, rgb in motes:
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
                            a = 240
                        cur_a = c.get_pixel(x, y)[3]
                        if a > cur_a:
                            c.set_pixel(x, y, (rgb[0], rgb[1], rgb[2], a))

    return c


# --- 2. Tileset & Obstacles ---

def generate_attic_tileset_floor() -> PixelCanvas:
    """256x96 px (8x3 32px tiles): Wide worn wooden floorboards with gaps, nail heads, knots.
    Row 0: Surface (plain 0,1; left pit 2; right pit 3; wood knot 4; stain 5; loose board 6; dropped button 7)
    Row 1: Ceiling lath & plaster fill
    Row 2: Dark attic floor void
    """
    sheet = PixelCanvas(256, 96, TRANSPARENT)

    def make_base_surface() -> PixelCanvas:
        t = PixelCanvas(32, 32, A2)
        # Top bevel lip
        t.line(0, 0, 31, 0, A4)
        t.line(0, 1, 31, 1, A3)
        # Wood grain lines
        t.line(0, 8, 31, 8, A1)
        t.line(0, 18, 31, 18, A1)
        t.line(0, 27, 31, 27, A0)
        return t

    def make_base_fill() -> PixelCanvas:
        t = PixelCanvas(32, 32, A0)
        # Horizontal lath wood strips & plaster keys
        t.rect(0, 4, 32, 6, A1, outline=A0)
        t.rect(0, 16, 32, 6, A1, outline=A0)
        t.line(0, 10, 31, 10, WHITE_SHADOW) # plaster dripping between lath
        return t

    def make_base_void() -> PixelCanvas:
        t = PixelCanvas(32, 32, VOID_BLACK)
        t.line(0, 0, 31, 0, A0)
        t.line(0, 1, 31, 1, A1)
        return t

    # --- ROW 0: SURFACE TILES ---
    # Tile 0: Plain oak floorboard
    t0 = make_base_surface()
    sheet.blit(t0, 0, 0)

    # Tile 1: Floorboard with square antique nail heads
    t1 = t0.clone()
    for nx, ny in [(8, 12), (24, 22)]:
        t1.rect(nx, ny, 3, 3, A0, outline=A12)
        t1.set_pixel(nx, ny, A13)
    sheet.blit(t1, 32, 0)

    # Tile 2: Left cliff edge into pit
    t2 = t0.clone()
    t2.line(0, 0, 0, 31, A0)
    t2.line(1, 0, 1, 31, A1)
    t2.set_pixel(0, 0, A4)
    sheet.blit(t2, 64, 0)

    # Tile 3: Right cliff edge into pit
    t3 = t0.clone()
    t3.line(31, 0, 31, 31, A0)
    t3.line(30, 0, 30, 31, A1)
    t3.set_pixel(31, 0, A4)
    sheet.blit(t3, 96, 0)

    # Tile 4: Wood knot & crack
    t4 = t0.clone()
    t4.circle(16, 14, 5, A0, outline=A1)
    t4.circle(16, 14, 2, A3)
    t4.line(12, 14, 6, 12, A0)
    t4.line(20, 14, 26, 16, A0)
    sheet.blit(t4, 128, 0)

    # Tile 5: Floorboard with varnish stain
    t5 = t0.clone()
    t5.circle(15, 16, 7, A1)
    t5.circle(16, 15, 4, A0)
    sheet.blit(t5, 160, 0)

    # Tile 6: Loose raised board edge with shadow gap
    t6 = t0.clone()
    t6.line(0, 14, 31, 14, A0)
    t6.line(0, 15, 31, 15, A4)
    sheet.blit(t6, 192, 0)

    # Tile 7: Dropped antique brass button
    t7 = t0.clone()
    t7.circle(16, 15, 4, A13, outline=A0)
    t7.set_pixel(15, 14, A14)
    sheet.blit(t7, 224, 0)

    # --- ROW 1: FILL TILES ---
    for c_idx in range(8):
        tf = make_base_fill()
        if c_idx == 2:
            tf.line(0, 0, 0, 31, A0)
        elif c_idx == 3:
            tf.line(31, 0, 31, 31, A0)
        sheet.blit(tf, c_idx * 32, 32)

    # --- ROW 2: VOID TILES ---
    for c_idx in range(8):
        tv = make_base_void()
        sheet.blit(tv, c_idx * 32, 64)

    return sheet


def generate_attic_pit_bg() -> PixelCanvas:
    """32x128 px: Attic pit between rafters, exposed insulation, lath & plaster ceiling."""
    c = PixelCanvas(32, 128, A0)

    # Vertical rafter timbers on sides
    c.rect(0, 0, 6, 128, A1)
    c.rect(26, 0, 6, 128, A1)
    c.line(5, 0, 5, 127, A0)
    c.line(26, 0, 26, 127, A0)

    # Fluffy yellow/pink fiberglass batt insulation in center
    for iy in range(10, 90, 8):
        c.rect(6, iy, 20, 6, A7, outline=A6)
        c.line(8, iy + 2, 22, iy + 2, A5)

    # Wood lath strips & white plaster keys at bottom (y=90..120)
    for ly in range(92, 120, 8):
        c.rect(6, ly, 20, 4, A1, outline=A0)
        c.line(6, ly + 4, 25, ly + 4, WHITE_SHADOW)

    # Dark void at bottom
    c.rect(0, 118, 32, 10, VOID_BLACK)

    return c


def generate_attic_obstacles() -> List[PixelCanvas]:
    """128x32 px total (4 frames 32x32): 4 stackable obstacle block skins:
    0: Stacked vintage suitcases
    1: Steamer trunks
    2: Round hat boxes
    3: Stack of old photo albums
    """
    frames = []

    # 0: Stacked suitcases
    c0 = PixelCanvas(32, 32, TRANSPARENT)
    for sy in [2, 17]:
        c0.rect(3, sy, 26, 13, A2, outline=A0)
        c0.line(3, sy, 28, sy, A4)
        # Leather straps
        c0.line(9, sy, 9, sy + 12, A1)
        c0.line(23, sy, 23, sy + 12, A1)
        # Brass corners
        c0.rect(3, sy, 3, 3, A13)
        c0.rect(26, sy, 3, 3, A13)
    frames.append(c0)

    # 1: Steamer trunk
    c1 = PixelCanvas(32, 32, TRANSPARENT)
    c1.rect(2, 2, 28, 28, A1, outline=A0)
    c1.line(2, 2, 29, 2, A3)
    # Heavy metal bands & brass latches
    for bx in [6, 24]:
        c1.rect(bx, 2, 3, 28, A12, outline=A0)
        c1.line(bx, 2, bx + 2, 2, A14)
    c1.rect(13, 12, 6, 8, A13, outline=A0)
    frames.append(c1)

    # 2: Round hat boxes
    c2 = PixelCanvas(32, 32, TRANSPARENT)
    for hy in [2, 17]:
        c2.rect(4, hy, 24, 13, A10, outline=A0)
        c2.line(4, hy, 27, hy, A11)
        c2.rect(2, hy, 28, 4, A8, outline=A0) # lid rim
    frames.append(c2)

    # 3: Stack of old photo albums
    c3 = PixelCanvas(32, 32, TRANSPARENT)
    for ay in [2, 12, 22]:
        c3.rect(3, ay, 26, 8, A1, outline=A0)
        c3.line(3, ay, 28, ay, A4)
        c3.rect(4, ay + 2, 4, 4, A13) # embossed corner
    frames.append(c3)

    return frames


def generate_attic_obstacles_tall() -> List[PixelCanvas]:
    """128x32 px total (4 frames 32x32): Cap variants for tall stack:
    0: Suitcase handle & luggage tag
    1: Arched trunk lid
    2: Hat box lid with ribbon bow
    3: Album with loose photo
    """
    frames = []

    # 0: Suitcase cap (handle & tag)
    c0 = PixelCanvas(32, 32, TRANSPARENT)
    c0.rect(3, 12, 26, 20, A2, outline=A0)
    c0.line(3, 12, 28, 12, A4)
    # Upright brass/leather handle
    c0.rect(12, 4, 8, 8, A1, outline=A0)
    c0.line(12, 4, 19, 4, A13)
    # Luggage paper tag swinging
    c0.rect(21, 6, 6, 8, A9, outline=A0)
    c0.line(20, 6, 21, 6, A8)
    frames.append(c0)

    # 1: Arched trunk lid
    c1 = PixelCanvas(32, 32, TRANSPARENT)
    c1.rect(2, 10, 28, 22, A1, outline=A0)
    # Arched curved lid top
    for x in range(2, 30):
        t = (x - 16) / 14.0
        arch_y = int(4 + t * t * 6)
        c1.line(x, arch_y, x, 10, A3)
        c1.set_pixel(x, arch_y, A4)
    # Brass latch
    c1.rect(13, 14, 6, 8, A13, outline=A0)
    frames.append(c1)

    # 2: Hat box lid with silk ribbon bow
    c2 = PixelCanvas(32, 32, TRANSPARENT)
    c2.rect(4, 12, 24, 20, A10, outline=A0)
    c2.line(4, 12, 27, 12, A11)
    # Ribbon bow on top
    c2.circle(12, 7, 4, A11, outline=A0)
    c2.circle(20, 7, 4, A11, outline=A0)
    c2.circle(16, 9, 3, A10, outline=A0)
    frames.append(c2)

    # 3: Album with loose sepia photo
    c3 = PixelCanvas(32, 32, TRANSPARENT)
    c3.rect(3, 12, 26, 20, A1, outline=A0)
    c3.line(3, 12, 28, 12, A4)
    # Loose sepia photo slipping out on right
    c3.rect(16, 2, 12, 12, A9, outline=A0)
    c3.rect(18, 4, 8, 8, A7) # photo image
    frames.append(c3)

    return frames


# --- 3. Goal Gate ---

def generate_attic_goal() -> List[PixelCanvas]:
    """384x128 px total (6 frames of 64x128 @ 10 fps):
    Brass kerosene lantern glowing brightly mounted on an old broom handle pole.
    """
    frames = []
    cx = 32

    for f_idx in range(6):
        c = PixelCanvas(64, 128, TRANSPARENT)

        # Rustic broom handle pole extending down to floor (grounded at y=127)
        c.rect(cx - 3, 44, 6, 80, A2, outline=A0)
        c.line(cx - 3, 44, cx - 3, 123, A4)
        # Wooden cross-base on floor
        c.rect(cx - 16, 122, 32, 6, A1, outline=A0)
        c.line(cx - 16, 122, cx + 15, 122, A4)

        # Kerosene lantern assembly mounted atop pole (y=8..48)
        # Top brass cap & hanging hoop
        c.circle(cx, 10, 5, A13, outline=A0)
        c.set_pixel(cx, 10, TRANSPARENT)
        c.rect(cx - 10, 15, 20, 6, A13, outline=A0)
        c.line(cx - 10, 15, cx + 9, 15, A14)

        # Glass globe / chimney (y=21..38)
        gy = 30
        c.circle(cx, gy, 11, A8, outline=A0)

        # Lower kerosene fount tank
        c.rect(cx - 12, 38, 24, 10, A12, outline=A0)
        c.line(cx - 12, 38, cx + 11, 38, A14)

        # Flame & Radiance animation
        if f_idx == 0:
            # Faint pilot flame
            c.circle(cx, gy, 3, A5)
            c.set_pixel(cx, gy - 1, PURE_WHITE)
        elif f_idx == 1:
            # Wick flares
            c.circle(cx, gy, 5, A5, outline=A4)
            c.set_pixel(cx, gy, PURE_WHITE)
        elif f_idx == 2:
            # Expanding amber warmth
            c.circle(cx, gy, 14, A4)
            c.circle(cx, gy, 8, A5)
            c.circle(cx, gy, 4, PURE_WHITE)
        else:
            # Brilliant golden lantern radiance (f_idx 3, 4, 5)
            glow_r = 24 + (f_idx - 3) * 5
            c.circle(cx, gy, glow_r, A0)
            c.circle(cx, gy, int(glow_r * 0.75), A4)
            c.circle(cx, gy, int(glow_r * 0.5), A5)
            c.circle(cx, gy, 10, A14)
            c.circle(cx, gy, 5, PURE_WHITE)
            # Radiating light rays
            for ang in range(0, 360, 45):
                rad = math.radians(ang + f_idx * 12)
                rx1 = int(cx + 14 * math.cos(rad))
                ry1 = int(gy + 14 * math.sin(rad))
                rx2 = int(cx + (glow_r + 6) * math.cos(rad))
                ry2 = int(gy + (glow_r + 6) * math.sin(rad))
                c.line(rx1, ry1, rx2, ry2, A5)

        frames.append(c)

    return frames


# --- 4. Floor Clutter (10 items + shadows) ---

def generate_attic_clutter() -> List[Tuple[str, PixelCanvas, PixelCanvas]]:
    """Returns list of (item_name, item_canvas, shadow_canvas)."""
    items = []

    # 1. marble (20x20)
    c1 = PixelCanvas(20, 20, TRANSPARENT)
    c1.circle(10, 10, 6, A15, outline=OUTLINE)
    c1.line(8, 8, 12, 12, A5) # amber swirl
    c1.set_pixel(8, 7, PURE_WHITE) # glass specular
    s1 = make_shadow(20, 20, 10, 16, 6, 2)
    items.append(("attic_deco_marble", c1, s1))

    # 2. brittle_comic (32x24)
    c2 = PixelCanvas(32, 24, TRANSPARENT)
    c2.rect(4, 5, 24, 14, A9, outline=OUTLINE)
    c2.line(4, 5, 27, 5, PURE_WHITE)
    # Faded superhero cover art
    c2.rect(8, 7, 16, 10, A10)
    c2.circle(16, 11, 3, YELLOW_MID)
    # Bent dog-eared corner
    c2.line(24, 5, 27, 8, A2)
    s2 = make_shadow(32, 24, 16, 17, 13, 3)
    items.append(("attic_deco_brittle_comic", c2, s2))

    # 3. faded_photo (28x24)
    c3 = PixelCanvas(28, 24, TRANSPARENT)
    c3.rect(3, 4, 22, 16, A9, outline=OUTLINE)
    c3.line(3, 4, 24, 4, PURE_WHITE)
    # Sepia tintype portrait silhouette
    c3.rect(6, 6, 16, 12, A7)
    c3.circle(14, 10, 3, A1) # face
    s3 = make_shadow(28, 24, 14, 18, 11, 3)
    items.append(("attic_deco_faded_photo", c3, s3))

    # 4. music_box_key (24x20)
    c4 = PixelCanvas(24, 20, TRANSPARENT)
    # Ornate butterfly winding bow
    c4.circle(7, 9, 4, A13, outline=OUTLINE)
    c4.set_pixel(7, 9, TRANSPARENT)
    c4.circle(13, 9, 4, A13, outline=OUTLINE)
    c4.set_pixel(13, 9, TRANSPARENT)
    # Stem
    c4.rect(9, 12, 3, 5, A12, outline=OUTLINE)
    s4 = make_shadow(24, 20, 10, 16, 8, 2)
    items.append(("attic_deco_music_box_key", c4, s4))

    # 5. tarnished_spoon (32x16)
    c5 = PixelCanvas(32, 16, TRANSPARENT)
    # Oval bowl on left
    c5.circle(7, 8, 4, A6, outline=OUTLINE)
    c5.circle(7, 8, 2, A8)
    # Thin handle to right with ornate tip
    c5.line(11, 8, 26, 8, A7)
    c5.line(11, 7, 24, 7, A8) # specular
    c5.circle(26, 8, 2, A13, outline=OUTLINE)
    s5 = make_shadow(32, 16, 16, 12, 13, 2)
    items.append(("attic_deco_tarnished_spoon", c5, s5))

    # 6. bundle_of_letters (32x24)
    c6 = PixelCanvas(32, 24, TRANSPARENT)
    # Stacked aged letters
    c6.rect(4, 6, 24, 13, A9, outline=OUTLINE)
    c6.line(4, 6, 27, 6, PURE_WHITE)
    # Jute string tied crosswise
    c6.line(16, 6, 16, 18, A2)
    c6.line(4, 12, 27, 12, A2)
    # Red wax seal in center
    c6.circle(16, 12, 3, RED_MID, outline=OUTLINE)
    s6 = make_shadow(32, 24, 16, 17, 13, 3)
    items.append(("attic_deco_bundle_of_letters", c6, s6))

    # 7. doll_arm (24x16)
    c7 = PixelCanvas(24, 16, TRANSPARENT)
    # Porcelain forearm and hand
    c7.rect(4, 6, 14, 5, A9, outline=OUTLINE)
    c7.line(4, 6, 17, 6, PURE_WHITE)
    # Joint ball on left
    c7.circle(4, 8, 2, A8)
    # Tiny hand on right
    c7.rect(17, 7, 4, 3, A9, outline=OUTLINE)
    s7 = make_shadow(24, 16, 12, 12, 9, 2)
    items.append(("attic_deco_doll_arm", c7, s7))

    # 8. teddy_eye (20x20)
    c8 = PixelCanvas(20, 20, TRANSPARENT)
    # Amber glass button eye
    c8.circle(10, 10, 5, A5, outline=OUTLINE)
    c8.circle(10, 10, 2, A0) # pupil
    c8.set_pixel(8, 8, PURE_WHITE) # specular
    s8 = make_shadow(20, 20, 10, 15, 6, 2)
    items.append(("attic_deco_teddy_eye", c8, s8))

    # 9. dust_bunny (28x20)
    c9 = PixelCanvas(28, 20, TRANSPARENT)
    # Fluffy irregular lump of dust
    c9.circle(14, 10, 6, A7)
    c9.circle(10, 11, 4, A8)
    c9.circle(18, 11, 4, A6)
    # Trapped stray wool threads
    c9.set_pixel(13, 8, A10)
    c9.set_pixel(16, 12, A5)
    s9 = make_shadow(28, 20, 14, 15, 10, 3)
    items.append(("attic_deco_dust_bunny", c9, s9))

    # 10. jar_of_buttons (24x32)
    c10 = PixelCanvas(24, 32, TRANSPARENT)
    # Glass jar body
    c10.rect(4, 8, 16, 22, A15, outline=OUTLINE)
    c10.rect(5, 9, 14, 20, A0)
    # Glass highlight
    c10.line(6, 10, 6, 28, WHITE_SHADOW)
    # Tin lid
    c10.rect(5, 4, 14, 4, A13, outline=OUTLINE)
    c10.line(5, 4, 18, 4, A14)
    # Colorful vintage buttons inside
    for bx, by, col in [(8, 14, A10), (14, 16, A5), (9, 21, A8), (15, 23, A11), (11, 26, PURE_WHITE)]:
        c10.circle(bx, by, 2, col)
    s10 = make_shadow(24, 32, 12, 29, 9, 3)
    items.append(("attic_deco_jar_of_buttons", c10, s10))

    return items


# --- 5. Animated Props (6 props) ---

def generate_attic_prop_rocking_chair() -> List[PixelCanvas]:
    """80x96 px, 10 frames @ 6 fps: Wooden rocking chair rocking back and forth on its own."""
    frames = []
    # Rocking angles in degrees
    angles = [-5, -4, -2, 0, 2, 4, 5, 4, 2, 0]

    for ang_deg in angles:
        c = PixelCanvas(80, 96, TRANSPARENT)
        rad = math.radians(ang_deg)

        # Rocker pivot on floor (x=40, y=95)
        cx = 40
        # Spindle back
        for sp_x in range(24, 56, 6):
            rx_top = int(cx + (sp_x - cx) * math.cos(rad) - 65 * math.sin(rad))
            ry_top = int(95 + (sp_x - cx) * math.sin(rad) - 65 * math.cos(rad))
            rx_bot = int(cx + (sp_x - cx) * math.cos(rad) - 25 * math.sin(rad))
            ry_bot = int(95 + (sp_x - cx) * math.sin(rad) - 25 * math.cos(rad))
            c.line(rx_top, ry_top, rx_bot, ry_bot, A2)

        # Seat slab
        sx1 = int(cx - 20 * math.cos(rad) - 25 * math.sin(rad))
        sy1 = int(95 - 20 * math.sin(rad) - 25 * math.cos(rad))
        sx2 = int(cx + 20 * math.cos(rad) - 25 * math.sin(rad))
        sy2 = int(95 + 20 * math.sin(rad) - 25 * math.cos(rad))
        c.line(sx1, sy1, sx2, sy2, A4)

        # Curved rocker runners along bottom (grounded at y=95)
        for rkx in range(12, 68):
            t = (rkx - cx) / 28.0
            rky = int(95 + t * t * 4 - ang_deg * t * 0.8)
            if 0 <= rkx < 80 and 0 <= rky < 96:
                c.set_pixel(rkx, rky, A3)

        frames.append(c)

    return frames


def generate_attic_prop_moon_window() -> List[PixelCanvas]:
    """96x128 px, 8 frames @ 6 fps: Slanted moonlight beam pouring from round window with swirling dust."""
    frames = []

    for f_idx in range(8):
        c = PixelCanvas(96, 128, TRANSPARENT)
        wx, wy = 48, 30

        # Round window frame
        c.circle(wx, wy, 24, A0)
        c.circle(wx, wy, 21, A4)
        c.circle(wx, wy, 18, A15)
        # Window muntins cross
        c.line(wx - 18, wy, wx + 18, wy, A0)
        c.line(wx, wy - 18, wx, wy + 18, A0)

        # Slanted moonlight shaft (y=30..128)
        for ly in range(wy + 10, 128):
            t = (ly - (wy + 10)) / 90.0
            span = int(12 + t * 28)
            lx_mid = int(wx + t * 24)
            for x in range(lx_mid - span, lx_mid + span + 1):
                if 0 <= x < 96:
                    dist = abs(x - lx_mid) / float(max(1, span))
                    if dist < 0.5:
                        c.set_pixel(x, ly, A15)
                    elif dist < 0.85:
                        c.set_pixel(x, ly, A8)

        # Swirling dust motes
        for d_idx in range(6):
            ang = (f_idx * 45 + d_idx * 60)
            rad = math.radians(ang)
            dx = int(wx + 15 + d_idx * 6 + 8 * math.cos(rad))
            dy = int(wy + 25 + d_idx * 12 + 6 * math.sin(rad))
            if 0 <= dx < 96 and 0 <= dy < 128:
                c.set_pixel(dx, dy, PURE_WHITE if d_idx % 2 == 0 else A5)

        frames.append(c)

    return frames


def generate_attic_prop_sheet_ghost() -> List[PixelCanvas]:
    """80x96 px, 8 frames @ 6 fps: White sheet covering a chair that billows gently as if moving."""
    frames = []

    for f_idx in range(8):
        c = PixelCanvas(80, 96, TRANSPARENT)
        cx = 40
        swell = int(math.sin(f_idx * 0.8) * 3)

        # Chair silhouette under sheet (grounded at y=95)
        c.rect(cx - 24 - swell, 30, 48 + swell * 2, 65, WHITE_SHADOW, outline=A0)
        c.circle(cx, 30, 22 + swell, WHITE_SHADOW)

        # Draped folds swelling
        c.line(cx - 24 - swell, 30, cx + 23 + swell, 30, PURE_WHITE)
        for fx in [cx - 14, cx, cx + 14]:
            c.line(fx, 30, fx + int(swell * 1.5), 94, WHITE_MID)
            c.line(fx + 1, 30, fx + 1 + int(swell * 1.5), 94, A8)

        # Spooky subtle folds around eye-height
        c.line(cx - 8, 42, cx - 4, 42, A8)
        c.line(cx + 4, 42, cx + 8, 42, A8)

        frames.append(c)

    return frames


def generate_attic_prop_music_box() -> List[PixelCanvas]:
    """64x64 px, 8 frames @ 8 fps: Open wooden music box with tiny ballerina figurine spinning."""
    frames = []

    for f_idx in range(8):
        c = PixelCanvas(64, 64, TRANSPARENT)
        cx = 32

        # Mahogany open music box base (grounded at y=63)
        c.rect(cx - 22, 38, 44, 25, A1, outline=A0)
        c.line(cx - 22, 38, cx + 21, 38, A4)
        # Open lid tilted up at back
        c.line(cx - 22, 38, cx - 22, 14, A2)
        c.line(cx + 21, 38, cx + 21, 14, A2)
        c.line(cx - 22, 14, cx + 21, 14, A4)
        # Velvet interior lining
        c.rect(cx - 18, 42, 36, 18, A10)

        # Mirrored pedestal in center
        c.circle(cx, 44, 6, A15, outline=A13)

        # Ballerina figurine spinning (360° across 8 frames)
        rot_ang = f_idx * 45
        rad = math.radians(rot_ang)
        facing_x = int(math.sin(rad) * 3)

        # Body & head (y=20..38)
        c.circle(cx + facing_x, 22, 3, SKIN_LIGHT, outline=A0) # head
        c.line(cx, 25, cx, 34, A11) # torso
        # Tutu skirt
        c.circle(cx, 32, 6, PURE_WHITE)
        # Pointed legs down to pedestal
        c.line(cx, 34, cx, 43, SKIN_LIGHT)
        # Raised arms
        arm_w = int(math.cos(rad) * 4)
        c.line(cx, 26, cx + arm_w, 20, SKIN_LIGHT)
        c.line(cx, 26, cx - arm_w, 20, SKIN_LIGHT)

        # Musical sparkle notes floating out
        if f_idx % 2 == 0:
            c.set_pixel(cx + 18, 22 - f_idx * 2, A14)
            c.set_pixel(cx - 16, 26 - f_idx * 2, PURE_WHITE)

        frames.append(c)

    return frames


def generate_attic_prop_cobweb() -> List[PixelCanvas]:
    """64x64 px, 8 frames @ 6 fps: Large corner cobweb swaying with tiny spider twitching."""
    frames = []

    for f_idx in range(8):
        c = PixelCanvas(64, 64, TRANSPARENT)
        sway = int(math.sin(f_idx * 0.8) * 2)

        # Wooden ceiling beam in top-left corner
        c.rect(0, 0, 64, 8, A1, outline=A0)
        c.rect(0, 0, 8, 64, A1, outline=A0)

        # Concentric cobweb arc filaments
        web_col = A8
        for rad in [16, 28, 42, 56]:
            rad_cur = rad + sway
            for ang in range(0, 91, 6):
                wx = int(rad_cur * math.cos(math.radians(ang)))
                wy = int(rad_cur * math.sin(math.radians(ang)))
                if 0 <= wx < 64 and 0 <= wy < 64:
                    c.set_pixel(wx, wy, web_col)

        # Radial web spokes
        for ang in [18, 36, 54, 72]:
            c.line(0, 0, int(60 * math.cos(math.radians(ang))), int(60 * math.sin(math.radians(ang))), web_col)

        # Tiny spider twitching near center (cx=24, cy=24)
        sp_x = 24 + sway
        sp_y = 24 + (1 if f_idx % 2 == 0 else 0)
        c.circle(sp_x, sp_y, 2, A0)
        # Legs
        c.set_pixel(sp_x - 3, sp_y - 2, A0)
        c.set_pixel(sp_x + 3, sp_y - 2, A0)
        c.set_pixel(sp_x - 3, sp_y + 2, A0)
        c.set_pixel(sp_x + 3, sp_y + 2, A0)

        frames.append(c)

    return frames


def generate_attic_prop_mobile() -> List[PixelCanvas]:
    """80x80 px, 10 frames @ 6 fps: Faded vintage crib mobile with worn hanging animal figures rotating."""
    frames = []

    for f_idx in range(10):
        c = PixelCanvas(80, 80, TRANSPARENT)
        cx = 40

        # Central cord from ceiling (y=0..15)
        c.line(cx, 0, cx, 15, A2)

        # Rotating crossbars (perspective ellipse)
        rot_ang = f_idx * 36
        rad1 = math.radians(rot_ang)
        rad2 = math.radians(rot_ang + 90)

        # Bar 1 ends
        x1_a = int(cx + 30 * math.cos(rad1))
        y1_a = int(15 + 8 * math.sin(rad1))
        x1_b = int(cx - 30 * math.cos(rad1))
        y1_b = int(15 - 8 * math.sin(rad1))
        c.line(x1_a, y1_a, x1_b, y1_b, A4)

        # Bar 2 ends
        x2_a = int(cx + 30 * math.cos(rad2))
        y2_a = int(15 + 8 * math.sin(rad2))
        x2_b = int(cx - 30 * math.cos(rad2))
        y2_b = int(15 - 8 * math.sin(rad2))
        c.line(x2_a, y2_a, x2_b, y2_b, A4)

        # Hanging figures on threads
        # Figure 1: Wooden sheep on end 1a
        c.line(x1_a, y1_a, x1_a, y1_a + 25, A8)
        c.circle(x1_a, y1_a + 30, 5, PURE_WHITE, outline=A0)
        c.set_pixel(x1_a - 3, y1_a + 28, A0) # sheep head

        # Figure 2: Crescent moon on end 1b
        c.line(x1_b, y1_b, x1_b, y1_b + 28, A8)
        c.circle(x1_b, y1_b + 34, 5, A5, outline=A0)
        c.circle(x1_b + 2, y1_b + 33, 4, TRANSPARENT)

        # Figure 3: Faded star on end 2a
        c.line(x2_a, y2_a, x2_a, y2_a + 22, A8)
        c.rect(x2_a - 3, y2_a + 26, 7, 7, A14, outline=A0)

        # Figure 4: Teddy bear cutout on end 2b
        c.line(x2_b, y2_b, x2_b, y2_b + 26, A8)
        c.circle(x2_b, y2_b + 32, 5, A3, outline=A0)

        frames.append(c)

    return frames


# ==============================================================================
# MANIFEST ENTRIES & MAIN RUNNER
# ==============================================================================

MANIFEST_UPDATES = {
    # --- Basement ---
    "basement_bg_far.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "basement_bg_far_anim.png": {"frame_w": 960, "frame_h": 540, "frames": 4, "fps": 3, "loop": True},
    "basement_bg_mid.png": {"frame_w": 1280, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "basement_bg_near.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "basement_sky_gradient.png": {"frame_w": 1, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "basement_fg_legs.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "basement_fg_dust.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "basement_tileset_floor.png": {"frame_w": 256, "frame_h": 96, "frames": 1, "fps": 0, "loop": False, "tile_w": 32, "tile_h": 32, "columns": 8, "rows": 3},
    "basement_pit_bg.png": {"frame_w": 32, "frame_h": 128, "frames": 1, "fps": 0, "loop": False},
    "basement_obstacles.png": {"frame_w": 32, "frame_h": 32, "frames": 4, "fps": 0, "loop": False},
    "basement_obstacles_tall.png": {"frame_w": 32, "frame_h": 32, "frames": 4, "fps": 0, "loop": False},
    "basement_goal.png": {"frame_w": 64, "frame_h": 128, "frames": 6, "fps": 10, "loop": True},
    "basement_deco_screw.png": {"frame_w": 20, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_screw_shadow.png": {"frame_w": 20, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_nail.png": {"frame_w": 24, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_nail_shadow.png": {"frame_w": 24, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_bolt.png": {"frame_w": 24, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_bolt_shadow.png": {"frame_w": 24, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_rag.png": {"frame_w": 32, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_rag_shadow.png": {"frame_w": 32, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_flashlight.png": {"frame_w": 36, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_flashlight_shadow.png": {"frame_w": 36, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_crumpled_blueprint.png": {"frame_w": 36, "frame_h": 24, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_crumpled_blueprint_shadow.png": {"frame_w": 36, "frame_h": 24, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_rusty_key.png": {"frame_w": 24, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_rusty_key_shadow.png": {"frame_w": 24, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_jar_of_nails.png": {"frame_w": 24, "frame_h": 32, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_jar_of_nails_shadow.png": {"frame_w": 24, "frame_h": 32, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_mouse_trap.png": {"frame_w": 32, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_mouse_trap_shadow.png": {"frame_w": 32, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_sawdust.png": {"frame_w": 32, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "basement_deco_sawdust_shadow.png": {"frame_w": 32, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "basement_prop_bulb.png": {"frame_w": 64, "frame_h": 96, "frames": 10, "fps": 6, "loop": True},
    "basement_prop_furnace.png": {"frame_w": 96, "frame_h": 96, "frames": 8, "fps": 8, "loop": True},
    "basement_prop_pipe_drip.png": {"frame_w": 48, "frame_h": 80, "frames": 10, "fps": 10, "loop": True},
    "basement_prop_washer.png": {"frame_w": 80, "frame_h": 80, "frames": 8, "fps": 12, "loop": True},
    "basement_prop_spider.png": {"frame_w": 32, "frame_h": 80, "frames": 12, "fps": 8, "loop": True},
    "basement_prop_tv_static.png": {"frame_w": 80, "frame_h": 64, "frames": 6, "fps": 12, "loop": True},

    # --- Attic ---
    "attic_bg_far.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "attic_bg_far_anim.png": {"frame_w": 960, "frame_h": 540, "frames": 4, "fps": 3, "loop": True},
    "attic_bg_mid.png": {"frame_w": 1280, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "attic_bg_near.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "attic_sky_gradient.png": {"frame_w": 1, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "attic_fg_legs.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "attic_fg_dust.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
    "attic_tileset_floor.png": {"frame_w": 256, "frame_h": 96, "frames": 1, "fps": 0, "loop": False, "tile_w": 32, "tile_h": 32, "columns": 8, "rows": 3},
    "attic_pit_bg.png": {"frame_w": 32, "frame_h": 128, "frames": 1, "fps": 0, "loop": False},
    "attic_obstacles.png": {"frame_w": 32, "frame_h": 32, "frames": 4, "fps": 0, "loop": False},
    "attic_obstacles_tall.png": {"frame_w": 32, "frame_h": 32, "frames": 4, "fps": 0, "loop": False},
    "attic_goal.png": {"frame_w": 64, "frame_h": 128, "frames": 6, "fps": 10, "loop": True},
    "attic_deco_marble.png": {"frame_w": 20, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_marble_shadow.png": {"frame_w": 20, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_brittle_comic.png": {"frame_w": 32, "frame_h": 24, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_brittle_comic_shadow.png": {"frame_w": 32, "frame_h": 24, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_faded_photo.png": {"frame_w": 28, "frame_h": 24, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_faded_photo_shadow.png": {"frame_w": 28, "frame_h": 24, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_music_box_key.png": {"frame_w": 24, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_music_box_key_shadow.png": {"frame_w": 24, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_tarnished_spoon.png": {"frame_w": 32, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_tarnished_spoon_shadow.png": {"frame_w": 32, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_bundle_of_letters.png": {"frame_w": 32, "frame_h": 24, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_bundle_of_letters_shadow.png": {"frame_w": 32, "frame_h": 24, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_doll_arm.png": {"frame_w": 24, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_doll_arm_shadow.png": {"frame_w": 24, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_teddy_eye.png": {"frame_w": 20, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_teddy_eye_shadow.png": {"frame_w": 20, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_dust_bunny.png": {"frame_w": 28, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_dust_bunny_shadow.png": {"frame_w": 28, "frame_h": 20, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_jar_of_buttons.png": {"frame_w": 24, "frame_h": 32, "frames": 1, "fps": 0, "loop": False},
    "attic_deco_jar_of_buttons_shadow.png": {"frame_w": 24, "frame_h": 32, "frames": 1, "fps": 0, "loop": False},
    "attic_prop_rocking_chair.png": {"frame_w": 80, "frame_h": 96, "frames": 10, "fps": 6, "loop": True},
    "attic_prop_moon_window.png": {"frame_w": 96, "frame_h": 128, "frames": 8, "fps": 6, "loop": True},
    "attic_prop_sheet_ghost.png": {"frame_w": 80, "frame_h": 96, "frames": 8, "fps": 6, "loop": True},
    "attic_prop_music_box.png": {"frame_w": 64, "frame_h": 64, "frames": 8, "fps": 8, "loop": True},
    "attic_prop_cobweb.png": {"frame_w": 64, "frame_h": 64, "frames": 8, "fps": 6, "loop": True},
    "attic_prop_mobile.png": {"frame_w": 80, "frame_h": 80, "frames": 10, "fps": 6, "loop": True},
}


def generate_all_basement_and_attic():
    out_dir = Path("art/v2")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=== Generating Basement Assets ===")
    save_single(generate_basement_sky_gradient(), str(out_dir / "basement_sky_gradient.png"))
    save_single(generate_basement_bg_far(), str(out_dir / "basement_bg_far.png"))
    assemble_strip(generate_basement_bg_far_anim(), str(out_dir / "basement_bg_far_anim.png"))
    save_single(generate_basement_bg_mid(), str(out_dir / "basement_bg_mid.png"))
    save_single(generate_basement_bg_near(), str(out_dir / "basement_bg_near.png"))
    save_single(generate_basement_fg_legs(), str(out_dir / "basement_fg_legs.png"))
    save_single(generate_basement_fg_dust(), str(out_dir / "basement_fg_dust.png"))

    save_single(generate_basement_tileset_floor(), str(out_dir / "basement_tileset_floor.png"))
    save_single(generate_basement_pit_bg(), str(out_dir / "basement_pit_bg.png"))
    assemble_strip(generate_basement_obstacles(), str(out_dir / "basement_obstacles.png"))
    assemble_strip(generate_basement_obstacles_tall(), str(out_dir / "basement_obstacles_tall.png"))
    assemble_strip(generate_basement_goal(), str(out_dir / "basement_goal.png"))

    for name, item_c, shadow_c in generate_basement_clutter():
        save_single(item_c, str(out_dir / f"{name}.png"))
        save_single(shadow_c, str(out_dir / f"{name}_shadow.png"))

    assemble_strip(generate_basement_prop_bulb(), str(out_dir / "basement_prop_bulb.png"))
    assemble_strip(generate_basement_prop_furnace(), str(out_dir / "basement_prop_furnace.png"))
    assemble_strip(generate_basement_prop_pipe_drip(), str(out_dir / "basement_prop_pipe_drip.png"))
    assemble_strip(generate_basement_prop_washer(), str(out_dir / "basement_prop_washer.png"))
    assemble_strip(generate_basement_prop_spider(), str(out_dir / "basement_prop_spider.png"))
    assemble_strip(generate_basement_prop_tv_static(), str(out_dir / "basement_prop_tv_static.png"))

    print("\n=== Generating Attic Assets ===")
    save_single(generate_attic_sky_gradient(), str(out_dir / "attic_sky_gradient.png"))
    save_single(generate_attic_bg_far(), str(out_dir / "attic_bg_far.png"))
    assemble_strip(generate_attic_bg_far_anim(), str(out_dir / "attic_bg_far_anim.png"))
    save_single(generate_attic_bg_mid(), str(out_dir / "attic_bg_mid.png"))
    save_single(generate_attic_bg_near(), str(out_dir / "attic_bg_near.png"))
    save_single(generate_attic_fg_legs(), str(out_dir / "attic_fg_legs.png"))
    save_single(generate_attic_fg_dust(), str(out_dir / "attic_fg_dust.png"))

    save_single(generate_attic_tileset_floor(), str(out_dir / "attic_tileset_floor.png"))
    save_single(generate_attic_pit_bg(), str(out_dir / "attic_pit_bg.png"))
    assemble_strip(generate_attic_obstacles(), str(out_dir / "attic_obstacles.png"))
    assemble_strip(generate_attic_obstacles_tall(), str(out_dir / "attic_obstacles_tall.png"))
    assemble_strip(generate_attic_goal(), str(out_dir / "attic_goal.png"))

    for name, item_c, shadow_c in generate_attic_clutter():
        save_single(item_c, str(out_dir / f"{name}.png"))
        save_single(shadow_c, str(out_dir / f"{name}_shadow.png"))

    assemble_strip(generate_attic_prop_rocking_chair(), str(out_dir / "attic_prop_rocking_chair.png"))
    assemble_strip(generate_attic_prop_moon_window(), str(out_dir / "attic_prop_moon_window.png"))
    assemble_strip(generate_attic_prop_sheet_ghost(), str(out_dir / "attic_prop_sheet_ghost.png"))
    assemble_strip(generate_attic_prop_music_box(), str(out_dir / "attic_prop_music_box.png"))
    assemble_strip(generate_attic_prop_cobweb(), str(out_dir / "attic_prop_cobweb.png"))
    assemble_strip(generate_attic_prop_mobile(), str(out_dir / "attic_prop_mobile.png"))

    # Update manifest.json
    manifest_path = out_dir / "manifest.json"
    manifest = {}
    if manifest_path.exists():
        with open(manifest_path, "r") as f:
            manifest = json.load(f)

    for k, v in MANIFEST_UPDATES.items():
        manifest[k] = v

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"\nUpdated {manifest_path} with {len(MANIFEST_UPDATES)} Basement & Attic entries.")


if __name__ == "__main__":
    generate_all_basement_and_attic()
