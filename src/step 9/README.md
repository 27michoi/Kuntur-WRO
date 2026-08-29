## Step 9

### Resumen

El paso 9 se centra en probar y validar el proceso de visión artificial sin conexión, utilizando el conjunto de datos estático capturado en el paso 8 en tres condiciones de iluminación (**normal**, **luminosa**, **oscura**). El objetivo principal es verificar el enmascaramiento de colores (paredes negras, líneas azules/naranjas, obstáculos rojos/verdes), los recuadros delimitadores, los centroides y la resistencia a las variaciones de iluminación antes de aplicar cambios en los parámetros en tiempo real.

___

### Flujo de trabajo

1. **Parche heredado y filtro de verificación:**
* Se ha actualizado el archivo `step9_tests/offline_summary.py` para filtrar las métricas heredadas que carecen de los parámetros `technical_status` o `source_sha256`.


2. **Generación de imágenes comparativas (`offline_summary.py`):**
* Procesa recortes y superposiciones en paralelo (`normal | brillante | oscuro`) en `/step9_results/comparisons/` para las máscaras clave:
* **Procesamiento de paredes:** `crop.jpg`, `binary.jpg`, `clean.jpg`, `polygon.jpg`
* **Superposiciones de color:** `blue_mask_overlay`, `orange_mask_overlay`, `green_mask_overlay`, `red_mask_overlay`, `combined_mask_overlay`


3. **Registro manual de datos de referencia (`scene_observations.csv`):**
* Se inspeccionaron manualmente los recortes de las imágenes originales y se registró la visibilidad de los objetos (`sí`/`no`) en las columnas: `wall`, `blue`, `orange`, `green`, `red` y `notes`.


4. **Evaluación semántica final y generación del informe:**
* Se volvió a ejecutar `offline_summary` utilizando las observaciones completadas para generar `mask_summary.csv`, `lighting_comparison.csv`, `semantic_checks.csv` y `step9_report.txt`.

___

### Problemas clave identificados durante la comprobación semántica

Al ejecutar `grep «REVIEW» semantic_checks.csv`, se detectaron fallos en casos extremos específicos que requieren atención:

* **Falsos positivos:** Se activaron máscaras rojas en las condiciones `bright/pink` (11,5 % de cobertura), `dark/corner` (2,5 %), `dark/lines` (6,1 %) y `normal/pink` (11,15 %).
* **Detecciones omitidas:** Faltan máscaras naranjas, azules y verdes en condiciones oscuras y normales (p. ej., `dark/gf`, `dark/gn`, `dark/left`, `dark/lines`, `dark/rf`, `normal/gf`).
* **Separación deficiente de máscaras:** Ambigüedad entre colores que compiten entre sí (p. ej., «bright/pink»: azul frente a naranja; «normal/gf» y «normal/gn»: verde frente a rojo).

___

### Criterios de superación y entregables

* **Condiciones para la superación final:** 30/30 superaciones técnicas, 0 resultados faltantes, cuadros delimitadores y centroides precisos, detección robusta del contorno de las paredes y alineación visual entre las máscaras y las características físicas reales.
* **Empaquetado del archivo:** Recursos finales empaquetados desde la raíz:
`tar -czf step9_results.tar.gz step9_results`

___

