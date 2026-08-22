from pathlib import Path

from classes.camera_manager import CameraManager

OUTPUT_DIR = Path("step8_tests/images/health")
OUTPUT_FILE = OUTPUT_DIR / "health.jpg"

EXPECTED_WIDTH = 640
EXPECTED_HEIGHT = 360

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=== STEP 8.1 CAMERA HEALTH ===")

    camera = CameraManager()

    print("Starting camera...")
    camera.start_camera()

    print("Capturing image...")
    camera.capture_image()

    image = camera.raw_image

    if image is None:
        print("FAIL: Camera returned no image.")
        return

    height, width = image.shape[:2]

    print(f"Image size: {width} x {height}")

    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        print("FAIL: Image dimensions are incorrect.")
        print(f"Expected: {EXPECTED_WIDTH} x {EXPECTED_HEIGHT}")
        return

    success = camera.raw_image is not None

    if success:
        import cv2

        cv2.imwrite(str(OUTPUT_FILE), image)

        print("PASS: Camera captured correctly.")
        print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
