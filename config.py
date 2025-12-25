from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dataset"
OUT_DIR  = BASE_DIR / "output"

FILE_GEOJSON = DATA_DIR / "gadm41_IDN_4.json"
FILE_CSV     = DATA_DIR / "data_agregat_bencana.csv"

IMG_MAP = OUT_DIR / "peta_risiko_final.png"
IMG_PCA = OUT_DIR / "plot_pca_cluster.png"

# Analysis Parameters
TARGET_PROV = "JawaBarat"
COL_CITY    = "nama_kabupaten_kota"
COL_CLUSTER = "cluster_label"
N_CLUSTERS  = 3

# Features to use for Clustering (Must exist in Aggregated CSV)
# Sesuaikan nama dengan hasil output aggregator.py
FEATURES = [
    "risiko_indeks_risiko_bencana",
    "banjir_jumlah_banjir",
    "gempa_jumlah_gempa_bumi",
    "longsor_jumlah_tanah_longsor",
    "cuaca_jumlah_kerusakan",
    "rumah_jumlah_kerusakan"
]