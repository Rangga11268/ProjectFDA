# 🌧️ Australian Weather Prediction AI

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-green.svg)
![ML](https://img.shields.io/badge/Model-Random%20Forest-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

Web aplikasi berbasis Machine Learning untuk memprediksi kemungkinan hujan di Australia berdasarkan data cuaca historis. Dibangun dengan Python (Flask) dan antarmuka modern menggunakan Tailwind CSS.

![Dashboard Preview](https://github.com/user-attachments/assets/placeholder-image.png)

---

## 👥 Tim Fundamental Data Analyst

Proyek ini disusun sebagai Tugas Akhir Mata Kuliah **Fundamental Data Analyst** (Semester 3).

| No  | Nama Anggota         | &nbsp; |
| --- | -------------------- | ------ |
| 1.  | **Darell Rangga**    | 👨‍💻     |
| 2.  | **Rifa Dini**        | 👩‍💻     |
| 3.  | **Syifa Aulia**      | 👩‍💻     |
| 4.  | **Megi Refkiansyah** | 👨‍💻     |
| 5.  | **Wahyu Rizky**      | 👨‍💻     |

---

## 🚀 Fitur Utama

- **🤖 High Accuracy Model**: Menggunakan Random Forest Classifier dengan akurasi ~85%.
- **✨ Modern UI**: Antarmuka bersih & gelap (Dark Mode) ala Vercel/Linear dengan Tailwind CSS.
- **⚡ Real-time Prediction**: Hasil prediksi instan dengan kalkulasi probabilitas.
- **📱 Responsive**: Teks dan layout menyesuaikan berbagai ukuran layar.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Machine Learning**: Scikit-Learn (Random Forest)
- **Data Processing**: Pandas, NumPy, SMOTE (Imbalanced Data Handling)
- **Frontend**: HTML5, Tailwind CSS, JavaScript (Vanilla)

---

## 📥 Cara Instalasi

Karena file model berukuran besar (>100MB), Anda perlu mengunduhnya secara manual sebelum menjalankan aplikasi.

### 1. Clone Repository

```bash
git clone https://github.com/Rangga11268/ProjectFDA.git
cd ProjectFDA
```

### 2. Setup Data & Model

Download file berikut [Link Google Drive/OneDrive Anda] dan letakkan sesuai struktur folder:

```
ProjectFDA/
├── models/
│   ├── random_forest_model.pkl  <-- (280 MB) DOWNLOAD INI
│   ├── label_encoders.pkl
│   └── feature_columns.pkl
├── data/
│   └── weatherAUS.csv
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
# Atau manual:
pip install flask pandas numpy scikit-learn joblib
```

### 4. Jalankan Aplikasi

```bash
cd webapp
python app.py
```

Buka browser di: `http://localhost:5000`

---

## 📊 Workflow Proyek (CRISP-DM)

Proyek ini mengikuti metodologi CRISP-DM:

1.  **Business Understanding**: Memahami faktor cuaca yang mempengaruhi hujan.
2.  **Data Understanding**: Eksplorasi dataset WeatherAUS (145k baris).
3.  **Data Preparation**: Cleaning, Feature Engineering (Date splitting), Encoding.
4.  **Modeling**: Training Random Forest dengan SMOTE balancing.
5.  **Evaluation**: Confusion matrix, Accuracy score testing.
6.  **Deployment**: Web App Flask.

---

## 📁 Struktur Folder

```bash
Project/
├── data/               # Dataset (Not in Git)
├── models/             # ML Models (Not in Git)
├── notebooks/          # Jupyter Notebooks Analisis
├── webapp/             # Source Code Web App
│   ├── static/         # CSS & JS
│   ├── templates/      # HTML Files
│   └── app.py          # Main Backend
└── README.md           # Dokumentasi
```

---

© 2026 Fundamental Data Analyst Team. Created with ❤️ and Python.
