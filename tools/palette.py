"""Younger Sibling Simulator - Shared 64-Color Palette for v2."""

from typing import Dict, Tuple, List
from PIL import Image

# 64 Colors strictly following the art brief:
# - Dusk tones: deep purples & indigos in shadow
# - Warm wood browns & oranges in light
# - Saturated toy colors: Red (#e64848), Blue (#4d99f2), Yellow (#f2cc40), Green (#66cc73)
# - Extended ramps with hue shifting: shadows lean purple/magenta, highlights lean warm yellow/white
# - Selective outline: darkest purple (#120d1f)
# - Maximum 64 colors

HEX_PALETTE: List[str] = [
    # 0..7: Deep Purples & Shadows (Selective outlines & dark ambients)
    "#0a0710",  # 0: VOID_BLACK (Deep void, pit bottom)
    "#120d1f",  # 1: OUTLINE (Darkest selective outline & deepest shadow)
    "#181128",  # 2: SHADOW_PURPLE_DARK
    "#201636",  # 3: SHADOW_PURPLE_DEEP
    "#2d1f47",  # 4: SHADOW_PURPLE_MID
    "#3d2859",  # 5: PURPLE_DARK
    "#49306b",  # 6: PURPLE_MID
    "#5c397d",  # 7: PURPLE_RICH

    # 8..14: Dusk Lilac, Pink & Peach Ramps
    "#6b4382",  # 8: PURPLE_LIGHT
    "#824d94",  # 9: DUSK_LILAC
    "#945998",  # 10: DUSK_PINK
    "#b06b9c",  # 11: DUSK_ROSE
    "#c482aa",  # 12: DUSK_PEACH
    "#dba0bc",  # 13: DUSK_BLUSH
    "#f0c5d6",  # 14: DUSK_CREAM

    # 15..19: Skin Tones (5 tones)
    "#6e2a22",  # 15: SKIN_DEEP
    "#a85042",  # 16: SKIN_SHADOW
    "#db8267",  # 17: SKIN_MID
    "#f7b594",  # 18: SKIN_LIGHT
    "#ffdab8",  # 19: SKIN_HIGHLIGHT

    # 20..26: Browns & Wood Ramps (7 tones)
    "#1c0e0b",  # 20: WOOD_BLACK
    "#2e1713",  # 21: BROWN_DARKEST
    "#4e2517",  # 22: BROWN_DARK
    "#753a1e",  # 23: BROWN_MID
    "#a85d2c",  # 24: BROWN_LIGHT
    "#d68945",  # 25: WOOD_HIGHLIGHT
    "#f0af67",  # 26: WOOD_LIT

    # 27..32: Toy Red / Warm Accent Ramp (6 tones)
    "#591024",  # 27: RED_DEEP
    "#821a36",  # 28: RED_SHADOW
    "#b8273d",  # 29: RED_RICH
    "#e64848",  # 30: RED_MID (Canonical brief toy red)
    "#f77963",  # 31: RED_LIGHT
    "#ffa894",  # 32: RED_HIGHLIGHT

    # 33..38: Toy Blue / Denim Ramp (6 tones)
    "#15244a",  # 33: BLUE_DEEP
    "#213970",  # 34: BLUE_SHADOW
    "#345eb0",  # 35: BLUE_RICH
    "#4d99f2",  # 36: BLUE_MID (Canonical brief toy blue)
    "#82cbfa",  # 37: BLUE_LIGHT
    "#bce4fc",  # 38: BLUE_HIGHLIGHT

    # 39..44: Toy Yellow / Gold Ramp (6 tones)
    "#633d0c",  # 39: YELLOW_DEEP
    "#a16a1b",  # 40: YELLOW_SHADOW
    "#cf9729",  # 41: YELLOW_RICH
    "#f2cc40",  # 42: YELLOW_MID (Canonical brief toy yellow)
    "#fdf07e",  # 43: YELLOW_LIGHT
    "#fffbc2",  # 44: YELLOW_HIGHLIGHT

    # 45..50: Toy Green Ramp (6 tones)
    "#113621",  # 45: GREEN_DEEP
    "#1f5939",  # 46: GREEN_SHADOW
    "#3d8f52",  # 47: GREEN_RICH
    "#66cc73",  # 48: GREEN_MID (Canonical brief toy green)
    "#a6e88e",  # 49: GREEN_LIGHT
    "#d5f7be",  # 50: GREEN_HIGHLIGHT

    # 51..54: Speed Orange Ramp (4 tones)
    "#7d2a0a",  # 51: ORANGE_DEEP
    "#b33f14",  # 52: ORANGE_SHADOW
    "#fa6d23",  # 53: ORANGE_MID
    "#ff9954",  # 54: ORANGE_LIGHT

    # 55..58: Rug / Teal / Mint Ramp (4 tones)
    "#144747",  # 55: TEAL_SHADOW
    "#227878",  # 56: TEAL_MID
    "#42b5ab",  # 57: TEAL_LIGHT
    "#82ebd9",  # 58: TEAL_HIGHLIGHT

    # 59..63: Whites, Metals & Highlights (5 tones)
    "#627387",  # 59: METAL_SHADOW
    "#8fa0b5",  # 60: METAL_MID
    "#c2d2e3",  # 61: WHITE_SHADOW
    "#e2ebf5",  # 62: WHITE_MID
    "#f5f8fc",  # 63: PURE_WHITE
]

assert len(HEX_PALETTE) == 64, f"Palette must have exactly 64 colors, got {len(HEX_PALETTE)}"

def hex_to_rgb(h: str) -> Tuple[int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

PALETTE_RGB: List[Tuple[int, int, int]] = [hex_to_rgb(h) for h in HEX_PALETTE]
PALETTE_RGBA: List[Tuple[int, int, int, int]] = [(r, g, b, 255) for (r, g, b) in PALETTE_RGB]

# Named RGBA constants
VOID_BLACK = PALETTE_RGBA[0]
OUTLINE = PALETTE_RGBA[1]
SHADOW_PURPLE_DARK = PALETTE_RGBA[2]
SHADOW_DEEP = PALETTE_RGBA[3]
SHADOW_PURPLE_DEEP = PALETTE_RGBA[3]
SHADOW_MID = PALETTE_RGBA[4]
SHADOW_PURPLE_MID = PALETTE_RGBA[4]
PURPLE_DARK = PALETTE_RGBA[5]
PURPLE_MID = PALETTE_RGBA[6]
PURPLE_RICH = PALETTE_RGBA[7]
PURPLE_LIGHT = PALETTE_RGBA[8]
DUSK_LILAC = PALETTE_RGBA[9]
DUSK_PINK = PALETTE_RGBA[10]
DUSK_ROSE = PALETTE_RGBA[11]
DUSK_PEACH = PALETTE_RGBA[12]
DUSK_BLUSH = PALETTE_RGBA[13]
DUSK_CREAM = PALETTE_RGBA[14]

SKIN_DEEP = PALETTE_RGBA[15]
SKIN_SHADOW = PALETTE_RGBA[16]
SKIN_MID = PALETTE_RGBA[17]
SKIN_LIGHT = PALETTE_RGBA[18]
SKIN_HIGHLIGHT = PALETTE_RGBA[19]

WOOD_BLACK = PALETTE_RGBA[20]
BROWN_DARKEST = PALETTE_RGBA[21]
BROWN_DARK = PALETTE_RGBA[22]
BROWN_MID = PALETTE_RGBA[23]
BROWN_LIGHT = PALETTE_RGBA[24]
WOOD_HIGHLIGHT = PALETTE_RGBA[25]
WOOD_LIT = PALETTE_RGBA[26]

RED_DEEP = PALETTE_RGBA[27]
RED_SHADOW = PALETTE_RGBA[28]
RED_RICH = PALETTE_RGBA[29]
RED_MID = PALETTE_RGBA[30]
RED_LIGHT = PALETTE_RGBA[31]
RED_HIGHLIGHT = PALETTE_RGBA[32]

BLUE_DEEP = PALETTE_RGBA[33]
BLUE_SHADOW = PALETTE_RGBA[34]
BLUE_RICH = PALETTE_RGBA[35]
BLUE_MID = PALETTE_RGBA[36]
BLUE_LIGHT = PALETTE_RGBA[37]
BLUE_HIGHLIGHT = PALETTE_RGBA[38]

YELLOW_DEEP = PALETTE_RGBA[39]
YELLOW_SHADOW = PALETTE_RGBA[40]
YELLOW_RICH = PALETTE_RGBA[41]
YELLOW_MID = PALETTE_RGBA[42]
YELLOW_LIGHT = PALETTE_RGBA[43]
YELLOW_HIGHLIGHT = PALETTE_RGBA[44]

GREEN_DEEP = PALETTE_RGBA[45]
GREEN_SHADOW = PALETTE_RGBA[46]
GREEN_RICH = PALETTE_RGBA[47]
GREEN_MID = PALETTE_RGBA[48]
GREEN_LIGHT = PALETTE_RGBA[49]
GREEN_HIGHLIGHT = PALETTE_RGBA[50]

ORANGE_DEEP = PALETTE_RGBA[51]
ORANGE_SHADOW = PALETTE_RGBA[52]
ORANGE_MID = PALETTE_RGBA[53]
ORANGE_LIGHT = PALETTE_RGBA[54]

TEAL_SHADOW = PALETTE_RGBA[55]
TEAL_MID = PALETTE_RGBA[56]
TEAL_LIGHT = PALETTE_RGBA[57]
TEAL_HIGHLIGHT = PALETTE_RGBA[58]

METAL_SHADOW = PALETTE_RGBA[59]
METAL_MID = PALETTE_RGBA[60]
WHITE_SHADOW = PALETTE_RGBA[61]
WHITE_MID = PALETTE_RGBA[62]
PURE_WHITE = PALETTE_RGBA[63]

TRANSPARENT = (0, 0, 0, 0)

VALID_PALETTE_RGBA = set(PALETTE_RGBA)
