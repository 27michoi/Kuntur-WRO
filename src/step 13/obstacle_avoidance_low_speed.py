from __future__ import annotations

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


SERVO_CENTER = 82
REPOSITORY_CENTER = 86
SPEED_LIMIT = 600
FORWARD_SIGN = -1

SERVO_LIMITS = {
    "left": (75, 92),
    "right": (72, 90),
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Step 13: bounded, low-speed, single-obstacle test"
    )
    parser.add_argument("--direction", choices=("left", "right"), required=True)
    parser.add_argument("--color", choices=("green", "red"), required=True)
    parser.add_argument("--steps", type=int, default=1700)
    parser.add_argument("--speed", type=int, default=SPEED_LIMIT)
    parser.add_argument("--port", default="/dev/ttyACM0")
    parser.add_argument("--countdown", type=int, default=5)
    parser.add_argument("--preflight-frames", type=int, default=20)
    parser.add_argument("--save-every", type=int, default=5)
    return parser.parse_args()


def physical_servo_angle(repository_angle, direction):
    if repository_angle is None:
        repository_angle = REPOSITORY_CENTER

    requested = round(
        SERVO_CENTER + float(repository_angle) - REPOSITORY_CENTER
    )
    minimum, maximum = SERVO_LIMITS[direction]
    return max(minimum, min(maximum, requested))


def detected_color(is_green, x_center, y_center):
    if is_green is None or x_center is None or y_center is None:
        return "none"
    return "green" if is_green else "red"


def add_diagnostics(image, expected, detected, servo, phase):
    if image is None:
        return

    lines = (
        f"STEP 13 - {phase}",
        f"Expected: {expected}",
        f"Detected: {detected}",
        f"Servo: {servo}",
    )

    for index, text in enumerate(lines):
        cv2.putText(
            image,
            text,
            (10, 25 + index * 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )


def save_frame(path, image):
    if image is None:
        return False
    return bool(cv2.imwrite(str(path), image))


def main():
    args = parse_args()

    if args.steps <= 0:
        raise SystemExit("--steps must be greater than zero")
    if args.speed <= 0 or args.speed > SPEED_LIMIT:
        raise SystemExit("For Step 13, --speed must be between 1 and 600")

    direction_enum = (
        Direction.LEFT if args.direction == "left" else Direction.RIGHT
    )

    project_root = Path(__file__).resolve().parents[3]
    results_root = project_root / "step13_results"
    logs_dir = results_root / "logs"
    frames_root = results_root / "frames"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"{args.direction}_{args.color}_{timestamp}"
    csv_path = logs_dir / f"{run_name}.csv"
    frames_dir = frames_root / run_name

    logs_dir.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)

    camera = None
    arduino = None
    rows = []
    completed_target = False
    preflight_passed = False
    expected_frames = 0
    wrong_color_frames = 0
    obstacle_control_frames = 0
    saved_images = 0
    servo_commands = []
    stop_reason = "NOT_STARTED"
    error_text = ""

    print("=== STEP 13: SINGLE-OBSTACLE AVOIDANCE ===")
    print(f"Direction: {args.direction}")
    print(f"Expected obstacle: {args.color}")
    print(f"Speed: {args.speed}")
    print(f"Target steps: {args.steps}")
    print(f"Servo center: {SERVO_CENTER}")
    print(
        "Servo limits: "
        f"{SERVO_LIMITS[args.direction][0]}-"
        f"{SERVO_LIMITS[args.direction][1]}"
    )
    print(f"CSV: {csv_path}")
    print(f"Frames: {frames_dir}")

    try:
        context = ContextManager()
        context.set_challenge(2)
        context.set_direction(direction_enum)

        camera = CameraManager()
        algorithms = ImageAlgorithms(context, camera)
        camera.start_camera()

        arduino = ArduinoComms(port=args.port)
        time.sleep(2)
        arduino.send("m", SERVO_CENTER, 0)

        print()
        print("Preflight: motor is stopped while the camera checks the obstacle.")

        correct_preflight = 0
        wrong_preflight = 0

        for index in range(args.preflight_frames):
            camera.capture_image()
            camera.transform_image()
            object_angle, is_green, x_center, y_center = (
                algorithms.find_obstacle_angle_and_draw_lines()
            )
            seen = detected_color(is_green, x_center, y_center)
            raw_obstacle = algorithms.calculate_servo_angle_from_obstacle(
                object_angle, is_green
            )
            servo = physical_servo_angle(raw_obstacle, args.direction)

            if seen == args.color:
                correct_preflight += 1
            elif seen != "none":
                wrong_preflight += 1

            add_diagnostics(
                camera.display_image,
                args.color,
                seen,
                servo,
                "PREFLIGHT",
            )

            if index % 5 == 0 or seen != "none":
                if save_frame(
                    frames_dir / f"preflight_{index:03d}.jpg",
                    camera.display_image,
                ):
                    saved_images += 1

            time.sleep(0.04)

        preflight_passed = (
            correct_preflight >= 3
            and correct_preflight > wrong_preflight
        )

        print(
            "Preflight detections: "
            f"expected={correct_preflight}, other-color={wrong_preflight}"
        )

        if not preflight_passed:
            stop_reason = "PREFLIGHT_OBSTACLE_NOT_CONFIRMED"
            print("Motor will not start.")
            print(
                "Reposition the robot or obstacle so the expected color is "
                "clearly visible, then run the same command again."
            )
        else:
            print("Preflight passed. The expected obstacle is visible.")
            print("Keep one hand near Ctrl+C or the robot power switch.")

            for remaining in range(args.countdown, 0, -1):
                print(f"Starting in {remaining}...")
                time.sleep(1)

            if hasattr(arduino, "arduino"):
                arduino.arduino.reset_input_buffer()

            arduino.send("!", FORWARD_SIGN * args.steps)
            arduino.send("m", SERVO_CENTER, args.speed)

            start_time = time.monotonic()
            timeout = max(8.0, args.steps / args.speed + 6.0)
            frame = 0
            stop_reason = "RUNNING"

            while True:
                camera.capture_image()
                camera.transform_image()

                object_angle, is_green, x_center, y_center = (
                    algorithms.find_obstacle_angle_and_draw_lines()
                )
                seen = detected_color(is_green, x_center, y_center)

                raw_wall, is_corner = (
                    algorithms.calculate_servo_angle_from_walls()
                )
                raw_obstacle = (
                    algorithms.calculate_servo_angle_from_obstacle(
                        object_angle, is_green
                    )
                )
                raw_selected = algorithms.choose_output_angle(
                    raw_wall, raw_obstacle
                )
                servo = physical_servo_angle(
                    raw_selected, args.direction
                )

                arduino.send("m", servo, args.speed)
                reply = arduino.read()
                elapsed = time.monotonic() - start_time

                servo_commands.append(servo)
                if seen == args.color:
                    expected_frames += 1
                elif seen != "none":
                    wrong_color_frames += 1
                if seen == args.color and raw_obstacle is not None:
                    obstacle_control_frames += 1

                phase = "AVOID" if raw_obstacle is not None else "WALL_FOLLOW"
                add_diagnostics(
                    camera.display_image,
                    args.color,
                    seen,
                    servo,
                    phase,
                )

                if (
                    frame % args.save_every == 0
                    or seen == args.color
                    or reply == "F"
                ):
                    if save_frame(
                        frames_dir / f"frame_{frame:04d}.jpg",
                        camera.display_image,
                    ):
                        saved_images += 1

                rows.append(
                    {
                        "time_s": f"{elapsed:.4f}",
                        "frame": frame,
                        "direction": args.direction,
                        "expected_color": args.color,
                        "detected_color": seen,
                        "x_center": "" if x_center is None else x_center,
                        "y_center": "" if y_center is None else y_center,
                        "object_angle": (
                            "" if object_angle is None else f"{object_angle:.2f}"
                        ),
                        "raw_wall_angle": raw_wall,
                        "raw_obstacle_angle": (
                            "" if raw_obstacle is None else raw_obstacle
                        ),
                        "raw_selected_angle": raw_selected,
                        "servo_command": servo,
                        "is_corner": int(bool(is_corner)),
                        "phase": phase,
                        "arduino_reply": "" if reply is None else reply,
                    }
                )

                if reply == "F":
                    completed_target = True
                    stop_reason = "TARGET_COMPLETE"
                    break

                if elapsed >= timeout:
                    stop_reason = "TIMEOUT"
                    break

                frame += 1
                time.sleep(0.01)

    except KeyboardInterrupt:
        stop_reason = "USER_ABORT"
        print("User stop received.")
    except Exception as error:
        stop_reason = "ERROR"
        error_text = f"{type(error).__name__}: {error}"
        print(f"ERROR: {error_text}")
    finally:
        if arduino is not None:
            try:
                arduino.send("m", SERVO_CENTER, 0)
            except Exception:
                pass

        if rows:
            with csv_path.open("w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        if camera is not None:
            try:
                camera.release_video()
            except Exception:
                pass
            try:
                camera.picam2.stop()
            except Exception:
                pass

        if arduino is not None and hasattr(arduino, "arduino"):
            try:
                arduino.arduino.close()
            except Exception:
                pass

        cv2.destroyAllWindows()

    color_result = (
        expected_frames >= 3
        and expected_frames > wrong_color_frames
    )
    technical_pass = (
        preflight_passed
        and completed_target
        and color_result
        and obstacle_control_frames >= 3
        and stop_reason == "TARGET_COMPLETE"
        and not error_text
    )

    print()
    print("=== STEP 13 RUN COMPLETE ===")
    print(f"Direction: {args.direction}")
    print(f"Expected obstacle: {args.color}")
    print(f"Preflight passed: {preflight_passed}")
    print(f"Expected-color frames: {expected_frames}")
    print(f"Other-color frames: {wrong_color_frames}")
    print(f"Obstacle-control frames: {obstacle_control_frames}")
    if servo_commands:
        print(
            "Servo range observed: "
            f"{min(servo_commands)} to {max(servo_commands)}"
        )
    else:
        print("Servo range observed: no movement")
    print(f"Completed target: {completed_target}")
    print(f"Stop reason: {stop_reason}")
    print(f"Images saved: {saved_images}")
    print(f"CSV: {csv_path}")
    print(f"Frames: {frames_dir}")
    print(f"Technical result: {'PASS' if technical_pass else 'REVIEW'}")


if __name__ == "__main__":
    main()
