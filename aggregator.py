import pandas as pd
from pathlib import Path
from typing import Optional

# Config
DATA_DIR = Path(__file__).parent / "dataset"
OUTPUT_FILE = DATA_DIR / "data_agregat_bencana.csv"

RAW_FILES = {
    "risiko": "indeks_risiko.csv",
    "banjir": "banjir.csv",
    "gempa": "gempa.csv",
    "longsor": "longsor.csv",
    "cuaca": "cuaca_ekstrem.csv",
    "rumah": "kerusakan_rumah.csv"
}

def clean_key(text: Optional[str]) -> Optional[str]:
    if pd.isna(text): return None
    text = str(text).upper()
    for w in ["KABUPATEN", "KOTA", "KAB.", "ADM."]:
        text = text.replace(w, "")
    return text.strip()

def run_aggregation():
    print("--- [AGGREGATOR] Processing Raw Data ---")
    dfs = []

    for category, filename in RAW_FILES.items():
        fpath = DATA_DIR / filename
        if not fpath.exists():
            print(f"  Skipping missing file: {filename}")
            continue

        df = pd.read_csv(fpath)
        # Detect city column
        col_city = next((c for c in df.columns if 'nama_kab' in c.lower() or 'kota' in c.lower()), None)
        if not col_city: continue

        # Normalize & Select Numeric
        df['key'] = df[col_city].apply(clean_key)
        numeric_cols = [c for c in df.select_dtypes('number').columns if 'tahun' not in c.lower() and 'kode' not in c.lower()]
        
        # Rename & Aggregate
        df_clean = df[['key'] + numeric_cols].rename(columns={c: f"{category}_{c}" for c in numeric_cols})
        df_clean = df_clean.groupby('key').sum().reset_index()
        dfs.append(df_clean)

    if not dfs: return

    # Merge All
    df_final = dfs[0]
    for df in dfs[1:]:
        df_final = pd.merge(df_final, df, on='key', how='outer')

    df_final.fillna(0, inplace=True)
    df_final.insert(0, 'nama_kabupaten_kota', df_final['key']) # Restore readable name
    df_final.drop(columns=['key'], inplace=True)
    
    df_final.to_csv(OUTPUT_FILE, index=False)
    print(f" Aggregation complete: {OUTPUT_FILE} ({len(df_final)} rows)")

if __name__ == "__main__":
    run_aggregation()