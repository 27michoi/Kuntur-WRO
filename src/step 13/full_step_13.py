# Step 13


# 1. What each obstacle should do

# Directions are from the robot's point of view while facing forward.

# Obstacle     Required path
# Green        Robot passes on the right side of the obstacle
# Red          Robot passes on the left side of the obstacle

# The --direction argument means the robot's lap direction.
# It does not change which side of a colored obstacle is required.


# 2. Install the test script

# Run:
# cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package
# source ../.venv/bin/activate
# mkdir -p step13_tests
# mkdir -p ../../step13_results/logs
# mkdir -p ../../step13_results/frames
# touch step13_tests/__init__.py

# Open the new file:
# nano step13_tests/obstacle_avoidance_low_speed.py

# The code to copy-paste is in the file obstacle_avoidance_low_speed.py

# Save and exit:
# Press Ctrl+O
# Press Enter
# Press Ctrl+X

# This avoids using the Downloads folder completely.

# Compile it:
# python -m py_compile \
#   step13_tests/obstacle_avoidance_low_speed.py

# No output means compilation passed.

# Confirm the command exists:
# python -m step13_tests.obstacle_avoidance_low_speed --help


# 3. What the script is configured to use

# The script already contains the final calibration:
# Servo centre: 82
# Left-direction limits: 75–92
# Right-direction limits: 72–90
# Maximum Step 13 speed: 600

# It also uses the forward motor direction established in the working
# Step 10–12 tests.


# 4. Prepare the field

# Use one straight WRO field section.

# For every run:
# Remove every obstacle except the one being tested.
# Do not start immediately before a corner.
# Place the obstacle in a normal legal field position.
# Place the robot approximately 50–70 cm before the obstacle.
# Point the robot straight along the track.
# Make sure the requested colored obstacle is visible to the camera.
# Keep the USB cable loose.
# Keep fingers and loose clothing away from the wheels.
# Be ready to press Ctrl+C or switch off robot power.

# The program checks the obstacle with the motor stopped before starting.
# If it cannot confirm the requested color, it will not move.


# 5. First run: right direction with green

# Place only a green obstacle ahead of the robot.

# Run:
# cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package
# source ../.venv/bin/activate
# python -u -m step13_tests.obstacle_avoidance_low_speed \
#   --direction right \
#   --color green \
#   --steps 1700 \
#   2>&1 | tee ../../step13_results/logs/right_green_console.log

# Before movement

# The terminal should report something similar to:
# Preflight detections: expected=...
# Preflight passed. The expected obstacle is visible.
# Starting in 5...

# If it instead says:
# Motor will not start.
# Stop reason: PREFLIGHT_OBSTACLE_NOT_CONFIRMED

# That is a safe abort. Adjust the obstacle position or lighting and repeat
# the same command.

# Expected physical behaviour

# After the countdown:
# The robot starts straight.
# It follows the wall until obstacle steering becomes active.
# It steers to pass on the right side of the green obstacle.
# It clears the obstacle without touching it.
# It resumes normal wall following.
# It stops automatically.

# The right-direction servo must remain between 72 and 90.

# Successful terminal result

# Preflight passed: True
# Expected-color frames: 3 or more
# Obstacle-control frames: 3 or more
# Servo range observed: 72 to 90
# Completed target: True
# Stop reason: TARGET_COMPLETE
# Technical result: PASS

# The exact detection counts and servo range may differ.

# Do not continue to the next run if:
# It approaches the wrong side.
# It touches the obstacle or wall.
# It fails to steer.
# It switches sharply left and right repeatedly.
# The result is REVIEW.

# Send that run's final output first if any of those occur.


# 6. Right direction with red

# Reposition the robot at the original starting position.
# Replace the green obstacle with a red obstacle.

# Run:
# python -u -m step13_tests.obstacle_avoidance_low_speed \
#   --direction right \
#   --color red \
#   --steps 1700 \
#   2>&1 | tee ../../step13_results/logs/right_red_console.log

# Expected behaviour:
# The red obstacle is confirmed before movement.
# The robot passes on the left side of the red obstacle.
# It does not touch the obstacle or walls.
# It resumes wall following.
# It stops automatically.
# Servo remains between 72–90.
# Final result is PASS.


# 7. Left direction with green

# Reposition the robot for a left-direction lap and use only the green
# obstacle.

# Run:
# python -u -m step13_tests.obstacle_avoidance_low_speed \
#   --direction left \
#   --color green \
#   --steps 1700 \
#   2>&1 | tee ../../step13_results/logs/left_green_console.log

# Expected behaviour:
# It passes on the right side of the green obstacle.
# It clears the obstacle and resumes wall following.
# Servo remains between 75–92.
# It stops automatically.
# Final result is PASS.


# 8. Left direction with red

# Replace the green obstacle with the red obstacle and reposition the robot.

# Run:
# python -u -m step13_tests.obstacle_avoidance_low_speed \
#   --direction left \
#   --color red \
#   --steps 1700 \
#   2>&1 | tee ../../step13_results/logs/left_red_console.log

# Expected behaviour:
# It passes on the left side of the red obstacle.
# It clears the obstacle and resumes wall following.
# Servo remains between 75–92.
# It stops automatically.
# Final result is PASS.


# 9. If the distance is insufficient

# If the avoidance maneuver is correct but the robot stops beside the
# obstacle before completely clearing it, do not change any steering values.
# Repeat only that run with:
# --steps 2000

# For example:
# python -u -m step13_tests.obstacle_avoidance_low_speed \
#   --direction right \
#   --color green \
#   --steps 2000 \
#   2>&1 | tee ../../step13_results/logs/right_green_console_final.log

# Do not increase the speed during Step 13.


# 10. Review generated results

# List the CSV files:
# find ../../step13_results/logs \
#   -type f -name "*.csv" | sort

# List the saved images:
# find ../../step13_results/frames \
#   -type f -name "*.jpg" | sort

# Check the four console summaries:
# tail -n 25 ../../step13_results/logs/right_green_console.log
# tail -n 25 ../../step13_results/logs/right_red_console.log
# tail -n 25 ../../step13_results/logs/left_green_console.log
# tail -n 25 ../../step13_results/logs/left_red_console.log


# Step 13 completion requirements

# Step 13 is complete when all four combinations pass:
# Direction     Obstacle
# Right         Green
# Right         Red
# Left          Green
# Left          Red

# Every run must satisfy:
# Preflight passed: True
# Correct obstacle color detected
# Obstacle steering activated
# Green passed on the right
# Red passed on the left
# No obstacle contact
# No wall contact
# No strong continuous oscillation
# Robot resumes wall following after clearing the obstacle
# Servo remains inside the direction's calibrated limits
# Completed target: True
# Stop reason: TARGET_COMPLETE
# Technical result: PASS

