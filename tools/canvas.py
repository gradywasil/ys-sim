"""Pixel canvas utility for crisp, palette-accurate pixel art generation."""

import math
from typing import Tuple, List, Optional
from PIL import Image
from palette import TRANSPARENT, OUTLINE, VALID_PALETTE_RGBA

RGBA = Tuple[int, int, int, int]

class PixelCanvas:
    def __init__(self, width: int, height: int, bg: RGBA = TRANSPARENT):
        self.width = width
        self.height = height
        self.pixels: List[List[RGBA]] = [[bg for _ in range(width)] for _ in range(height)]

    def set_pixel(self, x: int, y: int, color: RGBA):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = color

    def get_pixel(self, x: int, y: int) -> RGBA:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return TRANSPARENT

    def rect(self, x: int, y: int, w: int, h: int, fill: RGBA, outline: Optional[RGBA] = None):
        for cy in range(y, y + h):
            for cx in range(x, x + w):
                if 0 <= cx < self.width and 0 <= cy < self.height:
                    is_edge = (cx == x or cx == x + w - 1 or cy == y or cy == y + h - 1)
                    if is_edge and outline is not None:
                        self.pixels[cy][cx] = outline
                    else:
                        self.pixels[cy][cx] = fill

    def line(self, x0: int, y0: int, x1: int, y1: int, color: RGBA):
        # Bresenham's line algorithm
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        cx, cy = x0, y0
        while True:
            self.set_pixel(cx, cy, color)
            if cx == x1 and cy == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                cx += sx
            if e2 <= dx:
                err += dx
                cy += sy

    def circle(self, cx: int, cy: int, r: int, fill: RGBA, outline: Optional[RGBA] = None):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                d_sq = (x - cx) ** 2 + (y - cy) ** 2
                if d_sq <= r * r:
                    if outline is not None and (x - cx) ** 2 + (y - cy) ** 2 > (r - 1.2) ** 2:
                        self.set_pixel(x, y, outline)
                    else:
                        self.set_pixel(x, y, fill)

    def polygon(self, points: List[Tuple[int, int]], fill: RGBA, outline: Optional[RGBA] = None):
        """Fills a polygon using scanline rasterization."""
        if len(points) < 3:
            return
        min_y = max(0, min(p[1] for p in points))
        max_y = min(self.height - 1, max(p[1] for p in points))
        
        for y in range(min_y, max_y + 1):
            nodes = []
            j = len(points) - 1
            for i in range(len(points)):
                p1 = points[i]
                p2 = points[j]
                if (p1[1] < y <= p2[1]) or (p2[1] < y <= p1[1]):
                    x = p1[0] + (y - p1[1]) / (p2[1] - p1[1]) * (p2[0] - p1[0])
                    nodes.append(x)
                j = i
            nodes.sort()
            for k in range(0, len(nodes) - 1, 2):
                x_start = max(0, int(math.ceil(nodes[k])))
                x_end = min(self.width - 1, int(math.floor(nodes[k+1])))
                for x in range(x_start, x_end + 1):
                    self.set_pixel(x, y, fill)
                    
        if outline is not None:
            for i in range(len(points)):
                p1 = points[i]
                p2 = points[(i + 1) % len(points)]
                self.line(p1[0], p1[1], p2[0], p2[1], outline)

    def blit(self, src: 'PixelCanvas', dx: int, dy: int, ignore_transparent: bool = True):
        for sy in range(src.height):
            for sx in range(src.width):
                px = src.get_pixel(sx, sy)
                if ignore_transparent and px[3] == 0:
                    continue
                self.set_pixel(dx + sx, dy + sy, px)

    def clone(self) -> 'PixelCanvas':
        c = PixelCanvas(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                c.pixels[y][x] = self.pixels[y][x]
        return c

    def flip_h(self) -> 'PixelCanvas':
        c = PixelCanvas(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                c.pixels[y][x] = self.pixels[y][self.width - 1 - x]
        return c

    def apply_selective_outline(self, outline_color: RGBA = OUTLINE,
                                 light_rim: Optional[RGBA] = None,
                                 dark_rim: Optional[RGBA] = None):
        """Adds a 1px border around opaque shapes, with light rim on top-left and dark rim on bottom-right."""
        original = self.clone()
        for y in range(self.height):
            for x in range(self.width):
                if original.get_pixel(x, y)[3] != 0:
                    continue  # already opaque
                
                # Check neighbors
                n_up = original.get_pixel(x, y - 1)[3] != 0
                n_down = original.get_pixel(x, y + 1)[3] != 0
                n_left = original.get_pixel(x - 1, y)[3] != 0
                n_right = original.get_pixel(x + 1, y)[3] != 0
                
                if n_up or n_down or n_left or n_right:
                    # Neighboring an opaque pixel
                    if light_rim and (n_down or n_right) and not (n_up or n_left):
                        self.set_pixel(x, y, light_rim)
                    elif dark_rim and (n_up or n_left) and not (n_down or n_right):
                        self.set_pixel(x, y, dark_rim)
                    else:
                        self.set_pixel(x, y, outline_color)

    def to_image(self) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height))
        flat_data = [self.pixels[y][x] for y in range(self.height) for x in range(self.width)]
        img.putdata(flat_data)
        return img

def generate_normal_map(canvas: PixelCanvas, strength: float = 2.0) -> PixelCanvas:
    """Generates an OpenGL tangent-space normal map (Godot 2D compatible) from height."""
    w, h = canvas.width, canvas.height
    norm = PixelCanvas(w, h, TRANSPARENT)
    
    # Compute height from luminance and alpha distance
    heights = [[0.0 for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b, a = canvas.get_pixel(x, y)
            if a > 0:
                lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
                heights[y][x] = lum
            else:
                heights[y][x] = 0.0

    for y in range(h):
        for x in range(w):
            if canvas.get_pixel(x, y)[3] == 0:
                continue
            
            # Sobel filter or central difference
            xl = heights[y][x - 1] if x > 0 else heights[y][x]
            xr = heights[y][x + 1] if x < w - 1 else heights[y][x]
            yt = heights[y - 1][x] if y > 0 else heights[y][x]
            yb = heights[y + 1][x] if y < h - 1 else heights[y][x]
            
            dx = (xr - xl) * strength
            dy = (yb - yt) * strength  # Godot 2D normal maps: +Y is down
            dz = 1.0
            
            length = math.sqrt(dx * dx + dy * dy + dz * dz)
            nx = dx / length
            ny = dy / length
            nz = dz / length
            
            # Map [-1, 1] to [0, 255]
            nr = int((nx * 0.5 + 0.5) * 255)
            ng = int((ny * 0.5 + 0.5) * 255)
            nb = int((nz * 0.5 + 0.5) * 255)
            norm.set_pixel(x, y, (nr, ng, nb, 255))
            
    return norm

def assemble_strip(frames: List[PixelCanvas], output_path: str):
    if not frames:
        raise ValueError("Frames list cannot be empty")
    fw = frames[0].width
    fh = frames[0].height
    num_frames = len(frames)
    strip = Image.new("RGBA", (fw * num_frames, fh))
    for i, f in enumerate(frames):
        img_f = f.to_image()
        strip.paste(img_f, (i * fw, 0))
    strip.save(output_path, "PNG")
    print(f"Saved {output_path} ({strip.width}x{strip.height}, {num_frames} frames)")
