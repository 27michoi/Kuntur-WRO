**Step 8**
Measurement
Value
Wheelbase L
167 mm
Rear track width T
139 mm
Wheel diameter
56 mm
Wheel width
27 mm
Current servo centre
82
Motor speed
600

LOWER VALUES → RIGHT
HIGHER VALUES → LEFT

Angle
Start to 2 (mm)
2 to 3 (mm)
Start to 3 (mm)
75 (Right)
1067
1067
1945
75 (Right)
1070
1049
1930
75 (Right)
1030
1060
1890
66 (Right)
932
932
1050
90 (Left)
1048
1065
1962
90 (Left)
1054
1040
1961
90 (Left)
1067
1052
1971
105 (Left)
830
820
547

Target steps: 1800
Command
Direction
Radius
66
Right
564.0 mm
105
Left
437.3 mm


Step 7: Constant-radius test
1. Prepare the PlatformIO project
Run:
cd ~/Projects/MyRobot

mkdir -p step7_constant_radius_test/src
mkdir -p step7_constant_radius_test/results

cp step6_straight_line_test/platformio.ini \
  step7_constant_radius_test/platformio.ini

cp -a step6_straight_line_test/lib \
  step7_constant_radius_test/
Open the new program:
nano step7_constant_radius_test/src/main.cpp
Paste the following complete code.
#include <Arduino.h>
#include <FlexyStepper.h>
#include <Servo.h>

// Existing robot wiring
constexpr uint8_t ENABLE_PIN = 2;
constexpr uint8_t STEP_PIN = 9;
constexpr uint8_t DIR_PIN = 10;
constexpr uint8_t SERVO_PIN = 11;

// Current straight-ahead calibration
constexpr int SERVO_CENTER = 82;

// Wider Step 7 constant-radius test angles
constexpr int SERVO_LOW = 65;
constexpr int SERVO_HIGH = 100;

constexpr int SERVO_EXTREME_LOW = 60;
constexpr int SERVO_EXTREME_HIGH = 110;

// Expanded test limits
// Still below previous mechanical limits (74-124)
constexpr int TEST_MIN_ANGLE = 60;
constexpr int TEST_MAX_ANGLE = 110;

// Motor settings
constexpr float TEST_SPEED = 600.0F;
constexpr float ACCELERATION = 2000.0F;

// Based on previous measurement:
// 6400 steps ≈ 3500 mm
constexpr float ESTIMATED_STEPS_PER_MM = 6400.0F / 3500.0F;

// Test distances
constexpr long SHORT_STEPS = 450L;
constexpr long MEDIUM_STEPS = 900L;
constexpr long FULL_STEPS = 1800L;

constexpr long MIN_ALLOWED_STEPS = 100L;
constexpr long MAX_ALLOWED_STEPS = 1800L;

// Forward direction
constexpr int FORWARD_SIGN = 1;

constexpr unsigned long START_DELAY_MS = 5000UL;


Servo steeringServo;
FlexyStepper stepper;


enum RunState {
    IDLE,
    COUNTDOWN,
    MOVING,
    STOPPING
};


RunState state = IDLE;

String serialCommand;

unsigned long countdownStarted = 0;


int selectedAngle = SERVO_CENTER;
long selectedSteps = SHORT_STEPS;



void printHelp()
{
    Serial.println();
    Serial.println(F("=== STEP 7 CONSTANT-RADIUS TEST ==="));
    Serial.println(F(""));
    
    Serial.println(F("STEERING COMMANDS"));
    Serial.println(F("  CENTER  - steering position 82"));
    Serial.println(F("  LOW     - steering position 65"));
    Serial.println(F("  HIGH    - steering position 100"));
    Serial.println(F("  LEFT    - steering position 60"));
    Serial.println(F("  RIGHT   - steering position 110"));
    Serial.println(F("  Axx     - select custom angle"));
    
    Serial.println(F(""));
    
    Serial.println(F("DISTANCE COMMANDS"));
    Serial.println(F("  SHORT   - approximately 246 mm"));
    Serial.println(F("  MEDIUM  - approximately 492 mm"));
    Serial.println(F("  FULL    - approximately 984 mm"));
    Serial.println(F("  Nxxxx   - select custom steps"));

    Serial.println(F(""));
    
    Serial.println(F("CONTROL COMMANDS"));
    Serial.println(F("  GO      - five-second countdown"));
    Serial.println(F("  STOP    - stop robot"));
    Serial.println(F("  STATUS  - show settings"));
    Serial.println(F("  HELP    - show commands"));
    
    Serial.println();
}



void printStatus()
{
    Serial.println(F("----- STATUS -----"));

    Serial.print(F("Steering angle: "));
    Serial.println(selectedAngle);

    Serial.print(F("Target steps: "));
    Serial.println(selectedSteps);

    Serial.print(F("Estimated distance: "));
    Serial.print(selectedSteps / ESTIMATED_STEPS_PER_MM, 1);
    Serial.println(F(" mm"));

    Serial.print(F("Speed: "));
    Serial.println(TEST_SPEED);

    Serial.print(F("Acceleration: "));
    Serial.println(ACCELERATION);

    Serial.print(F("Motor position: "));
    Serial.println(stepper.getCurrentPositionInSteps());

    Serial.print(F("State: "));

    switch(state)
    {
        case IDLE:
            Serial.println(F("IDLE"));
            break;

        case COUNTDOWN:
            Serial.println(F("COUNTDOWN"));
            break;

        case MOVING:
            Serial.println(F("MOVING"));
            break;

        case STOPPING:
            Serial.println(F("STOPPING"));
            break;
    }
}



void setSteeringAngle(int newAngle)
{
    if(state != IDLE)
    {
        Serial.println(F("Stop robot before changing steering."));
        return;
    }


    if(newAngle < TEST_MIN_ANGLE || newAngle > TEST_MAX_ANGLE)
    {
        Serial.print(F("Rejected. Allowed range: "));
        Serial.print(TEST_MIN_ANGLE);
        Serial.print(F(" - "));
        Serial.println(TEST_MAX_ANGLE);
        return;
    }


    selectedAngle = newAngle;
    steeringServo.write(selectedAngle);


    Serial.print(F("Steering set to "));
    Serial.println(selectedAngle);
}



void setStepCount(long newSteps)
{
    if(state != IDLE)
    {
        Serial.println(F("Stop robot before changing distance."));
        return;
    }


    if(newSteps < MIN_ALLOWED_STEPS || newSteps > MAX_ALLOWED_STEPS)
    {
        Serial.println(F("Invalid step count."));
        return;
    }


    selectedSteps = newSteps;


    Serial.print(F("Distance set: "));
    Serial.print(selectedSteps);
    Serial.println(F(" steps"));
}



void scheduleRun()
{
    if(state != IDLE)
    {
        Serial.println(F("Robot not idle."));
        return;
    }


    steeringServo.write(selectedAngle);


    digitalWrite(ENABLE_PIN, HIGH);


    countdownStarted = millis();

    state = COUNTDOWN;


    Serial.println(F(""));
    Serial.println(F("GO accepted"));
    Serial.println(F("Starting in 5 seconds"));
}



void beginMovement()
{
    stepper.setCurrentPositionInSteps(0);
    stepper.setTargetPositionInSteps(0);

    stepper.setSpeedInStepsPerSecond(TEST_SPEED);

    stepper.setAccelerationInStepsPerSecondPerSecond(
        ACCELERATION
    );


    digitalWrite(ENABLE_PIN, LOW);


    stepper.setTargetPositionRelativeInSteps(
        FORWARD_SIGN * selectedSteps
    );


    state = MOVING;


    Serial.println(F("MOVING"));
}



void finishMovement()
{
    digitalWrite(ENABLE_PIN, HIGH);

    state = IDLE;


    Serial.println(F("RUN COMPLETE"));

    printStatus();
}



void requestStop()
{
    if(state == IDLE)
    {
        Serial.println(F("Already stopped."));
        return;
    }


    if(state == COUNTDOWN)
    {
        digitalWrite(ENABLE_PIN, HIGH);

        state = IDLE;

        Serial.println(F("Countdown cancelled."));
        return;
    }


    stepper.setTargetPositionToStop();

    state = STOPPING;


    Serial.println(F("Stopping..."));
}



void processCommand(String command)
{
    command.trim();
    command.toUpperCase();


    if(command.length()==0)
        return;


    if(command=="GO")
        scheduleRun();

    else if(command=="STOP")
        requestStop();


    else if(command=="CENTER")
        setSteeringAngle(SERVO_CENTER);


    else if(command=="LOW")
        setSteeringAngle(SERVO_LOW);


    else if(command=="HIGH")
        setSteeringAngle(SERVO_HIGH);


    else if(command=="LEFT")
        setSteeringAngle(SERVO_EXTREME_LOW);


    else if(command=="RIGHT")
        setSteeringAngle(SERVO_EXTREME_HIGH);


    else if(command=="SHORT")
        setStepCount(SHORT_STEPS);


    else if(command=="MEDIUM")
        setStepCount(MEDIUM_STEPS);


    else if(command=="FULL")
        setStepCount(FULL_STEPS);


    else if(command=="STATUS")
        printStatus();


    else if(command=="HELP")
        printHelp();


    else if(command.startsWith("A"))
        setSteeringAngle(command.substring(1).toInt());


    else if(command.startsWith("N"))
        setStepCount(command.substring(1).toInt());


    else
    {
        Serial.print(F("Unknown command: "));
        Serial.println(command);
    }
}



void readSerial()
{
    while(Serial.available()>0)
    {
        char received = Serial.read();


        if(received=='\r')
            continue;


        if(received=='\n')
        {
            processCommand(serialCommand);
            serialCommand="";
        }

        else if(serialCommand.length()<30)
        {
            serialCommand += received;
        }
    }
}



void setup()
{
    Serial.begin(115200);


    pinMode(ENABLE_PIN,OUTPUT);

    digitalWrite(ENABLE_PIN,HIGH);


    steeringServo.attach(SERVO_PIN);

    steeringServo.write(SERVO_CENTER);



    stepper.connectToPins(
        STEP_PIN,
        DIR_PIN
    );


    stepper.setCurrentPositionInSteps(0);

    stepper.setTargetPositionInSteps(0);

    stepper.setSpeedInStepsPerSecond(TEST_SPEED);

    stepper.setAccelerationInStepsPerSecondPerSecond(
        ACCELERATION
    );


    delay(700);


    printHelp();

    printStatus();
}



void loop()
{
    readSerial();



    if(
        state==COUNTDOWN &&
        millis()-countdownStarted >= START_DELAY_MS
    )
    {
        beginMovement();
    }



    if(state==MOVING || state==STOPPING)
    {
        stepper.processMovement();


        if(stepper.motionComplete())
        {
            finishMovement();
        }
    }
}

Save with:
Ctrl+O
Enter
Ctrl+X
2. Compile and upload
cd ~/Projects/MyRobot/step7_constant_radius_test

pio run
If compilation succeeds:
pio device list
pio run --target upload
pio device monitor
If pio is not found, use:
~/.platformio/penv/bin/pio run
~/.platformio/penv/bin/pio run --target upload
~/.platformio/penv/bin/pio device monitor
Exit the monitor with Ctrl+C.
3. Check steering safely
First lift the robot so the driven wheels cannot propel it. Keep fingers away from the steering linkage.
The motor driver stays disabled while the program says IDLE.
Enter these commands one at a time:
CENTER
A80
A78
A76 (LOWER--> RIGHT)
CENTER
A84
A86
A88
CENTER
For every position, check:
The linkage does not touch a mechanical stop.
The servo does not buzz or strain.
The tires do not rub the chassis.
The wheels return to straight at CENTER.
If it strains, immediately enter:
CENTER
or switch off robot power.
Determine which command turns the robot left when travelling forward:
LOW
and then:
HIGH
Record this mapping:
76 produces: left or right
88 produces: left or right
We should not assume that a lower number means left.
4. Perform two short safety runs
Use a clear floor with at least several metres of space. Keep the USB cable loose so it cannot pull on the robot.
Start with only about 246 mm of travel:
SHORT
LOW
STATUS
GO
After it stops:
CENTER
Return the robot to the starting point and test the other side:
SHORT
HIGH
STATUS
GO
Check that both runs:
Curve smoothly.
Stop automatically.
Do not cause steering binding.
Do not cause excessive wheel slipping.
Travel forward rather than backward.
STOP is a controlled deceleration, not an instant emergency stop. Keep the robot’s power switch accessible.
5. Select the measurement distance
If both short runs are safe, use:
MEDIUM
This travels approximately 492 mm.
If the curve is too short to measure accurately and you have enough space, use:
FULL
This travels approximately 984 mm.
Use the same step count for every left and right measurement.
Three-position method
Mark the midpoint of the rear axle—not the front wheels or the camera.
For each test:
Place the robot down and mark its rear-axle midpoint as P1.
Select the steering and distance:
MEDIUM
LOW
Run:
GO
When RUN COMPLETE appears, mark the new rear-axle midpoint as P2.
Do not move, rotate, or lift the robot.
Run the identical segment again:
GO
Mark the final rear-axle midpoint as P3.
Now measure only these three straight-line distances:
d12: P1 to P2
d23: P2 to P3
d13: P1 to P3
No curve tracing and no sagitta needed. Geometry does the annoying work for us.
How to mark the axle midpoint
After each run finishes and the motor disables:
Locate the midpoint between the two rear wheels.
Hold a ruler vertically down from that midpoint.
Put a small masking-tape cross on the floor.
Label it P1, P2, or P3.
Keep the USB cable completely slack so it does not pull the robot sideways.

Angle
Start to 2 (mm)
2 to 3 (mm)
Start to 3 (mm)
75 (Right)
1067
1067
1945
75 (Right)
1070
1049
1930
75 (Right)
1030
1060
1890
66 (Right)
932
932
1050
90 (Left)
1048
1065
1962
90 (Left)
1054
1040
1961
90 (Left)
1067
1052
1971
105 (Left)
830
820
547

Target steps: 1800

Command
Direction
Radius
66
Right
564.0 mm
105
Left
437.3 mm

Updated distance estimate
Across the six final trials, 1800 steps corresponded to approximately 1085 mm of path length:
steps per metre≈1659\text{steps per metre}\approx1659
Use 1660 as the new provisional value:
constexpr long STEPS_PER_METER = 1660L;
This should still be verified later with one direct straight-line measurement because it was calculated from curved paths.

