#!/usr/bin/env python3
"""Render static AltStore previews from the official Icon Composer packages."""
from __future__ import annotations

import io
import os
import zipfile
from pathlib import Path
from urllib.parse import quote

import cairosvg
import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
RAW_ICON_BASE = "https://raw.githubusercontent.com/Akatsubaki-Emu/Akatsubaki-Emu/main/Icons/"
ICON_ARCHIVES = {
    "default": "Akatsubaki emu default icon .icon.zip",
    "simple": "Akatsubaki emu simple icon .icon.zip",
}
OUTPUTS = {
    "default": ROOT / "static" / "img" / "akatsubaki-icon-default.png",
    "simple": ROOT / "static" / "img" / "akatsubaki-icon-simple.png",
}
SIZE = 1024


def _rgba(value: str) -> tuple[int, int, int, int]:
    if not value.startswith("srgb:"):
        raise ValueError(f"Unsupported Icon Composer color: {value}")
    channels = [float(part) for part in value.removeprefix("srgb:").split(",")]
    if len(channels) != 4 or any(not 0.0 <= channel <= 1.0 for channel in channels):
        raise ValueError(f"Invalid Icon Composer color: {value}")
    return tuple(round(channel * 255) for channel in channels)


def _gradient(metadata: dict, size: int) -> Image.Image:
    fill = metadata.get("fill", {})
    colors = fill.get("linear-gradient")
    if not isinstance(colors, list) or len(colors) < 2:
        raise ValueError("Icon Composer file has no supported linear-gradient fill")
    start = fill.get("orientation", {}).get("start", {}).get("y", 0.0)
    stop = fill.get("orientation", {}).get("stop", {}).get("y", 1.0)
    first, last = _rgba(colors[0]), _rgba(colors[-1])
    span = float(stop) - float(start)
    if span == 0:
        raise ValueError("Icon Composer gradient has a zero-length vertical axis")
    pixels = []
    for y in range(size):
        position = min(1.0, max(0.0, (y / max(1, size - 1) - float(start)) / span))
        pixels.extend(
            round(first[channel] + (last[channel] - first[channel]) * position)
            for channel in range(4)
        )
    row = bytes(pixels)
    return Image.frombytes("RGBA", (1, size), row).resize((size, size))


def render_icon_archive(archive_bytes: bytes, output_path: Path, size: int = SIZE) -> None:
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise ValueError(f"Corrupt icon archive member: {bad_member}")
        metadata_path = "Untitled.icon/icon.json"
        metadata = __import__("json").loads(archive.read(metadata_path))
        canvas = _gradient(metadata, size)
        for group in metadata.get("groups", []):
            group_opacity = float(group.get("opacity", 1.0))
            for layer in group.get("layers", []):
                if layer.get("hidden"):
                    continue
                image_name = layer.get("image-name")
                if not image_name:
                    continue
                asset_path = f"Untitled.icon/Assets/{image_name}"
                svg = archive.read(asset_path)
                png = cairosvg.svg2png(bytestring=svg, output_width=size, output_height=size)
                with Image.open(io.BytesIO(png)) as rendered:
                    layer_image = rendered.convert("RGBA")
                opacity = min(1.0, max(0.0, group_opacity * float(layer.get("opacity", 1.0))))
                if opacity < 1.0:
                    alpha = layer_image.getchannel("A").point(lambda value: round(value * opacity))
                    layer_image.putalpha(alpha)
                canvas = Image.alpha_composite(canvas, layer_image)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(output_path, format="PNG", optimize=True)


def fetch_archive(filename: str) -> bytes:
    headers = {"User-Agent": "Akatsubaki-Emu-AltSource/1.0"}
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = RAW_ICON_BASE + quote(filename)
    response = requests.get(url, headers=headers, timeout=(5, 30))
    response.raise_for_status()
    return response.content


def main() -> None:
    for channel, filename in ICON_ARCHIVES.items():
        render_icon_archive(fetch_archive(filename), OUTPUTS[channel])
        print(f"Rendered {channel} icon preview: {OUTPUTS[channel].relative_to(ROOT)}")


if __name__ == "__main__":
    main()
