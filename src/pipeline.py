from pathlib import Path

import cv2

from classes.camera_manager import CameraManager


OUTPUT_DIR = Path("step8_tests/images/pipeline")


def save_image(name, image):
    if image is None:
        print(f"  {name}: NOT AVAILABLE")
        return False

    path = OUTPUT_DIR / f"{name}.jpg"

    success = cv2.imwrite(str(path), image)

    if success:
        print(f"  {name}: saved")
        return True

    print(f"  {name}: FAILED TO SAVE")
    return False


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=== STEP 8.4 VISION PIPELINE ===")

    camera = CameraManager()

    print("Starting camera...")
    camera.start_camera()

    print("Capturing...")
    camera.capture_image()

    if camera.raw_image is None:
        print("FAIL: No raw image.")
        return

    print("Running repository transformation...")

    try:
        camera.transform_image()
    except Exception as error:
        print()
        print("FAIL: Vision pipeline crashed.")
        print(error)
        return

    print()
    print("Pipeline completed without crashing.")
    print()
    print("Saving outputs:")

    save_image("raw", camera.raw_image)
    save_image("crop", camera.cropped_image)
    save_image("binary", camera.binary_image)
    save_image("clean", camera.clean_image)
    save_image("polygon", camera.polygon_image)

    save_image("blue", camera.cnt_blueline)
    save_image("orange", camera.cnt_orangeline)

    save_image("obstacle", camera.obstacle_image)
    save_image("pink", camera.pink_mask)

    save_image("display", camera.display_image)

    print()
    print("PASS: Repository vision pipeline completed.")


if __name__ == "__main__":
    main()
