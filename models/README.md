# 3D Models
____

## Resumen

Este directorio contiene los archivos STL de los componentes impresos en 3D de nuestro robot para la WRO 2026. Los modelos incluyen las piezas del chasis estructural, del mecanismo de dirección, de los soportes de los motores, del soporte de la cámara y otros componentes mecánicos utilizados en el vehículo.
También se incluye una descripción del armado del robot junto con indicaciones para el ensamblaje.

____

## Estructura del chasis

### Placas de base

[`BasePlaqueV4.stl`](./BasePlaqueV4.stl)
[`BasePlaqueV4-modifiedV1.stl`](./BasePlaqueV4-modifiedV1.stl) 


### Placas del medio

[`MiddlePlaqueV4.stl`](./MiddlePlaqueV4.stl)
[`MiddlePlaqueV4-modified_lu.stl`](./MiddlePlaqueV4-modified_lu.stl)


### Placas superiores

[`TopPlaqueV4.stl`](./TopPlaqueV4.stl)

____

## Sistema de conducción

### Componentes de dirección

[`DirectionRods3.stl`](./DirectionRods3.stl)
[`DirectionRodsShort3.stl`](./DirectionRodsShort3.stl)
[`DirectionTabsLH.stl`](./DirectionTabsLH.stl)
[`DirectionTabsRH.stl`](./DirectionTabsRH.stl)

### Componentes de servo

[`ServoHolderV2.stl`](./ServoHolderV2.stl)
[`ServoCover.stl`](./ServoCover.stl)

____

## Sistema de manejo

[`StepMotorBracker.stl`](./StepMotorBracket.stl)
[`BaseMotorBig.stl`](./BaseMotorBig.stl)
[`CouplingV3.stl`](./CouplingV3.stl)

____

## Sistema de cámara

[`CamHolderV4.stl`](./CamHolderV4.stl)

____

## Componentes externos y auxiliares

[`FrontWingV2.stl`](./FrontWingV2.stl)
[`ButtonHolder.stl`](./ButtonHolder.stl)


___

# Diseño Mecánico

## Descripción general

Esta carpeta contiene los archivos correspondientes al diseño mecánico del robot autónomo desarrollado para la competencia WRO Future Engineers.

El diseño mecánico tuvo como objetivo principal desarrollar una estructura resistente, modular y fácil de ensamblar, permitiendo realizar modificaciones rápidas durante la etapa de pruebas y preparación para la competencia.

Los principales criterios de diseño fueron:

- Lograr una estructura rígida y estable para soportar todos los componentes mecánicos y electrónicos.
- Permitir un montaje y desmontaje sencillo de las piezas.
- Facilitar el mantenimiento y reemplazo de componentes durante las pruebas.
- Mejorar la precisión del sistema de dirección y transmisión.

Las piezas personalizadas fueron diseñadas mediante software CAD y fabricadas mediante impresión 3D.

---

# Arquitectura del chasis

El robot está compuesto por una estructura modular de tres niveles principales:

1. Placa inferior del chasis.
2. Placa intermedia para componentes electrónicos.
3. Placa superior para Raspberry Pi y sistema de cámara.

Las placas están unidas mediante pernos y separadores previamente calculados, permitiendo mantener una distancia adecuada entre niveles para organizar los componentes internos y evitar interferencias mecánicas.

---

# Placa inferior del chasis

La placa inferior constituye la base principal del robot.

En esta sección se encuentran instalados:

- Cuatro ruedas alineadas.
- Sistema de transmisión mediante motor paso a paso.
- Sistema diferencial de engranajes.
- Sistema de dirección Ackermann.
- Servomotor de dirección.
- Soporte para convertidor de voltaje DC-DC.

El diseño fue desarrollado para mantener una distribución equilibrada de peso y garantizar estabilidad durante el movimiento autónomo.

---

# Sistema de transmisión

## Motor y diferencial

El sistema de movimiento utiliza:

- Motor paso a paso NEMA 17.
- Engranaje diferencial bevel de 28 dientes.
- Eje de transmisión hacia las ruedas posteriores.

El motor transmite el movimiento mediante el sistema diferencial, permitiendo que las ruedas puedan adaptarse a diferentes velocidades durante los giros.

Este mecanismo reduce esfuerzos mecánicos y mejora la estabilidad del vehículo en curvas.

El soporte del motor fue diseñado para mantener una correcta alineación entre los engranajes y evitar pérdidas por desajustes mecánicos.

---

# Sistema de dirección Ackermann

El robot utiliza una geometría Ackermann para mejorar el comportamiento durante los giros.

El sistema está compuesto por:

- Soportes de ruedas delanteras.
- Elementos de unión de dirección.
- Ejes de giro.
- Servomotor.
- Sistema de conexión mecánica.

Durante las primeras pruebas se identificó que las piezas impresas en 3D presentaban cierta resistencia debido al contacto directo entre superficies plásticas.

Esto generaba:

- Mayor fricción.
- Menor precisión del movimiento.
- Mayor esfuerzo del servomotor.
- Variaciones en el ángulo de giro.

Para solucionar este problema se rediseñaron los soportes incorporando rodamientos de acero en los puntos de rotación.

La implementación de rodamientos permitió:

- Reducir la resistencia mecánica.
- Mejorar la suavidad del movimiento.
- Aumentar la precisión del control del servomotor.
- Obtener una respuesta más estable del sistema Ackermann.

---

# Placa intermedia de componentes electrónicos

La placa intermedia fue diseñada para organizar y proteger los componentes eléctricos del robot.

En ella se montan:

- Arduino Uno R3 Microcontroller.
- Mini protoboard.
- Baterías recicladas 18650 (4 celdas).
- Convertidor DC-DC de 12V a 5V (6A - 30W).
- Distribución del cableado.

La separación entre la placa inferior y la placa intermedia fue definida mediante separadores, considerando:

- Espacio necesario para cables.
- Facilidad de mantenimiento.
- Protección de componentes.
- Evitar contacto entre sistemas mecánicos y eléctricos.

---

# Sistema de alimentación

El robot utiliza un conjunto de cuatro baterías recicladas 18650.

La ubicación del sistema de baterías fue definida buscando:

- Mantener el centro de gravedad equilibrado.
- Evitar desplazamientos de peso durante aceleraciones.
- Mejorar la estabilidad del vehículo.

El convertidor DC-DC permite adaptar la tensión del sistema de baterías a los niveles requeridos por los componentes electrónicos.

---

# Placa superior y sistema de visión

La placa superior permite cerrar la estructura del robot y proporciona soporte para:

- Raspberry Pi 5 Starter Kit.
- Cámara Raspberry Pi.

El soporte de cámara fue diseñado para mantener una posición fija respecto al chasis.

Su ubicación permite realizar una correcta calibración considerando:

- Distancia hacia obstáculos.
- Altura de visión.
- Reconocimiento de elementos de la pista.

Una posición estable de la cámara permite mejorar la repetibilidad del sistema autónomo durante las pruebas.

---

# Procedimiento de ensamblaje

## 1. Ensamblaje del chasis inferior

1. Instalar el motor NEMA 17 en su soporte.
2. Colocar el sistema diferencial de engranajes.
3. Verificar alineación del eje de transmisión.
4. Instalar las ruedas posteriores.
5. Montar el sistema Ackermann delantero.
6. Instalar los rodamientos en los puntos de giro.
7. Conectar el servomotor al sistema de dirección.

---

## 2. Instalación de placa intermedia

1. Colocar los separadores entre placas.
2. Fijar la placa intermedia mediante pernos.
3. Instalar Arduino Uno.
4. Colocar baterías y convertidor DC-DC.
5. Organizar conexiones eléctricas.

---

## 3. Instalación de placa superior

1. Fijar la placa superior al conjunto.
2. Instalar Raspberry Pi 5.
3. Colocar soporte de cámara.
4. Ajustar posición de cámara según las necesidades de calibración.






