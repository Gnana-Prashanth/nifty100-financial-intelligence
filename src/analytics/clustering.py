import pandas as pd
import matplotlib.pyplot as plt
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

for cid in sorted(latest["cluster_id"].unique()):
    print(f"\nCluster {cid}")
    print(
        latest.loc[
            latest["cluster_id"] == cid,
            "company_id"
        ].tolist()
    )