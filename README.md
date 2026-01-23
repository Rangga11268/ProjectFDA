# 🌧️ Prediksi Hujan Australia

> ⚠️ **PENTING**: File model dan dataset tidak di-push ke GitHub karena ukuran besar (>100MB)

---

## 📥 Download Model & Data

Sebelum menjalankan aplikasi, download file berikut:

| File                      | Size   | Download Link                  |
| ------------------------- | ------ | ------------------------------ |
| `random_forest_model.pkl` | 280 MB | [Google Drive / OneDrive Link] |
| `label_encoders.pkl`      | 3 KB   | [Link]                         |
| `feature_columns.pkl`     | 355 B  | [Link]                         |
| `weatherAUS.csv`          | 17 MB  | [Link]                         |

**Letakkan file di folder:**

- Model files → `models/`
- Dataset → `data/`

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Rangga11268/ProjectFDA.git
cd ProjectFDA
```

### 2. Download Model & Data

Download file dari link di atas, lalu:

```bash
# Buat folder jika belum ada
mkdir -p models data

# Pindahkan file ke folder yang sesuai
# (Download manual dari link Google Drive/OneDrive)
```

### 3. Install Dependencies

```bash
pip install flask pandas numpy scikit-learn joblib
```

### 4. Jalankan Web App

```bash
cd webapp
python app.py
```

Buka browser: **http://localhost:5000**

---

## 📁 Struktur Proyek

```
Project/
├── data/                           # ⚠️ NOT in Git (download manually)
│   ├── weatherAUS.csv
│   ├── X_train_smote.csv
│   └── X_test.csv
│
├── models/                         # ⚠️ NOT in Git (download manually)
│   ├── random_forest_model.pkl
│   ├── label_encoders.pkl
│   └── feature_columns.pkl
│
├── notebooks/                      # ✅ In Git
│   └── ProjectFDAWeatherAUS.ipynb
│
├── webapp/                         # ✅ In Git
│   ├── app.py
│   ├── templates/index.html
│   └── static/
│
└── README.md
```

---

## 🤖 Model Info

- **Algorithm**: Random Forest Classifier
- **Accuracy**: ~85%
- **Dataset**: Weather Australia (145k records)
- **Features**: 24 fitur (suhu, kelembaban, angin, dll)

---

## ✨ Features

- ⚡ Mode Cepat (5 parameter)
- 🔧 Mode Lengkap (semua parameter)
- 🎨 Glassmorphism UI
- 📱 Mobile Responsive
- 🌧️ Rain Animation

---

## 📝 Credits

**Fundamental Data Analyst** - Semester 3  
GitHub: [@Rangga11268](https://github.com/Rangga11268)

---

> 💡 **Note**: Model file disimpan di Google Drive karena ukuran >100MB (GitHub limit)
