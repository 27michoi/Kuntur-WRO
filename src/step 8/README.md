## Step 8

### Resumen

El paso 8 verifica que la configuración final de la cámara proporcione imágenes nítidas y correctamente encuadradas al proceso de visión del repositorio **antes** de que el robot se mueva. Dado que el Módulo de Cámara 3 estándar tiene un campo de visión más estrecho (75°) que la cámara original del equipo (120°), estas pruebas estáticas garantizan que su perspectiva siga captando suficientes detalles de la pista para la navegación autónoma.

___

### Detalles de hardware y configuración

* **Energía y control:** Solo se alimenta la Raspberry Pi (mediante un cargador portátil); los motores de propulsión permanecen desconectados. Controla la Pi a través de VS Code Remote SSH por Wi-Fi.
* **Transmisión de imágenes:** Visualiza los fotogramas capturados directamente en tu portátil a través de VS Code, en lugar de utilizar las ventanas de visualización estándar de OpenCV en tiempo real.
* **Especificaciones de la imagen:** La Pi captura a **640 × 360** píxeles. A continuación, el software recorta las 80 filas superiores, dejando una región de trabajo de **640 × 280**.
* **Parámetros de la cámara que se deben registrar:** Anota la altura de la lente (mm), el ángulo de inclinación (°), la distancia al eje delantero (mm), el centrado horizontal y las condiciones de iluminación.

___

### Ejecución

1. **Comprobación del estado de la cámara (`step8_01_camera_health.py`)**
* Ejecuta `rpicam-hello --list-cameras` para confirmar que el sensor se registra como `imx708`.
* Ejecuta el script para comprobar la estabilidad de la transmisión, medir la frecuencia de fotogramas y capturar un fotograma de prueba de 640 × 360.


2. **Verificación del encuadre y el recorte (`step8_02_framing_and_crop.py`)**
* Captura una imagen de muestra para verificar que la cámara esté nivelada, centrada y sin obstrucciones por parte del chasis.
* Revisa los archivos de salida (`full 640×360`, `cropped 640×280` y `marked-crop`) para asegurarte de que las líneas del campo y los obstáculos encajan dentro de la región inferior de 280 píxeles. Ajusta el soporte físico si es necesario.


3. **Captura del conjunto de datos estático (`step8_03_capture_dataset.py SCENARIO_NAME`)**
* Coloca manualmente el robot en posiciones críticas del campo (sin alterar el soporte de la cámara) y captura imágenes para:
* **Posición de salida (SP):** Recta centrada.
* **Cerca de las paredes (CL):** Cerca de los límites izquierdo y derecho.
* **Acercándose a las esquinas (AC):** Al acercarse a las curvas.
* **Líneas del campo (BOL):** Líneas delimitadoras azules y naranjas.
* **Obstáculos (FRG):** Obstáculos rojos y verdes tanto a corta como a larga distancia.
* **Zona de aparcamiento (PP):** Zonas de aparcamiento de color rosa.


4. **Prueba del proceso de visión (`step8_04_pipeline_test.py`)**
* Introduce el conjunto de datos estáticos en el proceso del software para confirmar que procesa los cultivos sin fallar y que genera correctamente las máscaras de color iniciales (azul, naranja, verde, rojo, rosa) y las detecciones de paredes y suelos.

____

### Requisitos para superar la prueba

* El sensor se identifica correctamente como «imx708» en la Pi 5.
* La cámara física está fija, nivelada, centrada y documentada.
* Se generan imágenes recortadas nítidas de 640 × 280 sin obstrucciones del chasis.
* Los elementos cruciales de la pista (paredes, obstáculos, líneas de color) permanecen totalmente visibles dentro del campo de visión de 75°.
* El proceso genera con éxito máscaras de detección básicas en todos los escenarios estáticos guardados. 

___



