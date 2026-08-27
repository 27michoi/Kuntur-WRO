**Overview**

Step 9 focuses on testing and validating the computer vision pipeline offline using the static dataset captured in Step 8 across three lighting conditions (**normal**, **bright**, **dark**). The primary objective is to verify color masking (black walls, blue/orange lines, red/green obstacles), bounding boxes, centroids, and lighting resilience before applying live parameter changes.

---

**Directory Structure & Initial Setup**

```text
XX_2025_package/
├── classes/
├── step8_tests/images/dataset/ (normal, bright, dark)
└── step9_tests/
    ├── __init__.py
    ├── offline_verify.py
    └── offline_summary.py

```

* **Environment Execution:** Working directory is set to `/home/admin/Projects/WRO2026-CLM/code/XX_2025_package/` within the `.venv` virtual environment.
* **Technical Baseline:** 30 images processed, achieving **30 technical passes** and **0 technical failures**.

---

**Step-by-Step Workflow**

1. **Legacy Patch & Verification Filter:**
* Updated `step9_tests/offline_summary.py` to filter out legacy metrics that lack `technical_status` or `source_sha256` parameters.


2. **Comparison Image Generation (`offline_summary.py`):**
* Processes crops and overlays side-by-side (`normal | bright | dark`) in `/step9_results/comparisons/` for key masks:
* **Wall Processing:** `crop.jpg`, `binary.jpg`, `clean.jpg`, `polygon.jpg`
* **Color Overlays:** `blue_mask_overlay`, `orange_mask_overlay`, `green_mask_overlay`, `red_mask_overlay`, `combined_mask_overlay`




3. **Manual Ground-Truth Logging (`scene_observations.csv`):**
* Manually inspected original image crops and recorded object visibility (`yes`/`no`) across columns: `wall`, `blue`, `orange`, `green`, `red`, and `notes`.


4. **Final Semantic Evaluation & Report Generation:**
* Re-ran `offline_summary` using the completed observations to produce `mask_summary.csv`, `lighting_comparison.csv`, `semantic_checks.csv`, and `step9_report.txt`.



---

**Key Issues Identified During Semantic Check**

Running `grep "REVIEW" semantic_checks.csv` flagged specific edge-case failures requiring attention:

* **False Positives:** Red masks triggered under `bright/pink` (11.5% coverage), `dark/corner` (2.5%), `dark/lines` (6.1%), and `normal/pink` (11.15%).
* **Missed Detections:** Missing orange/blue/green masks under dark and normal conditions (e.g., `dark/gf`, `dark/gn`, `dark/left`, `dark/lines`, `dark/rf`, `normal/gf`).
* **Weak Mask Separation:** Ambiguity between competing colors (e.g., `bright/pink` blue vs. orange; `normal/gf` and `normal/gn` green vs. red).

---

**Pass Criteria & Deliverables**

* **Final Pass Conditions:** 30/30 technical passes, 0 missing outputs, accurate bounding boxes/centroids, robust wall contour detection, and visual alignment between masks and real physical features.
* **Archive Packaging:** Final assets packaged from root:
`tar -czf step9_results.tar.gz step9_results`
