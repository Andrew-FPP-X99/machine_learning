# Implementasi Pengelompokan Data Bencana Alam Jawa Barat menggunakan _K-Means Clustering_

Dokumentasi dari Implementasi _K-Means Clustering_ untuk Mengelompokkan Daerah dengan Ukuran Tingkat Risiko di Peta Jawa Barat, ini terdiri dari 5 tahap. Berikut ini penjelasan untuk masing-masing tahapnya.

## **TAHAP 1: Pengumpulan Dataset (Data Collection)**

Data dari Open Data Jabar. Unduh file-file berikut:

**A. Download Data (Format CSV/Excel):**
1. **Indeks Risiko Bencana:** Rename jadi: indeks_risiko.csv
2. **Kejadian Banjir:** Rename jadi: banjir.csv
3. **Kejadian Gempa:** Rename jadi: gempa.csv
4. **Kejadian Longsor:** Rename jadi: longsor.csv
5. **Cuaca Ekstrem:** Rename jadi: cuaca_ekstrem.csv
6. **Kerusakan Rumah:** Rename jadi: kerusakan_rumah.csv
7. **Peta GeoJSON:** File gadm41_IDN_4.json yang dimiliki.

**B. Penggabungan Data (PENTING !!):**
gabungkan menjadi satu file bernama data_agregat_bencana.csv.
    > _Caranya_: Bisa pakai Excel (VLOOKUP berdasarkan nama Kota/Kab) atau pakai Python (Pandas Merge).
    > _Hasil Akhir_: File CSv dengan kolom: nama_kabupaten_kota, indeks_risiko, jml_banjir, jml_gempa, jml_longsor, jml_rusak_berat, dll.

## **TAHAP 2: Struktur Kode Modular (Architecture)**

```text
tugas_besar_bencana/
│
├── dataset/            # Simpan 7 file download tadi disini
│ │
│ ├── gadm41_IDN_4.json
│ │
│ └── data_agregat_bencana.csv  # (File gabungan yang siap di-cluster)
│
├── output/             # Folder kosong untuk hasil gambar
│
├── src/                # Source code utama
│ │
│ ├── __init__.py         # File kosong
│ ├── data_loader.py      # Membaca & membersihkan data
│ ├── clustering.py       # (BARU) Melakukan _k-means clustering_
│ ├── evaluator.py        # Menghitung Silhouette/Davies-Bouldin
│ ├── geo_processor.py    # Mengurus peta & spatial join
│ └── visualizer.py       # Membuat Peta & Plot PCA
│
├── config.py           # Pengaturan Path file
│
├── main.py             # File utama yang dijalankan
│
├── pyproject.toml      # config uv
│
└── README.md           # Dokumentasi Laporan
```

## **TAHAP 3: Implementasi Kode (Workflow)**
1. **config.py:** Definisikan lokasi file data_agregat_bencana.csv dan gadm41_IDN_4.json.
2. **src/data_loader.py:** Fungsi untuk load CSV & GeoJSON + Normalisasi nama kota (Hapus "Kab.", Uppercase)
3. **src/clustering.py:**
    > Ambil fitur angka (banjir, gempa, risiko).
    > Lakukan standardisasi (Scaler).
    > Jalankan **K-Means.**
    > Simpan label cluster ke kolom baru di DataFrame.
4. **src/evaluator.py:** Hitung skor Silhouette dan Davies-Bouldin dari hasil _K-Means_ tadi. Berikan rekomendasi prioritas mitigasi (Misal: Cluster 1 = Risiko Tinggi).
5. **src/visualizer.py:**
    > Fungsi plot_pca(): Gambar scatter plot 2D.
    > Fungsi generate_map(): Gambar peta Jabar warna-warni.
6. **main.py:** Panggil semua fungsi di atas secara berurutan.

## **TAHAP 4: Eksekusi & Tuning**

Perintah untuk mengeksekusi:    **uv run main.py**

**Cek Output:**
1. Apakah muncul angka **Silhouette Score** di terminal? (Target > 0.5 bagus, tapi > 0.3 sudah lumayan uuntuk data _real_).
2. Cek folder output/:
    > Apakah ada peta_risiko_jabar.png?
    > Apakah ada pca_cluster_plot.png?

_Jika hasil clusternya asing (misal Silhouette bernilai minus), coba ubah jumlah n-clusters di file clustering dari 3 menjadi 4 atau 2._

## **TAHAP 5: Dokumentasi (README.md)**

### **Analisis Mitigasi Bencana Jawa Barat Berbasis Machine Learning**
    Tugas Besar Analisis Big Data
    Proyek ini mengelompokkan (Clustering) Kabupaten/Kota di Jawa Barat berdasarkan riwayat bencana dan indeks risiko untuk menentukan prioritas mitigasi.
    
### **Fitur Utama**
Sesuai dengan spesifikasi tugas, sistem ini melakukan:
1. **Clustering K-Means:** Mengelompokkan wilayah menjadi 3 kategori (Risiko Tinggi, Sedang, Rendah).
2. **Evaluasi Model:** Menggunakan metrik _Silhouette Score_, _Davies-Bouldin Index_, dan _Calinski-Harabasz_.
3. **Visualisasi PCA:** Reduksi dimensi ke 2D plot untuk melihat penyebaran cluster.
4. **Peta Geospasial:** Visualisasi interaktif sebaran risiko di Peta Jawa Barat (Level Kabupaten/Kota).

### **Dataset**
Data bersumber dari **Open Data Jabar**, mencakup:
> Indeks Risiko Bencana
> Jumlah Kejadian Banjir, Gempa Bumi, Tanah Longsor, Cuaca Ekstrem
> Kerusakan Rumah (Berat/Sedang/Ringan)

### **Metodologi Evaluasi**
Kami menggunakan pendekatan kuantitatif untuk memvalidasi kualitas cluster:

|Metrik            |Fungsi             |Interpretasi|
|------------------|-------------------|------------|
|Silhouette Score  |Mengukur seberapa mirip objek dengan clusternya sendiri dibandingkan cluster lain. |Rentang -1 s.d. 1. Semakin mendekati 1 semakin baik (terpisah jelas) |
|Davies-Bouldin    |Mengukur rasio jarak dalam cluster dengan jarak atau cluster. |Semakin kecil (mendekati 0) semakin baik |
|Calinski-Harabasz |Mengukur dispersi antar cluster. |Semakin tinggi nilainya semakin baik |

### **Karakteristik Cluster & Prioritas Mitigasi**
Berdasarkan hasil analisis (Generate Insight), berikut adalah profil risiko:
#### 1.  **Cluster 0 (Risiko Rendah):**
    > _Karakteristik_: Indeks risiko rendah, kejadian bencana jarang.
    > _Mitigasi_: Edukasi rutin, pemeliharaan lingkungan standar.

#### 2.  **Cluster 1 (Risiko Sedang):**
    > _Karakteristik_: Frekuensi banjir musiman tinggi, kerusakan rumah sedang.
    > _Mitigasi_: Perbaikan drainase, penguatan tanggul sungai.

#### 3.  **Cluster 2 (Risiko Tinggi - Prioritas Utama):**
    > _Karakteristik_: Indeks risiko > 150, sering terjadi longsor & gempa, kerusakan rumah berat tinggi.
    > _Mitigasi_: Relokasi hunian rawan, pemasangan _Early Warning System_, alokasi dana darurat terbesar.

### **Cara Menjalankan Program**
#### 1. **Instalasi Dependensi**
Pastikan uv terinstall, lalu jalankan:
```bash
uv sync
```

#### 2. **Jalankan Analisis**
```bash
uv run main.py
```

#### 3. **Hasil Output**
Cek folder output/ untuk melihat:
a. peta_risiko_final.png (Visualisasi Data)
b. cluster_pca_plot.png (Visualisasi Sebaran Data 2D)
