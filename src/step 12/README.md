## Step 12

### Resumen

El paso 12 pone a prueba la capacidad del robot para completar una vuelta completa sin obstáculos a una velocidad fija de 600 pasos/s. Utilizando el firmware de competición existente del paso 11 junto con las clases del repositorio principal (`CameraManager`, `LapTracker`, `ContextManager` y `ArduinoComms`), el robot sigue y recorre cuatro cuartos de vuelta mediante la detección de líneas azules y naranjas, deteniéndose automáticamente una vez completada la vuelta.

___

### Instrucciones

1. **Preparación del campo**
* Retira todos los obstáculos rojos y verdes, así como los elementos de aparcamiento, de la pista.
* Mantén una iluminación constante (que se ajuste a las condiciones del paso 11).
* Coloca el robot centrado en un tramo recto antes de la primera secuencia de líneas azules y naranjas, asegurándote de que los cables USB queden sueltos.



2. **Configuración y verificación del script**
* Instala `step12_one_complete_lap.py` en la Raspberry Pi:
```bash
cd /home/admin/Projects/WRO2026-CLM/code/XX_2025_package
source ../.venv/bin/activate
mkdir -p step12_tests ../../step12_results/logs ../../step12_results/frames
touch step12_tests/__init__.py
cp ~/Descargas/step12_one_complete_lap.py step12_tests/one_complete_lap.py
```
* Comprueba que el script se compila correctamente y que se importan los módulos:
```bash
python -m py_compile step12_tests/one_complete_lap.py
```
* Asegúrate de que la conexión con Arduino se reconoce en `/dev/ttyACM0`.



3. **Ejecución**
* Ejecuta la prueba en cualquiera de las dos direcciones (solo es necesaria una):
* **Dirección derecha:**
```bash
python -u -m step12_tests.one_complete_lap --direction right 2>&1 | tee ../../step12_results/logs/right_console.log
```
* **Dirección izquierda:**
```bash
python -u -m step12_tests.one_complete_lap --direction left 2>&1 | tee ../../step12_results/logs/left_console.log

```
* Despeja el circuito durante la cuenta atrás de 5 segundos.



4. **Seguimiento y parada automática**
* La parada se activa cuando el `LapTracker` registra cuatro cuartos de vuelta consecutivos (del `1/4` al `4/4`).
* Los límites de la dirección servo se aplican dinámicamente en función de la dirección (derecha: 72–90; izquierda: 75–90).
* Los límites de seguridad de respaldo (25 000 pasos / tiempo de espera de 50 segundos) solo existen para interrupciones de emergencia.


___

### Seguridad y resolución de problemas

* **Interrupción de emergencia:** Pulsa inmediatamente `Ctrl+C` o acciona el interruptor de encendido del motor si el robot corre el riesgo de chocar contra una pared, se salta un giro, oscila violentamente, no se detiene o si la cámara se bloquea.
* **Problemas de detección de la línea:** No aumentes los límites de pasos ni los tiempos de espera si la vuelta física se completa sin alcanzar «4/4»; esto indica un problema de detección de la línea, no una limitación de distancia.

___

### Requisitos para superar la prueba:

* Los informes técnicos indican «Vuelta completada: True», «Motivo de la parada: LAP_COMPLETE» y «Resultado técnico: PASS».
* El robot recorre cuatro esquinas físicas sin chocar contra las paredes ni oscilar de forma severa.
* Se detiene automáticamente cerca de la sección de salida al registrar 4/4 cuartos de vuelta.

### Entregables que hay que presentar:

* Salida final del registro de la consola:
```bash
tail -n 25 ../../step12_results/logs/right_console.log
```
* El último archivo CSV de registro generado durante la ejecución.
* Cuatro confirmaciones de observación física:
1. Se ha completado una vuelta física (sí/no)
2. Contacto con la pared (sí/no)
3. Oscilación intensa (sí/no)
4. Se ha detenido automáticamente cerca de la sección de salida (sí/no)


*(Nota: Las imágenes de diagnóstico solo son necesarias si se produce un contacto con la pared o si la prueba da como resultado `REVIEW`).*

___


