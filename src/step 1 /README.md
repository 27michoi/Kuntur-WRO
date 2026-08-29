## Step 1
### Overview

The purpose of this step is to verify that the Raspberry Pi 5 successfully detects and communicates with the Camera Module 3 Wide before proceeding with any project-specific camera or image-processing code.

This is a hardware and system-level validation step. The camera must first be physically connected correctly and recognized by Raspberry Pi OS before it can be used by the project's Python Picamera2, OpenCV, and image-processing systems.

The procedure consists of:

1. Safely powering off the Raspberry Pi before connecting or reconnecting the camera.
2. Checking the physical CSI ribbon cable connection.
3. Booting the Raspberry Pi.
4. Verifying that the camera is detected using rpicam-hello --list-cameras.
5. Confirming that the camera can initialize and produce a live preview using rpicam-hello.

Goal:
Confirm that the Raspberry Pi 5 can detect and successfully initialize the Camera Module 3 Wide.

Step 1 is complete when:
rpicam-hello --list-cameras detects at least one camera.
rpicam-hello successfully initializes the camera and displays a live preview.

____
