"""Younger Sibling Simulator - Parallax Backgrounds Generator.

Generates the 5 parallax background layers:
- bg_sky_gradient.png (1x270): 8 discrete hard color bands from dusk purple to warm plum.
- bg_far.png (480x270): Seamless horizontal tiling, diamond wallpaper, baseboard,
                       large window looking out to moon & stars, framed crayon drawing,
                       retro toy rocket poster.
- bg_far_stars.png (1920x270, 4 frames of 480x270, 3fps): Window star twinkle animation overlay.
- bg_mid.png (640x270): Seamless horizontal tiling, floor level at y=200, tall bookshelf
                       with colorful book spines, bedside nightstand with brass knobs & glowing lamp,
                       sibling's bed with soft pillow & quilted blue blanket, wooden toy chest with
                       cute peeking dinosaur.
- bg_near.png (480x270): Transparent above y=200, dark foreground toy silhouettes (teddy bear,
                        wooden locomotive & coal car, stacked block towers, rocking horse)
                        with crisp 1px upper-left rim lighting in pale purple.
"""

import math
from typing import List, Tuple
from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE,
    SHADOW_DEEP, SHADOW_MID, PURPLE_MID, PURPLE_LIGHT, DUSK_PINK, DUSK_PEACH,
    SKIN_MID, SKIN_LIGHT, SKIN_SHADOW,
    BROWN_DARKEST, BROWN_DARK, BROWN_MID, BROWN_LIGHT, WOOD_HIGHLIGHT,
    RED_SHADOW, RED_MID, RED_LIGHT,
    BLUE_SHADOW, BLUE_MID, BLUE_LIGHT,
    YELLOW_SHADOW, YELLOW_MID, YELLOW_LIGHT,
    GREEN_SHADOW, GREEN_MID, GREEN_LIGHT,
    ORANGE_SHADOW, ORANGE_MID,
    WHITE_SHADOW, PURE_WHITE,
    VOID_BLACK
)


def generate_bg_sky_gradient() -> PixelCanvas:
    """
    1x270 vertical strip.
    8 discrete hard color bands (no smooth blending).
    Transitions from deepest dusk purple/indigo down to luminous warm plum.
    """
    c = PixelCanvas(1, 270)
    # 8 bands summing to exactly 270: 34*6 + 33*2 = 204 + 66 = 270
    bands = [
        (0, 34, VOID_BLACK),       # Band 0: Deepest void twilight
        (34, 68, OUTLINE),         # Band 1: Midnight purple
        (68, 102, SHADOW_DEEP),    # Band 2: Deep dusk shadow
        (102, 136, SHADOW_MID),    # Band 3: Rich purple shadow
        (136, 170, PURPLE_MID),    # Band 4: Vibrant dusk purple
        (170, 204, PURPLE_LIGHT),  # Band 5: Twilight violet
        (204, 237, DUSK_PINK),     # Band 6: Warm plum rose
        (237, 270, DUSK_PEACH),    # Band 7: Luminous warm plum
    ]
    for y_start, y_end, color in bands:
        for y in range(y_start, y_end):
            c.set_pixel(0, y, color)
    return c


def generate_bg_far() -> PixelCanvas:
    """
    480x270 px bedroom wall.
    - Seamless horizontal tiling (480 is divisible by wallpaper period 24).
    - Rich warm dusk bedroom wall with subtle diamond wallpaper motif.
    - Baseboard moulding along bottom (y=244..270).
    - Large wooden framed window (x=300..375, y=30..120) looking out to night sky
      with glowing crescent moon and twinkling stars.
    - Framed crayon drawing (x=60..105, y=50..95) depicting the two siblings holding hands
      under a smiling sun with a heart.
    - Retro toy rocket poster (x=170..220, y=55..115) with pinned corners and thruster flames.
    """
    c = PixelCanvas(480, 270, SHADOW_MID)

    # 1. Subtle ceiling crown moulding shadow at top (y=0..7)
    c.rect(0, 0, 480, 1, OUTLINE)
    c.rect(0, 1, 480, 1, SHADOW_DEEP)
    c.rect(0, 2, 480, 1, PURPLE_MID)
    c.rect(0, 3, 480, 1, SHADOW_DEEP)
    for x in range(480):
        if x % 2 == 0:
            c.set_pixel(x, 4, SHADOW_DEEP)
        if x % 4 == 0:
            c.set_pixel(x, 5, SHADOW_DEEP)

    # 2. Seamless diamond wallpaper pattern (period = 24px, 480 / 24 = 20 repeats)
    for y in range(6, 244):
        for x in range(480):
            gx = x % 24
            gy = y % 24
            dx = abs(gx - 12)
            dy = abs(gy - 12)
            dist = dx + dy
            # Outer diamond ring
            if dist == 10:
                c.set_pixel(x, y, PURPLE_MID)
            # Inner diamond accent
            elif dist == 2:
                c.set_pixel(x, y, PURPLE_LIGHT)
            elif dist == 0:
                c.set_pixel(x, y, DUSK_PINK)
            # Corner grid intersection floret
            elif (gx == 0 and gy == 0) or (gx == 0 and gy == 1) or (gx == 1 and gy == 0):
                c.set_pixel(x, y, PURPLE_LIGHT)

    # 3. Baseboard moulding along bottom (y=244..270)
    # Carved classical profile with wood tones
    c.line(0, 244, 479, 244, WOOD_HIGHLIGHT)
    c.line(0, 245, 479, 245, BROWN_LIGHT)
    c.line(0, 246, 479, 246, BROWN_MID)
    c.line(0, 247, 479, 247, BROWN_DARKEST)
    c.line(0, 248, 479, 248, WOOD_HIGHLIGHT)
    c.line(0, 249, 479, 249, BROWN_MID)
    # Main plinth face with subtle repeating grain
    c.rect(0, 250, 480, 16, BROWN_DARK)
    for x in range(480):
        if x % 24 == 0:
            c.line(x, 250, x, 265, BROWN_MID)
        elif x % 24 == 1:
            c.line(x, 250, x, 265, BROWN_DARKEST)
        elif x % 12 == 6 and (x // 24) % 2 == 0:
            c.set_pixel(x, 256, BROWN_MID)
            c.set_pixel(x, 257, BROWN_MID)
    # Shoe moulding
    c.line(0, 266, 479, 266, WOOD_HIGHLIGHT)
    c.line(0, 267, 479, 267, BROWN_MID)
    c.line(0, 268, 479, 268, BROWN_DARKEST)
    c.line(0, 269, 479, 269, OUTLINE)

    # 4. Framed Crayon Drawing (x=60..105, y=50..95)
    # Wall drop shadow
    c.rect(63, 53, 45, 45, SHADOW_DEEP)
    # Picture hanging nail and cord
    c.set_pixel(82, 44, YELLOW_MID)
    c.set_pixel(82, 43, WOOD_HIGHLIGHT)
    c.line(82, 45, 68, 50, BROWN_DARKEST)
    c.line(82, 45, 96, 50, BROWN_DARKEST)
    # Mitred wooden frame
    c.rect(60, 50, 46, 46, BROWN_MID)
    # Frame bevels
    c.line(60, 50, 105, 50, WOOD_HIGHLIGHT)
    c.line(60, 50, 60, 95, WOOD_HIGHLIGHT)
    c.line(61, 51, 104, 51, BROWN_LIGHT)
    c.line(61, 51, 61, 94, BROWN_LIGHT)
    c.line(60, 95, 105, 95, BROWN_DARKEST)
    c.line(105, 50, 105, 95, BROWN_DARKEST)
    c.line(61, 94, 104, 94, BROWN_DARK)
    c.line(104, 51, 104, 94, BROWN_DARK)
    # Inner frame shadow
    c.line(63, 53, 102, 53, BROWN_DARKEST)
    c.line(63, 53, 63, 92, BROWN_DARKEST)
    c.line(63, 92, 102, 92, BROWN_LIGHT)
    c.line(102, 53, 102, 92, BROWN_LIGHT)
    # Drawing paper
    c.rect(64, 54, 38, 38, PURE_WHITE)
    c.set_pixel(64, 54, WHITE_SHADOW)
    c.set_pixel(101, 54, WHITE_SHADOW)
    c.set_pixel(64, 91, WHITE_SHADOW)
    c.set_pixel(101, 91, WHITE_SHADOW)

    # Crayon Art - Smiling Sun at top-left (71, 61)
    c.circle(71, 61, 4, YELLOW_MID, outline=YELLOW_SHADOW)
    # Crayon rays
    c.line(71, 54, 71, 55, YELLOW_LIGHT)
    c.line(71, 67, 71, 68, YELLOW_LIGHT)
    c.line(64, 61, 65, 61, YELLOW_LIGHT)
    c.line(77, 61, 78, 61, YELLOW_LIGHT)
    c.set_pixel(66, 56, ORANGE_MID)
    c.set_pixel(76, 56, ORANGE_MID)
    c.set_pixel(66, 66, ORANGE_MID)
    c.set_pixel(76, 66, ORANGE_MID)
    # Sun smiling face
    c.set_pixel(70, 60, OUTLINE)
    c.set_pixel(72, 60, OUTLINE)
    c.set_pixel(69, 62, ORANGE_MID)
    c.set_pixel(70, 63, OUTLINE)
    c.set_pixel(71, 63, OUTLINE)
    c.set_pixel(72, 63, OUTLINE)
    c.set_pixel(73, 62, ORANGE_MID)

    # Soft crayon cloud at top-right (92, 59)
    c.rect(88, 59, 9, 4, BLUE_LIGHT)
    c.rect(90, 57, 5, 2, WHITE_SHADOW)
    c.set_pixel(87, 61, BLUE_LIGHT)
    c.set_pixel(97, 61, BLUE_LIGHT)

    # Rolling green grass hill at bottom (y=84..91)
    for gx in range(64, 102):
        gy = int(85 + math.sin((gx - 64) * 0.22) * 2.5)
        c.line(gx, gy, gx, 91, GREEN_MID)
        c.set_pixel(gx, gy, GREEN_LIGHT)
    # Little crayon flower dots in the grass
    c.set_pixel(67, 88, RED_LIGHT)
    c.set_pixel(73, 89, YELLOW_LIGHT)
    c.set_pixel(94, 87, RED_LIGHT)
    c.set_pixel(98, 89, YELLOW_LIGHT)

    # Two stick kid siblings holding hands!
    # Sibling 1 (Older sibling, left, x=78):
    # Head & hair
    c.circle(78, 71, 2, SKIN_LIGHT, outline=SKIN_MID)
    c.set_pixel(77, 69, BROWN_DARK)
    c.set_pixel(78, 69, BROWN_DARK)
    c.set_pixel(79, 69, BROWN_DARK)
    # Face dots
    c.set_pixel(78, 71, OUTLINE)
    # Red hoodie
    c.line(78, 74, 78, 81, RED_MID)
    c.line(77, 75, 79, 75, RED_LIGHT)
    # Left arm down
    c.line(77, 76, 75, 79, RED_MID)
    # Right arm reaching to hold hands
    c.line(79, 76, 82, 78, RED_MID)
    # Blue pants
    c.line(78, 81, 76, 86, BLUE_MID)
    c.line(78, 81, 80, 86, BLUE_MID)

    # Sibling 2 (Younger sibling, right, smaller & cute, x=86):
    # Head & hair
    c.circle(86, 74, 2, SKIN_LIGHT, outline=SKIN_MID)
    c.set_pixel(85, 72, ORANGE_MID)
    c.set_pixel(86, 72, ORANGE_MID)
    c.set_pixel(87, 72, ORANGE_MID)
    # Face dot
    c.set_pixel(86, 74, OUTLINE)
    # Blue shirt
    c.line(86, 77, 86, 82, BLUE_LIGHT)
    c.set_pixel(86, 77, BLUE_MID)
    # Left arm reaching to hold hands
    c.line(85, 79, 82, 78, BLUE_LIGHT)
    # Right arm swinging joyfully
    c.line(87, 79, 89, 77, BLUE_LIGHT)
    # Green shorts/legs
    c.line(86, 82, 84, 87, GREEN_MID)
    c.line(86, 82, 87, 87, GREEN_MID)

    # Hand clasp at (82, 78)
    c.set_pixel(82, 78, SKIN_LIGHT)

    # Vibrant crayon heart floating over their hands (82, 72)
    c.set_pixel(81, 71, RED_LIGHT)
    c.set_pixel(83, 71, RED_LIGHT)
    c.set_pixel(82, 72, RED_MID)
    c.set_pixel(82, 73, RED_SHADOW)
    c.set_pixel(80, 71, RED_SHADOW)
    c.set_pixel(84, 71, RED_SHADOW)

    # 5. Retro Toy Rocket Poster (x=170..220, y=55..115)
    # Wall drop shadow
    c.rect(172, 57, 51, 61, SHADOW_DEEP)
    # Poster paper background
    c.rect(170, 55, 51, 61, VOID_BLACK, outline=WHITE_SHADOW)
    c.rect(172, 57, 47, 57, SHADOW_DEEP)
    # Inner border line
    c.rect(174, 59, 43, 53, VOID_BLACK, outline=PURPLE_MID)

    # Poster Deep Space Art:
    # Ringed planet at top-right (206, 68)
    c.circle(206, 68, 4, ORANGE_MID, outline=ORANGE_SHADOW)
    c.line(201, 70, 211, 66, YELLOW_LIGHT) # ring
    c.set_pixel(200, 71, YELLOW_MID)
    c.set_pixel(212, 65, YELLOW_MID)
    # Distant poster stars
    for px, py in [(178, 64), (184, 72), (211, 78), (177, 86), (182, 102), (210, 98)]:
        c.set_pixel(px, py, YELLOW_LIGHT if (px + py) % 2 == 0 else BLUE_LIGHT)

    # Vintage Retro Rocket Ship (centered at x=195)
    # Sharp red nose cone
    c.set_pixel(195, 63, RED_LIGHT)
    c.line(194, 64, 196, 64, RED_LIGHT)
    c.line(194, 65, 196, 65, RED_MID)
    c.line(193, 66, 197, 66, RED_MID)
    # White atomic fuselage body
    for fy in range(67, 87):
        c.line(193, fy, 197, fy, PURE_WHITE)
        c.set_pixel(193, fy, WHITE_SHADOW)
        c.set_pixel(197, fy, WHITE_SHADOW)
    # Vintage red racing stripes
    c.line(193, 75, 197, 75, RED_MID)
    c.line(193, 76, 197, 76, RED_LIGHT)
    c.line(193, 77, 197, 77, RED_MID)
    # Circular porthole window with glass shine
    c.circle(195, 71, 2, BLUE_LIGHT, outline=OUTLINE)
    c.set_pixel(195, 71, PURE_WHITE)
    # Swept retro fins
    # Left fin
    c.line(192, 80, 188, 86, BLUE_MID)
    c.line(191, 81, 189, 86, RED_MID)
    c.line(192, 82, 190, 86, RED_MID)
    c.line(188, 86, 192, 86, RED_SHADOW)
    # Right fin
    c.line(198, 80, 202, 86, BLUE_MID)
    c.line(199, 81, 201, 86, RED_MID)
    c.line(198, 82, 200, 86, RED_MID)
    c.line(198, 86, 202, 86, RED_SHADOW)
    # Center dorsal fin
    c.line(195, 80, 195, 86, RED_LIGHT)
    # Thruster engine nozzle
    c.rect(193, 87, 5, 2, BROWN_DARKEST)

    # Powerful thruster exhaust flame blast!
    # Core white hot
    c.line(194, 89, 196, 89, PURE_WHITE)
    c.set_pixel(195, 90, PURE_WHITE)
    c.set_pixel(195, 91, PURE_WHITE)
    # Yellow flame cone
    c.line(193, 90, 197, 90, YELLOW_LIGHT)
    c.line(194, 91, 196, 91, YELLOW_LIGHT)
    c.line(194, 92, 196, 92, YELLOW_MID)
    c.line(194, 93, 196, 93, YELLOW_MID)
    c.set_pixel(195, 94, YELLOW_MID)
    c.set_pixel(195, 95, YELLOW_MID)
    # Orange flame body & flares
    c.line(193, 94, 197, 94, ORANGE_MID)
    c.line(193, 96, 197, 96, ORANGE_MID)
    c.line(194, 97, 196, 97, ORANGE_MID)
    c.line(194, 98, 196, 98, ORANGE_SHADOW)
    c.set_pixel(195, 99, ORANGE_MID)
    c.set_pixel(195, 100, ORANGE_SHADOW)
    # Trailing sparks
    c.set_pixel(193, 102, RED_LIGHT)
    c.set_pixel(197, 101, RED_LIGHT)
    c.set_pixel(195, 104, RED_MID)
    c.set_pixel(194, 106, RED_SHADOW)

    # 4 Corner Pushpins (pinned corners)
    # Top-left (red)
    c.circle(173, 58, 2, RED_MID, outline=OUTLINE)
    c.set_pixel(172, 57, PURE_WHITE)
    # Top-right (yellow)
    c.circle(217, 58, 2, YELLOW_MID, outline=OUTLINE)
    c.set_pixel(216, 57, PURE_WHITE)
    # Bottom-left (blue)
    c.circle(173, 112, 2, BLUE_MID, outline=OUTLINE)
    c.set_pixel(172, 111, PURE_WHITE)
    # Bottom-right (red)
    c.circle(217, 112, 2, RED_MID, outline=OUTLINE)
    c.set_pixel(216, 111, PURE_WHITE)

    # 6. Large Wooden Framed Window (x=300..375, y=30..120)
    # Wall drop shadow from window sill and right jamb
    c.rect(302, 122, 78, 4, SHADOW_DEEP)
    c.rect(376, 34, 4, 88, SHADOW_DEEP)

    # Window Lintel (ornate wooden top cap, x=298..377, y=27..31)
    c.rect(298, 27, 80, 5, BROWN_MID)
    c.line(298, 27, 377, 27, WOOD_HIGHLIGHT)
    c.line(298, 28, 377, 28, BROWN_LIGHT)
    c.line(298, 31, 377, 31, BROWN_DARKEST)

    # Window Sill (protruding bottom ledge, x=295..380, y=117..122)
    c.rect(295, 117, 86, 6, BROWN_MID)
    c.line(295, 117, 380, 117, WOOD_HIGHLIGHT)
    c.line(295, 118, 380, 118, WOOD_HIGHLIGHT)
    c.line(295, 119, 380, 119, BROWN_LIGHT)
    c.line(295, 122, 380, 122, BROWN_DARKEST)

    # Outer Frame Jambs
    c.rect(300, 32, 76, 85, BROWN_DARK, outline=BROWN_DARKEST)
    c.line(300, 32, 300, 116, WOOD_HIGHLIGHT)
    c.line(301, 32, 301, 116, BROWN_MID)
    c.line(374, 32, 374, 116, BROWN_DARK)
    c.line(375, 32, 375, 116, BROWN_DARKEST)

    # Window Panes Glass (night sky opening: x=306..369, y=36..115)
    # Outside night sky gradient
    for gy in range(36, 116):
        if gy < 65:
            col = VOID_BLACK
        elif gy < 92:
            col = SHADOW_DEEP
        else:
            col = SHADOW_MID
        c.line(306, gy, 369, gy, col)

    # Distant rooftop & treetops horizon silhouette outside window (y=109..115)
    for hx in range(306, 370):
        # Charming gentle roof pitch & tree canopy
        hy = int(112 + math.sin((hx - 306) * 0.18) * 2)
        c.line(hx, hy, hx, 115, VOID_BLACK)

    # Glowing Crescent Moon in upper-left window pane (cx=323, cy=54)
    # Soft moon halo
    for my in range(43, 66):
        for mx in range(312, 335):
            d_halo = math.sqrt((mx - 323) ** 2 + (my - 54) ** 2)
            if 8.5 < d_halo <= 11.5 and (mx + my) % 2 == 0:
                c.set_pixel(mx, my, PURPLE_LIGHT)
    # Bright moon body
    c.circle(323, 54, 8, YELLOW_LIGHT, outline=YELLOW_MID)
    # Moon rim highlight
    c.line(316, 52, 316, 56, PURE_WHITE)
    c.line(317, 49, 318, 48, PURE_WHITE)
    c.line(317, 59, 318, 60, PURE_WHITE)
    # Cutout to form perfect elegant crescent
    c.circle(326, 52, 7, VOID_BLACK)

    # Distant Fixed Stars in Window Glass
    base_stars = [
        (312, 42), (328, 39), (314, 67), (329, 69),
        (345, 42), (356, 40), (364, 52), (348, 62), (362, 68),
        (312, 85), (324, 90), (315, 102), (330, 104),
        (345, 84), (358, 88), (350, 98), (364, 105)
    ]
    for sx, sy in base_stars:
        c.set_pixel(sx, sy, YELLOW_LIGHT if (sx + sy) % 3 == 0 else PURE_WHITE)

    # Wooden Window Mullions (dividing into 4 classic panes)
    # Vertical mullion (x=336..339, y=36..115)
    c.rect(336, 36, 4, 80, BROWN_MID)
    c.line(336, 36, 336, 115, WOOD_HIGHLIGHT)
    c.line(339, 36, 339, 115, BROWN_DARKEST)
    # Horizontal transom bar (x=306..369, y=74..77)
    c.rect(306, 74, 64, 4, BROWN_MID)
    c.line(306, 74, 369, 74, WOOD_HIGHLIGHT)
    c.line(306, 77, 369, 77, BROWN_DARKEST)
    # Center mullion joint shadow
    c.set_pixel(339, 77, BROWN_DARKEST)

    return c


def generate_bg_far_stars() -> List[PixelCanvas]:
    """
    4 frames of twinkling stars inside the window (fps 3).
    480x270 per frame, assembled into 1920x270 strip.
    Transparent canvas overlaying bg_far.png.
    """
    frames = []
    star_coords = [
        # Top-left pane (around crescent moon)
        (312, 42), (328, 39), (314, 67), (329, 69),
        # Top-right pane
        (345, 42), (356, 40), (364, 52), (348, 62), (362, 68),
        # Bottom-left pane
        (312, 85), (324, 90), (315, 102), (330, 104),
        # Bottom-right pane
        (345, 84), (358, 88), (350, 98), (364, 105)
    ]

    for f in range(4):
        c = PixelCanvas(480, 270, TRANSPARENT)
        for i, (sx, sy) in enumerate(star_coords):
            phase = (i * 3 + f) % 4
            if phase == 0:
                # 4-pointed cross sparkle
                c.set_pixel(sx, sy, PURE_WHITE)
                c.set_pixel(sx - 1, sy, YELLOW_LIGHT)
                c.set_pixel(sx + 1, sy, YELLOW_LIGHT)
                c.set_pixel(sx, sy - 1, YELLOW_LIGHT)
                c.set_pixel(sx, sy + 1, YELLOW_LIGHT)
            elif phase == 1:
                # Bright point
                c.set_pixel(sx, sy, PURE_WHITE)
            elif phase == 2:
                # Warm star
                c.set_pixel(sx, sy, YELLOW_LIGHT)
            else:
                # Soft distant glint
                c.set_pixel(sx, sy, PURPLE_LIGHT)
        frames.append(c)
    return frames


def generate_bg_mid() -> PixelCanvas:
    """
    640x270 px bedroom mid-ground.
    - Seamless horizontal tiling (x=0 matches x=639, both transparent open wall).
    - Floor level at y=200.
    - Tall bookshelf packed with colorful book spines, book titles/stripes.
    - Bedside nightstand with brass knobs, warm glowing lamp casting radial dusk light.
    - Sibling's bed with soft white pillow and cozy quilted blue blanket with cloth folds.
    - Wooden toy chest with brass lock and cute toy dinosaur peeking out.
    """
    c = PixelCanvas(640, 270, TRANSPARENT)

    # -------------------------------------------------------------------------
    # 1. Tall Bookshelf (x=36..186, y=38..200)
    # -------------------------------------------------------------------------
    # Top Crown Moulding (pediment)
    c.rect(34, 38, 155, 3, BROWN_MID)
    c.line(34, 38, 188, 38, WOOD_HIGHLIGHT)
    c.line(34, 40, 188, 40, BROWN_DARKEST)
    c.rect(36, 41, 151, 4, BROWN_LIGHT)
    c.line(36, 44, 186, 44, BROWN_DARK)

    # Bookshelf Outer Uprights (side panels)
    # Left upright
    c.rect(36, 45, 8, 151, BROWN_MID)
    c.line(36, 45, 36, 195, WOOD_HIGHLIGHT)
    c.line(37, 45, 37, 195, BROWN_LIGHT)
    c.line(43, 45, 43, 195, BROWN_DARKEST)
    # Right upright
    c.rect(179, 45, 8, 151, BROWN_DARK)
    c.line(179, 45, 179, 195, BROWN_DARKEST)
    c.line(186, 45, 186, 195, OUTLINE)

    # Dark Wooden Backboard behind books
    c.rect(44, 45, 135, 151, SHADOW_DEEP)

    # Thick Horizontal Shelves (y=80, y=118, y=156, y=194)
    for sy in [80, 118, 156, 194]:
        c.rect(44, sy, 135, 6, BROWN_MID)
        c.line(44, sy, 178, sy, WOOD_HIGHLIGHT)
        c.line(44, sy + 5, 178, sy + 5, BROWN_DARKEST)

    # Bottom Plinth Base (resting on floor at y=200)
    c.rect(34, 196, 155, 4, BROWN_DARK)
    c.line(34, 196, 188, 196, WOOD_HIGHLIGHT)
    c.line(34, 199, 188, 199, OUTLINE)
    # Floor contact shadow under bookshelf
    c.line(32, 200, 190, 200, SHADOW_DEEP)
    c.line(36, 201, 186, 201, SHADOW_MID)

    # --- Shelf 1 Books & Potted Houseplant (y=45..79) ---
    # Potted succulent / plant on left (x=48..59, y=62..79)
    # Terra cotta pot
    c.rect(49, 69, 10, 11, BROWN_LIGHT)
    c.line(48, 68, 59, 68, WOOD_HIGHLIGHT)
    c.line(49, 79, 58, 79, BROWN_DARKEST)
    # Green succulent leaves
    c.circle(53, 63, 4, GREEN_MID, outline=GREEN_SHADOW)
    c.circle(56, 64, 3, GREEN_LIGHT, outline=GREEN_MID)
    c.circle(51, 65, 3, GREEN_MID)
    c.set_pixel(53, 61, GREEN_LIGHT)

    # Colorful standing books (Shelf 1, x=64..155)
    shelf1_palette = [
        (RED_MID, RED_SHADOW, RED_LIGHT),
        (BLUE_MID, BLUE_SHADOW, BLUE_LIGHT),
        (YELLOW_MID, YELLOW_SHADOW, YELLOW_LIGHT),
        (GREEN_MID, GREEN_SHADOW, GREEN_LIGHT),
        (PURPLE_LIGHT, SHADOW_MID, DUSK_PINK),
        (ORANGE_MID, ORANGE_SHADOW, YELLOW_LIGHT),
        (DUSK_PINK, PURPLE_MID, DUSK_PEACH)
    ]
    bx = 64
    b_idx = 0
    while bx < 155:
        bw = 4 + (b_idx % 4)
        bh = 22 + ((b_idx * 5) % 11)
        by = 80 - bh
        col_mid, col_dark, col_light = shelf1_palette[b_idx % len(shelf1_palette)]
        # Spine
        c.rect(bx, by, bw, bh, col_mid, outline=OUTLINE)
        c.line(bx + 1, by + 1, bx + 1, by + bh - 2, col_light)
        c.line(bx + bw - 2, by + 1, bx + bw - 2, by + bh - 2, col_dark)
        # Gold embossed title stripes
        if bh > 25:
            c.line(bx + 1, by + 6, bx + bw - 2, by + 6, YELLOW_LIGHT)
            c.line(bx + 1, by + 8, bx + bw - 2, by + 8, YELLOW_LIGHT)
        bx += bw + 1
        b_idx += 1

    # Brass Bookend & Leaning book at end of shelf 1 (x=160..176)
    # Leaning book
    c.line(160, 58, 168, 79, BLUE_MID)
    c.line(161, 58, 169, 79, BLUE_LIGHT)
    c.line(163, 58, 171, 79, BLUE_SHADOW)
    # Bookend
    c.rect(173, 66, 4, 14, YELLOW_MID, outline=YELLOW_SHADOW)
    c.set_pixel(173, 66, PURE_WHITE)

    # --- Shelf 2 Books (y=86..117) ---
    # Packed colorful book collection with bookmark ribbons
    bx = 46
    b_idx = 0
    while bx < 176:
        bw = 5 + ((b_idx * 2) % 4)
        bh = 24 + ((b_idx * 7) % 8)
        by = 118 - bh
        col_mid, col_dark, col_light = shelf1_palette[(b_idx + 3) % len(shelf1_palette)]
        c.rect(bx, by, bw, bh, col_mid, outline=OUTLINE)
        c.line(bx + 1, by + 1, bx + 1, by + bh - 2, col_light)
        c.line(bx + bw - 2, by + 1, bx + bw - 2, by + bh - 2, col_dark)
        # Title bands & ribbing
        c.line(bx + 1, by + 4, bx + bw - 2, by + 4, PURE_WHITE if b_idx % 2 == 0 else YELLOW_LIGHT)
        c.line(bx + 1, by + bh - 6, bx + bw - 2, by + bh - 6, YELLOW_LIGHT)
        # Bookmark ribbon hanging out of book #4
        if b_idx == 4:
            c.line(bx + 2, 118, bx + 2, 122, RED_MID)
            c.set_pixel(bx + 2, 122, RED_LIGHT)
        bx += bw + 1
        b_idx += 1

    # --- Shelf 3 Stacked & Standing Books (y=124..155) ---
    # Stack of horizontal books on left (x=46..72)
    # Book 1 (bottom)
    c.rect(46, 148, 26, 8, RED_MID, outline=OUTLINE)
    c.line(47, 149, 71, 149, RED_LIGHT)
    c.line(48, 152, 68, 152, YELLOW_LIGHT) # title
    # Book 2 (middle)
    c.rect(48, 141, 23, 7, BLUE_MID, outline=OUTLINE)
    c.line(49, 142, 70, 142, BLUE_LIGHT)
    # Book 3 (top)
    c.rect(51, 135, 18, 6, GREEN_MID, outline=OUTLINE)
    c.line(52, 136, 68, 136, GREEN_LIGHT)
    # Toy crystal / geode on top of stack
    c.set_pixel(59, 133, PURE_WHITE)
    c.set_pixel(60, 133, PURPLE_LIGHT)
    c.set_pixel(59, 134, PURPLE_MID)

    # Standing books on right of Shelf 3 (x=76..176)
    bx = 76
    b_idx = 0
    while bx < 176:
        bw = 4 + (b_idx % 3)
        bh = 25 + ((b_idx * 4) % 6)
        by = 156 - bh
        col_mid, col_dark, col_light = shelf1_palette[(b_idx + 5) % len(shelf1_palette)]
        c.rect(bx, by, bw, bh, col_mid, outline=OUTLINE)
        c.line(bx + 1, by + 1, bx + 1, by + bh - 2, col_light)
        c.line(bx + bw - 2, by + 1, bx + bw - 2, by + bh - 2, col_dark)
        bx += bw + 1
        b_idx += 1

    # --- Shelf 4 Heavy Storybooks & Binders (y=162..193) ---
    bx = 46
    b_idx = 0
    while bx < 176:
        bw = 6 + (b_idx % 4)
        bh = 30 - (b_idx % 4)
        by = 194 - bh
        col_mid, col_dark, col_light = shelf1_palette[(b_idx + 1) % len(shelf1_palette)]
        c.rect(bx, by, bw, bh, col_mid, outline=OUTLINE)
        c.line(bx + 1, by + 1, bx + 1, by + bh - 2, col_light)
        c.line(bx + bw - 2, by + 1, bx + bw - 2, by + bh - 2, col_dark)
        # Spine label box
        c.rect(bx + 1, by + 8, bw - 2, 7, WHITE_SHADOW)
        c.set_pixel(bx + 2, by + 11, OUTLINE)
        bx += bw + 1
        b_idx += 1

    # -------------------------------------------------------------------------
    # 2. Bedside Nightstand & Warm Glowing Lamp (x=214..266, y=95..200)
    # -------------------------------------------------------------------------
    # Nightstand Tabletop
    c.rect(214, 144, 53, 5, BROWN_MID)
    c.line(214, 144, 266, 144, WOOD_HIGHLIGHT)
    c.line(214, 145, 266, 145, BROWN_LIGHT)
    c.line(214, 148, 266, 148, BROWN_DARKEST)

    # Nightstand Cabinet Body
    c.rect(218, 149, 45, 46, BROWN_DARK, outline=BROWN_DARKEST)

    # Drawer 1 (upper)
    c.rect(221, 153, 39, 17, BROWN_MID, outline=BROWN_DARKEST)
    c.line(222, 154, 258, 154, WOOD_HIGHLIGHT)
    # Brass Knob 1
    c.circle(240, 161, 2, YELLOW_MID, outline=YELLOW_SHADOW)
    c.set_pixel(240, 160, PURE_WHITE)

    # Drawer 2 (lower)
    c.rect(221, 173, 39, 17, BROWN_MID, outline=BROWN_DARKEST)
    c.line(222, 174, 258, 174, WOOD_HIGHLIGHT)
    # Brass Knob 2
    c.circle(240, 181, 2, YELLOW_MID, outline=YELLOW_SHADOW)
    c.set_pixel(240, 180, PURE_WHITE)

    # Four Turned Nightstand Legs (resting on floor at y=200)
    # Left front leg
    c.rect(218, 195, 5, 5, BROWN_MID, outline=BROWN_DARKEST)
    c.line(218, 195, 218, 199, WOOD_HIGHLIGHT)
    # Right front leg
    c.rect(258, 195, 5, 5, BROWN_MID, outline=BROWN_DARKEST)
    c.line(258, 195, 258, 199, WOOD_HIGHLIGHT)
    # Floor contact shadow under nightstand
    c.line(215, 200, 265, 200, SHADOW_DEEP)

    # Bedside Lamp on Nightstand
    # Rounded Brass Base
    c.circle(240, 140, 5, YELLOW_MID, outline=YELLOW_SHADOW)
    c.line(235, 143, 245, 143, WOOD_HIGHLIGHT)
    c.line(234, 144, 246, 144, BROWN_DARKEST)
    # Slender Brass Stem
    c.line(239, 118, 239, 139, YELLOW_LIGHT)
    c.line(240, 118, 240, 139, YELLOW_MID)
    c.line(241, 118, 241, 139, YELLOW_SHADOW)
    # Conical Warm Lampshade
    # Trapezoid rows: top width 15px (y=98), bottom width 27px (y=118)
    for ly in range(98, 119):
        progress = (ly - 98) / 20.0
        hw = int(7 + progress * 6)
        c.line(240 - hw, ly, 240 + hw, ly, YELLOW_MID)
        c.set_pixel(240 - hw, ly, OUTLINE)
        c.set_pixel(240 + hw, ly, OUTLINE)
        c.line(240 - hw + 1, ly, 240 - hw + 3, ly, YELLOW_LIGHT)
    # Lampshade rim lines
    c.line(233, 98, 247, 98, YELLOW_LIGHT)
    c.line(227, 118, 253, 118, ORANGE_MID)
    # Warm glowing bulb peeking out bottom
    c.rect(238, 119, 5, 3, PURE_WHITE)

    # Radial Dusk Light Glow from Lamp
    # Emanating from bulb at (240, 118)
    lamp_cx, lamp_cy = 240, 118
    for gy in range(lamp_cy - 50, lamp_cy + 52):
        for gx in range(lamp_cx - 65, lamp_cx + 66):
            if 0 <= gx < 640 and 0 <= gy < 270:
                # Don't draw glow over opaque furniture parts
                d = math.sqrt((gx - lamp_cx) ** 2 + ((gy - lamp_cy) * 1.2) ** 2)
                cur_px = c.get_pixel(gx, gy)
                if cur_px[3] != 0 and cur_px not in [TRANSPARENT]:
                    # Furniture surface highlight from lamp
                    if d < 40 and gy == 144 and 214 <= gx <= 266:
                        c.set_pixel(gx, gy, YELLOW_LIGHT)
                    continue

                # Atmospheric radial light dither
                if d < 14:
                    if (gx + gy) % 2 == 0:
                        c.set_pixel(gx, gy, YELLOW_LIGHT)
                elif d < 26:
                    if (gx + gy) % 4 == 0:
                        c.set_pixel(gx, gy, YELLOW_MID)
                elif d < 42:
                    if gx % 3 == 0 and gy % 3 == 0:
                        c.set_pixel(gx, gy, DUSK_PEACH)
                elif d < 58:
                    if (gx + 2 * gy) % 8 == 0:
                        c.set_pixel(gx, gy, DUSK_PINK)

    # -------------------------------------------------------------------------
    # 3. Sibling's Bed (x=295..485, y=86..200)
    # -------------------------------------------------------------------------
    # Wooden Headboard at Left (x=295..330, y=86..200)
    # Finial Sphere on top of post
    c.circle(300, 86, 5, WOOD_HIGHLIGHT, outline=BROWN_DARKEST)
    c.set_pixel(299, 84, PURE_WHITE)
    # Tall Headboard Post
    c.rect(296, 91, 9, 109, BROWN_MID, outline=BROWN_DARKEST)
    c.line(297, 91, 297, 199, WOOD_HIGHLIGHT)
    c.line(298, 91, 298, 199, BROWN_LIGHT)
    # Headboard Carved Panel
    c.rect(305, 105, 26, 45, BROWN_DARK, outline=BROWN_DARKEST)
    c.line(305, 105, 330, 105, WOOD_HIGHLIGHT)
    c.line(306, 106, 329, 106, BROWN_MID)

    # Footboard Post at Right (x=476..484, y=132..200)
    c.circle(480, 132, 4, WOOD_HIGHLIGHT, outline=BROWN_DARKEST)
    c.rect(476, 136, 8, 64, BROWN_MID, outline=BROWN_DARKEST)
    c.line(477, 136, 477, 199, WOOD_HIGHLIGHT)

    # Bed Wooden Side Rail & Frame
    c.rect(305, 185, 171, 11, BROWN_MID, outline=BROWN_DARKEST)
    c.line(305, 185, 475, 185, WOOD_HIGHLIGHT)
    c.line(305, 186, 475, 186, BROWN_LIGHT)
    c.line(305, 195, 475, 195, BROWN_DARKEST)
    # Bed feet contact shadow at y=200
    c.line(294, 200, 486, 200, SHADOW_DEEP)

    # Big Soft White Pillow (x=315..355, y=128..150)
    c.circle(335, 139, 11, WHITE_SHADOW)
    c.rect(320, 132, 30, 15, WHITE_SHADOW)
    # Plump curves
    c.circle(325, 139, 8, PURE_WHITE)
    c.circle(345, 139, 8, PURE_WHITE)
    c.circle(335, 137, 8, PURE_WHITE)
    # Pillow crest highlight
    c.line(322, 131, 348, 131, PURE_WHITE)
    c.line(320, 132, 350, 132, PURE_WHITE)
    # Head impression / indentation crease
    c.line(330, 138, 340, 138, WHITE_SHADOW)
    c.line(328, 139, 342, 139, WHITE_SHADOW)
    c.set_pixel(335, 140, BLUE_LIGHT)

    # Cozy Quilted Blue Blanket with Cloth Folds (x=332..476, y=142..190)
    # Blanket base fill
    c.rect(332, 148, 144, 38, BLUE_MID, outline=OUTLINE)
    # Turned-down white sheet lining near pillow
    c.rect(332, 144, 22, 5, PURE_WHITE, outline=OUTLINE)
    c.line(332, 144, 353, 144, PURE_WHITE)
    c.line(332, 148, 353, 148, WHITE_SHADOW)

    # Quilted Diamond Stitching Motif across blanket
    # Diamond pattern in BLUE_LIGHT
    for by in range(149, 185):
        for bx in range(354, 475):
            if (bx + by) % 12 == 0 or (bx - by) % 12 == 0:
                c.set_pixel(bx, by, BLUE_LIGHT)
            # Quilt stitch knot dots
            if (bx + by) % 12 == 0 and (bx - by) % 12 == 0:
                c.set_pixel(bx, by, BLUE_SHADOW)

    # Deep Cloth Folds / Creases cascading rhythmically
    for fold_x in [370, 400, 430, 455]:
        c.line(fold_x - 1, 149, fold_x + 6, 185, BLUE_LIGHT)
        c.line(fold_x, 149, fold_x + 7, 185, BLUE_SHADOW)
        c.line(fold_x + 1, 149, fold_x + 8, 185, OUTLINE)

    # Blanket Drape Skirt overlapping bed rail
    for sx in range(332, 476):
        drape_wave = int(math.sin((sx - 332) * 0.25) * 2)
        c.line(sx, 185, sx, 188 + drape_wave, BLUE_MID)
        c.set_pixel(sx, 188 + drape_wave, OUTLINE)
        c.set_pixel(sx, 187 + drape_wave, BLUE_SHADOW)

    # -------------------------------------------------------------------------
    # 4. Wooden Toy Chest with Cute Peeking Dinosaur (x=505..605, y=120..200)
    # -------------------------------------------------------------------------
    # Wooden Chest Body
    c.rect(510, 146, 90, 50, BROWN_MID, outline=BROWN_DARKEST)
    # Vertical Oak Planks Shading
    for px in [530, 550, 570]:
        c.line(px, 147, px, 195, BROWN_DARK)
        c.line(px + 1, 147, px + 1, 195, BROWN_DARKEST)
    # Brass/Iron Corner Reinforcement Brackets with Rivets
    # Top-left bracket
    c.rect(510, 146, 8, 8, YELLOW_SHADOW, outline=BROWN_DARKEST)
    c.set_pixel(513, 149, YELLOW_MID)
    # Top-right bracket
    c.rect(592, 146, 8, 8, YELLOW_SHADOW, outline=BROWN_DARKEST)
    c.set_pixel(595, 149, YELLOW_MID)
    # Bottom-left bracket
    c.rect(510, 188, 8, 8, YELLOW_SHADOW, outline=BROWN_DARKEST)
    c.set_pixel(513, 191, YELLOW_MID)
    # Bottom-right bracket
    c.rect(592, 188, 8, 8, YELLOW_SHADOW, outline=BROWN_DARKEST)
    c.set_pixel(595, 191, YELLOW_MID)

    # Chest Base Carved Feet (touching floor at y=200)
    c.rect(512, 196, 12, 4, BROWN_DARK, outline=BROWN_DARKEST)
    c.rect(586, 196, 12, 4, BROWN_DARK, outline=BROWN_DARKEST)
    c.line(508, 200, 602, 200, SHADOW_DEEP)

    # Dark Interior Void of slightly open chest (y=138..146)
    c.rect(512, 138, 86, 8, VOID_BLACK)

    # Cute Toy Dinosaur Peeking Out (x=568..592, y=120..146)
    # Green head
    c.circle(580, 127, 7, GREEN_MID, outline=OUTLINE)
    c.circle(580, 126, 6, GREEN_MID)
    # Crown highlight
    c.line(576, 121, 582, 121, GREEN_LIGHT)
    c.line(575, 122, 584, 122, GREEN_LIGHT)
    # Dinosaur Snout (protruding right)
    c.rect(584, 125, 6, 6, GREEN_MID, outline=OUTLINE)
    c.line(585, 125, 589, 125, GREEN_LIGHT)
    # Cute little nostril dot
    c.set_pixel(588, 126, GREEN_SHADOW)
    # Smiling mouth with tiny white tooth
    c.line(584, 129, 589, 129, OUTLINE)
    c.set_pixel(586, 128, PURE_WHITE) # cute tooth!
    # Big expressive cartoon eye
    c.circle(577, 125, 3, PURE_WHITE, outline=OUTLINE)
    c.set_pixel(578, 125, OUTLINE) # pupil
    c.set_pixel(577, 124, PURE_WHITE) # glint
    # Spikes / back crest along neck
    c.set_pixel(572, 123, YELLOW_MID)
    c.set_pixel(570, 126, YELLOW_MID)
    c.set_pixel(569, 130, YELLOW_MID)
    # Two cute dinosaur claws/paws resting over chest rim
    # Left paw
    c.rect(573, 142, 4, 4, GREEN_MID, outline=OUTLINE)
    c.set_pixel(574, 141, GREEN_LIGHT)
    # Right paw
    c.rect(584, 142, 4, 4, GREEN_MID, outline=OUTLINE)
    c.set_pixel(585, 141, GREEN_LIGHT)

    # Chest Propped-Open Wooden Lid (angled ajar, y=131..144)
    # Lid extends from x=508 to x=602
    c.line(508, 137, 602, 131, WOOD_HIGHLIGHT)
    c.line(508, 138, 602, 132, BROWN_MID)
    c.line(508, 139, 602, 133, BROWN_MID)
    c.line(508, 140, 602, 134, BROWN_DARK)
    c.line(508, 141, 602, 135, BROWN_DARKEST)

    # Heavy Brass Lock Hasp at Center (x=551..559, y=148..166)
    # Upper hasp hinge
    c.rect(552, 146, 6, 6, YELLOW_MID, outline=YELLOW_SHADOW)
    c.set_pixel(554, 148, WOOD_HIGHLIGHT)
    # Padlock / lock body
    c.rect(551, 153, 8, 10, YELLOW_MID, outline=YELLOW_SHADOW)
    c.line(551, 153, 558, 153, YELLOW_LIGHT)
    c.line(551, 154, 551, 162, YELLOW_LIGHT)
    c.line(558, 154, 558, 162, YELLOW_SHADOW)
    # Keyhole
    c.rect(554, 156, 2, 4, OUTLINE)

    # Ensure seamless transition at boundary (x=0 and x=639)
    # Both x=0..33 and x=603..639 are transparent, providing a 70px open room expanse
    # so x=0 matches x=639 with 100% mathematical perfection.

    return c


def generate_bg_near() -> PixelCanvas:
    """
    480x270 px foreground layer.
    - STRICT: Transparent above y=200!
    - Dark silhouetted foreground toys: fluffy teddy bear, wooden toy locomotive & coal car,
      stacked block towers, rocking horse.
    - Beautiful crisp 1px upper-left rim lighting in pale purple (PURPLE_LIGHT).
    """
    c = PixelCanvas(480, 270, TRANSPARENT)

    # -------------------------------------------------------------------------
    # 1. Fluffy Teddy Bear Silhouette (x=40..95, y=205..265)
    # -------------------------------------------------------------------------
    bx, by = 68, 236
    # Body silhouette (plump chubby teddy)
    c.circle(bx, by + 6, 17, SHADOW_DEEP)
    # Head silhouette
    c.circle(bx, by - 12, 13, SHADOW_DEEP)
    # Left Ear & Right Ear
    c.circle(bx - 11, by - 22, 6, SHADOW_DEEP)
    c.circle(bx + 11, by - 22, 6, SHADOW_DEEP)
    # Muzzle protrusion
    c.circle(bx - 1, by - 8, 6, SHADOW_DEEP)
    # Left Arm & Right Arm
    c.circle(bx - 16, by + 4, 8, SHADOW_DEEP)
    c.circle(bx + 16, by + 4, 8, SHADOW_DEEP)
    # Paws / Foot pads facing viewer
    c.circle(bx - 14, by + 19, 9, SHADOW_DEEP)
    c.circle(bx + 14, by + 19, 9, SHADOW_DEEP)

    # Crisp 1px Upper-Left Rim Lighting (PURPLE_LIGHT)
    # Left ear rim
    c.line(bx - 16, by - 24, bx - 9, by - 27, PURPLE_LIGHT)
    c.line(bx - 17, by - 23, bx - 17, by - 20, PURPLE_LIGHT)
    # Head crown rim
    c.line(bx - 8, by - 24, bx + 4, by - 25, PURPLE_LIGHT)
    # Right ear top rim
    c.line(bx + 7, by - 27, bx + 13, by - 27, PURPLE_LIGHT)
    # Muzzle cheek highlight
    c.line(bx - 6, by - 11, bx - 4, by - 14, PURPLE_LIGHT)
    # Left shoulder / arm rim
    c.line(bx - 23, by, bx - 23, by + 5, PURPLE_LIGHT)
    c.line(bx - 22, by - 2, bx - 17, by - 4, PURPLE_LIGHT)
    # Left foot top rim
    c.line(bx - 22, by + 16, bx - 11, by + 11, PURPLE_LIGHT)
    # Right foot top rim
    c.line(bx + 6, by + 12, bx + 16, by + 12, PURPLE_LIGHT)

    # -------------------------------------------------------------------------
    # 2. Wooden Toy Locomotive & Coal Car (x=122..242, y=208..265)
    # -------------------------------------------------------------------------
    tx, ty = 135, 232
    # Locomotive Front Cowcatcher Wedge (x=122..134, y=244..260)
    for cx in range(122, 135):
        c.line(cx, 244 + (134 - cx), cx, 260, SHADOW_DEEP)
    c.line(122, 256, 134, 244, PURPLE_LIGHT) # cowcatcher rim

    # Locomotive Boiler Cylinder Body (x=134..180, y=224..252)
    c.rect(tx - 1, ty - 8, 47, 28, SHADOW_DEEP)
    c.line(tx - 1, ty - 8, tx + 45, ty - 8, PURPLE_LIGHT) # top boiler rim

    # Smokestack with Flared Funnel (x=144..152, y=208..224)
    c.rect(tx + 9, ty - 22, 8, 14, SHADOW_DEEP)
    c.line(tx + 7, ty - 24, tx + 18, ty - 24, SHADOW_DEEP) # flared top
    c.line(tx + 7, ty - 24, tx + 18, ty - 24, PURPLE_LIGHT) # smokestack rim
    c.line(tx + 9, ty - 23, tx + 9, ty - 10, PURPLE_LIGHT) # smokestack left rim

    # Steam Dome (x=162..168, y=217..224)
    c.rect(tx + 27, ty - 14, 7, 7, SHADOW_DEEP)
    c.line(tx + 28, ty - 15, tx + 32, ty - 15, PURPLE_LIGHT)
    c.set_pixel(tx + 27, ty - 14, PURPLE_LIGHT)

    # Engineer's Cab with Pitched Roof (x=178..205, y=208..254)
    c.rect(tx + 43, ty - 23, 27, 43, SHADOW_DEEP)
    # Overhanging roof
    c.rect(tx + 41, ty - 24, 30, 3, SHADOW_DEEP)
    c.line(tx + 41, ty - 24, tx + 70, ty - 24, PURPLE_LIGHT) # roof rim
    c.line(tx + 41, ty - 23, tx + 41, ty - 10, PURPLE_LIGHT) # cab left rim
    # Cab Window Cutout (transparent opening looking through cab)
    c.rect(tx + 47, ty - 16, 12, 14, TRANSPARENT)
    c.line(tx + 47, ty - 16, tx + 58, ty - 16, PURPLE_LIGHT) # window sill rim

    # Locomotive Wheels
    # Small leading wheel at front
    c.circle(tx + 6, ty + 24, 5, SHADOW_DEEP, outline=OUTLINE)
    c.line(tx + 2, ty + 22, tx + 5, ty + 19, PURPLE_LIGHT)
    # Two large driving wheels
    c.circle(tx + 24, ty + 22, 9, SHADOW_DEEP, outline=OUTLINE)
    c.line(tx + 16, ty + 18, tx + 24, ty + 13, PURPLE_LIGHT)
    c.set_pixel(tx + 24, ty + 22, PURPLE_LIGHT) # hub
    c.circle(tx + 48, ty + 22, 9, SHADOW_DEEP, outline=OUTLINE)
    c.line(tx + 40, ty + 18, tx + 48, ty + 13, PURPLE_LIGHT)
    c.set_pixel(tx + 48, ty + 22, PURPLE_LIGHT)
    # Connecting drive rod
    c.line(tx + 24, ty + 24, tx + 48, ty + 24, SHADOW_DEEP)
    c.line(tx + 24, ty + 23, tx + 48, ty + 23, PURPLE_LIGHT)

    # Coupler Hitch
    c.rect(tx + 70, ty + 14, 8, 4, SHADOW_DEEP)
    c.line(tx + 70, ty + 14, tx + 77, ty + 14, PURPLE_LIGHT)

    # Coal Car / Tender (x=213..242, y=222..258)
    # Coal Bin
    c.rect(tx + 78, ty - 4, 29, 23, SHADOW_DEEP)
    c.line(tx + 78, ty - 4, tx + 106, ty - 4, PURPLE_LIGHT) # top rim
    c.line(tx + 78, ty - 3, tx + 78, ty + 15, PURPLE_LIGHT) # left rim
    # Bumpy Coal Mound on Top
    for cx in range(tx + 80, tx + 105):
        cy = int(ty - 7 + math.sin((cx - tx) * 0.5) * 3)
        c.line(cx, cy, cx, ty - 4, SHADOW_DEEP)
        if (cx - tx) % 4 == 0:
            c.set_pixel(cx, cy, PURPLE_LIGHT)
    # Tender Wheels
    c.circle(tx + 86, ty + 23, 6, SHADOW_DEEP, outline=OUTLINE)
    c.line(tx + 82, ty + 20, tx + 86, ty + 17, PURPLE_LIGHT)
    c.circle(tx + 100, ty + 23, 6, SHADOW_DEEP, outline=OUTLINE)
    c.line(tx + 96, ty + 20, tx + 100, ty + 17, PURPLE_LIGHT)

    # -------------------------------------------------------------------------
    # 3. Stacked Block Towers (x=272..342, y=203..265)
    # -------------------------------------------------------------------------
    # Tower 1 (Tall 3-block tower with pyramid roof)
    # Base Block (22x16)
    c.rect(276, 246, 22, 16, SHADOW_DEEP, outline=OUTLINE)
    c.line(276, 246, 297, 246, PURPLE_LIGHT)
    c.line(276, 246, 276, 261, PURPLE_LIGHT)
    # Middle Block (18x14)
    c.rect(278, 231, 18, 15, SHADOW_DEEP, outline=OUTLINE)
    c.line(278, 231, 295, 231, PURPLE_LIGHT)
    c.line(278, 231, 278, 245, PURPLE_LIGHT)
    # Top Block (14x13)
    c.rect(280, 217, 14, 14, SHADOW_DEEP, outline=OUTLINE)
    c.line(280, 217, 293, 217, PURPLE_LIGHT)
    c.line(280, 217, 280, 230, PURPLE_LIGHT)
    # Pyramid Roof Block on Top (y=204..216)
    for py in range(204, 217):
        pw = (py - 204)
        c.line(287 - pw, py, 287 + pw, py, SHADOW_DEEP)
    # Pyramid left slope rim-light
    c.line(287, 204, 275, 216, PURPLE_LIGHT)
    c.line(275, 216, 299, 216, OUTLINE)

    # Tower 2 (Shorter 2-block tower with arched cylinder top)
    # Base Block
    c.rect(310, 244, 20, 18, SHADOW_DEEP, outline=OUTLINE)
    c.line(310, 244, 329, 244, PURPLE_LIGHT)
    c.line(310, 244, 310, 261, PURPLE_LIGHT)
    # Upper Block
    c.rect(313, 228, 17, 16, SHADOW_DEEP, outline=OUTLINE)
    c.line(313, 228, 329, 228, PURPLE_LIGHT)
    c.line(313, 228, 313, 243, PURPLE_LIGHT)
    # Cylindrical Block lying on top (y=216..227)
    c.circle(321, 222, 6, SHADOW_DEEP, outline=OUTLINE)
    c.line(316, 218, 321, 216, PURPLE_LIGHT)

    # -------------------------------------------------------------------------
    # 4. Rocking Horse Silhouette (x=370..465, y=204..265)
    # -------------------------------------------------------------------------
    hx, hy = 416, 234

    # Curved Wooden Rockers at bottom (x=370..465)
    for rx in range(370, 465):
        # Graceful curved rocker arc
        ry = int(261 + ((rx - hx) / 22.0) ** 2)
        if ry < 268:
            c.set_pixel(rx, ry, SHADOW_DEEP)
            c.set_pixel(rx, ry + 1, SHADOW_DEEP)
            c.set_pixel(rx, ry + 2, OUTLINE)
            c.set_pixel(rx, ry - 1, PURPLE_LIGHT) # top rim light
    # Left & Right rocker tips
    c.circle(371, 252, 2, SHADOW_DEEP)
    c.set_pixel(370, 251, PURPLE_LIGHT)
    c.circle(463, 252, 2, SHADOW_DEEP)
    c.set_pixel(463, 251, PURPLE_LIGHT)

    # Four Sturdy Angled Legs
    # Back legs (slanted backward)
    c.line(hx - 16, hy + 2, hx - 28, 257, SHADOW_DEEP)
    c.line(hx - 15, hy + 2, hx - 27, 257, SHADOW_DEEP)
    c.line(hx - 17, hy + 2, hx - 29, 257, PURPLE_LIGHT) # leg left rim
    c.line(hx - 10, hy + 2, hx - 20, 258, SHADOW_DEEP)
    c.line(hx - 11, hy + 2, hx - 21, 258, PURPLE_LIGHT)
    # Front legs (slanted forward)
    c.line(hx + 14, hy + 2, hx + 28, 258, SHADOW_DEEP)
    c.line(hx + 15, hy + 2, hx + 29, 258, SHADOW_DEEP)
    c.line(hx + 13, hy + 2, hx + 27, 258, PURPLE_LIGHT)
    c.line(hx + 19, hy + 2, hx + 35, 257, SHADOW_DEEP)
    c.line(hx + 18, hy + 2, hx + 34, 257, PURPLE_LIGHT)

    # Horse Body Torso (barrel shape)
    c.circle(hx - 6, hy - 4, 12, SHADOW_DEEP)
    c.circle(hx + 6, hy - 4, 12, SHADOW_DEEP)
    c.rect(hx - 8, hy - 14, 16, 18, SHADOW_DEEP)
    # Saddle on back
    c.rect(hx - 8, hy - 17, 14, 4, SHADOW_DEEP)
    c.line(hx - 8, hy - 17, hx + 5, hy - 17, PURPLE_LIGHT) # saddle rim

    # Sculpted Horse Neck & Head
    # Arched neck rising forward
    for ny in range(hy - 28, hy - 8):
        progress = (ny - (hy - 28)) / 20.0
        nx = int(hx + 24 - progress * 16)
        c.line(nx - 4, ny, nx + 6, ny, SHADOW_DEEP)
        c.set_pixel(nx - 5, ny, PURPLE_LIGHT) # neck left rim

    # Expressive Head (y=206..218)
    c.circle(hx + 24, hy - 24, 7, SHADOW_DEEP)
    # Head crown & muzzle
    c.rect(hx + 24, hy - 25, 10, 6, SHADOW_DEEP)
    c.circle(hx + 33, hy - 22, 3, SHADOW_DEEP) # rounded muzzle
    # Pricked Ears
    c.line(hx + 21, hy - 32, hx + 23, hy - 27, SHADOW_DEEP)
    c.line(hx + 20, hy - 32, hx + 22, hy - 27, PURPLE_LIGHT)
    c.line(hx + 24, hy - 31, hx + 25, hy - 27, SHADOW_DEEP)

    # Head top rim-light
    c.line(hx + 22, hy - 29, hx + 34, hy - 25, PURPLE_LIGHT)
    c.set_pixel(hx + 35, hy - 24, PURPLE_LIGHT)

    # Flowing Mane Silhouette down neck
    c.set_pixel(hx + 17, hy - 25, PURPLE_LIGHT)
    c.set_pixel(hx + 14, hy - 21, PURPLE_LIGHT)
    c.set_pixel(hx + 10, hy - 16, PURPLE_LIGHT)

    # Curved Rocker Tail
    c.line(hx - 18, hy - 10, hx - 28, hy - 4, SHADOW_DEEP)
    c.line(hx - 28, hy - 4, hx - 26, hy + 4, SHADOW_DEEP)
    c.line(hx - 19, hy - 11, hx - 29, hy - 4, PURPLE_LIGHT)

    # Wooden Handlebars sticking out near base of neck
    c.rect(hx + 15, hy - 19, 6, 3, SHADOW_DEEP)
    c.circle(hx + 21, hy - 18, 2, SHADOW_DEEP)
    c.set_pixel(hx + 21, hy - 19, PURPLE_LIGHT)

    # Enforce strictly transparent above y=200
    for y in range(0, 200):
        for x in range(480):
            c.set_pixel(x, y, TRANSPARENT)

    return c


def generate_all_backgrounds():
    # 1. bg_sky_gradient.png (1x270)
    sky = generate_bg_sky_gradient()
    sky.to_image().save("art/incoming/bg_sky_gradient.png", "PNG")
    print(f"Saved art/incoming/bg_sky_gradient.png ({sky.width}x{sky.height})")

    # 2. bg_far.png (480x270)
    far = generate_bg_far()
    far.to_image().save("art/incoming/bg_far.png", "PNG")
    print(f"Saved art/incoming/bg_far.png ({far.width}x{far.height})")

    # 3. bg_far_stars.png (1920x270, 4 frames of 480x270)
    stars_frames = generate_bg_far_stars()
    assemble_strip(stars_frames, "art/incoming/bg_far_stars.png")

    # 4. bg_mid.png (640x270)
    mid = generate_bg_mid()
    mid.to_image().save("art/incoming/bg_mid.png", "PNG")
    print(f"Saved art/incoming/bg_mid.png ({mid.width}x{mid.height})")

    # 5. bg_near.png (480x270)
    near = generate_bg_near()
    near.to_image().save("art/incoming/bg_near.png", "PNG")
    print(f"Saved art/incoming/bg_near.png ({near.width}x{near.height})")


if __name__ == "__main__":
    generate_all_backgrounds()
