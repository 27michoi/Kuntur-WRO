## Step 11

### Resumen

En el paso 11 se comprueba la capacidad del robot para sortear una sola esquina a baja velocidad (600 pasos/s) utilizando el algoritmo de seguimiento de paredes y el sistema de visión de serie. Se evalúan tanto los giros a la izquierda como a la derecha utilizando el firmware de Arduino existente del paso 10, sin que sea necesario recalibrar el algoritmo ni los servomotores.

___

### Instrucciones

1. **Instalación y verificación del script**
* Descarga el archivo `step11_one_corner_low_speed.py` en la Raspberry Pi, en el directorio `/home/admin/Projects/WRO2026-CLM/code/XX_2025_package/step11_tests/one_corner_low_speed.py`.
* Crea las carpetas de salida: `step11_results/logs` y `step11_results/frames`.
* Compila el archivo Python con el comando `python -m py_compile` para verificar la sintaxis.
* Verifica las dependencias del paquete con:
```bash
python -c «from classes.camera_manager import CameraManager; from classes.image_algoriths import ImageAlgorithms; from classes.arduino_comms import ArduinoComms; print(“STEP 11 IMPORTS OK”)»

```

2. **Lógica de parada automática**
* El límite de recorrido por defecto está fijado en **6.500 pasos**.
* Al detectar una esquina, el objetivo se ajusta automáticamente a **4.000 pasos** tras el giro.
* Una carrera superada concluye con el motivo de parada: `CORNER_EXIT_COMPLETE`. Alcanzar el límite de reserva sin detectar una esquina (`MAX_DISTANCE_COMPLETE_NO_CORNER`) constituye una carrera fallida.

3. **Preparación del campo**
* Utiliza una sección del campo WRO libre de obstáculos con una recta de entre 400 y 500 mm que preceda a una curva despejada.
* Alinea el robot en paralelo a la pared de salida, asegurándote de que no haya interferencias con los cables.


4. **Ejecución en la esquina izquierda**
* Coloca el robot en el carril de giro a la izquierda.
* Ejecuta el comando:
```bash
python -m step11_tests.one_corner_low_speed --direction left --max-steps 6500 --exit-steps 4000 2>&1 | tee ../../step11_results/logs/left_console.log

```
* Aléjate durante la cuenta atrás de 5 segundos.
* Comprueba que el robot sigue la pared (rango del servo: 75–90), detecta la esquina, completa el giro, entra en la siguiente recta y se detiene sin tocar la pared ni presentar oscilaciones excesivas en la dirección.


5. **Ejecución en la esquina derecha**
* Mueve el robot para que se acerque a la esquina desde la dirección opuesta.
* Ejecuta el comando:
```bash
python -m step11_tests.one_corner_low_speed --direction right --max-steps 6500 --exit-steps 4000 2>&1 | tee ../../step11_results/logs/right_console.log
```
* Comprueba que el rendimiento del giro sea idéntico en dirección hacia la derecha.

___

### Ajustes de seguridad y distancia

* **Interrupción de emergencia:** Pulsa `Ctrl+C` o utiliza el interruptor físico de encendido si el robot gira incorrectamente, oscila violentamente, se mueve hacia atrás o corre el riesgo de chocar contra una pared.
* **Ajuste de los pasos de salida:** Si es necesario ajustar la posición de parada física tras una pasada técnica:
* *Se queda corto en la curva:* Aumenta a `--exit-steps 4500`
* *Se pasa de largo en la recta:* Disminuye a `--exit-steps 3500`

___

### Requisitos de la pasada (en ambas direcciones):

* Estado técnico: `PASS` (`Curva aceptada: True`, `Objetivo completado: True`, `Motivo de la parada: CORNER_EXIT_COMPLETE`).
* Velocidad fija en 600; salida del servo entre 75 y 90.
* Giro de ~90° completado hacia la siguiente recta.
* Sin choques contra las paredes, oscilaciones continuas de la dirección ni movimiento hacia atrás.

### Materiales que se deben presentar:

* Archivos de registro: `left_console.log` y `right_console.log`.
* Archivos CSV de telemetría de ambas pruebas.
* 6 imágenes de diagnóstico (3 por prueba: aproximación a la recta, fotograma `_CORNER` y salida de la recta).
* Notas de observación de ambas pruebas en las que se evalúen la finalización de la curva, el contacto con la pared, la alineación en la salida y la gravedad de la oscilación.


___

