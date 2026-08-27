#include <Arduino.h>
#include <FlexyStepper.h>
#include <Servo.h>

// Existing robot wiring
constexpr uint8_t ENABLE_PIN = 2;
constexpr uint8_t STEP_PIN = 9;
constexpr uint8_t DIR_PIN = 10;
constexpr uint8_t SERVO_PIN = 11;

// Results from Step 4
constexpr int SERVO_MIN = 74;
constexpr int SERVO_CENTER = 99;
constexpr int SERVO_MAX = 124;

// Results from Step 5
constexpr float TEST_SPEED = 600.0F;
constexpr float ACCELERATION = 2000.0F;

// Initial estimate for approximately 1000 mm
constexpr long TEST_STEPS = 6400L;

// Repository direction: negative step position is forward.
// Change this to +1 only if the robot moves backward.
constexpr int FORWARD_SIGN = -1;

// Time to move away after entering GO
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
int selectedCenter = SERVO_CENTER;

void printHelp()
{
    Serial.println();
    Serial.println(F("=== STEP 6 STRAIGHT-LINE TEST ==="));
    Serial.println(F("Commands:"));
    Serial.println(F("  GO      - wait 5 seconds, then run"));
    Serial.println(F("  STOP    - cancel or decelerate to stop"));
    Serial.println(F("  A98     - set steering angle to 98"));
    Serial.println(F("  A99     - restore steering angle to 99"));
    Serial.println(F("  STATUS  - show current settings"));
    Serial.println(F("  HELP    - show these instructions"));
    Serial.println();
}

void printStatus()
{
    Serial.println(F("----- STATUS -----"));

    Serial.print(F("Steering angle: "));
    Serial.println(selectedCenter);

    Serial.print(F("Target steps: "));
    Serial.println(TEST_STEPS);

    Serial.print(F("Speed: "));
    Serial.println(TEST_SPEED);

    Serial.print(F("Acceleration: "));
    Serial.println(ACCELERATION);

    Serial.print(F("Motor position: "));
    Serial.println(stepper.getCurrentPositionInSteps());

    Serial.print(F("State: "));

    switch (state) {
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

void scheduleRun()
{
    if (state != IDLE) {
        Serial.println(F("Run rejected: robot is not idle."));
        return;
    }

    steeringServo.write(selectedCenter);

    // Keep the driver disabled during the countdown.
    digitalWrite(ENABLE_PIN, HIGH);

    countdownStarted = millis();
    state = COUNTDOWN;

    Serial.println();
    Serial.println(F("GO accepted."));
    Serial.println(F("Robot will move in 5 seconds."));
    Serial.println(F("Clear the path and keep the USB cable loose."));
}

void beginMovement()
{
    stepper.setCurrentPositionInSteps(0);
    stepper.setTargetPositionInSteps(0);
    stepper.setSpeedInStepsPerSecond(TEST_SPEED);
    stepper.setAccelerationInStepsPerSecondPerSecond(ACCELERATION);

    digitalWrite(ENABLE_PIN, LOW);

    stepper.setTargetPositionRelativeInSteps(
        FORWARD_SIGN * TEST_STEPS
    );

    state = MOVING;

    Serial.println(F("MOVING"));
}

void requestStop()
{
    if (state == IDLE) {
        Serial.println(F("Robot is already stopped."));
        return;
    }

    if (state == COUNTDOWN) {
        state = IDLE;
        digitalWrite(ENABLE_PIN, HIGH);
        Serial.println(F("Countdown cancelled."));
        return;
    }

    stepper.setTargetPositionToStop();
    state = STOPPING;

    Serial.println(F("STOP requested: decelerating."));
}

void setSteeringAngle(const int newAngle)
{
    if (state != IDLE) {
        Serial.println(F("Stop the robot before changing the angle."));
        return;
    }

    if (newAngle < SERVO_MIN || newAngle > SERVO_MAX) {
        Serial.print(F("Invalid angle. Allowed range: "));
        Serial.print(SERVO_MIN);
        Serial.print(F(" to "));
        Serial.println(SERVO_MAX);
        return;
    }

    selectedCenter = newAngle;
    steeringServo.write(selectedCenter);

    Serial.print(F("Steering angle set to: "));
    Serial.println(selectedCenter);
}

void processCommand(String command)
{
    command.trim();
    command.toUpperCase();

    if (command.length() == 0) {
        return;
    }

    if (command == "GO") {
        scheduleRun();
    }
    else if (command == "STOP") {
        requestStop();
    }
    else if (command == "STATUS") {
        printStatus();
    }
    else if (command == "HELP") {
        printHelp();
    }
    else if (command.startsWith("A")) {
        const int requestedAngle = command.substring(1).toInt();
        setSteeringAngle(requestedAngle);
    }
    else {
        Serial.print(F("Unknown command: "));
        Serial.println(command);
        Serial.println(F("Enter HELP for the command list."));
    }
}

void readSerial()
{
    while (Serial.available() > 0) {
        const char received = static_cast<char>(Serial.read());

        if (received == '\r') {
            continue;
        }

        if (received == '\n') {
            processCommand(serialCommand);
            serialCommand = "";
        }
        else if (serialCommand.length() < 30) {
            serialCommand += received;
        }
    }
}

void setup()
{
    Serial.begin(115200);

    pinMode(ENABLE_PIN, OUTPUT);

    // DRV8825 ENABLE is active-low.
    digitalWrite(ENABLE_PIN, HIGH);

    steeringServo.attach(SERVO_PIN);
    steeringServo.write(SERVO_CENTER);

    stepper.connectToPins(STEP_PIN, DIR_PIN);
    stepper.setCurrentPositionInSteps(0);
    stepper.setTargetPositionInSteps(0);
    stepper.setSpeedInStepsPerSecond(TEST_SPEED);
    stepper.setAccelerationInStepsPerSecondPerSecond(ACCELERATION);

    delay(700);

    printHelp();
    printStatus();
}

void loop()
{
    readSerial();

    if (
        state == COUNTDOWN &&
        millis() - countdownStarted >= START_DELAY_MS
    ) {
        beginMovement();
    }

    if (state == MOVING || state == STOPPING) {
        stepper.processMovement();

        if (stepper.motionComplete()) {
            digitalWrite(ENABLE_PIN, HIGH);
            state = IDLE;

            Serial.println();
            Serial.println(F("DONE"));
            Serial.print(F("Final motor position: "));
            Serial.println(stepper.getCurrentPositionInSteps());
            Serial.println(F("Driver disabled."));
        }
    }
}
