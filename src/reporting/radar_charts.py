import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("nifty100.db")

peer_percentiles = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    conn
)

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

# -----------------------------
# Output Folder
# -----------------------------
output_folder = "reports/radar_charts"
os.makedirs(output_folder, exist_ok=True)

# -----------------------------
# Radar Metrics
# -----------------------------
radar_metrics = [
    "ROE",
    "ROCE",
    "Net Profit Margin",
    "Debt to Equity",
    "Free Cash Flow",
    "PAT CAGR 5yr",
    "Revenue CAGR 5yr",
    "Composite Score"
]

# -----------------------------
# Companies
# -----------------------------
companies = financial_ratios["company_id"].unique()

for company in companies:

    print(f"Generating chart for {company}")

    company_years = financial_ratios[
        (financial_ratios["company_id"] == company) &
        (financial_ratios["year"] != "TTM")
    ].copy()

    if company_years.empty:
        print("Skipped (No historical data)")
        continue

    latest_year = company_years.iloc[-1]["year"]

    company_metrics = peer_percentiles[
        (peer_percentiles["company_id"] == company) &
        (peer_percentiles["year"] == latest_year)
    ].copy()

    company_metrics = company_metrics[
        company_metrics["metric"].isin(radar_metrics[:-1])
    ]

    if company_metrics.empty:

        print(f"No peer group for {company} - generating standalone chart")

        composite = financial_ratios[
            (financial_ratios["company_id"] == company) &
            (financial_ratios["year"] == latest_year)
        ][
            [
                "company_id",
                "year",
                "composite_quality_score"
            ]
        ].copy()

        if composite.empty:
            print("Skipped (No composite score)")
            continue

        company_score = composite.iloc[0]["composite_quality_score"]

        nifty_average = financial_ratios[
            financial_ratios["year"] == latest_year
        ]["composite_quality_score"].mean()

        labels = ["Composite Score"]

        company_values = [company_score]
        peer_values = [nifty_average]

        angles = [0, 0]

        fig = plt.figure(figsize=(6, 6))

        ax = plt.subplot(
            111,
            polar=True
        )

        ax.plot(
            angles,
            company_values * 2,
            linewidth=2,
            label=company
        )

        ax.scatter(
            angles[:1],
            company_values,
            s=60
        )

        ax.plot(
            angles,
            peer_values * 2,
            linestyle="--",
            linewidth=2,
            label="Nifty 100 Average"
        )

        ax.scatter(
            angles[:1],
            peer_values,
            s=60
        )

        ax.set_xticks([0])

        ax.set_xticklabels(labels)

        ax.set_ylim(0, 100)

        plt.title(f"{company} ({latest_year})")

        plt.legend(loc="upper right")

        plt.savefig(
            os.path.join(
                output_folder,
                f"{company}_radar.png"
            ),
            dpi=300,
            bbox_inches="tight"
        )

        plt.close(fig)

        continue

    peer_group = company_metrics.iloc[0]["peer_group"]

    composite = financial_ratios[
        (financial_ratios["company_id"] == company) &
        (financial_ratios["year"] == latest_year)
    ][
        [
            "company_id",
            "year",
            "composite_quality_score"
        ]
    ].copy()

    composite["peer_group"] = peer_group
    composite["metric"] = "Composite Score"
    composite["value"] = composite["composite_quality_score"]
    composite["percentile_rank"] = composite["composite_quality_score"]

    composite = composite[
        [
            "company_id",
            "peer_group",
            "year",
            "metric",
            "value",
            "percentile_rank"
        ]
    ]

    radar_data = pd.concat(
        [
            company_metrics,
            composite
        ],
        ignore_index=True
    )

    radar_data = radar_data.dropna(
        subset=["value", "percentile_rank"]
    ).reset_index(drop=True)

    if len(radar_data) < 3:
        print("Skipped (Insufficient metrics)")
        continue

    peer_average = (
        peer_percentiles[
            (peer_percentiles["peer_group"] == peer_group) &
            (peer_percentiles["year"] == latest_year) &
            (peer_percentiles["metric"].isin(radar_data["metric"]))
        ]
        .groupby("metric")["percentile_rank"]
        .mean()
        .reset_index()
    )

    peer_average = peer_average.merge(
        radar_data[["metric"]],
        on="metric",
        how="right"
    )

    peer_average["percentile_rank"] = peer_average[
        "percentile_rank"
    ].fillna(0)

    # -----------------------------
    # Prepare Radar Values
    # -----------------------------
    labels = radar_data["metric"].tolist()

    company_values = radar_data[
        "percentile_rank"
    ].tolist()

    peer_values = peer_average[
        "percentile_rank"
    ].tolist()

    num_metrics = len(labels)

    angles = np.linspace(
        0,
        2 * np.pi,
        num_metrics,
        endpoint=False
    ).tolist()

    company_values += company_values[:1]
    peer_values += peer_values[:1]
    angles += angles[:1]

    # -----------------------------
    # Create Radar Chart
    # -----------------------------
    fig = plt.figure(figsize=(8, 8))

    ax = plt.subplot(
        111,
        polar=True
    )

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(
        labels,
        fontsize=9
    )

    ax.set_ylim(0, 100)

    ax.set_yticks([20, 40, 60, 80, 100])

    ax.set_yticklabels(
        ["20", "40", "60", "80", "100"],
        fontsize=8
    )

    # -----------------------------
    # Company Plot
    # -----------------------------
    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label=company
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25
    )

    # -----------------------------
    # Peer Average Plot
    # -----------------------------
    ax.plot(
        angles,
        peer_values,
        linestyle="--",
        linewidth=2,
        label="Peer Average"
    )

    # -----------------------------
    # Title & Legend
    # -----------------------------
    plt.title(
        f"{company} ({latest_year})",
        fontsize=13,
        pad=20
    )

    plt.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 1.15)
    )

    plt.tight_layout()

    # -----------------------------
    # Save Chart
    # -----------------------------
    output_path = os.path.join(
        output_folder,
        f"{company}_radar.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Saved -> {output_path}")

# -----------------------------
# Close Database
# -----------------------------
conn.close()

print("\n" + "=" * 50)
print("All radar charts generated successfully!")
print("=" * 50)