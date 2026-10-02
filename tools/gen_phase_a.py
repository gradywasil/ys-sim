"""Younger Sibling Simulator - Phase A Art Generator v3.

Generates all Phase A assets into art/v2/:
- A1. Replace placeholders and add placed bridge:
    item_umbrella.png (48x48, 6f, 8fps, loop: true)
    item_umbrella_pop.png (48x48, 3f, 24fps, loop: false)
    item_bridge.png (48x48, 6f, 8fps, loop: true)
    item_bridge_pop.png (48x48, 3f, 24fps, loop: false)
    bridge_plank.png (240x32, 1f, 0fps, loop: false)
    bridge_land.png (240x48, 6f, 24fps, loop: false)
    fx_umbrella_canopy.png (64x48, 8f, 12fps, loop: false)
- A2. Bedtime timer HUD:
    ui_bedtime_clock.png (96x96, 12f, 0fps, loop: false)
    ui_bedtime_clock_ring.png (96x96, 6f, 16fps, loop: true)
    ui_bedtime_moon.png (48x48, 4f, 0fps, loop: false)
    ui_bedtime_warning.png (960x540, 4f, 6fps, loop: true)
    ui_banner_bedtime.png (384x96, 6f, 12fps, loop: false)
    parent_bedtime.png (128x192, 8f, 10fps, loop: false)
    parent_speech_bedtime.png (192x96, 1f, 0fps, loop: false)
- A3. Cookie:
    item_cookie.png (48x48, 6f, 8fps, loop: true)
    item_cookie_pop.png (48x48, 4f, 24fps, loop: false)
    parent_happy.png (128x192, 8f, 10fps, loop: false)
    fx_crumbs.png (16x16, 6f, 14fps, loop: false)
    fx_calm_wave.png (128x64, 6f, 16fps, loop: false)
- A4. Active-buff status HUD:
    ui_status_ring.png (48x48, 16f, 0fps, loop: false)
    ui_status_bg.png (56x56, 1f, 0fps, loop: false)
- A5. New powerup icons & placed placeables:
    item_slippers.png + item_slippers_pop.png (48x48)
    item_sugar.png + item_sugar_pop.png (48x48)
    item_stopwatch.png + item_stopwatch_pop.png (48x48)
    item_bubblewrap.png + item_bubblewrap_pop.png (48x48)
    item_gloves.png + item_gloves_pop.png (48x48)
    item_trampoline.png + item_trampoline_pop.png (48x48)
    item_fan.png + item_fan_pop.png (48x48)
    item_tape.png + item_tape_pop.png (48x48)
    item_ramp.png + item_ramp_pop.png (48x48)
    placed_trampoline.png (96x48, 6f, 20fps, loop: false)
    placed_ramp.png (96x48, 1f, 0fps, loop: false)
    placed_fan.png (64x64, 8f, 16fps, loop: true)
    placed_tape.png (64x16, 1f, 0fps, loop: false)
"""

import json
import math
from pathlib import Path
from typing import List, Tuple
from PIL import Image

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

BOB_6 = [0, -1, -2, -2, -1, 0]

def save_single(canvas: PixelCanvas, output_path: str):
    canvas.to_image().save(output_path, "PNG")
    print(f"Saved {output_path} ({canvas.width}x{canvas.height}, 1 frame)")

# ==============================================================================
# A1. REPLACE PLACEHOLDERS & ADD PLACED BRIDGE
# ==============================================================================

def generate_item_umbrella() -> List[PixelCanvas]:
    """48x48, 6 frames, 8 fps, loop: true.
    Bright red-and-white kid's umbrella, bobbing, glint sweep.
    """
    frames = []
    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cy = 24 + BOB_6[f]
        cx = 24

        # Ferrule (top spike)
        c.rect(cx - 1, cy - 16, 2, 4, METAL_MID, outline=OUTLINE)
        c.set_pixel(cx - 1, cy - 16, PURE_WHITE)

        # Canopy - dome shape from cy-12 to cy+2
        # Width: cx-16 to cx+16 (33px)
        # Red and white alternating panels: 4 visible panels
        # Panel 1 (left outer): red
        # Panel 2 (left inner): white
        # Panel 3 (right inner): red
        # Panel 4 (right outer): white
        for y in range(cy - 12, cy + 3):
            dy = (y - (cy - 12)) / 14.0
            hw = int(math.sin(dy * math.pi * 0.5) * 16.5)
            left_x = cx - hw
            right_x = cx + hw
            # Canopy outline
            c.set_pixel(left_x, y, OUTLINE)
            c.set_pixel(right_x, y, OUTLINE)
            if y == cy - 12:
                c.line(left_x, y, right_x, y, OUTLINE)
                continue

            for x in range(left_x + 1, right_x):
                # Determine panel index (0..3)
                p_rel = (x - (cx - 16)) / 32.0
                if p_rel < 0.25:
                    p_idx = 0
                elif p_rel < 0.5:
                    p_idx = 1
                elif p_rel < 0.75:
                    p_idx = 2
                else:
                    p_idx = 3

                # Glint sweep position across panels
                is_glint = (abs(x - (cx - 14 + f * 5)) <= 1 and y <= cy - 4)

                if is_glint:
                    c.set_pixel(x, y, PURE_WHITE)
                elif p_idx % 2 == 0:
                    # Red panel
                    if y <= cy - 6 and x <= cx:
                        c.set_pixel(x, y, RED_LIGHT)
                    elif y >= cy:
                        c.set_pixel(x, y, RED_SHADOW)
                    else:
                        c.set_pixel(x, y, RED_MID)
                else:
                    # White / Cream panel
                    if y <= cy - 6 and x <= cx:
                        c.set_pixel(x, y, PURE_WHITE)
                    elif y >= cy:
                        c.set_pixel(x, y, WHITE_SHADOW)
                    else:
                        c.set_pixel(x, y, WHITE_MID)

        # Scalloped bottom rim of canopy (y = cy + 2..3)
        for rib_x in [cx - 16, cx - 8, cx, cx + 8, cx + 16]:
            c.set_pixel(rib_x, cy + 3, OUTLINE)
            c.set_pixel(rib_x, cy + 2, METAL_MID)
        for arc_x in [cx - 12, cx - 4, cx + 4, cx + 12]:
            c.set_pixel(arc_x, cy + 1, OUTLINE)

        # Shaft (pole)
        c.line(cx, cy + 2, cx, cy + 13, WOOD_BLACK)
        c.line(cx - 1, cy + 3, cx - 1, cy + 13, BROWN_DARK)

        # J-hook Handle (curving bottom right)
        # down to cy+16, curves right to cx+4, then up to cy+14
        c.polygon([
            (cx - 1, cy + 13), (cx - 1, cy + 16),
            (cx + 3, cy + 16), (cx + 5, cy + 14),
            (cx + 3, cy + 13), (cx + 1, cy + 15),
            (cx, cy + 13)
        ], fill=BROWN_MID, outline=OUTLINE)
        c.set_pixel(cx, cy + 15, WOOD_HIGHLIGHT)

        # Glint sparkle on frame
        if f in (1, 2):
            c.set_pixel(cx - 6 + f * 4, cy - 8, PURE_WHITE)
            c.set_pixel(cx - 5 + f * 4, cy - 8, YELLOW_LIGHT)

        frames.append(c)
    return frames

def generate_item_umbrella_pop() -> List[PixelCanvas]:
    """48x48, 3 frames, 24 fps, loop: false. Red-tinted pickup starburst."""
    frames = []
    cx, cy = 24, 24

    # Frame 0: Flash with red & white radial bursts
    c0 = PixelCanvas(48, 48, TRANSPARENT)
    c0.circle(cx, cy, 10, PURE_WHITE, outline=RED_MID)
    c0.line(cx - 16, cy, cx + 16, cy, RED_LIGHT)
    c0.line(cx, cy - 16, cx, cy + 16, RED_LIGHT)
    c0.line(cx - 11, cy - 11, cx + 11, cy + 11, PURE_WHITE)
    c0.line(cx - 11, cy + 11, cx + 11, cy - 11, PURE_WHITE)
    for dx, dy in [(-8, -8), (8, -8), (-8, 8), (8, 8)]:
        c0.set_pixel(cx + dx, cy + dy, RED_LIGHT)
    frames.append(c0)

    # Frame 1: Exploding fabric triangles, umbrella ribs, and handle pieces
    c1 = PixelCanvas(48, 48, TRANSPARENT)
    # Red fabric shard top-left
    c1.polygon([(cx - 14, cy - 14), (cx - 8, cy - 18), (cx - 6, cy - 10)], RED_MID, outline=OUTLINE)
    c1.line(cx - 12, cy - 14, cx - 8, cy - 16, RED_LIGHT)
    # White fabric shard top-right
    c1.polygon([(cx + 14, cy - 14), (cx + 8, cy - 18), (cx + 6, cy - 10)], PURE_WHITE, outline=OUTLINE)
    c1.line(cx + 10, cy - 14, cx + 8, cy - 16, WHITE_SHADOW)
    # Red fabric shard bottom-right
    c1.polygon([(cx + 12, cy + 10), (cx + 16, cy + 14), (cx + 8, cy + 16)], RED_MID, outline=OUTLINE)
    # Wooden J handle piece bottom-left
    c1.polygon([(cx - 12, cy + 8), (cx - 15, cy + 13), (cx - 10, cy + 15)], BROWN_MID, outline=OUTLINE)
    # Metallic ribs flying out
    c1.line(cx - 16, cy - 2, cx - 10, cy - 1, METAL_MID)
    c1.line(cx + 10, cy + 2, cx + 16, cy + 3, METAL_MID)
    # Sparks
    for sx, sy in [(-18, 0), (18, 0), (0, -18), (0, 18), (-12, -12), (12, -12), (-12, 12), (12, 12)]:
        c1.set_pixel(cx + sx, cy + sy, RED_LIGHT)
        c1.set_pixel(cx + sx * 3 // 4, cy + sy * 3 // 4, PURE_WHITE)
    frames.append(c1)

    # Frame 2: Outer sparkling dust ring dispersing
    c2 = PixelCanvas(48, 48, TRANSPARENT)
    outer_sparks = [
        (-18, -14), (-14, -18), (14, -18), (18, -14),
        (18, 14), (14, 18), (-14, 18), (-18, 14),
        (0, -20), (0, 20), (-20, 0), (20, 0),
        (-10, -10), (10, -10), (-10, 10), (10, 10),
    ]
    for ox, oy in outer_sparks:
        c2.set_pixel(cx + ox, cy + oy, RED_LIGHT if (ox + oy) % 2 == 0 else PURE_WHITE)
    frames.append(c2)

    return frames

def generate_item_bridge() -> List[PixelCanvas]:
    """48x48, 6 frames, 8 fps, loop: true.
    Corrugated cardboard flat with tape, bobbing.
    """
    frames = []
    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cy = 24 + BOB_6[f]
        cx = 24

        # Cardboard folded flat slab: 36px wide by 18px tall
        # Top surface: isometric/tilted rectangle
        poly_top = [
            (cx - 17, cy - 6), (cx + 9, cy - 8),
            (cx + 17, cy + 2), (cx - 9, cy + 4)
        ]
        c.polygon(poly_top, WOOD_HIGHLIGHT, outline=OUTLINE)
        c.line(cx - 16, cy - 5, cx + 8, cy - 7, WOOD_LIT)

        # Cardboard side thickness
        poly_side = [
            (cx - 17, cy - 6), (cx - 9, cy + 4),
            (cx - 9, cy + 10), (cx - 17, cy)
        ]
        c.polygon(poly_side, BROWN_MID, outline=OUTLINE)

        # Cardboard front edge thickness with corrugation fluting notches
        poly_front = [
            (cx - 9, cy + 4), (cx + 17, cy + 2),
            (cx + 17, cy + 8), (cx - 9, cy + 10)
        ]
        c.polygon(poly_front, BROWN_DARK, outline=OUTLINE)
        # Visible fluting wave on front edge
        for fx_i in range(cx - 8, cx + 16, 3):
            c.set_pixel(fx_i, cy + 6, BROWN_DARKEST)
            c.set_pixel(fx_i + 1, cy + 7, BROWN_LIGHT)

        # Bright blue painter's tape strapping across the flat
        tape_poly = [
            (cx - 3, cy - 7), (cx + 3, cy - 7),
            (cx + 1, cy + 3), (cx - 5, cy + 3)
        ]
        c.polygon(tape_poly, BLUE_MID, outline=OUTLINE)
        c.line(cx - 2, cy - 6, cx + 2, cy - 6, BLUE_LIGHT)
        # Tape edge wrap around front
        c.rect(cx - 5, cy + 4, 6, 6, BLUE_MID, outline=OUTLINE)
        c.line(cx - 4, cy + 5, cx - 1, cy + 8, BLUE_LIGHT)

        # Glint sweep on tape and cardboard rim
        gx = cx - 14 + f * 5
        if cx - 16 <= gx <= cx + 16:
            c.set_pixel(gx, cy - 4, PURE_WHITE)
            c.set_pixel(gx + 1, cy - 4, YELLOW_LIGHT)

        frames.append(c)
    return frames

def generate_item_bridge_pop() -> List[PixelCanvas]:
    """48x48, 3 frames, 24 fps, loop: false. Cardboard confetti pop."""
    frames = []
    cx, cy = 24, 24

    # Frame 0: Flash with golden kraft cardboard burst
    c0 = PixelCanvas(48, 48, TRANSPARENT)
    c0.circle(cx, cy, 10, PURE_WHITE, outline=WOOD_LIT)
    c0.line(cx - 16, cy, cx + 16, cy, WOOD_LIT)
    c0.line(cx, cy - 16, cx, cy + 16, WOOD_LIT)
    c0.line(cx - 11, cy - 11, cx + 11, cy + 11, BLUE_LIGHT)
    c0.line(cx - 11, cy + 11, cx + 11, cy - 11, BLUE_LIGHT)
    frames.append(c0)

    # Frame 1: Cardboard rectangular shards & blue tape scraps flying outward
    c1 = PixelCanvas(48, 48, TRANSPARENT)
    # Cardboard chunks
    c1.polygon([(cx - 16, cy - 12), (cx - 9, cy - 16), (cx - 7, cy - 9), (cx - 14, cy - 6)], WOOD_HIGHLIGHT, outline=OUTLINE)
    c1.line(cx - 14, cy - 10, cx - 9, cy - 13, WOOD_LIT)
    c1.polygon([(cx + 8, cy - 14), (cx + 15, cy - 10), (cx + 12, cy - 5), (cx + 6, cy - 8)], BROWN_LIGHT, outline=OUTLINE)
    c1.polygon([(cx - 15, cy + 8), (cx - 8, cy + 10), (cx - 10, cy + 16), (cx - 16, cy + 13)], BROWN_MID, outline=OUTLINE)
    # Blue tape strips flying out
    c1.polygon([(cx + 6, cy + 8), (cx + 14, cy + 6), (cx + 16, cy + 12), (cx + 9, cy + 13)], BLUE_MID, outline=OUTLINE)
    c1.line(cx + 8, cy + 9, cx + 13, cy + 8, BLUE_LIGHT)
    c1.polygon([(cx - 2, cy - 18), (cx + 3, cy - 16), (cx + 1, cy - 11), (cx - 4, cy - 12)], BLUE_MID, outline=OUTLINE)
    # Cardboard fluting crumbs & sparks
    for sx, sy in [(-18, 0), (18, 0), (0, -18), (0, 18), (-10, -10), (10, -10), (-10, 10), (10, 10)]:
        c1.set_pixel(cx + sx, cy + sy, WOOD_LIT)
    frames.append(c1)

    # Frame 2: Dispersing dust and confetti
    c2 = PixelCanvas(48, 48, TRANSPARENT)
    outer_sparks = [
        (-18, -14), (-14, -18), (14, -18), (18, -14),
        (18, 14), (14, 18), (-14, 18), (-18, 14),
        (0, -20), (0, 20), (-20, 0), (20, 0),
        (-8, -8), (8, -8), (-8, 8), (8, 8),
    ]
    for ox, oy in outer_sparks:
        c2.set_pixel(cx + ox, cy + oy, BLUE_LIGHT if (ox + oy) % 3 == 0 else WOOD_LIT)
    frames.append(c2)

    return frames

def generate_bridge_plank() -> PixelCanvas:
    """240x32, 1 frame, 0 fps, loop: false.
    Placed cardboard bridge with tape strips, 16px overhang on each end,
    top edge flush with floor lip (y=0..4), middle 128px tileable/free of unique details.
    """
    c = PixelCanvas(240, 32, TRANSPARENT)
    # The plank spans x=0..239.
    # Height of cardboard slab: y=0 to y=20 (thick sturdy cardboard beam)
    # Top edge flush at y=0.

    # 1. Main cardboard slab fill
    for y in range(0, 20):
        for x in range(0, 240):
            if y == 0:
                c.set_pixel(x, y, WOOD_LIT)
            elif y <= 3:
                c.set_pixel(x, y, WOOD_HIGHLIGHT)
            elif y <= 12:
                # Kraft cardboard body
                c.set_pixel(x, y, BROWN_LIGHT)
            elif y <= 16:
                c.set_pixel(x, y, BROWN_MID)
            else:
                c.set_pixel(x, y, BROWN_DARK)

    # Outlines on top, bottom, left, right
    c.line(0, 0, 239, 0, OUTLINE)
    c.line(0, 19, 239, 19, OUTLINE)
    c.line(0, 0, 0, 19, OUTLINE)
    c.line(239, 0, 239, 19, OUTLINE)

    # 2. Corrugated fluting visible along the lower edge (y=13..18)
    # Wave fluting pattern repeating every 6px
    for x in range(1, 239):
        flute_phase = x % 6
        if flute_phase in (0, 1):
            c.set_pixel(x, 15, BROWN_DARKEST)
            c.set_pixel(x, 16, BROWN_DARKEST)
            c.set_pixel(x, 17, BROWN_DARK)
        elif flute_phase in (3, 4):
            c.set_pixel(x, 14, WOOD_HIGHLIGHT)
            c.set_pixel(x, 15, BROWN_LIGHT)

    # 3. 16px overhang on each end (x=0..15 and x=224..239)
    # Add ledge overlap bevel / tape reinforcement
    # Left end tape strip at x=10..18
    for tx in range(10, 18):
        for ty in range(0, 20):
            c.set_pixel(tx, ty, BLUE_MID)
        c.set_pixel(tx, 1, BLUE_LIGHT)
        c.set_pixel(tx, 18, BLUE_SHADOW)
    c.line(9, 0, 9, 19, OUTLINE)
    c.line(18, 0, 18, 19, OUTLINE)

    # Right end tape strip at x=222..230
    for tx in range(222, 230):
        for ty in range(0, 20):
            c.set_pixel(tx, ty, BLUE_MID)
        c.set_pixel(tx, 1, BLUE_LIGHT)
        c.set_pixel(tx, 18, BLUE_SHADOW)
    c.line(221, 0, 221, 19, OUTLINE)
    c.line(230, 0, 230, 19, OUTLINE)

    # Intermediate tape strip at transition (x=46..52 and x=188..194)
    # Leaving middle 128px (x=56..184) tileable / clean of unique tape
    for tx in range(46, 52):
        for ty in range(0, 20):
            c.set_pixel(tx, ty, BLUE_MID)
        c.set_pixel(tx, 1, BLUE_LIGHT)
    c.line(45, 0, 45, 19, OUTLINE)
    c.line(52, 0, 52, 19, OUTLINE)

    for tx in range(188, 194):
        for ty in range(0, 20):
            c.set_pixel(tx, ty, BLUE_MID)
        c.set_pixel(tx, 1, BLUE_LIGHT)
    c.line(187, 0, 187, 19, OUTLINE)
    c.line(194, 0, 194, 19, OUTLINE)

    # Cardboard printed stamp "FRAGILE / THIS SIDE UP" or arrows near ends (outside middle 128)
    # Left stamp (x=24..38, y=5..11): small red arrow pointing up
    c.polygon([(30, 5), (26, 9), (28, 9), (28, 12), (32, 12), (32, 9), (34, 9)], RED_MID, outline=OUTLINE)

    # 4. Under-bridge drop shadow / bottom lip
    c.line(0, 20, 239, 20, SHADOW_PURPLE_DARK)

    return c

def generate_bridge_land() -> List[PixelCanvas]:
    """240x48, 6 frames, 24 fps, loop: false. Dust puff along length, settling bounce."""
    frames = []
    w, h = 240, 48

    for f in range(6):
        c = PixelCanvas(w, h, TRANSPARENT)

        # Puff centers along length (at x=20, 50, 90, 120, 150, 190, 220)
        centers = [20, 50, 85, 120, 155, 190, 220]

        if f == 0:
            # Initial impact line & small sharp puffs along ground
            c.line(10, 44, 230, 44, PURE_WHITE)
            c.line(16, 45, 224, 45, WHITE_SHADOW)
            for cx in centers:
                c.circle(cx, 42, 4, PURE_WHITE, outline=OUTLINE)
        elif f in (1, 2):
            # Billowing dust clouds swelling upward
            r = 7 + f * 5
            for i, cx in enumerate(centers):
                cy = 38 - f * 4 + (i % 2) * 2
                c.circle(cx, cy, r, WHITE_SHADOW, outline=OUTLINE)
                c.circle(cx - 2, cy - 2, r - 3, PURE_WHITE)
                c.circle(cx + 3, cy + 2, r - 4, WHITE_MID)
        elif f == 3:
            # Clouds fragmenting and rising higher
            r = 14
            for i, cx in enumerate(centers):
                cy = 26 + (i % 2) * 4
                c.circle(cx - 3, cy, r - 3, WHITE_SHADOW, outline=OUTLINE)
                c.circle(cx - 4, cy - 2, r - 6, PURE_WHITE)
                c.circle(cx + 6, cy + 2, r - 5, WHITE_SHADOW, outline=OUTLINE)
        elif f in (4, 5):
            # Dispersing dust particles settling
            for i, cx in enumerate(centers):
                spread = (f - 3) * 6
                cy = 22 + (f - 4) * 8
                for dx, dy in [(-spread, 0), (spread, 2), (-spread // 2, -4), (spread // 2, 4)]:
                    px = cx + dx
                    py = cy + dy
                    if 0 <= px < w and 0 <= py < h:
                        c.rect(px - 1, py - 1, 2, 2, PURE_WHITE if f == 4 else WHITE_SHADOW)

        frames.append(c)
    return frames

def generate_fx_umbrella_canopy() -> List[PixelCanvas]:
    """64x48, 8 frames, 12 fps, loop: false.
    Opens above P1's head (bottom-center sits on head) in frames 1-3, gentle sway in frames 4-8.
    Bottom-center is at x=32, y=47.
    """
    frames = []
    # Canopy center anchor: cx=32, base_y=46 (sits on head)
    # Sway offsets for frames 3..7
    sway_x = [0, 0, 0, -2, -1, 1, 2, 0]
    sway_rot = [0, 0, 0, -1, 0, 1, 1, 0]

    for f in range(8):
        c = PixelCanvas(64, 48, TRANSPARENT)
        cx = 32 + sway_x[f]
        cy_base = 46

        if f == 0:
            # Frame 0: closed umbrella canopy bud (folded cloth pointing up)
            c.rect(cx - 3, cy_base - 22, 6, 22, RED_MID, outline=OUTLINE)
            c.line(cx - 2, cy_base - 21, cx + 2, cy_base - 21, PURE_WHITE)
            c.line(cx - 3, cy_base - 24, cx + 2, cy_base - 24, METAL_MID)
            c.set_pixel(cx, cy_base - 25, PURE_WHITE)
            # Folded ribs strap
            c.rect(cx - 3, cy_base - 12, 6, 3, BROWN_DARK, outline=OUTLINE)
        elif f == 1:
            # Frame 1: Opening halfway (flaring outward)
            poly_opening = [
                (cx, cy_base - 26), (cx + 12, cy_base - 10),
                (cx + 6, cy_base - 4), (cx - 6, cy_base - 4),
                (cx - 12, cy_base - 10)
            ]
            c.polygon(poly_opening, RED_MID, outline=OUTLINE)
            c.line(cx - 5, cy_base - 16, cx + 5, cy_base - 16, PURE_WHITE)
            c.set_pixel(cx, cy_base - 27, METAL_MID)
        elif f >= 2:
            # Frames 2..7: Full dome canopy
            # Dome apex at cy_base - 28, rim at cy_base - 6
            apex_y = cy_base - 28
            rim_y = cy_base - 6
            canopy_w = 26  # half width: 52px total canopy span

            for y in range(apex_y, rim_y + 1):
                prog = (y - apex_y) / float(rim_y - apex_y)
                hw = int(math.sin(prog * math.pi * 0.5) * canopy_w)
                lx = cx - hw
                rx = cx + hw

                c.set_pixel(lx, y, OUTLINE)
                c.set_pixel(rx, y, OUTLINE)
                if y == apex_y:
                    c.line(lx, y, rx, y, OUTLINE)
                    continue

                for x in range(lx + 1, rx):
                    rel = (x - (cx - canopy_w)) / float(canopy_w * 2)
                    panel = int(rel * 4)  # 4 panels: red, white, red, white
                    if panel % 2 == 0:
                        col = RED_LIGHT if y < apex_y + 8 and x <= cx else (RED_SHADOW if y > rim_y - 4 else RED_MID)
                    else:
                        col = PURE_WHITE if y < apex_y + 8 and x <= cx else (WHITE_SHADOW if y > rim_y - 4 else WHITE_MID)
                    c.set_pixel(x, y, col)

            # Scalloped bottom rim
            c.line(cx - canopy_w, rim_y, cx + canopy_w, rim_y, OUTLINE)
            for rx_i in [-canopy_w, -canopy_w // 2, 0, canopy_w // 2, canopy_w]:
                c.set_pixel(cx + rx_i, rim_y + 1, OUTLINE)
                c.set_pixel(cx + rx_i, rim_y, METAL_MID)

            # Ferrule top
            c.rect(cx - 1, apex_y - 4, 2, 4, METAL_MID, outline=OUTLINE)
            c.set_pixel(cx - 1, apex_y - 4, PURE_WHITE)

            # Shaft down to head
            c.line(cx, rim_y, cx, cy_base, OUTLINE)
            c.line(cx - 1, rim_y, cx - 1, cy_base, BROWN_MID)

        frames.append(c)
    return frames

# ==============================================================================
# A2. BEDTIME TIMER HUD
# ==============================================================================

def generate_ui_bedtime_clock() -> List[PixelCanvas]:
    """96x96, 12 frames, 0 fps, loop: false.
    Cartoon alarm clock face from plenty of time (f1) to midnight (f12),
    hands advancing, last 3 frames panicking (bell shaking, red tint on rim).
    """
    frames = []
    cx, cy = 48, 52  # clock dial center
    dial_r = 28

    for f in range(12):
        c = PixelCanvas(96, 96, TRANSPARENT)
        is_panic = (f >= 9)
        panic_shake = [-2, 2, -1][f - 9] if is_panic else 0

        ccx = cx + panic_shake
        ccy = cy

        # Twin bells on top
        bell_color = RED_LIGHT if is_panic else YELLOW_LIGHT
        bell_sh = RED_DEEP if is_panic else YELLOW_SHADOW
        bell_outline = OUTLINE

        # Left Bell at (ccx - 22, ccy - 28)
        c.polygon([
            (ccx - 28, ccy - 22), (ccx - 22, ccy - 34),
            (ccx - 14, ccy - 26), (ccx - 20, ccy - 18)
        ], fill=bell_color, outline=bell_outline)
        c.line(ccx - 24, ccy - 24, ccx - 20, ccy - 30, PURE_WHITE)
        c.line(ccx - 20, ccy - 20, ccx - 16, ccy - 24, bell_sh)

        # Right Bell at (ccx + 22, ccy - 28)
        c.polygon([
            (ccx + 28, ccy - 22), (ccx + 22, ccy - 34),
            (ccx + 14, ccy - 26), (ccx + 20, ccy - 18)
        ], fill=bell_color, outline=bell_outline)
        c.line(ccx + 20, ccy - 30, ccx + 24, ccy - 24, PURE_WHITE)
        c.line(ccx + 16, ccy - 24, ccx + 20, ccy - 20, bell_sh)

        # Bell striker hammer (center top)
        hammer_shift = [-2, 2, -1, 1][f % 4] if is_panic else 0
        c.rect(ccx - 2 + hammer_shift, ccy - 38, 4, 10, METAL_MID, outline=OUTLINE)
        c.circle(ccx + hammer_shift, ccy - 38, 3, METAL_SHADOW, outline=OUTLINE)

        # Peg feet at bottom
        c.polygon([(ccx - 22, ccy + 26), (ccx - 28, ccy + 38), (ccx - 20, ccy + 38)], METAL_SHADOW, outline=OUTLINE)
        c.polygon([(ccx + 22, ccy + 26), (ccx + 28, ccy + 38), (ccx + 20, ccy + 38)], METAL_SHADOW, outline=OUTLINE)

        # Clock Outer Casing (circular rim)
        rim_color = RED_MID if is_panic else BLUE_MID
        rim_light = RED_LIGHT if is_panic else BLUE_LIGHT
        rim_dark = RED_DEEP if is_panic else BLUE_SHADOW

        c.circle(ccx, ccy, dial_r + 5, rim_color, outline=OUTLINE)
        c.circle(ccx, ccy, dial_r + 4, rim_light)
        c.circle(ccx, ccy, dial_r + 2, rim_color)

        # Inner Dial Face (Creamy White)
        c.circle(ccx, ccy, dial_r, PURE_WHITE, outline=OUTLINE)
        for dy in range(-dial_r + 1, dial_r):
            for dx in range(-dial_r + 1, dial_r):
                if dx * dx + dy * dy < (dial_r - 1) ** 2:
                    if dy > dial_r // 2:
                        c.set_pixel(ccx + dx, ccy + dy, WHITE_SHADOW)
                    elif dx < -dial_r // 2:
                        c.set_pixel(ccx + dx, ccy + dy, PURE_WHITE)
                    else:
                        c.set_pixel(ccx + dx, ccy + dy, WHITE_MID)

        # Dial hour tick marks (12, 3, 6, 9)
        c.line(ccx, ccy - dial_r + 3, ccx, ccy - dial_r + 6, OUTLINE)  # 12
        c.line(ccx + dial_r - 6, ccy, ccx + dial_r - 3, ccy, OUTLINE)  # 3
        c.line(ccx, ccy + dial_r - 6, ccx, ccy + dial_r - 3, OUTLINE)  # 6
        c.line(ccx - dial_r + 3, ccy, ccx - dial_r + 6, ccy, OUTLINE)  # 9

        # Center pin
        c.circle(ccx, ccy, 3, METAL_SHADOW, outline=OUTLINE)
        c.set_pixel(ccx, ccy, PURE_WHITE)

        # Clock Hands advancing:
        # Frame 0 is 8:00 (hour hand at 8, minute at 12)
        # Frame 11 is 12:00 (both hands at 12 midnight!)
        # Hour angle advances from 240 deg (8 o'clock) to 360 deg (12 o'clock)
        # Minute hand advances from 0 deg through multiple revolutions
        h_prog = f / 11.0
        h_angle = (240.0 + h_prog * 120.0) * math.pi / 180.0
        m_angle = (f * 110.0) * math.pi / 180.0
        if f == 11:
            h_angle = 0.0  # exactly 12
            m_angle = 0.0

        # Draw Hour Hand (length ~14px, thick)
        hx = int(ccx + math.sin(h_angle) * 14)
        hy = int(ccy - math.cos(h_angle) * 14)
        c.line(ccx, ccy, hx, hy, OUTLINE)
        c.line(ccx + 1, ccy, hx + 1, hy, VOID_BLACK)

        # Draw Minute Hand (length ~21px, slim)
        mx = int(ccx + math.sin(m_angle) * 21)
        my = int(ccy - math.cos(m_angle) * 21)
        c.line(ccx, ccy, mx, my, OUTLINE)
        c.set_pixel(mx, my, RED_MID if is_panic else OUTLINE)

        # Panic effects: sweat drops & vibrating bell sound lines
        if is_panic:
            # Sweating drops
            c.polygon([(ccx + 12, ccy - 8), (ccx + 16, ccy - 4), (ccx + 14, ccy - 2)], BLUE_LIGHT, outline=OUTLINE)
            c.set_pixel(ccx + 14, ccy - 5, PURE_WHITE)
            # Vibration sound lines around bells
            c.line(ccx - 34, ccy - 30, ccx - 30, ccy - 34, RED_MID)
            c.line(ccx + 30, ccy - 34, ccx + 34, ccy - 30, RED_MID)
            c.line(ccx - 32, ccy - 22, ccx - 28, ccy - 24, RED_MID)
            c.line(ccx + 28, ccy - 24, ccx + 32, ccy - 22, RED_MID)

        frames.append(c)
    return frames

def generate_ui_bedtime_clock_ring() -> List[PixelCanvas]:
    """96x96, 6 frames, 16 fps, loop: true. Ringing animation (shaking clock with sound lines)."""
    frames = []
    cx, cy = 48, 52
    dial_r = 28
    shakes = [(-3, -1), (3, 1), (-2, 2), (2, -2), (-3, 0), (3, -1)]

    for f in range(6):
        c = PixelCanvas(96, 96, TRANSPARENT)
        sx, sy = shakes[f]
        ccx = cx + sx
        ccy = cy + sy

        # Vibrating bells
        for b_side, bx_off in [(-1, -22), (1, 22)]:
            c.polygon([
                (ccx + bx_off - 6, ccy - 22), (ccx + bx_off, ccy - 34),
                (ccx + bx_off + 8, ccy - 26), (ccx + bx_off + 2, ccy - 18)
            ], fill=RED_LIGHT, outline=OUTLINE)
            c.line(ccx + bx_off - 2, ccy - 30, ccx + bx_off + 4, ccy - 24, PURE_WHITE)

        # Hammer bouncing frantically between bells
        hx_off = -4 if f % 2 == 0 else 4
        c.rect(ccx + hx_off - 2, ccy - 38, 4, 10, METAL_MID, outline=OUTLINE)
        c.circle(ccx + hx_off, ccy - 38, 3, METAL_SHADOW, outline=OUTLINE)

        # Feet
        c.polygon([(ccx - 22, ccy + 26), (ccx - 28, ccy + 38), (ccx - 20, ccy + 38)], METAL_SHADOW, outline=OUTLINE)
        c.polygon([(ccx + 22, ccy + 26), (ccx + 28, ccy + 38), (ccx + 20, ccy + 38)], METAL_SHADOW, outline=OUTLINE)

        # Red alarmed clock body
        c.circle(ccx, ccy, dial_r + 5, RED_MID, outline=OUTLINE)
        c.circle(ccx, ccy, dial_r + 4, RED_LIGHT)
        c.circle(ccx, ccy, dial_r, PURE_WHITE, outline=OUTLINE)

        # Hands at 12:00 MIDNIGHT
        c.circle(ccx, ccy, 3, METAL_SHADOW, outline=OUTLINE)
        c.line(ccx, ccy, ccx, ccy - 16, OUTLINE)  # hour hand
        c.line(ccx + 1, ccy, ccx + 1, ccy - 16, VOID_BLACK)
        c.line(ccx, ccy, ccx, ccy - 22, RED_MID)  # minute hand

        # Dynamic Sound lines radiating violently
        ring_r = 40 + (f % 3) * 4
        for ang in [-0.8, -0.5, -0.2, 0.2, 0.5, 0.8]:
            p0x = int(ccx + math.sin(ang) * ring_r)
            p0y = int(ccy - math.cos(ang) * ring_r)
            p1x = int(ccx + math.sin(ang) * (ring_r + 6))
            p1y = int(ccy - math.cos(ang) * (ring_r + 6))
            c.line(p0x, p0y, p1x, p1y, YELLOW_LIGHT if f % 2 == 0 else RED_LIGHT)

        frames.append(c)
    return frames

def generate_ui_bedtime_moon() -> List[PixelCanvas]:
    """48x48, 4 frames, 0 fps, loop: false.
    Crescent moon with sleepy face: awake (f0), drowsy (f1), yawning (f2), asleep (f3).
    """
    frames = []
    cx, cy = 24, 24
    r_outer = 16
    r_inner = 13
    in_cx, in_cy = 29, 21

    for f in range(4):
        c = PixelCanvas(48, 48, TRANSPARENT)

        # Draw Crescent Moon shape
        for y in range(cy - r_outer - 1, cy + r_outer + 2):
            for x in range(cx - r_outer - 1, cx + r_outer + 2):
                d_out_sq = (x - cx) ** 2 + (y - cy) ** 2
                d_in_sq = (x - in_cx) ** 2 + (y - in_cy) ** 2
                is_in_crescent = (d_out_sq <= r_outer * r_outer and d_in_sq >= r_inner * r_inner)

                if is_in_crescent:
                    # Shading from bright left/top rim to rich yellow/gold
                    if d_out_sq > (r_outer - 1.5) ** 2:
                        c.set_pixel(x, y, OUTLINE)
                    elif d_in_sq < (r_inner + 1.5) ** 2:
                        c.set_pixel(x, y, OUTLINE)
                    elif x <= cx - 8:
                        c.set_pixel(x, y, PURE_WHITE)
                    elif x <= cx:
                        c.set_pixel(x, y, YELLOW_LIGHT)
                    else:
                        c.set_pixel(x, y, YELLOW_MID)

        # Expressive sleepy facial features:
        face_x, face_y = 19, 24

        if f == 0:
            # Awake: cute bright open eyes, happy grin
            # Left eye
            c.rect(face_x - 3, face_y - 3, 2, 3, OUTLINE)
            c.set_pixel(face_x - 3, face_y - 3, PURE_WHITE)
            # Right eye
            c.rect(face_x + 2, face_y - 3, 2, 3, OUTLINE)
            c.set_pixel(face_x + 2, face_y - 3, PURE_WHITE)
            # Cheerful smile
            c.set_pixel(face_x - 2, face_y + 2, OUTLINE)
            c.set_pixel(face_x - 1, face_y + 3, OUTLINE)
            c.set_pixel(face_x, face_y + 3, OUTLINE)
            c.set_pixel(face_x + 1, face_y + 2, OUTLINE)
            # Tiny cheek blush
            c.set_pixel(face_x - 4, face_y, DUSK_PINK)
            c.set_pixel(face_x + 4, face_y, DUSK_PINK)
        elif f == 1:
            # Drowsy: half-lidded heavy eyes, droopy smile
            # Left eye half-closed
            c.line(face_x - 4, face_y - 2, face_x - 1, face_y - 2, OUTLINE)
            c.set_pixel(face_x - 3, face_y - 1, OUTLINE)
            # Right eye half-closed
            c.line(face_x + 1, face_y - 2, face_x + 4, face_y - 2, OUTLINE)
            c.set_pixel(face_x + 2, face_y - 1, OUTLINE)
            # Droopy little smile
            c.line(face_x - 2, face_y + 3, face_x + 1, face_y + 3, OUTLINE)
        elif f == 2:
            # Yawning: eyes squeezed shut tight (> <), round open mouth O
            # Left squeeze eye
            c.line(face_x - 4, face_y - 4, face_x - 1, face_y - 2, OUTLINE)
            c.line(face_x - 4, face_y, face_x - 1, face_y - 2, OUTLINE)
            # Right squeeze eye
            c.line(face_x + 4, face_y - 4, face_x + 1, face_y - 2, OUTLINE)
            c.line(face_x + 4, face_y, face_x + 1, face_y - 2, OUTLINE)
            # Round mouth "O"
            c.circle(face_x, face_y + 3, 2, RED_SHADOW, outline=OUTLINE)
            c.set_pixel(face_x, face_y + 3, RED_DEEP)
            # Teardrop of yawn
            c.set_pixel(face_x - 5, face_y - 1, BLUE_LIGHT)
        elif f == 3:
            # Asleep: peaceful curved eyes (^ ^), nightcap on top, sleep Z
            # Left curved eye
            c.set_pixel(face_x - 3, face_y - 2, OUTLINE)
            c.set_pixel(face_x - 2, face_y - 3, OUTLINE)
            c.set_pixel(face_x - 1, face_y - 2, OUTLINE)
            # Right curved eye
            c.set_pixel(face_x + 1, face_y - 2, OUTLINE)
            c.set_pixel(face_x + 2, face_y - 3, OUTLINE)
            c.set_pixel(face_x + 3, face_y - 2, OUTLINE)
            # Tiny peaceful smile
            c.line(face_x - 1, face_y + 2, face_x + 1, face_y + 2, OUTLINE)
            # Nightcap on moon's upper tip (cx-2, cy-15)
            c.polygon([(cx - 2, cy - 14), (cx + 4, cy - 18), (cx + 12, cy - 14), (cx + 6, cy - 12)], PURPLE_MID, outline=OUTLINE)
            c.circle(cx + 14, cy - 14, 2, PURE_WHITE, outline=OUTLINE)
            # Floating sleep "z"
            c.line(34, 10, 38, 10, BLUE_LIGHT)
            c.line(38, 10, 34, 14, BLUE_LIGHT)
            c.line(34, 14, 38, 14, BLUE_LIGHT)

        frames.append(c)
    return frames

def generate_ui_bedtime_warning() -> List[PixelCanvas]:
    """960x540, 4 frames, 6 fps, loop: true.
    Thin red-purple screen-edge pulse overlay (hard-banded alpha, transparent middle).
    """
    frames = []
    w, h = 960, 540
    # Pulse alphas for 4 frames
    alpha_scales = [0.4, 0.7, 1.0, 0.6]

    for f in range(4):
        c = PixelCanvas(w, h, TRANSPARENT)
        scale = alpha_scales[f]

        # Edge thickness: 32px
        # 4 hard bands: 0..8px, 8..16px, 16..24px, 24..32px
        band_alphas = [
            int(180 * scale),
            int(120 * scale),
            int(70 * scale),
            int(30 * scale),
        ]

        # Top & Bottom strips
        for y in range(32):
            band_idx = y // 8
            a = band_alphas[band_idx]
            col = (RED_MID[0], RED_MID[1], RED_MID[2], a)
            for x in range(w):
                c.set_pixel(x, y, col)
                c.set_pixel(x, h - 1 - y, col)

        # Left & Right strips
        for x in range(32):
            band_idx = x // 8
            a = band_alphas[band_idx]
            col = (RED_MID[0], RED_MID[1], RED_MID[2], a)
            for y in range(32, h - 32):
                c.set_pixel(x, y, col)
                c.set_pixel(w - 1 - x, y, col)

        frames.append(c)
    return frames

def draw_pixel_text_bedtime(canvas: PixelCanvas, cx: int, cy: int):
    """Draws chunky 3D pixel font 'BEDTIME!' centered at (cx, cy)."""
    # 7-character string: "BEDTIME!"
    # Each letter ~18px wide, 24px tall, 4px spacing
    letters = {
        'B': [
            "11110",
            "10001",
            "11110",
            "10001",
            "11110"
        ],
        'E': [
            "11111",
            "10000",
            "11110",
            "10000",
            "11111"
        ],
        'D': [
            "11110",
            "10001",
            "10001",
            "10001",
            "11110"
        ],
        'T': [
            "11111",
            "00100",
            "00100",
            "00100",
            "00100"
        ],
        'I': [
            "11111",
            "00100",
            "00100",
            "00100",
            "11111"
        ],
        'M': [
            "10001",
            "11011",
            "10101",
            "10001",
            "10001"
        ],
        '!': [
            "00100",
            "00100",
            "00100",
            "00000",
            "00100"
        ]
    }

    word = "BEDTIME!"
    total_w = len(word) * 26
    start_x = cx - total_w // 2

    for l_idx, char in enumerate(word):
        grid = letters.get(char)
        if not grid:
            continue
        lx = start_x + l_idx * 26
        ly = cy - 12
        for r, row in enumerate(grid):
            for col_i, bit in enumerate(row):
                if bit == '1':
                    # Scale 1 bit to 3x4 block
                    bx = lx + col_i * 3
                    by = ly + r * 4
                    # 3D shadow underneath
                    canvas.rect(bx + 1, by + 2, 4, 5, OUTLINE)
                    # Text face fill
                    canvas.rect(bx, by, 3, 4, YELLOW_LIGHT, outline=OUTLINE)
                    canvas.set_pixel(bx, by, PURE_WHITE)

def generate_ui_banner_bedtime() -> List[PixelCanvas]:
    """384x96, 6 frames, 12 fps, loop: false.
    'BEDTIME!' stamp banner for game over. Text as pixel shape.
    """
    frames = []
    w, h = 384, 96

    for f in range(6):
        c = PixelCanvas(w, h, TRANSPARENT)
        # Slam drop animation
        y_slam = min(24, f * 8 if f < 4 else 24)

        # Nighttime deep purple stamp banner
        c.polygon([
            (24, y_slam), (360, y_slam),
            (344, y_slam + 52), (40, y_slam + 52)
        ], SHADOW_PURPLE_DEEP, outline=OUTLINE)
        c.line(26, y_slam + 2, 358, y_slam + 2, PURPLE_LIGHT)
        c.line(40, y_slam + 50, 344, y_slam + 50, SHADOW_PURPLE_DARK)

        # Gold decorative border trims
        c.line(30, y_slam + 6, 354, y_slam + 6, YELLOW_MID)
        c.line(44, y_slam + 46, 340, y_slam + 46, YELLOW_MID)

        # Draw "BEDTIME!" in bold 3D block letters
        draw_pixel_text_bedtime(c, w // 2, y_slam + 26)

        # Impact dust puffs & stars on landing frames (3..5)
        if f >= 3:
            for px in [36, 100, 192, 284, 348]:
                pr = 4 + (f - 3) * 3
                c.circle(px, y_slam + 54, pr, WHITE_SHADOW, outline=OUTLINE)
                c.circle(px, y_slam + 54, pr - 2, PURE_WHITE)
            # Sleep Zs floating up
            for zx, zy in [(60, y_slam - 6), (324, y_slam - 8)]:
                c.line(zx, zy, zx + 6, zy, BLUE_LIGHT)
                c.line(zx + 6, zy, zx, zy + 6, BLUE_LIGHT)
                c.line(zx, zy + 6, zx + 6, zy + 6, BLUE_LIGHT)

        frames.append(c)
    return frames

def generate_parent_bedtime() -> List[PixelCanvas]:
    """128x192, 8 frames, 10 fps, loop: false.
    Parent at bedroom door in robe, tapping wristwatch, then pointing at bed.
    """
    frames = []

    for f in range(8):
        c = PixelCanvas(128, 192, TRANSPARENT)

        # 1. Door frame / molding on right edge (x=112..127)
        c.rect(112, 0, 16, 192, BROWN_MID, outline=OUTLINE)
        c.line(112, 0, 112, 191, WOOD_HIGHLIGHT)
        c.line(113, 0, 113, 191, BROWN_LIGHT)
        c.line(125, 0, 125, 191, BROWN_DARKEST)
        c.line(127, 0, 127, 191, VOID_BLACK)

        # 2. Wooden door slab (x=84..112)
        door_x = 84
        c.rect(door_x, 0, 112 - door_x, 192, BROWN_DARKEST)
        c.line(door_x, 0, door_x, 191, WOOD_HIGHLIGHT)
        c.line(door_x + 1, 0, door_x + 1, 191, PURE_WHITE)
        # Brass doorknob
        c.rect(door_x + 4, 100, 6, 10, YELLOW_MID, outline=OUTLINE)
        c.set_pixel(door_x + 6, 102, YELLOW_LIGHT)

        # 3. Hallway light pouring in
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

        # 4. Imposing Parent Silhouette in doorway (x=44..92)
        for y in range(56, 184):
            bw = int(24 + (y - 56) * 0.28)
            bx0 = 68 - (bw // 2)
            bx1 = bx0 + bw
            c.rect(bx0, y, bw, 1, OUTLINE)
            c.rect(bx0 + 3, y, max(1, bw - 6), 1, SHADOW_DEEP)
            c.line(bx1 - 2, y, bx1 - 1, y, YELLOW_LIGHT)

        # Bathrobe belt
        c.rect(52, 104, 32, 6, SHADOW_MID, outline=OUTLINE)
        c.line(56, 110, 60, 126, PURPLE_LIGHT)

        # Head silhouette
        c.circle(64, 40, 16, OUTLINE)
        c.circle(64, 40, 13, SHADOW_DEEP)
        c.line(76, 32, 78, 48, YELLOW_LIGHT)

        # Curlers in hair
        curlers = [(52, 22), (64, 18), (76, 22), (82, 34)]
        for cx_c, cy_c in curlers:
            c.rect(cx_c - 4, cy_c - 4, 8, 6, PURPLE_LIGHT, outline=OUTLINE)
            c.rect(cx_c - 2, cy_c - 2, 4, 3, DUSK_PINK)

        # Stern glowing red eye
        c.circle(52, 40, 3, RED_LIGHT, outline=OUTLINE)
        c.set_pixel(52, 40, RED_MID)
        c.line(50, 39, 54, 39, OUTLINE)

        # Gestures:
        # Frames 0..3: Tapping wristwatch on left wrist with right index finger
        # Frames 4..7: Pointing firmly down-left toward bed!
        if f <= 3:
            # Raised left wrist with gold wristwatch at (36, 104)
            c.rect(34, 100, 16, 14, SHADOW_DEEP, outline=OUTLINE)
            # Gold wristwatch
            c.rect(38, 102, 8, 8, YELLOW_MID, outline=OUTLINE)
            c.rect(40, 104, 4, 4, PURE_WHITE)
            c.line(40, 100, 44, 100, BROWN_DARK)
            c.line(40, 110, 44, 110, BROWN_DARK)

            # Right arm tapping down on watch face:
            tap_y = 96 + (f % 2) * 4
            c.rect(42, tap_y - 8, 14, 14, SHADOW_DEEP, outline=OUTLINE)
            c.rect(38, tap_y - 2, 8, 6, SHADOW_DEEP, outline=OUTLINE)
            c.set_pixel(37, tap_y + 1, SKIN_MID)  # fingertip tapping watch
            if f % 2 == 1:
                # Tap shock wave tick
                c.set_pixel(34, 104, YELLOW_LIGHT)
                c.set_pixel(48, 104, YELLOW_LIGHT)
        else:
            # Powerful accusatory arm pointing down-left toward bed!
            point_y = 110 + (f - 4) * 4
            c.rect(48, 96, 20, 16, SHADOW_DEEP, outline=OUTLINE)
            # Forearm extending left-down
            c.polygon([(48, 100), (20, point_y), (22, point_y + 10), (48, 114)], SHADOW_DEEP, outline=OUTLINE)
            # Pointing finger
            c.rect(6, point_y + 2, 16, 6, SHADOW_DEEP, outline=OUTLINE)
            c.set_pixel(6, point_y + 4, SKIN_MID)
            c.set_pixel(4, point_y + 4, RED_LIGHT)  # sharp emphasis tip

        frames.append(c)
    return frames

def generate_parent_speech_bedtime() -> PixelCanvas:
    """192x96, 1 frame, 0 fps, loop: false. Speech bubble shape for 'BEDTIME!'."""
    c = PixelCanvas(192, 96, TRANSPARENT)
    num_teeth = 28
    cx, cy = 96, 42
    rx, ry = 86, 34

    coords_outer = []
    for i in range(num_teeth):
        angle = (i / num_teeth) * 2 * math.pi
        is_spike = (i % 2 == 1)
        r_mult = 1.15 if is_spike else 0.88
        ox = cx + math.cos(angle) * (rx * r_mult)
        oy = cy + math.sin(angle) * (ry * r_mult)
        coords_outer.append((ox, oy))

    outer_poly = [(int(x), int(y)) for x, y in coords_outer]
    outer_poly.extend([(136, 70), (160, 94), (150, 68)])

    c.polygon(outer_poly, PURE_WHITE, outline=OUTLINE)
    c.apply_selective_outline(OUTLINE)
    return c

# ==============================================================================
# A3. COOKIE
# ==============================================================================

def generate_item_cookie() -> List[PixelCanvas]:
    """48x48, 6 frames, 8 fps, loop: true.
    Big chocolate-chip cookie with golden shimmer, warmer and shinier than coin.
    """
    frames = []
    cx, cy_base = 24, 24
    r = 15

    # 5 chunky chocolate chips
    chips = [(-6, -5), (4, -7), (0, 0), (-7, 5), (6, 5)]

    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cy = cy_base + BOB_6[f]

        # Draw Cookie Disc with crinkled rustic edges
        for y in range(cy - r - 1, cy + r + 2):
            for x in range(cx - r - 1, cx + r + 2):
                d_sq = (x - cx) ** 2 + (y - cy) ** 2
                # Edge wobble
                angle = math.atan2(y - cy, x - cx)
                wobble = math.sin(angle * 8.0) * 1.2
                if d_sq <= (r + wobble) ** 2:
                    if d_sq > (r + wobble - 1.5) ** 2:
                        c.set_pixel(x, y, OUTLINE)
                    elif y <= cy - 6 and x <= cx:
                        c.set_pixel(x, y, WOOD_LIT)
                    elif y >= cy + 4:
                        c.set_pixel(x, y, BROWN_MID)
                    else:
                        c.set_pixel(x, y, BROWN_LIGHT)

        # Chocolate Chips with dark facet and warm specular
        for chx, chy in chips:
            chip_x = cx + chx
            chip_y = cy + chy
            c.rect(chip_x - 2, chip_y - 2, 4, 4, WOOD_BLACK, outline=OUTLINE)
            c.set_pixel(chip_x - 1, chip_y - 1, BROWN_DARK)
            c.set_pixel(chip_x, chip_y - 1, WOOD_HIGHLIGHT)

        # Golden shimmer glint sweep across frames 0..5
        glint_x = cx - 14 + f * 5
        for gy in range(cy - 10, cy + 8):
            if c.get_pixel(glint_x, gy) != TRANSPARENT and c.get_pixel(glint_x, gy) != OUTLINE:
                c.set_pixel(glint_x, gy, PURE_WHITE)
                c.set_pixel(glint_x + 1, gy, YELLOW_LIGHT)

        frames.append(c)
    return frames

def generate_item_cookie_pop() -> List[PixelCanvas]:
    """48x48, 4 frames, 24 fps, loop: false. Crumb burst with hearts."""
    frames = []
    cx, cy = 24, 24

    # Frame 0: Golden flash & cookie fracturing
    c0 = PixelCanvas(48, 48, TRANSPARENT)
    c0.circle(cx, cy, 10, PURE_WHITE, outline=WOOD_LIT)
    c0.line(cx - 16, cy, cx + 16, cy, YELLOW_LIGHT)
    c0.line(cx, cy - 16, cx, cy + 16, YELLOW_LIGHT)
    # Fracture cracks
    c0.line(cx - 6, cy - 6, cx + 6, cy + 6, BROWN_DARKEST)
    c0.line(cx - 6, cy + 6, cx + 6, cy - 6, BROWN_DARKEST)
    frames.append(c0)

    # Frame 1: Exploding golden cookie shards & cute pink hearts
    c1 = PixelCanvas(48, 48, TRANSPARENT)
    # Cookie shards
    c1.polygon([(cx - 14, cy - 12), (cx - 8, cy - 16), (cx - 6, cy - 8), (cx - 12, cy - 6)], BROWN_LIGHT, outline=OUTLINE)
    c1.polygon([(cx + 10, cy - 14), (cx + 16, cy - 8), (cx + 12, cy - 4), (cx + 6, cy - 8)], WOOD_HIGHLIGHT, outline=OUTLINE)
    c1.polygon([(cx - 12, cy + 8), (cx - 6, cy + 14), (cx - 14, cy + 14)], BROWN_MID, outline=OUTLINE)
    # Pink Hearts bursting out
    for hx, hy in [(-12, -4), (12, -4), (0, -14)]:
        # Draw 5x5 heart
        c1.polygon([(cx + hx - 2, cy + hy - 2), (cx + hx, cy + hy - 1), (cx + hx + 2, cy + hy - 2), (cx + hx, cy + hy + 2)], DUSK_ROSE, outline=OUTLINE)
        c1.set_pixel(cx + hx, cy + hy - 1, PURE_WHITE)
    # Chocolate crumbs
    for ch_x, ch_y in [(-8, 4), (6, 6), (0, 8), (14, 10), (-16, 2)]:
        c1.rect(cx + ch_x, cy + ch_y, 2, 2, WOOD_BLACK, outline=OUTLINE)
    frames.append(c1)

    # Frame 2: Floating expanding hearts & dispersing crumbs
    c2 = PixelCanvas(48, 48, TRANSPARENT)
    for hx, hy in [(-16, -10), (16, -10), (0, -18)]:
        c2.polygon([(cx + hx - 3, cy + hy - 2), (cx + hx, cy + hy - 1), (cx + hx + 3, cy + hy - 2), (cx + hx, cy + hy + 3)], DUSK_PINK, outline=OUTLINE)
        c2.set_pixel(cx + hx - 1, cy + hy - 1, PURE_WHITE)
    # Crumb dust
    for dx, dy in [(-18, -4), (18, -4), (-14, 14), (14, 14), (0, 18), (-8, -16), (8, -16)]:
        c2.set_pixel(cx + dx, cy + dy, WOOD_LIT)
    frames.append(c2)

    # Frame 3: Soft heart fading, tiny sparkling dust settling
    c3 = PixelCanvas(48, 48, TRANSPARENT)
    for hx, hy in [(-18, -14), (18, -14), (0, -20)]:
        c3.set_pixel(cx + hx, cy + hy, DUSK_BLUSH)
    for dx, dy in [(-20, 0), (20, 0), (-16, 16), (16, 16)]:
        c3.set_pixel(cx + dx, cy + dy, PURE_WHITE if (dx + dy) % 2 == 0 else YELLOW_LIGHT)
    frames.append(c3)

    return frames

def generate_parent_happy() -> List[PixelCanvas]:
    """128x192, 8 frames, 10 fps, loop: false.
    Parent in doorway takes a bite, closes eyes happily, nods.
    """
    frames = []

    for f in range(8):
        c = PixelCanvas(128, 192, TRANSPARENT)

        # 1. Door frame & slab
        door_x = 84
        c.rect(112, 0, 16, 192, BROWN_MID, outline=OUTLINE)
        c.line(112, 0, 112, 191, WOOD_HIGHLIGHT)
        c.rect(door_x, 0, 112 - door_x, 192, BROWN_DARKEST)
        c.line(door_x, 0, door_x, 191, WOOD_HIGHLIGHT)

        # Warm comforting amber hallway glow (calmed down!)
        for y in range(192):
            beam_left = max(12, int(door_x - 42 - (y * 0.4)))
            for x in range(beam_left, door_x):
                dist = door_x - x
                if dist < 16:
                    c.set_pixel(x, y, YELLOW_LIGHT)
                elif dist < 36:
                    c.set_pixel(x, y, YELLOW_MID if (x + y) % 2 == 0 else YELLOW_LIGHT)
                else:
                    if (x + y) % 3 == 0:
                        c.set_pixel(x, y, YELLOW_SHADOW)

        # Head nod offset
        nod_y = [0, 0, 1, 2, 2, 1, 3, 0][f]

        # 2. Parent Body
        for y in range(56 + nod_y, 184):
            bw = int(24 + (y - (56 + nod_y)) * 0.28)
            bx0 = 68 - (bw // 2)
            c.rect(bx0, y, bw, 1, OUTLINE)
            c.rect(bx0 + 3, y, max(1, bw - 6), 1, SHADOW_DEEP)

        c.rect(52, 104 + nod_y, 32, 6, SHADOW_MID, outline=OUTLINE)

        # Head
        hy = 40 + nod_y
        c.circle(64, hy, 16, OUTLINE)
        c.circle(64, hy, 13, SHADOW_DEEP)
        c.line(76, hy - 8, 78, hy + 8, YELLOW_LIGHT)

        # Curlers
        for cx_c, cy_c in [(52, hy - 18), (64, hy - 22), (76, hy - 18), (82, hy - 6)]:
            c.rect(cx_c - 4, cy_c - 4, 8, 6, PURPLE_LIGHT, outline=OUTLINE)
            c.rect(cx_c - 2, cy_c - 2, 4, 3, DUSK_PINK)

        # Expression:
        if f <= 1:
            # Bringing cookie to mouth
            c.circle(52, hy, 3, RED_LIGHT, outline=OUTLINE)  # eye looking down at cookie
            c.set_pixel(52, hy, RED_MID)
            # Hand holding cookie at (44, hy + 16)
            c.circle(44, hy + 16, 6, BROWN_LIGHT, outline=OUTLINE)  # cookie
            c.set_pixel(43, hy + 15, WOOD_BLACK)  # chip
        elif f == 2:
            # Taking a big crunch bite!
            c.line(50, hy, 54, hy, OUTLINE)  # closed eye in bite
            c.circle(48, hy + 6, 5, BROWN_LIGHT, outline=OUTLINE)  # cookie at mouth
            # Crunch crumbs flying
            c.set_pixel(42, hy + 4, WOOD_LIT)
            c.set_pixel(40, hy + 8, WOOD_LIT)
            c.set_pixel(44, hy + 12, WOOD_BLACK)
        else:
            # Frames 3..7: Blissfully chewing, happy closed eyes (^ ^), rosy cheeks, nodding
            # Happy curved closed eye
            c.set_pixel(50, hy - 1, OUTLINE)
            c.set_pixel(51, hy - 2, OUTLINE)
            c.set_pixel(52, hy - 2, OUTLINE)
            c.set_pixel(53, hy - 1, OUTLINE)
            # Cute rosy blush
            c.rect(48, hy + 2, 6, 3, DUSK_PINK)
            # Gentle content smile
            c.set_pixel(52, hy + 6, OUTLINE)
            c.set_pixel(53, hy + 7, OUTLINE)
            c.set_pixel(54, hy + 7, OUTLINE)
            c.set_pixel(55, hy + 6, OUTLINE)
            # Holding remaining half cookie in hand
            c.polygon([(40, hy + 18), (48, hy + 18), (44, hy + 24)], BROWN_LIGHT, outline=OUTLINE)
            c.set_pixel(43, hy + 20, WOOD_BLACK)
            # Floating hearts of calm
            if f in (4, 5, 6):
                c.set_pixel(34, hy - 8, DUSK_ROSE)
                c.set_pixel(36, hy - 10, DUSK_ROSE)
                c.set_pixel(35, hy - 9, PURE_WHITE)

        frames.append(c)
    return frames

def generate_fx_crumbs() -> List[PixelCanvas]:
    """16x16, 6 frames, 14 fps, loop: false. Cookie crumbs."""
    frames = []
    for f in range(6):
        c = PixelCanvas(16, 16, TRANSPARENT)
        # Crumbs falling down and spreading out
        y_fall = f * 2
        spread = f * 1.5

        # Crumb 1 (golden dough)
        c.rect(int(8 - spread), int(4 + y_fall), 2, 2, WOOD_LIT, outline=OUTLINE)
        # Crumb 2 (chocolate chip)
        c.rect(int(8 + spread * 0.8), int(3 + y_fall * 1.2), 2, 2, WOOD_BLACK, outline=OUTLINE)
        # Crumb 3 (tiny mote)
        c.set_pixel(int(8 + spread * 0.3), int(6 + y_fall * 1.4), BROWN_LIGHT)
        # Crumb 4 (tiny mote)
        c.set_pixel(int(8 - spread * 0.6), int(7 + y_fall * 0.8), WOOD_HIGHLIGHT)

        frames.append(c)
    return frames

def generate_fx_calm_wave() -> List[PixelCanvas]:
    """128x64, 6 frames, 16 fps, loop: false.
    Soft ring of hearts and sparkles spreading from parent's door (right edge toward left).
    """
    frames = []
    w, h = 128, 64
    door_origin_x = 120
    door_origin_y = 32

    for f in range(6):
        c = PixelCanvas(w, h, TRANSPARENT)
        rx = 18 + f * 18
        ry = 10 + f * 9

        # Draw soft wave ring arc (expanding leftward)
        for i in range(24):
            ang = math.pi * 0.5 + (i / 24.0) * math.pi
            px = int(door_origin_x + math.cos(ang) * rx)
            py = int(door_origin_y + math.sin(ang) * ry)
            if 0 <= px < w and 0 <= py < h:
                c.set_pixel(px, py, YELLOW_LIGHT if (i + f) % 2 == 0 else DUSK_BLUSH)

        # Hearts and sparkles floating on the crest
        for i, ang in enumerate([math.pi * 0.7, math.pi, math.pi * 1.3]):
            hx = int(door_origin_x + math.cos(ang) * rx)
            hy = int(door_origin_y + math.sin(ang) * ry)
            if 4 <= hx < w - 4 and 4 <= hy < h - 4:
                # Heart
                c.polygon([(hx - 2, hy - 2), (hx, hy - 1), (hx + 2, hy - 2), (hx, hy + 2)], DUSK_ROSE, outline=OUTLINE)
                c.set_pixel(hx, hy - 1, PURE_WHITE)
                # Sparkle near heart
                c.set_pixel(hx + 3, hy - 3, YELLOW_LIGHT)

        frames.append(c)
    return frames

# ==============================================================================
# A4. ACTIVE-BUFF STATUS HUD
# ==============================================================================

def generate_ui_status_ring() -> List[PixelCanvas]:
    """48x48, 16 frames, 0 fps, loop: false.
    Circular timer ring: frame 0 full, frame 15 empty, center open for buff icon.
    Outer radius R_out=21, Inner radius R_in=15. Center open for buff icon.
    """
    frames = []
    cx, cy = 24, 24
    r_out = 21
    r_in = 15

    for f in range(16):
        c = PixelCanvas(48, 48, TRANSPARENT)
        # Remaining proportion of circle: frame 0 is 1.0 (full), frame 15 is 0.0 (empty)
        remain = (15 - f) / 15.0
        max_angle = remain * 2.0 * math.pi

        for y in range(48):
            for x in range(48):
                d_sq = (x - cx) ** 2 + (y - cy) ** 2
                if r_in * r_in <= d_sq <= r_out * r_out:
                    # Angle starting from 12 o'clock (top) clockwise
                    # atan2 gives [-pi, pi], angle from -Y axis:
                    ang = math.atan2(x - cx, cy - y)
                    if ang < 0:
                        ang += 2.0 * math.pi

                    if ang <= max_angle and remain > 0:
                        is_edge = (d_sq >= (r_out - 1.2) ** 2 or d_sq <= (r_in + 1.2) ** 2)
                        if is_edge:
                            c.set_pixel(x, y, OUTLINE)
                        else:
                            # Gradient around ring: cyan to gold
                            c.set_pixel(x, y, TEAL_LIGHT if d_sq <= ((r_in + r_out) / 2) ** 2 else TEAL_HIGHLIGHT)
                    else:
                        # Faint track outline for empty portion
                        if d_sq >= (r_out - 0.8) ** 2 or d_sq <= (r_in + 0.8) ** 2:
                            c.set_pixel(x, y, SHADOW_PURPLE_DARK)

        frames.append(c)
    return frames

def generate_ui_status_bg() -> PixelCanvas:
    """56x56, 1 frame, 0 fps, loop: false. Rounded badge behind ring."""
    c = PixelCanvas(56, 56, TRANSPARENT)
    cx, cy = 28, 28
    r = 25

    # Rounded hexagonal / beveled badge
    for y in range(56):
        for x in range(56):
            d_sq = (x - cx) ** 2 + (y - cy) ** 2
            if d_sq <= r * r:
                if d_sq > (r - 2) ** 2:
                    c.set_pixel(x, y, OUTLINE)
                elif d_sq > (r - 4) ** 2:
                    # Beveled metallic rim
                    c.set_pixel(x, y, METAL_MID if y <= cy and x <= cx else METAL_SHADOW)
                else:
                    # Deep dark recessed interior
                    c.set_pixel(x, y, VOID_BLACK if d_sq > (r - 8) ** 2 else SHADOW_PURPLE_DEEP)

    # 4 corner rivets
    for rx, ry in [(12, 12), (44, 12), (12, 44), (44, 44)]:
        c.circle(rx, ry, 2, METAL_MID, outline=OUTLINE)
        c.set_pixel(rx - 1, ry - 1, PURE_WHITE)

    return c

# ==============================================================================
# A5. NEW POWERUP ICONS & PLACED PLACEABLES
# ==============================================================================

# 1. Slippers
def generate_item_slippers() -> List[PixelCanvas]:
    """Fluffy pink bunny slippers with floppy ears."""
    frames = []
    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cy = 24 + BOB_6[f]
        cx = 24

        # Fluffy slipper body
        c.polygon([
            (cx - 14, cy + 8), (cx + 12, cy + 8),
            (cx + 15, cy + 2), (cx + 12, cy - 2),
            (cx - 8, cy - 2), (cx - 14, cy + 2)
        ], DUSK_ROSE, outline=OUTLINE)
        c.line(cx - 12, cy, cx + 10, cy, DUSK_PINK)
        c.line(cx - 10, cy - 1, cx + 8, cy - 1, DUSK_BLUSH)

        # Fluffy white inner collar
        c.circle(cx - 4, cy - 2, 5, PURE_WHITE, outline=OUTLINE)
        c.circle(cx - 4, cy - 2, 3, WHITE_SHADOW)

        # Bunny Head at front (cx+10, cy)
        c.circle(cx + 10, cy + 1, 6, DUSK_PINK, outline=OUTLINE)
        c.set_pixel(cx + 9, cy, PURE_WHITE)
        # Bunny black eye & pink nose
        c.set_pixel(cx + 13, cy, OUTLINE)
        c.set_pixel(cx + 15, cy + 2, RED_MID)

        # Floppy Bunny Ears (bobbing)
        ear_droop = [0, 1, 2, 2, 1, 0][f]
        # Front ear
        c.polygon([
            (cx + 6, cy - 4), (cx + 4, cy - 12 - ear_droop),
            (cx + 1, cy - 11 - ear_droop), (cx + 3, cy - 3)
        ], DUSK_ROSE, outline=OUTLINE)
        c.line(cx + 3, cy - 5, cx + 3, cy - 10 - ear_droop, DUSK_BLUSH)
        # Back ear
        c.polygon([
            (cx + 11, cy - 4), (cx + 14, cy - 12 + ear_droop),
            (cx + 17, cy - 10 + ear_droop), (cx + 13, cy - 3)
        ], DUSK_ROSE, outline=OUTLINE)
        c.line(cx + 13, cy - 5, cx + 15, cy - 10 + ear_droop, DUSK_BLUSH)

        # White pom-pom tail on heel
        c.circle(cx - 14, cy + 4, 4, PURE_WHITE, outline=OUTLINE)

        # Glint sweep
        if f in (2, 3):
            c.set_pixel(cx + 8, cy - 1, PURE_WHITE)
            c.set_pixel(cx + 7, cy - 1, YELLOW_LIGHT)

        frames.append(c)
    return frames

def generate_item_slippers_pop() -> List[PixelCanvas]:
    frames = []
    cx, cy = 24, 24
    # Frame 0
    c0 = PixelCanvas(48, 48, TRANSPARENT)
    c0.circle(cx, cy, 10, PURE_WHITE, outline=DUSK_PINK)
    c0.line(cx - 16, cy, cx + 16, cy, DUSK_ROSE)
    c0.line(cx, cy - 16, cx, cy + 16, DUSK_ROSE)
    frames.append(c0)
    # Frame 1
    c1 = PixelCanvas(48, 48, TRANSPARENT)
    c1.polygon([(cx - 14, cy - 12), (cx - 8, cy - 16), (cx - 6, cy - 8)], DUSK_PINK, outline=OUTLINE)
    c1.polygon([(cx + 12, cy - 10), (cx + 16, cy - 4), (cx + 8, cy - 2)], DUSK_ROSE, outline=OUTLINE)
    c1.circle(cx - 10, cy + 10, 4, PURE_WHITE, outline=OUTLINE)  # pompom flying
    for sx, sy in [(-16, 0), (16, 0), (0, -16), (0, 16), (-10, -10), (10, -10)]:
        c1.set_pixel(cx + sx, cy + sy, DUSK_BLUSH)
    frames.append(c1)
    # Frame 2
    c2 = PixelCanvas(48, 48, TRANSPARENT)
    for ox, oy in [(-18, -12), (18, -12), (-12, 16), (12, 16), (0, -20), (0, 20)]:
        c2.set_pixel(cx + ox, cy + oy, PURE_WHITE if (ox + oy) % 2 == 0 else DUSK_BLUSH)
    frames.append(c2)
    return frames

# 2. Sugar (fizzing soda can)
def generate_item_sugar() -> List[PixelCanvas]:
    """Fizzing soda can (cyan and yellow) with popping bubbles."""
    frames = []
    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cy = 24 + BOB_6[f]
        cx = 24

        # Soda Can Cylinder: 18px wide, 26px tall (x: cx-9..cx+9, y: cy-13..cy+13)
        # Silver top rim
        c.polygon([
            (cx - 8, cy - 13), (cx + 8, cy - 13),
            (cx + 9, cy - 10), (cx - 9, cy - 10)
        ], METAL_MID, outline=OUTLINE)
        c.line(cx - 7, cy - 12, cx + 7, cy - 12, PURE_WHITE)

        # Pull tab at top
        c.rect(cx - 2, cy - 15, 4, 3, METAL_SHADOW, outline=OUTLINE)

        # Can Body
        for y in range(cy - 9, cy + 12):
            for x in range(cx - 9, cx + 10):
                # Diagonal cyan and yellow stripes
                is_yellow = ((x + y * 2) // 6) % 2 == 0
                col_main = YELLOW_MID if is_yellow else BLUE_MID
                col_light = YELLOW_LIGHT if is_yellow else BLUE_LIGHT
                col_dark = YELLOW_SHADOW if is_yellow else BLUE_SHADOW

                if x == cx - 9 or x == cx + 9:
                    c.set_pixel(x, y, OUTLINE)
                elif x <= cx - 5:
                    c.set_pixel(x, y, col_light)
                elif x >= cx + 5:
                    c.set_pixel(x, y, col_dark)
                else:
                    c.set_pixel(x, y, col_main)

        # Silver bottom rim
        c.rect(cx - 8, cy + 12, 16, 2, METAL_SHADOW, outline=OUTLINE)

        # Fizzing bubbles spurting from pull tab
        bubble_y = [cy - 16, cy - 20, cy - 23, cy - 18, cy - 21, cy - 19][f]
        c.circle(cx - 3, bubble_y, 2, BLUE_LIGHT, outline=OUTLINE)
        c.set_pixel(cx - 3, bubble_y, PURE_WHITE)
        c.circle(cx + 4, bubble_y - 2, 2, YELLOW_LIGHT, outline=OUTLINE)
        c.set_pixel(cx + 4, bubble_y - 2, PURE_WHITE)

        # Glint sweep
        c.line(cx - 4, cy - 8, cx - 4, cy + 10, PURE_WHITE)

        frames.append(c)
    return frames

def generate_item_sugar_pop() -> List[PixelCanvas]:
    frames = []
    cx, cy = 24, 24
    c0 = PixelCanvas(48, 48, TRANSPARENT)
    c0.circle(cx, cy, 10, PURE_WHITE, outline=YELLOW_MID)
    c0.line(cx - 16, cy, cx + 16, cy, BLUE_LIGHT)
    c0.line(cx, cy - 16, cx, cy + 16, YELLOW_LIGHT)
    frames.append(c0)

    c1 = PixelCanvas(48, 48, TRANSPARENT)
    c1.polygon([(cx - 14, cy - 12), (cx - 8, cy - 16), (cx - 6, cy - 8)], BLUE_MID, outline=OUTLINE)
    c1.polygon([(cx + 12, cy - 10), (cx + 16, cy - 4), (cx + 8, cy - 2)], YELLOW_MID, outline=OUTLINE)
    # Splash droplets
    for dx, dy in [(-12, -12), (12, -12), (-12, 12), (12, 12), (0, -18), (0, 18)]:
        c1.circle(cx + dx, cy + dy, 2, BLUE_LIGHT, outline=OUTLINE)
        c1.set_pixel(cx + dx, cy + dy, PURE_WHITE)
    frames.append(c1)

    c2 = PixelCanvas(48, 48, TRANSPARENT)
    for ox, oy in [(-18, -14), (18, -14), (-14, 18), (14, 18), (-20, 0), (20, 0)]:
        c2.set_pixel(cx + ox, cy + oy, PURE_WHITE if (ox + oy) % 2 == 0 else YELLOW_LIGHT)
    frames.append(c2)
    return frames

# 3. Stopwatch
def generate_item_stopwatch() -> List[PixelCanvas]:
    """Chunky silver stopwatch with glowing blue face."""
    frames = []
    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cy = 25 + BOB_6[f]
        cx = 24
        r = 14

        # Top winder and ring
        c.rect(cx - 2, cy - r - 6, 4, 4, METAL_MID, outline=OUTLINE)
        c.polygon([(cx - 4, cy - r - 8), (cx + 4, cy - r - 8), (cx + 4, cy - r - 6), (cx - 4, cy - r - 6)], METAL_MID, outline=OUTLINE)

        # Round silver casing
        c.circle(cx, cy, r + 2, METAL_MID, outline=OUTLINE)
        c.circle(cx, cy, r + 1, PURE_WHITE)

        # Glowing blue dial
        c.circle(cx, cy, r - 1, BLUE_MID, outline=OUTLINE)
        c.circle(cx, cy, r - 3, BLUE_LIGHT)

        # Dial ticks
        c.set_pixel(cx, cy - r + 3, PURE_WHITE)
        c.set_pixel(cx + r - 3, cy, PURE_WHITE)
        c.set_pixel(cx, cy + r - 3, PURE_WHITE)
        c.set_pixel(cx - r + 3, cy, PURE_WHITE)

        # Rotating tick hand
        ang = (f / 6.0) * 2.0 * math.pi
        hx = int(cx + math.sin(ang) * 9)
        hy = int(cy - math.cos(ang) * 9)
        c.line(cx, cy, hx, hy, OUTLINE)
        c.set_pixel(cx, cy, PURE_WHITE)

        # Glint reflection across glass
        c.line(cx - 8, cy - 6, cx - 4, cy - 10, PURE_WHITE)

        frames.append(c)
    return frames

def generate_item_stopwatch_pop() -> List[PixelCanvas]:
    frames = []
    cx, cy = 24, 24
    c0 = PixelCanvas(48, 48, TRANSPARENT)
    c0.circle(cx, cy, 10, PURE_WHITE, outline=BLUE_LIGHT)
    c0.line(cx - 16, cy, cx + 16, cy, METAL_MID)
    c0.line(cx, cy - 16, cx, cy + 16, METAL_MID)
    frames.append(c0)

    c1 = PixelCanvas(48, 48, TRANSPARENT)
    # Clockwork gears and glass shards
    c1.polygon([(cx - 14, cy - 10), (cx - 8, cy - 16), (cx - 6, cy - 8)], METAL_MID, outline=OUTLINE)
    c1.polygon([(cx + 10, cy - 12), (cx + 16, cy - 6), (cx + 8, cy - 4)], BLUE_LIGHT, outline=OUTLINE)
    # Gear
    c1.circle(cx - 8, cy + 10, 4, YELLOW_MID, outline=OUTLINE)
    c1.set_pixel(cx - 8, cy + 10, OUTLINE)
    for sx, sy in [(-16, 0), (16, 0), (0, -16), (0, 16)]:
        c1.set_pixel(cx + sx, cy + sy, BLUE_HIGHLIGHT)
    frames.append(c1)

    c2 = PixelCanvas(48, 48, TRANSPARENT)
    for ox, oy in [(-18, -14), (18, -14), (-14, 18), (14, 18), (-20, 0), (20, 0)]:
        c2.set_pixel(cx + ox, cy + oy, PURE_WHITE if (ox + oy) % 2 == 0 else BLUE_LIGHT)
    frames.append(c2)
    return frames

# 4. Bubblewrap
def generate_item_bubblewrap() -> List[PixelCanvas]:
    """Roll of bubble wrap with shimmering bubbles."""
    frames = []
    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cy = 24 + BOB_6[f]
        cx = 24

        # Cylindrical roll: 30px wide, 20px tall
        c.polygon([
            (cx - 15, cy - 8), (cx + 11, cy - 8),
            (cx + 15, cy - 2), (cx + 15, cy + 8),
            (cx - 11, cy + 8), (cx - 15, cy + 2)
        ], TEAL_LIGHT, outline=OUTLINE)

        # Bubble grid (rows of round translucent bubbles)
        for by_off in [-4, 0, 4]:
            for bx_off in [-10, -5, 0, 5, 10]:
                bx = cx + bx_off
                by = cy + by_off
                c.circle(bx, by, 2, WHITE_MID, outline=OUTLINE)
                c.set_pixel(bx - 1, by - 1, PURE_WHITE)

        # Shimmer glint
        glint_col = (f * 5) - 12
        c.circle(cx + glint_col, cy, 3, PURE_WHITE)

        frames.append(c)
    return frames

def generate_item_bubblewrap_pop() -> List[PixelCanvas]:
    frames = []
    cx, cy = 24, 24
    c0 = PixelCanvas(48, 48, TRANSPARENT)
    c0.circle(cx, cy, 10, PURE_WHITE, outline=TEAL_LIGHT)
    frames.append(c0)

    c1 = PixelCanvas(48, 48, TRANSPARENT)
    for bx, by in [(-12, -8), (10, -10), (-6, 12), (12, 8)]:
        c1.circle(cx + bx, cy + by, 3, PURE_WHITE, outline=OUTLINE)
    for sx, sy in [(-16, 0), (16, 0), (0, -16), (0, 16)]:
        c1.set_pixel(cx + sx, cy + sy, TEAL_HIGHLIGHT)
    frames.append(c1)

    c2 = PixelCanvas(48, 48, TRANSPARENT)
    for ox, oy in [(-18, -12), (18, -12), (-12, 16), (12, 16)]:
        c2.set_pixel(cx + ox, cy + oy, PURE_WHITE)
    frames.append(c2)
    return frames

# 5. Gloves
def generate_item_gloves() -> List[PixelCanvas]:
    """Sticky green gloves with visible gooey sheen."""
    frames = []
    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cy = 24 + BOB_6[f]
        cx = 24

        # Toy sticky hand/glove
        # Palm
        c.circle(cx, cy, 8, GREEN_MID, outline=OUTLINE)
        c.circle(cx - 2, cy - 2, 5, GREEN_LIGHT)

        # 4 Fingers extending up-left
        fingers = [(-7, -7), (-3, -11), (2, -12), (7, -8)]
        for fx_off, fy_off in fingers:
            c.circle(cx + fx_off, cy + fy_off, 3, GREEN_MID, outline=OUTLINE)
            c.set_pixel(cx + fx_off - 1, cy + fy_off - 1, GREEN_HIGHLIGHT)

        # Dripping gooey slime strand hanging off bottom
        drip_len = 6 + (f % 3) * 2
        c.polygon([
            (cx - 2, cy + 6), (cx + 2, cy + 6),
            (cx + 1, cy + 6 + drip_len), (cx - 1, cy + 6 + drip_len)
        ], GREEN_LIGHT, outline=OUTLINE)
        c.circle(cx, cy + 7 + drip_len, 2, GREEN_HIGHLIGHT, outline=OUTLINE)

        # Gooey gloss shine
        c.set_pixel(cx - 3, cy - 3, PURE_WHITE)
        c.set_pixel(cx - 2, cy - 3, PURE_WHITE)

        frames.append(c)
    return frames

def generate_item_gloves_pop() -> List[PixelCanvas]:
    frames = []
    cx, cy = 24, 24
    c0 = PixelCanvas(48, 48, TRANSPARENT)
    c0.circle(cx, cy, 10, PURE_WHITE, outline=GREEN_LIGHT)
    frames.append(c0)

    c1 = PixelCanvas(48, 48, TRANSPARENT)
    # Green slime splat
    for dx, dy in [(-12, -8), (14, -6), (-10, 12), (8, 14), (0, -16)]:
        c1.circle(cx + dx, cy + dy, 3, GREEN_MID, outline=OUTLINE)
        c1.set_pixel(cx + dx, cy + dy, GREEN_HIGHLIGHT)
    frames.append(c1)

    c2 = PixelCanvas(48, 48, TRANSPARENT)
    for ox, oy in [(-18, -12), (18, -12), (-14, 16), (14, 16)]:
        c2.set_pixel(cx + ox, cy + oy, GREEN_HIGHLIGHT)
    frames.append(c2)
    return frames

# 6. Trampoline
def generate_item_trampoline() -> List[PixelCanvas]:
    """Tiny red-and-blue mini trampoline (dropped item)."""
    frames = []
    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cy = 24 + BOB_6[f]
        cx = 24

        # Red padded rim
        c.polygon([
            (cx - 16, cy), (cx, cy - 6),
            (cx + 16, cy), (cx, cy + 6)
        ], RED_MID, outline=OUTLINE)
        c.polygon([
            (cx - 11, cy), (cx, cy - 4),
            (cx + 11, cy), (cx, cy + 4)
        ], BLUE_MID, outline=OUTLINE)
        c.set_pixel(cx, cy, BLUE_LIGHT)

        # 4 Steel legs
        for lx in [cx - 12, cx - 4, cx + 4, cx + 12]:
            c.line(lx, cy + 3, lx, cy + 10, METAL_MID)
            c.set_pixel(lx, cy + 10, OUTLINE)

        # Glint
        if f in (1, 2):
            c.set_pixel(cx - 6, cy - 3, PURE_WHITE)

        frames.append(c)
    return frames

def generate_item_trampoline_pop() -> List[PixelCanvas]:
    frames = []
    cx, cy = 24, 24
    c0 = PixelCanvas(48, 48, TRANSPARENT)
    c0.circle(cx, cy, 10, PURE_WHITE, outline=RED_MID)
    frames.append(c0)

    c1 = PixelCanvas(48, 48, TRANSPARENT)
    c1.polygon([(cx - 14, cy - 10), (cx - 8, cy - 14), (cx - 6, cy - 8)], RED_MID, outline=OUTLINE)
    c1.polygon([(cx + 10, cy - 12), (cx + 16, cy - 8), (cx + 8, cy - 4)], BLUE_MID, outline=OUTLINE)
    # Springs
    c1.line(cx - 8, cy + 8, cx - 12, cy + 14, METAL_MID)
    c1.line(cx + 8, cy + 8, cx + 12, cy + 14, METAL_MID)
    frames.append(c1)

    c2 = PixelCanvas(48, 48, TRANSPARENT)
    for ox, oy in [(-18, -12), (18, -12), (-12, 16), (12, 16)]:
        c2.set_pixel(cx + ox, cy + oy, RED_LIGHT if (ox + oy) % 2 == 0 else BLUE_LIGHT)
    frames.append(c2)
    return frames

# 7. Fan
def generate_item_fan() -> List[PixelCanvas]:
    """Small desk fan with spinning blades."""
    frames = []
    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cy = 24 + BOB_6[f]
        cx = 24

        # Base and stand
        c.polygon([(cx - 8, cy + 14), (cx + 8, cy + 14), (cx + 6, cy + 10), (cx - 6, cy + 10)], METAL_SHADOW, outline=OUTLINE)
        c.line(cx, cy + 6, cx, cy + 10, METAL_MID)

        # Wire cage
        c.circle(cx, cy, 11, TEAL_LIGHT, outline=OUTLINE)
        c.circle(cx, cy, 10, WHITE_SHADOW)

        # 3 Spinning Blades
        ang_base = (f / 6.0) * 2.0 * math.pi
        for b_i in range(3):
            ang = ang_base + b_i * (2.0 * math.pi / 3.0)
            bx = int(cx + math.sin(ang) * 7)
            by = int(cy - math.cos(ang) * 7)
            c.line(cx, cy, bx, by, BLUE_MID)
        c.circle(cx, cy, 2, METAL_MID, outline=OUTLINE)

        frames.append(c)
    return frames

def generate_item_fan_pop() -> List[PixelCanvas]:
    frames = []
    cx, cy = 24, 24
    c0 = PixelCanvas(48, 48, TRANSPARENT)
    c0.circle(cx, cy, 10, PURE_WHITE, outline=TEAL_LIGHT)
    frames.append(c0)

    c1 = PixelCanvas(48, 48, TRANSPARENT)
    # Spinning blades flying
    for ang in [0, 2.1, 4.2]:
        bx = int(cx + math.sin(ang) * 12)
        by = int(cy - math.cos(ang) * 12)
        c1.polygon([(bx - 2, by - 2), (bx + 2, by - 2), (bx, by + 4)], BLUE_MID, outline=OUTLINE)
    frames.append(c1)

    c2 = PixelCanvas(48, 48, TRANSPARENT)
    for ox, oy in [(-18, -12), (18, -12), (-12, 16), (12, 16)]:
        c2.set_pixel(cx + ox, cy + oy, TEAL_HIGHLIGHT)
    frames.append(c2)
    return frames

# 8. Tape
def generate_item_tape() -> List[PixelCanvas]:
    """Roll of bright blue painter's tape."""
    frames = []
    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cy = 24 + BOB_6[f]
        cx = 24
        r = 13

        # Blue tape roll
        c.circle(cx, cy, r, BLUE_MID, outline=OUTLINE)
        c.circle(cx, cy, r - 1, BLUE_LIGHT)

        # Cardboard inner core
        c.circle(cx, cy, 6, BROWN_MID, outline=OUTLINE)
        c.circle(cx, cy, 5, TRANSPARENT)

        # Peeling loose tape tab (pointing top-right)
        tab_y = cy - r + (f % 2)
        c.polygon([(cx + 6, cy - r + 3), (cx + 15, tab_y - 3), (cx + 14, tab_y + 2), (cx + 6, cy - r + 7)], BLUE_MID, outline=OUTLINE)
        c.line(cx + 7, cy - r + 4, cx + 14, tab_y - 2, BLUE_LIGHT)

        frames.append(c)
    return frames

def generate_item_tape_pop() -> List[PixelCanvas]:
    frames = []
    cx, cy = 24, 24
    c0 = PixelCanvas(48, 48, TRANSPARENT)
    c0.circle(cx, cy, 10, PURE_WHITE, outline=BLUE_LIGHT)
    frames.append(c0)

    c1 = PixelCanvas(48, 48, TRANSPARENT)
    # Fluttering tape strips
    c1.polygon([(cx - 14, cy - 10), (cx - 6, cy - 14), (cx - 8, cy - 8)], BLUE_MID, outline=OUTLINE)
    c1.polygon([(cx + 10, cy - 12), (cx + 16, cy - 6), (cx + 8, cy - 4)], BLUE_LIGHT, outline=OUTLINE)
    c1.polygon([(cx - 10, cy + 8), (cx - 4, cy + 14), (cx - 12, cy + 14)], BLUE_MID, outline=OUTLINE)
    frames.append(c1)

    c2 = PixelCanvas(48, 48, TRANSPARENT)
    for ox, oy in [(-18, -12), (18, -12), (-12, 16), (12, 16)]:
        c2.set_pixel(cx + ox, cy + oy, BLUE_HIGHLIGHT)
    frames.append(c2)
    return frames

# 9. Ramp
def generate_item_ramp() -> List[PixelCanvas]:
    """Wedge-shaped stack of books (dropped item)."""
    frames = []
    for f in range(6):
        c = PixelCanvas(48, 48, TRANSPARENT)
        cy = 24 + BOB_6[f]
        cx = 24

        # Bottom big blue book (flat)
        c.polygon([(cx - 14, cy + 4), (cx + 14, cy + 4), (cx + 12, cy + 10), (cx - 16, cy + 10)], BLUE_MID, outline=OUTLINE)
        c.line(cx - 13, cy + 5, cx + 13, cy + 5, BLUE_LIGHT)
        c.line(cx - 15, cy + 8, cx + 10, cy + 8, WHITE_SHADOW)  # page edges

        # Middle red book (stepped)
        c.polygon([(cx - 10, cy - 2), (cx + 14, cy - 2), (cx + 12, cy + 4), (cx - 12, cy + 4)], RED_MID, outline=OUTLINE)
        c.line(cx - 9, cy - 1, cx + 13, cy - 1, RED_LIGHT)

        # Top yellow book (forming wedge apex)
        c.polygon([(cx - 4, cy - 8), (cx + 14, cy - 8), (cx + 12, cy - 2), (cx - 6, cy - 2)], YELLOW_MID, outline=OUTLINE)
        c.line(cx - 3, cy - 7, cx + 13, cy - 7, YELLOW_LIGHT)

        # Red bookmark ribbon dangling down
        c.line(cx + 8, cy - 4, cx + 10, cy + 8, RED_LIGHT)

        frames.append(c)
    return frames

def generate_item_ramp_pop() -> List[PixelCanvas]:
    frames = []
    cx, cy = 24, 24
    c0 = PixelCanvas(48, 48, TRANSPARENT)
    c0.circle(cx, cy, 10, PURE_WHITE, outline=YELLOW_MID)
    frames.append(c0)

    c1 = PixelCanvas(48, 48, TRANSPARENT)
    # Book covers & fluttering pages
    c1.polygon([(cx - 14, cy - 10), (cx - 6, cy - 14), (cx - 8, cy - 8)], BLUE_MID, outline=OUTLINE)
    c1.polygon([(cx + 10, cy - 12), (cx + 16, cy - 6), (cx + 8, cy - 4)], RED_MID, outline=OUTLINE)
    c1.polygon([(cx - 10, cy + 8), (cx - 4, cy + 14), (cx - 12, cy + 14)], YELLOW_MID, outline=OUTLINE)
    # Fluttering white pages
    c1.polygon([(cx - 2, cy - 14), (cx + 4, cy - 12), (cx + 2, cy - 6)], PURE_WHITE, outline=OUTLINE)
    frames.append(c1)

    c2 = PixelCanvas(48, 48, TRANSPARENT)
    for ox, oy in [(-18, -12), (18, -12), (-12, 16), (12, 16)]:
        c2.set_pixel(cx + ox, cy + oy, PURE_WHITE if (ox + oy) % 2 == 0 else YELLOW_LIGHT)
    frames.append(c2)
    return frames

# ------------------------------------------------------------------------------
# 4 PLACED PLACEABLES (Bottom-anchored on bottom edge)
# ------------------------------------------------------------------------------

def generate_placed_trampoline() -> List[PixelCanvas]:
    """96x48, 6 frames @ 20 fps, loop: false (still frame 0, squash, launch, settle).
    Bottom-anchored at y=47.
    """
    frames = []
    w, h = 96, 48
    cx = 48
    bottom_y = 47

    # Frame mat y positions:
    # 0: Rest (y=26)
    # 1: Squash deep (y=38)
    # 2: Launch peak (y=14)
    # 3: Overshoot bounce down (y=22)
    # 4: Rebound up (y=28)
    # 5: Settle rest (y=26)
    mat_ys = [26, 38, 14, 22, 28, 26]

    for f in range(6):
        c = PixelCanvas(w, h, TRANSPARENT)
        my = mat_ys[f]

        # 4 Steel legs resting on floor at bottom_y=47
        legs = [(18, 16), (36, 32), (60, 64), (78, 80)]
        for rim_lx, foot_lx in legs:
            c.polygon([
                (rim_lx - 2, 26), (rim_lx + 2, 26),
                (foot_lx + 2, bottom_y), (foot_lx - 2, bottom_y)
            ], METAL_MID, outline=OUTLINE)
            # Rubber footpad touching bottom_y
            c.rect(foot_lx - 3, bottom_y - 2, 6, 3, WOOD_BLACK, outline=OUTLINE)

        # Red outer safety rim (fixed elliptical frame around y=26)
        c.polygon([
            (12, 26), (48, 18), (84, 26), (48, 34)
        ], RED_MID, outline=OUTLINE)
        c.polygon([
            (16, 26), (48, 20), (80, 26), (48, 32)
        ], RED_LIGHT)

        # Bouncing Jumping Mat (moves dynamically with my)
        c.polygon([
            (20, 26), (48, my - 4), (76, 26), (48, my + 4)
        ], BLUE_MID, outline=OUTLINE)
        c.line(22, 26, 74, 26, BLUE_LIGHT)

        # Launch motion lines on frame 2
        if f == 2:
            c.line(44, 8, 44, 12, PURE_WHITE)
            c.line(48, 6, 48, 12, PURE_WHITE)
            c.line(52, 8, 52, 12, PURE_WHITE)

        frames.append(c)
    return frames

def generate_placed_ramp() -> PixelCanvas:
    """96x48, 1 frame, wedge of books, low side facing left. Bottom anchored at y=47."""
    c = PixelCanvas(96, 48, TRANSPARENT)
    bottom_y = 47

    # Wedge slope from left (x=6, height=4 at y=43) to right (x=90, height=36 at y=11)
    # Stacked encyclopedias and textbooks
    # Book 1 (bottom-most blue encyclopedia, spans x=6..90, y=39..47)
    c.polygon([(6, 43), (90, 39), (90, bottom_y), (6, bottom_y)], BLUE_MID, outline=OUTLINE)
    c.line(7, 44, 89, 40, BLUE_LIGHT)
    c.line(8, 46, 88, 46, WHITE_SHADOW)  # page edges

    # Book 2 (red dictionary, spans x=20..90, y=29..39)
    c.polygon([(20, 35), (90, 29), (90, 39), (20, 39)], RED_MID, outline=OUTLINE)
    c.line(21, 36, 89, 30, RED_LIGHT)
    c.line(22, 38, 88, 38, WHITE_SHADOW)

    # Book 3 (green textbook, spans x=36..90, y=19..29)
    c.polygon([(36, 25), (90, 19), (90, 29), (36, 29)], GREEN_MID, outline=OUTLINE)
    c.line(37, 26, 89, 20, GREEN_LIGHT)
    c.line(38, 28, 88, 28, WHITE_SHADOW)

    # Book 4 (top yellow hardback, spans x=54..90, y=11..19)
    c.polygon([(54, 15), (90, 11), (90, 19), (54, 19)], YELLOW_MID, outline=OUTLINE)
    c.line(55, 16, 89, 12, YELLOW_LIGHT)
    c.line(56, 18, 88, 18, WHITE_SHADOW)

    # Colorful spine labels & bookmark ribbons
    c.line(84, 15, 84, 32, RED_LIGHT)  # ribbon hanging off side

    return c

def generate_placed_fan() -> List[PixelCanvas]:
    """64x64, 8 frames @ 16 fps, loop: true.
    Blast of wind lines coming off right side (white hard-banded alpha at 60%).
    Bottom anchored at y=63.
    """
    frames = []
    w, h = 64, 64
    bottom_y = 63
    fan_cx, fan_cy = 18, 38

    for f in range(8):
        c = PixelCanvas(w, h, TRANSPARENT)

        # 1. Sturdy desk fan stand on floor
        c.polygon([
            (fan_cx - 12, bottom_y), (fan_cx + 12, bottom_y),
            (fan_cx + 8, bottom_y - 6), (fan_cx - 8, bottom_y - 6)
        ], METAL_SHADOW, outline=OUTLINE)
        c.rect(fan_cx - 2, fan_cy + 10, 4, bottom_y - 6 - (fan_cy + 10), METAL_MID, outline=OUTLINE)

        # 2. Wire Cage
        c.circle(fan_cx, fan_cy, 14, TEAL_LIGHT, outline=OUTLINE)
        c.circle(fan_cx, fan_cy, 13, WHITE_SHADOW)

        # 3. Spinning propeller blades
        ang_base = (f / 8.0) * 2.0 * math.pi
        for b_i in range(3):
            ang = ang_base + b_i * (2.0 * math.pi / 3.0)
            bx = int(fan_cx + math.sin(ang) * 9)
            by = int(fan_cy - math.cos(ang) * 9)
            c.line(fan_cx, fan_cy, bx, by, BLUE_MID)
        c.circle(fan_cx, fan_cy, 3, METAL_MID, outline=OUTLINE)

        # 4. Powerful wind lines blasting off to the right (x: 32..63)
        # Using hard-banded alpha at 60% (153) as allowed by art brief
        alpha_60 = 153
        wind_col = (PURE_WHITE[0], PURE_WHITE[1], PURE_WHITE[2], alpha_60)

        # 3 horizontal wind streaks with flutter
        y_offsets = [fan_cy - 8, fan_cy, fan_cy + 8]
        for idx, wy in enumerate(y_offsets):
            x_shift = (f * 4 + idx * 7) % 16
            for wx in range(32 + x_shift, min(63, 48 + x_shift)):
                c.set_pixel(wx, wy, wind_col)
                if wx % 3 == 0:
                    c.set_pixel(wx, wy - 1, wind_col)

        frames.append(c)
    return frames

def generate_placed_tape() -> PixelCanvas:
    """64x16, 1 frame, 0 fps, loop: false.
    Strip of blue tape flat on ground, slightly curled at ends.
    Bottom anchored at y=15.
    """
    c = PixelCanvas(64, 16, TRANSPARENT)
    bottom_y = 15

    # Main flat body along ground from x=6 to x=57, y=11..15
    for x in range(6, 58):
        c.set_pixel(x, 11, OUTLINE)
        c.set_pixel(x, 12, BLUE_LIGHT)
        c.set_pixel(x, 13, BLUE_MID)
        c.set_pixel(x, 14, BLUE_MID)
        c.set_pixel(x, bottom_y, OUTLINE)

    # Left curled end (peeling up to y=7)
    c.polygon([
        (2, 7), (6, 11), (8, 14), (4, 14)
    ], BLUE_LIGHT, outline=OUTLINE)
    c.set_pixel(3, 8, PURE_WHITE)

    # Right curled end (peeling up to y=6)
    c.polygon([
        (61, 6), (57, 11), (55, 14), (59, 14)
    ], BLUE_LIGHT, outline=OUTLINE)
    c.set_pixel(60, 7, PURE_WHITE)

    # Wrinkle creases in middle
    c.line(24, 12, 25, 14, BLUE_LIGHT)
    c.line(42, 12, 43, 14, BLUE_LIGHT)

    return c

# ==============================================================================
# MANIFEST REGISTRATION & ORCHESTRATION
# ==============================================================================

MANIFEST_UPDATES = {
    # A1
    "item_umbrella.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True},
    "item_umbrella_pop.png": {"frame_w": 48, "frame_h": 48, "frames": 3, "fps": 24, "loop": False},
    "item_bridge.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True},
    "item_bridge_pop.png": {"frame_w": 48, "frame_h": 48, "frames": 3, "fps": 24, "loop": False},
    "bridge_plank.png": {"frame_w": 240, "frame_h": 32, "frames": 1, "fps": 0, "loop": False},
    "bridge_land.png": {"frame_w": 240, "frame_h": 48, "frames": 6, "fps": 24, "loop": False},
    "fx_umbrella_canopy.png": {"frame_w": 64, "frame_h": 48, "frames": 8, "fps": 12, "loop": False},

    # A2
    "ui_bedtime_clock.png": {"frame_w": 96, "frame_h": 96, "frames": 12, "fps": 0, "loop": False},
    "ui_bedtime_clock_ring.png": {"frame_w": 96, "frame_h": 96, "frames": 6, "fps": 16, "loop": True},
    "ui_bedtime_moon.png": {"frame_w": 48, "frame_h": 48, "frames": 4, "fps": 0, "loop": False},
    "ui_bedtime_warning.png": {"frame_w": 960, "frame_h": 540, "frames": 4, "fps": 6, "loop": True},
    "ui_banner_bedtime.png": {"frame_w": 384, "frame_h": 96, "frames": 6, "fps": 12, "loop": False},
    "parent_bedtime.png": {"frame_w": 128, "frame_h": 192, "frames": 8, "fps": 10, "loop": False},
    "parent_speech_bedtime.png": {"frame_w": 192, "frame_h": 96, "frames": 1, "fps": 0, "loop": False},

    # A3
    "item_cookie.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True},
    "item_cookie_pop.png": {"frame_w": 48, "frame_h": 48, "frames": 4, "fps": 24, "loop": False},
    "parent_happy.png": {"frame_w": 128, "frame_h": 192, "frames": 8, "fps": 10, "loop": False},
    "fx_crumbs.png": {"frame_w": 16, "frame_h": 16, "frames": 6, "fps": 14, "loop": False},
    "fx_calm_wave.png": {"frame_w": 128, "frame_h": 64, "frames": 6, "fps": 16, "loop": False},

    # A4
    "ui_status_ring.png": {"frame_w": 48, "frame_h": 48, "frames": 16, "fps": 0, "loop": False},
    "ui_status_bg.png": {"frame_w": 56, "frame_h": 56, "frames": 1, "fps": 0, "loop": False},

    # A5 Items + Pops
    "item_slippers.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True},
    "item_slippers_pop.png": {"frame_w": 48, "frame_h": 48, "frames": 3, "fps": 24, "loop": False},
    "item_sugar.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True},
    "item_sugar_pop.png": {"frame_w": 48, "frame_h": 48, "frames": 3, "fps": 24, "loop": False},
    "item_stopwatch.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True},
    "item_stopwatch_pop.png": {"frame_w": 48, "frame_h": 48, "frames": 3, "fps": 24, "loop": False},
    "item_bubblewrap.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True},
    "item_bubblewrap_pop.png": {"frame_w": 48, "frame_h": 48, "frames": 3, "fps": 24, "loop": False},
    "item_gloves.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True},
    "item_gloves_pop.png": {"frame_w": 48, "frame_h": 48, "frames": 3, "fps": 24, "loop": False},
    "item_trampoline.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True},
    "item_trampoline_pop.png": {"frame_w": 48, "frame_h": 48, "frames": 3, "fps": 24, "loop": False},
    "item_fan.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True},
    "item_fan_pop.png": {"frame_w": 48, "frame_h": 48, "frames": 3, "fps": 24, "loop": False},
    "item_tape.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True},
    "item_tape_pop.png": {"frame_w": 48, "frame_h": 48, "frames": 3, "fps": 24, "loop": False},
    "item_ramp.png": {"frame_w": 48, "frame_h": 48, "frames": 6, "fps": 8, "loop": True},
    "item_ramp_pop.png": {"frame_w": 48, "frame_h": 48, "frames": 3, "fps": 24, "loop": False},

    # A5 Placed Placeables
    "placed_trampoline.png": {"frame_w": 96, "frame_h": 48, "frames": 6, "fps": 20, "loop": False},
    "placed_ramp.png": {"frame_w": 96, "frame_h": 48, "frames": 1, "fps": 0, "loop": False},
    "placed_fan.png": {"frame_w": 64, "frame_h": 64, "frames": 8, "fps": 16, "loop": True},
    "placed_tape.png": {"frame_w": 64, "frame_h": 16, "frames": 1, "fps": 0, "loop": False},
}

def generate_all_phase_a():
    out_dir = Path("art/v2")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=== Generating Phase A Assets ===")

    # A1
    assemble_strip(generate_item_umbrella(), str(out_dir / "item_umbrella.png"))
    assemble_strip(generate_item_umbrella_pop(), str(out_dir / "item_umbrella_pop.png"))
    assemble_strip(generate_item_bridge(), str(out_dir / "item_bridge.png"))
    assemble_strip(generate_item_bridge_pop(), str(out_dir / "item_bridge_pop.png"))
    save_single(generate_bridge_plank(), str(out_dir / "bridge_plank.png"))
    assemble_strip(generate_bridge_land(), str(out_dir / "bridge_land.png"))
    assemble_strip(generate_fx_umbrella_canopy(), str(out_dir / "fx_umbrella_canopy.png"))

    # A2
    assemble_strip(generate_ui_bedtime_clock(), str(out_dir / "ui_bedtime_clock.png"))
    assemble_strip(generate_ui_bedtime_clock_ring(), str(out_dir / "ui_bedtime_clock_ring.png"))
    assemble_strip(generate_ui_bedtime_moon(), str(out_dir / "ui_bedtime_moon.png"))
    assemble_strip(generate_ui_bedtime_warning(), str(out_dir / "ui_bedtime_warning.png"))
    assemble_strip(generate_ui_banner_bedtime(), str(out_dir / "ui_banner_bedtime.png"))
    assemble_strip(generate_parent_bedtime(), str(out_dir / "parent_bedtime.png"))
    save_single(generate_parent_speech_bedtime(), str(out_dir / "parent_speech_bedtime.png"))

    # A3
    assemble_strip(generate_item_cookie(), str(out_dir / "item_cookie.png"))
    assemble_strip(generate_item_cookie_pop(), str(out_dir / "item_cookie_pop.png"))
    assemble_strip(generate_parent_happy(), str(out_dir / "parent_happy.png"))
    assemble_strip(generate_fx_crumbs(), str(out_dir / "fx_crumbs.png"))
    assemble_strip(generate_fx_calm_wave(), str(out_dir / "fx_calm_wave.png"))

    # A4
    assemble_strip(generate_ui_status_ring(), str(out_dir / "ui_status_ring.png"))
    save_single(generate_ui_status_bg(), str(out_dir / "ui_status_bg.png"))

    # A5 Items + Pops
    assemble_strip(generate_item_slippers(), str(out_dir / "item_slippers.png"))
    assemble_strip(generate_item_slippers_pop(), str(out_dir / "item_slippers_pop.png"))
    assemble_strip(generate_item_sugar(), str(out_dir / "item_sugar.png"))
    assemble_strip(generate_item_sugar_pop(), str(out_dir / "item_sugar_pop.png"))
    assemble_strip(generate_item_stopwatch(), str(out_dir / "item_stopwatch.png"))
    assemble_strip(generate_item_stopwatch_pop(), str(out_dir / "item_stopwatch_pop.png"))
    assemble_strip(generate_item_bubblewrap(), str(out_dir / "item_bubblewrap.png"))
    assemble_strip(generate_item_bubblewrap_pop(), str(out_dir / "item_bubblewrap_pop.png"))
    assemble_strip(generate_item_gloves(), str(out_dir / "item_gloves.png"))
    assemble_strip(generate_item_gloves_pop(), str(out_dir / "item_gloves_pop.png"))
    assemble_strip(generate_item_trampoline(), str(out_dir / "item_trampoline.png"))
    assemble_strip(generate_item_trampoline_pop(), str(out_dir / "item_trampoline_pop.png"))
    assemble_strip(generate_item_fan(), str(out_dir / "item_fan.png"))
    assemble_strip(generate_item_fan_pop(), str(out_dir / "item_fan_pop.png"))
    assemble_strip(generate_item_tape(), str(out_dir / "item_tape.png"))
    assemble_strip(generate_item_tape_pop(), str(out_dir / "item_tape_pop.png"))
    assemble_strip(generate_item_ramp(), str(out_dir / "item_ramp.png"))
    assemble_strip(generate_item_ramp_pop(), str(out_dir / "item_ramp_pop.png"))

    # A5 Placed Placeables
    assemble_strip(generate_placed_trampoline(), str(out_dir / "placed_trampoline.png"))
    save_single(generate_placed_ramp(), str(out_dir / "placed_ramp.png"))
    assemble_strip(generate_placed_fan(), str(out_dir / "placed_fan.png"))
    save_single(generate_placed_tape(), str(out_dir / "placed_tape.png"))

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
    print(f"Updated {manifest_path} with {len(MANIFEST_UPDATES)} Phase A entries.")

if __name__ == "__main__":
    generate_all_phase_a()
