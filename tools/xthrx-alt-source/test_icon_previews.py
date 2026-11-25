import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image

from render_icon_previews import render_icon_archive


class IconPreviewRendererTests(unittest.TestCase):
    def test_renders_composer_layers_and_gradient_to_png(self):
        metadata = {
            "fill": {
                "linear-gradient": ["srgb:0.1,0.0,0.1,1.0", "srgb:0.8,0.2,0.3,1.0"],
                "orientation": {"start": {"x": 0.5, "y": 0}, "stop": {"x": 0.5, "y": 1}},
            },
            "groups": [{"opacity": 1.0, "layers": [{"image-name": "shape.svg", "opacity": 1.0}]}],
        }
        svg = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><circle cx="512" cy="512" r="220" fill="#ffffff"/></svg>'
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("Untitled.icon/icon.json", json.dumps(metadata))
            archive.writestr("Untitled.icon/Assets/shape.svg", svg)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "preview.png"
            render_icon_archive(buffer.getvalue(), output, size=128)
            self.assertTrue(output.is_file())
            with Image.open(output) as image:
                self.assertEqual(image.size, (128, 128))
                self.assertEqual(image.mode, "RGBA")
                self.assertNotEqual(image.getpixel((0, 0)), image.getpixel((64, 64)))


if __name__ == "__main__":
    unittest.main()
