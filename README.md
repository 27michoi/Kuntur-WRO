## Introducción

Nuestro equipo Kuntur creó «Luna» para participar en el Campeonato Nacional de la WRO 2026 (Lima, Perú). «Luna» es un carro de conducción autónoma, diseñado para detectar obstáculos y analizar su entorno con el fin de adaptar su conducción de forma adecuada. Colocamos la Raspberry Pi 3 Wide en la parte superior del carro. Utilizamos un stepper motor para crear un sistema de diferencial que acciona las dos ruedas traseras y un servomotor para crear un eje para las dos ruedas delanteras. Programamos nuestra cámara para que detectara líneas específicas, objetos de colores distintivos y las paredes.

**Por favor, lee los archivos README.md en cada carpeta para comprender mejor nuestra documentación.**

---

### Visión General y Filosofía del Proyecto

El desarrollo de «Luna» representa la culminación de un proceso intensivo de ingeniería mecatrónica, diseño de software y resolución de problemas por parte del Equipo Kuntur. Diseñar un vehículo verdaderamente autónomo capaz de desenvolverse de manera fluida y precisa dentro de un tapete delimitado de 3x3 metros exige una integración armónica entre el hardware mecatrónico y los algoritmos de decisión en tiempo real.

La navegación en un espacio acotado presenta desafíos únicos. El espacio limitado requiere que las maniobras de esquiva, corrección de trayectoria y detección de límites se ejecuten con una latencia mínima. A diferencia de plataformas más grandes o que operan en entornos abiertos, «Luna» no cuenta con margen de error para desviaciones acumulativas. Una pequeña imprecisión en la lectura de la línea de carril o un retardo en la señal del servo puede traducirse en una colisión contra una pared o la desalineación irreversible del vehículo dentro del circuito. Por esta razón, el Equipo Kuntur adoptó un enfoque metodológico estricto: cada decisión de diseño, desde la selección de materiales hasta la estructura de las clases en el código fuente, se orientó hacia la estabilidad, la repetibilidad y el control de precisión.

El nombre «Luna» simboliza la exploración y la guía en entornos desafiantes, reflejando el espíritu competitivo y la dedicación del equipo durante las etapas de conceptualización, prototipado y pruebas finales para el Campeonato Nacional de la WRO 2026.

---

### Arquitectura de Hardware y Diseño Mecánico

El chasis de «Luna» se diseñó bajo el principio de rigidez estructural y modularidad. Para lograr un vehículo liviano pero resistente a las variaciones dinámicas de masa durante la aceleración y el viraje, combinamos componentes fabricados mediante impresión 3D en PLA con elementos estructurales de LEGO Technic.

#### Chasis Híbrido y Modularidad

La base estructural del carro se divide en tres secciones claramente diferenciadas:

1. **Módulo Delantero de Dirección:** Alberga el servomotor y el varillaje mecánico que conecta los manguetones de las ruedas delanteras. Se diseñó específicamente para permitir un ajuste de alineación rápido y garantizar que el eje de rotación de cada rueda respete la geometría de giro sin generar tensiones en los brazos mecánicos.
2. **Cuna Central de Electrónica:** Posicionada estratégicamente en el centro de gravedad del vehículo. En esta zona se fijan la Raspberry Pi 3 Wide, el microcontrolador de bajo nivel, los convertidores de voltaje y los circuitos de distribución de energía. Al concentrar el peso electrónico en el centro, se reduce el momento de inercia del vehículo, permitiendo giros más ágiles y predecibles.
3. **Módulo Trasero de Propulsión:** Contiene el motor paso a paso (stepper motor), el tren de engranajes reductor y el mecanismo diferencial que transmite el movimiento a las ruedas traseras.

La integración de piezas de LEGO Technic en las vigas longitudinales permitió iterar con rapidez la posición exacta de los componentes durante las fases iniciales de prueba. Posteriormente, los soportes definitivos para la cámara, los sensores y las placas electrónicas se modelaron en CAD y se imprimieron en 3D, garantizando un acoplamiento perfecto mediante tornillería estandarizada. Los archivos de estos diseños están disponibles en la carpeta `models`.

#### Sistema de Tracción Posterior por Motor Paso a Paso Único

Una de las decisiones técnicas más representativas en el diseño de «Luna» fue la utilización de un único motor paso a paso para mover ambas ruedas traseras. En lugar de recurrir a la clásica configuración de dos motores de corriente continua independientes con control diferencial por software, optamos por un esquema mecánico basado en un diferencial físico impulsado por el motor paso a paso.

Esta configuración ofrece ventajas decisivas:

* **Control de Odometría Absoluta:** Un motor paso a paso avanza en incrementos angulares exactos y discretos. Al conocer la relación de transmisión de los engranajes y el radio de las ruedas, el software puede determinar con extrema precisión la distancia lineal recorrida contando simplemente la cantidad de pulsos enviados al motor. Esto elimina la necesidad de instalar codificadores ópticos o magnéticos externos en los ejes de las ruedas.
* **Eliminación de Desviaciones por Diferencia de Motores:** En sistemas con dos motores de corriente continua, pequeñas variaciones en la resistencia interna de los motores o en la fricción de los rodamientos causan que una rueda gire ligeramente más rápido que la otra, desviando al vehículo de su trayectoria recta. Al usar un solo motor paso a paso unido a un diferencial mecánico, ambas ruedas reciben la misma fuerza motriz, garantizando un avance perfectamente rectilíneo cuando la dirección se mantiene en el centro.
* **Diferencial Mecánico Activo:** Al tomar curvas cerradas dentro del tapete de 3x3 metros, la rueda trasera interior recorre una distancia menor que la rueda exterior. El diferencial mecánico permite esta diferencia de velocidad angular entre las ruedas sin perder la tracción del motor, evitando que los neumáticos derrapen o arrastren sobre la superficie del tapete.

#### Sistema de Dirección Delantera

La dirección de «Luna» se confía a un servomotor de alta precisión conectado a las ruedas delanteras mediante un varillaje articulado.

* **Geometría de Dirección:** El mecanismo se diseñó para aproximar la geometría de giro Ackermann, asegurando que la rueda interior mantenga un ángulo ligeramente superior a la rueda exterior durante un viraje. Esto reduce la fricción lateral del neumático delantero y proporciona un control de trayectoria suave.
* **Calibración y Protección Mecánica:** A través de rutinas de calibración específicas, fijamos el ángulo de centro mecánico en el software y definimos bordes de seguridad rígidos. Estos límites previenen que el servomotor intente girar más allá del tope físico de la suspensión, evitando sobrecalentamientos, consumo excesivo de batería o daños en los engranajes del servo.

---

### Esquema Electrónico y Distribución de Alimentación

El correcto diseño del sistema eléctrico es crucial para prevenir fallas aleatorias, caídas de voltaje o ruido electromagnético que pueda interferir con el procesamiento de la Raspberry Pi o la lectura de señales. Los esquemas electromecánicos completos se encuentran en la carpeta `schemes`.

#### Sistema de Procesamiento Jerárquico

Para optimizar el rendimiento y garantizar tiempos de respuesta en tiempo real, dividimos las tareas computacionales en dos niveles jerárquicos:

* **Procesador de Alto Nivel (Raspberry Pi 3 Wide):** Actúa como el "cerebro" del robot. Ejecuta el sistema operativo Linux, la pila de visión por computador en Python mediante la librería OpenCV, la lógica de navegación general, la detección de colores y obstáculos, y la toma de decisiones tácticas.
* **Controlador de Bajo Nivel (Microcontrolador Arduino):** Actúa como el "sistema nervioso" del robot. Se encarga exclusivamente de generar las señales físicas en tiempo real: los pulsos de alta frecuencia para el driver del motor paso a paso y la señal de modulación por ancho de pulsos (PWM) para el servomotor de la dirección.

Esta separación garantiza que las tareas críticas de tiempo como la generación de pasos del motor no sufran interrupciones ni fluctuaciones debido a la carga de procesamiento de la cámara en la Raspberry Pi.

#### Red de Alimentación y Aislamiento Electrónico

El sistema eléctrico de «Luna» se alimentó mediante un esquema de distribución cuidadosamente aislado:

* **Línea de Potencia (Motores y Servo):** Alimenta los actuadores mecánicos a través de un controlador dedicado (driver) para el motor paso a paso y una línea de regulador de voltaje de alta corriente para el servomotor. Esto aísla los picos de corriente que ocurren durante los arranques o detenciones bruscas del motor.
* **Línea de Lógica (Raspberry Pi y Sensores):** Cuenta con una regulación de voltaje filtrada que proporciona un suministro de energía limpio a la Raspberry Pi 3 Wide y al microcontrolador.
* **Masa Común y Filtrado:** Todas las líneas de masa del sistema se unieron en un punto común para establecer una referencia de voltaje idéntica en toda la electrónica. Se incorporaron condensadores de desacoplo de gran capacidad cerca de los controladores de motor para absorber los transitorios de inductancia.

---

### Sistema de Visión por Computador y Navegación Autónomica

El único sensor primario de percepción del entorno en «Luna» es la cámara Raspberry Pi 3 Wide colocada en la parte superior del chasis. Elegimos una lente de gran angular para maximizar el campo de visión, permitiendo que el robot observe simultáneamente el suelo inmediatamente delante de su paragolpes y las paredes o límites laterales del tapete.

#### Procesamiento de Imágenes en el Espacio de Color HSV

Las variaciones en la iluminación ambiental dentro del recinto de la competencia pueden alterar severamente la percepción del color si se trabaja en el espacio RGB convencional. Por ello, la primera etapa de nuestra canalización de visión convierte los fotogramas capturados por la cámara al espacio de color HSV (Hue, Saturation, Value):

1. **Canal Tono (Hue):** Representa el color puro de manera independiente de la intensidad luminosa. Esto permite definir rangos de umbración estables para aislar colores clave como el rojo, el verde, el azul y el negro de las líneas o paredes.
2. **Canales Saturación (Saturation) y Valor (Value):** Se utilizan para filtrar reflejos del suelo o zonas de sombra demasiado oscuras, asegurando que solo se procesen regiones con suficiente pureza de color.

#### Algoritmo de Detección de Paredes y Centrado de Carril

Para mantener a «Luna» en el centro del carril dentro del tapete de 3x3 metros, implementamos un algoritmo de análisis de contornos en la Región de Interés (ROI) de la imagen:

* **Definición de ROI:** Se descarta la parte superior de la imagen (que contiene elementos del entorno fuera del tapete) y se enfoca el procesamiento en la franja central e inferior del fotograma.
* **Segmentación de Límites:** Se aplican filtros morfológicos de erosión y dilatación para eliminar el ruido puntual. A continuación, se extraen los contornos de las paredes o líneas delimitadoras izquierda y derecha.
* **Cálculo del Punto Medio:** El software calcula el centroide espacial de los contornos detectados a ambos lados. La diferencia entre el centroide combinado de la pista y el centro geométrico del fotograma genera un vector de error. Este vector de error se convierte directamente en el ángulo de corrección para el servomotor de la dirección mediante una función de transferencia proporcional.

#### Detección y Evitación de Obstáculos

Además de seguir las paredes y líneas del circuito, «Luna» debe ser capaz de reaccionar ante obstáculos colocados en su trayectoria:

* **Evaluación de Área y Distancia:** Cuando el módulo de visión detecta una masa de color correspondiente a un objeto dentro de la ROI, calcula el área en píxeles del contorno. Si el área supera un umbral predefinido, el sistema determina que el objeto está a una distancia crítica de colisión.
* **Lógica de Esquiva por Código de Color:** Dependiendo del color del objeto identificado (por ejemplo, verde para esquivar por un costado o rojo para el lado opuesto), el algoritmo de decisión invalida temporalmente la referencia de centrado de paredes e introduce un desvío angular forzado en la dirección. Una vez que el contorno del objeto sale del campo de visión lateral de la cámara, el sistema retorna suavemente al modo de seguimiento de carril.

---

### Estructura del Software y Flujo de Control (`src`)

Todo el software desarrollado para controlar a «Luna» se encuentra documentado y estructurado modularmente dentro de la carpeta `src`. La arquitectura sigue patrones de diseño orientados a objetos en Python, asegurando un código limpio, reutilizable y fácil de depurar.

#### Arquitectura de Clases

* `run.py`: Script de entrada principal. Inicializa las clases de comunicación, la captura de video en un hilo dedicado, procesa el bucle principal de control y gestiona las paradas de emergencia.
* `classes/arduino_comms.py`: Encargada de gestionar la conexión serie (`/dev/ttyACM0` a 115200 baudios). Incluye funciones para empaquetar y enviar comandos de movimiento y leer las respuestas enviadas por el Arduino.
* `classes/image_algorithms.py`: Contiene los métodos matemáticos de visión por computador, la segmentación HSV, la detección de contornos, el cálculo de centroides y la generación de órdenes angulares.
* `battery.py`: Script de diagnóstico que evalúa la tensión del sistema antes de cada sesión de pruebas.

#### Protocolo de Comunicación Serie y Trama de Datos

La comunicación entre la Raspberry Pi y el Arduino se rige por un protocolo ligero basado en cadenas ASCII:

* **Comandos de Dirección y Velocidad:** Formateados como `m<ángulo>,<velocidad>.` (por ejemplo, `m85,1000.` indica fijar el servo en el centro de 85 grados y mover el motor paso a paso a 1000 pasos por segundo).
* **Comandos de Odometría Objetivo:** Formateados como `<pasos>!` (por ejemplo, `5000!` le indica al microcontrolador que debe avanzar exactamente 5000 pasos y detenerse).
* **Señales de Confirmación:** Cuando el microcontrolador completa una orden de pasos objetivo, transmite el carácter `'F'` por el puerto serie. La clase `ArduinoComms` intercepta este carácter para notificar al software principal que la maniobra ha concluido con éxito.

---

### Metodología de Calibración y Procedimiento Paso a Paso

Para garantizar que el vehículo funcione de forma idéntica en cada ejecución, establecimos un protocolo de calibración estructurado en 6 pasos que debe ejecutarse secuencialmente antes de cada competición o sesión de pruebas dinámicas.

```
+-----------------------------------------------------------------------+
|  Paso 1: Diagnóstico Electrónico y Nivel de Carga (battery.py)         |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|  Paso 2: Verificación de la Interfaz Serie (ArduinoComms)             |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|  Paso 3: Calibración de la Cámara y Umbralización HSV                 |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|  Paso 4: Calibración de Centro de Servo y Límites de Seguridad        |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|  Paso 5: Prueba de Avance / Parada Objetivo con Ruedas Elevadas       |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|  Paso 6: Pruebas Dinámicas en Pista y Ajuste de Bucle Cerrado         |
+-----------------------------------------------------------------------+

```

#### Paso 1: Diagnóstico Electrónico y Nivel de Carga

Antes de activar los motores, se ejecuta el script de diagnóstico de batería. Esto confirma que el voltaje de las líneas de lógica y potencia se encuentre dentro del rango nominal, evitando que caídas de tensión provoquen comportamientos anómalos en el motor paso a paso o en el procesamiento de la imagen.

#### Paso 2: Verificación de la Interfaz Serie

Se valida que el puerto USB serie entre la Raspberry Pi y el Arduino se abra correctamente a 115200 baudios, enviando tramas de prueba para medir la latencia del canal de comunicación y confirmar que no existan paquetes corruptos en el búfer.

#### Paso 3: Calibración de la Cámara y Umbralización HSV

Dado que la luz ambiente del recinto de la competición varía según la hora y la iluminación de la sala, colocamos al robot en diferentes puntos del tapete para ajustar los valores mínimos y máximos de los canales HSV. Guardamos estos parámetros en los archivos de configuración para garantizar una segmentación de color precisa.

#### Paso 4: Calibración de Centro de Servo y Límites de Seguridad

Se eleva el eje delantero para eliminar la fricción con el suelo. Mediante una consola interactiva, ajustamos el valor de `ANGLE_STRAIGHT` hasta que las ruedas delanteras queden perfectamente alineadas con el chasis (fijado nominalmente en 85 grados). Posteriormente, probamos los giros máximos a izquierda y derecha para establecer límites estrictos en el software que prevengan bloqueos mecánicos.

#### Paso 5: Prueba de Avance y Parada Objetivo con Ruedas Elevadas

Con el vehículo aún suspendido sobre un soporte, probamos el sistema de tracción posterior:

1. **Verificación de Dirección de Marcha:** Confirmamos que los comandos de velocidad positiva hagan girar ambas ruedas traseras en sentido de avance hacia adelante a través del diferencial.
2. **Respuesta a la Parada Objetivo:** Enviamos un comando de 5000 pasos y verificamos que el motor paso a paso se detenga automáticamente al alcanzar la cuenta exacta, transmitiendo la señal de confirmación `'F'` de regreso a la Raspberry Pi.

#### Paso 6: Pruebas Dinámicas en Pista y Ajuste de Bucle Cerrado

Finalmente, colocamos a «Luna» sobre el tapete de 3x3 metros. Ejecutamos el bucle de control completo en `run.py`, ajustando las ganancias de respuesta del algoritmo de dirección para lograr un seguimiento de carril fluido, sin sobreoscilaciones en las curvas y con una esquiva de obstáculos limpia y predecible.

---

### Organización de Repositorio y Documentación

Para garantizar que cualquier miembro de la comunidad de la WRO o jurado de la competencia pueda revisar, replicar o continuar nuestro trabajo, organizamos el repositorio oficial del Equipo Kuntur respetando una estructura estricta de carpetas. Cada directorio cuenta con su respectivo archivo `README.md` explicativo:

* **`t-photos/`**: Contiene la documentación fotográfica del equipo Kuntur. Incluye una foto oficial para la presentación de la competencia y una foto informal que refleja el espíritu colaborativo del grupo.
* **`v-photos/`**: Agrupa 6 fotografías detalladas de «Luna» desde todos los ángulos clave: vista superior (mostrando la disposición de la Raspberry Pi y el cableado), vista inferior (revelando el tren de engranajes del diferencial y el soporte del motor paso a paso), así como vistas frontal, posterior y laterales.
* **`video/`**: Contiene el archivo `video.md`, el cual proporciona el enlace directo al video demostrativo alojado en línea, donde se aprecia a «Luna» ejecutando una prueba completa de conducción autónoma en el tapete de 3x3 metros.
* **`schemes/`**: Alberga los esquemas mecánicos y electrónicos en formato JPEG, detallando la interconexión entre la Raspberry Pi, el Arduino, el driver del stepper motor, el servomotor y la red de alimentación.
* **`src/`**: Guarda la totalidad del código fuente ejecutable, incluyendo las clases de comunicación, los algoritmos de visión, los scripts de prueba individuales y el ejecutable principal `run.py`.
* **`models/`**: Contiene los archivos CAD en formato STL y código G para la impresión 3D de los componentes del chasis y soportes de sensores.
* **`other/`**: Reúne documentación complementaria, como hojas de datos técnicas de los componentes utilizados, bitácoras de pruebas de campo y archivos de configuración auxiliares.

---

### Resultados, Conclusiones y Agradecimientos

El desarrollo de «Luna» ha sido una experiencia de aprendizaje técnico inestimable para todo el Equipo Kuntur. A través de este proyecto logramos validar de manera práctica conceptos avanzados de mecatrónica, ingeniería de software, visión por computador y control en tiempo real.

El uso de un motor paso a paso acoplado a un diferencial mecánico demostró ser una alternativa innovadora y altamente eficiente para la tracción trasera de vehículos autónomos a pequeña escala, ofreciendo una odometría exacta sin incrementar la complejidad de sensores en el chasis. Del mismo modo, la arquitectura de procesamiento dual entre la Raspberry Pi 3 Wide y el Arduino garantizó un equilibrio perfecto entre capacidad de cómputo visual y precisión en la generación de señales de control.

Agradecemos sinceramente al Campeonato Nacional de la WRO 2026 en Lima, Perú, por brindar la oportunidad de poner a prueba nuestras capacidades de ingeniería, así como a nuestros mentores y familias por su apoyo constante durante las largas jornadas de diseño, impresión 3D y programación. Invitamos a todos los visitantes de nuestro sitio web a explorar las diferentes carpetas de nuestro repositorio para conocer a fondo los detalles técnicos que hacen de «Luna» un vehículo autónomo único.
