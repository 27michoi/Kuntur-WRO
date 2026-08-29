# Step 9:


# 1. Prepare Step 9

# Keep the motor battery disconnected and secure every cable outside the
# camera view.

# Terminal commands:

# cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package
# source ../.venv/bin/activate

# mkdir -p step9_tests
# mkdir -p ../../step9_results/logs

# touch step9_tests/__init__.py

# Check the Raspberry Pi status and camera:

# vcgencmd get_throttled
# rpicam-hello --list-cameras

# Expected:

# throttled=0x0


# 2. Create mask_verify.py

# Create:
# /home/admin/Projects/WRO2026-CLM/code/XX_2025_package/step9_tests/mask_verify.py

# The code is in file mask_verify.py.


# 3. Create the summary script

# Create:
# /home/admin/Projects/WRO2026-CLM/code/XX_2025_package/step9_tests/summary.py

# The code is in file summary.py.


# Compile both scripts:

# python -m py_compile \
#   step9_tests/mask_verify.py \
#   step9_tests/summary.py

# No output means both files are syntactically correct.


# 4. Physical scene positions

# Scene          Physical arrangement

# empty          Plain field area without colored line or obstacle
# wall           Black wall clearly visible; no colored obstacle
# blue           Blue line across the lower-middle field of view
# orange         Orange line across the lower-middle view
# green_near     Green obstacle 300–400 mm from lens
# green_far      Green obstacle 700–900 mm from lens
# red_near       Red obstacle 300–400 mm from lens
# red_far        Red obstacle 700–900 mm from lens
# mixed          Natural course view with wall, line and obstacle

# The distances are measured from the lens, so the missing lens-to-axle
# measurement does not affect Step 9.


# 5. Normal-lighting tests

# Reposition the stationary robot before every command.

# python -m step9_tests.mask_verify empty normal 2>&1 \
#   | tee ../../step9_results/logs/empty_normal.log

# python -m step9_tests.mask_verify wall normal 2>&1 \
#   | tee ../../step9_results/logs/wall_normal.log

# python -m step9_tests.mask_verify blue normal 2>&1 \
#   | tee ../../step9_results/logs/blue_normal.log

# python -m step9_tests.mask_verify orange normal 2>&1 \
#   | tee ../../step9_results/logs/orange_normal.log

# python -m step9_tests.mask_verify green_near normal 2>&1 \
#   | tee ../../step9_results/logs/green_near_normal.log

# python -m step9_tests.mask_verify green_far normal 2>&1 \
#   | tee ../../step9_results/logs/green_far_normal.log

# python -m step9_tests.mask_verify red_near normal 2>&1 \
#   | tee ../../step9_results/logs/red_near_normal.log

# python -m step9_tests.mask_verify red_far normal 2>&1 \
#   | tee ../../step9_results/logs/red_far_normal.log

# python -m step9_tests.mask_verify mixed normal 2>&1 \
#   | tee ../../step9_results/logs/mixed_normal.log


# 6. Bright-lighting tests

# Use brighter overhead lighting without shining a lamp directly into
# the lens.

# python -m step9_tests.mask_verify empty bright 2>&1 \
#   | tee ../../step9_results/logs/empty_bright.log

# python -m step9_tests.mask_verify wall bright 2>&1 \
#   | tee ../../step9_results/logs/wall_bright.log

# python -m step9_tests.mask_verify blue bright 2>&1 \
#   | tee ../../step9_results/logs/blue_bright.log

# python -m step9_tests.mask_verify orange bright 2>&1 \
#   | tee ../../step9_results/logs/orange_bright.log

# python -m step9_tests.mask_verify green_near bright 2>&1 \
#   | tee ../../step9_results/logs/green_near_bright.log

# python -m step9_tests.mask_verify red_near bright 2>&1 \
#   | tee ../../step9_results/logs/red_near_bright.log


# 7. Dark-lighting tests

# The field must remain visible. "Dark" should not mean that the scene
# is too dark for the camera to interpret.

# python -m step9_tests.mask_verify empty dark 2>&1 \
#   | tee ../../step9_results/logs/empty_dark.log

# python -m step9_tests.mask_verify wall dark 2>&1 \
#   | tee ../../step9_results/logs/wall_dark.log

# python -m step9_tests.mask_verify blue dark 2>&1 \
#   | tee ../../step9_results/logs/blue_dark.log

# python -m step9_tests.mask_verify orange dark 2>&1 \
#   | tee ../../step9_results/logs/orange_dark.log

# python -m step9_tests.mask_verify green_near dark 2>&1 \
#   | tee ../../step9_results/logs/green_near_dark.log

# python -m step9_tests.mask_verify red_near dark 2>&1 \
#   | tee ../../step9_results/logs/red_near_dark.log


# 8. Generate the comparison table

# python -m step9_tests.summary 2>&1 \
#   | tee ../../step9_results/logs/summary.log

# Verify the generated files:

# find ../../step9_results \
#   -type f \( -name "*.jpg" -o -name "*.json" -o -name "*.txt" \
#   -o -name "*.csv" -o -name "*.log" \) \
#   | sort

# vcgencmd get_throttled

# du -sh ../../step9_results


# 9. Pass criteria

# Step 9 passes when:

# Wall:
# - binary.jpg distinguishes black walls from the floor.
# - clean.jpg removes isolated noise without deleting the walls.
# - polygon.jpg presents continuous usable wall boundaries.

# Blue:
# - blue_mask forms a strong connected line.
# - orange_mask remains substantially smaller.
# - The blue overlay aligns with the real blue line.

# Orange:
# - orange_mask forms the correct line.
# - blue_mask remains substantially smaller.

# Green/red obstacles:
# - The correct mask produces a dominant component around the obstacle.
# - The competing-color mask remains small.
# - combined_mask contains the obstacle.
# - The bounding box and centroid align with the physical pillar.

# Empty:
# - Each color mask ideally covers less than approximately 1% of the image.
# - No large colored false-positive component appears.

# Bright/dark:
# - Correct objects remain detectable.
# - Masks do not suddenly cover large portions of the frame.

# The numeric rules are screening heuristics, not absolute truth. Far
# objects naturally produce fewer pixels, so the saved overlays are the
# final evidence.


# 10. Results to send for evaluation

# Send:

# step9_results/mask_summary.csv
# normal/wall/crop.jpg
# normal/wall/binary.jpg
# normal/wall/clean.jpg
# normal/wall/polygon.jpg
# normal/blue/blue_mask.jpg
# normal/blue/blue_mask_overlay.jpg
# normal/orange/orange_mask.jpg
# normal/orange/orange_mask_overlay.jpg
# normal/green_near/green_mask_overlay.jpg
# normal/green_far/green_mask_overlay.jpg
# normal/red_near/red_mask_overlay.jpg
# normal/red_far/red_mask_overlay.jpg
# normal/green_near/obstacle.jpg
# normal/red_near/obstacle.jpg
# normal/mixed/display.jpg
# empty_normal.log
# summary.log

# Also include the final output from:

# vcgencmd get_throttled

# If any mask is blank or noisy, do not modify the repository HSV limits
# yet. Send the corresponding crop.jpg, mask, overlay, metrics.json, and
# log first. The threshold adjustment should be calculated from the
# actual evidence.
