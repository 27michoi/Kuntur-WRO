from pathlib import Path

import cv2

from classes.camera_manager import CameraManager


OUTPUT_DIR = Path("step8_tests/images/framing")

FULL_FILE = OUTPUT_DIR / "full.jpg"
CROP_FILE = OUTPUT_DIR / "crop.jpg"
CUT_FILE = OUTPUT_DIR / "cut.jpg"


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=== STEP 8.2 FRAMING AND CROP ===")

    camera = CameraManager()
    camera.start_camera()
    camera.capture_image()

    image = camera.raw_image

    if image is None:
        print("FAIL: No image captured.")
        return

    height, width = image.shape[:2]

    print(f"Full image: {width} x {height}")

    if width != 640 or height != 360:
        print("FAIL: Expected 640 x 360.")
        return

    # Repository crop:
    # remove the upper 80 rows
    crop = image[80:360, 0:640]

    print(f"Cropped image: {crop.shape[1]} x {crop.shape[0]}")

    if crop.shape[1] != 640 or crop.shape[0] != 280:
        print("FAIL: Crop dimensions incorrect.")
        return

    # Save full image
    cv2.imwrite(str(FULL_FILE), image)

    # Save cropped image
    cv2.imwrite(str(CROP_FILE), crop)

    # Create image showing the crop boundary
    marked = image.copy()

    # Horizontal line at row 80
    cv2.line(
        marked,
        (0, 80),
        (639, 80),
        (0, 0, 255),
        2
    )

    cv2.putText(
        marked,
        "CROP START - TOP 80 ROWS REMOVED",
        (10, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 0, 255),
        2
    )

    cv2.imwrite(str(CUT_FILE), marked)

    print()
    print("PASS")
    print(f"Full:  {FULL_FILE}")
    print(f"Crop:  {CROP_FILE}")
    print(f"Cut:   {CUT_FILE}")


if __name__ == "__main__":
    main()
