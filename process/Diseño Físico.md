# Diario de Ingeniería - Diseño Físico del Robot Autónomo

## Inicio del proceso de diseño

El desarrollo mecánico del robot inició mediante el análisis de diferentes diseños utilizados en competencias anteriores de WRO Future Engineers, sistemas motrices encontrados en vehículos comerciales y soluciones mecánicas disponibles en plataformas como LEGO.

El objetivo inicial fue tener una arquitectura que facilitara:

- El montaje y desmontaje durante las pruebas.
- La modificación rápida de componentes.
- La accesibilidad de los sistemas internos.
- La preparación del robot para la presentación final.

Luego de evaluar diferentes alternativas, se decidió implementar una estructura modular basada en un chasis de tres niveles.

---

# Decisión del diseño modular del chasis

## Problema identificado

Un diseño de una sola placa generaba dificultades para integrar:

- Sistema de transmisión.
- Dirección.
- Baterías.
- Placas electrónicas.
- Sistema de procesamiento Raspberry Pi.
- Cámara.

Además, dificultaba realizar modificaciones rápidas durante las pruebas.

## Solución implementada

Se desarrolló un diseño compuesto por tres niveles:

### Nivel inferior:
Sistema mecánico:

- Motor.
- Diferencial.
- Ruedas.
- Dirección Ackermann.

### Nivel intermedio:
Sistema electrónico:

- Arduino.
- Baterías.
- Cableado.
- Conversor de voltaje.

### Nivel superior:
Sistema de procesamiento:

- Raspberry Pi.
- Cámara.

## Justificación

Esta separación permitió:

- Mejor organización interna.
- Mayor facilidad de mantenimiento.
- Menor interferencia entre componentes.
- Mayor rapidez para realizar ajustes.

---

# Desarrollo del sistema de transmisión

## Evaluación inicial

Se analizaron diferentes sistemas motrices utilizados en robots anteriores y vehículos comerciales.

El objetivo era encontrar una solución que proporcionara:

- Precisión de movimiento.
- Control adecuado de velocidad.
- Facilidad de integración.

## Decisión tomada

Se seleccionó:

- Motor paso a paso NEMA 17.
- Sistema diferencial mediante engranajes bevel de 28 dientes.

## Razón de la elección

El motor paso a paso permite controlar con precisión el desplazamiento del robot.

El diferencial fue seleccionado porque durante los giros las ruedas no recorren la misma distancia, por lo que permite reducir esfuerzos mecánicos y mejorar la estabilidad.

---

# Problema encontrado en el sistema Ackermann

## Primera versión

La primera versión del sistema Ackermann fue fabricada completamente mediante impresión 3D.

Durante las pruebas se observó:

- Movimiento irregular.
- Mayor resistencia mecánica.
- Pérdida de precisión del servomotor.
- Variación en el ángulo de dirección.

## Análisis del problema

La causa principal fue la fricción generada entre piezas impresas en 3D.

Debido a las características del proceso de impresión:

- Las superficies no eran completamente lisas.
- Existían pequeñas tolerancias dimensionales.
- Los puntos de giro presentaban resistencia.

Esto afectaba directamente la respuesta del sistema de dirección.

---

# Mejora mediante rodamientos

## Cambio realizado

Se rediseñaron los soportes delanteros incorporando rodamientos de acero en los puntos de giro.

## Motivo del cambio

Los rodamientos permiten reemplazar el contacto directo entre piezas plásticas por un movimiento rotacional más eficiente.

## Resultado obtenido

Después de la modificación:

- El movimiento del sistema Ackermann fue más suave.
- El servomotor requirió menor esfuerzo.
- La dirección presentó mayor precisión.
- El comportamiento durante pruebas fue más repetible.

Este diseño fue seleccionado para la versión final del robot.

---

# Diseño del sistema electrónico integrado

## Problema inicial

Durante las primeras configuraciones se identificó que los cables y componentes electrónicos podían interferir con la estructura mecánica.

Esto generaba:

- Mayor dificultad de ensamblaje.
- Riesgo de desconexiones.
- Mayor tiempo de mantenimiento.

## Solución

Se diseñó una placa intermedia específica para organizar:

- Arduino Uno.
- Protoboard.
- Baterías.
- Convertidor DC-DC.
- Cableado.

## Justificación

La placa permitió crear una estructura más limpia y modular, donde cada componente tiene una ubicación definida.

---

# Distribución de baterías y peso

Las baterías 18650 fueron ubicadas en la zona central del robot.

Esta decisión fue tomada considerando:

- Distribución uniforme de masa.
- Menor transferencia de peso durante aceleraciones.
- Mayor estabilidad en curvas.

Mantener el centro de gravedad bajo y centrado ayuda a mejorar el comportamiento del vehículo autónomo.

---

# Diseño del soporte de cámara

## Problema identificado

La precisión del sistema autónomo depende directamente de la información obtenida por la cámara.

Cambios pequeños en la posición podían modificar:

- Distancias calculadas.
- Detección de obstáculos.
- Interpretación de la pista.

## Modificación realizada

Se diseñó un soporte específico para Raspberry Pi Camera.

El soporte permite mantener:

- Altura constante.
- Ángulo fijo.
- Posición repetible.

## Resultado

La cámara pudo ser calibrada de forma consistente respecto a la pista y los obstáculos de la competencia.

---

# Diseño final seleccionado

Después de las pruebas realizadas, el diseño final integra:

- Chasis modular de tres niveles.
- Sistema diferencial con motor NEMA 17.
- Dirección Ackermann mejorada con rodamientos.
- Distribución organizada de componentes electrónicos.
- Sistema de cámara estable.

Cada modificación realizada respondió a un problema identificado durante pruebas físicas, buscando mejorar la precisión, confiabilidad y facilidad de mantenimiento del robot durante la competencia WRO Future Engineers.
