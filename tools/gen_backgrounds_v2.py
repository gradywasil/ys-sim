"""Younger Sibling Simulator - High-Resolution Backgrounds & Props Generator v2.

Redraws all parallax backgrounds, foreground layers, and ambient animated props
at their new v2 resolutions and delivers them directly into art/v2/.

Strictly uses the 64-color palette from tools/palette.py.
"""

import math
import json
import os
from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image

import sys
sys.path.append(os.path.dirname(__file__))

from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE,
    VOID_BLACK, SHADOW_PURPLE_DARK, SHADOW_PURPLE_DEEP, SHADOW_DEEP,
    SHADOW_PURPLE_MID, SHADOW_MID, PURPLE_DARK, PURPLE_MID, PURPLE_RICH,
    PURPLE_LIGHT, DUSK_LILAC, DUSK_PINK, DUSK_ROSE, DUSK_PEACH, DUSK_BLUSH, DUSK_CREAM,
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


# =============================================================================
# 1. PARALLAX BACKGROUNDS & FOREGROUNDS
# =============================================================================

def generate_bg_sky_gradient() -> PixelCanvas:
    """
    1x540 px: Smooth discrete hard color bands from twilight purple down to warm plum.
    8 discrete bands across 540 vertical pixels.
    """
    c = PixelCanvas(1, 540)
    bands = [
        (0, 68, VOID_BLACK),           # Band 0: Deepest void twilight
        (68, 136, OUTLINE),            # Band 1: Midnight purple
        (136, 203, SHADOW_PURPLE_DARK),# Band 2: Deep dusk shadow
        (203, 270, SHADOW_PURPLE_DEEP),# Band 3: Dark purple shadow
        (270, 338, SHADOW_PURPLE_MID), # Band 4: Rich dusk purple
        (338, 406, PURPLE_MID),        # Band 5: Twilight violet
        (406, 473, DUSK_LILAC),        # Band 6: Lilac rose
        (473, 540, DUSK_PEACH),        # Band 7: Warm luminous plum
    ]
    for y_start, y_end, color in bands:
        for y in range(y_start, y_end):
            c.set_pixel(0, y, color)
    return c


def generate_bg_far() -> PixelCanvas:
    """
    960x540 px: Far background wall.
    - Seamless horizontal tiling (period 48 px divides evenly into 960).
    - Wallpaper with subtle diamond pattern, crown moulding along top, baseboard moulding.
    - Wall decor:
      * Door frame with height chart marks (x=24..110, y=90..476)
      * Framed family photos (x=130..250, y=105..260)
      * Felt sports pennant (x=270..380, y=110..180)
      * Wall clock (x=400..465, y=90..155)
      * Corkboard of doodles (x=490..625, y=110..280)
      * Large wooden framed window with moon and stars (x=650..820, y=50..310)
      * Retro rocket poster (x=845..945, y=100..290)
    """
    c = PixelCanvas(960, 540, SHADOW_PURPLE_MID)

    # --- 1. Ceiling Crown Moulding (y=0..15) ---
    c.rect(0, 0, 960, 2, OUTLINE)
    c.rect(0, 2, 960, 2, SHADOW_PURPLE_DEEP)
    c.rect(0, 4, 960, 2, PURPLE_MID)
    c.rect(0, 6, 960, 2, PURPLE_LIGHT)
    c.rect(0, 8, 960, 4, SHADOW_PURPLE_MID)
    # Repeating dentils
    for x in range(0, 960, 16):
        c.rect(x + 2, 8, 10, 4, PURPLE_MID)
        c.rect(x + 2, 8, 10, 1, PURPLE_LIGHT)
        c.line(x + 11, 8, x + 11, 11, SHADOW_PURPLE_DEEP)
    c.rect(0, 12, 960, 2, SHADOW_PURPLE_DEEP)
    c.rect(0, 14, 960, 2, OUTLINE)

    # --- 2. Seamless Diamond Wallpaper Pattern (period = 48 px, 960 / 48 = 20 repeats) ---
    for y in range(16, 476):
        for x in range(960):
            gx = x % 48
            gy = (y - 16) % 48
            dx = abs(gx - 24)
            dy = abs(gy - 24)
            dist = dx + dy
            # Outer diamond line
            if dist == 20:
                c.set_pixel(x, y, PURPLE_MID)
            elif dist == 19:
                c.set_pixel(x, y, PURPLE_RICH)
            # Inner diamond accent
            elif dist == 6:
                c.set_pixel(x, y, PURPLE_LIGHT)
            elif dist in (1, 2):
                c.set_pixel(x, y, DUSK_LILAC)
            elif dist == 0:
                c.set_pixel(x, y, DUSK_PINK)
            # Corner grid florets (at x%48==0, y%48==0)
            elif (gx <= 2 or gx >= 46) and (gy <= 2 or gy >= 46):
                if gx in (0, 47) and gy in (0, 47):
                    c.set_pixel(x, y, DUSK_ROSE)
                elif gx in (1, 46) or gy in (1, 46):
                    c.set_pixel(x, y, PURPLE_LIGHT)

    # --- 3. Baseboard Moulding Along Bottom (y=476..540, 64 px) ---
    c.line(0, 476, 959, 476, WOOD_HIGHLIGHT)
    c.line(0, 477, 959, 477, BROWN_LIGHT)
    c.line(0, 478, 959, 478, BROWN_MID)
    c.line(0, 479, 959, 479, BROWN_DARKEST)
    c.line(0, 480, 959, 480, WOOD_HIGHLIGHT)
    c.line(0, 481, 959, 481, BROWN_LIGHT)
    c.line(0, 482, 959, 482, BROWN_MID)
    # Main plinth board
    c.rect(0, 483, 960, 46, BROWN_DARK)
    for x in range(960):
        if x % 48 == 0:
            c.line(x, 483, x, 528, BROWN_MID)
        elif x % 48 == 1:
            c.line(x, 483, x, 528, BROWN_DARKEST)
        elif x % 24 == 12 and (x // 24) % 2 == 0:
            c.set_pixel(x, 500, BROWN_MID)
            c.set_pixel(x + 1, 501, BROWN_MID)
            c.set_pixel(x, 502, BROWN_DARKEST)
    # Shoe moulding
    c.line(0, 529, 959, 529, WOOD_HIGHLIGHT)
    c.line(0, 530, 959, 530, BROWN_LIGHT)
    c.line(0, 531, 959, 531, BROWN_MID)
    c.rect(0, 532, 960, 5, BROWN_DARK)
    c.line(0, 537, 959, 537, BROWN_DARKEST)
    c.rect(0, 538, 960, 2, OUTLINE)

    # --- 4. Door Frame with Height Chart Marks (x=24..110, y=90..476) ---
    # Wall drop shadow
    c.rect(111, 94, 6, 382, SHADOW_PURPLE_DEEP)
    # Left door panel visible (recessed door)
    c.rect(24, 94, 56, 382, BROWN_DARKEST)
    c.rect(28, 108, 48, 140, BROWN_DARK, outline=BROWN_MID)
    c.rect(28, 270, 48, 190, BROWN_DARK, outline=BROWN_MID)
    # Brass doorknob
    c.circle(70, 330, 5, YELLOW_MID, outline=YELLOW_SHADOW)
    c.set_pixel(69, 329, YELLOW_LIGHT)
    c.set_pixel(69, 328, PURE_WHITE)
    c.rect(68, 336, 4, 8, YELLOW_SHADOW, outline=BROWN_DARKEST)
    # Wooden Door Casing Architrave (x=80..110, y=90..476)
    c.rect(80, 90, 31, 386, BROWN_MID, outline=BROWN_DARKEST)
    c.line(80, 90, 80, 475, WOOD_HIGHLIGHT)
    c.line(81, 90, 81, 475, BROWN_LIGHT)
    c.line(109, 90, 109, 475, BROWN_DARKEST)
    c.line(110, 90, 110, 475, OUTLINE)
    # Lintel over door
    c.rect(20, 86, 95, 12, BROWN_MID, outline=BROWN_DARKEST)
    c.line(20, 86, 114, 86, WOOD_HIGHLIGHT)
    c.line(20, 87, 114, 87, BROWN_LIGHT)

    # Height Chart Marks etched onto door frame casing (x=86..106)
    # Measurement ruler tick marks
    for hy in range(160, 460, 6):
        is_major = (hy % 24 == 0)
        w = 12 if is_major else 6
        c.line(86, hy, 86 + w, hy, BROWN_DARKEST)
        c.line(86, hy + 1, 86 + w, hy + 1, WOOD_HIGHLIGHT)

    # Child pencil growth scribbles with ages & dates:
    # y=420: "Age 2" + baby doodle
    c.line(92, 420, 104, 420, BROWN_DARKEST)
    c.set_pixel(94, 417, YELLOW_MID)
    c.set_pixel(95, 417, YELLOW_MID)
    c.set_pixel(95, 418, ORANGE_MID) # tiny chick doodle
    # y=360: "Age 4"
    c.line(92, 360, 104, 360, BROWN_DARKEST)
    c.line(94, 355, 100, 355, DUSK_CREAM)
    # y=300: "Age 6" (Big Sis)
    c.line(92, 300, 106, 300, BROWN_DARKEST)
    c.line(94, 296, 102, 296, BLUE_LIGHT)
    # y=240: "Age 8" + star
    c.line(90, 240, 106, 240, BROWN_DARKEST)
    c.set_pixel(96, 236, YELLOW_LIGHT)
    c.set_pixel(95, 237, YELLOW_MID)
    c.set_pixel(97, 237, YELLOW_MID)
    c.set_pixel(96, 238, YELLOW_MID)
    # y=190: "NOW!" with energetic red notch
    c.line(88, 190, 107, 190, RED_MID)
    c.line(88, 191, 107, 191, RED_LIGHT)
    c.set_pixel(98, 186, RED_LIGHT)
    c.set_pixel(97, 187, RED_MID)
    c.set_pixel(99, 187, RED_MID)

    # --- 5. Framed Family Photos (x=130..250, y=105..265) ---
    # Wall picture nails and cord
    c.set_pixel(165, 102, YELLOW_MID)
    c.line(165, 103, 140, 114, BROWN_DARKEST)
    c.line(165, 103, 190, 114, BROWN_DARKEST)
    # Photo 1 (Big wooden frame, x=135..195, y=114..185)
    c.rect(138, 117, 60, 71, SHADOW_PURPLE_DEEP) # drop shadow
    c.rect(135, 114, 60, 71, BROWN_MID, outline=BROWN_DARKEST)
    c.line(135, 114, 194, 114, WOOD_HIGHLIGHT)
    c.line(135, 115, 194, 115, BROWN_LIGHT)
    c.line(135, 114, 135, 184, WOOD_HIGHLIGHT)
    # Photo paper
    c.rect(142, 121, 46, 57, DUSK_CREAM)
    # Sky and tree in photo
    c.rect(142, 121, 46, 32, BLUE_LIGHT)
    c.circle(178, 134, 10, GREEN_MID, outline=GREEN_SHADOW)
    c.rect(176, 144, 4, 14, BROWN_DARK)
    c.rect(142, 150, 46, 10, GREEN_LIGHT) # lawn
    # Sibling stick figures smiling in photo
    # Older sibling (hoodie)
    c.circle(153, 140, 4, SKIN_LIGHT, outline=SKIN_MID)
    c.rect(151, 144, 5, 8, RED_MID)
    c.line(152, 152, 152, 158, BLUE_MID)
    c.line(154, 152, 154, 158, BLUE_MID)
    # Younger sibling
    c.circle(163, 144, 3, SKIN_LIGHT, outline=SKIN_MID)
    c.rect(161, 147, 5, 6, BLUE_LIGHT)
    c.line(162, 153, 162, 158, GREEN_MID)
    c.line(164, 153, 164, 158, GREEN_MID)
    # Glass glare across frame
    c.line(144, 122, 170, 148, PURE_WHITE)
    c.line(145, 122, 171, 148, WHITE_MID)

    # Photo 2 (Gold oval frame, x=205..250, y=120..175)
    c.rect(208, 123, 44, 54, SHADOW_PURPLE_DEEP) # shadow
    c.circle(227, 147, 21, YELLOW_MID, outline=YELLOW_SHADOW)
    c.circle(227, 147, 18, YELLOW_LIGHT, outline=YELLOW_DEEP)
    c.circle(227, 147, 15, DUSK_CREAM)
    # Baby P1 face portrait
    c.circle(227, 147, 9, SKIN_LIGHT, outline=SKIN_MID)
    c.set_pixel(225, 145, OUTLINE)
    c.set_pixel(229, 145, OUTLINE)
    c.circle(227, 141, 10, DUSK_PINK, outline=DUSK_ROSE) # baby bonnet
    c.circle(227, 152, 2, RED_LIGHT) # pacifier

    # Photo 3 (Curled sleeping cat photo, x=155..220, y=195..260)
    c.rect(158, 198, 64, 64, SHADOW_PURPLE_DEEP)
    c.rect(155, 195, 64, 64, BROWN_DARK, outline=BROWN_DARKEST)
    c.line(155, 195, 218, 195, WOOD_HIGHLIGHT)
    c.rect(161, 201, 52, 52, DUSK_CREAM)
    # Rug carpet in photo
    c.rect(161, 226, 52, 27, TEAL_MID)
    # Sleeping orange striped tabby cat
    c.circle(187, 232, 14, ORANGE_MID, outline=BROWN_DARKEST)
    c.circle(196, 228, 9, ORANGE_MID, outline=BROWN_DARKEST)
    # Ears
    c.line(196, 219, 199, 224, ORANGE_LIGHT)
    c.line(201, 220, 203, 224, ORANGE_LIGHT)
    # Closed sleeping eyes
    c.line(197, 228, 199, 228, BROWN_DARKEST)
    c.line(201, 228, 203, 228, BROWN_DARKEST)
    # Stripes
    c.line(184, 224, 188, 222, BROWN_MID)
    c.line(182, 230, 187, 229, BROWN_MID)
    # Curled tail
    for ta in range(16):
        c.set_pixel(174 + int(math.cos(ta * 0.2) * 5), 235 + int(math.sin(ta * 0.2) * 5), ORANGE_MID)

    # --- 6. Pennant (x=270..380, y=110..185) ---
    # Wall drop shadow
    c.polygon([(277, 125), (377, 152), (277, 182)], fill=SHADOW_PURPLE_DEEP)
    # Pennant body
    c.polygon([(275, 120), (375, 147), (275, 175)], fill=RED_MID, outline=RED_DEEP)
    c.line(275, 120, 375, 147, RED_LIGHT)
    # Contrast band along wide edge
    c.rect(273, 118, 5, 60, YELLOW_MID, outline=YELLOW_SHADOW)
    c.set_pixel(275, 120, PURE_WHITE)
    c.set_pixel(275, 176, PURE_WHITE)
    # Hanging ribbon tassels
    c.line(273, 120, 268, 134, YELLOW_LIGHT)
    c.line(273, 176, 267, 190, YELLOW_LIGHT)
    # Gold lettering / star motif
    c.set_pixel(300, 140, YELLOW_LIGHT)
    c.circle(302, 143, 3, YELLOW_MID, outline=YELLOW_LIGHT) # star
    # Letters "ROCKETS" stylized
    c.line(316, 141, 316, 149, YELLOW_LIGHT) # R
    c.line(316, 141, 320, 141, YELLOW_LIGHT)
    c.line(320, 141, 320, 145, YELLOW_LIGHT)
    c.line(316, 145, 320, 145, YELLOW_LIGHT)
    c.line(318, 145, 321, 149, YELLOW_LIGHT)
    c.rect(324, 143, 4, 6, YELLOW_LIGHT, outline=RED_MID) # O
    c.line(333, 144, 330, 144, YELLOW_LIGHT) # C
    c.line(330, 144, 330, 148, YELLOW_LIGHT)
    c.line(330, 148, 333, 148, YELLOW_LIGHT)
    c.line(336, 144, 336, 148, YELLOW_LIGHT) # K
    c.line(336, 146, 339, 144, YELLOW_LIGHT)
    c.line(336, 146, 339, 148, YELLOW_LIGHT)

    # --- 7. Wall Clock (x=400..465, y=90..155) ---
    c.circle(434, 124, 30, SHADOW_PURPLE_DEEP) # drop shadow
    c.circle(432, 122, 30, BROWN_MID, outline=BROWN_DARKEST)
    c.circle(432, 122, 28, WOOD_HIGHLIGHT)
    c.circle(432, 122, 26, BROWN_DARK)
    c.circle(432, 122, 24, DUSK_CREAM, outline=OUTLINE)
    # Dial marks for 12, 3, 6, 9
    c.line(432, 100, 432, 104, OUTLINE) # 12
    c.line(432, 140, 432, 144, OUTLINE) # 6
    c.line(450, 122, 454, 122, OUTLINE) # 3
    c.line(410, 122, 414, 122, OUTLINE) # 9
    # Minor marks
    for deg in [30, 60, 120, 150, 210, 240, 300, 330]:
        rad = math.radians(deg)
        mx = int(432 + math.cos(rad) * 20)
        my = int(122 + math.sin(rad) * 20)
        c.set_pixel(mx, my, SHADOW_PURPLE_MID)
    # Hands showing 8:20
    # Hour hand (pointing to 8)
    c.line(432, 122, 421, 130, OUTLINE)
    c.line(432, 121, 421, 129, OUTLINE)
    # Minute hand (pointing to 4 / 20 min)
    c.line(432, 122, 448, 131, OUTLINE)
    c.line(432, 123, 448, 132, SHADOW_PURPLE_DARK)
    # Red second hand
    c.line(432, 122, 436, 106, RED_MID)
    c.circle(432, 122, 2, YELLOW_MID, outline=OUTLINE)
    # Glass glare streak
    c.line(416, 110, 444, 104, PURE_WHITE)

    # --- 8. Corkboard of Doodles (x=490..625, y=110..280) ---
    c.rect(494, 114, 135, 170, SHADOW_PURPLE_DEEP) # drop shadow
    # Pine frame
    c.rect(490, 110, 135, 170, BROWN_MID, outline=BROWN_DARKEST)
    c.line(490, 110, 624, 110, WOOD_HIGHLIGHT)
    c.line(490, 110, 490, 279, WOOD_HIGHLIGHT)
    c.line(491, 111, 623, 111, BROWN_LIGHT)
    c.line(491, 111, 491, 278, BROWN_LIGHT)
    c.line(490, 279, 624, 279, BROWN_DARKEST)
    c.line(624, 110, 624, 279, BROWN_DARKEST)
    # Cork field with textured dither
    for cy in range(118, 272):
        for cx in range(498, 617):
            if (cx + cy) % 4 == 0:
                c.set_pixel(cx, cy, WOOD_LIT)
            elif (cx * 3 + cy) % 5 == 0:
                c.set_pixel(cx, cy, BROWN_LIGHT)
            else:
                c.set_pixel(cx, cy, WOOD_HIGHLIGHT)

    # Pinned Drawing 1: Green Dinosaur doodle (x=505..555, y=125..185)
    c.rect(505, 125, 52, 62, PURE_WHITE, outline=WHITE_SHADOW)
    # Red pushpin at top-center
    c.circle(530, 127, 2, RED_MID, outline=OUTLINE)
    c.set_pixel(529, 126, PURE_WHITE)
    # Green cartoon dinosaur in crayon
    c.circle(530, 155, 12, GREEN_MID, outline=GREEN_SHADOW)
    c.circle(538, 146, 8, GREEN_MID, outline=GREEN_SHADOW)
    c.rect(542, 144, 8, 8, GREEN_MID, outline=GREEN_SHADOW) # snout
    c.set_pixel(540, 144, OUTLINE) # eye
    c.set_pixel(546, 150, PURE_WHITE) # tooth
    # Orange back spikes
    c.set_pixel(526, 143, ORANGE_MID)
    c.set_pixel(522, 146, ORANGE_MID)
    c.set_pixel(519, 150, ORANGE_MID)
    # Legs & tail
    c.rect(524, 165, 4, 10, GREEN_MID)
    c.rect(532, 165, 4, 10, GREEN_MID)
    c.line(519, 158, 510, 162, GREEN_MID)
    # Fire puff
    c.circle(553, 148, 2, RED_LIGHT)
    c.set_pixel(554, 148, YELLOW_LIGHT)

    # Pinned Paper 2: School Test "100% A+" (x=562..610, y=130..190)
    c.rect(562, 130, 48, 60, PURE_WHITE, outline=WHITE_SHADOW)
    # Yellow pushpin
    c.circle(586, 132, 2, YELLOW_MID, outline=OUTLINE)
    # Ruled notebook lines
    for lny in range(140, 185, 6):
        c.line(566, lny, 606, lny, BLUE_LIGHT)
    # Big red crayon "100% A+" with circle
    c.circle(586, 158, 12, RED_MID, outline=RED_LIGHT)
    c.line(582, 152, 582, 162, RED_MID) # "A"
    c.line(582, 152, 586, 152, RED_MID)
    c.line(586, 152, 586, 162, RED_MID)
    c.line(582, 157, 586, 157, RED_MID)
    c.line(590, 155, 590, 159, RED_MID) # "+"
    c.line(588, 157, 592, 157, RED_MID)

    # Pinned Note 3: Folded paper airplane & note (x=515..585, y=200..265)
    c.rect(515, 202, 45, 55, DUSK_CREAM, outline=DUSK_ROSE)
    c.circle(537, 204, 2, BLUE_MID, outline=OUTLINE)
    # Sibling crayon figures holding hands under sun
    c.circle(548, 212, 4, YELLOW_MID, outline=YELLOW_LIGHT)
    c.circle(528, 225, 3, SKIN_LIGHT)
    c.line(528, 228, 528, 238, RED_MID)
    c.circle(538, 227, 2, SKIN_LIGHT)
    c.line(538, 229, 538, 238, BLUE_LIGHT)
    c.line(528, 232, 538, 232, SKIN_LIGHT) # hands held
    c.set_pixel(533, 228, RED_LIGHT) # heart
    # Folded Paper Airplane pinned at angle (x=570..612, y=205..250)
    c.polygon([(575, 215), (610, 205), (595, 245)], fill=PURE_WHITE, outline=WHITE_SHADOW)
    c.line(575, 215, 600, 225, METAL_MID) # center crease
    c.circle(590, 220, 2, GREEN_MID, outline=OUTLINE) # pushpin

    # --- 9. Large Wooden Framed Window (x=650..820, y=50..310) ---
    # Wall drop shadow beneath sill and right jamb
    c.rect(654, 311, 172, 8, SHADOW_PURPLE_DEEP)
    c.rect(821, 58, 8, 252, SHADOW_PURPLE_DEEP)

    # Architectural Window Header (Entablature, x=644..826, y=46..58)
    c.rect(644, 46, 182, 12, BROWN_MID, outline=BROWN_DARKEST)
    c.line(644, 46, 825, 46, WOOD_HIGHLIGHT)
    c.line(644, 47, 825, 47, BROWN_LIGHT)
    c.line(644, 57, 825, 57, BROWN_DARKEST)

    # Window Sill (Ledge at bottom, x=640..830, y=298..310)
    c.rect(640, 298, 190, 12, BROWN_MID, outline=BROWN_DARKEST)
    c.line(640, 298, 829, 298, WOOD_HIGHLIGHT)
    c.line(640, 299, 829, 299, WOOD_HIGHLIGHT)
    c.line(640, 300, 829, 300, BROWN_LIGHT)
    c.line(640, 309, 829, 309, BROWN_DARKEST)

    # Outer Frame Jambs
    c.rect(650, 58, 170, 240, BROWN_DARK, outline=BROWN_DARKEST)
    c.line(650, 58, 650, 297, WOOD_HIGHLIGHT)
    c.line(651, 58, 651, 297, BROWN_MID)
    c.line(818, 58, 818, 297, BROWN_DARKEST)
    c.line(819, 58, 819, 297, OUTLINE)

    # Glass Panes Area: x=660..810, y=66..290
    # Fill glass area with deep twilight sky gradient
    for gy in range(66, 290):
        if gy < 120:
            col = VOID_BLACK
        elif gy < 180:
            col = SHADOW_PURPLE_DARK
        elif gy < 235:
            col = SHADOW_PURPLE_DEEP
        else:
            col = SHADOW_PURPLE_MID
        c.line(660, gy, 810, gy, col)

    # Distant silhouetted neighborhood horizon (y=260..290)
    # Rooftops, gables, chimney with smoke, and pine treetops
    for hx in range(660, 811):
        # Wave/roof silhouette
        roof1 = 275 + int(math.sin((hx - 660) * 0.12) * 5)
        if 710 <= hx <= 750: # peaked gable
            roof1 = 262 + abs(hx - 730)
        c.line(hx, roof1, hx, 289, VOID_BLACK)
    # Chimney at x=740
    c.rect(740, 252, 10, 18, VOID_BLACK)
    # Smoke curl in sky
    c.set_pixel(746, 248, SHADOW_PURPLE_DEEP)
    c.set_pixel(748, 245, SHADOW_PURPLE_MID)
    c.set_pixel(752, 243, SHADOW_PURPLE_MID)

    # Crescent Moon in upper left pane (cx=695, cy=105, radius 20)
    # Soft purple/lilac halo
    for my in range(80, 131):
        for mx in range(670, 721):
            dist_m = math.sqrt((mx - 695) ** 2 + (my - 105) ** 2)
            if 20.0 < dist_m <= 26.0 and (mx + my) % 2 == 0:
                c.set_pixel(mx, my, PURPLE_LIGHT)
    # Golden moon body
    c.circle(695, 105, 20, YELLOW_LIGHT, outline=YELLOW_MID)
    c.line(678, 100, 678, 110, PURE_WHITE)
    c.line(679, 94, 683, 90, PURE_WHITE)
    c.line(679, 116, 683, 120, PURE_WHITE)
    # Cutout to form perfect crescent
    c.circle(703, 101, 18, VOID_BLACK)

    # Distant Fixed Stars in window glass
    window_stars = [
        (672, 80), (715, 75), (676, 138), (712, 145),
        (750, 78), (785, 82), (800, 110), (765, 130), (792, 142),
        (674, 195), (710, 205), (680, 235), (715, 245),
        (748, 192), (788, 200), (762, 230), (802, 240)
    ]
    for sx, sy in window_stars:
        col_s = YELLOW_LIGHT if (sx + sy) % 3 == 0 else PURE_WHITE
        c.set_pixel(sx, sy, col_s)

    # Wooden Window Mullions (dividing into 4 classic panes)
    # Vertical mullion (x=731..739, y=66..290)
    c.rect(731, 66, 8, 224, BROWN_MID, outline=BROWN_DARKEST)
    c.line(731, 66, 731, 289, WOOD_HIGHLIGHT)
    c.line(732, 66, 732, 289, BROWN_LIGHT)
    c.line(738, 66, 738, 289, BROWN_DARKEST)
    # Horizontal transom bar (x=660..810, y=174..182)
    c.rect(660, 174, 150, 8, BROWN_MID, outline=BROWN_DARKEST)
    c.line(660, 174, 809, 174, WOOD_HIGHLIGHT)
    c.line(660, 175, 809, 175, BROWN_LIGHT)
    c.line(660, 181, 809, 181, BROWN_DARKEST)

    # Glass specular glare streaks crossing panes
    c.line(668, 70, 720, 170, WHITE_SHADOW)
    c.line(674, 70, 726, 170, WHITE_MID)
    c.line(748, 70, 800, 170, WHITE_SHADOW)

    # --- 10. Retro Rocket Poster (x=845..945, y=100..290) ---
    c.rect(849, 104, 100, 190, SHADOW_PURPLE_DEEP) # drop shadow
    # Outer poster border
    c.rect(845, 100, 100, 190, VOID_BLACK, outline=WHITE_SHADOW)
    c.rect(849, 104, 92, 182, SHADOW_PURPLE_DEEP, outline=PURPLE_MID)
    c.rect(852, 107, 86, 176, VOID_BLACK)

    # Poster Deep Space Artwork:
    # Saturn-like ringed planet at top right (898, 126)
    c.circle(898, 126, 9, ORANGE_MID, outline=ORANGE_SHADOW)
    c.line(884, 131, 912, 121, YELLOW_LIGHT) # ring
    c.line(885, 132, 913, 122, YELLOW_MID)
    # Nebula cloud swirls
    for ny in range(112, 140):
        for nx in range(855, 890):
            if (nx * 2 + ny * 3) % 7 == 0:
                c.set_pixel(nx, ny, DUSK_PINK)

    # Vintage Atomic Rocket Ship (centered at x=895, y=170)
    # Sleek Red nose cone
    c.set_pixel(895, 146, RED_LIGHT)
    c.line(894, 147, 896, 147, RED_LIGHT)
    c.line(893, 148, 897, 148, RED_MID)
    c.line(892, 149, 898, 149, RED_MID)
    c.line(891, 150, 899, 150, RED_SHADOW)
    # White atomic fuselage
    for fy in range(151, 195):
        c.line(890, fy, 900, fy, PURE_WHITE)
        c.set_pixel(890, fy, WHITE_SHADOW)
        c.set_pixel(900, fy, WHITE_SHADOW)
    # Red racing stripes down fuselage
    c.rect(890, 168, 11, 5, RED_MID)
    c.line(890, 170, 900, 170, RED_LIGHT)
    # Circular chrome porthole with cyan shine
    c.circle(895, 160, 4, METAL_MID, outline=OUTLINE)
    c.circle(895, 160, 3, BLUE_LIGHT)
    c.set_pixel(894, 159, PURE_WHITE)
    # Swept retro fins
    # Left fin
    c.polygon([(890, 180), (878, 196), (890, 196)], fill=RED_MID, outline=RED_SHADOW)
    c.line(890, 180, 878, 196, RED_LIGHT)
    # Right fin
    c.polygon([(900, 180), (912, 196), (900, 196)], fill=RED_MID, outline=RED_SHADOW)
    c.line(900, 180, 912, 196, RED_LIGHT)
    # Center dorsal fin
    c.line(895, 180, 895, 196, RED_LIGHT)
    # Engine bell nozzle
    c.rect(891, 196, 9, 4, BROWN_DARKEST)

    # Blazing Rocket Thruster Exhaust Flame!
    # Core white blast
    c.polygon([(893, 200), (897, 200), (895, 216)], fill=PURE_WHITE)
    # Yellow flame cone
    c.polygon([(890, 200), (900, 200), (895, 230)], fill=YELLOW_LIGHT, outline=YELLOW_MID)
    # Orange billow & shock diamonds
    c.circle(895, 238, 6, ORANGE_MID, outline=ORANGE_SHADOW)
    c.circle(895, 252, 9, ORANGE_MID, outline=RED_SHADOW)
    # Sparks trailing down
    c.set_pixel(892, 265, YELLOW_LIGHT)
    c.set_pixel(897, 268, RED_LIGHT)
    c.set_pixel(894, 274, RED_MID)

    # 4 Corner Pushpins (pins holding poster)
    c.circle(848, 103, 2, RED_MID, outline=OUTLINE)
    c.circle(941, 103, 2, YELLOW_MID, outline=OUTLINE)
    c.circle(848, 286, 2, BLUE_MID, outline=OUTLINE)
    c.circle(941, 286, 2, GREEN_MID, outline=OUTLINE)

    return c


def generate_bg_far_stars() -> List[PixelCanvas]:
    """
    4 frames of twinkling stars inside the window panes.
    960x540 per frame, assembled into 3840x540 px strip (fps 3, loop: true).
    Transparent canvas overlaying bg_far.png.
    """
    frames = []
    # Stars located strictly within window panes (x=660..810, y=66..290)
    stars_coords = [
        # Top-left pane (around crescent moon)
        (672, 80), (688, 72), (715, 75), (676, 138), (702, 142), (718, 130), (680, 160),
        # Top-right pane
        (750, 78), (768, 70), (785, 82), (800, 110), (745, 120), (765, 130), (792, 142), (804, 162),
        # Bottom-left pane
        (674, 195), (690, 190), (710, 205), (680, 235), (700, 240), (715, 245), (688, 255),
        # Bottom-right pane
        (748, 192), (772, 196), (788, 200), (752, 222), (762, 230), (780, 238), (802, 240), (790, 255)
    ]

    for f in range(4):
        c = PixelCanvas(960, 540, TRANSPARENT)
        for i, (sx, sy) in enumerate(stars_coords):
            phase = (i * 3 + f) % 4
            if phase == 0:
                # 4-pointed cross sparkle
                c.set_pixel(sx, sy, PURE_WHITE)
                c.set_pixel(sx - 1, sy, YELLOW_LIGHT)
                c.set_pixel(sx + 1, sy, YELLOW_LIGHT)
                c.set_pixel(sx, sy - 1, YELLOW_LIGHT)
                c.set_pixel(sx, sy + 1, YELLOW_LIGHT)
                c.set_pixel(sx - 2, sy, YELLOW_MID)
                c.set_pixel(sx + 2, sy, YELLOW_MID)
            elif phase == 1:
                # Brilliant intense dot
                c.set_pixel(sx, sy, PURE_WHITE)
                c.set_pixel(sx, sy - 1, BLUE_LIGHT)
            elif phase == 2:
                # Warm radiant star (2x2)
                c.set_pixel(sx, sy, YELLOW_LIGHT)
                c.set_pixel(sx + 1, sy, YELLOW_MID)
            else:
                # Dim glint
                c.set_pixel(sx, sy, PURPLE_LIGHT)

        # Shooting star / comet streak gliding across top-right pane in frames 1..3
        if f == 1:
            c.line(755, 76, 765, 84, PURE_WHITE)
            c.line(752, 74, 755, 76, BLUE_LIGHT)
        elif f == 2:
            c.line(766, 85, 778, 95, PURE_WHITE)
            c.line(760, 80, 766, 85, BLUE_LIGHT)
            c.line(755, 76, 760, 80, PURPLE_LIGHT)
        elif f == 3:
            c.line(779, 96, 792, 107, PURE_WHITE)
            c.line(773, 91, 779, 96, BLUE_LIGHT)
            c.line(768, 87, 773, 91, PURPLE_LIGHT)

        frames.append(c)

    return frames


def generate_bg_mid() -> PixelCanvas:
    """
    1280x540 px: Mid-ground bedroom scene.
    - Seamless horizontal tiling at floor level y=400 (x=0 matches x=1279, both open floor buffer).
    - Bookshelves with uneven book heights and leaning books (x=50..260, y=80..400)
    - Globe on stand (x=275..335, y=290..400)
    - Guitar on stand (x=350..415, y=250..400)
    - Desk with glowing monitor (x=430..620, y=200..400)
    - Bed with rumpled blankets and plush toys (x=640..940, y=160..400)
    - Beanbag (x=960..1060, y=290..400)
    - Toy chest spilling toys (x=1080..1230, y=240..400)
    """
    c = PixelCanvas(1280, 540, TRANSPARENT)

    # -------------------------------------------------------------------------
    # 1. TALL BOOKSHELF (x=50..260, y=80..400)
    # -------------------------------------------------------------------------
    # Top Crown Moulding / Cornice (x=44..266, y=76..92)
    c.rect(44, 76, 222, 6, BROWN_MID, outline=BROWN_DARKEST)
    c.line(44, 76, 265, 76, WOOD_HIGHLIGHT)
    c.line(44, 77, 265, 77, BROWN_LIGHT)
    c.rect(48, 82, 214, 10, BROWN_LIGHT, outline=BROWN_DARKEST)

    # Left & Right Uprights
    c.rect(50, 92, 14, 304, BROWN_MID, outline=BROWN_DARKEST)
    c.line(50, 92, 50, 395, WOOD_HIGHLIGHT)
    c.line(51, 92, 51, 395, BROWN_LIGHT)
    c.rect(246, 92, 14, 304, BROWN_DARK, outline=BROWN_DARKEST)
    c.line(246, 92, 246, 395, BROWN_DARKEST)

    # Dark Wooden Backboard behind shelves
    c.rect(64, 92, 182, 304, SHADOW_PURPLE_DEEP)

    # 4 Shelves (y=160, y=240, y=320, y=394)
    for sy in [160, 240, 320, 394]:
        c.rect(64, sy, 182, 10, BROWN_MID, outline=BROWN_DARKEST)
        c.line(64, sy, 245, sy, WOOD_HIGHLIGHT)
        c.line(64, sy + 1, 245, sy + 1, BROWN_LIGHT)
        c.line(64, sy + 9, 245, sy + 9, BROWN_DARKEST)

    # Bookshelf Plinth Base (resting on floor at y=400)
    c.rect(46, 396, 218, 8, BROWN_DARK, outline=BROWN_DARKEST)
    c.line(46, 396, 263, 396, WOOD_HIGHLIGHT)
    c.line(42, 400, 268, 400, SHADOW_PURPLE_DEEP) # floor contact shadow

    # Shelf 1: Potted trailing ivy plant + horizontal books + leaning book
    # Terracotta pot on left
    c.rect(68, 126, 22, 22, BROWN_LIGHT, outline=BROWN_DARKEST)
    c.line(67, 125, 90, 125, WOOD_HIGHLIGHT)
    # Trailing green ivy vines cascading down side of shelf
    for vy in range(115, 175):
        c.set_pixel(64 + int(math.sin(vy * 0.2) * 4), vy, GREEN_MID)
        if vy % 6 == 0:
            c.circle(64 + int(math.sin(vy * 0.2) * 4), vy, 3, GREEN_LIGHT, outline=GREEN_SHADOW)
    # Stack of 4 horizontal books (x=100..155, y=124..160)
    book_colors = [(RED_MID, RED_LIGHT), (BLUE_MID, BLUE_LIGHT), (YELLOW_MID, YELLOW_LIGHT), (GREEN_MID, GREEN_LIGHT)]
    for i, (bcol, bhl) in enumerate(book_colors):
        by = 151 - i * 9
        c.rect(102, by, 50, 9, bcol, outline=OUTLINE)
        c.line(103, by + 1, 151, by + 1, bhl)
    # Standing books + bronze owl bookend on right
    c.rect(162, 108, 12, 52, PURPLE_LIGHT, outline=OUTLINE)
    c.line(163, 109, 163, 159, DUSK_PINK)
    c.rect(176, 114, 10, 46, ORANGE_MID, outline=OUTLINE)
    # Leaning book (x=190..215, leaning right)
    for ly in range(112, 160):
        lx = int(190 + (ly - 112) * 0.35)
        c.line(lx, ly, lx + 10, ly, BLUE_MID)
        c.set_pixel(lx, ly, BLUE_LIGHT)
    # Bronze owl bookend
    c.circle(225, 142, 10, YELLOW_MID, outline=YELLOW_SHADOW)
    c.circle(222, 138, 3, PURE_WHITE, outline=OUTLINE)
    c.circle(228, 138, 3, PURE_WHITE, outline=OUTLINE)

    # Shelf 2: Stuffed with colorful books of uneven heights (spines with titles)
    shelf_palette = [
        (RED_MID, RED_LIGHT, RED_SHADOW),
        (BLUE_MID, BLUE_LIGHT, BLUE_SHADOW),
        (YELLOW_MID, YELLOW_LIGHT, YELLOW_SHADOW),
        (GREEN_MID, GREEN_LIGHT, GREEN_SHADOW),
        (PURPLE_LIGHT, DUSK_PINK, PURPLE_MID),
        (ORANGE_MID, YELLOW_LIGHT, ORANGE_SHADOW),
        (DUSK_ROSE, DUSK_PEACH, DUSK_LILAC),
        (TEAL_MID, TEAL_LIGHT, TEAL_SHADOW)
    ]
    bx = 68
    b_idx = 0
    while bx < 240:
        bw = 7 + (b_idx % 5)
        bh = 48 + ((b_idx * 7) % 24) # uneven heights!
        by = 240 - bh
        col_m, col_l, col_d = shelf_palette[b_idx % len(shelf_palette)]
        c.rect(bx, by, bw, bh, col_m, outline=OUTLINE)
        c.line(bx + 1, by + 1, bx + 1, by + bh - 2, col_l)
        c.line(bx + bw - 2, by + 1, bx + bw - 2, by + bh - 2, col_d)
        # Gold embossed title stripes
        if bh > 55:
            c.line(bx + 2, by + 12, bx + bw - 3, by + 12, YELLOW_LIGHT)
            c.line(bx + 2, by + 15, bx + bw - 3, by + 15, YELLOW_LIGHT)
        # Bookmark ribbon hanging down
        if b_idx == 5:
            c.line(bx + 3, 240, bx + 3, 248, RED_LIGHT)
        bx += bw + 2
        b_idx += 1

    # Shelf 3: Model clipper sailboat on stand + books
    # Sailboat hull (x=75..135, y=302..318)
    c.polygon([(75, 304), (135, 304), (125, 318), (85, 318)], fill=BROWN_MID, outline=BROWN_DARKEST)
    c.line(75, 304, 135, 304, WOOD_HIGHLIGHT)
    # Mast & white triangular sails
    c.line(105, 255, 105, 304, WOOD_HIGHLIGHT)
    c.polygon([(105, 258), (128, 298), (105, 298)], fill=PURE_WHITE, outline=WHITE_SHADOW)
    c.polygon([(103, 265), (82, 300), (103, 300)], fill=WHITE_MID, outline=WHITE_SHADOW)
    # Books on right side of Shelf 3
    bx = 145
    while bx < 240:
        bw = 8 + (b_idx % 4)
        bh = 52 + ((b_idx * 5) % 18)
        by = 320 - bh
        col_m, col_l, col_d = shelf_palette[(b_idx + 2) % len(shelf_palette)]
        c.rect(bx, by, bw, bh, col_m, outline=OUTLINE)
        c.line(bx + 1, by + 1, bx + 1, by + bh - 2, col_l)
        bx += bw + 2
        b_idx += 1

    # Shelf 4: Heavy art binders with label inserts
    bx = 68
    while bx < 242:
        bw = 14 + (b_idx % 6)
        bh = 62 - (b_idx % 6)
        by = 394 - bh
        col_m, col_l, col_d = shelf_palette[(b_idx + 4) % len(shelf_palette)]
        c.rect(bx, by, bw, bh, col_m, outline=OUTLINE)
        c.line(bx + 1, by + 1, bx + 1, by + bh - 2, col_l)
        # Spine label box
        c.rect(bx + 2, by + 18, bw - 4, 14, WHITE_SHADOW, outline=OUTLINE)
        c.line(bx + 4, by + 25, bx + bw - 6, by + 25, OUTLINE)
        bx += bw + 3
        b_idx += 1

    # -------------------------------------------------------------------------
    # 2. GLOBE ON STAND (x=275..335, y=290..400)
    # -------------------------------------------------------------------------
    # Mahogany tripod legs touching floor at y=400
    c.line(305, 360, 280, 400, BROWN_MID)
    c.line(305, 360, 330, 400, BROWN_MID)
    c.line(305, 360, 305, 400, BROWN_DARK)
    c.circle(305, 355, 4, WOOD_HIGHLIGHT, outline=BROWN_DARKEST)
    # Brass meridian ring (radius 22, tilted)
    c.circle(305, 320, 23, YELLOW_MID, outline=YELLOW_SHADOW)
    # Globe sphere (radius 18)
    c.circle(305, 320, 18, BLUE_MID, outline=OUTLINE)
    # Continents
    c.circle(300, 314, 8, GREEN_MID)
    c.circle(310, 324, 7, GREEN_MID)
    c.set_pixel(298, 312, WOOD_HIGHLIGHT)
    c.set_pixel(312, 322, WOOD_HIGHLIGHT)
    # Glass shine on globe
    c.line(294, 308, 298, 304, PURE_WHITE)

    # -------------------------------------------------------------------------
    # 3. GUITAR ON STAND (x=350..415, y=250..400)
    # -------------------------------------------------------------------------
    # Black tubular steel tripod stand
    c.line(382, 340, 356, 400, METAL_SHADOW)
    c.line(382, 340, 408, 400, METAL_SHADOW)
    c.line(382, 340, 382, 400, VOID_BLACK)
    c.rect(374, 348, 16, 4, METAL_MID) # cradle
    # Acoustic Guitar Body (lower bout & upper bout)
    # Lower bout (radius 20, center 382, 355)
    c.circle(382, 355, 20, BROWN_DARKEST, outline=OUTLINE)
    c.circle(382, 355, 17, ORANGE_MID)
    c.circle(382, 355, 12, WOOD_HIGHLIGHT)
    # Upper bout (radius 15, center 382, 325)
    c.circle(382, 325, 15, BROWN_DARKEST, outline=OUTLINE)
    c.circle(382, 325, 12, ORANGE_MID)
    c.circle(382, 325, 8, WOOD_HIGHLIGHT)
    # Soundhole & bridge
    c.circle(382, 332, 6, VOID_BLACK, outline=YELLOW_MID)
    c.rect(374, 358, 16, 4, WOOD_BLACK)
    # Fretboard & Headstock
    c.rect(379, 258, 6, 68, BROWN_DARKEST, outline=OUTLINE)
    for fty in range(262, 324, 6):
        c.line(379, fty, 384, fty, METAL_MID) # frets
    # Headstock with 6 tuning pegs
    c.rect(377, 248, 10, 12, BROWN_MID, outline=BROWN_DARKEST)
    c.set_pixel(375, 250, PURE_WHITE)
    c.set_pixel(375, 254, PURE_WHITE)
    c.set_pixel(375, 258, PURE_WHITE)
    c.set_pixel(388, 250, PURE_WHITE)
    c.set_pixel(388, 254, PURE_WHITE)
    c.set_pixel(388, 258, PURE_WHITE)

    # -------------------------------------------------------------------------
    # 4. DESK WITH GLOWING MONITOR (x=430..620, y=200..400)
    # -------------------------------------------------------------------------
    # Wooden study desk surface at y=290
    c.rect(430, 288, 180, 12, BROWN_MID, outline=BROWN_DARKEST)
    c.line(430, 288, 609, 288, WOOD_HIGHLIGHT)
    c.line(430, 289, 609, 289, BROWN_LIGHT)
    # Left desk legs
    c.rect(434, 300, 10, 100, BROWN_MID, outline=BROWN_DARKEST)
    c.line(434, 300, 434, 399, WOOD_HIGHLIGHT)
    # Right pedestal with 3 drawers (x=550..610, y=300..400)
    c.rect(550, 300, 60, 98, BROWN_DARK, outline=BROWN_DARKEST)
    for dy in [304, 334, 364]:
        c.rect(554, dy, 52, 26, BROWN_MID, outline=BROWN_DARKEST)
        c.line(554, dy, 605, dy, WOOD_HIGHLIGHT)
        # Brass handle
        c.rect(576, dy + 11, 8, 4, YELLOW_MID, outline=YELLOW_SHADOW)
        c.set_pixel(577, dy + 11, PURE_WHITE)

    # Accessories on desk:
    # Pencil cup with colorful pens (x=442, y=265..288)
    c.rect(442, 270, 14, 18, RED_MID, outline=OUTLINE)
    c.line(444, 258, 444, 270, YELLOW_MID)
    c.line(447, 256, 447, 270, BLUE_MID)
    c.line(450, 260, 450, 270, GREEN_MID)
    c.line(453, 257, 453, 270, ORANGE_MID)
    # Open notebook with scribbled diagrams (x=462..500, y=282..288)
    c.rect(462, 284, 34, 4, PURE_WHITE, outline=WHITE_SHADOW)

    # Glowing Computer Monitor (x=500..574, y=210..288)
    # Stand & base
    c.rect(532, 274, 10, 14, METAL_SHADOW)
    c.rect(524, 285, 26, 3, METAL_MID, outline=OUTLINE)
    # Monitor bezel
    c.rect(500, 210, 74, 64, VOID_BLACK, outline=METAL_MID)
    c.line(500, 210, 573, 210, METAL_MID)
    # Power LED
    c.set_pixel(570, 271, GREEN_MID)

    # Glowing Game Screen on monitor (x=505..569, y=215..267)
    # Displays Younger Sibling Simulator in-game scene!
    c.rect(505, 215, 65, 36, BLUE_LIGHT) # sky
    c.rect(505, 251, 65, 17, BROWN_MID) # floor
    c.line(505, 251, 569, 251, GREEN_LIGHT) # grass/platform lip
    # Tiny running P1 character sprite on monitor
    c.circle(532, 240, 3, SKIN_LIGHT) # head
    c.rect(530, 244, 5, 5, RED_MID) # hoodie
    c.line(529, 249, 527, 252, BLUE_MID) # running legs
    c.line(533, 249, 536, 251, BLUE_MID)
    # Golden star coin
    c.circle(552, 238, 3, YELLOW_MID, outline=YELLOW_LIGHT)

    # Ambient Monitor Screen Glow casting cyan/blue light on desk
    for gy in range(288, 305):
        for gx in range(480, 590):
            if (gx + gy) % 3 == 0:
                c.set_pixel(gx, gy, TEAL_LIGHT)

    # -------------------------------------------------------------------------
    # 5. BED WITH RUMPLED BLANKETS AND PLUSH TOYS (x=640..940, y=160..400)
    # -------------------------------------------------------------------------
    # Tall Carved Wooden Headboard at Left (x=640..675, y=160..400)
    # Turned finial sphere at top
    c.circle(650, 166, 8, WOOD_HIGHLIGHT, outline=BROWN_DARKEST)
    c.set_pixel(648, 164, PURE_WHITE)
    # Headboard Post
    c.rect(644, 174, 14, 224, BROWN_MID, outline=BROWN_DARKEST)
    c.line(644, 174, 644, 397, WOOD_HIGHLIGHT)
    c.line(645, 174, 645, 397, BROWN_LIGHT)
    # Carved Panels of Headboard
    c.rect(658, 190, 42, 110, BROWN_DARK, outline=BROWN_DARKEST)
    c.rect(664, 200, 30, 90, BROWN_MID, outline=BROWN_DARKEST)

    # Footboard Post at Right (x=926..938, y=260..400)
    c.circle(932, 260, 6, WOOD_HIGHLIGHT, outline=BROWN_DARKEST)
    c.rect(927, 266, 12, 132, BROWN_MID, outline=BROWN_DARKEST)
    c.line(927, 266, 927, 397, WOOD_HIGHLIGHT)

    # Bed Side Rail connecting posts
    c.rect(658, 355, 270, 22, BROWN_MID, outline=BROWN_DARKEST)
    c.line(658, 355, 927, 355, WOOD_HIGHLIGHT)
    c.line(658, 356, 927, 356, BROWN_LIGHT)
    # Floor contact shadow under bed
    c.line(640, 400, 940, 400, SHADOW_PURPLE_DEEP)

    # Layered Fluffy Pillows (x=670..745, y=240..290)
    # Pillow 1 (back)
    c.circle(700, 258, 18, WHITE_SHADOW)
    c.circle(700, 256, 16, PURE_WHITE)
    # Pillow 2 (front, plump with indentation)
    c.circle(720, 272, 16, WHITE_SHADOW)
    c.circle(720, 270, 14, PURE_WHITE)
    c.line(714, 268, 726, 268, WHITE_SHADOW) # indent

    # Cozy Quilted Blue Bedspread with Rumpled Cloth Folds (x=705..926, y=270..375)
    # White turned-down sheet lining near pillow
    c.rect(705, 276, 36, 12, PURE_WHITE, outline=OUTLINE)
    c.line(705, 287, 740, 287, WHITE_SHADOW)
    # Blue blanket base
    c.rect(705, 288, 222, 75, BLUE_MID, outline=OUTLINE)

    # Quilted Diamond Stitch Pattern in BLUE_LIGHT
    for by in range(288, 362):
        for bx in range(740, 925):
            if (bx + by) % 16 == 0 or (bx - by) % 16 == 0:
                c.set_pixel(bx, by, BLUE_LIGHT)
            if (bx + by) % 16 == 0 and (bx - by) % 16 == 0:
                c.set_pixel(bx, by, BLUE_SHADOW)

    # Dynamic Rumpled Blanket Folds cascading rhythmically
    for fx in [755, 795, 840, 885]:
        c.line(fx - 2, 288, fx + 12, 362, BLUE_LIGHT)
        c.line(fx - 1, 288, fx + 13, 362, BLUE_SHADOW)
        c.line(fx, 288, fx + 14, 362, OUTLINE)

    # Blanket Skirt Drape overlapping the bed rail with organic ripples
    for sx in range(705, 927):
        wave = int(math.sin((sx - 705) * 0.18) * 4)
        c.line(sx, 362, sx, 368 + wave, BLUE_MID)
        c.set_pixel(sx, 368 + wave, OUTLINE)
        c.set_pixel(sx, 367 + wave, BLUE_SHADOW)

    # Plush Toys Nestled on Bed:
    # 1. Cute Plush Penguin (x=750..776, y=262..295)
    c.circle(762, 282, 11, VOID_BLACK, outline=OUTLINE) # body
    c.circle(762, 283, 8, PURE_WHITE) # tummy
    c.circle(762, 268, 7, VOID_BLACK, outline=OUTLINE) # head
    c.set_pixel(760, 267, PURE_WHITE) # eyes
    c.set_pixel(764, 267, PURE_WHITE)
    c.circle(762, 271, 3, YELLOW_MID) # orange beak
    c.set_pixel(762, 271, ORANGE_MID)
    # 2. Floppy-eared Rabbit Plushie (x=790..820, y=265..295)
    c.circle(805, 284, 9, DUSK_CREAM, outline=OUTLINE)
    c.circle(805, 272, 7, DUSK_CREAM, outline=OUTLINE)
    c.circle(805, 272, 2, DUSK_PINK) # nose
    # Floppy ears dangling to sides
    c.line(800, 266, 792, 276, DUSK_PINK)
    c.line(801, 266, 793, 276, DUSK_CREAM)
    c.line(810, 266, 818, 276, DUSK_PINK)
    c.line(809, 266, 817, 276, DUSK_CREAM)
    # 3. Smiling Star Pillow (x=835..865, y=272..296)
    c.circle(850, 284, 10, YELLOW_MID, outline=YELLOW_SHADOW)
    c.set_pixel(847, 282, OUTLINE) # smile face
    c.set_pixel(853, 282, OUTLINE)
    c.line(848, 286, 852, 286, OUTLINE)

    # -------------------------------------------------------------------------
    # 6. BEANBAG (x=960..1060, y=290..400)
    # -------------------------------------------------------------------------
    # Generous plush beanbag chair in cozy teal
    # Main round slouch body (width 100, height 95)
    c.circle(1010, 350, 44, TEAL_MID, outline=OUTLINE)
    c.circle(1005, 342, 38, TEAL_LIGHT)
    # Sunken seat crease where someone was sitting
    for cy in range(320, 345):
        cx = int(1010 + math.sin((cy - 320) * 0.25) * 8)
        c.line(cx - 16, cy, cx + 16, cy, TEAL_SHADOW)
        c.set_pixel(cx - 17, cy, OUTLINE)
    # Fabric seam lines
    c.line(976, 335, 1010, 392, TEAL_SHADOW)
    c.line(1044, 335, 1010, 392, TEAL_SHADOW)
    # Handheld game console resting on beanbag cushion
    c.rect(1000, 326, 22, 12, PURPLE_MID, outline=OUTLINE)
    c.rect(1005, 328, 12, 8, BLUE_LIGHT)
    c.set_pixel(1002, 331, YELLOW_LIGHT) # d-pad
    c.set_pixel(1019, 331, RED_LIGHT) # button
    # Floor contact shadow
    c.line(970, 398, 1050, 398, SHADOW_PURPLE_DEEP)

    # -------------------------------------------------------------------------
    # 7. TOY CHEST SPILLING TOYS (x=1080..1230, y=240..400)
    # -------------------------------------------------------------------------
    # Wooden chest main body (x=1090..1220, y=290..396)
    c.rect(1090, 290, 130, 104, BROWN_MID, outline=BROWN_DARKEST)
    # Vertical oak plank divisions
    for px in [1122, 1155, 1188]:
        c.line(px, 291, px, 393, BROWN_DARK)
        c.line(px + 1, 291, px + 1, 393, BROWN_DARKEST)
    # Brass reinforced corner brackets with rivets
    for bx, by in [(1090, 290), (1210, 290), (1090, 384), (1210, 384)]:
        c.rect(bx, by, 10, 10, YELLOW_MID, outline=YELLOW_SHADOW)
        c.set_pixel(bx + 3, by + 3, PURE_WHITE)
    # Chest base feet
    c.rect(1096, 394, 20, 6, BROWN_DARK, outline=BROWN_DARKEST)
    c.rect(1194, 394, 20, 6, BROWN_DARK, outline=BROWN_DARKEST)
    c.line(1086, 400, 1224, 400, SHADOW_PURPLE_DEEP)

    # Propped-Open Wooden Chest Lid (angled ajar, y=250..290)
    c.polygon([(1086, 280), (1224, 260), (1224, 272), (1086, 292)], fill=BROWN_MID, outline=BROWN_DARKEST)
    c.line(1086, 280, 1224, 260, WOOD_HIGHLIGHT)
    c.line(1086, 281, 1224, 261, BROWN_LIGHT)
    # Interior dark void of open chest
    c.rect(1092, 280, 126, 12, VOID_BLACK)

    # Cute Toy Dinosaur Peeking Out (x=1165..1205, y=242..288)
    c.circle(1185, 258, 12, GREEN_MID, outline=OUTLINE)
    c.circle(1185, 256, 10, GREEN_MID)
    c.line(1178, 248, 1190, 248, GREEN_LIGHT)
    # Snout
    c.rect(1192, 254, 10, 10, GREEN_MID, outline=OUTLINE)
    c.line(1193, 254, 1200, 254, GREEN_LIGHT)
    c.line(1192, 262, 1200, 262, OUTLINE) # smiling mouth
    c.set_pixel(1196, 261, PURE_WHITE) # cute tooth!
    # Big expressive eye
    c.circle(1182, 254, 4, PURE_WHITE, outline=OUTLINE)
    c.set_pixel(1183, 254, OUTLINE)
    c.set_pixel(1182, 253, PURE_WHITE)
    # Dinosaur paws over chest rim
    c.rect(1174, 284, 8, 6, GREEN_MID, outline=OUTLINE)
    c.rect(1194, 284, 8, 6, GREEN_MID, outline=OUTLINE)

    # Toys Spilling Out over chest lip and onto floor:
    # 1. Colorful building blocks tumbling
    c.rect(1120, 286, 12, 12, RED_MID, outline=OUTLINE)
    c.line(1121, 287, 1130, 287, RED_LIGHT)
    c.rect(1105, 305, 14, 14, YELLOW_MID, outline=OUTLINE)
    c.line(1106, 306, 1117, 306, YELLOW_LIGHT)
    c.rect(1135, 310, 12, 12, BLUE_MID, outline=OUTLINE)
    # 2. Block on floor (x=1075, y=388)
    c.rect(1072, 386, 14, 14, GREEN_MID, outline=OUTLINE)
    c.line(1073, 387, 1084, 387, GREEN_LIGHT)
    # 3. Red toy race car on floor (x=1215..1245, y=382..400)
    c.rect(1218, 386, 26, 10, RED_MID, outline=OUTLINE)
    c.line(1219, 387, 1242, 387, RED_LIGHT)
    c.rect(1224, 382, 12, 6, RED_MID, outline=OUTLINE) # cockpit
    c.circle(1222, 396, 4, VOID_BLACK, outline=OUTLINE) # wheels
    c.circle(1238, 396, 4, VOID_BLACK, outline=OUTLINE)
    c.set_pixel(1222, 396, WHITE_MID)
    c.set_pixel(1238, 396, WHITE_MID)
    # 4. Yo-yo with dangling string
    c.circle(1150, 335, 8, ORANGE_MID, outline=OUTLINE)
    c.circle(1150, 335, 5, YELLOW_MID)
    c.line(1150, 330, 1158, 305, WHITE_SHADOW) # string

    # Padlock on chest
    c.rect(1150, 305, 12, 14, YELLOW_MID, outline=YELLOW_SHADOW)
    c.rect(1154, 312, 3, 5, OUTLINE)

    return c


def generate_bg_near() -> PixelCanvas:
    """
    960x540 px: Foreground silhouettes layer.
    - STRICT: Transparent above floor line y=400 (y=0..399 is 100% transparent!).
    - Dark silhouetted foreground toys sitting on floor (y=400..540):
      1. Fluffy teddy bear (x=40..150, y=410..530)
      2. Wooden toy train (locomotive, tender, caboose) (x=170..380, y=415..530)
      3. Stacked block towers (x=400..510, y=402..530)
      4. Rocking horse (x=530..680, y=405..530)
      5. Soccer ball (x=700..770, y=440..525)
      6. Stuffed giraffe (x=790..920, y=402..530)
    - Crisp 1px warm rim light (WOOD_LIT) on upper-left edges.
    """
    c = PixelCanvas(960, 540, TRANSPARENT)

    # Rim light color: warm gold/peach rim light from palette
    RIM = WOOD_LIT
    BODY = SHADOW_PURPLE_DARK

    # -------------------------------------------------------------------------
    # 1. Fluffy Teddy Bear Silhouette (x=40..150, y=410..530)
    # -------------------------------------------------------------------------
    bx, by = 95, 470
    # Torso
    c.circle(bx, by + 12, 34, BODY)
    # Head
    c.circle(bx, by - 24, 26, BODY)
    # Ears
    c.circle(bx - 22, by - 44, 12, BODY)
    c.circle(bx + 22, by - 44, 12, BODY)
    # Muzzle
    c.circle(bx - 2, by - 16, 12, BODY)
    # Arms
    c.circle(bx - 32, by + 8, 16, BODY)
    c.circle(bx + 32, by + 8, 16, BODY)
    # Feet / Paws
    c.circle(bx - 28, by + 38, 18, BODY)
    c.circle(bx + 28, by + 38, 18, BODY)

    # 1px Upper-Left Warm Rim Light
    c.line(bx - 32, by - 48, bx - 18, by - 54, RIM) # left ear rim
    c.line(bx - 34, by - 46, bx - 34, by - 40, RIM)
    c.line(bx - 16, by - 48, bx + 8, by - 50, RIM)  # head crown
    c.line(bx + 14, by - 54, bx + 26, by - 54, RIM) # right ear top
    c.line(bx - 12, by - 22, bx - 8, by - 28, RIM)  # muzzle cheek
    c.line(bx - 46, by, bx - 46, by + 10, RIM)      # left arm
    c.line(bx - 44, by - 4, bx - 34, by - 8, RIM)
    c.line(bx - 44, by + 32, bx - 22, by + 22, RIM) # left foot
    c.line(bx + 12, by + 24, bx + 32, by + 24, RIM) # right foot

    # -------------------------------------------------------------------------
    # 2. Wooden Toy Train with Tender & Caboose (x=170..380, y=415..530)
    # -------------------------------------------------------------------------
    # Locomotive (x=170..280)
    # Cowcatcher at front (x=170..190, y=490..520)
    for cx in range(170, 191):
        c.line(cx, 490 + (190 - cx), cx, 520, BODY)
    c.line(170, 510, 190, 490, RIM) # cowcatcher rim
    # Boiler cylinder body
    c.rect(190, 450, 60, 54, BODY)
    c.line(190, 450, 250, 450, RIM) # top boiler rim
    # Smokestack with flared rim
    c.rect(202, 420, 14, 30, BODY)
    c.line(198, 418, 220, 418, BODY)
    c.line(198, 418, 220, 418, RIM)
    c.line(202, 420, 202, 448, RIM)
    # Steam dome
    c.circle(234, 442, 8, BODY)
    c.line(228, 436, 236, 436, RIM)
    # Cab with pitched roof
    c.rect(250, 420, 36, 84, BODY)
    c.rect(246, 418, 44, 6, BODY)
    c.line(246, 418, 290, 418, RIM) # cab roof rim
    c.line(246, 424, 246, 450, RIM) # cab left rim
    # Cab window cutout
    c.rect(258, 434, 18, 22, TRANSPARENT)
    c.line(258, 434, 276, 434, RIM)
    # Wheels
    c.circle(196, 514, 10, BODY, outline=OUTLINE) # front wheel
    c.line(188, 508, 196, 504, RIM)
    c.circle(230, 510, 16, BODY, outline=OUTLINE) # big driver 1
    c.line(216, 500, 230, 494, RIM)
    c.circle(268, 510, 16, BODY, outline=OUTLINE) # big driver 2
    c.line(254, 500, 268, 494, RIM)
    # Drive rod
    c.line(230, 514, 268, 514, BODY)
    c.line(230, 512, 268, 512, RIM)

    # Coal Tender Car (x=290..340, y=450..524)
    c.rect(294, 456, 44, 48, BODY)
    c.line(294, 456, 338, 456, RIM)
    c.line(294, 457, 294, 480, RIM)
    # Bumpy coal pile
    for cx in range(296, 336):
        cy = int(450 + math.sin((cx - 296) * 0.4) * 5)
        c.line(cx, cy, cx, 456, BODY)
        if (cx - 296) % 6 == 0:
            c.set_pixel(cx, cy, RIM)
    # Tender wheels
    c.circle(304, 514, 10, BODY, outline=OUTLINE)
    c.line(296, 508, 304, 504, RIM)
    c.circle(328, 514, 10, BODY, outline=OUTLINE)
    c.line(320, 508, 328, 504, RIM)

    # Caboose / Passenger Car (x=345..385, y=435..524)
    c.rect(348, 445, 36, 58, BODY)
    c.rect(344, 443, 44, 4, BODY)
    c.line(344, 443, 388, 443, RIM) # roof rim
    c.line(344, 444, 344, 470, RIM)
    # Cupola roof observation
    c.rect(356, 432, 20, 12, BODY)
    c.line(356, 432, 376, 432, RIM)
    c.circle(358, 514, 10, BODY, outline=OUTLINE)
    c.circle(378, 514, 10, BODY, outline=OUTLINE)

    # -------------------------------------------------------------------------
    # 3. Stacked Block Towers (x=400..510, y=402..530)
    # -------------------------------------------------------------------------
    # Tower 1 (Tall 4-block tower with spire roof, x=405..455)
    # Base block (44x32)
    c.rect(408, 492, 44, 32, BODY, outline=OUTLINE)
    c.line(408, 492, 451, 492, RIM)
    c.line(408, 492, 408, 523, RIM)
    # Block 2 (36x28)
    c.rect(412, 464, 36, 28, BODY, outline=OUTLINE)
    c.line(412, 464, 447, 464, RIM)
    c.line(412, 464, 412, 491, RIM)
    # Block 3 (28x26)
    c.rect(416, 438, 28, 26, BODY, outline=OUTLINE)
    c.line(416, 438, 443, 438, RIM)
    c.line(416, 438, 416, 463, RIM)
    # Pyramid Roof on Top (y=404..438)
    for py in range(404, 438):
        pw = int((py - 404) * 0.42)
        c.line(430 - pw, py, 430 + pw, py, BODY)
    c.line(430, 404, 416, 438, RIM) # left slope rim

    # Tower 2 (Castle battlements tower, x=460..510)
    c.rect(464, 485, 42, 38, BODY, outline=OUTLINE)
    c.line(464, 485, 505, 485, RIM)
    c.line(464, 485, 464, 522, RIM)
    # Archway cutout in base block
    c.circle(485, 510, 10, TRANSPARENT)
    c.rect(475, 510, 20, 14, TRANSPARENT)
    # Upper block with battlements
    c.rect(468, 445, 34, 40, BODY, outline=OUTLINE)
    c.line(468, 445, 501, 445, RIM)
    c.line(468, 445, 468, 484, RIM)
    # Castle crenellations
    c.rect(468, 435, 8, 10, BODY)
    c.line(468, 435, 476, 435, RIM)
    c.rect(481, 435, 8, 10, BODY)
    c.line(481, 435, 489, 435, RIM)
    c.rect(494, 435, 8, 10, BODY)
    c.line(494, 435, 502, 435, RIM)

    # -------------------------------------------------------------------------
    # 4. Rocking Horse Silhouette (x=530..680, y=405..530)
    # -------------------------------------------------------------------------
    hx, hy = 605, 465
    # Curved Rockers at bottom (x=535..675)
    for rx in range(535, 676):
        ry = int(518 + ((rx - hx) / 44.0) ** 2)
        if ry < 532:
            c.set_pixel(rx, ry, BODY)
            c.set_pixel(rx, ry + 1, BODY)
            c.set_pixel(rx, ry + 2, OUTLINE)
            c.set_pixel(rx, ry - 1, RIM) # rocker rim
    # Rocker tips
    c.circle(536, 500, 4, BODY)
    c.set_pixel(535, 498, RIM)
    c.circle(674, 500, 4, BODY)
    c.set_pixel(673, 498, RIM)

    # Four Sturdy Angled Legs
    c.line(hx - 32, hy + 4, hx - 56, 514, BODY)
    c.line(hx - 31, hy + 4, hx - 55, 514, BODY)
    c.line(hx - 33, hy + 4, hx - 57, 514, RIM)
    c.line(hx - 20, hy + 4, hx - 40, 516, BODY)
    c.line(hx - 21, hy + 4, hx - 41, 516, RIM)
    c.line(hx + 28, hy + 4, hx + 56, 516, BODY)
    c.line(hx + 29, hy + 4, hx + 57, 516, BODY)
    c.line(hx + 27, hy + 4, hx + 55, 516, RIM)
    c.line(hx + 38, hy + 4, hx + 70, 514, BODY)
    c.line(hx + 37, hy + 4, hx + 69, 514, RIM)

    # Horse Body Torso & Saddle
    c.circle(hx - 12, hy - 8, 24, BODY)
    c.circle(hx + 12, hy - 8, 24, BODY)
    c.rect(hx - 16, hy - 28, 32, 36, BODY)
    c.line(hx - 16, hy - 32, hx + 10, hy - 32, RIM) # saddle rim

    # Sculpted Horse Neck & Head
    for ny in range(hy - 56, hy - 16):
        prog = (ny - (hy - 56)) / 40.0
        nx = int(hx + 48 - prog * 32)
        c.line(nx - 8, ny, nx + 12, ny, BODY)
        c.set_pixel(nx - 9, ny, RIM) # neck rim
    # Head
    c.circle(hx + 48, hy - 48, 14, BODY)
    c.rect(hx + 48, hy - 50, 20, 12, BODY)
    c.circle(hx + 66, hy - 44, 6, BODY) # muzzle
    c.line(hx + 44, hy - 58, hx + 68, hy - 50, RIM) # head top rim
    # Ears
    c.line(hx + 42, hy - 64, hx + 46, hy - 54, RIM)
    c.line(hx + 48, hy - 62, hx + 50, hy - 54, BODY)
    # Handlebar
    c.rect(hx + 30, hy - 38, 12, 6, BODY)
    c.circle(hx + 42, hy - 36, 4, BODY)
    c.set_pixel(hx + 42, hy - 38, RIM)

    # -------------------------------------------------------------------------
    # 5. Soccer Ball Silhouette (x=700..770, y=440..525)
    # -------------------------------------------------------------------------
    sx, sy = 735, 482
    c.circle(sx, sy, 32, BODY, outline=OUTLINE)
    # Upper-left rim light arc
    for deg in range(120, 240):
        rad = math.radians(deg)
        c.set_pixel(int(sx + math.cos(rad) * 32), int(sy + math.sin(rad) * 32), RIM)
    # Pentagonal patch seams in darker purple
    c.polygon([(sx, sy - 14), (sx + 13, sy - 4), (sx + 8, sy + 12), (sx - 8, sy + 12), (sx - 13, sy - 4)], fill=OUTLINE)
    c.line(sx, sy - 14, sx, sy - 28, OUTLINE)
    c.line(sx + 13, sy - 4, sx + 26, sy - 8, OUTLINE)
    c.line(sx + 8, sy + 12, sx + 18, sy + 24, OUTLINE)
    c.line(sx - 8, sy + 12, sx - 18, sy + 24, OUTLINE)
    c.line(sx - 13, sy - 4, sx - 26, sy - 8, OUTLINE)

    # -------------------------------------------------------------------------
    # 6. Stuffed Giraffe Silhouette (x=790..920, y=402..530)
    # -------------------------------------------------------------------------
    gx, gy = 850, 480
    # Plump torso
    c.circle(gx, gy, 28, BODY)
    # Four knobby legs with little hooves
    c.rect(gx - 22, gy + 16, 8, 32, BODY)
    c.line(gx - 22, gy + 16, gx - 22, gy + 47, RIM)
    c.rect(gx - 10, gy + 16, 8, 32, BODY)
    c.line(gx - 10, gy + 16, gx - 10, gy + 47, RIM)
    c.rect(gx + 10, gy + 16, 8, 32, BODY)
    c.line(gx + 10, gy + 16, gx + 10, gy + 47, RIM)
    c.rect(gx + 22, gy + 16, 8, 32, BODY)
    c.line(gx + 22, gy + 16, gx + 22, gy + 47, RIM)

    # Long Graceful Neck (rising from gx - 16 to gx - 26, y=404..460)
    for ny in range(418, 470):
        nx = int(gx - 18 - (470 - ny) * 0.15)
        c.line(nx - 7, ny, nx + 7, ny, BODY)
        c.set_pixel(nx - 8, ny, RIM) # neck rim
        # Giraffe mane tufts down back of neck
        if ny % 6 == 0:
            c.set_pixel(nx + 8, ny, RIM)
    # Head & gentle muzzle
    c.circle(gx - 26, 414, 10, BODY)
    c.rect(gx - 38, 412, 14, 10, BODY)
    c.circle(gx - 38, 417, 5, BODY) # snout
    c.line(gx - 42, 413, gx - 20, 407, RIM) # snout rim
    # Rounded Ossicones (giraffe horns with tufted knobs)
    c.line(gx - 28, 404, gx - 28, 408, RIM)
    c.circle(gx - 28, 404, 3, BODY)
    c.set_pixel(gx - 29, 403, RIM)
    c.line(gx - 22, 404, gx - 22, 408, BODY)
    c.circle(gx - 22, 404, 3, BODY)
    c.set_pixel(gx - 23, 403, RIM)
    # Cute pricked ear
    c.line(gx - 18, 410, gx - 12, 414, RIM)
    # Tufted tail
    c.line(gx + 26, gy - 4, gx + 38, gy + 16, BODY)
    c.circle(gx + 38, gy + 16, 4, BODY)
    c.set_pixel(gx + 38, gy + 14, RIM)

    # STRICT RULE: Clear everything above floor line y=400!
    for y in range(0, 400):
        for x in range(960):
            c.set_pixel(x, y, TRANSPARENT)

    return c


def generate_fg_legs() -> PixelCanvas:
    """
    960x540 px, transparent: Foreground silhouettes layer.
    - Scrolls faster than player plane.
    - Dark silhouettes of:
      * Table and chair legs on left (x=10..130, y=260..540)
      * Hanging power cable looping from ceiling down to floor (x=220..320, y=0..460)
      * Stool leg (x=560..600, y=420..540)
      * Bed-skirt fringe / ruffled fabric hanging across bottom right (x=640..960, y=450..540)
    """
    c = PixelCanvas(960, 540, TRANSPARENT)
    SIL = VOID_BLACK
    RIM = PURPLE_LIGHT

    # 1. Turned Dining/Desk Table Leg (x=20..80, y=260..540)
    # Table apron top edge
    c.rect(0, 260, 110, 24, SIL)
    c.line(0, 284, 110, 284, OUTLINE)
    c.line(0, 260, 110, 260, RIM)
    # Heavy turned wooden leg with ornate lathe curves
    for ly in range(284, 540):
        # Lathe profile curve
        if ly < 330:
            hw = 16 + int(math.sin((ly - 284) * 0.14) * 6)
        elif ly < 400:
            hw = 22 + int(math.sin((ly - 330) * 0.1) * 8) # large bulb
        elif ly < 480:
            hw = 14 + int(math.sin((ly - 400) * 0.12) * 5)
        else:
            hw = 20 + int(math.sin((ly - 480) * 0.08) * 8) # foot
        c.line(45 - hw, ly, 45 + hw, ly, SIL)
        c.set_pixel(45 - hw, ly, RIM)
        c.set_pixel(45 + hw, ly, OUTLINE)

    # 2. Angled Chair Leg (x=85..125, y=340..540)
    for ly in range(340, 540):
        lx = int(85 + (ly - 340) * 0.18)
        c.line(lx, ly, lx + 12, ly, SIL)
        c.set_pixel(lx, ly, RIM)
        c.set_pixel(lx + 12, ly, OUTLINE)

    # 3. Hanging Power Cable / Extension Cord (x=220..320, y=0..460)
    # Cable hanging from top ceiling at (240, 0), sagging in catenary curve down to y=220,
    # looping gracefully back up to (285, 140), then dangling down to floor plug at (305, 460)
    # Loop 1: (240, 0) to (275, 230)
    for y in range(0, 230):
        t = y / 230.0
        x = int(240 + math.sin(t * math.pi) * 35)
        c.circle(x, y, 2, SIL)
        c.set_pixel(x - 1, y, RIM)
    # Loop 2: upward coil and descent
    for y in range(140, 460):
        t = (y - 140) / 320.0
        x = int(275 + math.sin(t * math.pi * 1.5) * 22)
        c.circle(x, y, 2, SIL)
        c.set_pixel(x - 1, y, RIM)
    # 3-prong wall outlet plug at bottom
    c.rect(300, 454, 12, 18, SIL, outline=OUTLINE)
    c.set_pixel(300, 454, RIM)

    # 4. Front Stool / Chair Leg (x=560..600, y=420..540)
    for ly in range(420, 540):
        lx = int(570 + (ly - 420) * 0.12)
        c.line(lx, ly, lx + 14, ly, SIL)
        c.set_pixel(lx, ly, RIM)
        c.set_pixel(lx + 14, ly, OUTLINE)

    # 5. Bed-Skirt Fringe / Ruffled Fabric Hanging (x=640..960, y=450..540)
    # Horizontal fabric hem line
    c.rect(640, 450, 320, 90, TRANSPARENT)
    # Dangling scalloped cloth ruffles
    for rx in range(640, 960):
        # Cascading ruffle waves
        wave1 = int(math.sin((rx - 640) * 0.08) * 12)
        wave2 = int(math.sin((rx - 640) * 0.22) * 6)
        hem_y = 475 + wave1 + wave2
        c.line(rx, hem_y, rx, 540, SIL)
        c.set_pixel(rx, hem_y, RIM)
        # Hanging tassel threads every 16px
        if rx % 16 == 0:
            c.line(rx, hem_y, rx, min(539, hem_y + 18), RIM)
            c.circle(rx, min(539, hem_y + 18), 2, SIL)

    return c


def generate_fg_dust() -> PixelCanvas:
    """
    960x540 px, transparent: Foreground soft round dust bokeh.
    3 sizes with hard-banded discrete alpha steps:
    - Large bokeh (r=20..26, 6 orbs, 4 hard alpha bands: 30, 70, 120, 180)
    - Medium bokeh (r=9..14, 14 orbs, 3 hard alpha bands: 50, 110, 200)
    - Small bokeh (r=3..6, 25 orbs, 2 hard alpha bands: 90, 255)
    Strictly uses RGB from palette (DUSK_CREAM and YELLOW_LIGHT).
    """
    c = PixelCanvas(960, 540, TRANSPARENT)
    rgb_cream = DUSK_CREAM[:3] # (240, 197, 214)
    rgb_yellow = YELLOW_LIGHT[:3] # (253, 240, 126)

    # Large bokeh orbs (cx, cy, radius, rgb)
    large_orbs = [
        (120, 110, 24, rgb_cream),
        (280, 380, 26, rgb_yellow),
        (450, 140, 22, rgb_cream),
        (620, 420, 25, rgb_yellow),
        (780, 160, 24, rgb_cream),
        (910, 360, 22, rgb_yellow),
    ]
    for cx, cy, r, rgb in large_orbs:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if 0 <= x < 960 and 0 <= y < 540:
                    d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    if d <= r:
                        if d > r * 0.75:
                            a = 30
                        elif d > r * 0.50:
                            a = 70
                        elif d > r * 0.25:
                            a = 120
                        else:
                            a = 180
                        cur_a = c.get_pixel(x, y)[3]
                        if a > cur_a:
                            c.set_pixel(x, y, (rgb[0], rgb[1], rgb[2], a))

    # Medium bokeh orbs (cx, cy, radius, rgb)
    med_orbs = [
        (60, 240, 12, rgb_cream), (190, 180, 14, rgb_yellow),
        (240, 80, 10, rgb_cream), (350, 260, 13, rgb_yellow),
        (410, 480, 11, rgb_cream), (520, 290, 14, rgb_yellow),
        (580, 90, 12, rgb_cream), (670, 240, 13, rgb_yellow),
        (720, 490, 11, rgb_cream), (830, 280, 14, rgb_yellow),
        (880, 100, 12, rgb_cream), (150, 490, 10, rgb_yellow),
        (500, 40, 11, rgb_cream), (930, 480, 13, rgb_yellow),
    ]
    for cx, cy, r, rgb in med_orbs:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if 0 <= x < 960 and 0 <= y < 540:
                    d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    if d <= r:
                        if d > r * 0.65:
                            a = 50
                        elif d > r * 0.35:
                            a = 110
                        else:
                            a = 200
                        cur_a = c.get_pixel(x, y)[3]
                        if a > cur_a:
                            c.set_pixel(x, y, (rgb[0], rgb[1], rgb[2], a))

    # Small sharp motes (cx, cy, radius, rgb)
    small_orbs = [
        (35, 75, 4, rgb_yellow), (95, 340, 5, rgb_cream), (160, 60, 3, rgb_yellow),
        (215, 290, 4, rgb_cream), (265, 440, 5, rgb_yellow), (310, 150, 4, rgb_cream),
        (380, 80, 3, rgb_yellow), (440, 350, 5, rgb_cream), (480, 210, 4, rgb_yellow),
        (540, 440, 5, rgb_cream), (595, 180, 4, rgb_yellow), (645, 320, 5, rgb_cream),
        (705, 110, 3, rgb_yellow), (750, 390, 4, rgb_cream), (810, 50, 5, rgb_yellow),
        (855, 210, 4, rgb_cream), (900, 430, 5, rgb_yellow), (945, 190, 3, rgb_cream),
        (130, 220, 4, rgb_yellow), (390, 410, 4, rgb_cream), (630, 30, 5, rgb_yellow),
        (760, 280, 4, rgb_cream), (840, 490, 3, rgb_yellow), (480, 510, 4, rgb_cream),
        (20, 450, 5, rgb_yellow),
    ]
    for cx, cy, r, rgb in small_orbs:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if 0 <= x < 960 and 0 <= y < 540:
                    d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    if d <= r:
                        a = 90 if d > r * 0.5 else 255
                        cur_a = c.get_pixel(x, y)[3]
                        if a > cur_a:
                            c.set_pixel(x, y, (rgb[0], rgb[1], rgb[2], a))

    return c


# =============================================================================
# 2. AMBIENT ANIMATED BACKGROUND PROPS (13 PROPS)
# =============================================================================

def generate_prop_curtain() -> List[PixelCanvas]:
    """
    prop_curtain.png: 96x192, 8 frames, 6 fps, loop: true.
    Curtain swaying in window draft.
    Hanging from brass rod at top, cascading fabric folds with sinusoidal wave propagation.
    """
    frames = []
    for f in range(8):
        c = PixelCanvas(96, 192, TRANSPARENT)
        phase = f / 8.0 * 2.0 * math.pi

        # Brass curtain rod along top (y=6..14)
        c.rect(4, 8, 88, 4, YELLOW_MID, outline=YELLOW_SHADOW)
        c.line(4, 8, 91, 8, YELLOW_LIGHT)
        c.circle(4, 10, 4, YELLOW_LIGHT, outline=BROWN_DARKEST)
        c.circle(91, 10, 4, YELLOW_LIGHT, outline=BROWN_DARKEST)

        # Hanging rings
        for rx in [16, 30, 44, 58, 72, 84]:
            c.circle(rx, 14, 3, YELLOW_MID, outline=YELLOW_SHADOW)

        # Curtain fabric billow
        # Base hanging area: x from 12 to 88, y from 16 to 184
        for y in range(16, 185):
            prog = (y - 16) / 168.0
            # Sinuous draft wave: amplitude increases toward bottom
            wave = math.sin(phase - prog * 3.5) * (prog * 9.0)

            # Left and right fabric edges
            left_x = int(14 + wave * 0.6)
            right_x = int(86 + wave * 1.2)

            for x in range(left_x, right_x + 1):
                # Vertical fold ridges across curtain width
                fold = math.sin((x - left_x) * 0.28 + wave * 0.4)
                if fold > 0.6:
                    col = DUSK_PEACH # highlight crest
                elif fold > 0.0:
                    col = DUSK_ROSE  # midtone
                elif fold > -0.6:
                    col = DUSK_PINK  # shadow
                else:
                    col = SHADOW_PURPLE_MID # deep fold valley
                c.set_pixel(x, y, col)

            # Edge outlines
            c.set_pixel(left_x, y, OUTLINE)
            c.set_pixel(right_x, y, OUTLINE)

        # Bottom scalloped hem
        prog = 1.0
        wave = math.sin(phase - 3.5) * 9.0
        left_x = int(14 + wave * 0.6)
        right_x = int(86 + wave * 1.2)
        for x in range(left_x, right_x + 1):
            hem_drop = int(math.sin((x - left_x) * 0.3) * 3)
            c.set_pixel(x, 184 + hem_drop, OUTLINE)
            c.set_pixel(x, 183 + hem_drop, DUSK_PEACH)

        # Tie-back sash band at y=95 with golden tassel
        sash_x = int(left_x + (right_x - left_x) * 0.28)
        c.rect(sash_x - 4, 94, 18, 5, YELLOW_MID, outline=YELLOW_SHADOW)
        c.line(sash_x - 4, 94, sash_x + 13, 94, YELLOW_LIGHT)
        # Dangling tassel swinging
        tassel_sway = int(math.sin(phase) * 3)
        c.line(sash_x + 5, 99, sash_x + 5 + tassel_sway, 114, YELLOW_LIGHT)
        c.circle(sash_x + 5 + tassel_sway, 115, 3, YELLOW_MID, outline=YELLOW_SHADOW)

        frames.append(c)
    return frames


def generate_prop_fan() -> List[PixelCanvas]:
    """
    prop_fan.png: 128x64, 8 frames, 12 fps, loop: true.
    Ceiling fan rotating with slight wobble and swinging pull chain.
    """
    frames = []
    for f in range(8):
        c = PixelCanvas(128, 64, TRANSPARENT)
        phase = f / 8.0 * 2.0 * math.pi
        wobble = int(math.sin(phase) * 1.2)

        # Ceiling mount cup at top (x=64, y=0..6)
        c.rect(58, 0, 12, 6, BROWN_MID, outline=BROWN_DARKEST)
        c.line(58, 0, 69, 0, WOOD_HIGHLIGHT)
        # Brass downrod
        c.line(64, 6, 64, 18 + wobble, YELLOW_MID)
        c.line(63, 6, 63, 18 + wobble, YELLOW_LIGHT)

        # Central motor housing (cx=64, cy=22 + wobble)
        mcy = 22 + wobble
        mcx = 64

        # 4 Blades rotating in perspective (squashed ellipse: rx=48, ry=14)
        # Blade angles
        blade_data = []
        for b in range(4):
            b_angle = phase + b * (math.pi / 2.0)
            # Tip coordinate
            tx = mcx + math.cos(b_angle) * 48
            ty = mcy + math.sin(b_angle) * 14
            depth = math.sin(b_angle) # negative = behind motor, positive = in front
            blade_data.append((depth, b_angle, tx, ty))

        # Sort by depth so back blades draw before motor housing, front blades draw after
        blade_data.sort(key=lambda item: item[0])

        for depth, b_angle, tx, ty in blade_data:
            if depth < 0: # back blade
                # Blade polygon
                norm_angle = b_angle + math.pi / 2.0
                nx = math.cos(norm_angle) * 5
                ny = math.sin(norm_angle) * 2
                pts = [
                    (int(mcx - nx * 0.4), int(mcy - ny * 0.4)),
                    (int(tx - nx), int(ty - ny)),
                    (int(tx + nx), int(ty + ny)),
                    (int(mcx + nx * 0.4), int(mcy + ny * 0.4))
                ]
                c.polygon(pts, fill=BROWN_DARK, outline=BROWN_DARKEST)

        # Motor housing body
        c.rect(mcx - 14, mcy - 6, 28, 12, BROWN_MID, outline=BROWN_DARKEST)
        c.line(mcx - 14, mcy - 6, mcx + 13, mcy - 6, WOOD_HIGHLIGHT)
        c.rect(mcx - 10, mcy + 6, 20, 4, YELLOW_MID, outline=YELLOW_SHADOW) # brass bottom cap

        # Front blades
        for depth, b_angle, tx, ty in blade_data:
            if depth >= 0:
                norm_angle = b_angle + math.pi / 2.0
                nx = math.cos(norm_angle) * 5
                ny = math.sin(norm_angle) * 2
                pts = [
                    (int(mcx - nx * 0.4), int(mcy - ny * 0.4)),
                    (int(tx - nx), int(ty - ny)),
                    (int(tx + nx), int(ty + ny)),
                    (int(mcx + nx * 0.4), int(mcy + ny * 0.4))
                ]
                c.polygon(pts, fill=BROWN_MID, outline=BROWN_DARKEST)
                c.line(int(mcx - nx * 0.4), int(mcy - ny * 0.4), int(tx - nx), int(ty - ny), WOOD_HIGHLIGHT)

        # Hanging pull chain swinging slightly
        chain_sway = int(math.sin(phase) * 2)
        c.line(mcx + 4, mcy + 10, mcx + 4 + chain_sway, mcy + 28, YELLOW_MID)
        c.circle(mcx + 4 + chain_sway, mcy + 30, 2, WOOD_HIGHLIGHT, outline=BROWN_DARKEST)

        frames.append(c)
    return frames


def generate_prop_clock() -> List[PixelCanvas]:
    """
    prop_clock.png: 64x64, 8 frames, 4 fps, loop: true.
    Wall clock with swinging pendulum and ticking second hand.
    """
    frames = []
    for f in range(8):
        c = PixelCanvas(64, 64, TRANSPARENT)
        phase = f / 8.0 * 2.0 * math.pi

        # Clock body case (x=14..49, y=4..60)
        c.rect(14, 4, 36, 56, BROWN_MID, outline=BROWN_DARKEST)
        c.line(14, 4, 49, 4, WOOD_HIGHLIGHT)
        c.line(14, 5, 14, 59, WOOD_HIGHLIGHT)

        # Top section: Clock Face (cx=32, cy=20, radius 14)
        c.circle(32, 20, 14, DUSK_CREAM, outline=OUTLINE)
        # Dial tick marks at 12, 3, 6, 9
        c.set_pixel(32, 8, OUTLINE)  # 12
        c.set_pixel(44, 20, OUTLINE) # 3
        c.set_pixel(32, 32, OUTLINE) # 6
        c.set_pixel(20, 20, OUTLINE) # 9

        # Hour hand (fixed at 8:00)
        c.line(32, 20, 25, 24, OUTLINE)
        # Minute hand (fixed at 15 min)
        c.line(32, 20, 41, 20, OUTLINE)
        # Second hand ticking each frame! (angle rotates 360 across 8 frames)
        sec_angle = phase - math.pi / 2.0
        sx = int(32 + math.cos(sec_angle) * 10)
        sy = int(20 + math.sin(sec_angle) * 10)
        c.line(32, 20, sx, sy, RED_MID)
        c.set_pixel(32, 20, YELLOW_MID) # brass pin center

        # Lower section: Glass window with swinging pendulum (x=20..44, y=36..56)
        c.rect(20, 36, 24, 20, SHADOW_PURPLE_DEEP, outline=BROWN_DARKEST)
        c.line(20, 36, 43, 36, BROWN_DARK)

        # Pendulum swinging: angle = sin(phase) * 0.3 radians
        pend_angle = math.sin(phase) * 0.32
        px = int(32 + math.sin(pend_angle) * 16)
        py = int(36 + math.cos(pend_angle) * 16)
        c.line(32, 36, px, py, YELLOW_SHADOW)
        # Shiny brass pendulum bob
        c.circle(px, py, 4, YELLOW_MID, outline=YELLOW_SHADOW)
        c.set_pixel(px - 1, py - 1, PURE_WHITE)

        frames.append(c)
    return frames


def generate_prop_lamp() -> List[PixelCanvas]:
    """
    prop_lamp.png: 96x128, 6 frames, 8 fps, loop: true.
    Desk lamp with flickering bulb and radial glow.
    """
    frames = []
    # Subtle brightness flicker offsets across 6 frames
    glow_levels = [1.0, 1.15, 0.85, 1.05, 1.2, 0.95]

    for f in range(6):
        c = PixelCanvas(96, 128, TRANSPARENT)
        lvl = glow_levels[f]

        # Lamp base (weighted circular base at x=50..74, y=118..124)
        c.rect(50, 118, 24, 6, RED_MID, outline=BROWN_DARKEST)
        c.line(50, 118, 73, 118, RED_LIGHT)
        c.circle(62, 120, 2, YELLOW_MID) # switch button

        # Articulated metal Pixar-style arm
        # Lower arm segment: (62, 118) to (76, 76)
        c.line(62, 118, 76, 76, METAL_MID)
        c.line(61, 118, 75, 76, METAL_SHADOW)
        c.circle(76, 76, 3, METAL_MID, outline=BROWN_DARKEST) # pivot joint
        # Upper arm segment: (76, 76) to (44, 46)
        c.line(76, 76, 44, 46, METAL_MID)
        c.line(75, 76, 43, 46, METAL_SHADOW)
        c.circle(44, 46, 3, METAL_MID, outline=BROWN_DARKEST) # shade joint

        # Conical lamp shade head (angled pointing downward-left, centered at (34, 52))
        c.polygon([(44, 42), (48, 50), (24, 68), (14, 54)], fill=RED_MID, outline=BROWN_DARKEST)
        c.line(44, 42, 24, 68, RED_LIGHT)
        # Bulb peeking out of shade rim
        c.circle(23, 64, 4, PURE_WHITE if lvl > 0.9 else YELLOW_LIGHT)

        # Radial glowing light cone (emanating from (23, 64) downwards onto desk/wall)
        cx, cy = 23, 64
        max_dist = int(50 * lvl)
        for gy in range(cy - 20, 128):
            for gx in range(0, 96):
                d = math.sqrt((gx - cx) ** 2 + (gy - cy) ** 2)
                angle = math.atan2(gy - cy, gx - cx)
                # Light cone facing down-left (angles between 0.3*pi and 0.9*pi)
                if 0.5 < angle < 2.5 and d < max_dist:
                    cur = c.get_pixel(gx, gy)
                    if cur[3] != 0:
                        continue # don't overwrite lamp body
                    if d < 15 * lvl:
                        if (gx + gy) % 2 == 0:
                            c.set_pixel(gx, gy, YELLOW_LIGHT)
                    elif d < 30 * lvl:
                        if (gx + gy) % 3 == 0:
                            c.set_pixel(gx, gy, YELLOW_MID)
                    elif d < max_dist:
                        if (gx * 2 + gy) % 5 == 0:
                            c.set_pixel(gx, gy, DUSK_PEACH)

        frames.append(c)
    return frames


def generate_prop_lavalamp() -> List[PixelCanvas]:
    """
    prop_lavalamp.png: 48x96, 10 frames, 6 fps, loop: true.
    Lava lamp blobs rising and falling.
    """
    frames = []
    for f in range(10):
        c = PixelCanvas(48, 96, TRANSPARENT)

        # Metallic base cone (x=14..33, y=74..92)
        c.polygon([(17, 74), (30, 74), (34, 92), (13, 92)], fill=METAL_MID, outline=METAL_SHADOW)
        c.line(17, 74, 30, 74, WHITE_MID)
        c.line(17, 75, 14, 91, WHITE_MID)

        # Metallic top cap (x=17..30, y=8..18)
        c.polygon([(20, 8), (27, 8), (30, 18), (17, 18)], fill=METAL_MID, outline=METAL_SHADOW)
        c.line(20, 8, 27, 8, WHITE_MID)

        # Glass cylinder filled with deep violet fluid (x=17..30, y=18..74)
        c.rect(17, 18, 14, 56, SHADOW_PURPLE_DARK, outline=OUTLINE)
        c.line(17, 18, 17, 73, PURPLE_LIGHT) # glass reflection highlight

        # Bottom heater pool of wax (y=66..73)
        c.rect(18, 68, 12, 6, RED_MID)
        c.line(18, 68, 29, 68, RED_LIGHT)

        # Animated Lava Blobs across 10 frames:
        # Blob 1: Rising from bottom to top
        t1 = (f / 10.0)
        b1_y = int(66 - t1 * 44) # rises from 66 to 22
        b1_r = 4 if 25 < b1_y < 60 else 3
        c.circle(23, b1_y, b1_r, RED_MID, outline=RED_SHADOW)
        c.set_pixel(23, b1_y, YELLOW_LIGHT) # glowing hot core

        # Blob 2: Descending slowly down right side
        t2 = ((f + 5) % 10) / 10.0
        b2_y = int(22 + t2 * 44) # falls from 22 to 66
        c.circle(25, b2_y, 3, RED_LIGHT, outline=RED_SHADOW)
        c.set_pixel(25, b2_y, ORANGE_LIGHT)

        # Blob 3: Tiny fast bubble through middle
        t3 = (f * 2 % 10) / 10.0
        b3_y = int(64 - t3 * 42)
        c.circle(21, b3_y, 2, RED_LIGHT)
        c.set_pixel(21, b3_y, YELLOW_LIGHT)

        # Top cooled wax pool (y=19..22)
        c.rect(18, 19, 12, 3, RED_SHADOW)

        frames.append(c)
    return frames


def generate_prop_fishbowl() -> List[PixelCanvas]:
    """
    prop_fishbowl.png: 96x96, 10 frames, 8 fps, loop: true.
    Goldfish swimming in bowl, bubbles rising.
    """
    frames = []
    for f in range(10):
        c = PixelCanvas(96, 96, TRANSPARENT)
        phase = f / 10.0 * 2.0 * math.pi

        # Spherical glass fishbowl (cx=48, cy=52, radius 34)
        c.circle(48, 52, 34, TEAL_SHADOW, outline=OUTLINE)
        # Flat water level at y=28
        c.line(26, 28, 70, 28, BLUE_LIGHT)

        # Bottom gravel pebbles (y=74..84)
        for gy in range(74, 85):
            for gx in range(30, 67):
                if (gx - 48) ** 2 + (gy - 52) ** 2 <= 32 ** 2:
                    col = BROWN_LIGHT if (gx + gy) % 3 == 0 else YELLOW_SHADOW
                    c.set_pixel(gx, gy, col)

        # Water plant swaying on left (x=30..38, y=42..74)
        plant_sway = int(math.sin(phase) * 2)
        for py in range(46, 75):
            px = int(34 + math.sin((py - 46) * 0.2) * 3 + plant_sway * (75 - py) / 30.0)
            c.set_pixel(px, py, GREEN_MID)
            c.set_pixel(px + 1, py, GREEN_LIGHT)

        # Goldfish position in swimming figure-8 loop
        gx = int(48 + math.cos(phase) * 14)
        gy = int(50 + math.sin(phase * 2.0) * 6)
        facing_left = (math.sin(phase) > 0)

        # Fish body (ellipse radius 6x4)
        c.circle(gx, gy, 5, ORANGE_MID, outline=OUTLINE)
        c.line(gx - 4, gy, gx + 4, gy, ORANGE_LIGHT) # belly
        # Cute eye
        eye_x = gx - 3 if facing_left else gx + 3
        c.set_pixel(eye_x, gy - 2, PURE_WHITE)
        c.set_pixel(eye_x, gy - 1, OUTLINE)
        # Tail fin wiggling
        tail_dir = 1 if facing_left else -1
        tail_wiggle = int(math.sin(phase * 3.0) * 2)
        tx = gx + tail_dir * 7
        c.polygon([
            (gx + tail_dir * 4, gy),
            (tx, gy - 4 + tail_wiggle),
            (tx, gy + 4 + tail_wiggle)
        ], fill=RED_MID, outline=OUTLINE)

        # 3 Air bubbles rising
        for b_idx in range(3):
            b_phase = (f + b_idx * 3.3) % 10.0 / 10.0
            by = int(72 - b_phase * 44)
            bx = int(42 + b_idx * 8 + math.sin(b_phase * 6.0) * 2)
            if by > 28: # only while underwater
                c.circle(bx, by, 1 + (b_idx % 2), BLUE_LIGHT)
                c.set_pixel(bx, by, PURE_WHITE)

        # Glass bowl rim highlights
        c.circle(48, 52, 34, TRANSPARENT, outline=OUTLINE)
        c.line(26, 28, 38, 28, WHITE_MID)
        c.line(24, 34, 20, 52, WHITE_MID) # glass specular reflection arc

        frames.append(c)
    return frames


def generate_prop_tv() -> List[PixelCanvas]:
    """
    prop_tv.png: 128x96, 6 frames, 10 fps, loop: true.
    Old CRT TV with cartoon flicker, color bars, static.
    """
    frames = []
    for f in range(6):
        c = PixelCanvas(128, 96, TRANSPARENT)

        # V-shaped rabbit ear antenna (x=64, y=4..24)
        c.line(64, 24, 44, 4, METAL_MID)
        c.circle(44, 4, 2, WHITE_MID) # foil ball
        c.line(64, 24, 84, 4, METAL_MID)
        c.circle(84, 4, 2, WHITE_MID)

        # Wooden TV cabinet body (x=16..112, y=24..88)
        c.rect(16, 24, 96, 64, BROWN_MID, outline=BROWN_DARKEST)
        c.line(16, 24, 111, 24, WOOD_HIGHLIGHT)
        c.line(16, 25, 16, 87, BROWN_LIGHT)
        c.rect(14, 88, 100, 4, BROWN_DARK, outline=BROWN_DARKEST) # plinth base

        # Right control panel (x=88..108, y=28..84)
        c.rect(88, 28, 20, 56, BROWN_DARK, outline=BROWN_DARKEST)
        # Rotary knobs
        c.circle(98, 38, 4, METAL_MID, outline=OUTLINE)
        c.circle(98, 52, 4, METAL_MID, outline=OUTLINE)
        # Speaker slots
        for sy in range(64, 82, 4):
            c.line(92, sy, 104, sy, OUTLINE)

        # CRT Screen bezel (x=22..84, y=28..84)
        c.rect(22, 28, 62, 56, VOID_BLACK, outline=METAL_SHADOW)

        # Screen display content cycling per frame:
        sx0, sy0, sw, sh = 25, 31, 56, 50

        if f == 0:
            # Color test bars
            bar_w = sw // 7
            bars = [PURE_WHITE, YELLOW_MID, TEAL_LIGHT, GREEN_MID, DUSK_PINK, RED_MID, BLUE_MID]
            for bi, bcol in enumerate(bars):
                c.rect(sx0 + bi * bar_w, sy0, bar_w + 1, sh, bcol)
        elif f in (1, 3):
            # Cartoon animation frame: Kid hero jumping with speedlines
            c.rect(sx0, sy0, sw, sh, BLUE_LIGHT)
            # Smiling kid face
            k_cy = 54 if f == 1 else 50
            c.circle(53, k_cy, 8, SKIN_LIGHT, outline=OUTLINE)
            c.circle(53, k_cy - 4, 9, ORANGE_MID) # hair
            c.set_pixel(51, k_cy, OUTLINE) # eye
            c.set_pixel(55, k_cy, OUTLINE)
            c.line(51, k_cy + 3, 55, k_cy + 3, RED_MID) # smile
            # Speedlines in background
            for ly in [36, 42, 68, 74]:
                c.line(sx0 + 2, ly, sx0 + 16, ly, PURE_WHITE)
                c.line(sx0 + 38, ly, sx0 + 52, ly, PURE_WHITE)
        elif f == 2:
            # Static noise snow
            for py in range(sy0, sy0 + sh):
                for px in range(sx0, sx0 + sw):
                    if (px * 7 + py * 13 + f * 5) % 3 == 0:
                        c.set_pixel(px, py, PURE_WHITE)
                    elif (px * 3 + py * 5) % 2 == 0:
                        c.set_pixel(px, py, METAL_SHADOW)
                    else:
                        c.set_pixel(px, py, VOID_BLACK)
        elif f == 4:
            # Static glitch sync bar rolling down
            c.rect(sx0, sy0, sw, sh, BLUE_RICH)
            c.rect(sx0, sy0 + 18, sw, 14, PURE_WHITE)
            c.line(sx0, sy0 + 24, sx0 + sw, sy0 + 24, OUTLINE)
        else: # f == 5
            # Cartoon heart celebration
            c.rect(sx0, sy0, sw, sh, DUSK_ROSE)
            c.circle(50, 52, 6, RED_MID)
            c.circle(56, 52, 6, RED_MID)
            c.polygon([(44, 54), (62, 54), (53, 66)], fill=RED_MID)
            c.set_pixel(48, 50, PURE_WHITE)

        # CRT Scanlines across screen
        for py in range(sy0, sy0 + sh, 2):
            c.line(sx0, py, sx0 + sw - 1, py, OUTLINE)

        # Screen glass corner reflection
        c.line(sx0 + 2, sy0 + 2, sx0 + 14, sy0 + 2, WHITE_MID)
        c.line(sx0 + 2, sy0 + 3, sx0 + 2, sy0 + 14, WHITE_MID)

        frames.append(c)
    return frames


def generate_prop_mobile() -> List[PixelCanvas]:
    """
    prop_mobile.png: 96x96, 10 frames, 6 fps, loop: true.
    Baby mobile of stars and moons rotating in 3D.
    """
    frames = []
    for f in range(10):
        c = PixelCanvas(96, 96, TRANSPARENT)
        phase = f / 10.0 * 2.0 * math.pi

        # Top ceiling cord down to center ring
        c.line(48, 0, 48, 16, YELLOW_MID)
        c.circle(48, 16, 3, YELLOW_MID, outline=YELLOW_SHADOW)

        # Crossbars rotating in perspective (rx=32, ry=10)
        # 4 rotating arms
        charms = [
            (0.0, "moon", YELLOW_LIGHT),
            (math.pi * 0.5, "star", YELLOW_MID),
            (math.pi, "cloud", BLUE_LIGHT),
            (math.pi * 1.5, "rocket", RED_MID)
        ]

        # Center hanging charm (Saturn, hangs lower)
        c.line(48, 16, 48, 48, YELLOW_SHADOW)
        c.circle(48, 52, 5, DUSK_PINK, outline=DUSK_ROSE)
        c.line(40, 53, 56, 51, DUSK_PEACH) # ring

        # Calculate 3D positions for the 4 orbital charms
        charm_pos = []
        for angle_offset, ctype, col in charms:
            a = phase + angle_offset
            cx = int(48 + math.cos(a) * 32)
            cy = int(16 + math.sin(a) * 10)
            depth = math.sin(a) # depth sorting
            charm_pos.append((depth, cx, cy, ctype, col))

        charm_pos.sort(key=lambda item: item[0])

        for depth, cx, cy, ctype, col in charm_pos:
            # Crossbar arm from center ring to charm hook
            c.line(48, 16, cx, cy, YELLOW_MID)
            # Hanging string
            hy = cy + 22
            c.line(cx, cy, cx, hy, YELLOW_SHADOW)

            # Draw specific charm shape
            if ctype == "moon":
                c.circle(cx, hy + 6, 6, col, outline=YELLOW_SHADOW)
                c.circle(cx + 3, hy + 5, 5, TRANSPARENT)
            elif ctype == "star":
                c.circle(cx, hy + 6, 5, col, outline=YELLOW_SHADOW)
                c.set_pixel(cx, hy + 2, PURE_WHITE)
            elif ctype == "cloud":
                c.circle(cx - 3, hy + 7, 4, col)
                c.circle(cx + 3, hy + 7, 4, col)
                c.circle(cx, hy + 5, 5, PURE_WHITE)
            elif ctype == "rocket":
                c.rect(cx - 2, hy + 2, 4, 8, col)
                c.set_pixel(cx, hy + 1, PURE_WHITE)
                c.set_pixel(cx - 3, hy + 8, RED_LIGHT)
                c.set_pixel(cx + 2, hy + 8, RED_LIGHT)

        frames.append(c)
    return frames


def generate_prop_poster_flap() -> List[PixelCanvas]:
    """
    prop_poster_flap.png: 64x96, 6 frames, 6 fps, loop: true.
    Poster corner fluttering in breeze.
    """
    frames = []
    # Corner flap displacements across 6 frames
    flap_heights = [2, 8, 16, 22, 12, 5]

    for f in range(6):
        c = PixelCanvas(64, 96, TRANSPARENT)
        fl = flap_heights[f]

        # Pinned poster base (x=8..56, y=8..88)
        # Drop shadow on wall
        c.rect(10, 10, 48, 80, SHADOW_PURPLE_DEEP)

        # Poster paper body
        c.rect(8, 8, 48, 80, VOID_BLACK, outline=PURE_WHITE)
        # Poster artwork: comic hero blast
        c.rect(12, 12, 40, 72, BLUE_RICH)
        c.circle(32, 44, 14, YELLOW_MID, outline=YELLOW_LIGHT)
        c.line(22, 44, 42, 44, RED_MID)
        c.line(32, 34, 32, 54, RED_MID)

        # 3 Secure Pushpins (top-left, top-right, bottom-left)
        c.circle(11, 11, 2, RED_MID, outline=OUTLINE)
        c.circle(53, 11, 2, YELLOW_MID, outline=OUTLINE)
        c.circle(11, 85, 2, BLUE_MID, outline=OUTLINE)

        # Bottom-right unpinned corner fluttering!
        # Clear the triangular corner from main poster
        c.polygon([(56 - fl, 88), (56, 88 - fl), (56, 88)], fill=TRANSPARENT)
        # Underside curled paper showing white reverse side & curl shadow
        c.polygon([(56 - fl, 88), (56, 88 - fl), (56 - int(fl * 0.8), 88 - int(fl * 0.8))],
                  fill=WHITE_SHADOW, outline=OUTLINE)
        c.line(56 - fl, 88, 56, 88 - fl, PURE_WHITE) # crease highlight

        frames.append(c)
    return frames


def generate_prop_plant() -> List[PixelCanvas]:
    """
    prop_plant.png: 64x96, 8 frames, 6 fps, loop: true.
    Potted plant leaves swaying.
    """
    frames = []
    for f in range(8):
        c = PixelCanvas(64, 96, TRANSPARENT)
        phase = f / 8.0 * 2.0 * math.pi

        # Terracotta flower pot (x=18..46, y=62..92)
        # Saucer
        c.rect(16, 90, 32, 4, BROWN_DARK, outline=BROWN_DARKEST)
        # Pot body
        c.polygon([(18, 68), (46, 68), (42, 90), (22, 90)], fill=BROWN_LIGHT, outline=BROWN_DARKEST)
        # Pot rim
        c.rect(16, 62, 32, 6, BROWN_MID, outline=BROWN_DARKEST)
        c.line(16, 62, 47, 62, WOOD_HIGHLIGHT)
        # Soil
        c.line(20, 68, 44, 68, WOOD_BLACK)

        # 3 Lush Monstera Leaves swaying on stems:
        # Left leaf sway
        l_sway = int(math.sin(phase) * 3)
        c.line(32, 68, 20 + l_sway, 46, GREEN_SHADOW)
        c.circle(18 + l_sway, 40, 10, GREEN_MID, outline=GREEN_DEEP)
        c.circle(17 + l_sway, 39, 8, GREEN_LIGHT)
        c.line(14 + l_sway, 37, 22 + l_sway, 43, GREEN_HIGHLIGHT) # vein

        # Center tall leaf sway
        c_sway = int(math.sin(phase + math.pi * 0.5) * 2)
        c.line(32, 68, 32 + c_sway, 32, GREEN_SHADOW)
        c.circle(32 + c_sway, 24, 12, GREEN_MID, outline=GREEN_DEEP)
        c.circle(32 + c_sway, 23, 9, GREEN_LIGHT)
        c.line(32 + c_sway, 16, 32 + c_sway, 30, GREEN_HIGHLIGHT)

        # Right leaf sway (lagging phase)
        r_sway = int(math.sin(phase - math.pi * 0.4) * 3)
        c.line(32, 68, 44 + r_sway, 48, GREEN_SHADOW)
        c.circle(46 + r_sway, 42, 10, GREEN_MID, outline=GREEN_DEEP)
        c.circle(46 + r_sway, 41, 8, GREEN_LIGHT)
        c.line(42 + r_sway, 45, 50 + r_sway, 39, GREEN_HIGHLIGHT)

        frames.append(c)
    return frames


def generate_prop_windup_robot() -> List[PixelCanvas]:
    """
    prop_windup_robot.png: 48x64, 8 frames, 10 fps, loop: true.
    Wind-up tin robot walking.
    """
    frames = []
    for f in range(8):
        c = PixelCanvas(48, 64, TRANSPARENT)
        phase = f / 8.0 * 2.0 * math.pi
        bob = 1 if f in (2, 6) else 0

        # Winding key on left side rotating 360 across 8 frames
        key_phase = phase
        kx = int(14 - math.cos(key_phase) * 4)
        c.line(16, 34 - bob, 20, 34 - bob, YELLOW_MID)
        c.circle(kx, 34 - bob, 3, YELLOW_MID, outline=YELLOW_SHADOW)
        c.set_pixel(kx, 34 - bob, PURE_WHITE)

        # Boxy robot head (x=19..33, y=14..28)
        hy = 14 - bob
        c.rect(19, hy, 14, 14, METAL_MID, outline=OUTLINE)
        c.line(19, hy, 32, hy, WHITE_MID)
        # Antenna with yellow ball tip
        c.line(26, hy - 6, 26, hy, METAL_SHADOW)
        c.circle(26, hy - 7, 2, YELLOW_MID, outline=OUTLINE)
        # Red dial eyes & mouth grille
        c.set_pixel(22, hy + 4, RED_MID)
        c.set_pixel(30, hy + 4, RED_MID)
        c.line(23, hy + 10, 29, hy + 10, OUTLINE)

        # Square tin torso (x=17..35, y=28..46)
        ty = 28 - bob
        c.rect(17, ty, 18, 18, METAL_MID, outline=OUTLINE)
        c.line(17, ty, 34, ty, WHITE_MID)
        # Chest meter gauge with needle
        c.rect(21, ty + 3, 10, 7, DUSK_CREAM, outline=OUTLINE)
        c.line(26, ty + 8, 28, ty + 4, RED_MID)
        c.rect(21, ty + 12, 10, 3, RED_MID) # red racing stripe

        # Arms swinging counter to legs
        arm_sway = int(math.sin(phase) * 4)
        # Left arm
        c.line(17, ty + 2, 12, ty + 10 + arm_sway, METAL_SHADOW)
        c.circle(12, ty + 10 + arm_sway, 2, METAL_MID, outline=OUTLINE)
        # Right arm
        c.line(35, ty + 2, 40, ty + 10 - arm_sway, METAL_SHADOW)
        c.circle(40, ty + 10 - arm_sway, 2, METAL_MID, outline=OUTLINE)

        # Legs walking (planted on floor at y=63)
        leg_sway = int(math.sin(phase) * 3)
        # Left leg
        c.rect(20, ty + 18, 4, 14 - bob + leg_sway, METAL_SHADOW, outline=OUTLINE)
        c.rect(18, ty + 32 - bob + leg_sway, 7, 4, METAL_MID, outline=OUTLINE)
        # Right leg
        c.rect(28, ty + 18, 4, 14 - bob - leg_sway, METAL_SHADOW, outline=OUTLINE)
        c.rect(27, ty + 32 - bob - leg_sway, 7, 4, METAL_MID, outline=OUTLINE)

        frames.append(c)
    return frames


def generate_prop_train() -> List[PixelCanvas]:
    """
    prop_train.png: 192x48, 8 frames, 10 fps, loop: true.
    Toy train puffing steam along track.
    """
    frames = []
    for f in range(8):
        c = PixelCanvas(192, 48, TRANSPARENT)
        phase = f / 8.0 * 2.0 * math.pi

        # Track along bottom (y=40..46)
        # Wooden sleepers / ties
        for tx in range(0, 192, 12):
            c.rect(tx, 42, 8, 4, BROWN_MID, outline=BROWN_DARKEST)
        # Steel rails
        c.line(0, 41, 191, 41, METAL_MID)
        c.line(0, 40, 191, 40, PURE_WHITE) # rail highlight

        # Locomotive Engine (x=50..150, y=14..42)
        # Cowcatcher at front (x=144..158, y=32..42)
        c.polygon([(144, 32), (158, 42), (144, 42)], fill=BROWN_DARKEST, outline=OUTLINE)
        c.line(144, 32, 158, 42, WOOD_HIGHLIGHT)

        # Red boiler cylinder
        c.rect(80, 22, 64, 18, RED_MID, outline=OUTLINE)
        c.line(80, 22, 143, 22, RED_LIGHT)
        c.rect(100, 21, 4, 20, YELLOW_MID) # brass boiler band
        c.rect(122, 21, 4, 20, YELLOW_MID)

        # Smokestack (x=132..140, y=12..22)
        c.rect(132, 14, 8, 8, BROWN_DARKEST, outline=OUTLINE)
        c.line(130, 13, 141, 13, YELLOW_MID)

        # Steam dome
        c.circle(112, 18, 4, YELLOW_MID, outline=YELLOW_SHADOW)

        # Blue engineer's cab (x=52..80, y=14..40)
        c.rect(52, 14, 28, 26, BLUE_MID, outline=OUTLINE)
        c.rect(50, 12, 32, 3, BLUE_LIGHT, outline=OUTLINE) # roof
        c.rect(58, 18, 12, 10, YELLOW_LIGHT, outline=OUTLINE) # window

        # Coal Tender Car (x=18..48, y=24..40)
        c.rect(18, 26, 30, 14, BLUE_MID, outline=OUTLINE)
        # Coal pile
        c.circle(33, 24, 6, VOID_BLACK)
        c.circle(26, 25, 4, VOID_BLACK)
        c.circle(40, 25, 4, VOID_BLACK)

        # Wheels and drive rods
        # Tender wheels
        c.circle(26, 40, 4, VOID_BLACK, outline=OUTLINE)
        c.circle(40, 40, 4, VOID_BLACK, outline=OUTLINE)
        # Engine wheels
        c.circle(70, 38, 6, RED_MID, outline=OUTLINE)
        c.circle(94, 38, 6, RED_MID, outline=OUTLINE)
        c.circle(118, 38, 6, RED_MID, outline=OUTLINE)
        c.circle(140, 41, 3, VOID_BLACK, outline=OUTLINE) # front small wheel

        # Reciprocating drive rod connecting wheels
        rx_off = int(math.cos(phase) * 3)
        ry_off = int(math.sin(phase) * 3)
        c.line(70 + rx_off, 38 + ry_off, 118 + rx_off, 38 + ry_off, METAL_MID)
        c.circle(70 + rx_off, 38 + ry_off, 1, PURE_WHITE)
        c.circle(94 + rx_off, 38 + ry_off, 1, PURE_WHITE)
        c.circle(118 + rx_off, 38 + ry_off, 1, PURE_WHITE)

        # 3 Billowing Steam Puffs expanding and drifting left
        for s_idx in range(3):
            s_prog = ((f + s_idx * 2.7) % 8.0) / 8.0
            sx = int(136 - s_prog * 45)
            sy = int(12 - s_prog * 10)
            sr = int(2 + s_prog * 5)
            if s_prog < 0.85:
                c.circle(sx, sy, sr, PURE_WHITE if s_prog < 0.4 else WHITE_SHADOW)

        frames.append(c)
    return frames


def generate_prop_snowglobe() -> List[PixelCanvas]:
    """
    prop_snowglobe.png: 64x64, 10 frames, 8 fps, loop: true.
    Snow globe with sparkle glitter swirling around a cozy winter cabin.
    """
    frames = []
    # 22 glitter particles orbiting cabin in 3D vortex
    glitter_seeds = [
        (0.2, 14, 6), (1.1, 18, 8), (2.3, 12, 5), (3.4, 16, 7),
        (4.2, 20, 9), (5.1, 10, 4), (0.8, 15, 6), (1.9, 17, 8),
        (2.8, 13, 5), (3.9, 19, 7), (4.7, 11, 4), (5.8, 16, 8),
        (0.5, 12, 5), (1.5, 15, 7), (2.5, 18, 8), (3.2, 14, 6),
        (4.0, 16, 7), (4.9, 13, 5), (5.5, 17, 8), (0.1, 11, 4),
        (2.0, 15, 6), (3.7, 18, 8)
    ]

    for f in range(10):
        c = PixelCanvas(64, 64, TRANSPARENT)
        phase = f / 10.0 * 2.0 * math.pi

        # Mahogany wooden base (y=46..60)
        c.polygon([(16, 48), (48, 48), (52, 60), (12, 60)], fill=BROWN_MID, outline=BROWN_DARKEST)
        c.line(16, 48, 47, 48, WOOD_HIGHLIGHT)
        # Brass plaque on base
        c.rect(24, 52, 16, 5, YELLOW_MID, outline=YELLOW_SHADOW)
        c.line(26, 54, 37, 54, OUTLINE)

        # Spherical glass dome (cx=32, cy=28, radius 23)
        c.circle(32, 28, 23, BLUE_SHADOW, outline=OUTLINE)
        # Snowy ground inside dome (y=42..47)
        c.rect(17, 43, 30, 5, PURE_WHITE)
        c.line(17, 47, 47, 47, WHITE_SHADOW)

        # Cozy winter cabin (x=22..36, y=32..43)
        c.rect(23, 34, 13, 9, BROWN_MID, outline=BROWN_DARKEST)
        # Warm glowing yellow window
        c.rect(26, 37, 4, 4, YELLOW_MID, outline=YELLOW_SHADOW)
        c.set_pixel(27, 38, YELLOW_LIGHT)
        # Snow-covered pitched roof with chimney
        c.polygon([(21, 34), (29, 27), (38, 34)], fill=PURE_WHITE, outline=WHITE_SHADOW)
        c.rect(33, 26, 3, 5, BROWN_DARK) # chimney
        c.set_pixel(34, 23, WHITE_SHADOW) # tiny smoke puff

        # Snowy evergreen pine tree (x=38..48, y=28..43)
        c.polygon([(43, 28), (38, 35), (48, 35)], fill=GREEN_MID, outline=GREEN_SHADOW)
        c.line(39, 34, 47, 34, PURE_WHITE) # snow on branches
        c.polygon([(43, 33), (37, 42), (49, 42)], fill=GREEN_MID, outline=GREEN_SHADOW)
        c.line(38, 41, 48, 41, PURE_WHITE)
        c.rect(42, 42, 2, 2, BROWN_DARK)

        # Swirling glitter snow particles inside globe
        for a_off, rx, ry in glitter_seeds:
            g_angle = phase + a_off
            gx = int(32 + math.cos(g_angle) * rx)
            gy = int(28 + math.sin(g_angle) * ry + math.sin(phase + a_off * 2.0) * 3)
            # Only draw inside the glass dome circle
            if (gx - 32) ** 2 + (gy - 28) ** 2 <= 21 ** 2:
                # Glitter sparkle flash
                is_sparkle = ((f + int(a_off * 10)) % 5 == 0)
                col = PURE_WHITE if is_sparkle else YELLOW_LIGHT
                c.set_pixel(gx, gy, col)

        # Glass dome perimeter reflection arc
        c.circle(32, 28, 23, TRANSPARENT, outline=OUTLINE)
        c.line(16, 20, 24, 12, PURE_WHITE)
        c.line(15, 24, 18, 18, WHITE_MID)

        frames.append(c)
    return frames


# =============================================================================
# 3. MAIN RUNNER & MANIFEST UPDATER
# =============================================================================

def update_manifest_and_art_data():
    manifest_path = Path("art/v2/manifest.json")
    if not manifest_path.exists():
        print("Warning: art/v2/manifest.json not found, creating new.")
        manifest = {}
    else:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)

    # Required manifest metadata for our 20 assets
    v2_specs = {
        "bg_sky_gradient.png": {"frame_w": 1, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
        "bg_far.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
        "bg_far_stars.png": {"frame_w": 960, "frame_h": 540, "frames": 4, "fps": 3, "loop": True},
        "bg_mid.png": {"frame_w": 1280, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
        "bg_near.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
        "fg_legs.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
        "fg_dust.png": {"frame_w": 960, "frame_h": 540, "frames": 1, "fps": 0, "loop": False},
        "prop_curtain.png": {"frame_w": 96, "frame_h": 192, "frames": 8, "fps": 6, "loop": True},
        "prop_fan.png": {"frame_w": 128, "frame_h": 64, "frames": 8, "fps": 12, "loop": True},
        "prop_clock.png": {"frame_w": 64, "frame_h": 64, "frames": 8, "fps": 4, "loop": True},
        "prop_lamp.png": {"frame_w": 96, "frame_h": 128, "frames": 6, "fps": 8, "loop": True},
        "prop_lavalamp.png": {"frame_w": 48, "frame_h": 96, "frames": 10, "fps": 6, "loop": True},
        "prop_fishbowl.png": {"frame_w": 96, "frame_h": 96, "frames": 10, "fps": 8, "loop": True},
        "prop_tv.png": {"frame_w": 128, "frame_h": 96, "frames": 6, "fps": 10, "loop": True},
        "prop_mobile.png": {"frame_w": 96, "frame_h": 96, "frames": 10, "fps": 6, "loop": True},
        "prop_poster_flap.png": {"frame_w": 64, "frame_h": 96, "frames": 6, "fps": 6, "loop": True},
        "prop_plant.png": {"frame_w": 64, "frame_h": 96, "frames": 8, "fps": 6, "loop": True},
        "prop_windup_robot.png": {"frame_w": 48, "frame_h": 64, "frames": 8, "fps": 10, "loop": True},
        "prop_train.png": {"frame_w": 192, "frame_h": 48, "frames": 8, "fps": 10, "loop": True},
        "prop_snowglobe.png": {"frame_w": 64, "frame_h": 64, "frames": 10, "fps": 8, "loop": True},
    }

    manifest.update(v2_specs)

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"Updated {manifest_path} with {len(v2_specs)} background & prop entries.")

    # Regenerate scripts/art_data.gd
    os.system("python3 tools/gen_art_data.py")


def generate_all_backgrounds_and_props():
    dst = Path("art/v2")
    dst.mkdir(parents=True, exist_ok=True)
    print("=== Generating High-Resolution Parallax Backgrounds & Ambient Props v2 ===")

    # 1. bg_sky_gradient.png (1x540)
    print("Generating bg_sky_gradient.png (1x540)...")
    sky = generate_bg_sky_gradient()
    sky.to_image().save(dst / "bg_sky_gradient.png", "PNG")

    # 2. bg_far.png (960x540)
    print("Generating bg_far.png (960x540)...")
    far = generate_bg_far()
    far.to_image().save(dst / "bg_far.png", "PNG")

    # 3. bg_far_stars.png (3840x540, 4 frames of 960x540)
    print("Generating bg_far_stars.png (4 frames of 960x540)...")
    stars_frames = generate_bg_far_stars()
    assemble_strip(stars_frames, str(dst / "bg_far_stars.png"))

    # 4. bg_mid.png (1280x540)
    print("Generating bg_mid.png (1280x540)...")
    mid = generate_bg_mid()
    mid.to_image().save(dst / "bg_mid.png", "PNG")

    # 5. bg_near.png (960x540)
    print("Generating bg_near.png (960x540)...")
    near = generate_bg_near()
    near.to_image().save(dst / "bg_near.png", "PNG")

    # 6. fg_legs.png (960x540)
    print("Generating fg_legs.png (960x540)...")
    legs = generate_fg_legs()
    legs.to_image().save(dst / "fg_legs.png", "PNG")

    # 7. fg_dust.png (960x540)
    print("Generating fg_dust.png (960x540)...")
    dust = generate_fg_dust()
    dust.to_image().save(dst / "fg_dust.png", "PNG")

    # Ambient Props:
    # 8. prop_curtain.png (96x192, 8 frames)
    print("Generating prop_curtain.png (8 frames of 96x192)...")
    assemble_strip(generate_prop_curtain(), str(dst / "prop_curtain.png"))

    # 9. prop_fan.png (128x64, 8 frames)
    print("Generating prop_fan.png (8 frames of 128x64)...")
    assemble_strip(generate_prop_fan(), str(dst / "prop_fan.png"))

    # 10. prop_clock.png (64x64, 8 frames)
    print("Generating prop_clock.png (8 frames of 64x64)...")
    assemble_strip(generate_prop_clock(), str(dst / "prop_clock.png"))

    # 11. prop_lamp.png (96x128, 6 frames)
    print("Generating prop_lamp.png (6 frames of 96x128)...")
    assemble_strip(generate_prop_lamp(), str(dst / "prop_lamp.png"))

    # 12. prop_lavalamp.png (48x96, 10 frames)
    print("Generating prop_lavalamp.png (10 frames of 48x96)...")
    assemble_strip(generate_prop_lavalamp(), str(dst / "prop_lavalamp.png"))

    # 13. prop_fishbowl.png (96x96, 10 frames)
    print("Generating prop_fishbowl.png (10 frames of 96x96)...")
    assemble_strip(generate_prop_fishbowl(), str(dst / "prop_fishbowl.png"))

    # 14. prop_tv.png (128x96, 6 frames)
    print("Generating prop_tv.png (6 frames of 128x96)...")
    assemble_strip(generate_prop_tv(), str(dst / "prop_tv.png"))

    # 15. prop_mobile.png (96x96, 10 frames)
    print("Generating prop_mobile.png (10 frames of 96x96)...")
    assemble_strip(generate_prop_mobile(), str(dst / "prop_mobile.png"))

    # 16. prop_poster_flap.png (64x96, 6 frames)
    print("Generating prop_poster_flap.png (6 frames of 64x96)...")
    assemble_strip(generate_prop_poster_flap(), str(dst / "prop_poster_flap.png"))

    # 17. prop_plant.png (64x96, 8 frames)
    print("Generating prop_plant.png (8 frames of 64x96)...")
    assemble_strip(generate_prop_plant(), str(dst / "prop_plant.png"))

    # 18. prop_windup_robot.png (48x64, 8 frames)
    print("Generating prop_windup_robot.png (8 frames of 48x64)...")
    assemble_strip(generate_prop_windup_robot(), str(dst / "prop_windup_robot.png"))

    # 19. prop_train.png (192x48, 8 frames)
    print("Generating prop_train.png (8 frames of 192x48)...")
    assemble_strip(generate_prop_train(), str(dst / "prop_train.png"))

    # 20. prop_snowglobe.png (64x64, 10 frames)
    print("Generating prop_snowglobe.png (10 frames of 64x64)...")
    assemble_strip(generate_prop_snowglobe(), str(dst / "prop_snowglobe.png"))

    # Update manifest & art data
    update_manifest_and_art_data()
    print("=== All Backgrounds & Props Generated Successfully! ===")


if __name__ == "__main__":
    generate_all_backgrounds_and_props()
