import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd
from sklearn.decomposition import PCA
from matplotlib.patches import Patch
from pathlib import Path
import numpy as np

# KONFIGURASI WARNA & LABEL (Pusat Kontrol)
RISK_CONFIG = {
    'High':   {'color': '#FF0000', 'label': 'RISIKO TINGGI (Prioritas)'}, # Merah
    'Medium': {'color': '#FFD700', 'label': 'RISIKO SEDANG (Waspada)'},   # Emas/Kuning
    'Low':    {'color': '#228B22', 'label': 'RISIKO RENDAH (Monitor)'}     # Hijau Hutan
}

def get_risk_levels(df, col_cluster):
    """
    Menentukan mana cluster High, Medium, Low berdasarkan rata-rata kerusakan.
    """
    col_damage = next((c for c in df.columns if 'rumah' in c or 'damage' in c), None)
    if not col_damage: return {}, None

    df_clean = df.dropna(subset=[col_cluster])
    if df_clean.empty: return {}, None
    
    stats = df_clean.groupby(col_cluster)[col_damage].mean().sort_values(ascending=False)
    clusters_ordered = stats.index.tolist()
    
    risk_map = {}
    if len(clusters_ordered) >= 3:
        risk_map[clusters_ordered[0]] = 'High'
        risk_map[clusters_ordered[1]] = 'Medium'
        for c in clusters_ordered[2:]: risk_map[c] = 'Low'
    elif len(clusters_ordered) == 2:
        risk_map[clusters_ordered[0]] = 'High'
        risk_map[clusters_ordered[1]] = 'Low'
    else:
        risk_map[clusters_ordered[0]] = 'High'
        
    return risk_map, col_damage

def plot_map(gdf, out_path, col_cluster, title_suffix):
    print("[VIZ] Rendering Map (Final)...")
    fig, ax = plt.subplots(figsize=(14, 10))
    
    risk_map, col_damage = get_risk_levels(gdf, col_cluster)
    
    gdf['color_hex'] = '#d3d3d3'
    for cluster_id, level in risk_map.items():
        gdf.loc[gdf[col_cluster] == cluster_id, 'color_hex'] = RISK_CONFIG[level]['color']
        
    gdf.plot(
        color=gdf['color_hex'],
        linewidth=0.8,
        edgecolor='black',
        ax=ax
    )
    
    legend_elements = []
    present_levels = set(risk_map.values())
    
    for level in ['High', 'Medium', 'Low']:
        if level in present_levels:
            info = RISK_CONFIG[level]
            patch = Patch(facecolor=info['color'], edgecolor='black', label=info['label'])
            legend_elements.append(patch)
            
    if (gdf['color_hex'] == '#d3d3d3').any():
        legend_elements.append(Patch(facecolor='#d3d3d3', edgecolor='black', label='Data Tidak Lengkap'))

    ax.legend(handles=legend_elements, loc='upper right', title="TINGKAT RISIKO", fontsize=10)
    ax.set_title(f"Peta Risiko Bencana: {title_suffix}", fontsize=16, fontweight='bold')
    ax.set_axis_off()
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f" Map saved: {out_path.name}")

def plot_pca(X_scaled, labels, out_path, df_original=None):
    print("[VIZ] Rendering PCA Plot (Legend Outside)...")
    
    # 1. Hitung PCA
    pca = PCA(n_components=2)
    comps = pca.fit_transform(X_scaled)
    df_pca = pd.DataFrame(comps, columns=['PC1', 'PC2'])
    
    # 2. Siapkan Label & Warna
    df_pca['Risk_Label'] = "Unknown"
    palette_dict = {}
    
    if df_original is not None:
        risk_map, _ = get_risk_levels(df_original, 'cluster_label')
        label_mapping = {}
        for c_id, level in risk_map.items():
            label_text = RISK_CONFIG[level]['label']
            label_mapping[c_id] = label_text
            palette_dict[label_text] = RISK_CONFIG[level]['color']
            
        pca_labels = []
        for l in labels:
            pca_labels.append(label_mapping.get(l, "Unknown"))
        df_pca['Risk_Label'] = pca_labels

    # 3. Plotting (Ukuran Figure Diperlebar agar muat legend)
    plt.figure(figsize=(13, 8))
    
    sns.scatterplot(
        x='PC1', y='PC2', 
        hue='Risk_Label',
        data=df_pca, 
        palette=palette_dict,
        s=200, 
        edgecolor='black', 
        alpha=0.9
    )
    
    plt.title('Validasi Cluster (PCA Projection)', fontsize=14, fontweight='bold')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # === PERBAIKAN DI SINI ===
    # bbox_to_anchor=(1.02, 1): Geser legend ke KANAN LUAR grafik
    # borderaxespad=0: Hilangkan jarak padding aneh
    plt.legend(
        title="PROFIL RISIKO", 
        bbox_to_anchor=(1.02, 1), 
        loc='upper left', 
        borderaxespad=0,
        frameon=True,
        fontsize=10
    )
    
    # Tight Layout wajib biar gambar gak kepotong saat disimpan
    plt.tight_layout()
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # bbox_inches='tight' adalah pengaman ganda biar legend luar tetap masuk frame
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"PCA saved: {out_path.name}")