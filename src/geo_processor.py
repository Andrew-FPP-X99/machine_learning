import pandas as pd
import geopandas as gpd

def normalize_key(text: str) -> str:
    """
    Membersihkan nama kota dengan LOGIKA KHUSUS untuk menangani
    perbedaan penamaan di GADM (Depok, Cimahi, Banjar).
    """
    if pd.isna(text): return ""
    text = str(text).upper()
    
    # 1. Standarisasi Dasar
    # Hapus Kabupaten/Adm, tapi BIARKAN 'KOTA' dulu
    text = text.replace("KABUPATEN", "").replace("KAB.", "").replace("ADM.", "")
    text = text.replace(" ", "") # Hapus spasi (Bandung Barat -> BANDUNGBARAT)
    
    text = text.strip()

    # 2. FIX ANOMALI (Kamus Perbaikan)
    # Ubah "KOTADEPOK" jadi "DEPOK" agar cocok dengan peta
    if text == "KOTADEPOK":  return "DEPOK"
    if text == "KOTACIMAHI": return "CIMAHI"
    if text == "KOTABANJAR": return "BANJAR"
    
    return text

def process_spatial_join(gdf: gpd.GeoDataFrame, df: pd.DataFrame, target_prov: str, col_city: str) -> gpd.GeoDataFrame:
    print(f"[GIS] Filtering Map ({target_prov})...")
    
    # 1. Filter Province
    prov_col = 'NAME_1' if 'NAME_1' in gdf.columns else gdf.columns[0]
    is_match = gdf[prov_col].astype(str).str.upper().str.contains(target_prov.upper(), na=False)
    gdf_prov = gdf[is_match].copy()
    
    if gdf_prov.empty:
        raise ValueError(f"Provinsi '{target_prov}' tidak ditemukan!")

    # 2. Normalisasi Key
    gdf_prov['join_key'] = gdf_prov['NAME_2'].apply(normalize_key)
    df['join_key'] = df[col_city].apply(normalize_key)

    # 3. Join Data
    merged = gdf_prov.merge(df, on='join_key', how='left')
    
    # Cek Pangandaran (Info untuk User)
    if "PANGANDARAN" in df['join_key'].values and "PANGANDARAN" not in gdf_prov['join_key'].values:
        print("\n[INFO PENTING] Wilayah 'PANGANDARAN' tidak terpisah di file Peta ini.")
        print("       Data Pangandaran akan ikut area 'CIAMIS' (Induk Semang).")

    # 4. Simplify (Optimasi biar gak berat)
    print(f"[GIS] Menyederhanakan geometri...")
    merged['geometry'] = merged.simplify(tolerance=0.005, preserve_topology=True)
    
    return merged