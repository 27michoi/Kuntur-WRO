**Overview**

Step 11 tests the robot’s ability to navigate a single corner at low speed (600 steps/s) using the production wall-following algorithm and vision system. Both left- and right-turn directions are evaluated using the existing Arduino firmware from Step 10, with no algorithm or servo recalibration required.

---

**Step-by-Step Instructions**

1. **Script Installation & Verification**
* Download `step11_one_corner_low_speed.py` on the Raspberry Pi into the directory `/home/admin/Projects/WRO2026-CLM/code/XX_2025_package/step11_tests/one_corner_low_speed.py`.
* Create output folders: `step11_results/logs` and `step11_results/frames`.
* Compile the Python file using `python -m py_compile` to verify syntax.
* Verify package dependencies using:
```bash
python -c "from classes.camera_manager import CameraManager; from classes.image_algoriths import ImageAlgorithms; from classes.arduino_comms import ArduinoComms; print('STEP 11 IMPORTS OK')"

```




2. **Automatic Stopping Logic**
* Default travel limit is set to **6,500 steps**.
* Upon corner detection, the target automatically converts to **4,000 steps** after the turn.
* A passing run concludes with the stop reason: `CORNER_EXIT_COMPLETE`. Reaching the fallback limit without detecting a corner (`MAX_DISTANCE_COMPLETE_NO_CORNER`) constitutes a failed run.


3. **Field Preparation**
* Use an obstacle-free WRO field section with 400–500 mm of straight track preceding a clear corner.
* Align the robot parallel to the starting wall, ensuring no cable interference.


4. **Left-Corner Execution**
* Position the robot in the left-turn lane.
* Run the command:
```bash
python -m step11_tests.one_corner_low_speed --direction left --max-steps 6500 --exit-steps 4000 2>&1 | tee ../../step11_results/logs/left_console.log

```


* Step away during the 5-second countdown.
* Confirm the robot follows the wall (servo range 75–90), detects the corner, completes the turn, enters the next straight, and halts without wall contact or excessive steering oscillation.


5. **Right-Corner Execution**
* Move the robot to approach the corner from the opposite direction.
* Run the command:
```bash
python -m step11_tests.one_corner_low_speed --direction right --max-steps 6500 --exit-steps 4000 2>&1 | tee ../../step11_results/logs/right_console.log

```


* Verify identical turn performance in the rightward direction.



---

**Safety & Distance Tweaks**

* **Emergency Abort:** Press `Ctrl+C` or use the physical power switch if the robot turns incorrectly, oscillates violently, moves backward, or risks hitting a wall.
* **Exit-Step Tuning:** If physical stopping position needs adjustment after a technical pass:
* *Undershooting curve:* Increase to `--exit-steps 4500`
* *Overshooting straight:* Decrease to `--exit-steps 3500`



---

**Pass Criteria & Required Deliverables**

**Pass Requirements (Both Directions):**

* Technical status: `PASS` (`Corner accepted: True`, `Completed target: True`, `Stop reason: CORNER_EXIT_COMPLETE`).
* Speed fixed at 600; servo output within 75–90.
* ~90° turn completed into the next straight section.
* No wall strikes, continuous steering oscillation, or backward motion.

**Deliverables to Submit:**

* Log files: `left_console.log` and `right_console.log`.
* CSV telemetry files for both runs.
* 6 Diagnostic Images (3 per run: straight approach, `_CORNER` frame, and exit straight).
* Observation notes for both runs evaluating corner completion, wall contact, exit alignment, and oscillation severity.
