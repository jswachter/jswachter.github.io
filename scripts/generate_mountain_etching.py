"""Trace selected landscape boundaries in the homepage's mountain photograph.

Run: python3 scripts/generate_mountain_etching.py
Requires Pillow, NumPy, and SciPy. The guides below are specific to the original
800 × 800 photo: they identify meaningful features, then image contrast locates
their contours. Source pixels are never resized, cropped, or geometrically warped.
"""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage


# These are search corridors, not the final drawn lines. Keeping them specific to
# this scene avoids mistaking isolated snow patches for major landscape features.
SKYLINE = [
    (0, 197), (80, 200), (110, 188), (150, 175), (180, 179), (210, 186),
    (240, 178), (263, 168), (280, 169), (316, 148), (330, 134), (360, 131),
    (390, 131), (410, 123), (450, 131), (465, 142), (489, 118), (510, 105),
    (535, 91), (551, 78), (570, 83), (580, 73), (600, 92), (619, 88),
    (642, 109), (664, 134), (682, 96), (700, 99), (720, 93), (749, 93),
    (767, 105), (789, 81), (799, 80),
]
SHORELINE = [
    (0, 563), (20, 559), (35, 548), (60, 539), (90, 532), (120, 520),
    (155, 509), (200, 502), (250, 495), (300, 491), (350, 488), (400, 490),
    (450, 494), (500, 502), (550, 507), (600, 513), (650, 517), (700, 522),
    (750, 527), (799, 536),
]
REFLECTION = [
    (0, 638), (35, 623), (70, 617), (100, 610), (130, 605), (150, 617),
    (180, 611), (200, 616), (230, 618), (270, 635), (290, 631), (320, 642),
    (338, 657), (370, 658), (410, 665), (445, 660), (479, 653), (500, 659),
    (530, 684), (560, 704), (580, 715), (600, 717), (618, 701), (630, 713),
    (650, 699), (675, 680), (690, 697), (710, 728), (745, 727), (770, 733),
    (799, 719),
]

# Each entry names a visible ridge, its guide, and whether to follow it down the
# image instead of across. These sparse lines describe the terrain's large planes.
RIDGES = [
    ("left slope", False, [
        (0, 199), (55, 210), (100, 218), (150, 237), (195, 253), (220, 262),
    ]),
    ("middle ridge", False, [
        (0, 274), (60, 278), (110, 276), (160, 274), (200, 270),
        (245, 255), (285, 245), (325, 244), (365, 251), (410, 251),
        (454, 261), (500, 263),
    ]),
    ("near ridge", False, [
        (0, 356), (55, 351), (95, 363), (130, 374), (164, 386),
        (197, 388), (230, 412), (266, 432), (305, 447), (350, 472), (374, 482),
    ]),
    ("right bank", False, [
        (340, 345), (382, 346), (421, 358), (453, 382), (488, 390),
        (532, 403), (584, 398), (625, 395), (680, 404), (735, 418), (799, 433),
    ]),
    ("central peak", True, [
        (594, 91), (602, 122), (595, 157), (585, 180), (570, 203),
        (548, 225), (520, 244), (503, 259),
    ]),
    ("right peak", True, [
        (683, 100), (671, 133), (663, 159), (653, 192), (656, 216),
        (678, 239), (702, 259), (735, 272),
    ]),
    ("middle slope", True, [
        (325, 245), (303, 268), (273, 290), (246, 313), (211, 339),
    ]),
    ("left cliff", True, [
        (0, 392), (23, 423), (43, 460), (57, 494), (63, 521), (63, 540),
    ]),
]


def trace_boundary(field, guide, radius=10, sigma=2.6, polarity=0,
                   vertical=False, water_onset=False, anchor_start=False):
    """Find a continuous, low-cost path through local image contrast.

    A narrow corridor selects the feature; the source image determines its exact
    position. Continuity connects weak sections without lowering an edge threshold
    across the whole photograph and bringing back surface texture.
    """
    guide = np.asarray(guide, dtype=float)
    if vertical:
        field = field.T
        guide = guide[:, ::-1]
    guide = guide[np.argsort(guide[:, 0])]
    xs = np.arange(int(guide[0, 0]), int(guide[-1, 0]) + 1)
    baseline = np.interp(xs, guide[:, 0], guide[:, 1])
    offsets = np.arange(-radius, radius + 1)
    yy = baseline[:, None] + offsets
    xx = np.broadcast_to(xs[:, None], yy.shape)

    smooth = ndimage.gaussian_filter(field, sigma)
    gx = ndimage.sobel(smooth, axis=1) / 8
    gy = ndimage.sobel(smooth, axis=0) / 8
    horizontal = ndimage.map_coordinates(gx, [yy, xx], order=1, mode="nearest")
    vertical_gradient = ndimage.map_coordinates(gy, [yy, xx], order=1, mode="nearest")
    slope = np.gradient(baseline)[:, None]
    contrast = (vertical_gradient - slope * horizontal) / np.sqrt(1 + slope ** 2)
    strength = np.maximum(polarity * contrast, 0) if polarity else abs(contrast)

    if water_onset:
        # Follow the first change from neutral land into blue-green water, rather
        # than the stronger colour changes farther down inside the reflection.
        chroma = ndimage.map_coordinates(smooth, [yy, xx], order=1, mode="nearest")
        strength *= 1 / (1 + np.exp(np.clip((chroma - 0.055) * 65, -40, 40)))

    strength /= np.maximum(strength.max(axis=1, keepdims=True), 0.002)
    cost = -strength + 0.06 * (offsets[None, :] / radius) ** 2
    transitions = 0.10 * (offsets[:, None] - offsets[None, :]) ** 2
    back = np.zeros_like(cost, dtype=int)
    totals = cost[0].copy()
    if anchor_start:
        totals[offsets != 0] = np.inf
    for i in range(1, len(xs)):
        choices = totals[:, None] + transitions
        back[i] = choices.argmin(axis=0)
        totals = cost[i] + choices.min(axis=0)

    path = np.empty(len(xs), dtype=int)
    path[-1] = totals.argmin()
    for i in range(len(xs) - 1, 0, -1):
        path[i - 1] = back[i, path[i]]
    ys = ndimage.gaussian_filter1d(baseline + offsets[path], 0.65)
    if anchor_start:
        ys[0] = baseline[0]
    points = np.column_stack([xs, ys])
    return points[:, ::-1] if vertical else points


def landscape_paths(source):
    if source.size != (800, 800):
        raise ValueError("The contour guides require the original 800 × 800 photograph.")
    rgb = np.asarray(source.convert("RGB"), dtype=float) / 255
    luminance = rgb @ [0.2126, 0.7152, 0.0722]
    water = (rgb[:, :, 1] + rgb[:, :, 2] - 2 * rgb[:, :, 0]) / (rgb.sum(axis=2) + 0.05)
    paths = [
        ("skyline", trace_boundary(luminance, SKYLINE, radius=9, sigma=1.4, polarity=-1)),
        ("shoreline", trace_boundary(water, SHORELINE, radius=8, sigma=1.6,
                                     polarity=1, water_onset=True)),
        ("reflection", trace_boundary(luminance, REFLECTION, sigma=1.4, polarity=1)),
    ]
    for name, vertical, guide in RIDGES:
        paths.append((name, trace_boundary(luminance, guide, vertical=vertical)))

    reflected_slope = trace_boundary(luminance, [
        (250, 604), (300, 608), (350, 601), (400, 591), (450, 582),
        (480, 578), (510, 595), (540, 605), (570, 618), (600, 631),
    ], radius=8, sigma=2.8)
    # Join the reflected face to the measured slope, rather than leave an
    # arbitrary gap where two independently traced sections meet.
    join = reflected_slope[-1].copy()
    join[1] = round(join[1])
    reflected_slope[-1] = join
    paths.extend([
        ("reflected slope", reflected_slope),
        ("reflected peak", trace_boundary(luminance, [
            join, (606, 650), (606, 678), (615, 699), (618, 710),
        ], radius=7, sigma=2.2, vertical=True, anchor_start=True)),
    ])
    return paths


def make_etching(source, paths):
    # Supersample only the strokes, not the source image. Preserve the 800 × 800
    # alignment while making fine lines readable at the homepage's 200 px size.
    scale = 3
    canvas = Image.new("L", (source.width * scale, source.height * scale), 255)
    draw = ImageDraw.Draw(canvas)
    for name, points in paths:
        primary = name in ("skyline", "shoreline")
        width = 5 if primary else (4 if name == "reflection" else 3)
        draw.line([tuple(p * scale) for p in points], fill=35 if primary else 65, width=width)
    return canvas.resize(source.size, Image.Resampling.LANCZOS)


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", type=Path, default=root / "images/home-mountain-left-square.png"
    )
    parser.add_argument(
        "--output", type=Path, default=root / "images/home-mountain-etching.webp"
    )
    parser.add_argument("--overlay", type=Path, help="Save a contour overlay for checking alignment.")
    args = parser.parse_args()
    with Image.open(args.source) as source:
        paths = landscape_paths(source)
        result = make_etching(source, paths)
        if args.overlay:
            overlay = source.convert("RGB")
            draw = ImageDraw.Draw(overlay)
            for name, points in paths:
                draw.line([tuple(p) for p in points],
                          fill="#e84094" if name == "shoreline" else "#e74736", width=2)
            overlay.save(args.overlay)
    result.save(args.output, format="WEBP", lossless=True, method=6)
    print(f"Saved {args.output} ({result.width} × {result.height})")


if __name__ == "__main__":
    main()
