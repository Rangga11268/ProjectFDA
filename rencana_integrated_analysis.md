# Rencana Gabungkan Semua Bab (Bab 2, 3, 4) dalam Satu File

## Tujuan
Menggabungkan keseluruhan proses analisis data dalam satu jupyter notebook (.ipynb) dan satu file python (.py) untuk mempresentasikan alur kerja lengkap dari awal hingga akhir.

## Struktur File Gabungan

### BAB 2: DATA UNDERSTANDING
- Deskripsi dataset (jumlah baris, kolom, tipe data)
- Statistik deskriptif
- Pengecekan missing values
- Visualisasi awal (distribusi target, hubungan fitur)
- Identifikasi outlier dari Bab 2 (seperti yang disebutkan untuk Rainfall dan WindGustSpeed)

### BAB 3: DATA PREPARATION  
- Penanganan outlier (berdasarkan hasil Bab 2, namun Random Forest robust terhadap outlier)
- Transformasi variabel kategorikal (Label Encoding)
- Encoding variabel target (HujanBesok)
- Pembuatan fitur baru dari tanggal (Year, Month, Day)
- Data splitting (80% training, 20% testing)
- Penanganan class imbalance dengan SMOTE
- Penyimpanan dataset hasil preprocessing

### BAB 4: MODELLING
- Pemilihan dan inisialisasi model (Random Forest)
- Pelatihan model dengan data training
- Penerapan model pada data uji
- Prediksi awal

## File yang Akan Dibuat

### 1. integrated_analysis_notebook.ipynb
- Semua bagian Bab 2, 3, 4 digabung dalam satu notebook
- Struktur sesuai dengan outline di atas
- Penjelasan dalam bahasa Indonesia
- Visualisasi di setiap bagian

### 2. integrated_analysis_script.py  
- Implementasi yang sama dalam bentuk script Python
- Struktur komentar sesuai dengan BAB
- Tidak perlu visualisasi yang terlalu banyak, fokus pada eksekusi

## Catatan Penting
- Mengikuti pendekatan yang diajarkan di kampus (splitting dan SMOTE di Bab 3)
- Tidak ada duplikasi proses antar BAB
- Flow harus logis dari Bab 2 ke Bab 4
- Gunakan dataset dan fungsi yang sudah dibuat sebelumnya
- Pastikan komentar dalam bahasa Indonesia sesuai dengan struktur BAB