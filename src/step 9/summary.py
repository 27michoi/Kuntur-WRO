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
        print("Fail: No metrics.json files found.")
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
        f"{'Light':<9} {'Scene':<13} "
        f"{'Blue%':>8} {'Orange%':>9} "
        f"{'Green%':>8} {'Red%':>8}"
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
