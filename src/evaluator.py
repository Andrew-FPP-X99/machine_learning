import pandas as pd
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

def calculate_metrics(X_scaled: pd.DataFrame, labels: pd.Series):
    """Prints validation metrics."""
    print("\n--- Model Evaluation ---")
    if len(set(labels)) < 2:
        print(" Not enough clusters for evaluation.")
        return

    sil = silhouette_score(X_scaled, labels)
    db = davies_bouldin_score(X_scaled, labels)
    ch = calinski_harabasz_score(X_scaled, labels)

    print(f"🔹 Silhouette Score     : {sil:.4f} (>0.5 is good)")
    print(f"🔹 Davies-Bouldin Idx   : {db:.4f} (Lower is better)")
    print(f"🔹 Calinski-Harabasz    : {ch:.4f} (Higher is better)")

def print_insights(df: pd.DataFrame, col_cluster: str, features: list):
    """Generates simple business insights."""
    print("\n--- Cluster Profiles ---")
    summary = df.groupby(col_cluster)[features].mean()
    print(summary.round(2))
    
    print("\n Recommendation Logic:")
    global_mean = summary.mean().mean()
    for cid, row in summary.iterrows():
        risk_level = "HIGH" if row.mean() > global_mean else "LOW/MEDIUM"
        print(f"   Cluster {cid}: {risk_level} Risk Profile -> {'Prioritize Mitigation' if risk_level == 'HIGH' else 'Maintain Monitoring'}")