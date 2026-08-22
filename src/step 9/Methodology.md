Step 9 is a stationary vision test. No chassis measurements are needed—the lens-to-front-axle distance becomes relevant when converting pixels into real distances.
We’ll verify:
Black-wall processing: binary_image, clean_image, polygon_image
Blue/orange lines: correct mask, competing-mask rejection
Green/red obstacles: individual and combined masks
False positives under normal, bright, and dark lighting
Connected components, bounding boxes, centroids, and mask coverage
This follows the standard WRO/OpenCV approach: HSV thresholding produces masks, morphological processing cleans them, and the largest contour/component identifies the object. WRO Future Engineers computer-vision guide.
1. Prepare Step 9
Keep the motor battery disconnected and secure every cable outside the camera view.

cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package
source ../.venv/bin/activate

mkdir -p step9_tests
mkdir -p ../../step9_results/logs

touch step9_tests/__init__.py

vcgencmd get_throttled
rpicam-hello --list-cameras


Expected:

throttled=0x0

2. Create mask_verify.py
Create:
/home/admin/Projects/WRO2026-CLM/code/XX_2025_package/step9_tests/mask_verify.py

Paste:
from pathlib import Path
import json
import sys
import time

import cv2
import numpy as np

from classes.camera_manager import CameraManager


PROJECT_DIR = Path(__file__).resolve().parents[3]

VALID_SCENES = {
    "empty",
    "wall",
    "blue",
    "orange",
    "green_near",
    "green_far",
    "red_near",
    "red_far",
    "mixed",
}

VALID_LIGHTING = {
    "normal",
    "bright",
    "dark",
}

IMAGE_ATTRIBUTES = {
    "raw": "raw_image",
    "crop": "cropped_image",
    "colormask": "colormask_image",
    "grayscale": "grayscale_image",
    "blurred": "blurred_image",
    "binary": "binary_image",
    "clean": "clean_image",
    "polygon": "polygon_image",

    "blue_mask": "blue_mask",
    "orange_mask": "orange_mask",
    "green_mask": "green_mask",
    "red_mask": "red_mask",
    "combined_mask": "combined_mask",

    "blue_line_clean": "clean_blueline_image",
    "orange_line_clean": "clean_orangeline_image",

    "obstacle": "obstacle_image",
    "display": "display_image",
}

MASK_ATTRIBUTES = {
    "blue_mask": "blue_mask",
    "orange_mask": "orange_mask",
    "green_mask": "green_mask",
    "red_mask": "red_mask",
    "combined_mask": "combined_mask",
}

OVERLAY_COLORS = {
    "blue_mask": (255, 0, 0),
    "orange_mask": (0, 140, 255),
    "green_mask": (0, 255, 0),
    "red_mask": (0, 0, 255),
    "combined_mask": (255, 0, 255),
}

REQUIRED_BY_SCENE = {
    "empty": {
        "blue_mask",
        "orange_mask",
        "green_mask",
        "red_mask",
    },
    "wall": {
        "binary",
        "clean",
        "polygon",
    },
    "blue": {
        "blue_mask",
        "orange_mask",
    },
    "orange": {
        "blue_mask",
        "orange_mask",
    },
    "green_near": {
        "green_mask",
        "red_mask",
        "combined_mask",
    },
    "green_far": {
        "green_mask",
        "red_mask",
        "combined_mask",
    },
    "red_near": {
        "green_mask",
        "red_mask",
        "combined_mask",
    },
    "red_far": {
        "green_mask",
        "red_mask",
        "combined_mask",
    },
    "mixed": {
        "blue_mask",
        "orange_mask",
        "green_mask",
        "red_mask",
        "combined_mask",
    },
}

MIN_COMPONENT_AREA = 25


def close_camera(camera):
    if camera is None:
        return

    try:
        camera.release_video()
    except Exception:
        pass

    picam2 = getattr(camera, "picam2", None)

    if picam2 is not None:
        try:
            picam2.stop()
        except Exception:
            pass

        try:
            picam2.close()
        except Exception:
            pass


def prepare_image(image):
    if not isinstance(image, np.ndarray):
        return None

    if image.ndim not in (2, 3):
        return None

    if image.shape[0] < 8 or image.shape[1] < 8:
        return None

    output = image

    if image.dtype == np.bool_:
        output = image.astype(np.uint8) * 255
    elif image.dtype not in (np.uint8, np.uint16):
        output = cv2.normalize(
            image,
            None,
            0,
            255,
            cv2.NORM_MINMAX,
        ).astype(np.uint8)

    return output


def save_image(output_dir, name, image):
    output = prepare_image(image)

    if output is None:
        print(f"  {name}: NOT AVAILABLE OR NOT AN IMAGE")
        return False

    if output.ndim == 3 and output.shape[2] not in (1, 3, 4):
        print(f"  {name}: UNSUPPORTED SHAPE {output.shape}")
        return False

    path = output_dir / f"{name}.jpg"

    try:
        success = cv2.imwrite(str(path), output)
    except Exception as error:
        print(f"  {name}: SAVE ERROR ({error})")
        return False

    if success:
        height, width = output.shape[:2]
        print(f"  {name}: saved ({width} x {height})")
        return True

    print(f"  {name}: FAILED TO SAVE")
    return False


def convert_to_binary(mask):
    image = prepare_image(mask)

    if image is None:
        return None

    if image.ndim == 3:
        if image.shape[2] == 4:
            gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        elif image.shape[2] == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image[:, :, 0]
    else:
        gray = image

    binary = np.where(gray > 0, 255, 0).astype(np.uint8)
    return binary


def analyze_mask(mask):
    binary = convert_to_binary(mask)

    if binary is None:
        return None

    height, width = binary.shape
    total_pixels = width * height
    active_pixels = int(cv2.countNonZero(binary))
    coverage = 100.0 * active_pixels / total_pixels

    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        binary,
        connectivity=8,
    )

    components = []

    for index in range(1, count):
        area = int(stats[index, cv2.CC_STAT_AREA])

        if area < MIN_COMPONENT_AREA:
            continue

        x = int(stats[index, cv2.CC_STAT_LEFT])
        y = int(stats[index, cv2.CC_STAT_TOP])
        w = int(stats[index, cv2.CC_STAT_WIDTH])
        h = int(stats[index, cv2.CC_STAT_HEIGHT])

        cx = float(centroids[index][0])
        cy = float(centroids[index][1])

        components.append(
            {
                "area": area,
                "bbox": [x, y, w, h],
                "centroid": [round(cx, 2), round(cy, 2)],
            }
        )

    components.sort(key=lambda item: item["area"], reverse=True)
    largest = components[0] if components else None

    return {
        "width": width,
        "height": height,
        "active_pixels": active_pixels,
        "coverage_percent": round(coverage, 4),
        "significant_components": len(components),
        "largest_component": largest,
    }


def create_overlay(base_image, mask, color, analysis):
    base = prepare_image(base_image)
    binary = convert_to_binary(mask)

    if base is None or binary is None:
        return None

    if base.ndim == 2:
        base = cv2.cvtColor(base, cv2.COLOR_GRAY2BGR)
    elif base.shape[2] == 4:
        base = cv2.cvtColor(base, cv2.COLOR_BGRA2BGR)

    if binary.shape[:2] != base.shape[:2]:
        binary = cv2.resize(
            binary,
            (base.shape[1], base.shape[0]),
            interpolation=cv2.INTER_NEAREST,
        )

    colored = np.zeros_like(base)
    colored[:] = color

    blended = cv2.addWeighted(base, 0.65, colored, 0.35, 0)
    overlay = base.copy()
    overlay[binary > 0] = blended[binary > 0]

    if analysis and analysis["largest_component"]:
        x, y, w, h = analysis["largest_component"]["bbox"]
        cx, cy = analysis["largest_component"]["centroid"]

        cv2.rectangle(
            overlay,
            (x, y),
            (x + w, y + h),
            (0, 255, 255),
            2,
        )

        cv2.circle(
            overlay,
            (int(cx), int(cy)),
            5,
            (255, 255, 255),
            -1,
        )

    return overlay


def build_checks(scene, metrics):
    checks = []

    if scene in {"empty", "wall"}:
        for name in (
            "blue_mask",
            "orange_mask",
            "green_mask",
            "red_mask",
        ):
            data = metrics.get(name)

            if data is None:
                checks.append(f"REVIEW: {name} unavailable")
            elif data["coverage_percent"] <= 1.0:
                checks.append(
                    f"PASS: {name} false-positive coverage "
                    f"{data['coverage_percent']}%"
                )
            else:
                checks.append(
                    f"REVIEW: {name} false-positive coverage "
                    f"{data['coverage_percent']}%"
                )

    comparisons = {
        "blue": ("blue_mask", "orange_mask"),
        "orange": ("orange_mask", "blue_mask"),
        "green_near": ("green_mask", "red_mask"),
        "green_far": ("green_mask", "red_mask"),
        "red_near": ("red_mask", "green_mask"),
        "red_far": ("red_mask", "green_mask"),
    }

    if scene in comparisons:
        target_name, competing_name = comparisons[scene]
        target = metrics.get(target_name)
        competing = metrics.get(competing_name)

        if target is None:
            checks.append(f"REVIEW: {target_name} unavailable")
        else:
            largest = target["largest_component"]
            largest_area = largest["area"] if largest else 0

            if largest_area >= MIN_COMPONENT_AREA:
                checks.append(
                    f"PASS: {target_name} component area "
                    f"{largest_area} pixels"
                )
            else:
                checks.append(
                    f"REVIEW: {target_name} has no significant component"
                )

        if target and competing:
            target_pixels = target["active_pixels"]
            competing_pixels = competing["active_pixels"]

            if target_pixels >= max(50, competing_pixels * 2):
                checks.append(
                    f"PASS: {target_name} dominates {competing_name}"
                )
            else:
                checks.append(
                    f"REVIEW: weak separation between "
                    f"{target_name} and {competing_name}"
                )

    if scene == "wall":
        checks.append(
            "VISUAL CHECK: wall must be continuous in binary, "
            "clean and polygon images"
        )

    if scene == "mixed":
        checks.append(
            "VISUAL CHECK: masks must remain separated when "
            "several field elements are visible"
        )

    return checks


def main():
    if len(sys.argv) not in (2, 3):
        print(
            "Usage:\n"
            "python -m step9_tests.mask_verify "
            "SCENE [LIGHTING]"
        )
        return 1

    scene = sys.argv[1].lower()
    lighting = sys.argv[2].lower() if len(sys.argv) == 3 else "normal"

    if scene not in VALID_SCENES:
        print(f"Unknown scene: {scene}")
        print("Valid:", ", ".join(sorted(VALID_SCENES)))
        return 1

    if lighting not in VALID_LIGHTING:
        print(f"Unknown lighting: {lighting}")
        print("Valid:", ", ".join(sorted(VALID_LIGHTING)))
        return 1

    output_dir = (
        PROJECT_DIR
        / "step9_results"
        / lighting
        / scene
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== STEP 9 MASK VERIFICATION ===")
    print(f"Scene: {scene}")
    print(f"Lighting: {lighting}")

    camera = None

    try:
        camera = CameraManager()

        print("Starting camera...")
        camera.start_camera()
        time.sleep(1.0)

        print("Capturing...")
        camera.capture_image()

        if camera.raw_image is None:
            print("FAIL: Camera returned no image.")
            return 1

        print("Transforming...")
        camera.transform_image()

        print()
        print("Saving pipeline images:")

        saved = set()

        for output_name, attribute in IMAGE_ATTRIBUTES.items():
            image = getattr(camera, attribute, None)

            if save_image(output_dir, output_name, image):
                saved.add(output_name)

        crop = getattr(camera, "cropped_image", None)
        metrics = {}

        print()
        print("Mask measurements:")

        for mask_name, attribute in MASK_ATTRIBUTES.items():
            mask = getattr(camera, attribute, None)
            analysis = analyze_mask(mask)
            metrics[mask_name] = analysis

            if analysis is None:
                print(f"  {mask_name}: NOT AVAILABLE")
                continue

            largest = analysis["largest_component"]
            largest_area = largest["area"] if largest else 0

            print(
                f"  {mask_name}: "
                f"{analysis['coverage_percent']}% coverage, "
                f"{analysis['significant_components']} components, "
                f"largest={largest_area}px"
            )

            overlay = create_overlay(
                crop,
                mask,
                OVERLAY_COLORS[mask_name],
                analysis,
            )

            save_image(
                output_dir,
                f"{mask_name}_overlay",
                overlay,
            )

        checks = build_checks(scene, metrics)

        scalar_values = {}

        for attribute in ("length_blue", "length_orange"):
            if hasattr(camera, attribute):
                value = getattr(camera, attribute)

                if isinstance(value, np.generic):
                    value = value.item()

                scalar_values[attribute] = value

        report = {
            "scene": scene,
            "lighting": lighting,
            "metrics": metrics,
            "scalars": scalar_values,
            "checks": checks,
        }

        metrics_file = output_dir / "metrics.json"

        metrics_file.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )

        report_file = output_dir / "report.txt"

        report_lines = [
            "STEP 9 MASK VERIFICATION",
            f"Scene: {scene}",
            f"Lighting: {lighting}",
            "",
            "Checks:",
        ]

        report_lines.extend(f"- {check}" for check in checks)

        report_file.write_text(
            "\n".join(report_lines) + "\n",
            encoding="utf-8",
        )

        print()
        print("Checks:")

        for check in checks:
            print(f"  {check}")

        required = REQUIRED_BY_SCENE[scene]
        missing = required - saved

        if missing:
            print()
            print("FAIL: Required outputs missing:")
            for name in sorted(missing):
                print(f"  {name}")
            return 1

        print()
        print("PASS: Technical mask test completed.")
        print(f"Outputs: {output_dir}")
        return 0

    except Exception as error:
        print()
        print("FAIL: Mask test crashed.")
        print(f"{type(error).__name__}: {error}")
        return 1

    finally:
        close_camera(camera)


if __name__ == "__main__":
    raise SystemExit(main())


3. Create the summary script
Create:
/home/admin/Projects/WRO2026-CLM/code/XX_2025_package/step9_tests/summary.py

Paste:
from pathlib import Path
import csv
import json


PROJECT_DIR = Path(__file__).resolve().parents[3]
RESULTS_DIR = PROJECT_DIR / "step9_results"
OUTPUT_FILE = RESULTS_DIR / "mask_summary.csv"

MASKS = [
    "blue_mask",
    "orange_mask",
    "green_mask",
    "red_mask",
    "combined_mask",
]


def metric_value(metrics, mask, field, default=""):
    data = metrics.get(mask)

    if not data:
        return default

    if field == "largest_area":
        largest = data.get("largest_component")
        return largest.get("area", 0) if largest else 0

    return data.get(field, default)


def main():
    files = sorted(RESULTS_DIR.rglob("metrics.json"))

    if not files:
        print("FAIL: No metrics.json files found.")
        return 1

    fieldnames = ["lighting", "scene"]

    for mask in MASKS:
        fieldnames.append(f"{mask}_coverage")
        fieldnames.append(f"{mask}_largest")

    fieldnames.extend(
        [
            "length_blue",
            "length_orange",
            "checks",
        ]
    )

    rows = []

    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        metrics = data.get("metrics", {})
        scalars = data.get("scalars", {})

        row = {
            "lighting": data.get("lighting", ""),
            "scene": data.get("scene", ""),
            "length_blue": scalars.get("length_blue", ""),
            "length_orange": scalars.get("length_orange", ""),
            "checks": " | ".join(data.get("checks", [])),
        }

        for mask in MASKS:
            row[f"{mask}_coverage"] = metric_value(
                metrics,
                mask,
                "coverage_percent",
            )

            row[f"{mask}_largest"] = metric_value(
                metrics,
                mask,
                "largest_area",
            )

        rows.append(row)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Tests summarized: {len(rows)}")
    print(f"Saved: {OUTPUT_FILE}")

    print()
    print(
        f"{'LIGHT':<9} {'SCENE':<13} "
        f"{'BLUE%':>8} {'ORANGE%':>9} "
        f"{'GREEN%':>8} {'RED%':>8}"
    )

    for row in rows:
        print(
            f"{row['lighting']:<9} "
            f"{row['scene']:<13} "
            f"{str(row['blue_mask_coverage']):>8} "
            f"{str(row['orange_mask_coverage']):>9} "
            f"{str(row['green_mask_coverage']):>8} "
            f"{str(row['red_mask_coverage']):>8}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


Compile both:
python -m py_compile \
  step9_tests/mask_verify.py \
  step9_tests/summary.py

No output means both files are syntactically correct.
4. Physical scene positions

Scene
Physical arrangement
empty
Plain field area without colored line or obstacle
wall
Black wall clearly visible; no colored obstacle
blue
Blue line across the lower-middle field of view
orange
Orange line across the lower-middle view
green_near
Green obstacle 300–400 mm from lens
green_far
Green obstacle 700–900 mm from lens
red_near
Red obstacle 300–400 mm from lens
red_far
Red obstacle 700–900 mm from lens
mixed
Natural course view with wall, line and obstacle

The distances are measured from the lens, so the missing lens-to-axle measurement does not affect Step 9.
5. Normal-lighting tests
Reposition the stationary robot before every command:

python -m step9_tests.mask_verify empty normal 2>&1 \
  | tee ../../step9_results/logs/empty_normal.log

python -m step9_tests.mask_verify wall normal 2>&1 \
  | tee ../../step9_results/logs/waull_normal.log

python -m step9_tests.mask_verify blue normal 2>&1 \
  | tee ../../step9_results/logs/blue_normal.log

python -m step9_tests.mask_verify orange normal 2>&1 \
  | tee ../../step9_results/logs/orange_normal.log

python -m step9_tests.mask_verify green_near normal 2>&1 \
  | tee ../../step9_results/logs/green_near_normal.log

python -m step9_tests.mask_verify green_far normal 2>&1 \
  | tee ../../step9_results/logs/green_far_normal.log

python -m step9_tests.mask_verify red_near normal 2>&1 \
  | tee ../../step9_results/logs/red_near_normal.log

python -m step9_tests.mask_verify red_far normal 2>&1 \
  | tee ../../step9_results/logs/red_far_normal.log

python -m step9_tests.mask_verify mixed normal 2>&1 \
  | tee ../../step9_results/logs/mixed_normal.log


6. Bright-lighting tests
Use brighter overhead lighting without shining a lamp directly into the lens:
python -m step9_tests.mask_verify empty bright 2>&1 \
  | tee ../../step9_results/logs/empty_bright.log

python -m step9_tests.mask_verify wall bright 2>&1 \
  | tee ../../step9_results/logs/wall_bright.log

python -m step9_tests.mask_verify blue bright 2>&1 \
  | tee ../../step9_results/logs/blue_bright.log

python -m step9_tests.mask_verify orange bright 2>&1 \
  | tee ../../step9_results/logs/orange_bright.log

python -m step9_tests.mask_verify green_near bright 2>&1 \
  | tee ../../step9_results/logs/green_near_bright.log

python -m step9_tests.mask_verify red_near bright 2>&1 \
  | tee ../../step9_results/logs/red_near_bright.log

7. Dark-lighting tests
The field must remain visible; “dark” should not mean “cave mode.”
python -m step9_tests.mask_verify empty dark 2>&1 \
  | tee ../../step9_results/logs/empty_dark.log

python -m step9_tests.mask_verify wall dark 2>&1 \
  | tee ../../step9_results/logs/wall_dark.log

python -m step9_tests.mask_verify blue dark 2>&1 \
  | tee ../../step9_results/logs/blue_dark.log

python -m step9_tests.mask_verify orange dark 2>&1 \
  | tee ../../step9_results/logs/orange_dark.log

python -m step9_tests.mask_verify green_near dark 2>&1 \
  | tee ../../step9_results/logs/green_near_dark.log

python -m step9_tests.mask_verify red_near dark 2>&1 \
  | tee ../../step9_results/logs/red_near_dark.log


8. Generate the comparison table
python -m step9_tests.summary 2>&1 \
  | tee ../../step9_results/logs/summary.log
Then verify files:
find ../../step9_results \
  -type f \( -name "*.jpg" -o -name "*.json" -o -name "*.txt" -o -name "*.csv" -o -name "*.log" \) \
  | sort

vcgencmd get_throttled

du -sh ../../step9_results
9. Pass criteria
Step 9 passes when:
wall:
binary.jpg distinguishes black walls from the floor.
clean.jpg removes isolated noise without deleting the walls.
polygon.jpg presents continuous usable wall boundaries.
blue:
blue_mask forms a strong connected line.
orange_mask remains substantially smaller.
The blue overlay aligns with the real blue line.
orange:
orange_mask forms the correct line.
blue_mask remains substantially smaller.
Green/red obstacles:
Correct mask produces a dominant component around the obstacle.
Competing-color mask remains small.
combined_mask contains the obstacle.
Bounding box and centroid align with the physical pillar.
empty:
Each color mask ideally covers less than approximately 1% of the image.
No large colored false-positive component appears.
Bright/dark:
Correct objects remain detectable.
Masks do not suddenly cover large portions of the frame.
The numeric rules are screening heuristics, not absolute truth. Far objects naturally produce fewer pixels, so the saved overlays are the final evidence.
10. Send me these results
Send:
step9_results/mask_summary.csv
normal/wall/crop.jpg
normal/wall/binary.jpg
normal/wall/clean.jpg
normal/wall/polygon.jpg
normal/blue/blue_mask.jpg
normal/blue/blue_mask_overlay.jpg
normal/orange/orange_mask.jpg
normal/orange/orange_mask_overlay.jpg
normal/green_near/green_mask_overlay.jpg
normal/green_far/green_mask_overlay.jpg
normal/red_near/red_mask_overlay.jpg
normal/red_far/red_mask_overlay.jpg
normal/green_near/obstacle.jpg
normal/red_near/obstacle.jpg
normal/mixed/display.jpg
empty_normal.log
summary.log
Final vcgencmd get_throttled output
If any mask is blank or noisy, do not modify the repository HSV limits yet. Send the corresponding crop.jpg, mask, overlay, metrics.json, and log; then we can calculate the correct threshold adjustment from actual evidence.


