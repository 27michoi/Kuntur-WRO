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

    print("Step 9 mask verification")
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
            print("Fail: Camera returned no image.")
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
            "Step 9 mask verification",
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
            print("Fail: Required outputs missing:")

            for name in sorted(missing):
                print(f"  {name}")

            return 1

        print()
        print("Pass: Technical mask test completed.")
        print(f"Outputs: {output_dir}")

        return 0

    except Exception as error:
        print()
        print("Fail: Mask test crashed.")
        print(f"{type(error).__name__}: {error}")

        return 1

    finally:
        close_camera(camera)


if __name__ == "__main__":
    raise SystemExit(main())
