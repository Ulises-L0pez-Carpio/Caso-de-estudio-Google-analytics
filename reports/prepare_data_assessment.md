# Prepare: evaluación de datos

## Fuente

El proyecto usa el dataset público **Fitbit Fitness Tracker Data**, distribuido como parte del caso de estudio de Google Data Analytics para Bellabeat. Los archivos locales se encuentran en `data/raw/`.

## Inventario de archivos CSV

| Archivo | Periodo | Granularidad | Columnas | KB |
| --- | --- | --- | ---: | ---: |
| dailyActivity_merged.csv | 3.12.16-4.11.16 | diario | 15 | 50.1 |
| heartrate_seconds_merged.csv | 3.12.16-4.11.16 | segundos | 3 | 40107.0 |
| hourlyCalories_merged.csv | 3.12.16-4.11.16 | horario | 3 | 852.2 |
| hourlyIntensities_merged.csv | 3.12.16-4.11.16 | horario | 4 | 948.9 |
| hourlySteps_merged.csv | 3.12.16-4.11.16 | horario | 3 | 845.0 |
| minuteCaloriesNarrow_merged.csv | 3.12.16-4.11.16 | minuto | 3 | 70763.6 |
| minuteIntensitiesNarrow_merged.csv | 3.12.16-4.11.16 | minuto | 3 | 49339.4 |
| minuteMETsNarrow_merged.csv | 3.12.16-4.11.16 | minuto | 3 | 50752.8 |
| minuteSleep_merged.csv | 3.12.16-4.11.16 | minuto | 4 | 9098.0 |
| minuteStepsNarrow_merged.csv | 3.12.16-4.11.16 | minuto | 3 | 49504.0 |
| weightLogInfo_merged.csv | 3.12.16-4.11.16 | peso | 8 | 3.3 |
| dailyActivity_merged.csv | 4.12.16-5.12.16 | diario | 15 | 108.7 |
| dailyCalories_merged.csv | 4.12.16-5.12.16 | diario | 3 | 24.5 |
| dailyIntensities_merged.csv | 4.12.16-5.12.16 | diario | 10 | 68.9 |
| dailySteps_merged.csv | 4.12.16-5.12.16 | diario | 3 | 24.6 |
| heartrate_seconds_merged.csv | 4.12.16-5.12.16 | segundos | 3 | 87488.6 |
| hourlyCalories_merged.csv | 4.12.16-5.12.16 | horario | 3 | 782.7 |
| hourlyIntensities_merged.csv | 4.12.16-5.12.16 | horario | 4 | 877.7 |
| hourlySteps_merged.csv | 4.12.16-5.12.16 | horario | 3 | 777.9 |
| minuteCaloriesNarrow_merged.csv | 4.12.16-5.12.16 | minuto | 3 | 64886.6 |
| minuteCaloriesWide_merged.csv | 4.12.16-5.12.16 | minuto | 62 | 22454.2 |
| minuteIntensitiesNarrow_merged.csv | 4.12.16-5.12.16 | minuto | 3 | 45272.3 |
| minuteIntensitiesWide_merged.csv | 4.12.16-5.12.16 | minuto | 62 | 3234.1 |
| minuteMETsNarrow_merged.csv | 4.12.16-5.12.16 | minuto | 3 | 46569.0 |
| minuteSleep_merged.csv | 4.12.16-5.12.16 | minuto | 4 | 8641.0 |
| minuteStepsNarrow_merged.csv | 4.12.16-5.12.16 | minuto | 3 | 45441.4 |
| minuteStepsWide_merged.csv | 4.12.16-5.12.16 | minuto | 62 | 3399.6 |
| sleepDay_merged.csv | 4.12.16-5.12.16 | sueño | 5 | 17.7 |
| weightLogInfo_merged.csv | 4.12.16-5.12.16 | peso | 8 | 6.6 |

## Tablas prioritarias para la primera versión

- `dailyActivity_merged.csv`: base principal para pasos, calorías, minutos activos, distancia y sedentarismo.
- `sleepDay_merged.csv`: base de sueño diario para unir con actividad por usuario y fecha.
- `hourlySteps_merged.csv`, `hourlyIntensities_merged.csv` y `hourlyCalories_merged.csv`: apoyo opcional para dashboard horario.

## Criterios de calidad revisados

- Registros de actividad diaria combinados: 1,373
- Usuarios únicos en actividad diaria: 35
- Rango de fechas de actividad: 2016-03-12 a 2016-05-12
- Registros de sueño diario disponibles: 410
- Usuarios únicos con sueño diario: 24
- Rango de fechas de sueño: 2016-04-12 a 2016-05-12

## Limitaciones relevantes

- El dataset no contiene datos reales de Bellabeat; se usa como proxy de comportamiento de usuarios de dispositivos inteligentes.
- La muestra es pequeña y no incluye variables demográficas, por lo que no permite inferencias sólidas por edad, género, ubicación o estilo de vida.
- La participación proviene de usuarios que compartieron datos de Fitbit, lo que puede introducir sesgo de autoselección.
- Los datos corresponden a 2016; las recomendaciones deben interpretarse como patrones de comportamiento, no como lectura actual del mercado.
- No se harán afirmaciones causales entre actividad y sueño; solo se reportarán asociaciones observadas.

## Decision de alcance

La primera versión del proyecto se concentrará en actividad diaria y sueño diario. Esta decisión mantiene el caso reproducible, comprensible para portafolio y suficientemente conectado con recomendaciones de marketing.
