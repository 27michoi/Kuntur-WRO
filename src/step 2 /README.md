## Step 2

### Resumen

El objetivo de este paso es comprobar que el entorno de Python de la Raspberry Pi puede acceder correctamente a las bibliotecas externas y a los módulos internos del proyecto que requiere el software del robot.

Antes de probar la captura de la cámara, el procesamiento de imágenes, la comunicación con Arduino o el programa autónomo completo, las dependencias de Python necesarias para el proyecto deben estar disponibles e importarse correctamente. Esto incluye bibliotecas externas como `cv2`, `numpy`, `serial` y `Picamera2`, así como módulos internos del proyecto dentro de los directorios `classes/` y `utils/`.

El procedimiento consiste en:

1. Acceder al directorio del proyecto de Python.
2. Confirmar que Python 3 está disponible e identificar el ejecutable de Python que se está utilizando.
3. Probar las bibliotecas externas básicas del proyecto.
4. Verificar que se pueda importar la biblioteca de la cámara `Picamera2`.
5. Probar las importaciones relacionadas con la cámara del proyecto a través de `CameraManager`.
6. Probar el conjunto completo de importaciones que requiere el programa principal sin poner en marcha el robot.

Objetivo:
Confirmar que el entorno de Python puede importar correctamente las bibliotecas externas y los módulos internos del proyecto que requiere el software del robot.


El paso 2 se da por completado cuando:
* Python 3 está disponible y se ejecuta correctamente.
* Se importan correctamente `cv2`, `numpy` y `serial`.
* Se importa correctamente `Picamera2`.
* Se importa correctamente `CameraManager`.
* Se importan correctamente los módulos necesarios del proyecto principal.
* No se producen errores `ModuleNotFoundError`, `ImportError` ni otros errores relacionados con la importación.


**Note:** Este paso solo verifica que se puedan importar las dependencias de software necesarias y los módulos del proyecto. No comprueba la captura de la cámara, el procesamiento de imágenes, la comunicación con Arduino ni la ejecución del programa autónomo completo.
