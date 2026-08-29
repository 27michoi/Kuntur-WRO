Este paso verifica la dirección de tracción de los motores, el control de velocidad por comunicación serie y la función de parada precisa por distancia sin fricción en el suelo, antes de realizar pruebas de movimiento sobre la superficie.

### **Preparación y Configuración**

* **Elevación Física:** Mantenga el chasis del robot elevado de manera segura para que las ruedas motrices traseras giren libremente sin tocar ninguna superficie.
* **Ajuste del Servo:** Posicione el servomotor de dirección en el centro mecánico calibrado para mantener las ruedas delanteras alineadas.
* **Conexión Serie:** Conecte el equipo al microcontrolador a través del puerto serie USB con la velocidad de transmisión adecuada.
* **Verificación de Energía:** Verifique que la fuente de alimentación de alta corriente para los motores esté activa y compruebe el estado de las baterías de la lógica y los motores.

---

### **Flujo de Trabajo y Procedimiento de Prueba**

* **Estructura de Comandos:** Configure el sistema para enviar instrucciones de cantidad de pasos objetivo, comandos de movimiento especificando ángulo y velocidad, y la señal de confirmación de parada.
* **Fase de Giro Continuo:** Active el movimiento de avance a baja velocidad durante un periodo breve para observar la rotación de las ruedas traseras y confirmar que la dirección coincide con los valores positivos.
* **Fase de Parada por Distancia:** Inicie un recorrido especificando un número de pasos objetivo y verifique que las ruedas se detengan automáticamente al alcanzarlos, emitiendo la señal de finalización correspondiente.

---

### **Criterios de Finalización y Resolución de Problemas**

* **Validación:** Las ruedas traseras deben girar de forma fluida hacia adelante, detenerse de inmediato al recibir el comando de velocidad cero y detenerse automáticamente al alcanzar el límite de pasos establecido.
* **Manejo de Fallas:** Si las ruedas giran en sentido contrario, invierta la polaridad del cableado del motor o la lógica de control. Si no se recibe la señal de confirmación de parada, inspeccione las conexiones de los codificadores y la configuración del puerto serie.
