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

d. Korelasi dengan Target (HujanBesok)

le = LabelEncoder()
data['HujanBesok_encoded'] = le.fit_transform(data['HujanBesok'])

# Calculate correlation for numeric columns including the encoded target variable

corr_with_target = data.corr(numeric_only=True)['HujanBesok_encoded'].sort_values(ascending=False)

Penjelasan Detail:

- LabelEncoder: Kita menginisialisasi objek LabelEncoder. Tujuannya adalah untuk mengubah variabel target 'HujanBesok' yang berisi teks ('Yes', 'No') menjadi format numerik (1, 0). Hal ini diperlukan karena perhitungan korelasi matematis hanya dapat dilakukan pada data angka.
- fit_transform: Metode ini mempelajari label unik pada kolom 'HujanBesok' dan secara langsung mengubahnya menjadi angka. Hasilnya disimpan dalam kolom sementara baru bernama 'HujanBesok_encoded'.
- data.corr(numeric_only=True): Kita menghitung matriks korelasi Pearson untuk seluruh DataFrame, namun dibatasi hanya pada kolom-kolom numerik saja (numeric_only=True) untuk menghindari error pada kolom teks.
- ['HujanBesok_encoded']: Dari matriks korelasi yang besar tersebut, kita melakukan slicing (pemotongan) untuk hanya mengambil nilai korelasi antara semua fitur terhadap variabel target 'HujanBesok_encoded'.
- sort_values(ascending=False): Hasil korelasi kemudian diurutkan dari nilai terbesar (positif terkuat) ke terkecil. Ini memudahkan kita untuk segera mengidentifikasi fitur mana yang memiliki hubungan linear paling kuat dengan kejadian hujan.

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

PENJELASAN MENDALAM BAB 5: EVALUASI MODEL (SUMMARY)

Bagian ini dirancang khusus untuk menjawab pertanyaan: "Kode ini sebenarnya untuk apa?" pada setiap langkah di Bab 5.

1. Memuat Data & Melatih Ulang Model (Khusus di Notebook)

Kode:

# Load Test Data

test_data = pd.read_csv('X_test.csv')
X_test = test_data.drop('HujanBesok', axis=1)
y_test = test_data['HujanBesok']

# Load Train Data (SMOTE) & Retrain

train_data = pd.read_csv('X_train_smote.csv')
X_train_smote = train_data.drop('HujanBesok', axis=1)
y_train_smote = train_data['HujanBesok']

model = RandomForestClassifier(random_state=42)
model.fit(X_train_smote, y_train_smote)

Tujuannya Apa?
Di dalam Notebook ini, kita melakukan pelatihan ulang (retraining) model sebelum evaluasi.

- Kenapa dilatih ulang? Karena di notebook ini kita tidak menyimpan model ke file (.pkl) di Bab 4. Jadi, agar kita punya model untuk diuji di Bab 5, kita harus melatihnya lagi menggunakan data X_train_smote.csv yang sudah disiapkan di Bab 3.
- X_test: Ini adalah "soal ujian" (data asli) untuk menguji model.
- model.fit: Proses model "belajar" kembali pola hujan dari data latih.

2. Melakukan Prediksi

Kode:

y_pred = model.predict(X_test)

Tujuannya Apa?
Ini adalah momen menjawab soal.

- model.predict: Model menggunakan "pengetahuan" yang sudah dipelajari untuk memprediksi label kelas (Hujan/Tidak Hujan) pada data uji X_test.
- y_pred: Hasil tebakannya disimpan dalam variabel ini. Array ini berisi deretan angka 0 dan 1 yang merupakan prediksi model untuk setiap baris data di X_test.

3. Cek Akurasi (Accuracy Score)

Kode:

accuracy = accuracy_score(y_test, y_pred)
print(f"Skor Akurasi: {accuracy:.4f}")

Tujuannya Apa?
Ini adalah nilai rapor umum.

- accuracy_score: Fungsi ini membandingkan jawaban model (y_pred) dengan kunci jawaban asli (y_test).
- Interpretasi: Menghitung berapa persen tebakan model yang benar secara keseluruhan.
- Catatan Penting: Di proyek ini, akurasi tinggi (misal 85%) bisa menipu karena data kita tidak seimbang (imbalance). Jadi ini hanya gambaran kasar dan bukan satu-satunya penentu keberhasilan.

4. Confusion Matrix

Kode:

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ...)

Tujuannya Apa?
Ini adalah bedah jawaban salah/benar. Kita ingin tahu detail kesalahan model:

- True Positive (TP): Model benar menebak "Hujan". (Bagus)
- True Negative (TN): Model benar menebak "Tidak Hujan". (Bagus)
- False Positive (FP): Model menebak "Hujan", padahal aslinya "Tidak Hujan". (Disebut juga Type I Error atau Alarm Palsu).
- False Negative (FN): Model menebak "Tidak Hujan", padahal aslinya "Hujan". (Disebut juga Type II Error). Ini berbahaya karena orang jadi tidak bawa payung saat hujan.

5. Classification Report

Kode:

print(classification_report(y_test, y_pred, target_names=['Tidak Hujan', 'Hujan']))

Tujuannya Apa?
Ini adalah analisis mendalam per kelas. Karena kita sangat peduli dengan kejadian "Hujan" (yang jarang terjadi), kita butuh metrik khusus:

- Precision: "Dari semua yang dibilang Hujan oleh model, berapa persen yang beneran Hujan?" (Fokus pada ketepatan prediksi positif).
- Recall: "Dari semua kejadian Hujan yang sebenarnya, berapa persen yang berhasil dideteksi model?" (Fokus pada cakupan deteksi).
- F1-Score: Nilai rata-rata harmonis antara Precision dan Recall. Ini adalah angka tunggal terbaik untuk menilai keseimbangan performa model pada data imbalance.

6. Feature Importance

Kode:

feature*importances = model.feature_importances*

# ... kode visualisasi bar chart ...

Tujuannya Apa?
Ini menjawab pertanyaan "Kenapa model memprediksi seperti itu?".

- feature*importances*: Atribut ini berisi skor untuk setiap fitur (kolom) yang menunjukkan seberapa besar kontribusinya dalam membuat keputusan di pohon-pohon Random Forest.
- Temuan: Di proyek ini, model memberi tahu bahwa Kecepatan Angin (WindGustSpeed), Sinar Matahari (Sunshine), dan Kelembaban (Humidity) adalah kunci utama penentu hujan. Ini membuktikan model kita logis secara ilmiah (meteorologis).

---

BAB 5 (LANJUTAN): ANALISIS KODE SPESIFIK & INTERPRETASI AKURASI

Bagian ini memberikan penjelasan baris demi baris untuk blok kode evaluasi dan analisis awal yang krusial.

1. Memuat Dataset Uji & Model

```python
# Load the test dataset
print("Loading prepared datasets...")
test_data = pd.read_csv('X_test.csv')
X_test = test_data.drop('HujanBesok', axis=1)
y_test = test_data['HujanBesok']
```

**Penjelasan:**

- Kode ini memuat **Data Uji (Test Set)** yang telah dipisahkan di awal proyek.
- `X_test`: Berisi fitur-fitur cuaca (Suhu, Angin, dll) yang akan digunakan untuk ujian.
- `y_test`: Berisi kunci jawaban sebenarnya (Hujan/Tidak) untuk menilai apakah prediksi model benar.

2. Melatih Ulang Model (Retraining Strategy)

```python
# Load the trained model from Bab 4
print("Loading trained model...")
# Since we don't have a saved model file...
train_data = pd.read_csv('X_train_smote.csv')
X_train_smote = train_data.drop('HujanBesok', axis=1)
y_train_smote = train_data['HujanBesok']

model = RandomForestClassifier(random_state=42)
model.fit(X_train_smote, y_train_smote)
```

**Penjelasan:**

- **Kenapa dilatih ulang?** Dalam skenario notebook ini, kita tidak memuat file model yang sudah jadi (seperti `.pkl`). Sebagai gantinya, kita memuat kembali data latih SMOTE (`X_train_smote`) dan melatih model `RandomForestClassifier` dari awal.
- **Tujuannya:** Memastikan kita memiliki objek `model` yang sudah "pintar" (sudah mempelajari pola dari data SMOTE) dan siap untuk diuji.

3. Prediksi & Cek Distribusi

```python
y_pred = model.predict(X_test)
print(f"Jumlah prediksi: {len(y_pred)}")
print(f"Distribusi prediksi: {pd.Series(y_pred).value_counts().to_dict()}")
```

**Penjelasan:**

- `model.predict`: Model memprediksi label (0 atau 1) untuk seluruh data uji.
- `value_counts()`: Kita menghitung berapa kali model memprediksi "Tidak Hujan" dan "Hujan". Ini langkah **Sanity Check** untuk memastikan model tidak hanya memprediksi satu kelas saja (misal: memprediksi "Tidak Hujan" untuk semua data).

4. Akurasi & Analisis Kritis (The Accuracy Paradox)

```python
accuracy = accuracy_score(y_test, y_pred)
print(f"Skor Akurasi: {accuracy:.4f}")

# Analysis
print("\n**Analisis Awal:**")
print(f"Model mencapai akurasi {accuracy:.2%}, yang terdengar cukup tinggi.")
print("Namun, akurasi bisa menyesatkan. Karena data kita tidak seimbang...")
```

**Penjelasan Mendalam:**

- Bagian ini adalah **inti dari pemahaman evaluasi**.
- Kode mencetak akurasi (misal 84%), tetapi langsung memberikan peringatan ("Analisis Awal").
- **Masalah:** Data kita _Imbalanced_ (78% Tidak Hujan vs 22% Hujan).
- **Logika:** Jika Anda menebak "Tidak Hujan" terus-menerus tanpa mikir, Anda akan benar 78% dari waktu. Jadi, akurasi 78% itu adalah _baseline_ (standar minimal), bukan prestasi.
- **Pesan Moral:** Jangan terkecoh dengan angka akurasi yang tinggi. Kita harus melihat metrik lain (Precision, Recall, F1-Score) untuk memastikan model benar-benar bisa mendeteksi "Hujan" (kelas minoritas), bukan hanya pintar menebak "Tidak Hujan".

---

# PENJELASAN DETAIL KODE BAB 5: EVALUASI (5.1 - 5.4)

Berikut adalah penjelasan mendalam untuk setiap blok kode pada Bab 5, mulai dari perhitungan akurasi hingga analisis fitur penting.

## 5.1 Skor Akurasi (Accuracy Score)

**Kode:**

```python
# Load test data
test_data = pd.read_csv('X_test.csv')
X_test = test_data.drop('HujanBesok', axis=1)
y_test = test_data['HujanBesok']

# Load train data (SMOTE) & Retrain Model
train_data = pd.read_csv('X_train_smote.csv')
X_train_smote = train_data.drop('HujanBesok', axis=1)
y_train_smote = train_data['HujanBesok']

model = RandomForestClassifier(random_state=42)
model.fit(X_train_smote, y_train_smote)

# Predict
y_pred = model.predict(X_test)

# Calculate Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Skor Akurasi: {accuracy:.4f}")
```

**Penjelasan Teknis & Alur Logika:**

1.  **Memuat Data Uji (`X_test`, `y_test`):**

    - Kita memuat file `X_test.csv` yang berisi data **asli** (tanpa SMOTE).
    - **Penting:** Evaluasi wajib menggunakan data asli yang tidak seimbang (imbalanced) untuk mensimulasikan kondisi dunia nyata.

2.  **Melatih Ulang Model (`model.fit`):**

    - Kita memuat `X_train_smote.csv` (data hasil oversampling).
    - Kita melatih `RandomForestClassifier` menggunakan data SMOTE ini.
    - **Kenapa ada SMOTE di sini?** Karena ini tahap **Training (Belajar)**. Kita ingin model belajar dari data yang seimbang agar tidak bias ke kelas mayoritas ("Tidak Hujan").

3.  **Prediksi (`y_pred`):**

    - Model yang sudah "pintar" (dilatih dengan SMOTE) sekarang diuji mengerjakan soal ujian (`X_test`).
    - Hasil tebakannya disimpan di `y_pred`.

4.  **Akurasi (`accuracy_score`):**
    - Fungsi ini menghitung: `(Jumlah Tebakan Benar) / (Total Soal)`.
    - **Interpretasi:** Jika hasilnya 0.85 (85%), artinya 85 dari 100 tebakan model benar.
    - **Peringatan:** Pada data cuaca yang jarang hujan, akurasi tinggi bisa menipu. Model yang malas dan selalu menebak "Tidak Hujan" pun bisa dapat akurasi tinggi. Makanya kita butuh Bab 5.2 dan 5.3.

## 5.2 Confusion Matrix

**Kode:**

```python
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Tidak Hujan', 'Hujan'], yticklabels=['Tidak Hujan', 'Hujan'])
```

**Penjelasan Teknis:**

1.  **`confusion_matrix`:** Fungsi ini membedah hasil prediksi menjadi 4 kategori detail:

    - **True Negative (TN):** Pojok Kiri Atas. Model bilang "Tidak", Data asli "Tidak". (Prediksi Benar).
    - **False Positive (FP):** Pojok Kanan Atas. Model bilang "Hujan", Data asli "Tidak". (Salah: Alarm Palsu).
    - **False Negative (FN):** Pojok Kiri Bawah. Model bilang "Tidak", Data asli "Hujan". (Salah: Gagal Mendeteksi).
    - **True Positive (TP):** Pojok Kanan Bawah. Model bilang "Hujan", Data asli "Hujan". (Prediksi Benar).

2.  **`sns.heatmap`:**
    - Membuat visualisasi kotak warna-warni.
    - `annot=True`: Menampilkan angkanya di dalam kotak.
    - `fmt='d'`: Memastikan angka ditampilkan sebagai bilangan bulat (integer), bukan desimal.
    - **Tujuan:** Memudahkan kita melihat di mana model paling sering salah. Apakah sering "PHP" (False Positive) atau sering "Kecolongan" (False Negative)?

## 5.3 Laporan Klasifikasi (Classification Report)

**Kode:**

```python
print(classification_report(y_test, y_pred, target_names=['Tidak Hujan', 'Hujan']))
```

**Penjelasan Teknis:**

Fungsi ini menghitung metrik kualitas untuk **setiap kelas** secara terpisah. Fokus utama kita biasanya pada kelas **'Hujan'** (kelas minoritas).

1.  **Precision (Ketepatan):**

    - Rumus: `TP / (TP + FP)`
    - **Arti:** "Saat model teriak 'HUJAN!', seberapa sering dia benar?"
    - Jika Precision rendah, berarti model sering "bawel" (banyak alarm palsu).

2.  **Recall (Sensitivitas):**

    - Rumus: `TP / (TP + FN)`
    - **Arti:** "Dari seluruh kejadian hujan yang benar-benar terjadi hari ini, berapa persen yang berhasil dideteksi model?"
    - Jika Recall rendah, berarti model sering melewatkan hujan (kita jadi kehujanan karena tidak bawa payung).

3.  **F1-Score:**
    - Rumus: `2 * (Precision * Recall) / (Precision + Recall)`
    - **Arti:** Nilai tengah (rata-rata harmonis) antara Precision dan Recall.
    - Ini adalah **Satu Angka Terpenting** untuk menilai model pada data imbalance. F1-Score yang tinggi menandakan model yang seimbang: cukup tepat dan cukup peka.

## 5.4 Identifikasi Fitur Penting (Feature Importance)

**Kode:**

```python
feature_importances = model.feature_importances_
# ... (kode visualisasi bar chart) ...
```

**Penjelasan Teknis:**

1.  **`model.feature_importances_`:**

    - Ini adalah atribut spesial milik Random Forest.
    - Saat membuat ribuan pohon keputusan, algoritma mencatat fitur (kolom) mana yang paling sering dipakai untuk memisahkan data "Hujan" dan "Tidak Hujan" dengan bersih.
    - Semakin sering dan efektif sebuah fitur dipakai, semakin tinggi skornya.

2.  **Visualisasi Bar Chart:**
    - Kita mengurutkan skor tersebut dari terbesar ke terkecil.
    - **Tujuan:** Memverifikasi logika model.
    - **Contoh:** Jika fitur teratas adalah `Cloud3pm` (Awan jam 3 sore) dan `Humidity3pm` (Kelembaban), itu masuk akal secara ilmu cuaca. Jika fitur teratas aneh (misalnya `Date`), berarti model kita mungkin salah belajar (overfitting).

---

# PERTANYAAN DOSEN LANJUTAN (FEATURE ENGINEERING)

Bagian ini khusus membahas keputusan teknis kenapa memilih metode tertentu (Label Encoder) dibandingkan metode lain (One-Hot, PCA, Feature Selection).

## Q: Mengapa Anda menggunakan Label Encoder untuk data Kategori (seperti Lokasi)? Bukankah secara teori harusnya One-Hot Encoder?

**A (Jawaban Cerdas):**
"Betul Pak/Bu, secara teori statistik untuk data nominal harusnya One-Hot Encoder. Namun, saya memilih **Label Encoder** karena pertimbangan **Efisiensi Engineering** khusus untuk algoritma **Random Forest**:

1.  **Menghindari Ledakan Dimensi:** Fitur `Lokasi` memiliki 49 kota unik. Jika saya pakai One-Hot, feature kita akan meledak bertambah ~50 kolom baru yang isinya kebanyakan angka nol (sparse). Ini akan sangat memperberat komputasi tanpa memberikan gain yang signifikan.
2.  **Kecocokan Model:** Random Forest adalah algoritma berbasis Tree. Dia bekerja dengan mencari _threshold_ (titik potong), bukan perkalian bobot seperti Regresi Linear. Jadi, Random Forest cukup pintar untuk memisahkan kategori yang diberi label angka (0-48) tanpa terjebak asumsi bahwa 'Kota 48' lebih besar nilainya dari 'Kota 0'."

**A (Jawaban Sederhana):**
"Karena data Lokasi variasinya terlalu banyak (49 kota). Kalau dipecah satu-satu (One-Hot), data jadi terlalu gemuk dan bikin komputer lambat. Random Forest sudah cukup pintar untuk membaca kode angka sederhana, jadi Label Encoder adalah solusi paling efisien."

## Q: Kenapa Anda tidak membuang kolom yang tidak perlu di awal (Feature Selection)? Kenapa dimasukkan semua?

**A (Jawaban Strategis):**
"Saya sengaja memasukkan semua fitur karena saya ingin **Menghindari Bias Pribadi**.

1.  **Let Data Speak:** Saya tidak ingin sok tahu membuang data (misal data kota kecil) yang mungkin ternyata punya pola cuaca unik.
2.  **Embedded Feature Selection:** Kelebihan utama Random Forest adalah dia punya kemampuan seleksi fitur otomatis di dalamnya. Saat training, model akan otomatis mengabaikan kolom yang tidak berguna dan memberikan skor tinggi pada kolom penting (seperti yang kita lihat di Feature Importance Bab 5). Jadi, memasukkan semua fitur justru cara paling aman untuk memastikan tidak ada informasi penting yang terbuang."

## Q: Kenapa tidak dikurangi saja dimensinya pakai PCA (Dimensionality Reduction)?

**A (Jawaban Mematikan):**
"Saya tidak menggunakan PCA karena alasan **Interpretabilitas (Kemudahan Penjelasan)**.

1.  **Data Analyst butuh Insight:** Tujuan saya bukan cuma prediksi, tapi juga paham penyebab hujan. Jika saya pakai PCA, fitur 'Angin' dan 'Lokasi' akan lebur jadi variabel abstrak 'PC1' atau 'PC2' yang tidak bisa dijelaskan artinya.
2.  **Efisiensi Label Encoder:** Sebenarnya, dengan saya memilih Label Encoder (mengubah 49 potensi kolom menjadi 1 kolom angka), saya **sudah melakukan reduksi dimensi** dengan cara yang paling efektif dan tetap bisa dibaca manusia."
