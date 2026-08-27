## Overview

This document guides you through setting up, testing, and calibrating a robot's 1-meter straight-line movement using PlatformIO, C++ code, and serial commands.

###### Resumen

######

___

## Step-by-Step Instructions

1. **Environment Setup**
* Create a new project directory (`step6_straight_line_test`) with `src` and `lib` subdirectories on the Raspberry Pi via SSH.
* Copy the required `FlexyStepper` and `Servo` libraries into the project's `lib` folder.
* Open the project folder in VS Code.


2. **Configuration & Code Creation**
* Create `platformio.ini` set to target an Arduino Uno with a monitor speed of 115200.
* Create `src/main.cpp` with the provided code, which handles state management (`IDLE`, `COUNTDOWN`, `MOVING`, `STOPPING`), serial input commands (`GO`, `STOP`, `STATUS`, `HELP`, and `A<angle>`), a 5-second start delay, and stepper motor motion routines.


3. **Compilation & Upload**
* Disconnect the motor battery before uploading.
* Compile using `pio run`.
* Identify the serial port (`/dev/ttyACM0` or similar) using `pio device list`.
* Upload the firmware to the Arduino using `pio run --target upload --upload-port /dev/ttyACM0`.


4. **Initial Wheel-Raised Test**
* Elevate the robot wheels off the ground and connect the motor battery.
* Open the serial monitor (`pio device monitor --port /dev/ttyACM0 --baud 115200`).
* Send commands `STATUS`, `A99`, then `GO`.
* Verify the wheels wait 5 seconds, spin for ~11 seconds total, and print `DONE`.
* *Correction:* If wheels spin backward, exit the monitor (`Ctrl + ]`), update `FORWARD_SIGN = 1` in `main.cpp`, and re-upload.


5. **Floor Test Setup**
* Mark a straight centerline (at least 1.2 m), a start line, and a 1000 mm target line on a flat, hard surface.
* Position the robot centered over the start reference line with the front wheels straight and a loose USB cable trailing behind.


6. **Data Collection & Calibration**
* Run `A99` followed by `GO` for 3 separate floor trials. Measure and record:
* Forward distance traveled
* Distance error (actual mm minus 1000 mm)
* Lateral deviation and drift direction (Left/Right)


* **Steering Calibration:** Adjust the angle 1 degree at a time (`A98` if drifting left, `A100` if drifting right). Inspect mechanical alignment if more than 3 degrees of correction is needed. Update `SERVO_CENTER` in code once calibrated.
* **Distance Calibration:** Calculate the new step count using the formula:

$$\text{New Steps} = 6400 \times \frac{1000}{D_{\text{average}}}$$



Update `TEST_STEPS` in `main.cpp` and re-upload.


7. **Pass Criteria & Required Deliverables**
* **Pass Criteria:** 3 consecutive runs without resets/stalls, automatic stopping, final average distance within $\pm 30\text{ mm}$ of 1000 mm, lateral drift within $\pm 50\text{ mm}$, and no hardware overheating.
* **Deliverables to Send:**
* The 3 measured distances and lateral deviations.
* Confirmation that 6400 steps moved the robot forward.
* Photos: Top-down view at `A99`, side view of wheel against a ruler, and a close-up of the gears/microstep jumpers.
