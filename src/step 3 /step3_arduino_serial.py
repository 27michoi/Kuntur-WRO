# Step 3

import glob
import os
import subprocess


EXPECTED_DEVICE = "/dev/ttyACM0"
BAUD_RATE = 115200


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


# Check for ttyACM serial devices
def check_ttyacm_devices():
    """
    Checks whether the Raspberry Pi currently detects any ttyACM
    serial devices.

    The expected device for this project is:

        /dev/ttyACM0
    """

    print("\nChecking for ttyACM serial devices")

    devices = sorted(glob.glob("/dev/ttyACM*"))

    if devices:
        print("Detected serial devices:")

        for device in devices:
            print(f"  {device}")

        return devices

    print("No /dev/ttyACM* devices were detected.")

    return []


# Check for ttyUSB serial devices
def check_ttyusb_devices():
    """
    Checks whether the Raspberry Pi detects any ttyUSB serial devices.

    This is useful for troubleshooting if the Arduino does not appear
    as /dev/ttyACM0.
    """

    print("\nChecking for ttyUSB serial devices")

    devices = sorted(glob.glob("/dev/ttyUSB*"))

    if devices:
        print("Detected USB serial devices:")

        for device in devices:
            print(f"  {device}")

        return devices

    print("No /dev/ttyUSB* devices were detected.")

    return []


# Check the expected serial device
def check_expected_device():
    """
    Checks whether /dev/ttyACM0 exists.

    Returns:
        bool:
            True if the expected device exists.
            False otherwise.
    """

    print(f"\nChecking for expected device: {EXPECTED_DEVICE}")

    if os.path.exists(EXPECTED_DEVICE):

        print(f"Device found: {EXPECTED_DEVICE}")

        return True

    print(f"Device not found: {EXPECTED_DEVICE}")

    return False


# Display information about the expected device
def check_device_information():
    """
    Runs:

        ls -l /dev/ttyACM0

    This confirms that the expected serial device exists and allows
    its device information to be recorded.
    """

    print(f"\nChecking device information for {EXPECTED_DEVICE}")

    result = run_command([
        "ls",
        "-l",
        EXPECTED_DEVICE
    ])

    if result is None:
        return False

    if result.returncode == 0:
        print("\nSerial device information was retrieved.")
        return True

    print("\nCould not retrieve information for the expected device.")

    return False


# Check recent USB and serial messages
def check_recent_usb_messages():
    """
    Runs:

        dmesg | tail -n 30

    This displays recent kernel messages and can help identify whether
    the Raspberry Pi recognized the Arduino when it was connected.
    """

    print("\nChecking recent USB and serial messages")

    result = run_command([
        "dmesg",
        "tail",
        "-n",
        "30"
    ])

    if result is None:
        return False

    return result.returncode == 0


# Troubleshooting
def print_troubleshooting():
    """
    Prints troubleshooting instructions if the expected serial device
    is not detected.
    """

    print("\nTroubleshooting")

    print(
        "\nA. Disconnect and reconnect the Arduino"
        "\n"
        "\nDisconnect the Arduino from the Raspberry Pi."
        "\nWait a few seconds, reconnect it, and run:"
        "\n"
        "\nls /dev/ttyACM*"
    )

    print(
        "\nB. Check recent USB messages"
        "\n"
        "\nRun:"
        "\n"
        "\ndmesg | tail -n 30"
        "\n"
        "\nLook for messages related to USB detection, serial devices,"
        "\nor ttyACM."
    )

    print(
        "\nC. Check for another serial device name"
        "\n"
        "\nRun:"
        "\n"
        "\nls /dev/ttyUSB*"
        "\nls /dev/ttyACM*"
        "\n"
        "\nIf another device appears, record its exact path."
    )

    print(
        "\nD. Check the USB cable"
        "\n"
        "\nMake sure the USB cable supports data transfer."
        "\nA charging-only cable may power the Arduino without allowing"
        "\nserial communication with the Raspberry Pi."
    )

    print(
        "\nE. Check the Arduino IDE upload"
        "\n"
        "\nIf the Arduino was not successfully programmed, return to"
        "\nArduino IDE and confirm that:"
        "\n- Arduino Uno is selected as the board."
        "\n- The correct port is selected."
        "\n- The project compiles without errors."
        "\n- The firmware uploads successfully."
    )

    print(
        "\nF. If a different ttyACM number appears"
        "\n"
        f"\nThe project currently expects {EXPECTED_DEVICE}."
        "\nDo not immediately change the Python code."
        "\nRecord the actual device name first and determine why"
        "\na different device path was assigned."
    )




def main():

    print("\nStep 3: Arduino Serial Device Test")

    print(
        f"\nProject serial configuration:"
        f"\n- Board: Arduino Uno"
        f"\n- Baud rate: {BAUD_RATE}"
        f"\n- Expected device: {EXPECTED_DEVICE}"
    )

    print(
        "\nBefore running this script, make sure that:"
        "\n- The Arduino project has been opened in Arduino IDE."
        "\n- Arduino Uno is selected as the board."
        "\n- The correct Arduino port was selected."
        "\n- The project compiled successfully."
        "\n- The firmware uploaded successfully."
        "\n- The Arduino is connected to the Raspberry Pi using a USB data cable."
    )

    ttyacm_devices = check_ttyacm_devices()

    expected_device_found = check_expected_device()

    if expected_device_found:

        device_information_found = check_device_information()

        if device_information_found:

            print("\nStep 3 result: Pass")

            print(
                f"\nThe Raspberry Pi detected the expected Arduino"
                f"\nserial device at {EXPECTED_DEVICE}."
            )

            print(
                f"\nThe project is configured to use a baud rate of"
                f" {BAUD_RATE}."
            )

            return

    print(
        "\nThe expected Arduino serial device was not detected."
    )

    ttyusb_devices = check_ttyusb_devices()

    if ttyacm_devices or ttyusb_devices:

        print(
            "\nA serial device was detected, but it does not match"
            f"\nthe expected project device: {EXPECTED_DEVICE}"
        )

        print(
            "\nRecord the detected device path before changing"
            "\nthe project's serial configuration."
        )

    user_input = input(
        "\nCheck recent USB messages for troubleshooting? (y/n): "
    ).strip().lower()

    if user_input in ["y", "yes"]:
        check_recent_usb_messages()

    print("\nStep 3 result: Fail")

    print(
        f"\nThe expected serial device {EXPECTED_DEVICE}"
        "\nwas not detected."
    )

    print_troubleshooting()



if __name__ == "__main__":
    main()


