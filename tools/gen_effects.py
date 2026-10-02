"""Younger Sibling Simulator - Effects Generator (1-bit style white on transparent)."""

import math
from typing import List, Tuple
from canvas import PixelCanvas, assemble_strip
from palette import TRANSPARENT, PURE_WHITE

WHITE = PURE_WHITE


def generate_fx_dust() -> List[PixelCanvas]:
    """16x16, 6 frames, fps 20. Crisp landing & skid dust puff."""
    frames = []

    # Frame 0: Instant impact birth - squashed energetic puff hugging ground (y=13..15)
    c0 = PixelCanvas(16, 16, TRANSPARENT)
    # Ground contact pad
    c0.line(4, 14, 11, 14, WHITE)
    c0.line(5, 13, 10, 13, WHITE)
    c0.line(6, 12, 9, 12, WHITE)
    # Ejecta specks flinging outward
    c0.set_pixel(2, 14, WHITE)
    c0.set_pixel(13, 14, WHITE)
    frames.append(c0)

    # Frame 1: Expanding dual billowing lobes pushing left & right
    c1 = PixelCanvas(16, 16, TRANSPARENT)
    # Left billow
    c1.circle(4, 11, 3, WHITE)
    # Right billow
    c1.circle(11, 11, 3, WHITE)
    # Connecting bottom fill
    c1.rect(4, 12, 8, 3, WHITE)
    # Top central notch between lobes
    c1.set_pixel(7, 9, TRANSPARENT)
    c1.set_pixel(8, 9, TRANSPARENT)
    # Little flying pebbles
    c1.set_pixel(1, 12, WHITE)
    c1.set_pixel(14, 12, WHITE)
    frames.append(c1)

    # Frame 2: Peak poof & curly volume with hollowed core
    c2 = PixelCanvas(16, 16, TRANSPARENT)
    # Left expanding cloud
    c2.circle(3, 9, 3, WHITE)
    c2.circle(5, 8, 2, WHITE)
    # Right expanding cloud
    c2.circle(12, 9, 3, WHITE)
    c2.circle(10, 8, 2, WHITE)
    # Hollow center blowout where foot pressed
    c2.rect(6, 9, 4, 4, TRANSPARENT)
    # Trailing base wisps
    c2.line(2, 13, 5, 13, WHITE)
    c2.line(10, 13, 13, 13, WHITE)
    # Air sparks
    c2.set_pixel(4, 5, WHITE)
    c2.set_pixel(11, 5, WHITE)
    frames.append(c2)

    # Frame 3: Splitting into distinct flying cloudlets
    c3 = PixelCanvas(16, 16, TRANSPARENT)
    # Left detached clumps
    c3.rect(1, 7, 3, 3, WHITE)
    c3.set_pixel(1, 7, TRANSPARENT)
    c3.rect(3, 5, 2, 2, WHITE)
    # Right detached clumps
    c3.rect(12, 7, 3, 3, WHITE)
    c3.set_pixel(14, 7, TRANSPARENT)
    c3.rect(11, 5, 2, 2, WHITE)
    # Ground dust specks
    c3.set_pixel(0, 10, WHITE)
    c3.set_pixel(15, 10, WHITE)
    c3.set_pixel(5, 12, WHITE)
    c3.set_pixel(10, 12, WHITE)
    frames.append(c3)

    # Frame 4: Dispersing wisp particles
    c4 = PixelCanvas(16, 16, TRANSPARENT)
    for x, y in [(1, 6), (2, 5), (4, 4), (11, 4), (13, 5), (14, 6), (7, 6)]:
        c4.set_pixel(x, y, WHITE)
    c4.set_pixel(0, 9, WHITE)
    c4.set_pixel(15, 9, WHITE)
    frames.append(c4)

    # Frame 5: Fading specks
    c5 = PixelCanvas(16, 16, TRANSPARENT)
    for x, y in [(0, 5), (3, 3), (12, 3), (15, 5), (8, 5)]:
        c5.set_pixel(x, y, WHITE)
    frames.append(c5)

    return frames


def generate_fx_jump_puff() -> List[PixelCanvas]:
    """16x16, 5 frames, fps 24. Downward launch cloud burst."""
    frames = []

    # Frame 0: Launch snap - compressed high-energy shock pad (y=3..6)
    c0 = PixelCanvas(16, 16, TRANSPARENT)
    c0.rect(4, 3, 8, 3, WHITE)
    c0.line(2, 4, 13, 4, WHITE)
    c0.line(5, 6, 10, 6, WHITE)
    frames.append(c0)

    # Frame 1: Downward surging mushroom burst
    c1 = PixelCanvas(16, 16, TRANSPARENT)
    # Central dome
    c1.circle(8, 6, 4, WHITE)
    # Downward thrust lobes
    c1.rect(5, 8, 6, 3, WHITE)
    c1.set_pixel(4, 10, WHITE)
    c1.set_pixel(11, 10, WHITE)
    c1.line(6, 11, 9, 11, WHITE)
    # Side escape puffs
    c1.set_pixel(2, 6, WHITE)
    c1.set_pixel(13, 6, WHITE)
    frames.append(c1)

    # Frame 2: Hollow shockwave ring blowout expanding downward
    c2 = PixelCanvas(16, 16, TRANSPARENT)
    # Outer expanding oval ring
    for y in range(3, 15):
        for x in range(1, 15):
            dx = (x - 7.5) / 6.0
            dy = (y - 8.5) / 5.0
            d_sq = dx * dx + dy * dy
            if 0.55 <= d_sq <= 1.05:
                c2.set_pixel(x, y, WHITE)
    frames.append(c2)

    # Frame 3: Shockwave ring shattering into droplets
    c3 = PixelCanvas(16, 16, TRANSPARENT)
    droplets = [
        (2, 4), (3, 4), (12, 4), (13, 4),  # top-side
        (1, 8), (2, 8), (13, 8), (14, 8),  # mid-side
        (3, 12), (4, 13), (11, 13), (12, 12),  # bottom-side
        (7, 14), (8, 14), (8, 15),  # bottom jet
    ]
    for x, y in droplets:
        c3.set_pixel(x, y, WHITE)
    frames.append(c3)

    # Frame 4: Tiny dissipating specks
    c4 = PixelCanvas(16, 16, TRANSPARENT)
    for x, y in [(0, 3), (15, 3), (0, 9), (15, 9), (2, 14), (13, 14), (8, 15)]:
        c4.set_pixel(x, y, WHITE)
    frames.append(c4)

    return frames


def generate_fx_stars() -> List[PixelCanvas]:
    """
    24x24, 8 frames, fps 16, loop: true.
    3 circling dizzy stars on ellipse with depth perspective.
    """
    frames = []
    cx, cy = 11.5, 11.0
    rx, ry = 8.5, 3.8

    # Glyph definitions
    # Foreground 5x5 cartoon diamond star
    star_fg = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
    ]
    # Midground 3x3 star
    star_mid = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]

    for f in range(8):
        c = PixelCanvas(24, 24, TRANSPARENT)
        base_angle = (f / 8.0) * 2.0 * math.pi

        star_data = []
        for s in range(3):
            angle = base_angle + s * (2.0 * math.pi / 3.0)
            sx = cx + math.cos(angle) * rx
            sy = cy + math.sin(angle) * ry
            depth = math.sin(angle)  # -1.0 (back) to +1.0 (front)
            star_data.append((depth, angle, sx, sy))

        # Sort back to front so foreground stars draw on top
        star_data.sort(key=lambda item: item[0])

        for depth, angle, sx, sy in star_data:
            ix = int(round(sx))
            iy = int(round(sy))

            # Motion trail glint for spinning stars
            trail_ang = angle - 0.38
            tx = int(round(cx + math.cos(trail_ang) * rx))
            ty = int(round(cy + math.sin(trail_ang) * ry))

            if depth > 0.3:
                # Foreground: Large 5x5 star
                for dy in range(5):
                    for dx in range(5):
                        if star_fg[dy][dx]:
                            c.set_pixel(ix - 2 + dx, iy - 2 + dy, WHITE)
                # Trailing glint
                c.set_pixel(tx, ty, WHITE)
            elif depth > -0.35:
                # Midground: 3x3 diamond star
                for dy in range(3):
                    for dx in range(3):
                        if star_mid[dy][dx]:
                            c.set_pixel(ix - 1 + dx, iy - 1 + dy, WHITE)
                c.set_pixel(tx, ty, WHITE)
            else:
                # Background: Small 1-2px twinkle speck
                c.set_pixel(ix, iy, WHITE)
                if depth > -0.65:
                    c.set_pixel(ix + 1, iy, WHITE)

        frames.append(c)

    return frames


def generate_fx_impact() -> List[PixelCanvas]:
    """32x32, 5 frames, fps 30. Comic 'bang' starburst for hitstop frames."""
    frames = []
    cx, cy = 15.5, 15.5

    # Frame 0: Flash core with 4 piercing primary needle rays
    c0 = PixelCanvas(32, 32, TRANSPARENT)
    # Bright center diamond
    for y in range(12, 20):
        for x in range(12, 20):
            if abs(x - cx) + abs(y - cy) <= 4.5:
                c0.set_pixel(x, y, WHITE)
    # Sharp primary cross spikes
    c0.line(15, 3, 16, 3, WHITE)
    c0.rect(15, 4, 2, 24, WHITE)
    c0.line(3, 15, 3, 16, WHITE)
    c0.rect(4, 15, 24, 2, WHITE)
    # Secondary diagonal spikes
    for d in range(4, 9):
        c0.set_pixel(int(cx + d), int(cy + d), WHITE)
        c0.set_pixel(int(cx - d), int(cy + d), WHITE)
        c0.set_pixel(int(cx + d), int(cy - d), WHITE)
        c0.set_pixel(int(cx - d), int(cy - d), WHITE)
    frames.append(c0)

    # Frame 1: Full comic 'BANG' starburst (jagged alternating spikes)
    c1 = PixelCanvas(32, 32, TRANSPARENT)
    # 16-point starburst
    num_pts = 16
    radii = [15.0 if i % 2 == 0 else 7.5 for i in range(num_pts)]
    angles = [i * (2.0 * math.pi / num_pts) for i in range(num_pts)]
    coords = []
    for r, a in zip(radii, angles):
        px = cx + math.cos(a) * r
        py = cy + math.sin(a) * r
        coords.append((px, py))

    # Fill starburst polygon using ray-triangle filling
    for y in range(32):
        for x in range(32):
            dx = x - cx
            dy = y - cy
            dist = math.hypot(dx, dy)
            if dist < 0.5:
                c1.set_pixel(x, y, WHITE)
                continue
            ang = math.atan2(dy, dx)
            if ang < 0:
                ang += 2.0 * math.pi
            # Find which two points bracket this angle
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

    # Detached action wedge flecks around outer tips
    for a in angles[::2]:
        fx = int(round(cx + math.cos(a) * 15.5))
        fy = int(round(cy + math.sin(a) * 15.5))
        c1.set_pixel(fx, fy, WHITE)
    frames.append(c1)

    # Frame 2: Starburst center blows open, spikes fly outward as jagged comic shards
    c2 = PixelCanvas(32, 32, TRANSPARENT)
    # Hollow center ring
    for y in range(32):
        for x in range(32):
            dx = x - cx
            dy = y - cy
            dist = math.hypot(dx, dy)
            if dist < 6.5:
                continue  # Hollow center
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
            max_r = (1.0 - t) * (radii[idx] + 1.0) + t * (radii[next_idx] + 1.0)
            if dist <= max_r and (idx % 2 == 0 or dist >= 8.0):
                c2.set_pixel(x, y, WHITE)

    # Flying sharp diamond shards
    for a in angles[::2]:
        sx = int(round(cx + math.cos(a) * 15.0))
        sy = int(round(cy + math.sin(a) * 15.0))
        c2.set_pixel(sx, sy, WHITE)
    frames.append(c2)

    # Frame 3: Shattered flying debris & spark flecks
    c3 = PixelCanvas(32, 32, TRANSPARENT)
    for a in angles:
        r = 14.5
        sx = int(round(cx + math.cos(a) * r))
        sy = int(round(cy + math.sin(a) * r))
        if 0 <= sx < 32 and 0 <= sy < 32:
            c3.set_pixel(sx, sy, WHITE)
            if (int(round(a * 10)) % 2 == 0) and 0 <= sx + 1 < 32:
                c3.set_pixel(sx + 1, sy, WHITE)
    frames.append(c3)

    # Frame 4: Dissipating specks at outer perimeter
    c4 = PixelCanvas(32, 32, TRANSPARENT)
    for a in angles[::2]:
        r = 15.5
        sx = int(round(cx + math.cos(a) * r))
        sy = int(round(cy + math.sin(a) * r))
        if 0 <= sx < 32 and 0 <= sy < 32:
            c4.set_pixel(sx, sy, WHITE)
    frames.append(c4)

    return frames


def generate_fx_speedline() -> List[PixelCanvas]:
    """24x8, 4 frames, fps 30. Horizontal speedlines."""
    frames = []

    # Frame 0: Quick sharp burst of speed streaks born at right (x=12..23)
    c0 = PixelCanvas(24, 8, TRANSPARENT)
    c0.line(14, 1, 22, 1, WHITE)
    c0.line(11, 4, 23, 4, WHITE)
    c0.line(18, 5, 23, 5, WHITE)  # 2px head
    c0.line(16, 6, 21, 6, WHITE)
    frames.append(c0)

    # Frame 1: Full-length piercing streaks streaking across the frame
    c1 = PixelCanvas(24, 8, TRANSPARENT)
    c1.line(6, 1, 20, 1, WHITE)
    c1.line(2, 3, 22, 3, WHITE)
    c1.set_pixel(15, 3, TRANSPARENT)  # speed dash break
    c1.line(7, 5, 19, 5, WHITE)
    c1.line(3, 6, 16, 6, WHITE)
    frames.append(c1)

    # Frame 2: Streaks flashing leftward
    c2 = PixelCanvas(24, 8, TRANSPARENT)
    c2.line(1, 2, 14, 2, WHITE)
    c2.line(0, 4, 12, 4, WHITE)
    c2.line(2, 6, 10, 6, WHITE)
    frames.append(c2)

    # Frame 3: Dissipating exit wisps
    c3 = PixelCanvas(24, 8, TRANSPARENT)
    c3.line(0, 2, 5, 2, WHITE)
    c3.line(0, 4, 3, 4, WHITE)
    c3.line(0, 6, 4, 6, WHITE)
    frames.append(c3)

    return frames


def generate_fx_sparkle() -> List[PixelCanvas]:
    """8x8, 5 frames, fps 16. 4-point twinkle sparkle."""
    frames = []

    # Frame 0: Tiny nascent glint (2x2 center)
    c0 = PixelCanvas(8, 8, TRANSPARENT)
    c0.set_pixel(3, 3, WHITE)
    c0.set_pixel(4, 4, WHITE)
    frames.append(c0)

    # Frame 1: 4x4 plus cross
    c1 = PixelCanvas(8, 8, TRANSPARENT)
    c1.line(3, 2, 4, 2, WHITE)
    c1.line(3, 5, 4, 5, WHITE)
    c1.rect(2, 3, 4, 2, WHITE)
    frames.append(c1)

    # Frame 2: Max brilliance 4-point cartoon twinkle sparkle
    c2 = PixelCanvas(8, 8, TRANSPARENT)
    # Vertical needle
    c2.line(3, 0, 4, 0, WHITE)
    c2.rect(3, 1, 2, 6, WHITE)
    c2.line(3, 7, 4, 7, WHITE)
    # Horizontal needle
    c2.line(0, 3, 0, 4, WHITE)
    c2.rect(1, 3, 6, 2, WHITE)
    c2.line(7, 3, 7, 4, WHITE)
    # Diagonal diamond fill
    for dx, dy in [(2, 2), (5, 2), (2, 5), (5, 5)]:
        c2.set_pixel(dx, dy, WHITE)
    frames.append(c2)

    # Frame 3: Contracting X-cross twinkle
    c3 = PixelCanvas(8, 8, TRANSPARENT)
    # Center diamond
    c3.rect(3, 3, 2, 2, WHITE)
    # 4 corner detached sparks
    for dx, dy in [(1, 1), (6, 1), (1, 6), (6, 6)]:
        c3.set_pixel(dx, dy, WHITE)
    frames.append(c3)

    # Frame 4: 4 tiny corner specks fading out
    c4 = PixelCanvas(8, 8, TRANSPARENT)
    for dx, dy in [(0, 0), (7, 0), (0, 7), (7, 7)]:
        c4.set_pixel(dx, dy, WHITE)
    frames.append(c4)

    return frames


def generate_fx_bubble() -> PixelCanvas:
    """
    96x24 speech bubble 9-slice with tail at bottom-center and 6px rounded corners.
    1-bit white on transparent.
    Body: 96x18 (y=0..17), tail: y=18..23.
    """
    c = PixelCanvas(96, 24, TRANSPARENT)
    w, h = 96, 18
    r = 6

    # Fill rounded rectangle body (y=0..17) with exact 6px corner cutouts
    # Corner offsets for radius 6
    cutouts = [5, 3, 2, 1, 1, 0]
    for y in range(h):
        cut = 0
        if y < r:
            cut = cutouts[y]
        elif y >= h - r:
            cut = cutouts[h - 1 - y]

        for x in range(cut, w - cut):
            c.set_pixel(x, y, WHITE)

    # Speech tail at bottom center (x=42..54, y=18..23) tapering downward
    tail_spans = [
        (18, 42, 54),  # width 13
        (19, 43, 53),  # width 11
        (20, 44, 52),  # width 9
        (21, 45, 51),  # width 7
        (22, 46, 50),  # width 5
        (23, 47, 49),  # width 3 with center point
    ]
    for y, x0, x1 in tail_spans:
        c.line(x0, y, x1, y, WHITE)

    return c


def generate_all_effects():
    assemble_strip(generate_fx_dust(), "art/incoming/fx_dust.png")
    assemble_strip(generate_fx_jump_puff(), "art/incoming/fx_jump_puff.png")
    assemble_strip(generate_fx_stars(), "art/incoming/fx_stars.png")
    assemble_strip(generate_fx_impact(), "art/incoming/fx_impact.png")
    assemble_strip(generate_fx_speedline(), "art/incoming/fx_speedline.png")
    assemble_strip(generate_fx_sparkle(), "art/incoming/fx_sparkle.png")

    bubble = generate_fx_bubble()
    bubble.to_image().save("art/incoming/fx_bubble.png", "PNG")
    print(f"Saved art/incoming/fx_bubble.png ({bubble.width}x{bubble.height})")


if __name__ == "__main__":
    generate_all_effects()
