# Guía para construir el dashboard en Power BI

## Objetivo

Construir un dashboard ejecutivo para comunicar los principales patrones de actividad, sueño y segmentación observados en el caso Bellabeat. El dashboard debe permitir explicar los hallazgos a una audiencia de negocio y conectar cada visual con una recomendación de marketing.

## Archivos a importar

Importar solo estos CSV procesados:

- `data/processed/bellabeat_analysis_dataset.csv`
- `data/processed/user_segments.csv`

No usar archivos de `data/raw/` en Power BI. La limpieza y transformación ya están documentadas y reproducidas en Python.

## Modelo de datos

Crear la relación:

- `user_segments[user_id]` 1:* `bellabeat_analysis_dataset[user_id]`

Configurar tipos de datos:

- `user_id`: texto
- `activity_date`: fecha
- `day_of_week`, `activity_level`, `user_segment`: texto/categoría
- `day_order`: número entero
- `meets_10000_steps`: verdadero/falso
- pasos, calorías, minutos, horas, ratios y eficiencia: numérico decimal o entero según corresponda

Ordenar `day_of_week` por `day_order` desde la vista de datos.

## Medidas DAX

Crear estas medidas en Power BI:

```DAX
Usuarios = DISTINCTCOUNT(bellabeat_analysis_dataset[user_id])

Registros diarios = COUNTROWS(bellabeat_analysis_dataset)

Pasos promedio = AVERAGE(bellabeat_analysis_dataset[total_steps])

Calorías promedio = AVERAGE(bellabeat_analysis_dataset[calories])

Minutos activos promedio = AVERAGE(bellabeat_analysis_dataset[active_minutes])

Minutos sedentarios promedio = AVERAGE(bellabeat_analysis_dataset[sedentary_minutes])

Horas de sueño promedio = AVERAGE(bellabeat_analysis_dataset[sleep_hours])

Eficiencia de sueño promedio = AVERAGE(bellabeat_analysis_dataset[sleep_efficiency])

% días 10k pasos = AVERAGE(bellabeat_analysis_dataset[meets_10000_steps])

Usuarios con sueño = CALCULATE(
    DISTINCTCOUNT(bellabeat_analysis_dataset[user_id]),
    NOT(ISBLANK(bellabeat_analysis_dataset[sleep_hours]))
)
```

Formatear `% días 10k pasos` como porcentaje.

## Página 1: Resumen ejecutivo

Objetivo: dar una lectura rápida del caso y de los indicadores principales.

Visuales:

- Tarjetas KPI: `Usuarios`, `Registros diarios`, `Pasos promedio`, `Calorías promedio`, `Minutos activos promedio`, `Horas de sueño promedio`.
- Gráfico de barras: eje `day_of_week`, valor `Pasos promedio`.
- Segmentadores: `activity_date`, `activity_level`, `user_segment`.
- Caja de texto con tres hallazgos:
  - El promedio diario de pasos queda por debajo de 10,000.
  - La actividad varía por segmento y día de la semana.
  - El sueño tiene menor cobertura, pero aporta una línea clara de comunicación sobre bienestar integral.

## Página 2: Actividad

Objetivo: explicar patrones de movimiento, calorías y sedentarismo.

Visuales:

- Línea: eje `activity_date`, valor `Pasos promedio`.
- Barras: eje `day_of_week`, valor `Minutos activos promedio`.
- Barras apiladas: valores `very_active_minutes`, `fairly_active_minutes`, `lightly_active_minutes`, `sedentary_minutes`.
- Dispersión: eje X `total_steps`, eje Y `calories`, leyenda `activity_level`.
- Segmentador: `activity_level`.

Mensaje esperado: Bellabeat puede segmentar campañas según intensidad de uso y diseñar retos de actividad progresiva.

## Página 3: Sueño

Objetivo: comunicar la relación entre descanso, actividad y bienestar.

Visuales:

- Tarjetas KPI: `Horas de sueño promedio`, `Eficiencia de sueño promedio`, `Usuarios con sueño`.
- Barras: eje `day_of_week`, valor `Horas de sueño promedio`.
- Dispersión: eje X `total_steps`, eje Y `sleep_hours`.
- Tabla: `user_id`, promedio de `total_steps`, promedio de `sleep_hours`, promedio de `sleep_efficiency`.
- Nota visible: la cobertura de sueño es menor que la de actividad, por lo que las conclusiones deben tomarse como indicios, no como afirmaciones causales.

Mensaje esperado: Bellabeat puede reforzar una narrativa de bienestar integral: movimiento, descanso y consistencia.

## Página 4: Segmentos y recomendaciones

Objetivo: convertir hallazgos en acciones de marketing.

Visuales:

- Barras: eje `user_segment`, valor `Usuarios`.
- Matriz por `user_segment`: promedio de `avg_steps`, `avg_active_minutes`, `avg_sleep_hours`, `pct_days_meeting_10000_steps`.
- Panel de recomendaciones:
  - `baja_actividad`: metas pequeñas, recordatorios suaves y contenido educativo.
  - `actividad_ligera`: retos semanales simples y mensajes de progreso.
  - `actividad_media`: campañas de consistencia y logros.
  - `alta_actividad`: retos avanzados, comunidad y recompensas.
  - sueño: mensajes de descanso y bienestar integral.

## Exportación

Guardar el archivo editable como:

- `dashboard/powerbi/bellabeat_dashboard.pbix`

Exportar capturas PNG como:

- `dashboard/exports/01_resumen_ejecutivo.png`
- `dashboard/exports/02_actividad.png`
- `dashboard/exports/03_sueno.png`
- `dashboard/exports/04_segmentos_recomendaciones.png`

Estas capturas serán la evidencia principal del dashboard en GitHub.

## Checklist final

- Los dos CSV importados provienen de `data/processed/`.
- `day_of_week` está ordenado por `day_order`.
- La relación por `user_id` está activa.
- Las medidas DAX calculan sin errores.
- Las cuatro páginas tienen título, KPIs o visuales centrales y una lectura de negocio.
- Las capturas exportadas están en `dashboard/exports/`.
