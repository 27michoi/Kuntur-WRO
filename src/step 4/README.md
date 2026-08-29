Este paso establece la línea base de calibración de la dirección, alineando las ruedas delanteras en el centro y fijando límites de seguridad para evitar atascamientos mecánicos o sobrecarga en el servomotor.

### **Preparación y Configuración**

* **Inspección Física:** Eleve el chasis del robot para que las ruedas delanteras giren libremente sin fricción con el suelo.
* **Conexión:** Verifique que el cable de señal del servo esté conectado al pin de modulación por ancho de pulsos en el microcontrolador.
* **Energía:** Asegúrese de activar las fuentes de alimentación del motor y de la lógica del sistema, comprobando los niveles de batería si es necesario.

---

### **Flujo de Trabajo de Calibración**

* **Definición de Constantes:** Revise el archivo de configuración para identificar el ángulo de centro predeterminado y registrar los rangos límites de giro hacia ambos lados.
* **Calibración del Ángulo Central:** Ajuste gradualmente el valor del ángulo hasta que las ruedas apunten perfectamente en línea recta con respecto al chasis.
* **Prueba de Límites Seguros:** Incremente y decremente el ángulo progresivamente hacia la izquierda y hacia la derecha. Detenga la prueba inmediatamente si detecta resistencia mecánica o esfuerzo en el brazo de dirección, registrando los límites máximos alcanzados.

---

### **Criterios de Finalización**

* **Validación:** El mecanismo de dirección debe moverse de manera fluida en todo su recorrido sin atascos ni ruidos mecánicos. Al restaurar el ángulo central, las ruedas deben quedar completamente alineadas.
* **Guardado de Configuración:** Actualice la constante del centro mecánico en el script principal y asegúrese de que los algoritmos de navegación restrinjan los ángulos de salida estrictamente dentro de los límites seguros probados.
