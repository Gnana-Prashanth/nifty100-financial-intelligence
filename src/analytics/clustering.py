import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

BASE_DIR = Path(__file__).resolve().parents[2]

ratios = pd.read_excel(
    BASE_DIR / "data/supporting/financial_ratios.xlsx"
)

sectors = pd.read_excel(
    BASE_DIR / "data/supporting/sectors.xlsx"
)

ratios = ratios[
    ratios["year"] != "TTM"
]

latest = (
    ratios
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
    .reset_index(drop=True)
)

latest = latest.merge(
    sectors[
        ["company_id", "broad_sector"]
    ],
    on="company_id",
    how="left"
)


features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct"
]

for feature in features:

    latest[feature] = (

        latest
        .groupby("broad_sector")[feature]
        .transform(
            lambda x: x.fillna(x.median())
        )

    )

imputer = SimpleImputer(strategy="median")

latest[features] = imputer.fit_transform(
    latest[features]
)


scaler = StandardScaler()

X = scaler.fit_transform(
    latest[features]
)


inertia = []

for k in range(2, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X)

    inertia.append(model.inertia_)


reports_dir = BASE_DIR / "reports"
reports_dir.mkdir(exist_ok=True)

plt.figure(figsize=(6,4))

plt.plot(
    range(2,11),
    inertia,
    marker="o"
)

plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.title("Elbow Method")

plt.grid(True)

plt.savefig(
    reports_dir / "elbow_plot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

latest["cluster_id"] = kmeans.fit_predict(X)

# # Cluster profiling
# profile = (
#     latest
#     .groupby("cluster_id")[features]
#     .mean()
#     .round(2)
# )

# print("\nCluster Profile (Mean):")
# print(profile)


distances = kmeans.transform(X)

latest["distance_from_centroid"] = (

    distances.min(axis=1)

)


cluster_map = {
    0: "Financial & Leveraged Institutions",
    1: "Core Quality Businesses",
    2: "Defense High-ROE Outliers",
    3: "High-Margin Leaders",
    4: "Cash-Rich Outlier"
}

latest["cluster_name"] = latest["cluster_id"].map(cluster_map)

output = latest[
    [
        "company_id",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid"
    ]
]


output_dir = BASE_DIR / "output"
output_dir.mkdir(parents=True, exist_ok=True)

output.to_csv(
    output_dir / "cluster_labels.csv",
    index=False
)

## Companies in Each Cluster
# for cid in sorted(latest["cluster_id"].unique()):
#     print(f"\nCluster {cid}")
#     print(
#         latest.loc[
#             latest["cluster_id"] == cid,
#             "company_id"
#         ].tolist()
#     )


# ==========================================================
#                  Correlation Matrix
# ==========================================================

kpis = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "interest_coverage",
    "asset_turnover",
    "composite_quality_score"
]

corr = latest[kpis].corr(method="pearson")

plt.figure(figsize=(10,8))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5,
    square=True
)

plt.title("Correlation Matrix")

plt.savefig(
    BASE_DIR / "reports" / "correlation_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================================================
#                 Portfolio Statistics
# ==========================================================

stats = []

for metric in kpis:

    values = latest[metric].dropna()

    stats.append({

        "Metric": metric,

        "P10": values.quantile(0.10),

        "P25": values.quantile(0.25),

        "P50": values.quantile(0.50),

        "P75": values.quantile(0.75),

        "P90": values.quantile(0.90),

        "Mean": values.mean(),

        "Std": values.std()

    })

portfolio_stats = pd.DataFrame(stats)

output_dir = BASE_DIR / "output"
output_dir.mkdir(parents=True, exist_ok=True)

portfolio_stats.to_csv(
    output_dir / "portfolio_stats.csv",
    index=False
)

#print(portfolio_stats)


# ==========================================================
#                  Outlier Detection
# ==========================================================

outliers = []

for sector, group in latest.groupby("broad_sector"):

    for metric in kpis:

        mean = group[metric].mean()

        std = group[metric].std()

        if pd.isna(std) or std == 0:
            continue

        z_scores = (group[metric] - mean) / std

        flagged = group[abs(z_scores) > 3].copy()

        flagged["z_score"] = z_scores[abs(z_scores) > 3]

        for _, row in flagged.iterrows():

            outliers.append({
                "company_id": row["company_id"],
                "metric": metric,
                "value": row[metric],
                "z_score": row["z_score"],
                "sector": sector,
                "sector_mean": mean,
                "sector_std": std
            })

outlier_df = pd.DataFrame(outliers)

outlier_df = outlier_df.sort_values(
    by=["sector", "company_id", "metric"]
).reset_index(drop=True)

outlier_df.to_csv(
    BASE_DIR /
    "output" /
    "outlier_report.csv",
    index=False
            )

# print(outlier_df)
# print()
# print(f"Outliers Found: {len(outlier_df)}")