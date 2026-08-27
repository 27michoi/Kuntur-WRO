**Overview**

Step 13 evaluates single-obstacle avoidance at a controlled speed of 600 steps/s across four distinct conditions: both driving directions (Right and Left) combined with both obstacle colors (Green and Red). The test uses the existing competition logic, camera pipeline, and wall-following models without requiring modifications to `main.py` or the Arduino firmware.

---

**Rules & System Logic**

* **Obstacle Rules:**
* **Green Obstacles:** The robot must pass on the **right** side.
* **Red Obstacles:** The robot must pass on the **left** side.
* *Note:* The `--direction` flag indicates lap direction, not the avoidance side.


* **Preflight Check:** Before moving, the software verifies that the target obstacle color is visible. If not detected, the system aborts (`PREFLIGHT_OBSTACLE_NOT_CONFIRMED`).
* **Calibrated Limits:**
* Servo Center: 82
* Left-Direction Servo Limits: 75–92
* Right-Direction Servo Limits: 72–90



---

**Step-by-Step Execution**

1. **Setup Script & Directories**
* Create target folders and the test script file directly on the Raspberry Pi:
```bash
cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package
source ../.venv/bin/activate
mkdir -p step13_tests ../../step13_results/logs ../../step13_results/frames
touch step13_tests/__init__.py
nano step13_tests/obstacle_avoidance_low_speed.py

```


* Paste the script contents, save, and verify compilation using `python -m py_compile step13_tests/obstacle_avoidance_low_speed.py`.


2. **Field Preparation**
* Use a single straight track section with only the test obstacle placed in a legal position.
* Place the robot straight on the track **50–70 cm before the obstacle**.
* Ensure loose cables, a clear line of sight for preflight check, and manual access to the power switch.


3. **Run the 4 Test Configurations**
Execute each command sequentially, repositioning the robot and switching obstacles between runs:
* **Right Direction + Green Obstacle**
```bash
python -u -m step13_tests.obstacle_avoidance_low_speed --direction right --color green --steps 1700 2>&1 | tee ../../step13_results/logs/right_green_console.log

```


* **Right Direction + Red Obstacle**
```bash
python -u -m step13_tests.obstacle_avoidance_low_speed --direction right --color red --steps 1700 2>&1 | tee ../../step13_results/logs/right_red_console.log

```


* **Left Direction + Green Obstacle**
```bash
python -u -m step13_tests.obstacle_avoidance_low_speed --direction left --color green --steps 1700 2>&1 | tee ../../step13_results/logs/left_green_console.log

```


* **Left Direction + Red Obstacle**
```bash
python -u -m step13_tests.obstacle_avoidance_low_speed --direction left --color red --steps 1700 2>&1 | tee ../../step13_results/logs/left_red_console.log

```





---

**Troubleshooting & Distance Adjustment**

* **Insufficient Clearance:** If the avoidance maneuver executes properly but the robot stops before completely clearing the obstacle, re-run only that specific test increasing distance to `--steps 2000`. Do not increase speed.
* **Aborts:** Press `Ctrl+C` or flip the motor power switch if the robot attempts to pass on the wrong side, makes wall/obstacle contact, or oscillates heavily.

---

**Pass Criteria & Required Deliverables**

**Pass Requirements (All 4 Runs):**

* Preflight check passed (`Preflight passed: True`).
* Robot passes Green on the right and Red on the left.
* Zero contact with obstacles or walls, no severe steering oscillation, and successful resumption of wall-following.
* Servo outputs stay within calibrated bounds.
* Console summary shows `Stop reason: TARGET_COMPLETE` and `Technical result: PASS`.

**Deliverables to Submit:**

1. Package all results into an archive:
```bash
cd /home/admin/Projects/WRO2026-CLM
tar -czf step13_for_review.tar.gz step13_results

```


2. Send `step13_for_review.tar.gz` along with observation responses for all four runs (confirming: correct side, no obstacle contact, no wall contact, no strong oscillation).
