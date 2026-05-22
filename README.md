# Bellabeat: análisis de hábitos de bienestar con datos de Fitbit

## Contexto

Bellabeat es una empresa de tecnología enfocada en productos de bienestar para mujeres. Este caso de estudio, inspirado en el proyecto final del certificado Google Data Analytics, analiza datos públicos de dispositivos Fitbit para identificar patrones de actividad, sueño y uso que puedan orientar recomendaciones de marketing para Bellabeat.

El proyecto sigue el proceso completo de análisis de datos: **Ask, Prepare, Process, Analyze, Share y Act**.

## Problema de negocio

Bellabeat busca crecer en el mercado de dispositivos inteligentes de bienestar. Para tomar mejores decisiones de marketing, necesita entender cómo las personas usan dispositivos de seguimiento de actividad y descanso, y convertir esos patrones en acciones concretas de comunicación, segmentación y posicionamiento.

## Objetivo

Analizar datos públicos de Fitbit Fitness Tracker Data con Python y `pandas`, preparar datasets limpios para análisis y Power BI, construir visualizaciones exploratorias y traducir los hallazgos en recomendaciones accionables para Bellabeat.

## Preguntas guía

1. ¿Qué tendencias existen en el uso de dispositivos inteligentes?
2. ¿Cómo pueden aplicarse estas tendencias a clientes potenciales o actuales de Bellabeat?
3. ¿De qué forma estos hallazgos pueden influir en la estrategia de marketing de Bellabeat?

## Fuente de datos

- Caso base: `data/Case Study 2 How can a wellness company play it smart.pdf`
- Dataset: Fitbit Fitness Tracker Data, distribuido públicamente por Mobius/Kaggle.
- Datos locales:
  - `data/raw/mturkfitbit_export_3.12.16-4.11.16/`
  - `data/raw/mturkfitbit_export_4.12.16-5.12.16/`

El dataset se usa como proxy de comportamiento de usuarios de dispositivos inteligentes. No contiene datos reales de Bellabeat y no incluye variables demográficas, por lo que las conclusiones se mantienen en el nivel de patrones observados y recomendaciones razonables de marketing.

## Herramientas

- Python
- pandas
- Jupyter Notebook
- matplotlib
- Power BI
- Git

## Metodología

### Ask

Se define la tarea de negocio, los stakeholders y las preguntas analíticas que conectan actividad física, sueño, comportamiento de uso y oportunidades de marketing.

### Prepare

Se inventarian los archivos fuente, se evalúan alcance y limitaciones del dataset, y se seleccionan las tablas prioritarias para una primera versión del caso.

Documento: `reports/prepare_data_assessment.md`

### Process

Se limpian datos de actividad diaria y sueño, se normalizan columnas, se corrigen tipos de fecha, se eliminan duplicados y se generan variables derivadas para análisis.

Script: `scripts/prepare_fitbit_data.py`

Datasets procesados:

- `data/processed/daily_activity_clean.csv`
- `data/processed/sleep_daily_clean.csv`
- `data/processed/bellabeat_analysis_dataset.csv`
- `data/processed/user_segments.csv`

### Analyze

Se exploran tendencias por usuario, día de la semana, nivel de actividad, sedentarismo y sueño. Cada hallazgo se conecta con cálculos reproducibles.

Script: `scripts/analyze_fitbit_data.py`

Reporte: `reports/analysis_findings.md`

### Share

Se preparan visualizaciones exploratorias y una estructura clara para el dashboard final en Power BI.

Visualizaciones:

- `visualizations/avg_steps_by_day.png`
- `visualizations/avg_sleep_by_day.png`
- `visualizations/users_by_activity_segment.png`
- `visualizations/steps_vs_sleep.png`

Guía de dashboard: `dashboard/README.md`

### Act

Se traducen los hallazgos en recomendaciones de marketing para Bellabeat, priorizando segmentación por nivel de actividad, mensajes de bienestar integral y retos semanales.

Reporte ejecutivo: `reports/caso_estudio_bellabeat.md`

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
│   └── powerbi/
├── reports/
└── README.md
```

## Cómo reproducir el proyecto

Desde la raíz del repositorio:

```powershell
pip install -r requirements.txt
python scripts/prepare_fitbit_data.py
python scripts/analyze_fitbit_data.py
```

El primer comando regenera los datasets procesados y la documentación de preparación. El segundo comando actualiza las visualizaciones, el reporte de hallazgos, el caso de estudio y la guía del dashboard.

## Entregables

- Documentación del proceso Ask, Prepare, Process, Analyze, Share y Act.
- Scripts reproducibles de limpieza y análisis.
- Datasets procesados listos para Power BI.
- Visualizaciones exploratorias.
- Reporte ejecutivo de portafolio.
- Estructura preparada para dashboard final en Power BI.

## Estado

El proyecto ya cuenta con la base metodológica, limpieza reproducible, análisis exploratorio inicial y reportes principales. El siguiente paso es construir el dashboard final en Power BI usando los archivos de `data/processed/`.
