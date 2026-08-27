**Overview**

Step 10 validates the competition wall-following algorithm in a low-speed, straight-line environment before attempting turns. It integrates the original Arduino firmware, the repository's `CameraManager`, `ImageAlgorithms`, and `ArduinoComms` to ensure closed-loop steering control operates correctly without hitting walls or oscillating.

---

**Preparation & Setup**

1. **Firmware Restoration:** Reflash the original competition firmware via PlatformIO (`code/arduino`) to restore standard serial communication protocols:
* Continuous movement command: `m<angle>,<speed>.`
* Target step movement command: `<steps>!`


2. **Environment & Directory Setup:** Set up Python virtual environment, dependencies, and create directories at `step10_results/logs` and `step10_results/frames`.
3. **Angle Remapping:** Map the repository's default center angle (86) to the robot's physical calibrated center (**82**), constraining working steering bounds between **75 (Right)** and **90 (Left)**.

---

**Execution Workflow**

* **Script Creation:** Implement `step10_tests/wall_follow_low_speed.py` which:
* Accepts `--direction` (`left` or `right`), `--steps` (100–2000), and `--speed` (fixed at 600 steps/sec).
* Runs a 5-second countdown.
* Continuously captures images, calculates wall positions via `find_wall_to_follow()`, dynamically converts steering angles, and updates the Arduino.
* Records execution telemetry to a CSV log and saves diagnostic frames every 5 frames.


* **Test Progression:**
1. **Raised-Wheel Test:** Verify servo movements, limits (75–90), and automatic motor shutoff (`TARGET_COMPLETE`) without floor contact.
2. **Short Floor Runs:** Execute 500 steps (~300 mm) for both left and right directions on a straight path.
3. **Medium Floor Runs:** Execute 1000 steps (~600 mm).
4. **Full 1-Meter Runs:** Execute 1660 steps (~1000 mm) for both left and right directions.



---

**Completion Criteria & Required Deliverables**

* **Pass Criteria:**
* Flawless execution using real repository components (`CameraManager`, `ArduinoComms`, and `calculate_servo_angle_from_walls()`).
* Successful completion of 1660-step runs (~1 meter) in both directions at speed 600.
* Zero wall contact, zero excessive steering oscillation, and automatic stopping at target distance.


* **Required Output to Report:**
* Console outputs from 1660-step left and right runs.
* Log files (`.csv`) from `step10_results/logs/`.
* Diagnostic frames (`.jpg`) from `step10_results/frames/`.
* Status report confirming no wall contact and no oscillation for both runs.
