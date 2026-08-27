Electromechanical diagrams
====

___

## Introduction

This directory documents the electromechanical configuration of our vehicle. The schematics illustrate how the Raspberry Pi, Arduino, motors, motor driver, breadboard, and other supporting components are connected within the robot.

Our system divides responsibilities between two main controllers. The Raspberry Pi 5 serves as our main computer, processing information from the Raspberry Pi Camera Module 3 Wide and running the integrated tests used to evaluate the robot's complete performance. The Arduino Uno is responsible for the vehicle's movement mechanisms, communicating with the steering and driving systems.

The diagrams represent both the complete vehicle configuration and a chassis-focused test configuration.

###### Introducción

###### Este directorio documenta la configuración electromecánica de nuestro vehículo. Los esquemas ilustran cómo se conectan entre sí, dentro del robot, la Raspberry Pi, el Arduino, los motores, el controlador de motores y otros componentes auxiliares.

###### Nuestro sistema divide las responsabilidades entre dos controladores principales. La Raspberry Pi 5 actúa como nuestra computadora principal, procesando la información procedente del módulo de cámara Raspberry Pi Camera Module 3 Wide y ejecutando las pruebas integradas que se utilizan para evaluar el rendimiento general del robot. El Arduino Uno se encarga de los mecanismos de movimiento del vehículo, comunicándose con los sistemas de dirección y conducción.

###### Los diagramas representan tanto la configuración completa del vehículo como una configuración de prueba centrada en el chasis.

____

## System Set-up 

Our robot's electromechanical system can be understood through four main functions.

1. **Vision and computation**: handled by the Raspberry Pi 5 and Raspberry Pi Camera Module 3 Wide.
2. **Steering**: controlled through the Arduino, servo motor, and front-wheel steering mechanism.
3. **Driving**: controlled through the Arduino, stepper motor driver, and stepper motor.
4. **Power**: supplied by four 3.7 V batteries and routed through the vehicle's power management system.

Separating these functions allows the Raspberry Pi to focus on camera processing and higher-level testing while the Arduino manages the hardware responsible for physically moving the vehicle.

###### Configuración del Sistema

###### El sistema electromecánico de nuestro robot puede entenderse a través de cuatro funciones principales.

###### 1. **Visión y cálculo**: a cargo de la Raspberry Pi 5 y el módulo de cámara Raspberry Pi 3 Wide.
###### 2. **Dirección**: controlada mediante el Arduino, el servomotor y el mecanismo de dirección de las ruedas delanteras.
###### 3. **Propulsión**: controlada mediante el Arduino, el controlador del stepper motor driver y el stepper motor.
###### 4. **Poder**:  cuatro baterías de 3,7 V y canalizada a través del sistema de gestión de energía del vehículo.

###### La separación de estas funciones permite que la Raspberry Pi se centre en el procesamiento de las imágenes de la cámara y en las pruebas de nivel superior, mientras que el Arduino gestiona el hardware responsable del movimiento físico del vehículo.

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

###### _Raspberry Pi 5 y Cámara_

###### La Raspberry Pi 5 actúa como ordenador principal del robot, procesando los datos que recibe del módulo de cámara Raspberry Pi Camera Module 3 Wide y ejecutando nuestras pruebas de sistema completo. La cámara wide ofrece una visión más amplia del entorno de la competición.

###### _Arduino Uno_

###### El Arduino Uno actúa como controlador de movimiento del vehículo, comunicándose con los sistemas de dirección y movimiento, mientras que la Raspberry Pi se encarga de la visión y del procesamiento de nivel superior.

###### _Servomotor (+ruedas delanteras)_

###### El servomotor ajusta el ángulo de las ruedas delanteras para controlar la dirección del robot. La estructura de las ruedas delanteras se basa en la geometría de dirección de Ackermann.

###### _Stepper Motor y Stepper Motor Driver_

###### El controlador del stepper motor driver recibe señales de control del Arduino y acciona el stepper motor, que impulsa el movimiento de las ruedas traseras del robot.

###### _Mini protoboard_

###### La mini protoboard centraliza las conexiones eléctricas en un espacio compacto, lo que ayuda a mantener un esquema de cableado organizado dentro de las limitaciones de tamaño del vehículo.

###### _Sistema de power_

###### El robot se alimenta mediante cuatro baterías de 3,7 V, conectadas a través de un interruptor de on/off y un convertidor DC-DC para distribuir la potencia adecuada a los componentes electrónicos.

___




