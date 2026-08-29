import time
from classes.arduino_comms import ArduinoComms

ANGLE_STRAIGHT_DEFAULT = 85
SPEED_STOP = 0

def run_servo_calibration():
    arduino = ArduinoComms()
    time.sleep(2)

    print("=== Step 4: Servo Calibration & Limit Testing ===")
    print("Commands: Enter target angle (0-180), or 'q' to quit.")

    current_angle = ANGLE_STRAIGHT_DEFAULT
    arduino.send('m', current_angle, SPEED_STOP)
    print(f"Initialized servo to default center angle: {current_angle}")

    while True:
        user_input = input("Enter target steering angle: ").strip()
        
        if user_input.lower() == 'q':
            print("Exiting calibration loop...")
            break

        try:
            angle = int(user_input)
            if 0 <= angle <= 180:
                arduino.send('m', angle, SPEED_STOP)
                current_angle = angle
                print(f"Sent steering angle: {current_angle}")
            else:
                print("Angle out of range. Enter a value between 0 and 180.")
        except ValueError:
            print("Invalid input. Enter an integer angle between 0 and 180, or 'q' to quit.")

    arduino.send('m', ANGLE_STRAIGHT_DEFAULT, SPEED_STOP)
    print(f"Reset servo to default center ({ANGLE_STRAIGHT_DEFAULT}). Calibration complete.")

if __name__ == "__main__":
    run_servo_calibration()
