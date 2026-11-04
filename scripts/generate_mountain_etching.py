"""Trace the photograph's main contours at their original pixel coordinates.

Run: python3 scripts/generate_mountain_etching.py
Requires Pillow, NumPy, and SciPy. No resizing, cropping, or geometric warping.
"""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def make_etching(source):
    rgb = np.asarray(source.convert("RGB"), dtype=np.float32) / 255
    luminance = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    y, x = np.indices(luminance.shape, dtype=np.float32)
    # Suppress rock/snow texture before tracing the main landscape boundaries.
    smooth = ndimage.gaussian_filter(luminance, 3.6)

    # Trace local contrast ridges, thinning them along the gradient direction.
    gx = ndimage.sobel(smooth, axis=1) / 8
    gy = ndimage.sobel(smooth, axis=0) / 8
    magnitude = np.hypot(gx, gy)
    dx = gx / (magnitude + 1e-6)
    dy = gy / (magnitude + 1e-6)
    before = ndimage.map_coordinates(
        magnitude, [y - dy, x - dx], order=1, mode="nearest"
    )
    after = ndimage.map_coordinates(
        magnitude, [y + dy, x + dx], order=1, mode="nearest"
    )
    ridges = (magnitude >= before) & (magnitude >= after)
    edges = ndimage.binary_propagation(
        ridges & (magnitude > 0.045),
        structure=np.ones((3, 3)),
        mask=ridges & (magnitude > 0.018),
    )
    labels, _ = ndimage.label(edges, structure=np.ones((3, 3)))
    sizes = np.bincount(labels.ravel())
    edges &= sizes[labels] >= 70

    # Keep a light, antialiased stroke with no hatching, texture, or tonal fill.
    ink = np.clip(ndimage.gaussian_filter(edges.astype(float), 0.45) * 1.4, 0, 1) * 0.90
    return Image.fromarray(np.uint8(np.clip(1 - ink, 0, 1) * 255))


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", type=Path, default=root / "images/home-mountain-left-square.png"
    )
    parser.add_argument(
        "--output", type=Path, default=root / "images/home-mountain-etching.webp"
    )
    args = parser.parse_args()
    with Image.open(args.source) as source:
        result = make_etching(source)
    result.save(args.output, format="WEBP", lossless=True, method=6)
    print(f"Saved {args.output} ({result.width} × {result.height})")


if __name__ == "__main__":
    main()
