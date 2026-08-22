from pathlib import Path
import sys

import cv2

from classes.camera_manager import CameraManager


VALID_SCENARIOS = {
    "start",
    "left",
    "right",
    "corner",
    "lines",
    "gf",
    "gn",
    "rf",
    "rn",
    "pink",
}

VALID_LIGHTING = {
    "normal",
    "bright",
    "dark",
}


def main():

    if len(sys.argv) not in (2, 3):
        print(
            "Usage:\n"
            "python step8_tests/step8_03_capture.py "
            "SCENARIO [LIGHTING]"
        )
        return

    scenario = sys.argv[1].lower()
    lighting = sys.argv[2].lower() if len(sys.argv) == 3 else "normal"

    if scenario not in VALID_SCENARIOS:
        print(f"Unknown scenario: {scenario}")
        return

    if lighting not in VALID_LIGHTING:
        print(f"Unknown lighting condition: {lighting}")
        return

    output_dir = Path(
        f"step8_tests/images/dataset/{lighting}"
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{scenario}.jpg"

    print("=== STEP 8.3 FIELD IMAGE ===")
    print(f"Scenario: {scenario}")
    print(f"Lighting: {lighting}")

    camera = CameraManager()
    camera.start_camera()
    camera.capture_image()

    image = camera.raw_image

    if image is None:
        print("FAIL: No image captured.")
        return

    height, width = image.shape[:2]

    print(f"Captured: {width} x {height}")

    if width != 640 or height != 360:
        print("FAIL: Expected 640 x 360.")
        return

    cv2.imwrite(str(output_file), image)

    print(f"PASS: {output_file}")


if __name__ == "__main__":
    main()
