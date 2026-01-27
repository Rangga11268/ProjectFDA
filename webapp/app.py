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


# Load Dataset untuk Historical Backtest (Lazy loading atau sample)
# Kita ambil sample 1000 data terbaru yang ada HujanBesok-nya untuk backtest
print("🔄 Memuat data historical...")
try:
    # Mapping nama kolom dataset asli ke nama fitur kita
    # Dataset weatherAUS.csv sudah ditranslate ke Indonesia
    historical_data = pd.read_csv(os.path.join(BASE_DIR, 'data', 'weatherAUS.csv'))
    
    # Pastikan format tanggal benar
    historical_data['Tanggal'] = pd.to_datetime(historical_data['Tanggal'])
    historical_data.dropna(subset=['HujanBesok'], inplace=True)
    
    # Ambil sample acak 5000 baris untuk optimasi RAM
    historical_data = historical_data.sample(n=5000, random_state=42).sort_values('Tanggal', ascending=False)
    print(f"✅ Historical data dimuat: {len(historical_data)} records")
except Exception as e:
    print(f"⚠️ Gagal memuat data historical: {e}")
    historical_data = None

@app.route('/')
def index():
    """Halaman utama"""
    # Ambil list lokasi unik dari historical data jika ada
    locs = LOCATIONS
    if historical_data is not None:
        if 'Lokasi' in historical_data.columns:
            locs = sorted(historical_data['Lokasi'].unique().tolist())
    return render_template('index.html', locations=locs)

@app.route('/docs')
def docs():
    """Halaman dokumentasi"""
    return render_template('docs.html')


@app.route('/api/locations')
def get_locations():
    """API: Daftar lokasi"""
    return jsonify(LOCATIONS)

def generate_explanation(input_data, probability):
    """Simple Rule-based Explainability"""
    reasons = []
    
    # Aturan Heuristik sederhana berdasarkan EDA
    if input_data['KelembabanJam3'] > 70:
        reasons.append("Kelembaban sore sangat tinggi (>70%)")
    elif input_data['KelembabanJam3'] < 30:
        reasons.append("Udara sangat kering, menghambat pembentukan hujan") # Negative factor
        
    if input_data['AwanJam3'] >= 7:
        reasons.append("Langit mendung tebal (Tutupan Awan tinggi)")
        
    if input_data['SinarMatahari'] < 5:
        reasons.append("Minim sinar matahari (< 5 jam)")
        
    if input_data['CurahHujan'] > 5:
        reasons.append(f"Intensitas hujan hari ini cukup tinggi ({input_data['CurahHujan']}mm)")
        
    if input_data['KecepatanAnginKencang'] > 50:
        reasons.append("Terdeteksi angin kencang berpotensi badai")
        
    if input_data['TekananUdaraJam3'] < 1010:
        reasons.append("Tekanan udara rendah (Sistem Low Pressure)")

    # Fallback reason
    if not reasons and probability > 50:
        reasons.append("Kombinasi faktor suhu dan kelembaban mendukung hujan")
    elif not reasons and probability <= 50:
        reasons.append("Kondisi cuaca relatif stabil dan cerah")
        
    return reasons

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
        prob_rain = round(probability[1] * 100, 2)

        # Generate Explanation
        explanations = generate_explanation(input_data, prob_rain)
        
        # Hasil
        result = {
            'success': True,
            'prediction': int(prediction),
            'result': 'AKAN HUJAN' if prediction == 1 else 'TIDAK HUJAN',
            'probability_rain': prob_rain,
            'probability_no_rain': round(probability[0] * 100, 2),
            'explanations': explanations, # [NEW] Why?
            'input_data': input_data      # [NEW] Return clean data for chart
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/historical/search', methods=['POST'])
def search_historical():
    """API: Cari data historical untuk backtest"""
    if historical_data is None:
        return jsonify({'success': False, 'error': 'Database historical tidak tersedia'})
    
    try:
        req = request.get_json()
        location = req.get('location')
        
        # Filter by location (Gunakan nama kolom bahasa Indonesia 'Lokasi')
        matches = historical_data[historical_data['Lokasi'] == location].head(20)
        
        results = []
        for _, row in matches.iterrows():
            results.append({
                'date': row['Tanggal'].strftime('%Y-%m-%d'),
                'rain_tomorrow': row['HujanBesok'], # Yes/No
                'data': {
                    'KelembabanJam3': row.get('KelembabanJam3', 50),
                    'SinarMatahari': row.get('SinarMatahari', 7),
                    'KecepatanAnginKencang': row.get('KecepatanAnginKencang', 40),
                    'AwanJam3': row.get('AwanJam3', 5),
                    'CurahHujan': row.get('CurahHujan', 0),
                    # Tambahan untuk display enak
                    'SuhuMax': row.get('SuhuMax', 25) 
                }
            })
            
        return jsonify({'success': True, 'results': results})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/historical/test', methods=['POST'])
def test_historical():
    """API: Test model vs kenyataan pada tanggal tertentu"""
    try:
        req = request.get_json()
        print(f"DEBUG TEST: Received data: {req}") # DEBUG
        
        raw_data = req.get('data')
        input_data = DEFAULT_VALUES.copy()
        
        # Pastikan konversi tipe data aman
        for k, v in raw_data.items():
            if k in input_data:
                try:
                    input_data[k] = float(v)
                except:
                    pass # Keep default if fail
        
        ordered_data = {col: input_data.get(col, 0) for col in feature_columns}
        input_df = pd.DataFrame([ordered_data])
        
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        
        actual = req.get('actual')
        print(f"DEBUG TEST: Prediction={prediction}, Actual={actual}") # DEBUG
        
        actual_bool = 1 if str(actual).strip().lower() == 'yes' else 0
        is_correct = (int(prediction) == int(actual_bool))
        
        return jsonify({
            'success': True,
            'prediction': int(prediction),
            'probability': round(probability[1] * 100, 1),
            'actual': actual,
            'is_correct': is_correct,
            'explanations': generate_explanation(input_data, probability[1]*100)
        })

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        return jsonify({'success': False, 'error': str(e)})

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
