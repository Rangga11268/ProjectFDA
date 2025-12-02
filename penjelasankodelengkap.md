Penjelasan Sintaks & Kode Lengkap: Project FDA Weather AUS

Dokumen ini dirancang sebagai Cheat Sheet untuk presentasi. Penjelasan disusun berdasarkan BAB yang ada di dalam Notebook ProjectFDAWeatherAUS.ipynb agar mudah diikuti saat presentasi.

---

BAB 1 & 2: DATA UNDERSTANDING

Tahap ini berfokus pada pemahaman awal terhadap data, meliputi pemuatan library, pemuatan data, dan eksplorasi statistik serta visualisasi.

1. Import Library & Konfigurasi

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)

# ... opsi display lainnya

Penjelasan Detail:

- pandas (pd): Library utama dalam Python yang digunakan untuk analisis dan manipulasi data. Pandas menyediakan struktur data yang disebut DataFrame, yang memungkinkan kita mengolah data berbentuk tabel (baris dan kolom) dengan sangat efisien.
- numpy (np): Library dasar untuk komputasi ilmiah. Numpy menyediakan dukungan untuk array multidimensi dan berbagai fungsi matematika tingkat lanjut yang dibutuhkan untuk operasi numerik yang cepat.
- matplotlib.pyplot (plt): Modul dari library Matplotlib yang digunakan sebagai dasar untuk membuat visualisasi data statis, seperti grafik garis, batang, dan histogram.
- seaborn (sns): Library visualisasi data yang dibangun di atas Matplotlib. Seaborn menyediakan antarmuka tingkat tinggi untuk menggambar grafik statistik yang lebih menarik dan informatif secara visual.
- pd.set_option: Fungsi ini digunakan untuk mengonfigurasi tampilan output Pandas. Parameter 'display.max_columns', None menginstruksikan Pandas untuk menampilkan seluruh kolom yang ada di DataFrame tanpa menyembunyikannya (tanpa menyingkat dengan tanda titik-titik), sehingga kita bisa melihat struktur data secara utuh.

2. Data Loading (Memuat Data)

data = pd.read_csv("weatherAUS.csv")
data.head()

Penjelasan Detail:

- pd.read_csv: Fungsi ini bertugas membaca file data dengan format CSV (Comma Separated Values) dari penyimpanan lokal dan memuatnya ke dalam memori komputer sebagai objek DataFrame Pandas. Fungsi ini secara otomatis mendeteksi pemisah kolom dan baris header.
- data.head(): Metode ini digunakan untuk menampilkan 5 baris pertama dari DataFrame. Tujuannya adalah untuk melakukan pemeriksaan cepat (sanity check) guna memastikan bahwa data telah berhasil dimuat dengan benar dan struktur kolomnya sesuai dengan yang diharapkan.

3. Cek Informasi Dasar & Statistik

data.info()
data.describe()

Penjelasan Detail:

- data.info(): Metode ini memberikan ringkasan teknis yang komprehensif tentang DataFrame. Informasi yang ditampilkan meliputi jumlah total baris (entries), daftar nama kolom, jumlah data yang tidak kosong (non-null) pada setiap kolom, dan tipe data (dtype) dari masing-masing kolom (misalnya float64 untuk angka desimal, object untuk teks/string). Ini langkah awal untuk mendeteksi masalah pada tipe data atau adanya nilai yang hilang.
- data.describe(): Metode ini menghasilkan ringkasan statistik deskriptif untuk semua kolom yang bertipe numerik. Outputnya mencakup nilai rata-rata (mean), standar deviasi (std), nilai minimum, nilai maksimum, serta kuartil (25%, 50%, 75%). Statistik ini sangat berguna untuk memahami distribusi data, pemusatan data, dan penyebaran data secara cepat.

4. Cek Missing Values

data.isnull().sum().sort_values(ascending=False)

Penjelasan Detail:

- data.isnull(): Metode ini memindai seluruh DataFrame dan menghasilkan DataFrame baru berisi nilai boolean (True/False). Nilai True menandakan bahwa data pada sel tersebut hilang atau bernilai NaN (Not a Number).
- .sum(): Metode ini menjumlahkan nilai True (yang dianggap bernilai 1) di setiap kolom. Hasilnya adalah jumlah total data yang hilang (missing values) untuk masing-masing variabel.
- .sort_values(ascending=False): Metode ini mengurutkan hasil penjumlahan missing values dari yang terbanyak ke yang paling sedikit. Langkah ini penting untuk memprioritaskan kolom mana yang memerlukan penanganan khusus, seperti penghapusan kolom atau pengisian nilai (imputasi).

5. Visualisasi Data (EDA)

a. Histogram (Distribusi Numerik)

data[['SuhuMin', 'SuhuMax']].hist(...)

- Tujuan Teknis: Untuk menganalisis distribusi frekuensi dari variabel numerik. Kita ingin melihat apakah data terdistribusi normal (berbentuk lonceng), menceng ke kiri/kanan (skewed), atau memiliki pola distribusi lain.
- Sintaks: Metode .hist() secara otomatis membagi rentang nilai data menjadi beberapa interval (bins) dan menghitung frekuensi data yang jatuh ke dalam setiap interval tersebut.

b. Boxplot (Deteksi Outlier)

sns.boxplot(x=data['CurahHujan'])

- Tujuan Teknis: Untuk mengidentifikasi outlier (pencilan) dan melihat sebaran data berdasarkan kuartil. Boxplot menampilkan 5 serangkai statistik: nilai minimum, kuartil bawah (Q1), median (Q2), kuartil atas (Q3), dan nilai maksimum.
- Interpretasi: Titik-titik data yang berada di luar "whiskers" (garis perpanjangan dari kotak) dikategorikan sebagai outlier secara statistik.
- Keputusan Proyek: Outlier pada variabel CurahHujan dan KecepatanAngin diputuskan untuk TIDAK dihapus. Hal ini karena dalam konteks data cuaca, nilai ekstrem tersebut merepresentasikan fenomena alam nyata (seperti badai) yang justru mengandung informasi penting untuk prediksi hujan.

c. Heatmap (Korelasi)

sns.heatmap(data.corr(), annot=True, ...)

- Tujuan Teknis: Untuk memvisualisasikan matriks korelasi antar variabel numerik. Matriks ini menunjukkan seberapa kuat hubungan linear antara satu variabel dengan variabel lainnya.
- Sintaks: data.corr() menghitung koefisien korelasi (biasanya Pearson). sns.heatmap kemudian memetakan nilai-nilai ini ke dalam spektrum warna.
- Temuan: Ditemukan korelasi positif yang kuat antara variabel target 'HujanBesok' dengan fitur-fitur seperti 'SinarMatahari' (korelasi negatif) dan 'KelembabanJam3' (korelasi positif), yang mengindikasikan fitur-fitur ini akan menjadi prediktor yang baik.

---

BAB 3: DATA PREPARATION

Tahap ini melibatkan transformasi data mentah menjadi format yang bersih dan terstruktur yang dapat diproses oleh algoritma Machine Learning.

1. Feature Engineering (Tanggal)

df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df['Year'] = df['Tanggal'].dt.year
df['Month'] = df['Tanggal'].dt.month
df['Day'] = df['Tanggal'].dt.day
df = df.drop('Tanggal', axis=1)

Penjelasan Detail:

- pd.to_datetime: Mengonversi kolom 'Tanggal' yang awalnya bertipe string (object) menjadi tipe data datetime64 khusus Pandas. Ini memungkinkan kita mengakses properti waktu.
- .dt accessor: Digunakan untuk mengekstrak komponen spesifik dari objek datetime. Kita memecah satu kolom tanggal menjadi tiga fitur numerik terpisah: Tahun, Bulan, dan Hari. Hal ini dilakukan agar model dapat mempelajari pola musiman (seasonality) yang terdapat pada data bulan dan tahun.
- .drop: Menghapus kolom 'Tanggal' asli dari DataFrame karena informasinya sudah direpresentasikan oleh tiga kolom baru tersebut, dan model tidak dapat memproses tipe data datetime mentah.

2. Encoding Variabel Kategorikal

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df[col] = le.fit_transform(df[col].astype(str))

Penjelasan Detail:

- LabelEncoder: Sebuah utilitas dari Scikit-Learn yang berfungsi untuk mengubah label kategori (teks) menjadi nilai numerik (integer). Algoritma Machine Learning matematis memerlukan input berupa angka.
- Proses: Metode .fit_transform() pertama-tama memetakan setiap kategori unik ke sebuah angka (misalnya: 'No' -> 0, 'Yes' -> 1), lalu mentransformasikan seluruh data di kolom tersebut menjadi angka yang sesuai. Ini diterapkan pada semua fitur kategorikal dan juga variabel target.

3. Splitting Data (Train/Test Split)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

Penjelasan Detail:

- train_test_split: Fungsi ini membagi dataset menjadi dua himpunan bagian yang saling lepas: Training Set (untuk melatih model) dan Testing Set (untuk evaluasi model).
- test_size=0.2: Menentukan bahwa 20% dari total data akan dialokasikan sebagai data uji, sedangkan 80% sisanya digunakan sebagai data latih.
- stratify=y: Parameter ini sangat krusial untuk dataset dengan kelas yang tidak seimbang. Stratify memastikan bahwa proporsi kelas target (Hujan vs Tidak Hujan) pada data latih dan data uji adalah sama persis dengan proporsi pada data asli. Ini mencegah bias evaluasi yang mungkin terjadi jika data uji kebetulan hanya berisi satu kelas saja.

4. Handling Imbalance Data (SMOTE)

from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

Penjelasan Detail:

- Masalah Imbalance: Dataset cuaca ini memiliki ketidakseimbangan kelas yang signifikan, di mana jumlah sampel 'Tidak Hujan' jauh lebih banyak daripada 'Hujan'. Model yang dilatih pada data seperti ini cenderung bias memprediksi kelas mayoritas.
- SMOTE (Synthetic Minority Over-sampling Technique): Teknik oversampling yang bekerja dengan cara membuat sampel sintetis (buatan) baru untuk kelas minoritas. Alih-alih hanya menduplikasi data lama, SMOTE menggunakan pendekatan k-Nearest Neighbors untuk menginterpolasi data baru di antara data minoritas yang sudah ada.
- Hasil: Menghasilkan dataset pelatihan baru (X_train_smote, y_train_smote) yang memiliki jumlah sampel seimbang antara kelas positif dan negatif, sehingga model dapat mempelajari karakteristik kedua kelas dengan sama baiknya.

---

BAB 4: MODELLING

Tahap ini adalah inti dari proses machine learning, di mana algoritma matematika diterapkan pada data latih untuk membangun model prediktif.

1. Inisialisasi Model

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(random_state=42)

Penjelasan Detail:

- RandomForestClassifier: Algoritma pembelajaran ensemble yang bekerja dengan cara membangun banyak pohon keputusan (Decision Trees) pada waktu pelatihan. Keputusan akhir diambil berdasarkan voting mayoritas dari seluruh pohon yang ada. Algoritma ini dipilih karena performanya yang stabil, kemampuannya menangani data non-linear, dan ketahanannya terhadap overfitting dibandingkan decision tree tunggal.
- random_state=42: Parameter ini digunakan untuk menginisialisasi generator angka acak. Tujuannya adalah untuk memastikan reprodusibilitas, yaitu agar setiap kali kode dijalankan, hasil inisialisasi model dan pembagian data internalnya tetap sama persis.

2. Pelatihan Model (Training)

model.fit(X_train_smote, y_train_smote)

Penjelasan Detail:

- model.fit(): Ini adalah metode utama untuk melatih model. Pada tahap ini, algoritma Random Forest memproses data fitur (X_train_smote) dan label target (y_train_smote).
- Proses Internal: Model akan mencari pola, aturan, dan hubungan matematis antara fitur input dan target output. Karena kita menggunakan data yang sudah diseimbangkan dengan SMOTE, model akan belajar untuk mengenali pola kelas 'Hujan' dan 'Tidak Hujan' tanpa bias ke salah satu kelas.

3. Prediksi

y_pred = model.predict(X_test)

Penjelasan Detail:

- model.predict(): Setelah model selesai dilatih, metode ini digunakan untuk melakukan prediksi pada data baru yang belum pernah dilihat sebelumnya (X_test).
- Output: Menghasilkan array berisi label prediksi (0 atau 1) untuk setiap baris data pada X_test. Hasil prediksi ini (y_pred) nantinya akan dibandingkan dengan label sebenarnya (y_test) untuk mengukur kinerja model.

---

BAB 5: EVALUASI

Tahap ini bertujuan untuk mengukur kinerja model secara objektif menggunakan berbagai metrik statistik.

1. Akurasi (Accuracy Score)

accuracy_score(y_test, y_pred)

- Definisi: Rasio jumlah prediksi yang benar (positif dan negatif) dibagi dengan total jumlah sampel data uji.
- Interpretasi: Hasil sekitar 84-85% menunjukkan tingkat kebenaran global model. Namun, pada kasus data tidak seimbang, akurasi saja tidak cukup karena bisa menjadi bias jika model hanya memprediksi kelas mayoritas. Oleh karena itu, diperlukan metrik tambahan.

2. Confusion Matrix

confusion_matrix(y_test, y_pred)

- Definisi: Tabel matriks yang merinci performa model klasifikasi. Matriks ini membagi hasil prediksi menjadi 4 kategori:
  - True Negative (TN): Model memprediksi Tidak Hujan, dan kenyataannya Tidak Hujan.
  - True Positive (TP): Model memprediksi Hujan, dan kenyataannya Hujan.
  - False Positive (FP): Model memprediksi Hujan, padahal kenyataannya Tidak Hujan (Kesalahan Tipe I).
  - False Negative (FN): Model memprediksi Tidak Hujan, padahal kenyataannya Hujan (Kesalahan Tipe II).
- Pentingnya: Membantu kita melihat jenis kesalahan mana yang lebih sering dilakukan oleh model.

3. Classification Report

classification_report(y_test, y_pred)

- Precision: Mengukur ketepatan model saat memprediksi kelas positif. Dari semua data yang diprediksi 'Hujan', berapa persen yang benar-benar hujan.
- Recall (Sensitivity): Mengukur kemampuan model dalam menemukan kembali informasi. Dari semua kejadian 'Hujan' yang sebenarnya terjadi, berapa persen yang berhasil dideteksi oleh model.
- F1-Score: Rata-rata harmonis dari Precision dan Recall. Metrik ini memberikan gambaran tunggal tentang keseimbangan performa model, sangat berguna ketika ada trade-off antara precision dan recall.

4. Feature Importance

model.feature*importances*

- Definisi: Atribut dari model Random Forest yang memberikan skor untuk setiap fitur input. Skor ini merepresentasikan seberapa besar kontribusi fitur tersebut dalam mengurangi ketidakmurnian (impurity) saat pembentukan pohon keputusan.
- Temuan Utama: Analisis menunjukkan bahwa fitur-fitur berikut memiliki pengaruh terbesar terhadap prediksi hujan:
  1. KecepatanAnginKencang (WindGustSpeed)
  2. SinarMatahari (Sunshine)
  3. AwanJam3 (Cloud3pm)
  4. CurahHujan (Rainfall)
  5. KelembabanJam3 (Humidity3pm)
- Kesimpulan Teknis: Model secara otomatis mengidentifikasi bahwa parameter fisik atmosfer seperti kelembaban, tutupan awan, dan dinamika angin adalah prediktor terkuat untuk kejadian hujan, yang sejalan dengan prinsip meteorologi.

---

PERTANYAAN DOSEN (Q&A)

Q: Mengapa pada tahap Evaluasi (Bab 5) kita menggunakan data X_test (Data Asli) dan bukan X_train_smote (Data SMOTE)?

A:
Ini adalah pertanyaan metodologi yang sangat penting. Jawabannya adalah karena kita ingin mengukur performa model pada kondisi dunia nyata (real-world scenario).

1. Tujuan SMOTE pada Training:
   Kita menggunakan SMOTE pada data latih (X_train) hanya untuk membantu model "belajar" dengan lebih adil. Jika kita melatih model dengan data yang tidak seimbang, model akan cenderung bias ke kelas mayoritas (Tidak Hujan). SMOTE menyeimbangkan "buku pelajaran" model sehingga ia bisa mengenali pola "Hujan" dan "Tidak Hujan" dengan sama baiknya.

2. Tujuan X_test pada Evaluasi:
   Data uji (X_test) adalah representasi dari data baru yang akan ditemui model di lapangan. Di dunia nyata, kejadian hujan memang jarang terjadi (imbalance). Oleh karena itu, kita harus menguji model menggunakan data asli yang tidak dimodifikasi distribusinya.

Jika kita menggunakan data SMOTE untuk evaluasi, hasil akurasi akan menjadi bias dan terlalu optimis (over-optimistic) karena data SMOTE adalah data sintetis (buatan) yang memiliki pola yang mirip dengan data latih. Hal ini tidak mencerminkan kemampuan model yang sesungguhnya dalam memprediksi data baru yang belum pernah dilihat sebelumnya.

Kesimpulan:

- Training menggunakan SMOTE agar proses pembelajaran optimal dan tidak bias.
- Evaluasi menggunakan Data Asli (X_test) agar pengukuran performa jujur, objektif, dan mencerminkan kondisi sebenarnya.

---

# PENJELASAN MENDALAM BAB 5: EVALUASI MODEL (SUMMARY)

Bagian ini dirancang khusus untuk menjawab pertanyaan: **"Kode ini sebenarnya untuk apa?"** pada setiap langkah di Bab 5.

1. Memuat Data Uji & Model

test_data = pd.read_csv('X_test.csv')
model = joblib.load('random_forest_model.pkl')

Penjelasan Detail:

- Tujuan: Ibarat seorang siswa yang sudah selesai belajar (training), sekarang saatnya **ujian**.
- X_test.csv: Adalah "soal ujian" yang belum pernah dilihat model sebelumnya. Kita menggunakan data asli (bukan SMOTE) agar ujiannya jujur sesuai kondisi lapangan.
- joblib.load: Memanggil kembali "otak" model yang sudah kita latih dan simpan sebelumnya di Bab 4.

2. Melakukan Prediksi

y_pred = model.predict(X_test)

Penjelasan Detail:

- Tujuan: Ini adalah momen **menjawab soal**.
- Proses: Model melihat data cuaca (suhu, angin, kelembaban, dll) di `X_test` dan mencoba menebak: "Besok Hujan (1)" atau "Tidak Hujan (0)".
- y_pred: Hasil tebakannya disimpan dalam variabel ini.

3. Cek Akurasi (Accuracy Score)

accuracy = accuracy_score(y_test, y_pred)

Penjelasan Detail:

- Tujuan: Ini adalah **nilai rapor umum**.
- Fungsi: Menghitung berapa persen tebakan model yang benar secara keseluruhan.
- Catatan Penting: Di proyek ini, akurasi tinggi (misal 85%) bisa menipu karena data kita tidak seimbang. Jadi ini hanya gambaran kasar.

4. Confusion Matrix

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, ...)

Penjelasan Detail:

- Tujuan: Ini adalah **bedah jawaban salah/benar**. Kita ingin tahu detailnya.
- True Positive: Berapa kali model benar menebak Hujan?
- False Positive: Berapa kali model **salah** menebak Hujan padahal tidak? ("Alarm Palsu")
- False Negative: Berapa kali model **gagal** mendeteksi Hujan padahal kejadian? ("Bahaya, kebasahan")

5. Classification Report

print(classification_report(y_test, y_pred, ...))

Penjelasan Detail:

- Tujuan: Ini adalah **analisis mendalam per kelas**. Karena kita sangat peduli dengan kejadian "Hujan" (yang jarang terjadi), kita butuh metrik khusus.
- Precision: Seberapa bisa dipercaya saat model bilang "Hujan"?
- Recall: Seberapa peka model mendeteksi "Hujan"?
- F1-Score: Nilai gabungan untuk melihat keseimbangan performa model.

6. Feature Importance

feature*importances = model.feature_importances*
plt.barh(...)

Penjelasan Detail:

- Tujuan: Ini menjawab pertanyaan **"Kenapa?"**.
- Fungsi: Model memberi tahu kita faktor apa saja yang paling dia perhatikan saat membuat keputusan.
- Temuan: Di proyek ini, model memberi tahu bahwa **Kecepatan Angin**, **Sinar Matahari**, dan **Kelembaban** adalah kunci utama penentu hujan. Ini membuktikan model kita logis secara ilmiah.
