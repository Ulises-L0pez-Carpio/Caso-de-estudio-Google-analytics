# Caso de estudio: Bellabeat

## Resumen ejecutivo

Bellabeat busca convertir datos de uso de dispositivos inteligentes en decisiones de marketing más precisas. Para este caso se analizaron datos públicos de Fitbit como proxy de comportamiento de usuarios de wearables. El análisis cubre 1,373 registros diarios de 35 usuarios entre 2016-03-12 y 2016-05-12.

Los usuarios registran en promedio 7,247 pasos diarios, 217.7 minutos activos, 993.4 minutos sedentarios y 6.99 horas de sueño cuando existe registro. Solo 30.6% de los días alcanzan 10,000 pasos, lo que abre una oportunidad clara para campañas de metas progresivas, recordatorios y retos semanales.

## Ask: problema de negocio

Bellabeat necesita identificar tendencias en el uso de dispositivos inteligentes para orientar su estrategia de marketing. La tarea de negocio es transformar datos de actividad y sueño de usuarios de Fitbit en recomendaciones accionables para productos de bienestar como Leaf, Time y la app de Bellabeat.

Preguntas que guían el análisis:

- Qué tendencias existen en actividad diaria, descanso y uso del dispositivo.
- Cómo pueden aplicarse esas tendencias a clientes potenciales de Bellabeat.
- Cómo pueden influir los hallazgos en campañas, mensajes y segmentación de marketing.

## Prepare: fuente y alcance

Se utilizaron datos públicos de Fitbit disponibles en `data/raw/`. El dataset se usa como proxy de comportamiento de usuarios de dispositivos inteligentes, no como información real de clientes Bellabeat. La evaluación completa está documentada en `reports/prepare_data_assessment.md`.

Limitaciones clave:

- Muestra pequeña y autoseleccionada.
- Sin variables demográficas.
- Datos de 2016.
- Cobertura desigual entre actividad y sueño.

Estas limitaciones obligan a mantener el análisis en términos de patrones observados. No se hacen inferencias demográficas ni conclusiones causales.

## Process: limpieza y modelado

La limpieza se realizó con `scripts/prepare_fitbit_data.py`. El flujo combina actividad diaria, limpia sueño diario, normaliza columnas, calcula variables derivadas y genera datasets listos para análisis y Power BI.

Archivos principales:

- `data/processed/daily_activity_clean.csv`
- `data/processed/sleep_daily_clean.csv`
- `data/processed/bellabeat_analysis_dataset.csv`
- `data/processed/user_segments.csv`

Variables analíticas creadas:

- `active_minutes`: suma de minutos muy activos, moderados y ligeros.
- `sedentary_ratio`: proporción de minutos sedentarios sobre minutos registrados.
- `activity_level`: clasificación diaria por pasos.
- `meets_10000_steps`: indicador de días con al menos 10,000 pasos.
- `sleep_hours` y `sleep_efficiency`: métricas de descanso.
- `day_order`: orden numérico para visualizar días correctamente en Power BI.

## Analyze: hallazgos

El análisis explora 1,373 registros diarios de 35 usuarios entre 2016-03-12 y 2016-05-12. Los usuarios registran en promedio 7,247 pasos diarios, 217.7 minutos activos y 993.4 minutos sedentarios.

Hallazgos principales:

- La actividad varía de forma suficiente para justificar segmentación por nivel de uso.
- Solo 30.6% de los días alcanzan 10,000 pasos, lo que sugiere oportunidad para metas progresivas.
- **sábado** muestra el mayor promedio de pasos y **domingo** el menor, por lo que el momento de la semana puede orientar mensajes.
- El sueño promedio observado es de 6.99 horas en registros disponibles, con cobertura menor que actividad.

Resumen por segmento:

| Segmento | Usuarios | Pasos promedio | Minutos activos promedio | Sueño promedio | Promedio de días 10k |
| --- | ---: | ---: | ---: | ---: | ---: |
| actividad_ligera | 7 | 6,760 | 257.1 | 6.02 | 11.0% |
| actividad_media | 8 | 8,528 | 240.0 | 6.98 | 41.0% |
| alta_actividad | 7 | 12,438 | 290.6 | 4.89 | 82.0% |
| baja_actividad | 13 | 3,139 | 136.9 | 6.58 | 3.0% |

## Share: comunicación visual

El dashboard final en Power BI debe construirse a partir de `data/processed/bellabeat_analysis_dataset.csv` y `data/processed/user_segments.csv`. La guía detallada está en `dashboard/guia_dashboard_powerbi.md`.

Vistas recomendadas:

- Actividad diaria: pasos, calorías y minutos activos.
- Sueño: horas dormidas, tiempo en cama y eficiencia.
- Segmentos: usuarios por nivel de actividad.
- Implicaciones de negocio: hallazgos y recomendaciones.

## Act: recomendaciones de marketing

Recomendaciones para Bellabeat:

1. Crear campañas segmentadas por nivel de actividad: usuarios de baja actividad requieren metas pequeñas y recordatorios suaves; usuarios activos pueden responder mejor a retos y logros.
2. Posicionar el bienestar como combinación de movimiento y descanso, usando mensajes que conecten actividad, sueño y consistencia.
3. Diseñar retos semanales ajustados al comportamiento observado, reforzando los días con menor actividad.
4. Usar la app de Bellabeat para contenido educativo personalizado sobre hábitos saludables y seguimiento del progreso.
5. Validar estas recomendaciones con datos propios de Bellabeat o pruebas A/B antes de escalar campañas.

## Siguientes pasos

- Construir el dashboard final en Power BI siguiendo `dashboard/guia_dashboard_powerbi.md`.
- Exportar las cuatro páginas como PNG en `dashboard/exports/`.
- Validar recomendaciones con datos propios de Bellabeat si estuvieran disponibles.
- Incorporar variables demográficas o encuestas para mejorar la segmentación.
