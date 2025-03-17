# /// script
# requires-python=">=3.12"
# ///

import subprocess
from pathlib import Path


def convert_images_to_webp(dir: Path) -> None:
    img_files = list(dir.glob("*.jpg")) + list(dir.glob("*.png"))
    for img in img_files:
        output_file = img.with_suffix(".webp")
        try:
            subprocess.run(["cwebp", str(img), "-o", str(output_file)], check=True)
            print(f"converted {img} to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"error while converting {img}: {e}")


if __name__ == "__main__":
    convert_images_to_webp(Path("./output/static/images/"))
