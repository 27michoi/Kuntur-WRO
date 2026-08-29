### **Introducción y Visión General del Proyecto de Robótica**

El desarrollo y la puesta en marcha de un vehículo autónomo de alta precisión para competencias de robótica exige una metodología rigurosa, modular y progresiva. En este contexto, la interacción entre el firmware del microcontrolador y los algoritmos de alto nivel alojados en el ordenador de a bordo resulta crítica. Para garantizar que la plataforma móvil pueda resolver desafíos complejos —tales como la navegación autónoma entre paredes, la evitación dinámica de obstáculos de distintos colores y las maniobras de estacionamiento paralelo en zonas delimitadas— es imperativo establecer un proceso de pruebas secuencial que aísle y valide cada subsistema de hardware y software de forma independiente antes de proceder a la integración total del vehículo.

Los pasos de calibración y prueba inicial representan el cimiento sobre el cual se construyen los algoritmos de control en bucle cerrado. Antes de permitir que el robot realice desplazamientos autónomos sobre la pista, se deben caracterizar las respuestas mecánicas y eléctricas de sus actuadores principales: el sistema de dirección accionado por un servomotor de precisión y el sistema de tracción impulsado por motores con retroalimentación por codificadores de cuadratura. La omisión o ejecución deficiente de estas fases preliminares suele derivar en comportamientos erráticos, tales como oscilaciones violentas en la trayectoria, consumo excesivo de corriente, sobrecalentamiento de los controladores de potencia y eventuales colisiones físicas contra la infraestructura del entorno.

El propósito fundamental de esta metodología detallada es articular un protocolo de pruebas exhaustivo para los subsistemas de dirección y tracción. A lo largo de esta especificación se abordan minuciosamente la preparación del hardware, la arquitectura de la comunicación serie, los procedimientos interactivos de calibración, la validación de límites de seguridad, el diagnóstico de fallas y la integración de parámetros ajustados dentro del sistema general de archivos del proyecto. La meta final es transformar las señales digitales y los comandos serie en respuestas mecánicas predecibles, repetibles y completamente seguras.

---

### **Fase de Calibración de la Dirección: Servomotor y Límites Mecánicos de Seguridad**

#### **Fundamentos Teóricos y Necesidad Mecánica**

El sistema de dirección de un vehículo autónomo tipo tracción trasera con dirección delantera requiere una relación lineal y simétrica entre el comando de ángulo solicitado por el algoritmo de visión por computador y la orientación física real de las ruedas directrices. En los servomotores de modelismo o de grado industrial, la señal de control consiste en un pulso de modulación por ancho de pulsos donde la duración del nivel alto determina la posición angular del eje de salida. Sin embargo, debido a las tolerancias de fabricación en el acoplamiento mecánico, las variaciones en el montaje del brazo del servo y las imperfecciones en el varillaje de la dirección, la posición angular neutra del servo casi nunca coincide de forma exacta con la alineación geométrica neutra del chasis del robot.

Además, los mecanismos de dirección poseen restricciones físicas insalvables impuestas por el diseño del chasis, la geometría del sistema de alineación y la presencia de topes mecánicos en los manguetones de las ruedas. Si el software de control envía una orden de giro que excede estos límites físicos, el servomotor intentará alcanzar una posición inalcanzable. Esta condición, conocida como bloqueo mecánico o atascamiento del servo, provoca un disparo inmediato en el consumo de corriente eléctrica, genera un esfuerzo torsional desmedido sobre los engranajes internos del servomotor, introduce ruido térmico en las líneas de alimentación y puede causar caídas de tensión en el microcontrolador principal, resultando en reinicios no deseados del sistema durante la competencia.

Por lo tanto, la calibración de la dirección persigue dos objetivos centrales: identificar con precisión absoluta el valor numérico correspondiente al centro mecánico perfecto y definir un rango operacional seguro que limite las excursiones angulares máximas tanto a la izquierda como a la derecha.

#### **Inspección Física y Preparación del Hardware**

Antes de aplicar energía a los actuadores o ejecutar cualquier rutina de prueba por puerto serie, se debe acondicionar el entorno físico del vehículo para prevenir daños mecánicos y garantizar mediciones precisas:

* **Elevación del Chasis:** Se debe colocar el robot sobre un soporte de pruebas estable, de modo que ni las ruedas delanteras directrices ni las ruedas traseras motrices entren en contacto con la superficie de trabajo. Esta elevación elimina la fricción estática del neumático contra el suelo, permitiendo que el servomotor se mueva sin oponer resistencia y facilitando la detección auditiva o visual de cualquier rozamiento mecánico interno.
* **Inspección del Varillaje:** Se debe verificar manualmente que las bieletas de dirección, los rótulos de articulación y los manguetones no presenten holguras excesivas ni un apretado sobremedido que genere fricción parásita. El mecanismo debe pivotar suavemente en todo su rango manual de movimiento.
* **Conexión de Señal:** Se debe confirmar la integridad del cableado de interfaz del servomotor, asegurando que la línea de señal esté conectada al pin de modulación por ancho de pulsos asignado en la placa del microcontrolador, y que las líneas de masa y alimentación dedicada de alta corriente compartan un punto de referencia común pero aislado de la lógica sensible de procesamiento.
* **Verificación de Alimentación Electrónica:** Mediante el uso de las utilidades de diagnóstico del sistema, se debe supervisar el estado de carga de la batería del sistema. Un nivel de voltaje deficiente en la línea de los actuadores alterará el par disponible del servomotor y puede distorsionar las lecturas de posición neutral debido a caídas de tensión durante el movimiento rápido.

#### **Protocolo Extendido de Calibración Interactiva**

El procedimiento de calibración requiere una herramienta de interfaz por consola que permita al operador enviar valores angulares directos en tiempo real al microcontrolador mientras observa el comportamiento físico de las ruedas directrices.

##### **Definición y Verificación de Constantes Base**

El código fuente del vehículo utiliza variables globales y constantes de configuración que definen el comportamiento de la dirección a lo largo de las distintas fases de la competencia. Es necesario inspeccionar los archivos principales de ejecución para identificar los valores predeterminados y comprender cómo los módulos de visión e inteligencia artificial calculan las desviaciones angulares.

El sistema funciona típicamente con un ángulo central de referencia a partir del cual se aplican desviaciones positivas o negativas. Por ejemplo, en el software de la competencia se parte de un centro nominal estandarizado y se establecen amplitudes de giro máximas para maniobras evasivas o giros en curvas cerradas. Durante esta fase de prueba, se debe validar si los valores nominales teóricos coinciden con la realidad del chasis ensamblado.

##### **Procedimiento de Determinación del Centro Mecánico**

1. Con el robot elevado y la comunicación serie establecida entre el ordenador central y el microcontrolador, se envía el comando correspondiente al ángulo neutro predeterminado.
2. Se realiza una alineación visual utilizando una regla de precisión o una herramienta de alineación láser paralela a la estructura longitudinal del chasis.
3. Se evalúa la convergencia o divergencia de las ruedas delanteras. Si la rueda muestra un ángulo de desalineación hacia la izquierda o hacia la derecha, se incrementa o decrementa de forma unitaria el valor numérico enviado al servomotor.
4. Se repite la entrada de comandos angulares en pequeños pasos discretos hasta que el plano medio de ambas ruedas delanteras sea perfectamente paralelo a la línea central de simetría del chasis del vehículo.
5. Una vez encontrado este punto exacto, se registra el valor numérico como el nuevo ángulo de centro mecánico. Este valor reemplazará el valor predeterminado en todos los archivos de configuración del proyecto.

##### **Procedimiento de Identificación de Límites Operacionales Seguros**

1. **Prueba de Extremo Izquierdo:** Partiendo del ángulo de centro mecánico recién calibrado, se comienza a incrementar de manera progresiva el ángulo transmitido al servomotor en pasos de dos en dos unidades. En cada paso, el operador debe girar suavemente el mecanismo de dirección con la mano para sentir si existe holgura o si el servomotor ha llegado al tope físico de la suspensión. Si se percibe un zumbido agudo proveniente del motor del servo o si la corriente consumida se eleva drásticamente, se ha superado el límite seguro. Se retrocede inmediatamente el valor en dos o tres unidades y se registra esa cifra como el límite máximo absoluto a la izquierda.
2. **Prueba de Extremo Derecho:** Regresando primero al centro calibrado, se procede a reducir paulatinamente el valor del ángulo enviado al servomotor. Se aplica el mismo criterio de detección: observación del esfuerzo mecánico, escucha de vibraciones por bloqueo y verificación de contacto físico con el chasis. Una vez detectado el punto donde el mecanismo comienza a hacer tope, se incrementa el valor en dos o tres unidades para dejar un margen de tolerancia estructural. Este valor se registra como el límite máximo absoluto a la derecha.
3. **Comprobación de Simetría y Rango Dinámico:** Se calcula la diferencia entre el centro mecánico y los límites máximos izquierdo y derecho. En un chasis ideal, el rango de deflexión hacia ambos lados debe ser simétrico. Si existe una asimetría pronunciada, se debe verificar si el brazo del servo está montado con un diente de desfase en su estriado mecánico y corregir el montaje antes de fijar las constantes en el código.

#### **Criterios de Aceptación, Validación y Almacenamiento**

Para considerar concluida con éxito la fase de calibración de la dirección, el sistema debe cumplir estrictamente con los siguientes requisitos:

* **Movimiento Continuo y Fluido:** Al realizar un barrido completo de extremo a extremo a través de comandos de prueba, el mecanismo de dirección debe desplazarse suavemente sin saltos, enganches mecánicos ni caídas repentinas de velocidad angular.
* **Ausencia de Esfuerzo Estático:** Cuando las ruedas están en cualquier posición dentro del rango delimitado (incluyendo los extremos), el servomotor no debe emitir zumbidos térmicos ni generar un calentamiento apreciable en su carcasa.
* **Repetibilidad del Punto Cero:** Tras efectuar múltiples giros bruscos alternados hacia la izquierda y hacia la derecha, el envío del comando del ángulo de centro calibrado debe retornar las ruedas exactamente a la posición de alineación paralela, sin desviaciones causadas por holguras en el varillaje.
* **Actualización del Repositorio de Código:** Los valores definitivos obtenidos durante las pruebas de campo deben ser transcritos en los módulos de configuración correspondientes. Se deben actualizar las constantes del ángulo central en los scripts principales de ejecución y garantizar que las funciones encargadas del cálculo de dirección en los algoritmos de navegación por pared y evitación de obstáculos utilicen estas constantes calibradas para acotar y recortar cualquier comando de salida dentro de los bordes seguros identificados.

---

### **Fase de Prueba de Tracción: Avance Lento y Parada Precisa con Ruedas Elevadas**

#### **Fundamentos Teóricos del Control de Tracción y Odometría**

El sistema de propulsión de un vehículo autónomo de competencia no solo debe garantizar el desplazamiento longitudinal a distintas velocidades, sino que también debe ofrecer un control riguroso sobre la distancia recorrida. El control de la tracción se gestiona mediante señales enviadas desde el procesador principal hacia el microcontrolador, el cual convierte las órdenes de velocidad y distancia en modulación de ancho de pulsos para los controladores de potencia de los motores de corriente continua.

Para medir el desplazamiento real del vehículo, el sistema utiliza codificadores ópticos o magnéticos adjuntos al eje de transmisión de los motores. Estos sensores generan pulsos digitales periódicos a medida que la rueda gira. Al contar la cantidad de pulsos recibidos, el microcontrolador calcula los pasos de odometría acumulados. La precisión en la ejecución de las órdenes de parada por distancia depende de la velocidad de respuesta de las interrupciones del microcontrolador y de la solidez del bucle de control interno del firmware.

La prueba de tracción con ruedas elevadas representa una etapa de verificación intermedia indispensable. Su objetivo principal es asegurar que el protocolo de comunicación serie procese correctamente las tramas de comandos de velocidad y distancia, que los motores giren en el sentido correcto en función de la polaridad asignada, y que el mecanismo de interrupción por distancia recorrida responda adecuadamente antes de someter al vehículo al impacto de la inercia real sobre la pista.

#### **Configuración del Entorno de Prueba y Seguridad**

Para llevar a cabo las pruebas de tracción en modo suspendido, se deben tomar precauciones específicas orientadas a proteger los componentes electrónicos y prevenir accidentes:

* **Fijación del Vehículo:** El chasis debe estar firme sobre el bloque de soporte, garantizando que la vibración producida por la rotación de los motores traseros no desplace el robot ni provoque su caída accidental sobre la mesa de trabajo.
* **Alineación Previa de la Dirección:** Antes de alimentar el circuito de potencia de los motores, el servomotor de dirección debe fijarse en su posición de centro calibrado previamente. Esto evita que las fluctuaciones de corriente causadas por el arranque de los motores alteren la posición de las ruedas delanteras.
* **Verificación de la Interfaz Serie:** La conexión por cable entre el procesador principal y el microcontrolador debe estar activa y configurada a la velocidad de transmisión especificada por el protocolo del proyecto. Se debe comprobar que el flujo de datos sea bidireccional, permitiendo enviar comandos desde el ordenador y recibir señales de estado desde el microcontrolador.
* **Chequeo de Baterías de Tracción:** Los motores de tracción demandan picos elevados de corriente durante la fase de aceleración. Es fundamental asegurar que la batería dedicada a la etapa de potencia cuente con la carga suficiente para evitar caídas de voltaje que puedan distorsionar la lógica del sistema.

#### **Protocolo Extendido de Pruebas de Tracción**

La validación de la tracción se divide en dos fases secuenciales: la prueba de rotación continua a baja velocidad y la prueba de parada por cumplimiento de pasos objetivo de odometría.

##### **Estructura del Protocolo de Comunicación**

La comunicación entre el sistema operativo principal y el microcontrolador se basa en el intercambio de caracteres específicos formateados mediante tramas serie compuestas por delimitadores de inicio y fin:

1. **Comando de Configuración de Pasos Objetivo:** El ordenador central transmite una trama que especifica la cantidad total de pasos de odometría que el robot debe recorrer antes de detenerse automáticamente. Para pruebas de movimiento continuo, se envía un valor numérico extremadamente alto que simula un límite infinito. Para pruebas de distancia finita, se envía el número exacto de pasos deseado.
2. **Comando de Control de Movimiento:** Se transmite una trama que condensa el ángulo de dirección requerido y la velocidad angular o lineal deseada para los motores de tracción. El microcontrolador interpreta este paquete, ajusta la dirección de los servomotores y aplica el nivel correspondiente de potencia a las etapas de salida de los motores.
3. **Respuesta de Finalización de Tarea:** Cuando el microcontrolador detecta que el contador de pasos de los codificadores ha alcanzado o superado el valor objetivo preestablecido, corta inmediatamente la alimentación de los motores y transmite un carácter de confirmación por el puerto serie para notificar al procesador principal que la maniobra ha concluido.

##### **Fase 1: Prueba de Movimiento Continuo a Baja Velocidad**

1. Se inicializan los módulos de comunicación serie en el software de pruebas.
2. Se transmite un comando para establecer un límite de pasos de odometría arbitrariamente alto, asegurando que el microcontrolador no interrumpa el movimiento por alcance de distancia durante esta fase.
3. Se envía el comando de movimiento configurando el ángulo de dirección en el centro calibrado y seleccionando una velocidad de avance baja y segura.
4. Se observa el comportamiento de las ruedas motrices traseras durante un intervalo determinado de tiempo.
5. **Verificaciones de la Fase 1:**
* Se confirma visualmente que ambas ruedas traseras giren en el sentido correspondiente al movimiento hacia adelante. Si las ruedas giran en sentido inverso, se identifica una inversión de polaridad en el cableado de los motores o un error de signo en la lógica del controlador de potencia.
* Se comprueba que no existan ruidos de fricción anómalos en los engranajes de la caja reductora ni vibraciones desmedidas en los ejes de transmisión.
* Se envía el comando de parada especificando una velocidad nula y se verifica que los motores respondan interrumpiendo el giro de forma inmediata.



##### **Fase 2: Prueba de Parada Automática por Distancia Objetivo**

1. Se establece la comunicación y se envía un comando de configuración de pasos objetivo correspondiente a una distancia corta predeterminada.
2. Se transmite la orden de movimiento a baja velocidad con la dirección centrada.
3. El ordenador central entra en un bucle de lectura no bloqueante en el puerto serie, a la espera de recibir el carácter de confirmación devuelto por el microcontrolador.
4. Se monitorea la rotación de las ruedas motrices. En el instante exacto en que los codificadores acumulan la cantidad de pasos programada, el firmware del microcontrolador debe desactivar las salidas de potencia y transmitir la señal de finalización.
5. **Verificaciones de la Fase 2:**
* Se confirma que las ruedas se detengan automáticamente sin requerir un comando explícito de parada enviado desde el ordenador central.
* Se verifica que la señal de confirmación de finalización sea recibida correctamente por el script de prueba dentro de un intervalo de tiempo razonable, registrando el evento en la consola del sistema.
* Si la prueba no concluye y los motores continúan girando de forma indefinida, se diagnostica una falla en la lectura de los pines de los codificadores, una pérdida de paquetes en la transmisión serie o un error de desbordamiento en las variables internas del contador de pasos.



#### **Criterios de Aceptación, Diagnóstico de Fallas y Corrección**

La prueba de tracción con ruedas elevadas se dará por aprobada únicamente cuando el sistema responda de manera consistente bajo los siguientes estándares:

* **Direccionalidad Correcta:** La rotación de las ruedas debe coincidir de manera precisa con la polaridad del valor de velocidad comandado. Velocidades positivas deben generar un avance hacia adelante y velocidades negativas deben generar una rotación en reversa.
* **Sincronismo de Respuesta:** El tiempo transcurrido entre la emisión del comando serie y el inicio físico del giro de las ruedas debe ser imperceptible para el operador, descartando retrasos por almacenamiento en búfer de la interfaz de comunicación.
* **Precisión de la Parada por Odometría:** El corte de energía de los motores debe ejecutarse exactamente al alcanzar el número de pasos prefijado. El carácter de notificación de finalización debe llegar al procesador principal sin pérdidas de tramas.
* **Resolución de Problemas Frecuentes:**
* **Rotación Invertida:** Si los motores giran en sentido contrario al esperado, se debe corregir la asignación de pines en la configuración del firmware del microcontrolador o invertir físicamente las conexiones de los terminales del motor en la etapa de potencia.
* **Falta de Recepción de la Señal de Parada:** Si las ruedas continúan girando y el ordenador nunca recibe la notificación de finalización, se debe verificar el cableado de los canales A y B de los codificadores magnéticos, probar la continuidad de las líneas de datos, confirmar la activación de las interrupciones por hardware en el microcontrolador y validar que la velocidad de baudios configurada en el puerto serie sea idéntica en ambos extremos de la arquitectura.



---

### **Integración de los Pasos de Calibración en la Arquitectura Global del Software**

#### **Estructura Modular del Código del Proyecto**

El software del vehículo está diseñado bajo una arquitectura modular desacoplada que separa las tareas de adquisición de imágenes, procesamiento algorítmico, toma de decisiones de alto nivel y comunicación con el hardware. Esta división en capas asegura que las modificaciones en los parámetros mecánicos o en los sensores de bajo nivel no afecten la lógica fundamental de los algoritmos de navegación autónoma.

A continuación se detalla cómo interactúan los diferentes componentes de la arquitectura de software durante la ejecución de los algoritmos de control:

##### **Módulo de Comunicación Hardware**

Este componente abstrae las complejidades del puerto serie. Se encarga de abrir la conexión con el microcontrolador, formatear los paquetes de datos de entrada y salida, gestionar los tiempos de espera de lectura y ofrecer funciones simplificadas para enviar comandos de dirección, velocidad y límites de distancia a través de la interfaz serie. Es el encargado directo de transmitir los parámetros calibrados hacia los actuadores.

##### **Módulo de Procesamiento de Imágenes y Visión**

Esta capa procesa los fotogramas capturados por la cámara de a bordo. Realiza las conversiones de espacio de color, aplica transformaciones de perspectiva y ejecuta los algoritmos de detección de bordes, líneas de carril, paredes laterales y obstáculos de color. Su función es calcular las coordenadas espaciales del entorno y determinar las desviaciones angulares requeridas para mantener al robot dentro de la trayectoria deseada.

##### **Módulo de Algoritmos de Navegación**

Este bloque toma las métricas generadas por el módulo de visión y las transforma en decisiones de control. Contiene la lógica para calcular el ángulo de dirección adecuado en función de la distancia a las paredes laterales, la presencia de obstáculos de color verde o rojo y el estado actual de la pista. Es en este módulo donde se aplican las funciones de limitación angular que recortan cualquier orden de dirección dentro de los bordes seguros identificados durante la calibración del servomotor.

##### **Módulo de Gestión de Estado y Seguimiento de Carrera**

Este gestor central mantiene el registro del estado actual del vehículo dentro del flujo de la competencia. Supervisa el conteo de vueltas, detecta las líneas de cruce mediante la identificación de colores específicos, gestiona las transiciones entre la navegación en rectas, el abordaje de curvas y la ejecución de las maniobras finales de estacionamiento, y coordina los cambios de velocidad requeridos para cada fase de la prueba.

#### **Flujo de Ejecución e Interacción de Módulos durante la Navegación Autónomica**

Para comprender la importancia de una calibración precisa de la dirección y la tracción, es necesario analizar la secuencia de operaciones que realiza el software durante cada ciclo del bucle principal de control autónomo:

1. **Captura y Transformación de Imagen:** El módulo de cámara obtiene un nuevo fotograma, aplica la corrección de perspectiva y genera las imágenes binarias e hipercubos de color para analizar las paredes e identificar las líneas demarcadoras del circuito.
2. **Análisis de Paredes y Cálculo Angular:** El algoritmo de análisis de contornos localiza la posición de las paredes izquierda y derecha. Calcula el error de centrado del robot respecto al eje medio de la pista y genera un ángulo de dirección teórico para corregir la trayectoria.
3. **Detección y Tratamiento de Obstáculos:** Si el módulo de visión detecta un obstáculo en la trayectoria, calcula la posición angular relativa del objeto y determina si el robot debe eludirlo por la izquierda o por la derecha según el color identificado. Se genera un ángulo de dirección alternativo enfocado en la esquiva.
4. **Arbitraje y Filtrado Angular:** El módulo de algoritmos evalúa las propuestas angulares de la navegación entre paredes y de la evitación de obstáculos, seleccionando la salida óptima. Inmediatamente, la función de filtrado somete este valor angular a las restricciones de seguridad: comprueba que el ángulo no sea inferior al límite máximo derecho ni superior al límite máximo izquierdo, y aplica el valor de centro calibrado como punto de referencia cero.
5. **Generación del Comando Serie y Transmisión:** El ángulo filtrado y la velocidad correspondiente al estado actual de la carrera se entregan al módulo de comunicación serie. Este empaqueta la orden en el formato correspondiente y la transmite al microcontrolador.
6. **Ejecución en Microcontrolador y Retroalimentación:** El microcontrolador ajusta la señal de modulación de ancho de pulsos del servomotor para posicionar las ruedas delanteras en el ángulo exacto comandado y ajusta la potencia de los motores de tracción. Si el vehículo se encuentra ejecutando una maniobra por distancia prefijada, el microcontrolador monitorea los codificadores y, al completar los pasos esperados, interrumpe el movimiento y transmite la señal de finalización hacia el ordenador central.

#### **Importancia de la Calibración en las Maniobras Complejas**

La precisión alcanzada en las etapas de prueba descritas impacta de manera directa en el éxito de las maniobras críticas de la competencia, tales como el recorrido en curvas cerradas y el estacionamiento paralelo autónomo:

* **Navegación Estable en Rectas:** Si el ángulo de centro mecánico está mal calibrado, el vehículo tenderá a desviarse constantemente hacia un lado incluso cuando el algoritmo indique una trayectoria recta. Esto obliga al bucle de control visual a corregir continuamente la dirección, generando un efecto de oscilación serpentina que reduce la velocidad media y aumenta el riesgo de colisión contra las paredes laterales.
* **Prevención de Bloqueos en Curvas:** En las esquinas de la pista, los algoritmos de navegación suelen exigir ángulos de giro pronunciados. Si el software solicita un ángulo que sobrepasa el límite seguro del servo y el filtro de seguridad no está correctamente parametrizado, el servo se bloqueará contra la suspensión, provocando caídas de tensión que pueden reiniciar el procesador de visión en medio del viraje.
* **Precisión en Maniobras de Estacionamiento:** Durante la fase final de estacionamiento paralelo, el robot ejecuta una secuencia ciega o semi-ciega basada en movimientos hacia adelante y marcha atrás combinando giros de dirección predeterminados y distancias prefijadas por odometría. Si los comandos de pasos de odometría no han sido validados previamente en las pruebas de tracción, el robot se detendrá antes de ingresar al cajón de estacionamiento o colisionará contra la pared trasera por exceso de desplazamiento.

---

### **Matriz de Diagnóstico y Plan de Contingencia Técnico**

Durante la puesta a punto y ejecución de las fases de calibración y prueba, pueden presentarse anomalías operativas de origen mecánico, eléctrico o de software. La siguiente guía de resolución de problemas establece los procedimientos sistematizados para identificar y corregir las fallas más recurrentes.

#### **Anomalías en el Sistema de Dirección**

##### **El servomotor no responde a los comandos enviados desde la consola**

* **Causas Posibles:** Ausencia de alimentación en la línea de potencia del servo, desconexión del cable de señal, puerto serie incorrecto seleccionado en el script de prueba o desacoplamiento de masa entre la lógica y la potencia.
* **Procedimiento de Diagnóstico:**
1. Utilizar un multímetro para medir la tensión en los pines de alimentación del servomotor, verificando que el voltaje se encuentre dentro del rango operacional especificado por el fabricante.
2. Confirmar que la masa de la fuente de alimentación del servo esté unida eléctricamente a la masa del microcontrolador.
3. Comprobar la emisión de impulsos en la línea de señal mediante un osciloscopio o un analizador lógico.
4. Verificar en el sistema operativo que el identificador del dispositivo serie coincida con la ruta declarada en el código de comunicación.



##### **El servomotor vibra o genera un zumbido agudo en las posiciones extremas**

* **Causas Posibles:** El ángulo comandado excede el límite mecánico físico del varillaje de dirección, provocando un bloqueo mecánico.
* **Procedimiento de Diagnóstico:**
1. Reducir inmediatamente el ángulo enviado desde la consola hasta que el zumbido desaparezca por completo.
2. Ajustar las constantes de límite seguro en el archivo de configuración, reduciendo la excursión angular permisible hacia el lado afectado.
3. Inspeccionar el mecanismo físico para asegurar que no existan cables, tornillos o elementos del chasis interfiriendo con el recorrido del brazo del servo.



##### **Las ruedas directrices no retornan a la misma posición neutra tras giros sucesivos**

* **Causas Posibles:** Holgura excesiva en las rótulas del varillaje de dirección, prisionero del brazo del servo flojo en el estriado del eje o deformación en los soportes plásticos del chasis.
* **Procedimiento de Diagnóstico:**
1. Aplicar una fuerza manual suave sobre las ruedas con el servo alimentado en posición central y verificar si existe juego mecánico sin resistencia del motor.
2. Apretar el tornillo de fijación central del brazo del servo.
3. Reemplazar los cabezales de las bieletas de dirección si presentan desgaste en sus alojamientos esféricos.



#### **Anomalías en el Sistema de Tracción**

##### **Los motores de tracción no giran al enviar el comando de movimiento**

* **Causas Posibles:** Batería de potencia descargada o desconectada, interruptor general de motores abierto, señal de habilitación del controlador de potencia inactiva o falta de envío del comando de límite de pasos inicial.
* **Procedimiento de Diagnóstico:**
1. Medir el voltaje de la batería de tracción bajo carga utilizando la utilidad de verificación de batería.
2. Comprobar el estado de los fusibles de protección de la etapa de potencia de los motores.
3. Asegurar que el firmware del microcontrolador haya recibido el comando de definición de pasos de odometría antes de procesar el comando de movimiento, ya que si el límite de pasos remanente es cero, el motor no se activará.



##### **Los motores giran pero no se detienen al alcanzar la cantidad de pasos objetivo**

* **Causas Posibles:** Desconexión o falla en las líneas de datos de los codificadores de cuadratura, canales A y B invertidos, interrupciones de hardware desactivadas en el microcontrolador o desbordamiento de las variables de conteo.
* **Procedimiento de Diagnóstico:**
1. Girar manualmente la rueda motriz y monitorear con un osciloscopio o led de prueba si se generan pulsos limpios de onda cuadrada en los canales de salida del codificador.
2. Verificar que los pines del microcontrolador asignados a los codificadores coincidan con las líneas de interrupción por cambio de estado configuradas en el firmware.
3. Comprobar la lógica del bucle de lectura en el ordenador central para garantizar que no esté descartando la señal de confirmación de finalización debido a un tiempo de espera demasiado corto.



##### **El microcontrolador se reinicia de manera fortuita al acelerar los motores**

* **Causas Posibles:** Caída de tensión brusca en la línea de lógica provocada por la demanda de corriente de arranque de los motores (efecto de bajón de voltaje), ausencia de condensadores de desacoplo o falla en el regulador de voltaje.
* **Procedimiento de Diagnóstico:**
1. Separar completamente las fuentes de alimentación de la etapa lógica y de la etapa de potencia de los motores.
2. Añadir condensadores electrolíticos de alta capacidad en los bornes de entrada del controlador de motores para absorber los picos de corriente transitorios.
3. Verificar que el cable USB de datos posea un filtro de ferrita para mitigar la interferencia electromagnética inducida por las conmutaciones del motor de corriente continua.



---

### **Listado de Comprobación Final y Protocolo de Firma de Fases**

Antes de declarar concluidas las etapas de calibración y prueba de laboratorio para autorizar el despliegue del vehículo en pistas de movimiento real sobre el suelo, el equipo de ingeniería debe completar y certificar la siguiente lista de verificación:

#### **Verificación Mecánica y Eléctrica**

* El chasis del robot ha sido sometido a inspección visual sin detectar elementos sueltos, fisuras en la estructura ni interferencias en la suspensión.
* Las baterías del sistema lógico y de los sistemas de potencia se encuentran completamente cargadas y verificadas mediante el instrumental correspondiente.
* Las líneas de alimentación de alta corriente y las líneas de señal de baja tensión se encuentran aisladas y adecuadamente canalizadas para evitar acoplamientos inductivos.

#### **Verificación de la Dirección**

* Se ha determinado con precisión el ángulo de centro mecánico y se ha comprobado la alineación perfectamente paralela de las ruedas delanteras respecto al eje longitudinal del chasis.
* Se han identificado y probado operativamente los ángulos límites de seguridad para giros a la izquierda y a la derecha.
* Se ha verificado que el servomotor no sufra bloqueos mecánicos, vibraciones ni sobrecalentamiento en ningún punto del rango de movimiento habilitado.
* Los parámetros de centro y límites seguros han sido guardados en el archivo de configuración del proyecto y validados dentro de las funciones de filtrado angular del módulo de algoritmos.

#### **Verificación de la Tracción y Odometría**

* Se ha verificado que la rotación de las ruedas motrices coincida con el sentido de marcha comandado tanto en avance como en retroceso.
* Se ha confirmado la correcta recepción y procesamiento de los comandos de velocidad y configuración de distancia objetivo en el firmware del microcontrolador.
* Se ha validado que el sistema corte la alimentación de los motores de forma autónoma al alcanzar la cantidad de pasos de odometría prefijada y que la señal de confirmación sea recibida y registrada por el procesador central.
* Se ha comprobado la estabilidad del sistema electrónico frente a variaciones de carga sin evidenciar reinicios no deseados en la lógica de control.

Una vez validados la totalidad de los puntos de esta lista de comprobación, el vehículo autónomo se encuentra oficialmente certificado para avanzar a las etapas posteriores de pruebas de movimiento sobre pista, navegación entre paredes a baja velocidad y ajuste de los bucles de control visual en tiempo real.
