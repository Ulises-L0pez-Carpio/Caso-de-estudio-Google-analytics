"""Analyze processed Fitbit data for the Bellabeat portfolio case study."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
VIS_DIR = PROJECT_ROOT / "visualizations"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"


DAY_ORDER = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    analysis = pd.read_csv(PROCESSED_DIR / "bellabeat_analysis_dataset.csv", parse_dates=["activity_date"])
    users = pd.read_csv(PROCESSED_DIR / "user_segments.csv")
    return analysis, users


def save_bar_chart(data: pd.Series, title: str, ylabel: str, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    data.plot(kind="bar", ax=ax, color="#2a9d8f")
    ax.set_title(title)
    ax.set_xlabel("")
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=35)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def save_scatter(data: pd.DataFrame, x: str, y: str, title: str, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(data[x], data[y], alpha=0.65, color="#264653")
    ax.set_title(title)
    ax.set_xlabel(x.replace("_", " ").title())
    ax.set_ylabel(y.replace("_", " ").title())
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def build_metrics(analysis: pd.DataFrame, users: pd.DataFrame) -> dict[str, object]:
    by_day = (
        analysis.groupby("day_of_week")["total_steps"]
        .mean()
        .reindex(DAY_ORDER)
        .dropna()
        .round(0)
    )
    sleep_by_day = (
        analysis.dropna(subset=["sleep_hours"])
        .groupby("day_of_week")["sleep_hours"]
        .mean()
        .reindex(DAY_ORDER)
        .dropna()
        .round(2)
    )
    segment_counts = users["user_segment"].value_counts().sort_index()
    corr = analysis[["total_steps", "calories", "active_minutes", "sedentary_minutes", "sleep_hours"]].corr(
        numeric_only=True
    )
    sleep_corr = corr.loc["total_steps", "sleep_hours"] if "sleep_hours" in corr.columns else float("nan")

    return {
        "records": len(analysis),
        "users": analysis["user_id"].nunique(),
        "date_min": analysis["activity_date"].min().date(),
        "date_max": analysis["activity_date"].max().date(),
        "avg_steps": round(analysis["total_steps"].mean(), 0),
        "avg_calories": round(analysis["calories"].mean(), 0),
        "avg_active_minutes": round(analysis["active_minutes"].mean(), 1),
        "avg_sedentary_minutes": round(analysis["sedentary_minutes"].mean(), 1),
        "avg_sleep_hours": round(analysis["sleep_hours"].mean(), 2),
        "pct_10000_days": round(analysis["meets_10000_steps"].mean() * 100, 1),
        "top_day": by_day.idxmax(),
        "low_day": by_day.idxmin(),
        "top_day_steps": int(by_day.max()),
        "low_day_steps": int(by_day.min()),
        "sleep_corr": round(sleep_corr, 3),
        "by_day": by_day,
        "sleep_by_day": sleep_by_day,
        "segment_counts": segment_counts,
    }


def create_visualizations(analysis: pd.DataFrame, users: pd.DataFrame, metrics: dict[str, object]) -> None:
    VIS_DIR.mkdir(parents=True, exist_ok=True)
    save_bar_chart(
        metrics["by_day"],
        "Promedio de pasos por día de la semana",
        "Pasos promedio",
        VIS_DIR / "avg_steps_by_day.png",
    )
    save_bar_chart(
        metrics["sleep_by_day"],
        "Promedio de horas de sueño por día de la semana",
        "Horas promedio",
        VIS_DIR / "avg_sleep_by_day.png",
    )
    save_bar_chart(
        metrics["segment_counts"],
        "Usuarios por segmento de actividad",
        "Usuarios",
        VIS_DIR / "users_by_activity_segment.png",
    )
    save_scatter(
        analysis.dropna(subset=["sleep_hours"]),
        "total_steps",
        "sleep_hours",
        "Relación entre pasos diarios y horas de sueño",
        VIS_DIR / "steps_vs_sleep.png",
    )


def write_analysis_report(metrics: dict[str, object]) -> None:
    report = f"""# Analyze: hallazgos del análisis exploratorio

## Resumen de datos analizados

- Registros diarios analizados: {metrics["records"]:,}
- Usuarios únicos: {metrics["users"]:,}
- Periodo cubierto: {metrics["date_min"]} a {metrics["date_max"]}
- Pasos promedio por dia: {metrics["avg_steps"]:,.0f}
- Calorias promedio por dia: {metrics["avg_calories"]:,.0f}
- Minutos activos promedio por dia: {metrics["avg_active_minutes"]:,.1f}
- Minutos sedentarios promedio por dia: {metrics["avg_sedentary_minutes"]:,.1f}
- Horas de sueño promedio cuando hay registro: {metrics["avg_sleep_hours"]:,.2f}
- Días con al menos 10,000 pasos: {metrics["pct_10000_days"]}%

## Hallazgos principales

1. La actividad física diaria es heterogénea: los usuarios se distribuyen en segmentos de baja, ligera, media y alta actividad, lo que sugiere que una sola estrategia de marketing sería menos efectiva que mensajes segmentados.
2. El promedio diario de pasos queda por debajo del punto de referencia de 10,000 pasos en una parte importante de los días observados; esto abre oportunidad para retos, recordatorios y metas graduales dentro de la app.
3. El día con mayor promedio de pasos es **{metrics["top_day"]}** ({metrics["top_day_steps"]:,} pasos), mientras que el menor promedio ocurre en **{metrics["low_day"]}** ({metrics["low_day_steps"]:,} pasos). La comunicación puede adaptarse por momento de la semana.
4. El sueño está disponible para menos usuarios que la actividad, pero permite conectar bienestar, descanso y consistencia como ejes de contenido.
5. La correlación observada entre pasos diarios y horas de sueño es **{metrics["sleep_corr"]}**. Esta asociación no debe interpretarse causalmente, pero ayuda a explorar mensajes integrales de bienestar.

## Visualizaciones generadas

- `visualizations/avg_steps_by_day.png`
- `visualizations/avg_sleep_by_day.png`
- `visualizations/users_by_activity_segment.png`
- `visualizations/steps_vs_sleep.png`
"""
    (REPORTS_DIR / "analysis_findings.md").write_text(report, encoding="utf-8")


def write_case_study(metrics: dict[str, object]) -> None:
    report = f"""# Caso de estudio: Bellabeat

## Ask

Bellabeat necesita identificar tendencias en el uso de dispositivos inteligentes para orientar su estrategia de marketing. La tarea de negocio es transformar datos de actividad y sueño de usuarios de Fitbit en recomendaciones accionables para productos de bienestar como Leaf, Time y la app de Bellabeat.

Preguntas que guían el análisis:

- Qué tendencias existen en actividad diaria, descanso y uso del dispositivo.
- Cómo pueden aplicarse esas tendencias a clientes potenciales de Bellabeat.
- Cómo pueden influir los hallazgos en campañas, mensajes y segmentación de marketing.

## Prepare

Se utilizaron datos públicos de Fitbit disponibles en `data/raw/`. El dataset se usa como proxy de comportamiento de usuarios de dispositivos inteligentes, no como información real de clientes Bellabeat. La evaluación completa está documentada en `reports/prepare_data_assessment.md`.

Limitaciones clave:

- Muestra pequeña y autoseleccionada.
- Sin variables demográficas.
- Datos de 2016.
- Cobertura desigual entre actividad y sueño.

## Process

La limpieza se realizó con `scripts/prepare_fitbit_data.py`. El flujo combina actividad diaria, limpia sueño diario, normaliza columnas, calcula variables derivadas y genera datasets listos para análisis y Power BI.

Archivos principales:

- `data/processed/daily_activity_clean.csv`
- `data/processed/sleep_daily_clean.csv`
- `data/processed/bellabeat_analysis_dataset.csv`
- `data/processed/user_segments.csv`

## Analyze

El análisis explora {metrics["records"]:,} registros diarios de {metrics["users"]:,} usuarios entre {metrics["date_min"]} y {metrics["date_max"]}. Los usuarios registran en promedio {metrics["avg_steps"]:,.0f} pasos diarios, {metrics["avg_active_minutes"]:,.1f} minutos activos y {metrics["avg_sedentary_minutes"]:,.1f} minutos sedentarios.

Hallazgos principales:

- La actividad varía de forma suficiente para justificar segmentación por nivel de uso.
- Solo {metrics["pct_10000_days"]}% de los días alcanzan 10,000 pasos, lo que sugiere oportunidad para metas progresivas.
- **{metrics["top_day"]}** muestra el mayor promedio de pasos y **{metrics["low_day"]}** el menor, por lo que el momento de la semana puede orientar mensajes.
- El sueño promedio observado es de {metrics["avg_sleep_hours"]:,.2f} horas en registros disponibles, con cobertura menor que actividad.

## Share

El dashboard final en Power BI debe construirse a partir de `data/processed/bellabeat_analysis_dataset.csv` y `data/processed/user_segments.csv`.

Vistas recomendadas:

- Actividad diaria: pasos, calorías y minutos activos.
- Sueño: horas dormidas, tiempo en cama y eficiencia.
- Segmentos: usuarios por nivel de actividad.
- Implicaciones de negocio: hallazgos y recomendaciones.

## Act

Recomendaciones para Bellabeat:

1. Crear campañas segmentadas por nivel de actividad: usuarios de baja actividad requieren metas pequeñas y recordatorios suaves; usuarios activos pueden responder mejor a retos y logros.
2. Posicionar el bienestar como combinación de movimiento y descanso, usando mensajes que conecten actividad, sueño y consistencia.
3. Diseñar retos semanales ajustados al comportamiento observado, reforzando los días con menor actividad.
4. Usar la app de Bellabeat para contenido educativo personalizado sobre hábitos saludables y seguimiento del progreso.
5. Validar estas recomendaciones con datos propios de Bellabeat o pruebas A/B antes de escalar campañas.
"""
    (REPORTS_DIR / "caso_estudio_bellabeat.md").write_text(report, encoding="utf-8")


def write_dashboard_readme() -> None:
    dashboard_readme = """# Dashboard Power BI

## Fuente recomendada

Construir el dashboard desde estos archivos procesados:

- `data/processed/bellabeat_analysis_dataset.csv`
- `data/processed/user_segments.csv`

## Paginas sugeridas

1. **Resumen ejecutivo**: KPIs de pasos, calorías, minutos activos, sueño y usuarios.
2. **Actividad**: tendencias por día de la semana, distribución de pasos y segmentos.
3. **Sueño**: horas dormidas, tiempo en cama y eficiencia.
4. **Recomendaciones**: hallazgos clave traducidos a acciones de marketing.

## Evidencia exportada

Las capturas finales del dashboard deben guardarse en `dashboard/exports/` para que el portafolio sea visible aunque el archivo `.pbix` no se pueda previsualizar en GitHub.
"""
    (DASHBOARD_DIR / "README.md").write_text(dashboard_readme, encoding="utf-8")


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    analysis, users = load_data()
    metrics = build_metrics(analysis, users)
    create_visualizations(analysis, users, metrics)
    write_analysis_report(metrics)
    write_case_study(metrics)
    write_dashboard_readme()

    print("Analyzed Fitbit data successfully.")
    print(f"Users={metrics['users']:,}, records={metrics['records']:,}, avg_steps={metrics['avg_steps']:,.0f}")


if __name__ == "__main__":
    main()
