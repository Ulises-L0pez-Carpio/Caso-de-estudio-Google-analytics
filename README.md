# Bellabeat: análisis de hábitos de bienestar con datos de Fitbit

## Resumen ejecutivo

Este proyecto desarrolla un caso de estudio de analítica de datos inspirado en el caso final de Google Data Analytics: **Bellabeat, "How can a wellness company play it smart?"**.

El objetivo es identificar patrones de actividad, sueño y uso de dispositivos inteligentes a partir del dataset público **Fitbit Fitness Tracker Data**, y traducir esos hallazgos en recomendaciones de marketing para Bellabeat.

El análisis cubre datos diarios de actividad y sueño, genera datasets procesados con Python y `pandas`, produce visualizaciones exploratorias y deja una guía exacta para construir el dashboard final en Power BI.

## Problema de negocio

Bellabeat busca fortalecer su estrategia de crecimiento en el mercado de bienestar. Para ello necesita entender cómo las personas usan dispositivos inteligentes en su vida diaria y convertir esos patrones en acciones de marketing más relevantes: segmentación, mensajes, retos, recordatorios y posicionamiento de producto.

## Preguntas guía

1. ¿Qué tendencias existen en el uso de dispositivos inteligentes?
2. ¿Cómo pueden aplicarse estas tendencias a clientes potenciales o actuales de Bellabeat?
3. ¿De qué forma estos hallazgos pueden influir en la estrategia de marketing de Bellabeat?

## Hallazgos principales

- Se analizaron `1,373` registros diarios de `35` usuarios.
- El promedio diario observado fue de aproximadamente `7,247` pasos.
- Solo `30.6%` de los días alcanzaron al menos `10,000` pasos.
- El sueño promedio registrado fue de aproximadamente `6.99` horas cuando había datos disponibles.
- La actividad varía por usuario, día de la semana y segmento, lo que respalda una estrategia de marketing segmentada.

## Recomendaciones de marketing

- Crear campañas segmentadas por nivel de actividad: metas pequeñas para usuarios de baja actividad y retos avanzados para usuarios más activos.
- Posicionar Bellabeat como una solución de bienestar integral, conectando movimiento, descanso y consistencia.
- Diseñar retos semanales y recordatorios basados en patrones de actividad por día de la semana.
- Usar la app de Bellabeat para entregar contenido educativo y seguimiento personalizado.
- Validar estas recomendaciones con datos propios de Bellabeat o pruebas A/B antes de escalar campañas.

## Metodología

### Ask

Se definió la tarea de negocio, las preguntas guía y los criterios de éxito del análisis.

### Prepare

Se inventariaron los archivos del dataset, se evaluaron limitaciones y se seleccionaron las tablas prioritarias para el análisis.

Documento: [`reports/prepare_data_assessment.md`](reports/prepare_data_assessment.md)

### Process

Se limpiaron y combinaron datos de actividad diaria y sueño. El flujo normaliza columnas, corrige fechas, elimina duplicados y genera variables analíticas.

Script: [`scripts/prepare_fitbit_data.py`](scripts/prepare_fitbit_data.py)

### Analyze

Se exploraron patrones de pasos, calorías, minutos activos, sedentarismo, sueño y segmentos de usuario.

Reporte: [`reports/analysis_findings.md`](reports/analysis_findings.md)

### Share

Se generaron visualizaciones exploratorias y se preparó una guía detallada para construir el dashboard final en Power BI.

Guía Power BI: [`dashboard/guia_dashboard_powerbi.md`](dashboard/guia_dashboard_powerbi.md)

### Act

Se tradujeron los hallazgos en recomendaciones accionables de marketing para Bellabeat.

Reporte ejecutivo: [`reports/caso_estudio_bellabeat.md`](reports/caso_estudio_bellabeat.md)

## Dashboard Power BI

El dashboard final debe construirse en Power BI Desktop usando únicamente:

- `data/processed/bellabeat_analysis_dataset.csv`
- `data/processed/user_segments.csv`

La guía completa de construcción está en [`dashboard/guia_dashboard_powerbi.md`](dashboard/guia_dashboard_powerbi.md). El archivo editable debe guardarse como `dashboard/powerbi/bellabeat_dashboard.pbix` y las capturas finales deben exportarse a `dashboard/exports/`.

Páginas definidas:

- Resumen ejecutivo
- Actividad
- Sueño
- Segmentos y recomendaciones

## Visualizaciones exploratorias

- [`visualizations/avg_steps_by_day.png`](visualizations/avg_steps_by_day.png)
- [`visualizations/avg_sleep_by_day.png`](visualizations/avg_sleep_by_day.png)
- [`visualizations/users_by_activity_segment.png`](visualizations/users_by_activity_segment.png)
- [`visualizations/steps_vs_sleep.png`](visualizations/steps_vs_sleep.png)

## Datos procesados

- [`data/processed/daily_activity_clean.csv`](data/processed/daily_activity_clean.csv)
- [`data/processed/sleep_daily_clean.csv`](data/processed/sleep_daily_clean.csv)
- [`data/processed/bellabeat_analysis_dataset.csv`](data/processed/bellabeat_analysis_dataset.csv)
- [`data/processed/user_segments.csv`](data/processed/user_segments.csv)
- [`data/processed/raw_file_inventory.csv`](data/processed/raw_file_inventory.csv)

## Habilidades demostradas

- Definición de problema de negocio y preguntas analíticas.
- Evaluación de calidad, sesgos y limitaciones de datos.
- Limpieza y transformación reproducible con Python y `pandas`.
- Análisis exploratorio y generación de variables analíticas.
- Storytelling con datos orientado a una audiencia de negocio.
- Diseño de dashboard en Power BI a partir de datasets procesados.
- Documentación de portafolio y control de versiones con Git/GitHub.

## Cómo reproducir el análisis

Desde la raíz del repositorio:

```powershell
pip install -r requirements.txt
python scripts/prepare_fitbit_data.py
python scripts/analyze_fitbit_data.py
```

El primer comando regenera los datasets procesados y la documentación de preparación. El segundo comando actualiza las visualizaciones, el reporte de hallazgos, el reporte ejecutivo y la documentación del dashboard.

## Estructura del proyecto

```text
Caso-de-exito/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── scripts/
├── visualizations/
├── dashboard/
│   ├── exports/
│   ├── powerbi/
│   ├── README.md
│   └── guia_dashboard_powerbi.md
├── reports/
├── requirements.txt
└── README.md
```

## Limitaciones

- El dataset no contiene datos reales de Bellabeat; se usa como proxy de comportamiento de usuarios de dispositivos inteligentes.
- La muestra es pequeña y autoseleccionada.
- No hay variables demográficas.
- Los datos corresponden a 2016.
- Las relaciones observadas no deben interpretarse como causalidad.

## Estado del proyecto

El análisis reproducible, los reportes y la guía del dashboard están completos. El último paso manual es construir el dashboard en Power BI Desktop, guardar el `.pbix` y exportar las cuatro capturas finales a `dashboard/exports/`.
