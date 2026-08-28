#Step 6 — Straight-line distance test

#1. Prepare a separate PlatformIO project

#In the Raspberry Pi terminal through Remote SSH, run:
#export PATH="$HOME/.platformio/penv/bin:$PATH"

#mkdir -p /home/admin/MyRobot/step6_straight_line_test/src
#mkdir -p /home/admin/MyRobot/step6_straight_line_test/lib

#cp -R /home/admin/Projects/WRO2026-CLM/code/arduino/lib/FlexyStepper-master \
#/home/admin/MyRobot/step6_straight_line_test/lib/FlexyStepper

#cp -R /home/admin/Projects/WRO2026-CLM/code/arduino/lib/Servo-master \
#/home/admin/MyRobot/step6_straight_line_test/lib/Servo

#cd /home/admin/MyRobot/step6_straight_line_test

#In VS Code, select:
#File → Open Folder
#Open:
#/home/admin/MyRobot/step6_straight_line_test

#2. Create platformio.ini
#Create this file:
#/home/admin/MyRobot/step6_straight_line_test/platformio.ini

#Paste:
#[env:uno]
#platform = atmelavr
#board = uno
#framework = arduino
#monitor_speed = 115200

#3. Create src/main.cpp
#Create:
#/home/admin/MyRobot/step6_straight_line_test/src/main.cpp
#Paste the C++ code attached separately (titled "step6_main.cpp")

#4. Compile the program
#Disconnect the motor battery before compiling and uploading.

#In the project terminal:
#cd /home/admin/MyRobot/step6_straight_line_test
#pio run

#Expected ending:
#[SUCCESS]

#If pio is not found:
#/home/admin/.platformio/penv/bin/pio run

#5. Find the Arduino port

#Run:
#pio device list
#export PATH="$HOME/.platformio/penv/bin:$PATH"
#pio run

#You should find:
#/dev/ttyACM0
#If it displays /dev/ttyACM1, use that instead in every following command.

#6. Upload

#Keep the motor battery disconnected while uploading:
#pio run --target upload --upload-port /dev/ttyACM0

#Expected:
#[SUCCESS]

#7. First test with the wheels raised
#Before putting the robot on the floor, verify the new program.
#Raise the wheels.
#Connect the motor battery.
#Keep hands, wires, and loose objects away from the drivetrain.

#Open the serial monitor:
#pio device monitor --port /dev/ttyACM0 --baud 115200

#Enter:
#STATUS

#Then:
#A99

#Then:
#GO

#The program waits five seconds, accelerates, runs, decelerates, stops, and prints:
#DONE
#Driver disabled.

#Expected duration is approximately 11 seconds.

#If the wheels rotate backward    

#Exit the monitor with:
#Ctrl + ]

#Change:
#constexpr int FORWARD_SIGN = -1;
#to:
#constexpr int FORWARD_SIGN = 1;

#Upload again. Do not reverse the motor wires just for this.

#8. Prepare the floor test
#Use a flat, hard floor—not carpet.
#You need:
#Measuring tape
#Painter’s tape
#Straight reference line
#At least 1.5–2 metres of clear space
#Paper for recording results
#Make these marks:
#A straight centerline at least 1.2 m long.
#A perpendicular starting line.
#A perpendicular target line exactly 1000 mm from the starting line.
#Use the same chassis reference point for every measurement. The easiest reference is the center of the front axle projected onto the floor.
#Position the robot so that:
#Front wheels are straight.
#Chassis center is over the reference line.
#Front-axle reference is exactly over the starting line.
#No cable is pulling sideways.
#At least 50 cm of additional stopping space remains after the target.
#The USB cable should form a loose loop behind the robot. A tight cable can steer the robot and ruin the measurement.

#9. Run the 1 m test

#Open the monitor:
#pio device monitor --port /dev/ttyACM0 --baud 115200

#Enter:
#A99

#Then:
#GO

#During the five-second delay:
#Move away from the robot.
#Stand beside or behind it, not directly in its path.
#Be ready to disconnect motor power if it behaves unexpectedly.

#To request a controlled stop, enter:
#STOP

#That command decelerates the motor. The battery switch remains the emergency stop.

#10. Measure the result
#After the robot stops, measure:
#Forward distance: starting reference to final reference.
#Distance error: actual distance minus 1000 mm.
#Lateral deviation: sideways distance from the original centerline.
#Direction of drift: left or right.

#Record three runs:
#Run
#Servo angle
#Steps
#Actual distance
#Lateral deviation
#Drift

#Return the robot to exactly the same starting position for every run.

#11. Correct the steering drift
#Your calibrated steering direction is:
#Decreasing angle → right
#Increasing angle → left

#Therefore:
#Robot behavior
#Drifts left --> A98, then GO
#Drifts right --> A100, then GO
#Travels straight --> Keep A99

#Only adjust by one degree at a time.
#Run three trials for each candidate value. Do not choose an angle based on a single run.
#If it needs more than approximately three degrees of correction from 99, stop trimming electronically and inspect:
#Front-wheel alignment
#Steering-link lengths
#Loose servo horn
#Unequal tire contact
#Cable pulling the chassis
#Bent or tight steering linkage

#Once the best value is found, change:
#constexpr int SERVO_CENTER = 99;
#to the new result and upload again.

#12. Calibrate the travel distance
#First calculate the average of the three measured distances.

#You can calculate it on the Pi. Replace 930 with your measured average:
#python3 - <<'PY'
#old_steps = 6400
#target_mm = 1000
#actual_mm = 930

#new_steps = round(old_steps * target_mm / actual_mm)

#print("New TEST_STEPS =", new_steps)
#PY

#Then change:
#constexpr long TEST_STEPS = 6400L;
#to the calculated number, for example:
#constexpr long TEST_STEPS = 6882L;

#Exit the serial monitor first:
#Ctrl + ]

#Then upload:
#pio run --target upload --upload-port /dev/ttyACM0

#Repeat three floor runs.

#Step 6 pass conditions
#A practical pass is:
#Three complete runs without Arduino resets.
#No motor stalls or obviously missed steps.
#Robot stops automatically.
#Average distance within approximately ±30 mm of 1000 mm.
#Lateral deviation within approximately ±50 mm after 1 m.
#Results reasonably repeatable across all three runs.
#No thermal shutdown, burning smell, or loose drivetrain parts.
#Some extra noise during acceleration and braking is expected from Step 5. Stop the test if the drivetrain starts jumping, the motor loses synchronization, or anything becomes unusually hot.
#One important repository detail: its current Arduino files still contain the old servo center around 88 and broader limits, while your measured values are 74, 99, and 124. This Step 6 firmware uses your real calibration; later, those values should also be transferred into the main repository firmware. Repository Arduino firmware
#After the first three runs, send me:
#The three actual distances
#Lateral deviation and direction for each run
#Whether 6400 steps moved forward
#A top-down photo with the front wheels at A99
#A side photo of one wheel beside a ruler
#A close-up of the gears and DRV8825 microstep jumper area
#With those measurements, I can calculate the final TEST_STEPS, steps per millimetre, and best steering-center value.

