"""Stage 2 EDA report generator.

Reads the six EDA query CSVs produced by stage2.sh (output/q1.csv ...
output/q6.csv) and produces:
  - One PNG chart per insight under output/charts/
  - One narrative markdown report at output/stage2_eda_report.md

The report ties each insight to its query, chart, and a 2-4 sentence
business-stakeholder story (course rubric: each insight = query + chart +
story of the data).

Runs on the headless cluster gateway, so matplotlib is forced to the Agg
backend before pyplot is imported.
"""
import os

import matplotlib

matplotlib.use("Agg")
# pylint: disable=wrong-import-position
import matplotlib.pyplot as plt
import pandas as pd


OUTPUT_DIR = "output"
CHARTS_DIR = os.path.join(OUTPUT_DIR, "charts")
REPORT_PATH = os.path.join(OUTPUT_DIR, "stage2_eda_report.md")
DPI = 150


WEEKDAY_ORDER = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]


def render_q1(df, out_dir):
    """Monthly trip counts across 2023 (line chart)."""
    df = df.sort_values("year_month").reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["year_month"], df["trip_count"], marker="o", linewidth=2)
    ax.set_title("Citi Bike trips per month (2023)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Trip count")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    path = os.path.join(out_dir, "q1_monthly_trips.png")
    plt.savefig(path, dpi=DPI)
    plt.close(fig)
    return path


def render_q2(df, out_dir):
    """Trip distribution by day of week (vertical bar)."""
    df = df.set_index("weekday_name").reindex(WEEKDAY_ORDER).reset_index()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(df["weekday_name"], df["trip_count"], color="#2c7fb8")
    ax.set_title("Citi Bike trips by day of week (2023)")
    ax.set_xlabel("Day of week")
    ax.set_ylabel("Trip count")
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    path = os.path.join(out_dir, "q2_weekday_distribution.png")
    plt.savefig(path, dpi=DPI)
    plt.close(fig)
    return path


def render_q3(df, out_dir):
    """Hourly trip count (bar) overlaid with average duration (line)."""
    df = df.sort_values("ride_hour").reset_index(drop=True)
    fig, ax_count = plt.subplots(figsize=(10, 5))
    ax_count.bar(df["ride_hour"], df["trip_count"], color="#41b6c4", alpha=0.7,
                 label="Trip count")
    ax_count.set_xlabel("Hour of day")
    ax_count.set_ylabel("Trip count", color="#1d6f7a")
    ax_count.tick_params(axis="y", labelcolor="#1d6f7a")
    ax_count.set_xticks(df["ride_hour"])

    ax_dur = ax_count.twinx()
    ax_dur.plot(df["ride_hour"], df["avg_ride_duration_minutes"],
                marker="o", color="#e34a33", linewidth=2,
                label="Avg duration (min)")
    ax_dur.set_ylabel("Average ride duration (minutes)", color="#a32c1f")
    ax_dur.tick_params(axis="y", labelcolor="#a32c1f")

    ax_count.set_title(
        "Citi Bike hourly trip volume vs. average ride duration"
    )
    ax_count.grid(True, axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    path = os.path.join(out_dir, "q3_hourly_trips_duration.png")
    plt.savefig(path, dpi=DPI)
    plt.close(fig)
    return path


def render_q4(df, out_dir):
    """Member vs casual: share (pie) + average duration comparison (bar)."""
    fig, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(11, 5))

    ax_pie.pie(
        df["trip_count"],
        labels=df["rider_type"],
        autopct="%1.1f%%",
        colors=["#2c7fb8", "#fdae61", "#888888"][: len(df)],
        startangle=90,
    )
    ax_pie.set_title("Share of trips: member vs casual")

    ax_bar.bar(df["rider_type"], df["avg_ride_duration_minutes"],
               color=["#2c7fb8", "#fdae61", "#888888"][: len(df)])
    ax_bar.set_title("Average ride duration by rider type")
    ax_bar.set_xlabel("Rider type")
    ax_bar.set_ylabel("Average duration (minutes)")
    ax_bar.grid(True, axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    path = os.path.join(out_dir, "q4_member_vs_casual.png")
    plt.savefig(path, dpi=DPI)
    plt.close(fig)
    return path


def render_q5(df, out_dir):
    """Top 20 start stations by trip count (horizontal bar)."""
    df = df.sort_values("trip_count").reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(df["start_station_name"], df["trip_count"], color="#2c7fb8")
    ax.set_title("Top 20 Citi Bike start stations by trip count (2023)")
    ax.set_xlabel("Trip count")
    ax.set_ylabel("Start station")
    ax.grid(True, axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()
    path = os.path.join(out_dir, "q5_top20_stations.png")
    plt.savefig(path, dpi=DPI)
    plt.close(fig)
    return path


def render_q6(df, out_dir):
    """Rideable type usage: trip count (bar) + avg duration (line)."""
    fig, ax_count = plt.subplots(figsize=(8, 5))
    ax_count.bar(df["rideable_type"], df["trip_count"], color="#41b6c4",
                 alpha=0.7, label="Trip count")
    ax_count.set_xlabel("Rideable type")
    ax_count.set_ylabel("Trip count", color="#1d6f7a")
    ax_count.tick_params(axis="y", labelcolor="#1d6f7a")

    ax_dur = ax_count.twinx()
    ax_dur.plot(df["rideable_type"], df["avg_ride_duration_minutes"],
                marker="o", color="#e34a33", linewidth=2,
                label="Avg duration (min)")
    ax_dur.set_ylabel("Average ride duration (minutes)", color="#a32c1f")
    ax_dur.tick_params(axis="y", labelcolor="#a32c1f")

    ax_count.set_title("Trip count and average duration by rideable type")
    ax_count.grid(True, axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    path = os.path.join(out_dir, "q6_rideable_types.png")
    plt.savefig(path, dpi=DPI)
    plt.close(fig)
    return path


INSIGHTS = [
    {
        "id": "q1",
        "title": "Seasonal demand: monthly trip volume",
        "csv": "q1.csv",
        "render": render_q1,
        "summary": (
            "GROUP BY ride_year, ride_month over citibike_trips_optimized; "
            "ordered chronologically."
        ),
        "story": (
            "Winter months (January and February) show the lowest volume, "
            "consistent with cold-weather behaviour, while most other months "
            "sit close to the dataset's per-month cap of around one million "
            "rides. Two months (June and September) stand out as much lower "
            "than their neighbours, suggesting a sampling gap in the "
            "underlying monthly archives rather than a real demand drop. "
            "For operations, the cold-weather dip is the only robust signal "
            "to plan capacity around; the June and September outliers are a "
            "data-quality flag to investigate before drawing seasonal "
            "conclusions."
        ),
    },
    {
        "id": "q2",
        "title": "Weekly rhythm: trips by day of week",
        "csv": "q2.csv",
        "render": render_q2,
        "summary": (
            "GROUP BY ride_weekday with weekday names; ordered Monday-Sunday."
        ),
        "story": (
            "Weekday usage dominates volume, consistent with commuter "
            "behaviour, while weekend volumes are typically lower but skew "
            "toward longer leisure trips. Marketing campaigns and promo "
            "pricing should differentiate commuter weekdays from leisure "
            "weekends to capture the right intent at the right time."
        ),
    },
    {
        "id": "q3",
        "title": "Daily rhythm: hourly volume vs. ride length",
        "csv": "q3.csv",
        "render": render_q3,
        "summary": (
            "GROUP BY ride_hour returning trip count and average duration."
        ),
        "story": (
            "Two pronounced rush hours - morning and evening - dominate the "
            "day, while average ride duration is often longer outside those "
            "peaks (leisure trips). The combined view tells operations not "
            "just when to rebalance bikes but also that midday rebalancing "
            "must account for longer trip times pulling bikes off the grid."
        ),
    },
    {
        "id": "q4",
        "title": "Customer mix: members vs casuals",
        "csv": "q4.csv",
        "render": render_q4,
        "summary": (
            "GROUP BY member_casual returning trip share and average "
            "duration."
        ),
        "story": (
            "Members account for the majority of trips, but casual riders "
            "consistently take longer trips on average. That mix matters for "
            "revenue: members drive volume and predictability while casuals "
            "drive per-trip revenue and tourist-area utilisation, suggesting "
            "different retention strategies for each segment."
        ),
    },
    {
        "id": "q5",
        "title": "Spatial demand: top 20 start stations",
        "csv": "q5.csv",
        "render": render_q5,
        "summary": (
            "GROUP BY start_station_id, start_station_name; LIMIT 20 by "
            "trip count."
        ),
        "story": (
            "Demand is concentrated in a small number of stations, "
            "predominantly in midtown and lower Manhattan transit hubs. "
            "These hot spots should be the focus of capacity expansion, "
            "preventive maintenance, and the rebalancing fleet's first "
            "stops of every shift."
        ),
    },
    {
        "id": "q6",
        "title": "Fleet mix: rideable type usage and duration",
        "csv": "q6.csv",
        "render": render_q6,
        "summary": (
            "GROUP BY rideable_type returning trip count and average "
            "duration."
        ),
        "story": (
            "Classic and electric bikes dominate the trip mix; electric "
            "bikes typically support shorter or faster trips while classic "
            "bikes carry the bulk of volume. Future fleet investment should "
            "weigh marginal demand for e-bikes against their higher unit "
            "and maintenance cost implied by usage intensity."
        ),
    },
]


def build_report(records):
    """Assemble the markdown narrative from per-insight render results."""
    lines = [
        "# Stage 2 EDA Report",
        "",
        "Six insights into the 2023 Citi Bike trip dataset, drawn from the "
        "Hive table `team19_projectdb.citibike_trips_optimized`. Each "
        "insight pairs its HiveQL summary with a chart and a short "
        "business-stakeholder story.",
        "",
    ]
    for index, record in enumerate(records, start=1):
        chart_rel = os.path.relpath(record["chart"], OUTPUT_DIR)
        chart_rel = chart_rel.replace(os.sep, "/")
        lines.extend([
            "## Insight {}: {}".format(index, record["title"]),
            "",
            "**Query:** {}".format(record["summary"]),
            "",
            "![{}]({})".format(record["title"], chart_rel),
            "",
            "**Story.** {}".format(record["story"]),
            "",
        ])
    return "\n".join(lines)


def main():
    if not os.path.isdir(OUTPUT_DIR):
        raise SystemExit(
            "Missing output/ directory; run scripts/stage2.sh first."
        )
    if not os.path.isdir(CHARTS_DIR):
        os.makedirs(CHARTS_DIR, exist_ok=True)

    records = []
    for insight in INSIGHTS:
        csv_path = os.path.join(OUTPUT_DIR, insight["csv"])
        if not os.path.isfile(csv_path):
            raise SystemExit("Missing input CSV: " + csv_path)
        df = pd.read_csv(csv_path)
        if df.empty:
            raise SystemExit(
                "Empty input CSV: " + csv_path
                + " (Stage 2 Hive queries returned no rows)"
            )
        chart_path = insight["render"](df, CHARTS_DIR)
        print("Rendered " + chart_path)
        records.append({
            "title": insight["title"],
            "summary": insight["summary"],
            "story": insight["story"],
            "chart": chart_path,
        })

    report = build_report(records)
    with open(REPORT_PATH, "w", encoding="utf-8") as fh:
        fh.write(report)
    print("Wrote " + REPORT_PATH)


if __name__ == "__main__":
    main()
