# Step 10

# 1. Restore the original competition Arduino firmware


# Navigate to the Arduino project:
# cd /home/admin/Projects/WRO2026-CLM/code/arduino

# Compile the original firmware:
# pio run

# Upload the firmware:
# pio run --target upload

# Check the serial device:
# ls -l /dev/ttyACM* /dev/ttyUSB* 2>/dev/null
#
# The original firmware accepts:
# m<angle>,<speed>.
# for continuous movement and:
# <steps>!
# for a limited target distance.

# This is the same protocol used by the repository's ArduinoComms.
# Do not leave the PlatformIO device monitor open because Python cannot
# use the serial port while the monitor owns it.


# 2. Prepare Step 10

# Navigate to the Python project:
# cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package

# Activate the virtual environment:
# source ../.venv/bin/activate

# Create the Step 10 directories:
# mkdir -p step10_tests
# mkdir -p ../../step10_results/logs
# mkdir -p ../../step10_results/frames

# Create the Python package initializer:
# touch step10_tests/__init__.py

# Check the required imports:
# python -c "import cv2, numpy, serial; from classes.camera_manager import CameraManager; from classes.image_algoriths import ImageAlgorithms; from classes.arduino_comms import ArduinoComms; print('Step 10 imports OK')"


# 3. Create the competition wall-following test

# Create the test file:
# nano step10_tests/wall_follow_low_speed.py

# The code is in the file wall_follow_low_speed.py


# Save the file:
# Ctrl + O
# Enter
# Ctrl + X

# Compile-check the Python file:
# python -m py_compile \
#   step10_tests/wall_follow_low_speed.py

# No output means the syntax is valid.


# 4. Raised-wheel verification

# Raise the driven wheels before the first run.

# Run the left direction:
# python -m step10_tests.wall_follow_low_speed \
#   --direction left \
#   --steps 500 \
#   --port /dev/ttyACM0

# During the countdown, hold or position the field wall where the camera
# can see it.

# Confirm:
# - The motor begins after the countdown.
# - The servo changes while the motor is moving.
# - The servo never exceeds 75–90.
# - The motor stops automatically.
# - The output says:

# Completed target: True
# Stop reason: TARGET_COMPLETE

# Repeat for the right direction:
# python -m step10_tests.wall_follow_low_speed \
#   --direction right \
#   --steps 500 \
#   --port /dev/ttyACM0

# If the Arduino uses another device, replace /dev/ttyACM0 with the
# appropriate device path.


# 5. First floor runs

# Place the robot on a straight WRO section, well before any corner.
# Start centred and aligned straight.

# Left direction, approximately 300 mm:
# python -m step10_tests.wall_follow_low_speed \
#   --direction left \
#   --steps 500

# Right direction, approximately 300 mm:
# python -m step10_tests.wall_follow_low_speed \
#   --direction right \
#   --steps 500

# Both directions should pass before increasing the distance.


# 6. Longer straight-wall run

# Approximately 600 mm:
# python -m step10_tests.wall_follow_low_speed \
#   --direction left \
#   --steps 1000
# python -m step10_tests.wall_follow_low_speed \
#   --direction right \
#   --steps 1000

# If those runs pass, test approximately one metre:
# python -m step10_tests.wall_follow_low_speed \
#   --direction left \
#   --steps 1660
# python -m step10_tests.wall_follow_low_speed \
#   --direction right \
#   --steps 1660

# Keep all these runs on a straight section.
# Step 11 will deliberately introduce the first corner.


# Step 10 completion requirements

# Step 10 passes when:

# - The original Arduino competition firmware is running.
# - The test uses the repository's real CameraManager.
# - The test uses the repository's real calculate_servo_angle_from_walls().
# - The test uses the repository's real ArduinoComms.
# - Both left and right directions correct toward the intended path.
# - Servo commands stay between 75 and 90.
# - Speed remains 600.
# - The robot stops automatically at the target.
# - The robot completes a straight run of approximately one metre
#   in each direction.
# - The robot does not touch the wall.
# - The robot does not show continuous left-right oscillation.
# - Diagnostic frames and CSV logs are generated.


# What to send after testing

# Send the final console output from the 1660-step left run.

# Send the final console output from the 1660-step right run.

# Find the corresponding CSV files:
# find ../../step10_results/logs \
#   -type f -name "*.csv" | sort

# Find the diagnostic images:
# find ../../step10_results/frames \
#   -type f -name "*.jpg" | sort
#
# Approximately three representative images from each final run should
# be provided.

# Report:
# Left run wall contact: no
# Right run wall contact: no
# Left run oscillation: none
# Right run oscillation: none

# No additional physical measurements are needed for Step 10.

# Once both final runs pass, Step 10 is complete and the project can move
# to Step 11: one corner.


