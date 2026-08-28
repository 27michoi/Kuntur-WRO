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
