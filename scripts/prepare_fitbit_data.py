"""Prepare Fitbit data for the Bellabeat portfolio case study.

This script inventories the raw CSV files, cleans the priority daily activity
and sleep tables, and writes reproducible processed datasets for analysis and
Power BI.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"

DAY_NAMES_ES = {
    "Monday": "lunes",
    "Tuesday": "martes",
    "Wednesday": "miércoles",
    "Thursday": "jueves",
    "Friday": "viernes",
    "Saturday": "sábado",
    "Sunday": "domingo",
}

DAY_ORDER_ES = {
    "lunes": 1,
    "martes": 2,
    "miércoles": 3,
    "jueves": 4,
    "viernes": 5,
    "sábado": 6,
    "domingo": 7,
}


def snake_case(name: str) -> str:
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"[^a-zA-Z0-9]+", "_", name)
    return name.strip("_").lower()


def infer_period(path: Path) -> str:
    match = re.search(r"(\d+\.\d+\.\d+-\d+\.\d+\.\d+)", str(path))
    return match.group(1) if match else "unknown"


def infer_granularity(filename: str) -> str:
    lower = filename.lower()
    if lower.startswith("daily"):
        return "diario"
    if lower.startswith("hourly"):
        return "horario"
    if lower.startswith("minute"):
        return "minuto"
    if "sleep" in lower:
        return "sueño"
    if "weight" in lower:
        return "peso"
    if "heartrate" in lower:
        return "segundos"
    return "otro"


def inventory_raw_files() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for path in sorted(RAW_DIR.rglob("*.csv")):
        sample = pd.read_csv(path, nrows=5)
        rows.append(
            {
                "file_name": path.name,
                "relative_path": path.relative_to(PROJECT_ROOT).as_posix(),
                "period": infer_period(path),
                "granularity": infer_granularity(path.name),
                "columns": ", ".join(sample.columns),
                "column_count": len(sample.columns),
                "sample_rows_read": len(sample),
                "file_size_kb": round(path.stat().st_size / 1024, 1),
            }
        )
    return pd.DataFrame(rows)


def read_and_combine(pattern: str) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in sorted(RAW_DIR.rglob(pattern)):
        frame = pd.read_csv(path)
        frame["source_period"] = infer_period(path)
        frame["source_file"] = path.relative_to(PROJECT_ROOT).as_posix()
        frames.append(frame)
    if not frames:
        raise FileNotFoundError(f"No files found for pattern: {pattern}")
    return pd.concat(frames, ignore_index=True)


def clean_daily_activity() -> pd.DataFrame:
    activity = read_and_combine("dailyActivity_merged.csv")
    activity.columns = [snake_case(col) for col in activity.columns]
    activity["activity_date"] = pd.to_datetime(activity["activity_date"], format="%m/%d/%Y").dt.date
    activity = activity.drop_duplicates(subset=["id", "activity_date"]).copy()

    numeric_columns = [
        col
        for col in activity.columns
        if col not in {"id", "activity_date", "source_period", "source_file"}
    ]
    for col in numeric_columns:
        activity[col] = pd.to_numeric(activity[col], errors="coerce")

    activity["active_minutes"] = (
        activity["very_active_minutes"]
        + activity["fairly_active_minutes"]
        + activity["lightly_active_minutes"]
    )
    activity["tracked_minutes"] = activity["active_minutes"] + activity["sedentary_minutes"]
    activity["sedentary_ratio"] = (
        activity["sedentary_minutes"] / activity["tracked_minutes"].replace(0, pd.NA)
    ).round(4)
    activity["day_of_week"] = pd.to_datetime(activity["activity_date"]).dt.day_name().map(DAY_NAMES_ES)
    activity["day_order"] = activity["day_of_week"].map(DAY_ORDER_ES)
    activity["activity_level"] = pd.cut(
        activity["total_steps"],
        bins=[-1, 4999, 7499, 9999, float("inf")],
        labels=["baja", "ligera", "activa", "muy_activa"],
    )
    activity["meets_10000_steps"] = activity["total_steps"] >= 10000
    return activity


def clean_sleep_daily() -> pd.DataFrame:
    sleep = read_and_combine("sleepDay_merged.csv")
    sleep.columns = [snake_case(col) for col in sleep.columns]
    sleep["sleep_date"] = pd.to_datetime(sleep["sleep_day"], format="%m/%d/%Y %I:%M:%S %p").dt.date
    sleep = sleep.drop(columns=["sleep_day"])
    sleep = sleep.drop_duplicates(subset=["id", "sleep_date"]).copy()
    for col in ["total_sleep_records", "total_minutes_asleep", "total_time_in_bed"]:
        sleep[col] = pd.to_numeric(sleep[col], errors="coerce")
    sleep["sleep_hours"] = (sleep["total_minutes_asleep"] / 60).round(2)
    sleep["time_in_bed_hours"] = (sleep["total_time_in_bed"] / 60).round(2)
    sleep["sleep_efficiency"] = (
        sleep["total_minutes_asleep"] / sleep["total_time_in_bed"].replace(0, pd.NA)
    ).round(4)
    sleep["day_of_week"] = pd.to_datetime(sleep["sleep_date"]).dt.day_name().map(DAY_NAMES_ES)
    sleep["day_order"] = sleep["day_of_week"].map(DAY_ORDER_ES)
    return sleep


def build_analysis_dataset(activity: pd.DataFrame, sleep: pd.DataFrame) -> pd.DataFrame:
    analysis = activity.merge(
        sleep,
        how="left",
        left_on=["id", "activity_date"],
        right_on=["id", "sleep_date"],
        suffixes=("", "_sleep"),
    )
    analysis = analysis.drop(
        columns=["sleep_date", "source_period_sleep", "source_file_sleep", "day_of_week_sleep", "day_order_sleep"]
    )
    analysis = analysis.rename(columns={"id": "user_id"})
    return analysis


def build_user_segments(analysis: pd.DataFrame) -> pd.DataFrame:
    users = (
        analysis.groupby("user_id")
        .agg(
            tracked_days=("activity_date", "nunique"),
            avg_steps=("total_steps", "mean"),
            avg_calories=("calories", "mean"),
            avg_active_minutes=("active_minutes", "mean"),
            avg_sedentary_minutes=("sedentary_minutes", "mean"),
            avg_sleep_hours=("sleep_hours", "mean"),
            days_meeting_10000_steps=("meets_10000_steps", "sum"),
        )
        .reset_index()
    )
    users["avg_steps"] = users["avg_steps"].round(1)
    users["avg_calories"] = users["avg_calories"].round(1)
    users["avg_active_minutes"] = users["avg_active_minutes"].round(1)
    users["avg_sedentary_minutes"] = users["avg_sedentary_minutes"].round(1)
    users["avg_sleep_hours"] = users["avg_sleep_hours"].round(2)
    users["pct_days_meeting_10000_steps"] = (
        users["days_meeting_10000_steps"] / users["tracked_days"]
    ).round(4)
    users["user_segment"] = pd.cut(
        users["avg_steps"],
        bins=[-1, 4999, 7499, 9999, float("inf")],
        labels=["baja_actividad", "actividad_ligera", "actividad_media", "alta_actividad"],
    )
    return users


def write_prepare_report(inventory: pd.DataFrame, activity: pd.DataFrame, sleep: pd.DataFrame) -> None:
    priority_tables = [
        "dailyActivity_merged.csv",
        "sleepDay_merged.csv",
        "hourlySteps_merged.csv",
        "hourlyIntensities_merged.csv",
        "hourlyCalories_merged.csv",
    ]
    inventory_rows = "\n".join(
        f"| {row.file_name} | {row.period} | {row.granularity} | {row.column_count} | {row.file_size_kb} |"
        for row in inventory.itertuples(index=False)
    )
    report = f"""# Prepare: evaluación de datos

## Fuente

El proyecto usa el dataset público **Fitbit Fitness Tracker Data**, distribuido como parte del caso de estudio de Google Data Analytics para Bellabeat. Los archivos locales se encuentran en `data/raw/`.

## Inventario de archivos CSV

| Archivo | Periodo | Granularidad | Columnas | KB |
| --- | --- | --- | ---: | ---: |
{inventory_rows}

## Tablas prioritarias para la primera versión

- `dailyActivity_merged.csv`: base principal para pasos, calorías, minutos activos, distancia y sedentarismo.
- `sleepDay_merged.csv`: base de sueño diario para unir con actividad por usuario y fecha.
- `hourlySteps_merged.csv`, `hourlyIntensities_merged.csv` y `hourlyCalories_merged.csv`: apoyo opcional para dashboard horario.

## Criterios de calidad revisados

- Registros de actividad diaria combinados: {len(activity):,}
- Usuarios únicos en actividad diaria: {activity["id"].nunique():,}
- Rango de fechas de actividad: {activity["activity_date"].min()} a {activity["activity_date"].max()}
- Registros de sueño diario disponibles: {len(sleep):,}
- Usuarios únicos con sueño diario: {sleep["id"].nunique():,}
- Rango de fechas de sueño: {sleep["sleep_date"].min()} a {sleep["sleep_date"].max()}

## Limitaciones relevantes

- El dataset no contiene datos reales de Bellabeat; se usa como proxy de comportamiento de usuarios de dispositivos inteligentes.
- La muestra es pequeña y no incluye variables demográficas, por lo que no permite inferencias sólidas por edad, género, ubicación o estilo de vida.
- La participación proviene de usuarios que compartieron datos de Fitbit, lo que puede introducir sesgo de autoselección.
- Los datos corresponden a 2016; las recomendaciones deben interpretarse como patrones de comportamiento, no como lectura actual del mercado.
- No se harán afirmaciones causales entre actividad y sueño; solo se reportarán asociaciones observadas.

## Decision de alcance

La primera versión del proyecto se concentrará en actividad diaria y sueño diario. Esta decisión mantiene el caso reproducible, comprensible para portafolio y suficientemente conectado con recomendaciones de marketing.
"""
    (REPORTS_DIR / "prepare_data_assessment.md").write_text(report, encoding="utf-8")

    inventory.to_csv(PROCESSED_DIR / "raw_file_inventory.csv", index=False, encoding="utf-8")


def write_cleaning_log(activity: pd.DataFrame, sleep: pd.DataFrame, analysis: pd.DataFrame) -> None:
    log = f"""# Process: decisiones de limpieza

## Transformaciones aplicadas

- Se combinaron los archivos `dailyActivity_merged.csv` de ambos periodos disponibles.
- Se normalizaron nombres de columnas a `snake_case`.
- Se convirtieron fechas de actividad y sueño a tipo fecha.
- Se eliminaron duplicados por usuario y fecha en actividad diaria y sueño diario.
- Se calcularon variables derivadas: `active_minutes`, `tracked_minutes`, `sedentary_ratio`, `activity_level`, `meets_10000_steps`, `sleep_hours`, `time_in_bed_hours`, `sleep_efficiency` y `day_order`.
- Se unieron actividad y sueño por `user_id` y fecha para crear `bellabeat_analysis_dataset.csv`.

## Archivos generados

- `data/processed/daily_activity_clean.csv`: {len(activity):,} filas.
- `data/processed/sleep_daily_clean.csv`: {len(sleep):,} filas.
- `data/processed/bellabeat_analysis_dataset.csv`: {len(analysis):,} filas.
- `data/processed/user_segments.csv`: resumen por usuario para segmentacion.
- `data/processed/raw_file_inventory.csv`: inventario de archivos fuente.

## Limitaciones despues de limpieza

- El sueño diario solo está disponible para una parte de usuarios y fechas, por lo que el dataset integrado conserva valores nulos en métricas de sueño.
- La clasificación de actividad por pasos usa puntos de referencia generales y no debe interpretarse como recomendación médica.
- No se imputaron valores de sueño faltantes para evitar inventar comportamiento no observado.
"""
    (REPORTS_DIR / "process_cleaning_log.md").write_text(log, encoding="utf-8")


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    inventory = inventory_raw_files()
    activity = clean_daily_activity()
    sleep = clean_sleep_daily()
    analysis = build_analysis_dataset(activity, sleep)
    users = build_user_segments(analysis)

    activity.to_csv(PROCESSED_DIR / "daily_activity_clean.csv", index=False, encoding="utf-8")
    sleep.to_csv(PROCESSED_DIR / "sleep_daily_clean.csv", index=False, encoding="utf-8")
    analysis.to_csv(PROCESSED_DIR / "bellabeat_analysis_dataset.csv", index=False, encoding="utf-8")
    users.to_csv(PROCESSED_DIR / "user_segments.csv", index=False, encoding="utf-8")

    write_prepare_report(inventory, activity, sleep)
    write_cleaning_log(activity, sleep, analysis)

    print("Prepared Fitbit data successfully.")
    print(f"Processed rows: activity={len(activity):,}, sleep={len(sleep):,}, analysis={len(analysis):,}")


if __name__ == "__main__":
    main()
