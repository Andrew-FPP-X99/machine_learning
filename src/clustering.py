import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from typing import Tuple, List

def run_kmeans(df: pd.DataFrame, features: List[str], n_clusters: int = 3) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Executes K-Means and returns result DF + Scaled Data."""
    print(f"[ML] Running K-Means (k={n_clusters})...")
    
    # Validate columns
    available_feats = [f for f in features if f in df.columns]
    if not available_feats:
        raise ValueError("No matching feature columns found.")

    # Preprocessing
    X = df[available_feats].fillna(0)
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=available_feats)

    # Modeling
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = model.fit_predict(X_scaled)

    # Result construction
    df_out = df.copy()
    df_out['cluster_label'] = labels
    
    return df_out, X_scaled