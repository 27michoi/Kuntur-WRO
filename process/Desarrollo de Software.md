# Diario de Ingeniería - Desarrollo del Sistema de Programación del Robot Autónomo

## Introducción

El desarrollo del software del robot autónomo para la competencia WRO Future Engineers se realizó mediante un proceso progresivo de pruebas, validaciones y mejoras.

El objetivo principal fue construir un sistema capaz de:

- Controlar el movimiento del robot con precisión.
- Interpretar el entorno mediante visión artificial.
- Seguir la trayectoria de la pista.
- Detectar obstáculos.
- Tomar decisiones autónomas durante la competencia.

El desarrollo se dividió en diferentes etapas, comenzando desde la validación individual de componentes hasta la integración completa del sistema autónomo.

---

# Etapa inicial: Validación del movimiento y comunicación

## Objetivo

Antes de desarrollar algoritmos autónomos, fue necesario comprobar que la plataforma física respondiera correctamente.

Las primeras pruebas estuvieron enfocadas en:

- Comunicación entre Raspberry Pi y Arduino.
- Control del motor paso a paso.
- Control del servomotor.
- Determinación de velocidades seguras.
- Calibración inicial de dirección.

## Problema encontrado

El robot presentaba diferencias entre los valores enviados por software y el movimiento físico real.

Esto ocurrió debido a:

- Tolerancias mecánicas.
- Diferencias entre el ángulo indicado y el ángulo real del servo.
- Respuesta del sistema de transmisión.

## Solución aplicada

Se realizaron pruebas independientes para determinar:

- Velocidad máxima estable.
- Posición central real del servo.
- Límites seguros de giro.

Estos valores fueron utilizados posteriormente en los algoritmos autónomos.

---

# Desarrollo del sistema de cámara y visión artificial

## Primera etapa: Validación de imagen

Antes de implementar reconocimiento de objetos, se evaluó el comportamiento de la cámara en diferentes condiciones.

Se realizaron capturas considerando:

- Iluminación normal.
- Alta iluminación.
- Baja iluminación.
- Diferentes posiciones dentro de la pista.

También se analizaron:

- Paredes.
- Líneas de colores.
- Obstáculos.
- Zona de estacionamiento.

## Razón de esta etapa

La cámara es el principal sensor del robot, por lo que era necesario conocer cómo cambiaban las imágenes antes de crear algoritmos de decisión.

---

# Desarrollo del pipeline de visión

## Primera aproximación

Inicialmente se evaluó la detección directa mediante imágenes completas.

Sin embargo, este método generaba problemas debido a:

- Elementos irrelevantes dentro del campo visual.
- Variaciones de iluminación.
- Ruido en la imagen.

## Mejora implementada

Se desarrolló un pipeline de procesamiento:

1. Captura de imagen.
2. Recorte de región de interés (ROI).
3. Conversión a espacio HSV.
4. Creación de máscaras de color.
5. Limpieza mediante operaciones morfológicas.
6. Detección de contornos.
7. Obtención de centroides y dimensiones.

## Resultado

El robot pudo identificar de manera más estable:

- Líneas de pista.
- Obstáculos.
- Paredes.
- Elementos de colores utilizados en la competencia.

---

# Validación offline del sistema de visión

## Problema

Probar directamente en pista cada modificación del algoritmo consumía demasiado tiempo.

## Solución

Se creó un conjunto de imágenes de prueba obtenidas durante diferentes situaciones reales.

Estas imágenes permitieron evaluar:

- Cambios en iluminación.
- Falsos positivos.
- Capacidad de detección.

## Resultado

El sistema pudo mejorarse antes de realizar pruebas físicas, reduciendo tiempo de ajuste en pista.

---

# Desarrollo del seguimiento de paredes (Wall Following)

## Primera estrategia autónoma

Después de validar la visión, se desarrolló un método inicial basado en seguimiento de paredes.

El objetivo era que el robot pudiera mantener una distancia estable respecto al borde de la pista.

## Pruebas realizadas

Se evaluaron:

- Seguimiento por izquierda.
- Seguimiento por derecha.
- Diferentes velocidades del motor.
- Diferentes cantidades de pasos del motor.

Se realizaron pruebas con:

- 600 steps/s.
- 1660 steps.

## Problemas encontrados

El robot podía mantener la trayectoria, pero presentaba dificultades en:

- Curvas cerradas.
- Cambios bruscos de dirección.
- Interacción con obstáculos.

## Aprendizaje

El seguimiento de pared funcionaba como una base estable, pero necesitaba combinarse con detección de objetos para resolver completamente el desafío.

---

# Integración del sistema autónomo completo

## Creación de módulos de software

Para mejorar la organización del código, el programa fue dividido en módulos:

### CameraManager

Responsable de:

- Captura de imágenes.
- Configuración de cámara.
- Gestión del flujo visual.

### ImageAlgorithms

Responsable de:

- Procesamiento de imágenes.
- Detección de colores.
- Identificación de elementos.

### LapTracker

Responsable de:

- Seguimiento del progreso de vueltas.
- Identificación de etapas del recorrido.

### ContextManager

Responsable de:

- Mantener información del estado actual del robot.
- Gestionar decisiones.

### ArduinoComms

Responsable de:

- Comunicación entre Raspberry Pi y Arduino.
- Envío de comandos de movimiento.

---

# Primera versión de una vuelta completa

## Método utilizado

La pista fue dividida en cuatro secciones principales.

Cada vuelta fue interpretada como cuatro secuencias:

- Quarter-lap 1.
- Quarter-lap 2.
- Quarter-lap 3.
- Quarter-lap 4.

El robot utilizaba información visual para saber en qué etapa se encontraba.

## Parámetros calibrados

Durante estas pruebas se ajustaron:

- Servo físico central: aproximadamente 82.
- Centro lógico del programa: 86.
- Límites de dirección.
- Velocidad de movimiento: 600.

## Resultado

El robot logró completar vueltas completas de forma autónoma.

---

# Desarrollo del Challenge 2: detección y evasión de obstáculos

## Primera aproximación

Se adaptó una estrategia basada en detección de obstáculos mediante color.

El robot debía:

- Detectar obstáculos.
- Determinar el lado correcto de paso.
- Modificar trayectoria.

## Problemas encontrados

Los primeros resultados mostraron que:

- Los obstáculos podían interferir con el seguimiento de pared.
- El robot podía acercarse demasiado a elementos físicos.
- Las esquinas requerían prioridad diferente.

---

# Mejora del sistema de evasión

## Cambio realizado

Se añadió:

- Margen de seguridad alrededor del obstáculo.
- Confirmación de detección durante varios frames.
- Recuperación de trayectoria después del giro.

## Lógica implementada

El robot utiliza:

- Obstáculo verde → pasar por izquierda.
- Obstáculo rojo → pasar por derecha.

La decisión no se toma con una sola imagen, sino mediante confirmación de varios frames para reducir errores.

---

# Prioridad de paredes durante curvas

## Problema final identificado

Durante las pruebas del Challenge 2 se observó que los obstáculos cercanos a las paredes podían generar conflictos entre:

- Evitar obstáculos.
- Mantener trayectoria.

## Solución

Se modificó la lógica para dar prioridad a la protección del robot cuando existe riesgo de acercamiento excesivo a paredes.

Se incorporó:

- Margen corporal de seguridad.
- Límites de servo ajustados.
- Control de pared durante esquinas.

## Resultado

El robot logró realizar movimientos más seguros, evitando perder estabilidad por realizar maniobras demasiado agresivas.

---

# Estado final del sistema de programación

La versión final integra:

- Control de motores.
- Comunicación Raspberry Pi - Arduino.
- Procesamiento de imágenes.
- Seguimiento de pista.
- Conteo de vueltas.
- Detección de obstáculos.
- Evasión automática.
- Recuperación de trayectoria.

El desarrollo del software fue un proceso iterativo donde cada mejora surgió a partir de pruebas reales del robot.

Las decisiones finales no fueron únicamente basadas en simulación, sino en el comportamiento observado físicamente durante las pruebas en pista.
