# 🌧️ Web Prediksi Hujan Australia

Aplikasi web untuk memprediksi cuaca menggunakan model Machine Learning (Random Forest).

## 🚀 Cara Menjalankan

### 1. Install Dependencies

```bash
pip install flask pandas numpy scikit-learn joblib
```

### 2. Jalankan Aplikasi

```bash
cd webapp
python app.py
```

### 3. Buka Browser

Kunjungi: **http://localhost:5000**

---

## 📁 Struktur Folder

```
Project/
├── webapp/
│   ├── app.py              # Flask backend
│   ├── templates/
│   │   └── index.html      # Halaman utama
│   └── static/
│       ├── css/style.css   # Styling
│       └── js/main.js      # JavaScript
│
├── random_forest_model.pkl # Model ML (280 MB)
├── label_encoders.pkl      # Encoder
├── feature_columns.pkl     # Kolom fitur
└── README.md
```

---

## ✨ Fitur

- **Mode Cepat**: Input 5 parameter utama saja
- **Mode Lengkap**: Input semua parameter
- **Animasi Cuaca**: Efek awan dan hujan
- **Desain Modern**: Glassmorphism UI
- **Responsif**: Mendukung mobile

---

## 📊 Parameter Input

| Parameter        | Range | Satuan |
| ---------------- | ----- | ------ |
| Kelembaban Jam 3 | 0-100 | %      |
| Sinar Matahari   | 0-14  | jam    |
| Kecepatan Angin  | 0-150 | km/h   |
| Tutupan Awan     | 0-8   | oktas  |
| Curah Hujan      | 0-400 | mm     |

---

## 🎓 Credits

Proyek Fundamental Data Analyst - Semester 3
