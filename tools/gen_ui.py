"""Younger Sibling Simulator - UI & Font Generator."""

from typing import List, Dict
from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE,
    SHADOW_DEEP, SHADOW_MID, PURPLE_MID, PURPLE_LIGHT,
    BROWN_DARKEST, BROWN_DARK, BROWN_MID, BROWN_LIGHT, WOOD_HIGHLIGHT,
    RED_SHADOW, RED_MID, RED_LIGHT,
    YELLOW_SHADOW, YELLOW_MID, YELLOW_LIGHT,
    ORANGE_SHADOW, ORANGE_MID,
    WHITE_SHADOW, PURE_WHITE,
    VOID_BLACK
)


def generate_ui_trouble_pip() -> List[PixelCanvas]:
    """12x12, 2 frames.
    Frame 0: Empty recessed circle.
    Frame 1: Bright red angry kid face with gritted teeth and furrowed brow.
    """
    frames = []

    # Frame 0: Empty recessed circular socket
    c0 = PixelCanvas(12, 12, TRANSPARENT)
    # Outer circle border (radius ~5, center at 5.5, 5.5)
    c0.circle(5, 5, 5, SHADOW_DEEP, outline=OUTLINE)
    c0.circle(6, 6, 5, SHADOW_DEEP, outline=OUTLINE)
    # Top-left deep recessed cavity shadow
    c0.rect(3, 2, 6, 2, VOID_BLACK)
    c0.rect(2, 3, 2, 4, VOID_BLACK)
    c0.circle(5, 5, 3, SHADOW_MID)
    c0.set_pixel(4, 4, SHADOW_DEEP)
    # Bottom-right bevel catch-light (ambient light from top-left)
    c0.line(5, 9, 8, 9, PURPLE_LIGHT)
    c0.line(7, 8, 9, 8, PURPLE_LIGHT)
    c0.set_pixel(8, 7, PURPLE_MID)
    c0.set_pixel(9, 6, PURPLE_MID)
    frames.append(c0)

    # Frame 1: Bright red angry kid face with gritted teeth & furrowed brow
    c1 = PixelCanvas(12, 12, TRANSPARENT)
    # Circular head base in RED_MID with OUTLINE
    c1.circle(5, 5, 5, RED_MID, outline=OUTLINE)
    c1.circle(6, 6, 5, RED_MID, outline=OUTLINE)

    # Top-left rim highlight & bottom-right rim shadow
    c1.line(3, 1, 7, 1, RED_LIGHT)
    c1.line(1, 3, 1, 5, RED_LIGHT)
    c1.set_pixel(2, 2, RED_LIGHT)
    c1.line(4, 10, 8, 10, RED_SHADOW)
    c1.line(10, 4, 10, 7, RED_SHADOW)
    c1.set_pixel(9, 9, RED_SHADOW)

    # Furrowed angry brow (sharp steep V-shape scowl)
    # Left eyebrow slanting down
    c1.set_pixel(2, 3, OUTLINE)
    c1.set_pixel(3, 3, OUTLINE)
    c1.set_pixel(4, 4, OUTLINE)
    # Right eyebrow slanting down
    c1.set_pixel(9, 3, OUTLINE)
    c1.set_pixel(8, 3, OUTLINE)
    c1.set_pixel(7, 4, OUTLINE)
    # Center brow furrow wrinkle
    c1.set_pixel(5, 3, RED_SHADOW)
    c1.set_pixel(6, 3, RED_SHADOW)
    c1.set_pixel(5, 4, OUTLINE)
    c1.set_pixel(6, 4, OUTLINE)

    # Glaring angry eyes (pupils glaring inward)
    # Left eye
    c1.set_pixel(3, 5, PURE_WHITE)
    c1.set_pixel(4, 5, OUTLINE)  # pupil
    # Right eye
    c1.set_pixel(7, 5, OUTLINE)  # pupil
    c1.set_pixel(8, 5, PURE_WHITE)
    # Eye shadows
    c1.set_pixel(2, 5, RED_SHADOW)
    c1.set_pixel(9, 5, RED_SHADOW)

    # Gritted teeth clenched mouth (x=3..8, y=7..8)
    c1.rect(3, 7, 6, 2, PURE_WHITE, outline=OUTLINE)
    # Vertical tooth separators
    c1.set_pixel(4, 7, OUTLINE)
    c1.set_pixel(4, 8, OUTLINE)
    c1.set_pixel(6, 7, OUTLINE)
    c1.set_pixel(6, 8, OUTLINE)
    # Horizontal clench line
    c1.set_pixel(3, 7, OUTLINE)
    c1.set_pixel(8, 7, OUTLINE)
    # Chin crease / grimace
    c1.line(4, 9, 7, 9, RED_SHADOW)
    # Anger cheek flush
    c1.set_pixel(2, 6, RED_LIGHT)
    c1.set_pixel(9, 6, RED_LIGHT)

    frames.append(c1)
    return frames


def generate_ui_slot() -> List[PixelCanvas]:
    """52x28, 2 frames.
    Frame 0: Toy-box wood slot with corner rivets.
    Frame 1: Selected golden glowing frame with corner stars.
    """
    frames = []
    w, h = 52, 28

    # Frame 0: Toy-box wood slot with corner rivets
    c0 = PixelCanvas(w, h, TRANSPARENT)
    # Outer outline
    c0.rect(0, 0, w, h, BROWN_MID, outline=OUTLINE)

    # Wooden frame bevels & grain
    c0.line(1, 1, w - 2, 1, WOOD_HIGHLIGHT)
    c0.line(1, 2, w - 2, 2, BROWN_LIGHT)
    c0.line(1, 1, 1, h - 2, WOOD_HIGHLIGHT)
    c0.line(2, 2, 2, h - 3, BROWN_LIGHT)
    c0.line(w - 2, 1, w - 2, h - 2, BROWN_DARK)
    c0.line(1, h - 2, w - 2, h - 2, BROWN_DARK)
    c0.line(1, h - 3, w - 2, h - 3, BROWN_DARKEST)

    # Inset dark cavity bed (x=3..48, y=3..24)
    c0.rect(3, 3, w - 6, h - 6, SHADOW_DEEP, outline=BROWN_DARKEST)
    # Inset cavity drop shadow
    c0.line(4, 4, w - 5, 4, VOID_BLACK)
    c0.line(4, 4, 4, h - 5, VOID_BLACK)
    c0.line(4, 5, w - 5, 5, SHADOW_DEEP)

    # 4 Corner metallic dome rivets (2x2 with specular highlight)
    for rx, ry in [(2, 2), (w - 4, 2), (2, h - 4), (w - 4, h - 4)]:
        c0.set_pixel(rx, ry, PURE_WHITE)
        c0.set_pixel(rx + 1, ry, WHITE_SHADOW)
        c0.set_pixel(rx, ry + 1, WHITE_SHADOW)
        c0.set_pixel(rx + 1, ry + 1, OUTLINE)

    frames.append(c0)

    # Frame 1: Selected golden glowing frame with corner stars
    c1 = PixelCanvas(w, h, TRANSPARENT)
    # Radiant gold border
    c1.rect(0, 0, w, h, YELLOW_MID, outline=OUTLINE)
    # Top and left bright gleam
    c1.line(1, 1, w - 2, 1, PURE_WHITE)
    c1.line(1, 2, w - 2, 2, YELLOW_LIGHT)
    c1.line(1, 1, 1, h - 2, PURE_WHITE)
    c1.line(2, 2, 2, h - 3, YELLOW_LIGHT)
    # Bottom and right golden shadow bevels
    c1.line(w - 2, 1, w - 2, h - 2, YELLOW_SHADOW)
    c1.line(1, h - 2, w - 2, h - 2, ORANGE_SHADOW)
    c1.line(1, h - 3, w - 2, h - 3, YELLOW_SHADOW)

    # Inset cavity with glowing golden inner rim
    c1.rect(3, 3, w - 6, h - 6, SHADOW_DEEP, outline=OUTLINE)
    c1.line(4, 4, w - 5, 4, YELLOW_LIGHT)
    c1.line(4, 4, 4, h - 5, YELLOW_LIGHT)
    c1.line(w - 5, 4, w - 5, h - 5, YELLOW_SHADOW)
    c1.line(4, h - 5, w - 5, h - 5, YELLOW_SHADOW)

    # 4 Corner twinkling golden stars (3x3 with PURE_WHITE core)
    for cx, cy in [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]:
        c1.set_pixel(cx, cy, PURE_WHITE)
        c1.set_pixel(cx - 1, cy, YELLOW_LIGHT)
        c1.set_pixel(cx + 1, cy, YELLOW_LIGHT)
        c1.set_pixel(cx, cy - 1, YELLOW_LIGHT)
        c1.set_pixel(cx, cy + 1, YELLOW_LIGHT)

    frames.append(c1)
    return frames


def generate_ui_cooldown_bar() -> List[PixelCanvas]:
    """160x6, 2 frames.
    Frame 0: Empty track.
    Frame 1: Bright yellow/amber candy-striped fill.
    """
    frames = []
    w, h = 160, 6

    # Frame 0: Empty track
    c0 = PixelCanvas(w, h, TRANSPARENT)
    c0.rect(0, 0, w, h, SHADOW_DEEP, outline=OUTLINE)
    # Deep inset groove shadow along top
    c0.line(1, 1, w - 2, 1, VOID_BLACK)
    # Catch-light along bottom lip
    c0.line(1, 4, w - 2, 4, SHADOW_MID)
    frames.append(c0)

    # Frame 1: Filled gauge with bright yellow/amber candy stripes
    c1 = PixelCanvas(w, h, TRANSPARENT)
    c1.rect(0, 0, w, h, YELLOW_MID, outline=OUTLINE)

    # Glossy top highlight beam across full width
    c1.line(1, 1, w - 2, 1, YELLOW_LIGHT)

    # Alternating 45-degree candy stripes across rows 2..4
    for x in range(1, w - 1):
        for y in range(2, 5):
            stripe = ((x + y) // 4) % 2
            if stripe == 0:
                # Bright Sunny Gold stripe
                if y == 2:
                    c1.set_pixel(x, y, YELLOW_LIGHT)
                elif y == 3:
                    c1.set_pixel(x, y, YELLOW_MID)
                else:
                    c1.set_pixel(x, y, YELLOW_SHADOW)
            else:
                # Warm Amber/Orange stripe
                if y == 2:
                    c1.set_pixel(x, y, ORANGE_MID)
                elif y == 3:
                    c1.set_pixel(x, y, ORANGE_MID)
                else:
                    c1.set_pixel(x, y, ORANGE_SHADOW)

    frames.append(c1)
    return frames


def generate_keycap(num: str) -> PixelCanvas:
    """10x10 beveled keycap icon with centered numeral."""
    c = PixelCanvas(10, 10, TRANSPARENT)

    # Outer outline with rounded corners
    c.rect(0, 0, 10, 10, WHITE_SHADOW, outline=OUTLINE)
    c.set_pixel(0, 0, TRANSPARENT)
    c.set_pixel(9, 0, TRANSPARENT)
    c.set_pixel(0, 9, TRANSPARENT)
    c.set_pixel(9, 9, TRANSPARENT)

    # Top & left 3D highlight bevel
    c.line(1, 1, 8, 1, PURE_WHITE)
    c.line(1, 1, 1, 8, PURE_WHITE)

    # Bottom & right 3D shadow bevel
    c.line(1, 8, 8, 8, PURPLE_MID)
    c.line(8, 1, 8, 8, PURPLE_MID)
    c.set_pixel(8, 8, SHADOW_DEEP)

    # Centered numeral in dark OUTLINE
    if num == "1":
        # Centered 1 (width 4, height 5, at x=3..6, y=2..6)
        c.line(5, 2, 5, 6, OUTLINE)
        c.set_pixel(4, 3, OUTLINE)  # serif flag
        c.line(3, 6, 6, 6, OUTLINE)  # base pedestal
    elif num == "2":
        # Centered 2 (width 4, height 5, at x=3..6, y=2..6)
        c.line(3, 2, 5, 2, OUTLINE)
        c.set_pixel(6, 3, OUTLINE)
        c.line(4, 4, 5, 4, OUTLINE)
        c.set_pixel(3, 5, OUTLINE)
        c.line(3, 6, 6, 6, OUTLINE)
    elif num == "3":
        # Centered 3 (width 4, height 5, at x=3..6, y=2..6)
        c.line(3, 2, 5, 2, OUTLINE)
        c.set_pixel(6, 3, OUTLINE)
        c.line(4, 4, 5, 4, OUTLINE)
        c.set_pixel(6, 5, OUTLINE)
        c.line(3, 6, 5, 6, OUTLINE)

    return c


def generate_font_pixel() -> PixelCanvas:
    """
    5x7 ASCII bitmap font sheet covering ASCII 32 to 126 (95 chars).
    Grid: 16 columns x 6 rows of 6x8 cells -> 96x48 px.
    1-bit pure white on transparent.
    """
    c = PixelCanvas(96, 48, TRANSPARENT)

    GLYPHS: Dict[str, List[str]] = {
        ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
        '!': ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
        '"': ["01010", "01010", "01010", "00000", "00000", "00000", "00000"],
        '#': ["01010", "01010", "11111", "01010", "11111", "01010", "01010"],
        '$': ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
        '%': ["11001", "11010", "00100", "01000", "01011", "10011", "00000"],
        '&': ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
        "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
        '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
        ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
        '*': ["00000", "10101", "01110", "11111", "01110", "10101", "00000"],
        '+': ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
        ',': ["00000", "00000", "00000", "00000", "00100", "00100", "01000"],
        '-': ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
        '.': ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
        '/': ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],

        '0': ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
        '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
        '2': ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
        '3': ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
        '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
        '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
        '6': ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
        '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
        '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
        '9': ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],

        ':': ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
        ';': ["00000", "01100", "01100", "00000", "01100", "00100", "01000"],
        '<': ["00010", "00100", "01000", "10000", "01000", "00100", "00010"],
        '=': ["00000", "11111", "00000", "11111", "00000", "00000", "00000"],
        '>': ["01000", "00100", "00010", "00001", "00010", "00100", "01000"],
        '?': ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
        '@': ["01110", "10001", "00101", "01011", "01000", "10001", "01110"],

        'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
        'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
        'C': ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
        'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
        'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
        'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
        'G': ["01111", "10000", "10000", "10111", "10001", "10001", "01111"],
        'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
        'I': ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
        'J': ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
        'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
        'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
        'M': ["10001", "11011", "10101", "10001", "10001", "10001", "10001"],
        'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
        'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
        'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
        'Q': ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
        'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
        'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
        'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
        'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
        'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
        'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
        'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
        'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
        'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],

        '[': ["01110", "01000", "01000", "01000", "01000", "01000", "01110"],
        '\\': ["10000", "01000", "01000", "00100", "00010", "00010", "00001"],
        ']': ["01110", "00010", "00010", "00010", "00010", "00010", "01110"],
        '^': ["00100", "01010", "10001", "00000", "00000", "00000", "00000"],
        '_': ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
        '`': ["01000", "00100", "00000", "00000", "00000", "00000", "00000"],

        'a': ["00000", "00000", "01110", "00001", "01111", "10001", "01111"],
        'b': ["10000", "10000", "10110", "11001", "10001", "10001", "11110"],
        'c': ["00000", "00000", "01111", "10000", "10000", "10000", "01111"],
        'd': ["00001", "00001", "01101", "10011", "10001", "10001", "01111"],
        'e': ["00000", "00000", "01110", "10001", "11111", "10000", "01111"],
        'f': ["00110", "01001", "01000", "11110", "01000", "01000", "01000"],
        'g': ["00000", "00000", "01111", "10001", "01111", "00001", "01110"],
        'h': ["10000", "10000", "10110", "11001", "10001", "10001", "10001"],
        'i': ["00100", "00000", "01100", "00100", "00100", "00100", "01110"],
        'j': ["00010", "00000", "00110", "00010", "00010", "10010", "01100"],
        'k': ["10000", "10000", "10010", "10100", "11000", "10100", "10010"],
        'l': ["01100", "00100", "00100", "00100", "00100", "00100", "01110"],
        'm': ["00000", "00000", "11010", "10101", "10101", "10101", "10001"],
        'n': ["00000", "00000", "10110", "11001", "10001", "10001", "10001"],
        'o': ["00000", "00000", "01110", "10001", "10001", "10001", "01110"],
        'p': ["00000", "00000", "11110", "10001", "11110", "10000", "10000"],
        'q': ["00000", "00000", "01111", "10001", "01111", "00001", "00001"],
        'r': ["00000", "00000", "10110", "11001", "10000", "10000", "10000"],
        's': ["00000", "00000", "01111", "10000", "01110", "00001", "11110"],
        't': ["01000", "01000", "11110", "01000", "01000", "01001", "00110"],
        'u': ["00000", "00000", "10001", "10001", "10001", "10011", "01101"],
        'v': ["00000", "00000", "10001", "10001", "10001", "01010", "00100"],
        'w': ["00000", "00000", "10001", "10101", "10101", "11011", "01010"],
        'x': ["00000", "00000", "10001", "01010", "00100", "01010", "10001"],
        'y': ["00000", "00000", "10001", "10001", "01111", "00001", "01110"],
        'z': ["00000", "00000", "11111", "00010", "00100", "01000", "11111"],

        '{': ["00010", "00100", "00100", "01000", "00100", "00100", "00010"],
        '|': ["00100", "00100", "00100", "00100", "00100", "00100", "00100"],
        '}': ["01000", "00100", "00100", "00010", "00100", "00100", "01000"],
        '~': ["00000", "01101", "10010", "00000", "00000", "00000", "00000"],
    }

    for ascii_code in range(32, 127):
        idx = ascii_code - 32
        col = idx % 16
        row = idx // 16
        gx = col * 6
        gy = row * 8

        char = chr(ascii_code)
        if char in GLYPHS:
            lines = GLYPHS[char]
            for py, line in enumerate(lines):
                for px, bit in enumerate(line):
                    if bit == '1':
                        c.set_pixel(gx + px, gy + py, PURE_WHITE)

    return c


def generate_all_ui():
    assemble_strip(generate_ui_trouble_pip(), "art/incoming/ui_trouble_pip.png")
    assemble_strip(generate_ui_slot(), "art/incoming/ui_slot.png")
    assemble_strip(generate_ui_cooldown_bar(), "art/incoming/ui_cooldown_bar.png")

    k1 = generate_keycap("1")
    k1.to_image().save("art/incoming/ui_key_1.png", "PNG")
    print("Saved art/incoming/ui_key_1.png (10x10)")

    k2 = generate_keycap("2")
    k2.to_image().save("art/incoming/ui_key_2.png", "PNG")
    print("Saved art/incoming/ui_key_2.png (10x10)")

    k3 = generate_keycap("3")
    k3.to_image().save("art/incoming/ui_key_3.png", "PNG")
    print("Saved art/incoming/ui_key_3.png (10x10)")

    font = generate_font_pixel()
    font.to_image().save("art/incoming/font_pixel.png", "PNG")
    print("Saved art/incoming/font_pixel.png (96x48)")


if __name__ == "__main__":
    generate_all_ui()
