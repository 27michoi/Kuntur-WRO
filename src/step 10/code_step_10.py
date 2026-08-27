1. Restore the original competition Arduino firmware
Step 7 used separate test firmware. Step 10 requires the original Arduino serial protocol.
Compile the original:
cd /home/admin/Projects/WRO2026-CLM/code/arduino

pio run
Upload:
pio run --target upload
Check the device:
ls -l /dev/ttyACM* /dev/ttyUSB* 2>/dev/null
The original firmware accepts:
m<angle>,<speed>.
for continuous movement and:
<steps>!
for a limited target distance. This is the same protocol used by the repository’s ArduinoComms.
Do not leave pio device monitor open, because Python cannot use the serial port while the monitor owns it.

2. Prepare Step 10
cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package
source ../.venv/bin/activate

mkdir -p step10_tests
mkdir -p ../../step10_results/logs
mkdir -p ../../step10_results/frames

touch step10_tests/__init__.py
Check imports:
python -c "import cv2, numpy, serial; from classes.camera_manager import CameraManager; from classes.image_algoriths import ImageAlgorithms; from classes.arduino_comms import ArduinoComms; print('Step 10 imports OK')"

3. Create the competition wall-following test
Open:
nano step10_tests/wall_follow_low_speed.py
Paste:
import argparse
import csv
import time
from datetime import datetime
from pathlib import Path

import cv2

from classes.arduino_comms import ArduinoComms
from classes.camera_manager import CameraManager
from classes.context_manager import ContextManager
from classes.image_algoriths import ImageAlgorithms
from utils.enums import Direction


# Repository wall algorithm was calibrated around 86.
REPOSITORY_SERVO_CENTER = 86

# Results from our physical calibration.
SERVO_RIGHT = 75
SERVO_CENTER = 82
SERVO_LEFT = 90

TEST_SPEED = 600
DEFAULT_TEST_STEPS = 500


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def convert_repository_angle(raw_angle):
    """
    Preserve the correction calculated by the original repository,
    but transfer its centre from 86 to our calibrated centre of 82.
    Limit Step 10 steering to our tested normal operating pair.
    """
    correction = raw_angle - REPOSITORY_SERVO_CENTER
    converted = SERVO_CENTER + correction

    return int(round(clamp(
        converted,
        SERVO_RIGHT,
        SERVO_LEFT,
    )))


def close_camera(camera):
    if camera is None:
        return

    try:
        camera.release_video()
    except Exception:
        pass

    try:
        camera.picam2.stop()
    except Exception:
        pass

    try:
        camera.picam2.close()
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Step 10 competition wall-following test"
    )

    parser.add_argument(
        "--direction",
        required=True,
        choices=("left", "right"),
        help="Competition travel direction",
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=DEFAULT_TEST_STEPS,
        help="Maximum movement distance in stepper steps",
    )

    parser.add_argument(
        "--speed",
        type=int,
        default=TEST_SPEED,
        help="Motor speed in steps per second",
    )

    parser.add_argument(
        "--port",
        default="/dev/ttyACM0",
        help="Arduino serial device",
    )

    parser.add_argument(
        "--display",
        action="store_true",
        help="Show the diagnostic window",
    )

    args = parser.parse_args()

    if args.steps < 100 or args.steps > 2000:
        raise SystemExit(
            "For Step 10, --steps must be between 100 and 2000."
        )

    if args.speed != TEST_SPEED:
        raise SystemExit(
            "Step 10 must initially use speed 600."
        )

    direction = (
        Direction.LEFT
        if args.direction == "left"
        else Direction.RIGHT
    )

    project_root = Path(__file__).resolve().parents[3]
    results_root = project_root / "step10_results"
    logs_dir = results_root / "logs"
    frames_dir = results_root / "frames"

    logs_dir.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)

    run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"{args.direction}_{args.steps}_{run_stamp}"

    log_path = logs_dir / f"{run_name}.csv"
    run_frames_dir = frames_dir / run_name
    run_frames_dir.mkdir(parents=True, exist_ok=True)

    camera = None
    arduino = None
    completed = False
    stop_reason = "UNKNOWN"

    try:
        context = ContextManager()
        context.set_challenge(1)
        context.set_direction(direction)

        camera = CameraManager()
        algorithms = ImageAlgorithms(context, camera)

        arduino = ArduinoComms(port=args.port)

        # Make sure the robot begins stopped and centred.
        arduino.send("m", SERVO_CENTER, 0)

        camera.start_camera()
        camera.capture_image()
        camera.transform_image()

        print()
        print("=== STEP 10 WALL-FOLLOWING TEST ===")
        print(f"Direction: {args.direction}")
        print(f"Speed: {args.speed} steps/s")
        print(f"Target: {args.steps} steps")
        print(f"Serial port: {args.port}")
        print()
        print("Place the robot on a straight WRO section.")
        print("Keep the path clear and the power switch accessible.")

        input("Press Enter when ready for the countdown...")

        for remaining in range(5, 0, -1):
            print(f"Starting in {remaining}...")
            time.sleep(1)

        # Original firmware target command.
        arduino.send("!", args.steps)

        started = time.monotonic()
        frame_number = 0

        timeout_seconds = max(
            8.0,
            (args.steps / args.speed) * 4.0 + 4.0,
        )

        with log_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as log_file:
            writer = csv.writer(log_file)

            writer.writerow([
                "time_s",
                "frame",
                "direction",
                "avg_x",
                "avg_y",
                "raw_repository_angle",
                "servo_command",
                "is_corner",
            ])

            while True:
                camera.capture_image()
                camera.transform_image()

                avg_x, avg_y = algorithms.find_wall_to_follow()

                raw_angle, is_corner = (
                    algorithms.calculate_servo_angle_from_walls()
                )

                servo_command = convert_repository_angle(raw_angle)

                arduino.send(
                    "m",
                    servo_command,
                    args.speed,
                )

                elapsed = time.monotonic() - started

                writer.writerow([
                    f"{elapsed:.4f}",
                    frame_number,
                    args.direction,
                    f"{avg_x:.2f}",
                    f"{avg_y:.2f}",
                    raw_angle,
                    servo_command,
                    int(is_corner),
                ])

                if camera.display_image is not None:
                    cv2.putText(
                        camera.display_image,
                        f"Raw: {raw_angle}  Command: {servo_command}",
                        (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                    )

                    cv2.putText(
                        camera.display_image,
                        f"Direction: {args.direction}",
                        (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                    )

                    if frame_number % 5 == 0:
                        frame_path = (
                            run_frames_dir
                            / f"frame_{frame_number:05d}.jpg"
                        )

                        cv2.imwrite(
                            str(frame_path),
                            camera.display_image,
                        )

                    if args.display:
                        cv2.imshow(
                            "Step 10 Wall Following",
                            camera.display_image,
                        )

                message = arduino.read()

                if message == "F":
                    completed = True
                    stop_reason = "TARGET_COMPLETE"
                    break

                if elapsed > timeout_seconds:
                    stop_reason = "TIMEOUT"
                    break

                if args.display:
                    key = cv2.waitKey(1)

                    if key == 27:
                        stop_reason = "ESCAPE"
                        break

                frame_number += 1
                time.sleep(0.001)

    except KeyboardInterrupt:
        stop_reason = "KEYBOARD_INTERRUPT"

    except Exception as error:
        stop_reason = f"ERROR: {error}"
        raise

    finally:
        if arduino is not None:
            try:
                arduino.send("m", SERVO_CENTER, 0)
            except Exception:
                pass

            try:
                arduino.arduino.close()
            except Exception:
                pass

        close_camera(camera)
        cv2.destroyAllWindows()

        print()
        print("=== RUN FINISHED ===")
        print(f"Completed target: {completed}")
        print(f"Stop reason: {stop_reason}")
        print(f"Log: {log_path}")


if __name__ == "__main__":
    main()
Save:
Ctrl+O
Enter
Ctrl+X
Compile-check it:
python -m py_compile \
  step10_tests/wall_follow_low_speed.py
No output means the syntax is valid.

4. Raised-wheel verification
Raise the driven wheels before the first run.
Run left direction:
python -m step10_tests.wall_follow_low_speed \
  --direction left \
  --steps 500 \
  --port /dev/ttyACM0
During the countdown, hold or position the field wall where the camera can see it. Confirm:
Motor begins after the countdown.
Servo changes while the motor is moving.
Servo never exceeds 75–90.
Motor stops automatically.
Output says:
Completed target: True
Stop reason: TARGET_COMPLETE
Repeat right:
python -m step10_tests.wall_follow_low_speed \
  --direction right \
  --steps 500 \
  --port /dev/ttyACM0
If your Arduino uses another device, replace /dev/ttyACM0.

5. First floor runs
Place the robot on a straight WRO section, well before any corner.
Start centred and aligned straight.
Left direction, approximately 300 mm
python -m step10_tests.wall_follow_low_speed \
  --direction left \
  --steps 500
Right direction, approximately 300 mm
python -m step10_tests.wall_follow_low_speed \
  --direction right \
  --steps 500
Pass both before increasing distance.

6. Longer straight-wall run
Approximately 600 mm:
python -m step10_tests.wall_follow_low_speed \
  --direction left \
  --steps 1000

python -m step10_tests.wall_follow_low_speed \
  --direction right \
  --steps 1000
If those pass, approximately one metre:
python -m step10_tests.wall_follow_low_speed \
  --direction left \
  --steps 1660

python -m step10_tests.wall_follow_low_speed \
  --direction right \
  --steps 1660
Keep all these runs on a straight. Step 11 will deliberately introduce the first corner.

Step 10 completion requirements
Step 10 passes when:
Original Arduino competition firmware is running.
The test uses the repository’s real CameraManager.
The test uses the repository’s real calculate_servo_angle_from_walls().
The test uses the repository’s real ArduinoComms.
Both left and right directions correct toward the intended path.
Servo commands stay between 75 and 90.
Speed remains 600.
The robot stops automatically at the target.
It completes a straight run of approximately one metre in each direction.
It does not touch the wall.
It does not show continuous left-right oscillation.
Diagnostic frames and CSV logs are generated.
What to send me
After the tests, send:
The final console output from the 1660-step left run.
The final console output from the 1660-step right run.
The two corresponding CSV files from:
find ../../step10_results/logs \
  -type f -name "*.csv" | sort

Approximately three representative images from each final run:
find ../../step10_results/frames \
  -type f -name "*.jpg" | sort

Tell me only:
Left run wall contact: no
Right run wall contact: no
Left run oscillation: none
Right run oscillation: none
No additional physical measurements are needed for Step 10. Once those two final runs pass, we mark Step 10 complete and move directly to Step 11: one corner.
