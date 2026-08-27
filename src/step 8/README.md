**Overview**

Step 8 verifies that your final camera setup supplies clean, properly framed images to the repository's vision pipeline **before** the robot ever moves. Because the standard Camera Module 3 has a narrower field of view (75°) than the original team's camera (120°), these static tests ensure its perspective still captures enough track detail for autonomous navigation.

---

**Hardware & Setup Details**

* **Power & Control:** Only the Raspberry Pi is powered (via a portable bank); drive motors remain disconnected. Control the Pi via VS Code Remote SSH over Wi-Fi.
* **Image Delivery:** View captured frames directly on your laptop via VS Code rather than using live standard OpenCV display windows.
* **Image Specifications:** The Pi captures at **640 × 360** pixels. The software then crops out the top 80 rows, leaving a **640 × 280** working region.
* **Camera Metrics to Log:** Document lens height (mm), tilt angle (°), distance to the front axle (mm), horizontal centering, and lighting conditions.

---

**Step-by-Step Test Execution**

1. **Camera Health Check (`step8_01_camera_health.py`)**
* Run `rpicam-hello --list-cameras` to confirm the sensor registers as `imx708`.
* Run the script to test stream stability, measure frame rate, and capture a test 640 × 360 frame.


2. **Framing and Crop Verification (`step8_02_framing_and_crop.py`)**
* Capture a sample image to verify the camera is level, centered, and unobstructed by the chassis.
* Inspect the output files (`full 640×360`, `cropped 640×280`, and `marked-crop`) to ensure field lines and obstacles fit within the lower 280-pixel region. Adjust the physical mount if needed.


3. **Static Dataset Capture (`step8_03_capture_dataset.py SCENARIO_NAME`)**
* Manually position the robot in critical field positions (without altering the camera mount) and capture images for:
* **Start Position (SP):** Centered straightaway.
* **Close to Walls (CL):** Near left and right boundaries.
* **Approaching Corners (AC):** Approaching turns.
* **Field Lines (BOL):** Blue and orange boundary lines.
* **Obstacles (FRG):** Red and green obstacles at both near and far distances.
* **Parking Area (PP):** Pink parking zones.
* *(Optional)* Re-run scenarios under varying brightness levels to evaluate lighting resilience.




4. **Vision Pipeline Test (`step8_04_pipeline_test.py`)**
* Feed the static dataset into the software pipeline to confirm it processes crops without crashing and successfully generates initial color masks (blue, orange, green, red, pink) and wall/floor detections.



---

**Pass Requirements**

* Sensor correctly identified as `imx708` on Pi 5.
* Physical camera is rigid, level, centered, and documented.
* Clean 640 × 280 cropped images generated with zero chassis obstruction.
* Crucial track elements (walls, obstacles, colored lines) remain fully visible within the 75° field of view.
* Pipeline successfully generates basic detection masks across all saved static scenarios.
