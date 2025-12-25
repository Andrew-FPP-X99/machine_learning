import pandas as pd
import geopandas as gpd
from pathlib import Path
from typing import Tuple

# KAMUS KODE WILAYAH JABAR (Fix Data Angka)
KODE_BPS_JABAR = {
    3201: "KABUPATEN BOGOR",
    3202: "KABUPATEN SUKABUMI",
    3203: "KABUPATEN CIANJUR",
    3204: "KABUPATEN BANDUNG",
    3205: "KABUPATEN GARUT",
    3206: "KABUPATEN TASIKMALAYA",
    3207: "KABUPATEN CIAMIS",
    3208: "KABUPATEN KUNINGAN",
    3209: "KABUPATEN CIREBON",
    3210: "KABUPATEN MAJALENGKA",
    3211: "KABUPATEN SUMEDANG",
    3212: "KABUPATEN INDRAMAYU",
    3213: "KABUPATEN SUBANG",
    3214: "KABUPATEN PURWAKARTA",
    3215: "KABUPATEN KARAWANG",
    3216: "KABUPATEN BEKASI",
    3217: "KABUPATEN BANDUNG BARAT",
    3218: "KABUPATEN PANGANDARAN",
    3271: "KOTA BOGOR",
    3272: "KOTA SUKABUMI",
    3273: "KOTA BANDUNG",
    3274: "KOTA CIREBON",
    3275: "KOTA BEKASI",
    3276: "KOTA DEPOK",
    3277: "KOTA CIMAHI",
    3278: "KOTA TASIKMALAYA",
    3279: "KOTA BANJAR"
}

def load_data(csv_path: Path, geo_path: Path) -> Tuple[pd.DataFrame, gpd.GeoDataFrame]:
    """Loads CSV and GeoJSON with validation & Code Mapping."""
    print(f"[IO] Loading datasets...")
    
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing CSV: {csv_path}")
    if not geo_path.exists():
        raise FileNotFoundError(f"Missing GeoJSON: {geo_path}")

    # 1. Baca CSV
    df = pd.read_csv(csv_path)
    
    # 2. FIX: Konversi Kode Angka ke Nama Kota (Jika perlu)
    col_nama = "nama_kabupaten_kota"
    if col_nama in df.columns:
        # Cek apakah isinya angka (integer/float)
        if pd.api.types.is_numeric_dtype(df[col_nama]):
            print("[INFO] Mendeteksi Kode Wilayah Angka, melakukan konversi ke Nama Kota...")
            df[col_nama] = df[col_nama].map(KODE_BPS_JABAR)
            # Isi yang tidak dikenal dengan string kosong agar tidak error
            df[col_nama] = df[col_nama].fillna("")

    # 3. Baca GeoJSON
    try:
        gdf = gpd.read_file(geo_path, engine="pyogrio")
    except Exception:
        gdf = gpd.read_file(geo_path)
        
    return df, gdf