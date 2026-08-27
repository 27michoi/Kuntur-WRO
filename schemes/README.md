Electromechanical diagrams
====

___

## Introduction

This directory documents the electromechanical configuration of our vehicle. The schematics illustrate how the Raspberry Pi, Arduino, motors, motor driver, breadboard, and other supporting components are connected within the robot.

Our system divides responsibilities between two main controllers. The Raspberry Pi 5 serves as our main computer, processing information from the Raspberry Pi Camera Module 3 Wide and running the integrated tests used to evaluate the robot's complete performance. The Arduino Uno is responsible for the vehicle's movement mechanisms, communicating with the steering and driving systems.

The diagrams represent both the complete vehicle configuration and a chassis-focused test configuration.

###### Introducción

###### _texto_

____

## System Set-up 

Our robot's electromechanical system can be understood through four main functions.

1. **Vision and computation**: handled by the Raspberry Pi 5 and Raspberry Pi Camera Module 3 Wide.
2. **Steering**: controlled through the Arduino, servo motor, and front-wheel steering mechanism.
3. **Driving**: controlled through the Arduino, stepper motor driver, and stepper motor.
4. **Power**: supplied by four 3.7 V batteries and routed through the vehicle's power management system.

Separating these functions allows the Raspberry Pi to focus on camera processing and higher-level testing while the Arduino manages the hardware responsible for physically moving the vehicle.

###### Configuración del Sistema

###### _texto_

____

## Complete Vehicle Configuration

#### Raspberry Pi 5 and Camera 

The Raspberry Pi 5 serves as the robot's main computer, processing input from the Raspberry Pi Camera Module 3 Wide and running our full-system tests. The wide-angle camera provides a broader view of the competition environment.

#### Arduino Uno

The Arduino Uno acts as the vehicle's movement controller, communicating with the steering and driving systems while the Raspberry Pi handles vision and higher-level processing.

#### Servo Motor (+Front Wheels)

The servo motor adjusts the angle of the front wheels to control the robot's direction. The steering structure is based on Ackermann steering geometry.

#### Stepper Motor and Motor Driver

The stepper motor driver receives control signals from the Arduino and operates the stepper motor, which drives the robot's rear-wheel movement.

#### Mini Breadboard

The mini breadboard centralizes electrical connections in a compact area, helping maintain an organized wiring layout within the vehicle's size constraints.

#### Power System

The robot is powered by four 3.7 V batteries, connected through an on/off switch and DC-DC converter to distribute appropriate power to the electronic components.

###### Configuración Completa del Vehículo

###### _texto_

___

