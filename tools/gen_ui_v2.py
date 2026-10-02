"""Younger Sibling Simulator - UI, FX, Light Overlays & Fonts Generator v2.

Generates:
1. Particles & FX (Redo at 2x & New Particles):
   - fx_dust.png (32x32, 6f, 20fps)
   - fx_jump_puff.png (32x32, 5f, 24fps)
   - fx_stars.png (48x48, 8f, 16fps)
   - fx_impact.png (64x64, 5f, 30fps)
   - fx_speedline.png (48x16, 4f, 30fps)
   - fx_sparkle.png (16x16, 5f, 16fps)
   - fx_bubble.png (192x48)
   - fx_mote.png (8x8, 6f, 8fps)
   - fx_fluff.png (16x16, 6f, 8fps)
   - fx_firefly.png (12x12, 8f, 10fps)
   - fx_steam.png (24x24, 8f, 10fps)
   - fx_sweat.png (12x12, 4f, 14fps)
   - fx_heart.png (16x16, 6f, 12fps)
   - fx_sleepz.png (16x16, 8f, 6fps)
   - fx_shockwave.png (128x64, 6f, 24fps)
   - fx_confetti.png (16x16, 10f, 16fps)
   - Comic text pops (96x48, 6f, 18fps):
     - fx_text_oof.png
     - fx_text_yikes.png
     - fx_text_nice.png
     - fx_text_whoops.png

2. Light Overlays (hard-banded alpha):
   - light_window.png (384x540, 3 alpha bands)
   - light_lamp.png (256x256, 4 alpha bands)
   - light_vignette.png (960x540, 6 alpha bands)
   - light_godray_anim.png (384x540 per frame, 6 frames, 4 fps)

3. UI Life:
   - ui_trouble_pip.png (24x24, 2 frames)
   - ui_slot.png (104x56, 2 frames)
   - ui_cooldown_bar.png (320x12, 2 frames)
   - ui_key_1.png, ui_key_2.png, ui_key_3.png (20x20)
   - ui_logo.png (384x144)
   - ui_button.png (192x48, 3 frames)
   - ui_banner_clear.png (384x96, 6 frames, 12 fps)
   - ui_banner_grounded.png (384x96, 6 frames, 12 fps)
   - font_pixel.png (10x14 font, 160x84) + font_pixel.json
   - font_pixel_small.png (6x9 font, 96x54)
"""

import json
import math
from typing import List, Dict, Tuple
from PIL import Image
from canvas import PixelCanvas, assemble_strip
from palette import (
    TRANSPARENT, OUTLINE, VOID_BLACK,
    SHADOW_DEEP, SHADOW_MID, SHADOW_PURPLE_DARK, PURPLE_DARK, PURPLE_MID, PURPLE_RICH, PURPLE_LIGHT,
    DUSK_LILAC, DUSK_PINK, DUSK_ROSE, DUSK_PEACH, DUSK_BLUSH, DUSK_CREAM,
    SKIN_DEEP, SKIN_SHADOW, SKIN_MID, SKIN_LIGHT, SKIN_HIGHLIGHT,
    WOOD_BLACK, BROWN_DARKEST, BROWN_DARK, BROWN_MID, BROWN_LIGHT, WOOD_HIGHLIGHT, WOOD_LIT,
    RED_DEEP, RED_SHADOW, RED_RICH, RED_MID, RED_LIGHT, RED_HIGHLIGHT,
    BLUE_DEEP, BLUE_SHADOW, BLUE_RICH, BLUE_MID, BLUE_LIGHT, BLUE_HIGHLIGHT,
    YELLOW_DEEP, YELLOW_SHADOW, YELLOW_RICH, YELLOW_MID, YELLOW_LIGHT, YELLOW_HIGHLIGHT,
    GREEN_DEEP, GREEN_SHADOW, GREEN_RICH, GREEN_MID, GREEN_LIGHT, GREEN_HIGHLIGHT,
    ORANGE_DEEP, ORANGE_SHADOW, ORANGE_MID, ORANGE_LIGHT,
    TEAL_SHADOW, TEAL_MID, TEAL_LIGHT, TEAL_HIGHLIGHT,
    METAL_SHADOW, METAL_MID, WHITE_SHADOW, WHITE_MID, PURE_WHITE
)

WHITE = PURE_WHITE


# ==============================================================================
# 1. PARTICLES & FX (REDO AT 2X & NEW PARTICLES)
# ==============================================================================

def generate_fx_dust() -> List[PixelCanvas]:
    """32x32, 6 frames, fps 20. Crisp ground impact & skid dust puff."""
    frames = []

    # Frame 0: Instant impact burst hugging ground (y=26..30)
    c0 = PixelCanvas(32, 32, TRANSPARENT)
    c0.rect(8, 28, 16, 3, WHITE)
    c0.line(10, 26, 22, 26, WHITE)
    c0.set_pixel(5, 29, WHITE)
    c0.set_pixel(27, 29, WHITE)
    frames.append(c0)

    # Frame 1: Expanding dual billowing lobes
    c1 = PixelCanvas(32, 32, TRANSPARENT)
    c1.circle(8, 22, 6, WHITE)
    c1.circle(23, 22, 6, WHITE)
    c1.rect(8, 24, 16, 6, WHITE)
    c1.set_pixel(2, 24, WHITE)
    c1.set_pixel(29, 24, WHITE)
    frames.append(c1)

    # Frame 2: Peak poof volume with hollowed center blowout
    c2 = PixelCanvas(32, 32, TRANSPARENT)
    c2.circle(7, 18, 6, WHITE)
    c2.circle(11, 16, 4, WHITE)
    c2.circle(24, 18, 6, WHITE)
    c2.circle(20, 16, 4, WHITE)
    c2.rect(13, 18, 6, 8, TRANSPARENT)
    c2.line(4, 26, 10, 26, WHITE)
    c2.line(21, 26, 28, 26, WHITE)
    frames.append(c2)

    # Frame 3: Splitting into distinct flying cloudlets
    c3 = PixelCanvas(32, 32, TRANSPARENT)
    c3.rect(3, 14, 6, 6, WHITE)
    c3.circle(6, 17, 3, WHITE)
    c3.rect(23, 14, 6, 6, WHITE)
    c3.circle(26, 17, 3, WHITE)
    c3.set_pixel(1, 20, WHITE)
    c3.set_pixel(30, 20, WHITE)
    c3.set_pixel(10, 24, WHITE)
    c3.set_pixel(21, 24, WHITE)
    frames.append(c3)

    # Frame 4: Dispersing wisp particles
    c4 = PixelCanvas(32, 32, TRANSPARENT)
    for x, y in [(3, 12), (5, 10), (8, 8), (22, 8), (26, 10), (28, 12), (15, 12)]:
        c4.rect(x, y, 2, 2, WHITE)
    frames.append(c4)

    # Frame 5: Fading specks
    c5 = PixelCanvas(32, 32, TRANSPARENT)
    for x, y in [(1, 10), (6, 6), (24, 6), (30, 10), (16, 10)]:
        c5.set_pixel(x, y, WHITE)
    frames.append(c5)

    return frames


def generate_fx_jump_puff() -> List[PixelCanvas]:
    """32x32, 5 frames, fps 24. Downward launch burst cloud."""
    frames = []

    # Frame 0: Launch snap
    c0 = PixelCanvas(32, 32, TRANSPARENT)
    c0.rect(8, 6, 16, 6, WHITE)
    c0.line(4, 8, 27, 8, WHITE)
    frames.append(c0)

    # Frame 1: Downward surging mushroom burst
    c1 = PixelCanvas(32, 32, TRANSPARENT)
    c1.circle(16, 12, 8, WHITE)
    c1.rect(10, 16, 12, 6, WHITE)
    c1.line(12, 22, 19, 22, WHITE)
    c1.set_pixel(4, 12, WHITE)
    c1.set_pixel(27, 12, WHITE)
    frames.append(c1)

    # Frame 2: Expanding hollow shock ring
    c2 = PixelCanvas(32, 32, TRANSPARENT)
    for y in range(6, 30):
        for x in range(2, 30):
            dx = (x - 15.5) / 12.0
            dy = (y - 17.0) / 10.0
            d_sq = dx * dx + dy * dy
            if 0.55 <= d_sq <= 1.05:
                c2.set_pixel(x, y, WHITE)
    frames.append(c2)

    # Frame 3: Shattering droplet particles
    c3 = PixelCanvas(32, 32, TRANSPARENT)
    for x, y in [(4, 8), (6, 8), (24, 8), (26, 8), (2, 16), (29, 16), (6, 24), (24, 24), (15, 28)]:
        c3.rect(x, y, 2, 2, WHITE)
    frames.append(c3)

    # Frame 4: Dissipating specks
    c4 = PixelCanvas(32, 32, TRANSPARENT)
    for x, y in [(1, 6), (30, 6), (1, 18), (30, 18), (5, 28), (26, 28), (16, 30)]:
        c4.set_pixel(x, y, WHITE)
    frames.append(c4)

    return frames


def generate_fx_stars() -> List[PixelCanvas]:
    """48x48, 8 frames, fps 16, loop: true. Circling dizzy stars with 3D perspective."""
    frames = []
    cx, cy = 23.5, 22.0
    rx, ry = 17.0, 7.5

    star_large = [
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
    ]

    for f in range(8):
        c = PixelCanvas(48, 48, TRANSPARENT)
        base_angle = (f / 8.0) * 2.0 * math.pi

        stars = []
        for s in range(3):
            angle = base_angle + s * (2.0 * math.pi / 3.0)
            sx = cx + math.cos(angle) * rx
            sy = cy + math.sin(angle) * ry
            depth = math.sin(angle)
            stars.append((depth, angle, sx, sy))

        stars.sort(key=lambda item: item[0])

        for depth, angle, sx, sy in stars:
            ix = int(round(sx))
            iy = int(round(sy))

            if depth > 0.2:
                # Large foreground star
                for dy in range(7):
                    for dx in range(7):
                        if star_large[dy][dx]:
                            c.set_pixel(ix - 3 + dx, iy - 3 + dy, WHITE)
            elif depth > -0.4:
                # Medium 5x5 star
                for dy in range(5):
                    for dx in range(5):
                        if abs(dx - 2) + abs(dy - 2) <= 2:
                            c.set_pixel(ix - 2 + dx, iy - 2 + dy, WHITE)
            else:
                # Small 2x2 background twinkle
                c.rect(ix - 1, iy - 1, 2, 2, WHITE)

        frames.append(c)

    return frames


def generate_fx_impact() -> List[PixelCanvas]:
    """64x64, 5 frames, fps 30. Comic BANG starburst for hitstop frames."""
    frames = []
    cx, cy = 31.5, 31.5

    # Frame 0: Flash core with 4 piercing cross rays
    c0 = PixelCanvas(64, 64, TRANSPARENT)
    for y in range(24, 40):
        for x in range(24, 40):
            if abs(x - cx) + abs(y - cy) <= 9.0:
                c0.set_pixel(x, y, WHITE)
    c0.rect(30, 6, 4, 52, WHITE)
    c0.rect(6, 30, 52, 4, WHITE)
    frames.append(c0)

    # Frame 1: Full comic BANG starburst
    c1 = PixelCanvas(64, 64, TRANSPARENT)
    num_pts = 16
    radii = [30.0 if i % 2 == 0 else 15.0 for i in range(num_pts)]
    angles = [i * (2.0 * math.pi / num_pts) for i in range(num_pts)]

    for y in range(64):
        for x in range(64):
            dx = x - cx
            dy = y - cy
            dist = math.hypot(dx, dy)
            if dist < 1.0:
                c1.set_pixel(x, y, WHITE)
                continue
            ang = math.atan2(dy, dx)
            if ang < 0:
                ang += 2.0 * math.pi
            idx = int(ang / (2.0 * math.pi / num_pts)) % num_pts
            next_idx = (idx + 1) % num_pts
            a0 = angles[idx]
            a1 = angles[next_idx]
            if a1 < a0:
                a1 += 2.0 * math.pi
            t = (ang - a0) / (a1 - a0)
            max_r = (1.0 - t) * radii[idx] + t * radii[next_idx]
            if dist <= max_r:
                c1.set_pixel(x, y, WHITE)
    frames.append(c1)

    # Frame 2: Hollow center ring blowout, spikes flying outward
    c2 = PixelCanvas(64, 64, TRANSPARENT)
    for y in range(64):
        for x in range(64):
            dist = math.hypot(x - cx, y - cy)
            if 13.0 <= dist <= 31.0:
                ang = math.atan2(y - cy, x - cx)
                if ang < 0: ang += 2.0 * math.pi
                idx = int(ang / (2.0 * math.pi / num_pts)) % num_pts
                if idx % 2 == 0 or dist >= 16.0:
                    c2.set_pixel(x, y, WHITE)
    frames.append(c2)

    # Frame 3: Shattered debris shards
    c3 = PixelCanvas(64, 64, TRANSPARENT)
    for a in angles:
        r = 29.0
        sx = int(round(cx + math.cos(a) * r))
        sy = int(round(cy + math.sin(a) * r))
        if 0 <= sx < 64 and 0 <= sy < 64:
            c3.rect(sx - 1, sy - 1, 3, 3, WHITE)
    frames.append(c3)

    # Frame 4: Outer specks dissipating
    c4 = PixelCanvas(64, 64, TRANSPARENT)
    for a in angles[::2]:
        r = 31.0
        sx = int(round(cx + math.cos(a) * r))
        sy = int(round(cy + math.sin(a) * r))
        if 0 <= sx < 64 and 0 <= sy < 64:
            c4.set_pixel(sx, sy, WHITE)
    frames.append(c4)

    return frames


def generate_fx_speedline() -> List[PixelCanvas]:
    """48x16, 4 frames, fps 30. Horizontal speedlines."""
    frames = []

    # Frame 0: Quick sharp burst of speed streaks born at right
    c0 = PixelCanvas(48, 16, TRANSPARENT)
    c0.line(28, 2, 44, 2, WHITE)
    c0.line(22, 8, 46, 8, WHITE)
    c0.line(36, 10, 46, 10, WHITE)
    c0.line(32, 12, 42, 12, WHITE)
    frames.append(c0)

    # Frame 1: Full-length piercing streaks streaking across
    c1 = PixelCanvas(48, 16, TRANSPARENT)
    c1.line(12, 2, 40, 2, WHITE)
    c1.line(4, 6, 44, 6, WHITE)
    c1.set_pixel(30, 6, TRANSPARENT)
    c1.line(14, 10, 38, 10, WHITE)
    c1.line(6, 12, 32, 12, WHITE)
    frames.append(c1)

    # Frame 2: Streaks flashing leftward
    c2 = PixelCanvas(48, 16, TRANSPARENT)
    c2.line(2, 4, 28, 4, WHITE)
    c2.line(0, 8, 24, 8, WHITE)
    c2.line(4, 12, 20, 12, WHITE)
    frames.append(c2)

    # Frame 3: Dissipating exit wisps
    c3 = PixelCanvas(48, 16, TRANSPARENT)
    c3.line(0, 4, 10, 4, WHITE)
    c3.line(0, 8, 6, 8, WHITE)
    c3.line(0, 12, 8, 12, WHITE)
    frames.append(c3)

    return frames


def generate_fx_sparkle() -> List[PixelCanvas]:
    """16x16, 5 frames, fps 16. 4-point twinkle sparkle."""
    frames = []

    # Frame 0: 2x2 nascent glint
    c0 = PixelCanvas(16, 16, TRANSPARENT)
    c0.rect(7, 7, 2, 2, WHITE)
    frames.append(c0)

    # Frame 1: 4x4 plus cross
    c1 = PixelCanvas(16, 16, TRANSPARENT)
    c1.line(7, 4, 8, 4, WHITE)
    c1.line(7, 11, 8, 11, WHITE)
    c1.rect(4, 7, 8, 2, WHITE)
    frames.append(c1)

    # Frame 2: Max brilliance 4-point sparkle
    c2 = PixelCanvas(16, 16, TRANSPARENT)
    c2.rect(7, 1, 2, 14, WHITE)
    c2.rect(1, 7, 14, 2, WHITE)
    for dx, dy in [(5, 5), (10, 5), (5, 10), (10, 10)]:
        c2.set_pixel(dx, dy, WHITE)
    frames.append(c2)

    # Frame 3: Contracting X-cross twinkle
    c3 = PixelCanvas(16, 16, TRANSPARENT)
    c3.rect(7, 7, 2, 2, WHITE)
    for dx, dy in [(3, 3), (12, 3), (3, 12), (12, 12)]:
        c3.rect(dx, dy, 2, 2, WHITE)
    frames.append(c3)

    # Frame 4: Fading corner specks
    c4 = PixelCanvas(16, 16, TRANSPARENT)
    for dx, dy in [(1, 1), (14, 1), (1, 14), (14, 14)]:
        c4.set_pixel(dx, dy, WHITE)
    frames.append(c4)

    return frames


def generate_fx_bubble() -> PixelCanvas:
    """192x48 speech bubble 9-slice with rounded corners and downward tail."""
    c = PixelCanvas(192, 48, TRANSPARENT)
    w, h = 192, 36
    r = 12

    # Rounded rectangle body (y=0..35)
    for y in range(h):
        for x in range(w):
            in_body = True
            if x < r and y < r and (x - r) ** 2 + (y - r) ** 2 > r * r:
                in_body = False
            elif x >= w - r and y < r and (x - (w - r - 1)) ** 2 + (y - r) ** 2 > r * r:
                in_body = False
            elif x < r and y >= h - r and (x - r) ** 2 + (y - (h - r - 1)) ** 2 > r * r:
                in_body = False
            elif x >= w - r and y >= h - r and (x - (w - r - 1)) ** 2 + (y - (h - r - 1)) ** 2 > r * r:
                in_body = False
            if in_body:
                c.set_pixel(x, y, WHITE)

    # Speech tail at bottom center (x=84..108, y=36..47)
    for ty in range(36, 48):
        t = (ty - 36) / 12.0
        hw = int(12 * (1.0 - t))
        c.line(96 - hw, ty, 96 + hw, ty, WHITE)

    return c


# --- NEW PARTICLES ---

def generate_fx_mote() -> List[PixelCanvas]:
    """8x8, 6 frames, 8 fps. Dust mote drifting in light."""
    frames = []
    positions = [(3, 4), (4, 3), (4, 4), (3, 5), (3, 4), (2, 3)]
    for f in range(6):
        c = PixelCanvas(8, 8, TRANSPARENT)
        mx, my = positions[f]
        c.rect(mx, my, 2, 2, WHITE)
        c.set_pixel(mx - 1, my, WHITE_SHADOW)
        c.set_pixel(mx + 2, my, WHITE_SHADOW)
        frames.append(c)
    return frames


def generate_fx_fluff() -> List[PixelCanvas]:
    """16x16, 6 frames, 8 fps. Floating fluff/feather drifting down."""
    frames = []
    for f in range(6):
        c = PixelCanvas(16, 16, TRANSPARENT)
        ang = (f / 6.0) * math.pi
        y_off = f * 2
        for t in range(8):
            px = int(8 + math.sin(ang + t * 0.4) * 4)
            py = int(2 + t + y_off * 0.5)
            c.set_pixel(px, py, WHITE)
            c.set_pixel(px + 1, py, WHITE_SHADOW)
        frames.append(c)
    return frames


def generate_fx_firefly() -> List[PixelCanvas]:
    """12x12, 8 frames, 10 fps. Soft pulsing firefly bug."""
    frames = []
    sizes = [1, 2, 3, 4, 3, 2, 1, 0]
    for f in range(8):
        c = PixelCanvas(12, 12, TRANSPARENT)
        sz = sizes[f]
        cx, cy = 6, 6
        if sz > 0:
            c.circle(cx, cy, sz, GREEN_LIGHT)
            c.set_pixel(cx, cy, PURE_WHITE)
            c.circle(cx, cy, sz + 1, GREEN_MID)
        else:
            c.set_pixel(cx, cy, GREEN_DEEP)
        frames.append(c)
    return frames


def generate_fx_steam() -> List[PixelCanvas]:
    """24x24, 8 frames, 10 fps. Swirling rising steam wisp."""
    frames = []
    for f in range(8):
        c = PixelCanvas(24, 24, TRANSPARENT)
        for t in range(12):
            wave = math.sin((t + f) * 0.6) * 3.5
            x = int(12 + wave)
            y = int(22 - t * 1.6)
            r = int(1 + t * 0.25)
            c.circle(x, y, r, WHITE_SHADOW)
            c.set_pixel(x, y, PURE_WHITE)
        frames.append(c)
    return frames


def generate_fx_sweat() -> List[PixelCanvas]:
    """12x12, 4 frames, 14 fps. Flinging sweat drop."""
    frames = []
    for f in range(4):
        c = PixelCanvas(12, 12, TRANSPARENT)
        # Teardrop shape moving diagonally
        sx = 2 + f * 2
        sy = 2 + f * 2
        c.polygon([(sx, sy), (sx + 4, sy + 6), (sx - 1, sy + 6)], BLUE_LIGHT, outline=OUTLINE)
        c.circle(sx + 1, sy + 5, 2, BLUE_LIGHT)
        c.set_pixel(sx + 1, sy + 4, PURE_WHITE)
        frames.append(c)
    return frames


def generate_fx_heart() -> List[PixelCanvas]:
    """16x16, 6 frames, 12 fps. Beating cute heart."""
    frames = []
    scales = [0, 1, 2, 1, 0, 0]
    for f in range(6):
        c = PixelCanvas(16, 16, TRANSPARENT)
        s = scales[f]
        # Draw heart
        c.circle(5, 6 - s, 3 + s, RED_MID, outline=OUTLINE)
        c.circle(10, 6 - s, 3 + s, RED_MID, outline=OUTLINE)
        c.polygon([(2 - s, 7 - s), (13 + s, 7 - s), (8, 14 + s)], RED_MID, outline=OUTLINE)
        c.set_pixel(5, 5 - s, RED_LIGHT)
        frames.append(c)
    return frames


def generate_fx_sleepz() -> List[PixelCanvas]:
    """16x16, 8 frames, 6 fps. Cartoon Zzz rising."""
    frames = []
    for f in range(8):
        c = PixelCanvas(16, 16, TRANSPARENT)
        zx = 4 + (f % 3)
        zy = 14 - f * 2
        # Draw 5x5 Z letter
        c.line(zx, zy, zx + 4, zy, WHITE)
        c.line(zx + 4, zy, zx, zy + 4, WHITE)
        c.line(zx, zy + 4, zx + 4, zy + 4, WHITE)
        frames.append(c)
    return frames


def generate_fx_shockwave() -> List[PixelCanvas]:
    """128x64, 6 frames, 24 fps. Expanding ground ring on hard landings."""
    frames = []
    for f in range(6):
        c = PixelCanvas(128, 64, TRANSPARENT)
        rx = 12 + f * 9
        ry = 4 + f * 3
        cx, cy = 64, 32
        for y in range(max(0, cy - ry), min(64, cy + ry + 1)):
            for x in range(max(0, cx - rx), min(128, cx + rx + 1)):
                d_sq = ((x - cx) / float(rx)) ** 2 + ((y - cy) / float(ry)) ** 2
                if 0.75 <= d_sq <= 1.0:
                    c.set_pixel(x, y, WHITE)
        frames.append(c)
    return frames


def generate_fx_confetti() -> List[PixelCanvas]:
    """16x16, 10 frames, 16 fps. Tumbling colorful confetti pieces."""
    frames = []
    colors = [RED_MID, BLUE_MID, YELLOW_MID, GREEN_MID, ORANGE_MID]
    for f in range(10):
        c = PixelCanvas(16, 16, TRANSPARENT)
        # 3 confetti squares rotating
        col = colors[f % len(colors)]
        w_t = int(abs(math.cos(f * 0.7)) * 5) + 1
        h_t = int(abs(math.sin(f * 0.7)) * 5) + 1
        c.rect(8 - w_t // 2, 8 - h_t // 2, w_t, h_t, col, outline=OUTLINE)
        frames.append(c)
    return frames


# --- COMIC TEXT POPS ---

def draw_comic_text(text: str, w: int, h: int, color, glow_color) -> List[PixelCanvas]:
    """96x48, 6 frames, 18 fps comic text pop animation."""
    frames = []
    for f in range(6):
        c = PixelCanvas(w, h, TRANSPARENT)
        cx, cy = w // 2, h // 2

        scale_factor = [0.6, 1.15, 1.25, 1.1, 1.0, 0.95][f]
        if f >= 1:
            # Starburst background
            burst_r = int(20 * scale_factor)
            for a_idx in range(12):
                ang = a_idx * (2 * math.pi / 12)
                r_len = burst_r if a_idx % 2 == 0 else burst_r // 2
                bx = int(cx + math.cos(ang) * r_len)
                by = int(cy + math.sin(ang) * r_len)
                c.line(cx, cy, bx, by, glow_color)

        # Draw text block with thick outline
        font_len = len(text) * 10
        x0 = cx - font_len // 2
        y0 = cy - 7

        # Simple chunky letter block
        for i, ch in enumerate(text):
            lx = x0 + i * 11
            ly = y0
            # Background outline block
            c.rect(lx - 2, ly - 2, 10, 14, OUTLINE)
            c.rect(lx - 1, ly - 1, 8, 12, color)
            c.set_pixel(lx + 1, ly + 1, PURE_WHITE)

        frames.append(c)
    return frames


def generate_fx_text_oof() -> List[PixelCanvas]:
    return draw_comic_text("OOF!", 96, 48, RED_MID, YELLOW_MID)


def generate_fx_text_yikes() -> List[PixelCanvas]:
    return draw_comic_text("YIKES!", 96, 48, ORANGE_MID, YELLOW_LIGHT)


def generate_fx_text_nice() -> List[PixelCanvas]:
    return draw_comic_text("NICE!", 96, 48, TEAL_LIGHT, BLUE_LIGHT)


def generate_fx_text_whoops() -> List[PixelCanvas]:
    return draw_comic_text("WHOOPS", 96, 48, YELLOW_MID, ORANGE_LIGHT)


# ==============================================================================
# 2. LIGHT OVERLAYS (HARD-BANDED ALPHA)
# ==============================================================================

def generate_light_window() -> Image.Image:
    """384x540. Slanted window light shaft with 3 hard alpha bands."""
    w, h = 384, 540
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pixels = img.load()

    # Slanted beam from top-left (x=20..140) down to bottom-right (x=160..380)
    for y in range(h):
        center_x = 80 + (y / float(h)) * 190
        beam_w = 60 + (y / float(h)) * 100

        for x in range(w):
            dist = abs(x - center_x)
            if dist <= beam_w * 0.4:
                # Band 1: Core
                pixels[x, y] = (253, 240, 126, 80)
            elif dist <= beam_w * 0.75:
                # Band 2: Mid
                pixels[x, y] = (253, 240, 126, 45)
            elif dist <= beam_w:
                # Band 3: Outer
                pixels[x, y] = (253, 240, 126, 20)

    return img


def generate_light_lamp() -> Image.Image:
    """256x256. Round lamp glow with 4 hard alpha bands."""
    w, h = 256, 256
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pixels = img.load()
    cx, cy = 128, 128
    max_r = 110.0

    for y in range(h):
        for x in range(w):
            dist = math.hypot(x - cx, y - cy)
            if dist <= max_r * 0.25:
                pixels[x, y] = (255, 251, 194, 150)
            elif dist <= max_r * 0.5:
                pixels[x, y] = (242, 204, 64, 90)
            elif dist <= max_r * 0.75:
                pixels[x, y] = (242, 204, 64, 45)
            elif dist <= max_r:
                pixels[x, y] = (242, 204, 64, 18)

    return img


def generate_light_vignette() -> Image.Image:
    """960x540. Dark border vignette with 6 hard alpha bands."""
    w, h = 960, 540
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pixels = img.load()
    cx, cy = w / 2.0, h / 2.0

    for y in range(h):
        for x in range(w):
            dx = (x - cx) / (cx * 1.05)
            dy = (y - cy) / (cy * 1.05)
            d = math.hypot(dx, dy)
            # 6 hard alpha bands
            if d >= 1.25:
                pixels[x, y] = (10, 7, 16, 200)
            elif d >= 1.1:
                pixels[x, y] = (10, 7, 16, 150)
            elif d >= 0.95:
                pixels[x, y] = (10, 7, 16, 100)
            elif d >= 0.8:
                pixels[x, y] = (10, 7, 16, 60)
            elif d >= 0.65:
                pixels[x, y] = (10, 7, 16, 30)
            elif d >= 0.5:
                pixels[x, y] = (10, 7, 16, 12)

    return img


def generate_light_godray_anim() -> Image.Image:
    """384x540 per frame, 6 frames, 4 fps -> 2304x540 total strip."""
    fw, fh = 384, 540
    num_frames = 6
    strip = Image.new("RGBA", (fw * num_frames, fh), (0, 0, 0, 0))

    base_window = generate_light_window()

    for f in range(num_frames):
        frame_img = base_window.copy()
        px = frame_img.load()
        # Add subtle drifting dust pocket variations
        drift_offset = (f / float(num_frames)) * 2 * math.pi
        for py in range(0, fh, 6):
            px_val = int(80 + (py / float(fh)) * 190 + math.sin(drift_offset + py * 0.03) * 15)
            for r in range(-12, 13):
                xx = px_val + r
                if 0 <= xx < fw:
                    cur = px[xx, py]
                    if cur[3] > 0:
                        # Slightly intensify
                        px[xx, py] = (cur[0], cur[1], cur[2], min(255, cur[3] + 15))

        strip.paste(frame_img, (f * fw, 0))

    return strip


# ==============================================================================
# 3. UI LIFE
# ==============================================================================

def generate_ui_trouble_pip() -> List[PixelCanvas]:
    """24x24, 2 frames. Frame 0: Empty recessed socket. Frame 1: Bright red angry face."""
    frames = []

    # Frame 0: Empty recessed socket
    c0 = PixelCanvas(24, 24, TRANSPARENT)
    c0.circle(12, 12, 10, SHADOW_DEEP, outline=OUTLINE)
    c0.circle(12, 12, 8, VOID_BLACK)
    c0.circle(12, 12, 6, SHADOW_MID)
    c0.line(5, 19, 19, 19, PURPLE_LIGHT)  # bevel catch
    frames.append(c0)

    # Frame 1: Bright red angry face
    c1 = PixelCanvas(24, 24, TRANSPARENT)
    c1.circle(12, 12, 10, RED_MID, outline=OUTLINE)
    c1.line(6, 4, 18, 4, RED_LIGHT)
    c1.line(4, 6, 4, 18, RED_LIGHT)
    c1.line(6, 20, 18, 20, RED_SHADOW)

    # Furrowed eyebrows
    c1.line(6, 8, 10, 10, OUTLINE)
    c1.line(18, 8, 14, 10, OUTLINE)

    # Glaring eyes
    c1.rect(7, 11, 3, 3, PURE_WHITE, outline=OUTLINE)
    c1.set_pixel(8, 12, OUTLINE)
    c1.rect(14, 11, 3, 3, PURE_WHITE, outline=OUTLINE)
    c1.set_pixel(15, 12, OUTLINE)

    # Gritted teeth
    c1.rect(7, 16, 10, 4, PURE_WHITE, outline=OUTLINE)
    c1.line(9, 16, 9, 19, OUTLINE)
    c1.line(12, 16, 12, 19, OUTLINE)
    c1.line(15, 16, 15, 19, OUTLINE)
    frames.append(c1)

    return frames


def generate_ui_slot() -> List[PixelCanvas]:
    """104x56, 2 frames. Frame 0: Toy-box wood slot. Frame 1: Glowing gold slot."""
    frames = []
    w, h = 104, 56

    # Frame 0: Toy-box wood slot
    c0 = PixelCanvas(w, h, TRANSPARENT)
    c0.rect(0, 0, w, h, BROWN_MID, outline=OUTLINE)
    c0.line(2, 2, w - 3, 2, WOOD_HIGHLIGHT)
    c0.line(2, 3, w - 3, 3, BROWN_LIGHT)
    c0.line(2, 2, 2, h - 3, WOOD_HIGHLIGHT)
    c0.line(w - 3, 2, w - 3, h - 3, BROWN_DARK)
    c0.line(2, h - 3, w - 3, h - 3, BROWN_DARK)

    # Inset dark bed
    c0.rect(6, 6, w - 12, h - 12, SHADOW_DEEP, outline=OUTLINE)
    c0.line(7, 7, w - 8, 7, VOID_BLACK)
    c0.line(7, 7, 7, h - 8, VOID_BLACK)

    # 4 Corner rivets
    for rx, ry in [(4, 4), (w - 6, 4), (4, h - 6), (w - 6, h - 6)]:
        c0.rect(rx, ry, 3, 3, METAL_MID, outline=OUTLINE)
        c0.set_pixel(rx + 1, ry + 1, PURE_WHITE)
    frames.append(c0)

    # Frame 1: Glowing gold slot
    c1 = PixelCanvas(w, h, TRANSPARENT)
    c1.rect(0, 0, w, h, YELLOW_MID, outline=OUTLINE)
    c1.line(2, 2, w - 3, 2, PURE_WHITE)
    c1.line(2, 2, 2, h - 3, PURE_WHITE)
    c1.line(w - 3, 2, w - 3, h - 3, YELLOW_SHADOW)
    c1.line(2, h - 3, w - 3, h - 3, YELLOW_SHADOW)

    c1.rect(6, 6, w - 12, h - 12, SHADOW_DEEP, outline=OUTLINE)
    c1.line(7, 7, w - 8, 7, YELLOW_LIGHT)
    c1.line(7, 7, 7, h - 8, YELLOW_LIGHT)

    # 4 Corner twinkling stars
    for cx, cy in [(4, 4), (w - 5, 4), (4, h - 5), (w - 5, h - 5)]:
        c1.set_pixel(cx, cy, PURE_WHITE)
        c1.set_pixel(cx - 1, cy, YELLOW_LIGHT)
        c1.set_pixel(cx + 1, cy, YELLOW_LIGHT)
        c1.set_pixel(cx, cy - 1, YELLOW_LIGHT)
        c1.set_pixel(cx, cy + 1, YELLOW_LIGHT)
    frames.append(c1)

    return frames


def generate_ui_cooldown_bar() -> List[PixelCanvas]:
    """320x12, 2 frames. Frame 0: Empty track. Frame 1: Amber candy-striped fill."""
    frames = []
    w, h = 320, 12

    # Frame 0: Empty track
    c0 = PixelCanvas(w, h, TRANSPARENT)
    c0.rect(0, 0, w, h, SHADOW_DEEP, outline=OUTLINE)
    c0.line(2, 2, w - 3, 2, VOID_BLACK)
    c0.line(2, h - 3, w - 3, h - 3, SHADOW_MID)
    frames.append(c0)

    # Frame 1: Candy-striped fill
    c1 = PixelCanvas(w, h, TRANSPARENT)
    c1.rect(0, 0, w, h, YELLOW_MID, outline=OUTLINE)
    c1.line(2, 2, w - 3, 2, YELLOW_LIGHT)

    for x in range(2, w - 2):
        for y in range(3, h - 2):
            stripe = ((x + y) // 6) % 2
            if stripe == 0:
                c1.set_pixel(x, y, YELLOW_LIGHT if y < 6 else YELLOW_MID)
            else:
                c1.set_pixel(x, y, ORANGE_LIGHT if y < 6 else ORANGE_MID)
    frames.append(c1)

    return frames


def generate_ui_keycap(num: str) -> PixelCanvas:
    """20x20 keycap icon with 3D bevels."""
    c = PixelCanvas(20, 20, TRANSPARENT)
    c.rect(0, 0, 20, 20, WHITE_SHADOW, outline=OUTLINE)
    c.set_pixel(0, 0, TRANSPARENT)
    c.set_pixel(19, 0, TRANSPARENT)
    c.set_pixel(0, 19, TRANSPARENT)
    c.set_pixel(19, 19, TRANSPARENT)

    # 3D bevel highlights
    c.line(2, 2, 17, 2, PURE_WHITE)
    c.line(2, 2, 2, 17, PURE_WHITE)
    c.line(2, 17, 17, 17, PURPLE_MID)
    c.line(17, 2, 17, 17, PURPLE_MID)

    # Numerals in OUTLINE
    if num == "1":
        c.line(10, 5, 10, 14, OUTLINE)
        c.line(11, 5, 11, 14, OUTLINE)
        c.set_pixel(8, 7, OUTLINE)
        c.set_pixel(9, 6, OUTLINE)
        c.line(7, 14, 13, 14, OUTLINE)
    elif num == "2":
        c.line(7, 6, 12, 6, OUTLINE)
        c.line(12, 6, 13, 9, OUTLINE)
        c.line(9, 11, 12, 9, OUTLINE)
        c.line(7, 12, 9, 11, OUTLINE)
        c.line(7, 14, 13, 14, OUTLINE)
    elif num == "3":
        c.line(7, 6, 12, 6, OUTLINE)
        c.line(12, 6, 13, 9, OUTLINE)
        c.line(9, 10, 12, 9, OUTLINE)
        c.line(12, 11, 13, 13, OUTLINE)
        c.line(7, 14, 12, 14, OUTLINE)

    return c


def generate_ui_logo() -> PixelCanvas:
    """384x144 chunky toy-block title 'YOUNGER SIBLING SIMULATOR' with small hand poking in."""
    c = PixelCanvas(384, 144, TRANSPARENT)

    # Background toy block pedestal / banner
    c.rect(12, 16, 360, 112, BROWN_MID, outline=OUTLINE)
    c.line(14, 18, 370, 18, WOOD_HIGHLIGHT)
    c.line(14, 18, 14, 126, WOOD_HIGHLIGHT)
    c.line(370, 18, 370, 126, BROWN_DARK)
    c.line(14, 126, 370, 126, BROWN_DARK)

    # Row 1: "YOUNGER SIBLING" in chunky toy blocks (Red, Blue, Yellow, Green)
    # Block dimensions: 20x24 per letter block
    text1 = "YOUNGER SIBLING"
    block_colors = [RED_MID, BLUE_MID, YELLOW_MID, GREEN_MID, ORANGE_MID]
    start_x1 = 28
    for i, ch in enumerate(text1):
        if ch == ' ':
            continue
        bx = start_x1 + i * 22
        by = 28
        col = block_colors[i % len(block_colors)]
        c.rect(bx, by, 20, 24, col, outline=OUTLINE)
        c.line(bx + 1, by + 1, bx + 18, by + 1, PURE_WHITE)
        c.line(bx + 1, by + 1, bx + 1, by + 22, PURE_WHITE)

    # Row 2: "SIMULATOR"
    text2 = "SIMULATOR"
    start_x2 = 92
    for i, ch in enumerate(text2):
        bx = start_x2 + i * 22
        by = 64
        col = block_colors[(i + 2) % len(block_colors)]
        c.rect(bx, by, 20, 24, col, outline=OUTLINE)
        c.line(bx + 1, by + 1, bx + 18, by + 1, PURE_WHITE)
        c.line(bx + 1, by + 1, bx + 1, by + 22, PURE_WHITE)

    # Sibling hand poking in from the top right (x=330..376, y=2..40)
    c.circle(350, 12, 14, SKIN_MID, outline=OUTLINE)
    c.rect(342, 14, 8, 18, SKIN_MID, outline=OUTLINE)  # pointing finger
    c.circle(346, 32, 4, SKIN_MID, outline=OUTLINE)
    c.set_pixel(346, 32, SKIN_HIGHLIGHT)

    return c


def generate_ui_button() -> List[PixelCanvas]:
    """192x48, 3 frames: idle, hover, pressed."""
    frames = []
    w, h = 192, 48

    # Frame 0: Idle
    c0 = PixelCanvas(w, h, TRANSPARENT)
    c0.rect(4, 4, w - 8, h - 8, BROWN_MID, outline=OUTLINE)
    c0.line(6, 6, w - 7, 6, WOOD_HIGHLIGHT)
    c0.line(6, 6, 6, h - 7, WOOD_HIGHLIGHT)
    c0.line(w - 7, 6, w - 7, h - 7, BROWN_DARK)
    c0.line(6, h - 7, w - 7, h - 7, BROWN_DARK)
    frames.append(c0)

    # Frame 1: Hover (Glowing golden lit)
    c1 = PixelCanvas(w, h, TRANSPARENT)
    c1.rect(4, 4, w - 8, h - 8, YELLOW_MID, outline=OUTLINE)
    c1.line(6, 6, w - 7, 6, PURE_WHITE)
    c1.line(6, 6, 6, h - 7, PURE_WHITE)
    c1.line(w - 7, 6, w - 7, h - 7, YELLOW_SHADOW)
    c1.line(6, h - 7, w - 7, h - 7, YELLOW_SHADOW)
    frames.append(c1)

    # Frame 2: Pressed (Depressed 2px into slot)
    c2 = PixelCanvas(w, h, TRANSPARENT)
    c2.rect(4, 6, w - 8, h - 8, WOOD_BLACK, outline=OUTLINE)
    c2.line(6, 8, w - 7, 8, BROWN_DARKEST)
    c2.line(6, 8, 6, h - 5, BROWN_DARKEST)
    c2.line(w - 7, 8, w - 7, h - 5, WOOD_HIGHLIGHT)
    c2.line(6, h - 5, w - 7, h - 5, WOOD_HIGHLIGHT)
    frames.append(c2)

    return frames


def generate_ui_banner_clear() -> List[PixelCanvas]:
    """384x96, 6 frames, 12 fps. Level clear celebration banner with confetti."""
    frames = []
    w, h = 384, 96
    confetti_colors = [RED_MID, BLUE_MID, YELLOW_MID, GREEN_MID, ORANGE_MID]

    for f in range(6):
        c = PixelCanvas(w, h, TRANSPARENT)
        # Gold banner unfurling
        c.polygon([
            (24, 20), (360, 20), (344, 76), (40, 76)
        ], YELLOW_MID, outline=OUTLINE)
        c.line(26, 22, 358, 22, PURE_WHITE)

        # Ribbon swallow-tail ends
        c.polygon([(10, 30), (28, 20), (40, 76), (18, 64)], YELLOW_SHADOW, outline=OUTLINE)
        c.polygon([(374, 30), (356, 20), (344, 76), (366, 64)], YELLOW_SHADOW, outline=OUTLINE)

        # Confetti burst around banner
        for i in range(16):
            ang = (i / 16.0) * 2 * math.pi
            r = 30 + f * 15
            cx = int(w // 2 + math.cos(ang) * (r * 2.2))
            cy = int(h // 2 + math.sin(ang) * r)
            if 0 <= cx < w and 0 <= cy < h:
                c.rect(cx - 2, cy - 2, 4, 4, confetti_colors[i % len(confetti_colors)], outline=OUTLINE)

        frames.append(c)
    return frames


def generate_ui_banner_grounded() -> List[PixelCanvas]:
    """384x96, 6 frames, 12 fps. Grounded stamp banner slamming down."""
    frames = []
    w, h = 384, 96

    for f in range(6):
        c = PixelCanvas(w, h, TRANSPARENT)
        y_slam = min(24, f * 8 if f < 4 else 24)

        # Heavy red wooden stamp banner
        c.rect(36, y_slam, 312, 48, RED_MID, outline=OUTLINE)
        c.line(38, y_slam + 2, 346, y_slam + 2, RED_LIGHT)
        c.line(38, y_slam + 45, 346, y_slam + 45, RED_SHADOW)

        # Impact dust puffs on frames 3..5
        if f >= 3:
            for px in [40, 90, 192, 290, 340]:
                c.circle(px, y_slam + 48, 4 + (f - 3) * 2, WHITE_SHADOW)
                c.circle(px, y_slam + 48, 2 + (f - 3), PURE_WHITE)

        frames.append(c)
    return frames


# ==============================================================================
# 4. BITMAP FONTS (10x14 & 6x9)
# ==============================================================================

# Standard 5x7 glyph definitions for base character forms
BASE_GLYPHS: Dict[str, List[str]] = {
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


def generate_font_pixel_10x14() -> Tuple[PixelCanvas, Dict]:
    """10x14 font, ASCII 32-126 in 16x6 grid -> 160x84 px. Plus json metrics."""
    w, h = 160, 84
    c = PixelCanvas(w, h, TRANSPARENT)
    metrics = {
        "cell_w": 10,
        "cell_h": 14,
        "columns": 16,
        "rows": 6,
        "chars": {}
    }

    for ascii_code in range(32, 127):
        idx = ascii_code - 32
        col = idx % 16
        row = idx // 16
        cell_x = col * 10
        cell_y = row * 14

        char = chr(ascii_code)
        # Scale 5x7 base glyph by 2x to fit 10x14 cell
        if char in BASE_GLYPHS:
            lines = BASE_GLYPHS[char]
            for py, line in enumerate(lines):
                for px, bit in enumerate(line):
                    if bit == '1':
                        c.rect(cell_x + px * 2, cell_y + py * 2, 2, 2, PURE_WHITE)

        metrics["chars"][char] = {
            "x": cell_x,
            "y": cell_y,
            "width": 10,
            "height": 14,
            "advance": 10
        }

    return c, metrics


def generate_font_pixel_small_6x9() -> PixelCanvas:
    """6x9 font, ASCII 32-126 in 16x6 grid -> 96x54 px."""
    w, h = 96, 54
    c = PixelCanvas(w, h, TRANSPARENT)

    for ascii_code in range(32, 127):
        idx = ascii_code - 32
        col = idx % 16
        row = idx // 16
        cell_x = col * 6
        cell_y = row * 9

        char = chr(ascii_code)
        if char in BASE_GLYPHS:
            lines = BASE_GLYPHS[char]
            for py, line in enumerate(lines):
                for px, bit in enumerate(line):
                    if bit == '1':
                        c.set_pixel(cell_x + px, cell_y + py + 1, PURE_WHITE)

    return c


# ==============================================================================
# MAIN GENERATION RUNNER
# ==============================================================================

def generate_all_ui_and_fx():
    print("--- Generating 2x Particles & FX (art/v2/) ---")
    assemble_strip(generate_fx_dust(), "art/v2/fx_dust.png")
    assemble_strip(generate_fx_jump_puff(), "art/v2/fx_jump_puff.png")
    assemble_strip(generate_fx_stars(), "art/v2/fx_stars.png")
    assemble_strip(generate_fx_impact(), "art/v2/fx_impact.png")
    assemble_strip(generate_fx_speedline(), "art/v2/fx_speedline.png")
    assemble_strip(generate_fx_sparkle(), "art/v2/fx_sparkle.png")

    bubble = generate_fx_bubble()
    bubble.to_image().save("art/v2/fx_bubble.png", "PNG")
    print("Saved art/v2/fx_bubble.png (192x48)")

    print("\n--- Generating New Particles (art/v2/) ---")
    assemble_strip(generate_fx_mote(), "art/v2/fx_mote.png")
    assemble_strip(generate_fx_fluff(), "art/v2/fx_fluff.png")
    assemble_strip(generate_fx_firefly(), "art/v2/fx_firefly.png")
    assemble_strip(generate_fx_steam(), "art/v2/fx_steam.png")
    assemble_strip(generate_fx_sweat(), "art/v2/fx_sweat.png")
    assemble_strip(generate_fx_heart(), "art/v2/fx_heart.png")
    assemble_strip(generate_fx_sleepz(), "art/v2/fx_sleepz.png")
    assemble_strip(generate_fx_shockwave(), "art/v2/fx_shockwave.png")
    assemble_strip(generate_fx_confetti(), "art/v2/fx_confetti.png")

    print("\n--- Generating Comic Text Pops (art/v2/) ---")
    assemble_strip(generate_fx_text_oof(), "art/v2/fx_text_oof.png")
    assemble_strip(generate_fx_text_yikes(), "art/v2/fx_text_yikes.png")
    assemble_strip(generate_fx_text_nice(), "art/v2/fx_text_nice.png")
    assemble_strip(generate_fx_text_whoops(), "art/v2/fx_text_whoops.png")

    print("\n--- Generating Light Overlays (art/v2/) ---")
    generate_light_window().save("art/v2/light_window.png", "PNG")
    print("Saved art/v2/light_window.png (384x540)")

    generate_light_lamp().save("art/v2/light_lamp.png", "PNG")
    print("Saved art/v2/light_lamp.png (256x256)")

    generate_light_vignette().save("art/v2/light_vignette.png", "PNG")
    print("Saved art/v2/light_vignette.png (960x540)")

    generate_light_godray_anim().save("art/v2/light_godray_anim.png", "PNG")
    print("Saved art/v2/light_godray_anim.png (2304x540, 6 frames)")

    print("\n--- Generating UI Life (art/v2/) ---")
    assemble_strip(generate_ui_trouble_pip(), "art/v2/ui_trouble_pip.png")
    assemble_strip(generate_ui_slot(), "art/v2/ui_slot.png")
    assemble_strip(generate_ui_cooldown_bar(), "art/v2/ui_cooldown_bar.png")

    generate_ui_keycap("1").to_image().save("art/v2/ui_key_1.png", "PNG")
    generate_ui_keycap("2").to_image().save("art/v2/ui_key_2.png", "PNG")
    generate_ui_keycap("3").to_image().save("art/v2/ui_key_3.png", "PNG")
    print("Saved art/v2/ui_key_1.png, ui_key_2.png, ui_key_3.png (20x20)")

    generate_ui_logo().to_image().save("art/v2/ui_logo.png", "PNG")
    print("Saved art/v2/ui_logo.png (384x144)")

    assemble_strip(generate_ui_button(), "art/v2/ui_button.png")
    assemble_strip(generate_ui_banner_clear(), "art/v2/ui_banner_clear.png")
    assemble_strip(generate_ui_banner_grounded(), "art/v2/ui_banner_grounded.png")

    print("\n--- Generating Bitmap Fonts (art/v2/) ---")
    font10, metrics = generate_font_pixel_10x14()
    font10.to_image().save("art/v2/font_pixel.png", "PNG")
    with open("art/v2/font_pixel.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print("Saved art/v2/font_pixel.png (160x84) and art/v2/font_pixel.json")

    font6 = generate_font_pixel_small_6x9()
    font6.to_image().save("art/v2/font_pixel_small.png", "PNG")
    print("Saved art/v2/font_pixel_small.png (96x54)")


if __name__ == "__main__":
    generate_all_ui_and_fx()
