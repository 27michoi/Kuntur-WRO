Electromechanical diagrams
====

___

## Introducción

Este directorio documenta la configuración electromecánica de nuestro vehículo. Los esquemas ilustran cómo se conectan entre sí, dentro del robot, la Raspberry Pi, el Arduino, los motores, el controlador de motores y otros componentes auxiliares.

Nuestro sistema divide las responsabilidades entre dos controladores principales. La Raspberry Pi 5 actúa como nuestra computadora principal, procesando la información procedente del módulo de cámara Raspberry Pi Camera Module 3 Wide y ejecutando las pruebas integradas que se utilizan para evaluar el rendimiento general del robot. El Arduino Uno se encarga de los mecanismos de movimiento del vehículo, comunicándose con los sistemas de dirección y conducción.

Los diagramas representan tanto la configuración completa del vehículo como una configuración de prueba centrada en el chasis.

____

## Configuración del Sistema

El sistema electromecánico de nuestro robot puede entenderse a través de cuatro funciones principales.

1. **Visión y cálculo**: a cargo de la Raspberry Pi 5 y el módulo de cámara Raspberry Pi 3 Wide.
2. **Dirección**: controlada mediante el Arduino, el servomotor y el mecanismo de dirección de las ruedas delanteras.
3. **Propulsión**: controlada mediante el Arduino, el controlador del stepper motor driver y el stepper motor.
4. **Poder**:  cuatro baterías de 3,7 V y canalizada a través del sistema de gestión de energía del vehículo.

La separación de estas funciones permite que la Raspberry Pi se centre en el procesamiento de las imágenes de la cámara y en las pruebas de nivel superior, mientras que el Arduino gestiona el hardware responsable del movimiento físico del vehículo.

____

## Configuración Completa del Vehículo

### Raspberry Pi 5 y Cámara

La Raspberry Pi 5 actúa como ordenador principal del robot, procesando los datos que recibe del módulo de cámara Raspberry Pi Camera Module 3 Wide y ejecutando nuestras pruebas de sistema completo. La cámara wide ofrece una visión más amplia del entorno de la competición.

### Arduino Uno

El Arduino Uno actúa como controlador de movimiento del vehículo, comunicándose con los sistemas de dirección y movimiento, mientras que la Raspberry Pi se encarga de la visión y del procesamiento de nivel superior.

### Servomotor (+ruedas delanteras)

El servomotor ajusta el ángulo de las ruedas delanteras para controlar la dirección del robot. La estructura de las ruedas delanteras se basa en la geometría de dirección de Ackermann.

### Stepper motor y stepper motor driver

El controlador del stepper motor driver recibe señales de control del Arduino y acciona el stepper motor, que impulsa el movimiento de las ruedas traseras del robot.

### Mini protoboard

La mini protoboard centraliza las conexiones eléctricas en un espacio compacto, lo que ayuda a mantener un esquema de cableado organizado dentro de las limitaciones de tamaño del vehículo.

### Sistema de power

El robot se alimenta mediante cuatro baterías de 3,7 V, conectadas a través de un interruptor de on/off y un convertidor DC-DC para distribuir la potencia adecuada a los componentes electrónicos.

___




