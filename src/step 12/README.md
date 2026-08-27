**Overview**

Step 12 tests the robot’s ability to complete one full, obstacle-free lap at a fixed speed of 600 steps/s. Using existing Step 11 competition firmware alongside the core repository classes (`CameraManager`, `LapTracker`, `ContextManager`, and `ArduinoComms`), the robot tracks and negotiates four quarter-laps via blue/orange line detection, stopping automatically once the lap is complete.

---

**Step-by-Step Instructions**

1. **Field Preparation**
* Clear all red/green obstacles and parking elements from the track.
* Maintain consistent lighting (matching Step 11 conditions).
* Position the robot centered on a straight section before the first blue/orange line sequence, ensuring USB cables run loose.


2. **Script Setup & Verification**
* Install `step12_one_complete_lap.py` on the Raspberry Pi:
```bash
cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package
source ../.venv/bin/activate
mkdir -p step12_tests ../../step12_results/logs ../../step12_results/frames
touch step12_tests/__init__.py
cp ~/Downloads/step12_one_complete_lap.py step12_tests/one_complete_lap.py

```


* Validate script compilation and module imports:
```bash
python -m py_compile step12_tests/one_complete_lap.py

```


* Ensure the Arduino connection is recognized at `/dev/ttyACM0`.


3. **Execution**
* Run the test in either direction (only one direction is required):
* **Right Direction:**
```bash
python -u -m step12_tests.one_complete_lap --direction right 2>&1 | tee ../../step12_results/logs/right_console.log

```


* **Left Direction:**
```bash
python -u -m step12_tests.one_complete_lap --direction left 2>&1 | tee ../../step12_results/logs/left_console.log

```




* Clear the course during the 5-second countdown.


4. **Tracking & Automatic Stopping**
* Stopping is driven by the `LapTracker` registering four sequential quarter-laps (`Quarter 1/4` through `4/4`).
* Servo steering limits apply dynamically based on direction (Right: 72–90; Left: 75–90).
* Safety fallback limits (25,000 steps / 50-second timeout) exist only for emergency aborts.



---

**Safety & Troubleshooting**

* **Emergency Abort:** Instantly press `Ctrl+C` or flip the motor power switch if the robot risks hitting a wall, misses a turn, oscillates violently, fails to stop, or if the camera freezes.
* **Line-Detection Issues:** Do not increase step limits or timeouts if the physical lap completes without hitting `4/4`; this indicates a line detection issue, not a distance limitation.

---

**Pass Criteria & Required Deliverables**

**Pass Requirements:**

* Technical output reports `Completed lap: True`, `Stop reason: LAP_COMPLETE`, and `Technical result: PASS`.
* Robot navigates four physical corners without hitting walls or oscillating severely.
* Automatically halts near the starting section upon registering 4/4 quarter-laps.

**Deliverables to Submit:**

* Final console log output:
```bash
tail -n 25 ../../step12_results/logs/right_console.log

```


* Latest CSV log file generated during the run.
* Four physical observation confirmations:
1. Completed one physical lap (yes/no)
2. Wall contact (yes/no)
3. Strong oscillation (yes/no)
4. Stopped automatically near starting section (yes/no)


* *(Note: Diagnostic images are only required if wall contact occurs or if the test results in `REVIEW`).*
