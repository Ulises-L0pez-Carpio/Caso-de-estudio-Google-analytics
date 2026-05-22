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
    segment_summary = (
        users.groupby("user_segment", observed=True)
        .agg(
            usuarios=("user_id", "nunique"),
            pasos_promedio=("avg_steps", "mean"),
            minutos_activos_promedio=("avg_active_minutes", "mean"),
            sueno_promedio=("avg_sleep_hours", "mean"),
            pct_dias_10k=("pct_days_meeting_10000_steps", "mean"),
        )
        .round(2)
    )
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
        "segment_summary": segment_summary,
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
    segment_rows = "\n".join(
        f"| {idx} | {row.usuarios:.0f} | {row.pasos_promedio:,.0f} | {row.minutos_activos_promedio:,.1f} | {row.sueno_promedio:,.2f} | {row.pct_dias_10k:.1%} |"
        for idx, row in metrics["segment_summary"].iterrows()
    )
    report = f"""# Caso de estudio: Bellabeat

## Resumen ejecutivo

Bellabeat busca convertir datos de uso de dispositivos inteligentes en decisiones de marketing más precisas. Para este caso se analizaron datos públicos de Fitbit como proxy de comportamiento de usuarios de wearables. El análisis cubre {metrics["records"]:,} registros diarios de {metrics["users"]:,} usuarios entre {metrics["date_min"]} y {metrics["date_max"]}.

Los usuarios registran en promedio {metrics["avg_steps"]:,.0f} pasos diarios, {metrics["avg_active_minutes"]:,.1f} minutos activos, {metrics["avg_sedentary_minutes"]:,.1f} minutos sedentarios y {metrics["avg_sleep_hours"]:,.2f} horas de sueño cuando existe registro. Solo {metrics["pct_10000_days"]}% de los días alcanzan 10,000 pasos, lo que abre una oportunidad clara para campañas de metas progresivas, recordatorios y retos semanales.

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

El análisis explora {metrics["records"]:,} registros diarios de {metrics["users"]:,} usuarios entre {metrics["date_min"]} y {metrics["date_max"]}. Los usuarios registran en promedio {metrics["avg_steps"]:,.0f} pasos diarios, {metrics["avg_active_minutes"]:,.1f} minutos activos y {metrics["avg_sedentary_minutes"]:,.1f} minutos sedentarios.

Hallazgos principales:

- La actividad varía de forma suficiente para justificar segmentación por nivel de uso.
- Solo {metrics["pct_10000_days"]}% de los días alcanzan 10,000 pasos, lo que sugiere oportunidad para metas progresivas.
- **{metrics["top_day"]}** muestra el mayor promedio de pasos y **{metrics["low_day"]}** el menor, por lo que el momento de la semana puede orientar mensajes.
- El sueño promedio observado es de {metrics["avg_sleep_hours"]:,.2f} horas en registros disponibles, con cobertura menor que actividad.

Resumen por segmento:

| Segmento | Usuarios | Pasos promedio | Minutos activos promedio | Sueño promedio | Promedio de días 10k |
| --- | ---: | ---: | ---: | ---: | ---: |
{segment_rows}

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
"""
    (REPORTS_DIR / "caso_estudio_bellabeat.md").write_text(report, encoding="utf-8")


def write_dashboard_readme() -> None:
    dashboard_readme = """# Dashboard Power BI

Esta carpeta contiene la guía y los artefactos del dashboard final del caso Bellabeat.

## Archivos esperados

- `guia_dashboard_powerbi.md`: instrucciones exactas para construir el dashboard en Power BI.
- `powerbi/bellabeat_dashboard.pbix`: archivo editable de Power BI cuando se construya manualmente.
- `exports/`: capturas PNG de las páginas finales del dashboard.

## Fuente del dashboard

Usar únicamente estos archivos procesados:

- `data/processed/bellabeat_analysis_dataset.csv`
- `data/processed/user_segments.csv`

## Páginas esperadas

1. **Resumen ejecutivo**: KPIs de pasos, calorías, minutos activos, sueño y usuarios.
2. **Actividad**: tendencias por día de la semana, distribución de pasos y segmentos.
3. **Sueño**: horas dormidas, tiempo en cama y eficiencia.
4. **Segmentos y recomendaciones**: segmentación de usuarios y acciones de marketing.

## Evidencia exportada

Las capturas finales deben guardarse como:

- `exports/01_resumen_ejecutivo.png`
- `exports/02_actividad.png`
- `exports/03_sueno.png`
- `exports/04_segmentos_recomendaciones.png`
"""
    (DASHBOARD_DIR / "README.md").write_text(dashboard_readme, encoding="utf-8")


def write_dashboard_guide() -> None:
    guide = """# Guía para construir el dashboard en Power BI

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
"""
    (DASHBOARD_DIR / "guia_dashboard_powerbi.md").write_text(guide, encoding="utf-8")


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    analysis, users = load_data()
    metrics = build_metrics(analysis, users)
    create_visualizations(analysis, users, metrics)
    write_analysis_report(metrics)
    write_case_study(metrics)
    write_dashboard_readme()
    write_dashboard_guide()

    print("Analyzed Fitbit data successfully.")
    print(f"Users={metrics['users']:,}, records={metrics['records']:,}, avg_steps={metrics['avg_steps']:,.0f}")


if __name__ == "__main__":
    main()
