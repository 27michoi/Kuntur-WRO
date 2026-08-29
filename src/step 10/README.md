## Step 10

### Resumen

El paso 10 valida el algoritmo de seguimiento de paredes de la competición en un entorno de línea recta y a baja velocidad antes de intentar realizar giros. Integra el firmware original de Arduino, los módulos `CameraManager`, `ImageAlgorithms` y `ArduinoComms` del repositorio para garantizar que el control de dirección en bucle cerrado funcione correctamente sin chocar contra las paredes ni oscilar.
___

### Preparación y configuración

1. **Restauración del firmware:** Vuelve a flashear el firmware original de la competición a través de PlatformIO (`code/arduino`) para restaurar los protocolos estándar de comunicación serie:
* Comando de movimiento continuo: `m<ángulo>,<velocidad>.`
* Comando de movimiento por pasos hasta un objetivo: `<pasos>!`


2. **Configuración del entorno y los directorios:** Configura el entorno virtual de Python y las dependencias, y crea los directorios `step10_results/logs` y `step10_results/frames`.


3. **Reasignación de ángulos:** Asigna el ángulo central predeterminado del repositorio (86) al centro físico calibrado del robot (**82**), limitando los límites de giro operativos entre **75 (derecha)** y **90 (izquierda)**.

___

### Ejecución

**Creación del script:** Implementa `step10_tests/wall_follow_low_speed.py`, que:
* Acepta `--direction` (`left` o `right`), `--steps` (100–2000) y `--speed` (fijada en 600 pasos/segundo).
* Realiza una cuenta atrás de 5 segundos.
* Captura imágenes de forma continua, calcula las posiciones de las paredes mediante `find_wall_to_follow()`, convierte dinámicamente los ángulos de giro y actualiza el Arduino.
* Registra la telemetría de la ejecución en un archivo CSV y guarda fotogramas de diagnóstico cada 5 fotogramas.

**Progresión de las pruebas:**
1. **Prueba con rueda levantada:** Verifica los movimientos de los servos, los límites (75–90) y el apagado automático del motor (`TARGET_COMPLETE`) sin contacto con el suelo.
2. **Recorridos cortos por el suelo:** Ejecuta 500 pasos (~300 mm) tanto hacia la izquierda como hacia la derecha en una trayectoria recta.
3. **Recorridos medios por el suelo:** Ejecutar 1000 pasos (~600 mm).
4. **Recorridos completos de 1 metro:** Ejecutar 1660 pasos (~1000 mm) tanto hacia la izquierda como hacia la derecha.

___

### Criterios de finalización 

**Criterios de superación:**
* Ejecución impecable utilizando componentes reales del repositorio (`CameraManager`, `ArduinoComms` y `calculate_servo_angle_from_walls()`).
* Finalización satisfactoria de recorridos de 1660 pasos (~1 metro) en ambas direcciones a una velocidad de 600.
* Cero contactos con las paredes, cero oscilaciones excesivas de la dirección y parada automática a la distancia objetivo.

**Resultados que deben incluirse en el informe:**
* Salidas de la consola de las pruebas de 1 660 pasos hacia la izquierda y hacia la derecha.
* Archivos de registro (`.csv`) de `step10_results/logs/`.
* Imágenes de diagnóstico (`.jpg`) de `step10_results/frames/`.
* Informe de estado que confirme la ausencia de contacto con las paredes y de oscilaciones en ambas pruebas.

____
