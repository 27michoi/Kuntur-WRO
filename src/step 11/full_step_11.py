# Step 11


# 1. Install the Step 11 script

# On the Raspberry Pi:
# cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package
# source ../.venv/bin/activate
# mkdir -p step11_tests
# mkdir -p ../../step11_results/logs
# mkdir -p ../../step11_results/frames
# touch step11_tests/__init__.py

# If the downloaded script is in the Pi's Downloads folder:
# cp ~/Downloads/step11_one_corner_low_speed.py \
#   step11_tests/one_corner_low_speed.py

# Confirm:
# ls -lh step11_tests/one_corner_low_speed.py

# If the file was downloaded onto another computer, open the linked file,
# copy its contents, and paste them into:
# nano step11_tests/one_corner_low_speed.py

# Save with Ctrl+O, press Enter, and exit with Ctrl+X.

# 2. Verify the script

# Compile it:
# python -m py_compile \
#   step11_tests/one_corner_low_speed.py

# No output means the syntax passed.

# Check repository imports:
# python -c "from classes.camera_manager import CameraManager; from classes.image_algoriths import ImageAlgorithms; from classes.arduino_comms import ArduinoComms; print('Step 11 imports OK')"

# Expected:
# Step 11 imports OK

# Do not upload another Arduino sketch.
# The original competition firmware already running from Step 10 is correct.


# 3. Understand the automatic stopping

# The script initially sets a maximum of 6500 steps as a safety limit.

# When the real wall-following algorithm reports the corner, it replaces
# that target with:
# 4000 steps after corner detection

# This distance was selected using the turning behaviour measured during
# Step 7. It should allow the robot to complete the curve and enter the
# following straight.

# Expected successful stop reason:
# CORNER_EXIT_COMPLETE

# If the robot never recognizes the corner, it stops at the fallback limit
# and reports:
# MAX_DISTANCE_COMPLETE_NO_CORNER

# That is a safe stop, but it is not a Step 11 pass.


# 4. Prepare the field

# Use the actual WRO field with:
# - One clear corner.
# - No red or green obstacles.
# - At least approximately 400–500 mm of straight before the corner.
# - A clear section after the corner.
# - The robot in the same normal lateral position used for Step 10.
# - Robot aligned parallel to the starting straight.
# - Motor and USB cables unable to snag.

# Colored field lines can remain. They are part of the real field and the
# wall pipeline already accounts for them.

# For the left test, position the robot so the physical route turns left.

# For the right test, approach a corner that physically turns right.
# You can use the same field corner by approaching it from the opposite
# direction.

# Do not put the robot directly at the corner.
# It needs a short straight approach so the wall follower establishes a
# stable reference first.


# 5. Left-corner test

# Keep someone near the robot's power switch.

# Start the test:
# python -m step11_tests.one_corner_low_speed \
#   --direction left \
#   --max-steps 6500 \
#   --exit-steps 4000 \
#   2>&1 | tee ../../step11_results/logs/left_console.log

# During the five-second countdown, move away from the robot.

# Expected behaviour:
# - Robot moves forward.
# - It follows the wall at speed 600.
# - Servo commands remain between 75–90.
# - Near the corner, the terminal prints something similar to:

# Corner accepted at 2.45s (frame 47).

# - The robot turns left through the corner.
# - It enters the following straight.
# - It stops automatically.
# - It does not touch either wall.
# - It does not repeatedly swing left and right.

# During the corner, the servo may remain at one limit for several frames.
# That is acceptable.

# Repeated switching from 75 to 90 and back would indicate oscillation.

# Successful final output:
# Corner accepted: True
# Completed target: True
# Stop reason: CORNER_EXIT_COMPLETE
# Technical result: PASS


# 6. Right-corner test

# Reposition the robot before running the second test.
# Do not simply leave it where the left test stopped.

# Run:
# python -m step11_tests.one_corner_low_speed \
#   --direction right \
#   --max-steps 6500 \
#   --exit-steps 4000 \
#   2>&1 | tee ../../step11_results/logs/right_console.log

# Expect the same sequence, but the robot must turn right and enter the
# next straight.

# Successful output:
# Corner accepted: True
# Completed target: True
# Stop reason: CORNER_EXIT_COMPLETE
# Technical result: PASS


# 7. When to stop immediately

# Press Ctrl+C if:
# - Robot moves backward.
# - It turns opposite to the physical corner.
# - It is clearly about to contact a wall.
# - A cable catches.
# - Steering remains stuck in the wrong direction.
# - It leaves the intended field path.

# The script should send speed 0 during cleanup.
# If necessary, use the robot's motor power switch.

# Do not repeat a failed run several times without reviewing its CSV and
# frames.


# 8. Result files

# List the generated CSV files:
# find ../../step11_results/logs \
#   -type f -name "*.csv" | sort

# List the console logs:
# find ../../step11_results/logs \
#   -type f -name "*console.log" | sort

# List the diagnostic images:
# find ../../step11_results/frames \
#   -type f -name "*.jpg" | sort

# Images containing the accepted corner have "_CORNER" in their filename.


# Step 11 pass requirements

# Both directions must satisfy:
# - Original competition Arduino firmware remained installed.
# - Speed remained 600.
# - Servo commands remained within 75–90.
# - Corner accepted: True.
# - Completed target: True.
# - Stop reason: CORNER_EXIT_COMPLETE.
# - Robot turned in the correct direction.
# - Robot completed approximately 90° of turning.
# - Robot entered the next straight.
# - No wall contact.
# - No strong or continuous oscillation.
# - No reverse motion.
# - CSV and diagnostic images were generated.

# A single-frame is_corner=1 is normal because the repository detects a
# corner from a sudden change between consecutive wall measurements.


# If the stopping distance is slightly wrong

# Only adjust this if the technical result passes but the physical stopping
# position is unsuitable.

# If it stops before finishing the curve:
# --exit-steps 4500

# If it travels too far down the following straight:
# --exit-steps 3500

# Do not change servo limits, speed, gains, target sign, or repository
# classes at this stage.


# What to send for review

# Send:
# - left_console.log
# - right_console.log
# - The corresponding left and right CSV files
# - Three images from each run:
#   - Straight approach
#   - _CORNER frame
#   - Exit straight

# Record these physical observations:

# Left corner completed: yes/no
# Left wall contact: yes/no
# Left exit aligned: yes/no
# Left oscillation: none/mild/strong

# Right corner completed: yes/no
# Right wall contact: yes/no
# Right exit aligned: yes/no
# Right oscillation: none/mild/strong

# If both console summaries say PASS and the physical observations are
# acceptable, Step 11 is complete and we proceed to Step 12:
# one complete lap.

