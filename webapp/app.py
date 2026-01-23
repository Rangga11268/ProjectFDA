"""
🌧️ Web Prediksi Hujan Australia
Flask Backend untuk model Random Forest
"""

from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Path ke model files (di folder models)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'random_forest_model.pkl')
ENCODERS_PATH = os.path.join(MODELS_DIR, 'label_encoders.pkl')
FEATURES_PATH = os.path.join(MODELS_DIR, 'feature_columns.pkl')

# Load model dan data pendukung saat startup
print("🔄 Memuat model dan data pendukung...")
try:
    model = joblib.load(MODEL_PATH)
    label_encoders = joblib.load(ENCODERS_PATH)
    feature_columns = joblib.load(FEATURES_PATH)
    print("✅ Model berhasil dimuat!")
except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    print("Pastikan file model ada di folder parent.")
    model = None
    label_encoders = None
    feature_columns = None

# Default values (median dari dataset)
DEFAULT_VALUES = {
    "Lokasi": 24.0, "SuhuMin": 12.1, "SuhuMax": 22.7, "CurahHujan": 0.0,
    "Penguapan": 5.47, "SinarMatahari": 7.61, "ArahAnginKencang": 9.0,
    "KecepatanAnginKencang": 39.0, "ArahAnginJam9": 7.0, "ArahAnginJam3": 8.0,
    "KecepatanAnginJam9": 13.0, "KecepatanAnginJam3": 18.66, "KelembabanJam9": 70.0,
    "KelembabanJam3": 51.54, "TekananUdaraJam9": 1017.65, "TekananUdaraJam3": 1015.26,
    "AwanJam9": 4.45, "AwanJam3": 4.51, "SuhuJam9": 16.8, "SuhuJam3": 21.3,
    "HujanHariIni": 0.0, "Year": 2024.0, "Month": 6.0, "Day": 15.0
}

# Daftar lokasi di Australia
LOCATIONS = [
    "Adelaide", "Albany", "Albury", "AliceSprings", "BadgerysCreek", "Ballarat",
    "Bendigo", "Brisbane", "Cairns", "Canberra", "Cobar", "CoffsHarbour",
    "Dartmoor", "Darwin", "GoldCoast", "Hobart", "Katherine", "Launceston",
    "Melbourne", "MelbourneAirport", "Mildura", "Moree", "MountGambier",
    "MountGinini", "Newcastle", "Nhil", "NorahHead", "NorfolkIsland",
    "Nuriootpa", "PearceRAAF", "Penrith", "Perth", "PerthAirport",
    "Portland", "Richmond", "Sale", "SalmonGums", "Sydney", "SydneyAirport",
    "Townsville", "Tuggeranong", "Uluru", "WasaWaga", "Watsonia",
    "Williamtown", "Witchcliffe", "Wollongong", "Woomera"
]


@app.route('/')
def index():
    """Halaman utama"""
    return render_template('index.html', locations=LOCATIONS)


@app.route('/api/locations')
def get_locations():
    """API: Daftar lokasi"""
    return jsonify(LOCATIONS)


@app.route('/predict', methods=['POST'])
def predict():
    """API: Prediksi hujan"""
    if model is None:
        return jsonify({
            'success': False,
            'error': 'Model belum dimuat. Pastikan file model tersedia.'
        }), 500

    try:
        data = request.get_json()
        
        # Mulai dengan default values
        input_data = DEFAULT_VALUES.copy()
        
        # Update dengan input user (mode simple - 5 fitur utama)
        if 'kelembaban_jam3' in data:
            input_data['KelembabanJam3'] = float(data['kelembaban_jam3'])
        if 'sinar_matahari' in data:
            input_data['SinarMatahari'] = float(data['sinar_matahari'])
        if 'kecepatan_angin' in data:
            input_data['KecepatanAnginKencang'] = float(data['kecepatan_angin'])
        if 'tutupan_awan' in data:
            input_data['AwanJam3'] = float(data['tutupan_awan'])
        if 'curah_hujan' in data:
            input_data['CurahHujan'] = float(data['curah_hujan'])
        
        # Mode advanced - fitur tambahan
        if 'suhu_min' in data:
            input_data['SuhuMin'] = float(data['suhu_min'])
        if 'suhu_max' in data:
            input_data['SuhuMax'] = float(data['suhu_max'])
        if 'kelembaban_jam9' in data:
            input_data['KelembabanJam9'] = float(data['kelembaban_jam9'])
        if 'hujan_hari_ini' in data:
            input_data['HujanHariIni'] = 1.0 if data['hujan_hari_ini'] else 0.0
        
        # Buat DataFrame dengan urutan kolom yang benar
        ordered_data = {col: input_data.get(col, 0) for col in feature_columns}
        input_df = pd.DataFrame([ordered_data])
        
        # Prediksi
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        
        # Hasil
        result = {
            'success': True,
            'prediction': int(prediction),
            'result': 'AKAN HUJAN' if prediction == 1 else 'TIDAK HUJAN',
            'probability_rain': round(probability[1] * 100, 2),
            'probability_no_rain': round(probability[0] * 100, 2),
            'input_summary': {
                'Kelembaban Jam 3': f"{input_data['KelembabanJam3']}%",
                'Sinar Matahari': f"{input_data['SinarMatahari']} jam",
                'Kecepatan Angin': f"{input_data['KecepatanAnginKencang']} km/h",
                'Tutupan Awan': f"{input_data['AwanJam3']} oktas",
                'Curah Hujan': f"{input_data['CurahHujan']} mm"
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/defaults')
def get_defaults():
    """API: Default values untuk form"""
    return jsonify({
        'kelembaban_jam3': DEFAULT_VALUES['KelembabanJam3'],
        'sinar_matahari': DEFAULT_VALUES['SinarMatahari'],
        'kecepatan_angin': DEFAULT_VALUES['KecepatanAnginKencang'],
        'tutupan_awan': DEFAULT_VALUES['AwanJam3'],
        'curah_hujan': DEFAULT_VALUES['CurahHujan'],
        'suhu_min': DEFAULT_VALUES['SuhuMin'],
        'suhu_max': DEFAULT_VALUES['SuhuMax'],
        'kelembaban_jam9': DEFAULT_VALUES['KelembabanJam9']
    })


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🌧️  WEB PREDIKSI HUJAN AUSTRALIA")
    print("="*50)
    print("📍 Buka browser: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
