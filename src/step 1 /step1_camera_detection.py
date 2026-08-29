# Step 1: Camera Detection Test

import subprocess

# Helper function

def run_command(command):
    """
    Runs a terminal command and prints its output.

    Parameters:
        command (list): Terminal command split into a list.

    Returns:
        subprocess.CompletedProcess or None:
            The completed command result, or None if the command
            could not be executed.
    """

    print("\nRunning command:")
    print(" ".join(command))

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        return result

    except FileNotFoundError:
        print(f"\nError: Command not found: {command[0]}")
        return None


# Check for detected cameras

def check_camera_list():
    """
    Runs:

        rpicam-hello --list-cameras

    Success criterion:
        At least one camera should be listed.

    For the Camera Module 3 Wide, the detected camera may reference
    an IMX708-based sensor.
    """

    print("\nStep 1: Checking for detected cameras")

    result = run_command([
        "rpicam-hello",
        "--list-cameras"
    ])

    if result is None:
        return False

    # If the command reports an error, the camera check failed.
    if result.returncode != 0:
        print("\nResult: Fail")
        print("rpicam-hello could not successfully list cameras.")
        return False

    # Combine standard output and error output for checking.
    output = (
        result.stdout.lower()
        + result.stderr.lower()
    )

    # Check whether the output indicates that no cameras are available.
    if (
        "no cameras available" in output
        or "no camera available" in output
        or "no cameras found" in output
    ):
        print("\nResult: Fail")
        print("No camera was detected.")
        return False

    # A successful command with output is treated as a detected camera.
    if result.stdout.strip():
        print("\nResult: Pass")
        print("At least one camera appears to have been detected.")
        return True

    print("\nResult: Fail")
    print("No camera information was returned.")

    return False


# Troubleshooting

def check_camera_boot_messages():
    """
    Runs:

        dmesg | grep -i -E "imx708|camera|csi|unicam"

    This can help identify whether the operating system recognized
    camera-related activity during boot.
    """

    print("\nTroubleshooting: Checking camera-related boot messages")

    command = 'dmesg | grep -i -E "imx708|camera|csi|unicam"'

    result = run_command([
        "bash",
        "-c",
        command
    ])

    if result is not None:

        if result.stdout.strip():
            print("\nCamera-related boot messages were found.")

        else:
            print("\nNo matching camera-related boot messages were found.")


# Main program

def main():

    print("\nRaspberry Pi Camera Detection Test")

    print(
        "\nImportant physical check before testing:"
        "\n- Ensure the Raspberry Pi was powered off before connecting"
        "\n  or reseating the CSI ribbon cable."
        "\n- Ensure the ribbon cable is fully inserted."
        "\n- Ensure the connector clips are secured."
        "\n- Check that the cable orientation is correct."
        "\n- Check that the cable is not visibly damaged or sharply bent."
    )

    # Camera detection test

    camera_detected = check_camera_list()

    # If the camera was detected

    if camera_detected:

        print(
            "\nThe camera detection test passed."
            "\nYou can now test the live preview."
        )

        user_input = input(
            "\nStart rpicam-hello preview? (y/n): "
        ).strip().lower()

        if user_input in ["y", "yes"]:
            start_camera_preview()

        print(
            "\nStep 1 completed."
            "\nIf the preview successfully displayed an image,"
            "\nthe camera hardware detection test is considered a pass."
        )
      

if __name__ == "__main__":
    main()

