## Step 7

### Resumen

En el paso 7 evaluamos la geometría de la dirección y los radios de giro del robot mediante pruebas de arco de radio constante. Al recorrer un número determinado de pasos con ángulos fijos de los servomotores, el procedimiento calcula la dinámica de giro utilizando un método de posicionamiento de tres puntos ($P_1, P_2, P_3$).

___

### Datos de configuración y calibración del robot

#### Dimensiones físicas:
* **Distancia entre ejes ($L$):** 167 mm
* **Ancho de vía trasero ($T$):** 139 mm
* **Diámetro/ancho de la rueda:** 56 mm / 27 mm


#### Asignación de controles:
* **Centro del servo:** 82 (en línea recta)
* **Valores más bajos del servo ($< 82$):** Gira a **la DERECHA**
* **Valores más altos del servo ($> 82$):** Gira a **la IZQUIERDA**
* **Velocidad del motor:** 600 pasos/seg. | **Aceleración:** 2000 pasos/seg.²

___

### Test Method & Execution

1. **Configuración del firmware:**
* El código de PlatformIO (`step7_constant_radius_test/src/main.cpp`) controla la dirección mediante los ángulos de los servomotores y la distancia mediante los pasos del motor paso a paso, ejecutándose con una cuenta atrás de 5 segundos (`GO`).



2. **Medición geométrica de tres puntos:**
* El punto medio del eje trasero se marca en el suelo al inicio ($P_1$), tras la primera pasada ($P_2$) y tras una segunda pasada idéntica ($P_3$).
* Se registran las distancias en línea recta entre los puntos ($d_{12}, d_{23}, d_{13}$) para calcular los radios exactos del arco de giro sin necesidad de trazar manualmente las trayectorias curvas.

___

### Datos experimentales y resultados calculados

#### (Número de pasos objetivo = 1800 en todas las pruebas)

| Ángulo | Dirección | $P_1 \to P_2$ ($d_{12}$) | $P_2 \to P_3$ ($d_{23}$) | $P_1 \to P_3$ ($d_{13}$) | Radio de giro calculado |
| --- | --- | --- | --- | --- | --- |
| **75** | Derecha | 1067 mm | 1067 mm | 1945 mm | — |
| **75** | Derecha | 1070 mm | 1049 mm | 1930 mm | — |
| **75** | Derecha | 1030 mm | 1060 mm | 1890 mm | — |
| **66** | Derecha | 932 mm | 932 mm | 1050 mm | **564.0 mm** |
| **90** | Izquierda | 1048 mm | 1065 mm | 1962 mm | — |
| **90** | Izquierda | 1054 mm | 1040 mm | 1961 mm | — |
| **90** | Izquierda | 1067 mm | 1052 mm | 1971 mm | — |
| **105** | Izquierda | 830 mm | 820 mm | 547 mm | **437.3 mm** |

___

### Key Takeaways

#### Resultados del radio de giro:
* **Ángulo 66 (derecha):** Da como resultado un radio de giro de **564,0 mm**.
* **Ángulo 105 (izquierda):** Da como resultado un radio de giro más cerrado de **437,3 mm**.


#### Calibración del accionamiento actualizada:
* A lo largo de las pruebas de 1800 pasos (con una longitud media de recorrido de ~1085 mm), la calibración de la conducción se actualizó a **1660 pasos/metro** (`constexpr long STEPS_PER_METER = 1660L;`).
* *Nota:* Esta conversión de distancia revisada debe verificarse posteriormente con un recorrido directo en línea recta.

___


