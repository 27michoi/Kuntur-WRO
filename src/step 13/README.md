## Step 13

### Resumen

El paso 13 evalúa la capacidad de esquivar un único obstáculo a una velocidad controlada de 600 pasos/s en cuatro condiciones distintas: ambas direcciones de conducción (derecha e izquierda) combinadas con ambos colores de obstáculo (verde y rojo). La prueba utiliza la lógica de competición existente, el proceso de procesamiento de la cámara y los modelos de seguimiento de paredes sin necesidad de realizar modificaciones en `main.py` ni en el firmware de Arduino.

___

### Reglas y Sistema

* **Reglas sobre obstáculos:**
* **Obstáculos verdes:** El robot debe pasar por el lado **derecho**.
* **Obstáculos rojos:** El robot debe pasar por el lado **izquierdo**.
* *Nota:* El indicador `--direction` indica la dirección de la vuelta, no el lado por el que debe esquivar el obstáculo.


* **Comprobación previa al vuelo:** Antes de moverse, el software comprueba que el color del obstáculo objetivo sea visible. Si no se detecta, el sistema se detiene (`PREFLIGHT_OBSTACLE_NOT_CONFIRMED`).
* **Límites calibrados:**
* Centro del servo: 82
* Límites del servo en dirección izquierda: 75–92
* Límites del servo en dirección derecha: 72–90

___

### Instrucciones

1. **Script de configuración y directorios**
* Crea las carpetas de destino y el archivo del script de prueba directamente en la Raspberry Pi:
```bash
cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package
source ../.venv/bin/activate
mkdir -p step13_tests ../../step13_results/logs ../../step13_results/frames
touch step13_tests/__init__.py
nano step13_tests/obstacle_avoidance_low_speed.py

```

* Pega el contenido del script, guarda el archivo y comprueba que se compila correctamente con el comando `python -m py_compile step13_tests/obstacle_avoidance_low_speed.py`.


2. **Preparación del campo**
* Utiliza un único tramo recto de pista en el que solo se coloque el obstáculo de prueba en una posición reglamentaria.
* Coloca el robot en línea recta sobre la pista **entre 50 y 70 cm antes del obstáculo**.
* Asegúrate de que no haya cables sueltos, de que haya una línea de visión despejada para la comprobación previa al inicio y de que se pueda acceder manualmente al interruptor de encendido.


3. **Ejecuta las 4 configuraciones de prueba**
Ejecuta cada comando de forma secuencial, cambiando la posición del robot y los obstáculos entre cada ejecución:
* **Dirección derecha + obstáculo verde**
```bash
python -u -m step13_tests.obstacle_avoidance_low_speed --direction right --color green --steps 1700 2>&1 | tee ../../step13_results/logs/right_green_console.log

```

* **Dirección derecha + obstáculo rojo**
```bash
python -u -m step13_tests.obstacle_avoidance_low_speed --direction right --color red --steps 1700 2>&1 | tee ../../step13_results/logs/right_red_console.log

```

* **Dirección izquierda + obstáculo verde**
```bash
python -u -m step13_tests.obstacle_avoidance_low_speed --direction left --color green --steps 1700 2>&1 | tee ../../step13_results/logs/left_green_console.log

```

* **Dirección izquierda + obstáculo rojo**
```bash
python -u -m step13_tests.obstacle_avoidance_low_speed --direction left --color red --steps 1700 2>&1 | tee ../../step13_results/logs/left_red_console.log

```

___

### Troubleshooting

* **Distancia insuficiente:** Si la maniobra de evasión se ejecuta correctamente pero el robot se detiene antes de haber superado por completo el obstáculo, vuelve a ejecutar solo esa prueba concreta aumentando la distancia a `--steps 2000`. No aumentes la velocidad.
* **Interrupciones:** Pulsa `Ctrl+C` o apaga el interruptor de alimentación del motor si el robot intenta pasar por el lado equivocado, entra en contacto con una pared u obstáculo, u oscila excesivamente.

___

### Requisitos para superar la prueba (las 4 ejecuciones):

* Superada la comprobación previa (`Preflight passed: True`).
* El robot pasa por el verde a la derecha y por el rojo a la izquierda.
* Cero contacto con obstáculos o paredes, sin oscilaciones graves en la dirección y reanudación satisfactoria del seguimiento de la pared.
* Las salidas de los servos se mantienen dentro de los límites calibrados.
* El resumen de la consola muestra `Motivo de la parada: TARGET_COMPLETE` y `Resultado técnico: APROBADO`.

### Materiales que se deben enviar:

1. Empaquetar todos los resultados en un archivo:
```bash
cd /home/admin/Projects/WRO2026-CLM
tar -czf step13_for_review.tar.gz step13_results

```

2. Envía `step13_for_review.tar.gz` junto con las respuestas de observación de las cuatro ejecuciones (confirmando: lado correcto, sin contacto con obstáculos, sin contacto con paredes, sin oscilaciones fuertes).

___

