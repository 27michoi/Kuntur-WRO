# STEP 7: CONSTANT-RADIUS TEST

# IMPORTANT:
# This document contains instructions and notes for a robot project.
# The actual robot program for this step is written in C++, not Python.

# Check the C++ code attached separately in the folder.

# The C++ file should be saved as:
# step7_constant_radius_test/src/main.cpp


# MEASUREMENTS

# Wheelbase L:              167 mm
# Rear track width T:       139 mm
# Wheel diameter:            56 mm
# Wheel width:               27 mm
# Current servo centre:      82
# Motor speed:               600

# LOWER VALUES → RIGHT
# HIGHER VALUES → LEFT


# INITIAL TEST MEASUREMENTS

# Angle          Start to 2 (mm)    2 to 3 (mm)    Start to 3 (mm)
# 75 (Right)     1067               1067           1945
# 75 (Right)     1070               1049           1930
# 75 (Right)     1030               1060           1890
# 66 (Right)      932                932           1050
# 90 (Left)      1048               1065           1962
# 90 (Left)      1054               1040           1961
# 90 (Left)      1067               1052           1971
# 105 (Left)      830                820            547

# Target steps: 1800

# Command        Direction          Radius
# 66             Right              564.0 mm
# 105            Left               437.3 mm


# 1. PREPARE THE PLATFORMIO PROJECT

# Run the following commands in Terminal:
#cd ~/Projects/MyRobot
#mkdir -p step7_constant_radius_test/src
#mkdir -p step7_constant_radius_test/results
#cp step6_straight_line_test/platformio.ini \
#tep7_constant_radius_test/platformio.ini
#cp -a step6_straight_line_test/lib \
#step7_constant_radius_test/

# Open the new C++ program:
#nano step7_constant_radius_test/src/main.cpp

# Then paste the C++ code attached separately in the folder.

# Save with:
#
# Ctrl+O
# Enter
# Ctrl+X


# 2. COMPILE AND UPLOAD

# Run in Terminal:
#cd ~/Projects/MyRobot/step7_constant_radius_test
#pio run

# If compilation succeeds:
#pio device list
#pio run --target upload
#pio device monitor

# If pio is not found, use:
#~/.platformio/penv/bin/pio run
#~/.platformio/penv/bin/pio run --target upload
#~/.platformio/penv/bin/pio device monitor

# Exit the monitor with Ctrl+C.


# 3. CHECK STEERING SAFELY

# First lift the robot so the driven wheels cannot propel it.
# Keep fingers away from the steering linkage.
# The motor driver stays disabled while the program says IDLE.

# Enter these commands one at a time in the serial monitor:
#CENTER
#A80
#A78
#A76
#CENTER
#A84
#A86
#A88
#CENTER

# For every position, check:
# - The linkage does not touch a mechanical stop.
# - The servo does not buzz or strain.
# - The tires do not rub the chassis.
# - The wheels return to straight at CENTER.

# If it strains, immediately enter:
#CENTER

# Or switch off robot power.

# Determine which command turns the robot left when travelling forward:
#LOW
# Then:
#HIGH

# Record this mapping:
#
# 76 produces: left or right
# 88 produces: left or right

# We should not assume that a lower number means left.


# 4. PERFORM TWO SHORT SAFETY RUNS

# Use a clear floor with at least several metres of space.
# Keep the USB cable loose so it cannot pull on the robot.
# Start with approximately 246 mm of travel.

# Enter:
#SHORT
#LOW
#STATUS
#GO

# After it stops:
#CENTER

# Return the robot to the starting point and test the other side:
#SHORT
#HIGH
#STATUS
#GO

# Check that both runs:
# - Curve smoothly.
# - Stop automatically.
# - Do not cause steering binding.
# - Do not cause excessive wheel slipping.
# - Travel forward rather than backward.

# STOP is a controlled deceleration, not an instant emergency stop.
# Keep the robot's power switch accessible.


# 5. SELECT THE MEASUREMENT DISTANCE

# If both short runs are safe, use:
#MEDIUM

# This travels approximately 492 mm.

# If the curve is too short to measure accurately and you have enough space,
# use:
#FULL

# This travels approximately 984 mm.

# Use the same step count for every left and right measurement.


# THREE-POSITION METHOD

# Mark the midpoint of the rear axle—not the front wheels or the camera.

# For each test:

# 1. Place the robot down and mark its rear-axle midpoint as P1.

# 2. Select the steering and distance:
#MEDIUM
#LOW

# 3. Run:
#GO

# 4. When RUN COMPLETE appears, mark the new rear-axle midpoint as P2.

# 5. Do not move, rotate, or lift the robot.

# 6. Run the identical segment again:
#GO

# 7. Mark the final rear-axle midpoint as P3.

# Now measure only these three straight-line distances:
# d12: P1 to P2
# d23: P2 to P3
# d13: P1 to P3

# No curve tracing and no sagitta needed.
# Geometry does the annoying work for us.


# HOW TO MARK THE AXLE MIDPOINT

# After each run finishes and the motor disables:

# 1. Locate the midpoint between the two rear wheels.
# 2. Hold a ruler vertically down from that midpoint.
# 3. Put a small masking-tape cross on the floor.
# 4. Label it P1, P2, or P3.

# Keep the USB cable completely slack so it does not pull the robot sideways.


# FINAL MEASUREMENTS

# Angle          Start to 2 (mm)    2 to 3 (mm)    Start to 3 (mm)
# 75 (Right)     1067               1067           1945
# 75 (Right)     1070               1049           1930
# 75 (Right)     1030               1060           1890
# 66 (Right)      932                932           1050
# 90 (Left)      1048               1065           1962
# 90 (Left)      1054               1040           1961
# 90 (Left)      1067               1052           1971
# 105 (Left)      830                820            547

# Target steps: 1800

# Command        Direction          Radius
# 66             Right              564.0 mm
# 105            Left               437.3 mm


# UPDATED DISTANCE ESTIMATE

# Across the six final trials, 1800 steps corresponded to approximately 1085 mm of path length.
# Steps per metre ≈ 1659.
# Use 1660 as the new provisional value.

# C++ code:
# constexpr long STEPS_PER_METER = 1660L;

# This should still be verified later with one direct straight-line measurement because it was calculated from curved paths.
