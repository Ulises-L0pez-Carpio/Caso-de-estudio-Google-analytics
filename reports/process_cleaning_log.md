# Process: decisiones de limpieza

## Transformaciones aplicadas

- Se combinaron los archivos `dailyActivity_merged.csv` de ambos periodos disponibles.
- Se normalizaron nombres de columnas a `snake_case`.
- Se convirtieron fechas de actividad y sueño a tipo fecha.
- Se eliminaron duplicados por usuario y fecha en actividad diaria y sueño diario.
- Se calcularon variables derivadas: `active_minutes`, `tracked_minutes`, `sedentary_ratio`, `activity_level`, `meets_10000_steps`, `sleep_hours`, `time_in_bed_hours`, `sleep_efficiency` y `day_order`.
- Se unieron actividad y sueño por `user_id` y fecha para crear `bellabeat_analysis_dataset.csv`.

## Archivos generados

- `data/processed/daily_activity_clean.csv`: 1,373 filas.
- `data/processed/sleep_daily_clean.csv`: 410 filas.
- `data/processed/bellabeat_analysis_dataset.csv`: 1,373 filas.
- `data/processed/user_segments.csv`: resumen por usuario para segmentacion.
- `data/processed/raw_file_inventory.csv`: inventario de archivos fuente.

## Limitaciones despues de limpieza

- El sueño diario solo está disponible para una parte de usuarios y fechas, por lo que el dataset integrado conserva valores nulos en métricas de sueño.
- La clasificación de actividad por pasos usa puntos de referencia generales y no debe interpretarse como recomendación médica.
- No se imputaron valores de sueño faltantes para evitar inventar comportamiento no observado.
