## Step 1

### Resumen

El objetivo de este paso es comprobar que la Raspberry Pi 5 detecta correctamente el módulo de cámara «Camera Module 3 Wide» y se comunica con él antes de continuar con cualquier código específico del proyecto relacionado con la cámara o el procesamiento de imágenes.

Se trata de un paso de validación a nivel de hardware y del sistema. La cámara debe estar primero conectada físicamente de forma correcta y ser reconocida por el sistema operativo Raspberry Pi antes de que pueda ser utilizada por los sistemas Python Picamera2, OpenCV y de procesamiento de imágenes del proyecto.

El procedimiento consiste en:

1. Apagar de forma segura la Raspberry Pi antes de conectar o volver a conectar la cámara.
2. Comprobar la conexión física del cable plano CSI.
3. Arrancar la Raspberry Pi.
4. Verificar que la cámara se detecta mediante el comando rpicam-hello --list-cameras.
5. Confirmar que la cámara puede inicializarse y mostrar una vista previa en directo mediante rpicam-hello.

Objetivo:
Confirmar que la Raspberry Pi 5 puede detectar e inicializar correctamente el módulo de cámara 3 Wide.

El paso 1 se da por completado cuando:
rpicam-hello --list-cameras detecta al menos una cámara.
rpicam-hello inicializa correctamente la cámara y muestra una vista previa en directo.

____
