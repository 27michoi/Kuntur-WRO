## Resumen

Este documento te guía a lo largo del proceso de configuración, prueba y calibración del movimiento en línea recta de 1 metro de un robot utilizando PlatformIO, código C++ y comandos serie.

___

## Instrucciones

1. **Configuración del entorno**
* Crea un nuevo directorio de proyecto (`step6_straight_line_test`) con los subdirectorios `src` y `lib` en la Raspberry Pi a través de SSH.
* Copia las bibliotecas necesarias `FlexyStepper` y `Servo` en la carpeta `lib` del proyecto.
* Abre la carpeta del proyecto en VS Code.


2. **Configuración y creación del código**
* Crea el archivo `platformio.ini` configurado para un Arduino Uno con una velocidad de monitor de 115200.
* Crea el archivo `src/main.cpp` con el código proporcionado, que se encarga de la gestión de estados (`IDLE`, `COUNTDOWN`, `MOVING`, `STOPPING`), los comandos de entrada en serie (`GO`, `STOP`, `STATUS`, `HELP` y `A<ángulo>`), un retraso de arranque de 5 segundos y las rutinas de movimiento del motor paso a paso.


3. **Compilación y carga**
* Desconecta la batería del motor antes de realizar la carga.
* Compila utilizando `pio run`.
* Identifica el puerto serie (`/dev/ttyACM0` o similar) utilizando `pio device list`.
* Carga el firmware en el Arduino utilizando `pio run --target upload --upload-port /dev/ttyACM0`.


5. **Configuración de la prueba en el suelo**
* Marca una línea central recta (de al menos 1,2 m), una línea de salida y una línea de meta de 1000 mm sobre una superficie plana y dura.
* Coloca el robot centrado sobre la línea de referencia de salida, con las ruedas delanteras rectas y un cable USB suelto colgando por detrás.


6. **Recopilación de datos y calibración**
* Ejecuta `A99` seguido de `GO` para realizar tres pruebas en el suelo independientes. Mide y anota:
* Distancia recorrida hacia delante
* Error de distancia (mm reales menos 1000 mm)
* Desviación lateral y dirección de la deriva (izquierda/derecha)


* **Calibración de la dirección:** Ajusta el ángulo 1 grado cada vez (`A98` si se desvía hacia la izquierda, `A100` si se desvía hacia la derecha). Comprueba la alineación mecánica si se necesita una corrección de más de 3 grados. Actualiza `SERVO_CENTER` en el código una vez calibrado.
* **Calibración de la distancia:** Calcula el nuevo recuento de pasos utilizando la fórmula:

$$\text{Nuevos pasos} = 6400 \times \frac{1000}{D_{\text{promedio}}}$$


Actualiza `TEST_STEPS` en `main.cpp` y vuelve a subirlo. 


7. **Criterios de superación y entregables obligatorios**
* **Criterios de superación:** 3 recorridos consecutivos sin reinicios ni bloqueos, parada automática, distancia media final dentro de un margen de $\pm 30\text{ mm}$ respecto a 1000 mm, desviación lateral dentro de un margen de $\pm 50\text{ mm}$ y ausencia de sobrecalentamiento del hardware.
* **Resultados que hay que enviar:**
* Las tres distancias medidas y las desviaciones laterales.
* Confirmación de que 6400 pasos hicieron avanzar al robot.
* Fotos: vista desde arriba en `A99`, vista lateral de la rueda junto a una regla y un primer plano de los engranajes y los puentes de micropasos.


____
