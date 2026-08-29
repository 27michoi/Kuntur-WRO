# Step 12 


# 1. Prepare the field

# For this step:
# - Remove all green/red obstacles and parking pieces.
# - Use the complete WRO wall layout.
# - Keep the lighting exactly as it was during the successful Step 11 test.
# - Place the robot in the normal starting area, on a straight.
# - Place it before the first blue/orange line sequence.
# - Align it straight and approximately centred.
# - Keep the USB cable loose.
# - Have someone ready to press Ctrl+C or switch off the robot.

# Do not upload different Arduino firmware.
# Continue using the competition firmware that worked in Step 11.


# 2. Install the script

# The downloaded file must first exist on the Raspberry Pi.

# If you downloaded it using the Pi's browser, confirm:
# ls -lh ~/Downloads/step12_one_complete_lap.py

# Then install it:
# cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package
# source ../.venv/bin/activate
# mkdir -p step12_tests
# mkdir -p ../../step12_results/logs
# mkdir -p ../../step12_results/frames
# touch step12_tests/__init__.py
# cp ~/Downloads/step12_one_complete_lap.py \
#   step12_tests/one_complete_lap.py

# Confirm:
# ls -lh step12_tests/one_complete_lap.py


# 3. Verify the script

# Compile the script:
# python -m py_compile step12_tests/one_complete_lap.py

# No output means it compiled successfully.

# Check the required imports:
# python - <<'PY'
# from classes.camera_manager import CameraManager
# from classes.image_algoriths import ImageAlgorithms
# from classes.context_manager import ContextManager
# from classes.lap_tracker import LapTracker
# from classes.arduino_comms import ArduinoComms
# print("Step 12 imports OK")
# PY

# Expected:
# Step 12 imports OK

# Check the Arduino:
# ls -l /dev/ttyACM*

# Normally you should see:
# /dev/ttyACM0


# 4. How the test works

# The script uses:
# - Real CameraManager.
# - Real calculate_servo_angle_from_walls().
# - Real LapTracker.
# - Real ContextManager.
# - Real ArduinoComms.
# - Speed 600.
# - Servo centre 82.
# - Left-direction limits 75–90.
# - Right-direction limits 72–90.

# The robot does not stop based on a guessed travel distance.
# The repository's LapTracker detects the blue/orange sequence four times:

# Quarter 1/4
# Quarter 2/4
# Quarter 3/4
# Quarter 4/4

# After 4/4, it stops the motor automatically.

# The 25000-step target and 50-second timeout are only emergency limits.


# 5. Run one complete lap

# Since the final Step 11 calibration was the right direction, test right
# first.

# Reposition the robot at the normal starting point, facing the
# right-direction competition route.

# Run:
# cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package
# source ../.venv/bin/activate
# python -u -m step12_tests.one_complete_lap \
#   --direction right \
#   2>&1 | tee ../../step12_results/logs/right_console.log

# If the course is arranged for left-direction travel instead, use:
# python -u -m step12_tests.one_complete_lap \
#   --direction left \
#   2>&1 | tee ../../step12_results/logs/left_console.log

# Only one direction is required for Step 12.
# Step 11 already demonstrated that the robot can negotiate individual
# corners in both directions.


# 6. What to expect

# During the five-second countdown, move away from the course.

# The robot should:
# - Begin moving forward at speed 600.
# - Follow the first straight without strong oscillation.
# - Complete the first corner.
# - Print "Quarter 1/4 detected".
# - Continue through the remaining straights and corners.
# - Print quarter progress until 4/4.
# - Return approximately to its starting section.
# - Stop automatically after completing one lap.

# The terminal should eventually show something similar to:
# Quarter 1/4 detected
# Quarter 2/4 detected
# Quarter 3/4 detected
# Quarter 4/4 detected
# One complete lap detected. Motor stopped.

# Final output should be similar to:
# Step 12 run complete
# Quarter-laps detected: 4/4
# Completed lap: True
# Stop reason: LAP_COMPLETE
# Technical result: PASS

# Corner events observed is diagnostic only.
# It does not have to equal exactly four because the repository's corner
# detector can occasionally miss a single-frame corner event.

# The blue/orange LapTracker determines lap completion.


# 7. Stop the run if necessary

# Press:
# Ctrl+C

# immediately if:
# - The robot is about to touch a wall.
# - It travels in the wrong direction.
# - It passes a corner without turning.
# - It begins continuously oscillating.
# - It reaches the starting area but fails to stop.
# - The camera freezes.

# The cleanup code should command motor speed 0.

# Do not increase --max-steps or --timeout if the robot completes the
# physical lap but fails to register 4/4.
# That would indicate a line-detection problem, not insufficient distance.


# Step 12 completion requirements

# Step 12 passes when:
# - The competition Arduino firmware remains installed.
# - The real repository camera and control classes are used.
# - Speed remains 600.
# - The robot completes four physical corners.
# - It returns to the starting section.
# - It detects 4/4 quarter-laps.
# - It stops automatically.
# - It does not touch any wall.
# - It does not show strong continuous oscillation.
# - The servo remains within the direction's tested limits.
# - CSV logs and diagnostic images are generated.

# The console should report:
# Completed lap: True
# Stop reason: LAP_COMPLETE
# Technical result: PASS


# What to send for review

# Send the final console summary:
# tail -n 25 ../../step12_results/logs/right_console.log
# If you ran left, replace right_console.log with left_console.log.

# List the CSV files:
# find ../../step12_results/logs \
#   -type f -name "*.csv" | sort

# Send the newest CSV, plus these four observations:
# Completed one physical lap: yes/no
# Wall contact: yes/no
# Strong oscillation: yes/no
# Stopped automatically near the starting section: yes/no

# You only need to send images if the result says REVIEW, the robot stops
# early, or there is wall contact.

# If the technical output says PASS and all four physical answers are
# satisfactory, Step 12 is complete.
