## Step 3

### Resumen

El objetivo de este paso es comprobar que el Arduino Uno puede ejecutar correctamente el firmware del proyecto y que la Raspberry Pi 5 lo reconoce como un dispositivo serie USB.

Antes de probar la comunicación con el Arduino a través del programa de Python, es necesario que el firmware del Arduino se compile y se cargue correctamente. El proyecto de Arduino se gestiona por separado del paquete de Python y contiene varios archivos fuente y de cabecera necesarios para la compilación. El firmware utiliza la clase `SerialReceiver` para procesar los comandos entrantes e inicializa la comunicación serie a `115200` baudios.

Tras cargar el firmware, el Arduino se conecta a la Raspberry Pi a través de USB. A continuación, se comprueba en la Raspberry Pi la presencia del dispositivo serie utilizado por el sistema de comunicación en Python del proyecto. La configuración actual del proyecto espera que el Arduino aparezca como `/dev/ttyACM0`.

El procedimiento consiste en:

1. Localizar el código fuente del proyecto de Arduino y comprobar que la estructura completa del proyecto está disponible.
2. Conectar el Arduino Uno a un ordenador mediante un cable de datos USB.
3. Abrir el proyecto de Arduino en el IDE de Arduino.
4. Seleccionar la placa Arduino Uno y el puerto serie correcto.
5. Compilar el proyecto de Arduino y confirmar que no se producen errores.
6. Cargar el firmware en el Arduino y confirmar que la carga se realiza correctamente.
7. Conectar el Arduino a la Raspberry Pi 5 a través de USB.
8. Comprobar si la Raspberry Pi detecta el Arduino como un dispositivo serie `ttyACM`.
9. Confirmar que `/dev/ttyACM0` está disponible.
10. Solucionar los problemas de conexión USB o de asignación del dispositivo serie si no se detecta el dispositivo esperado.

Objetivo:
Confirmar que el firmware de Arduino se compila y se carga correctamente, y que la Raspberry Pi puede detectar el Arduino como el dispositivo serie USB `/dev/ttyACM0` requerido por el sistema de comunicación en Python del proyecto.


El paso 3 se da por completado cuando:
* La estructura completa del proyecto de Arduino está disponible.
* El proyecto de Arduino se compila correctamente sin errores.
* El firmware se carga correctamente en el Arduino Uno.
* El Arduino está conectado a la Raspberry Pi 5 a través de una conexión de datos USB.
* La Raspberry Pi detecta el Arduino como un dispositivo serie.
* `/dev/ttyACM0` está disponible y el sistema puede acceder a él.
* No se producen desconexiones USB repetidas ni errores de conexión.


___


