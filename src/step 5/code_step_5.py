```python
import time
from classes.arduino_comms import ArduinoComms

angle_straight = 85
speed_slow_forward = 1000
speed_stop = 0
test_target_steps = 5000

def main():
    arduino = ArduinoComms()
    time.sleep(2)

    print("Step 5: Wheels Raised Slow Forward and Stop Test")

    print("Phase 1: Testing continuous slow forward movement")
    arduino.send('!', 10000000)
    arduino.send('m', angle_straight, speed_slow_forward)

    print("Spinning drive wheels for 3 seconds...")
    time.sleep(3)

    arduino.send('m', angle_straight, speed_stop)
    print("Stopped drive wheels.")
    time.sleep(1)

    print("Phase 2: Testing target step stop command")
    arduino.send('!', test_target_steps)
    arduino.send('m', angle_straight, speed_slow_forward)

    print(f"Sent target step count ({test_target_steps}). Waiting for Arduino finished flag 'F'...")

    start_time = time.time()
    reached_target = False

    while time.time() - start_time < 10:
        msg = arduino.read()
        if msg == 'F':
            reached_target = True
            print("Received 'F' signal from Arduino: Target distance reached successfully.")
            break
        time.sleep(0.01)

    if not reached_target:
        print("Warning: Timed out waiting for target completion flag 'F'. Check Arduino firmware/encoders.")

    arduino.send('m', angle_straight, speed_stop)
    print("Test Complete")

if __name__ == "__main__":
    main()

```
