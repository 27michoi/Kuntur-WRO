## Step 3

### Overview

The purpose of this step is to verify that the Arduino Uno can successfully run the project's firmware and is recognized by the Raspberry Pi 5 as a USB serial device.

Before testing Arduino communication through the Python program, the Arduino firmware must compile and upload successfully. The Arduino project is maintained separately from the Python package and contains multiple source and header files required for compilation. The firmware uses the `SerialReceiver` class to process incoming commands and initializes serial communication at `115200` baud.

After uploading the firmware, the Arduino is connected to the Raspberry Pi through USB. The Raspberry Pi is then checked for the serial device used by the project's Python communication system. The current project configuration expects the Arduino to appear as `/dev/ttyACM0`.

The procedure consists of:

1. Locating the Arduino project source and confirming that the complete project structure is available.
2. Connecting the Arduino Uno to a computer using a USB data cable.
3. Opening the Arduino project in Arduino IDE.
4. Selecting the Arduino Uno board and the correct serial port.
5. Compiling the Arduino project and confirming that no errors occur.
6. Uploading the firmware to the Arduino and confirming that the upload succeeds.
7. Connecting the Arduino to the Raspberry Pi 5 through USB.
8. Checking whether the Raspberry Pi detects the Arduino as a `ttyACM` serial device.
9. Confirming that `/dev/ttyACM0` is available.
10. Troubleshooting the USB connection or serial-device assignment if the expected device is not detected.

Goal:
Confirm that the Arduino firmware compiles and uploads successfully and that the Raspberry Pi can detect the Arduino as the `/dev/ttyACM0` USB serial device required by the project's Python communication system.


Step 3 is complete when:
* The complete Arduino project structure is available.
* The Arduino project compiles successfully without errors.
* The firmware uploads successfully to the Arduino Uno.
* The Arduino is connected to the Raspberry Pi 5 through a USB data connection.
* The Raspberry Pi detects the Arduino as a serial device.
* `/dev/ttyACM0` is available and can be accessed by the system.
* No repeated USB disconnections or connection errors occur.

___
