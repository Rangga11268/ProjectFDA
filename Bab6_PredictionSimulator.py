import pandas as pd
import numpy as np
import joblib
import warnings
import os
import random

# Filter warning untuk kebersihan output
warnings.filterwarnings('ignore')

# Konfigurasi tampilan pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_resources():
    print("Memuat model dan data pendukung...")
    try:
        model = joblib.load('random_forest_model.pkl')
        label_encoders = joblib.load('label_encoders.pkl')
        feature_columns_list = joblib.load('feature_columns.pkl')
        
        # Load X_test untuk simulasi batch (mengambil data asli untuk testing)
        X_test_real = pd.read_csv('X_test.csv')
        
        print("Model dan data berhasil dimuat.\n")
        return model, label_encoders, feature_columns_list, X_test_real
    except FileNotFoundError as e:
        print(f"Error: File tidak ditemukan ({e}).")
        print("Pastikan Anda sudah menjalankan Bab3_DataPreparation.py dan Bab4_Modelling.py")
        exit()

def get_user_input(feature_columns, label_encoders):
    print("\n--- Masukkan Data Cuaca Baru ---")
    input_data = {}
    
    for col in feature_columns:
        # Skip jika kolom target masuk ke feature (seharusnya tidak, tapi untuk jaga-jaga)
        if col == 'HujanBesok': 
            continue
            
        while True:
            try:
                # Cek apakah kolom ini kategorikal (ada di label_encoders)
                if col in label_encoders:
                    print(f"\nInput untuk {col} (Pilihan: {', '.join(label_encoders[col].classes_[:5])}...):")
                    val = input(f"Masukkan nilai {col}: ").strip()
                    
                    # Cek validitas input kategori
                    if val in label_encoders[col].classes_:
                        # Encode nilai input
                        encoded_val = label_encoders[col].transform([val])[0]
                        input_data[col] = encoded_val
                        break
                    else:
                        print(f"Nilai tidak valid. Harap pilih dari: {label_encoders[col].classes_}")
                else:
                    # Input numerik
                    val = input(f"Masukkan nilai numeric {col}: ").strip()
                    input_data[col] = float(val)
                    break
            except ValueError:
                print("Input tidak valid, harap masukkan angka yang benar.")
    
    return pd.DataFrame([input_data])

def batch_simulation(model, X_test_real, feature_columns, n_samples=10):
    print(f"\n--- Memulai Simulasi Batch ({n_samples} Sampel) ---")
    
    if n_samples > len(X_test_real):
        print(f"Warning: Jumlah sampel yang diminta ({n_samples}) melebihi data test yang ada ({len(X_test_real)}). Menggunakan semua data test.")
        n_samples = len(X_test_real)
    
    # Ambil sampel acak dari data test
    # Catatan: X_test.csv sebenarnya sudah pre-processed (encoded), jadi kita bisa langsung prediksi
    # Namun kita perlu juga nilai asli (HujanBesok) untuk verifikasi. 
    # Karena X_test.csv di Bab3 digabung fiturnya, kita asumsikan kolom terakhir atau kita load ulang y_test jika ada.
    # Tapi di script Bab3, X_test.csv menyimpan fitur DAN target HujanBesok.
    
    samples = X_test_real.sample(n=n_samples)
    
    # Pisahkan fitur dan target
    X_samples = samples.drop('HujanBesok', axis=1)
    y_true = samples['HujanBesok']
    
    # Prediksi
    y_pred = model.predict(X_samples)
    y_prob = model.predict_proba(X_samples)[:, 1]
    
    # Tampilkan Hasil
    print("\n{:<5} | {:<15} | {:<15} | {:<10}".format("No", "Prediksi Model", "Kenyataan", "Status"))
    print("-" * 55)
    
    correct_count = 0
    
    results = []
    
    for i in range(n_samples):
        # Decode target jika perlu (misal 0=Tidak, 1=Ya)
        # Asumsi 0=No, 1=Yes berdasarkan encoding umum, tapi mari kita pakai string output
        pred_label = "Hujan" if y_pred[i] == 1 else "Tidak Hujan"
        true_label = "Hujan" if y_true.iloc[i] == 1 else "Tidak Hujan"
        
        status = "BENAR" if y_pred[i] == y_true.iloc[i] else "SALAH"
        if status == "BENAR":
            correct_count += 1
            
        print("{:<5} | {:<15} | {:<15} | {:<10}".format(i+1, pred_label, true_label, status))
        results.append({
            'Actual': true_label,
            'Predicted': pred_label,
            'Prob_Rain': y_prob[i]
        })

    accuracy = (correct_count / n_samples) * 100
    print("-" * 55)
    print(f"Akurasi pada batch ini: {accuracy:.2f}% ({correct_count}/{n_samples})")
    return results

def generate_synthetic_data(X_real, n_synthetic=10000):
    """
    Membuat data sintetik dengan menambahkan sedikit noise pada data asli.
    Ini mensimulasikan variasi data di dunia nyata.
    """
    print(f"\n[INFO] Men-generate {n_synthetic} data sintetik dari data asli...")
    
    # Ambil sampel acak dari data asli sebagai basis
    base_data = X_real.sample(n=n_synthetic, replace=True)
    
    X_synthetic = base_data.drop('HujanBesok', axis=1).copy()
    y_synthetic = base_data['HujanBesok'].copy() # Asumsi label tetap sama untuk perubahan kecil
    
    # Tambahkan noise gaussian ke kolom numerik
    # Kita perlu tahu kolom mana yang numerik. 
    # Sederhananya, kolom dengan banyak unique values biasanya numerik.
    # Atau kita iterate semua dan try-except.
    
    noise_level = 0.05 # 5% variasi
    
    for col in X_synthetic.columns:
        # Cek jika kolom numerik (float/int) dan bukan hasil encoding kategori (biasanya integer kecil)
        # Cara kasar: jika unique values > 20, anggap continue/numerik yang bisa di-noise
        if X_synthetic[col].nunique() > 20: 
            sigma = X_synthetic[col].std() * noise_level
            noise = np.random.normal(0, sigma, X_synthetic.shape[0])
            X_synthetic[col] = X_synthetic[col] + noise
            
    return X_synthetic, y_synthetic

def augmentation_stress_test(model, X_test_real, n_synthetic=10000):
    print("\n==================================================")
    print(f"   STRESS TEST: DATA AUGMENTATION ({n_synthetic:,} Data Baru)")
    print("==================================================")
    print(f"Skenario: Menambahkan {n_synthetic:,} data baru (sintetik) ke data test asli.")
    print("Tujuannya: Menguji apakah model tetap konsisten saat menghadapi variasi data.")
    
    # 1. Data Asli
    X_real = X_test_real.drop('HujanBesok', axis=1)
    y_real = X_test_real['HujanBesok']
    n_real = len(X_real)
    
    # 2. Generate Data Sintetik
    X_syn, y_syn = generate_synthetic_data(X_test_real, n_synthetic=n_synthetic)
    n_syn = len(X_syn)
    
    print(f"\nJumlah Data Asli    : {n_real:,}")
    print(f"Jumlah Data Tambahan: {n_syn:,}")
    print(f"TOTAL DATA PENGUJIAN: {n_real + n_syn:,}")
    
    print("\nMelakukan Prediksi pada Total Data (Mohon tunggu)...")
    
    # Gabungkan
    X_total = pd.concat([X_real, X_syn])
    y_total = pd.concat([y_real, y_syn])
    
    # Prediksi
    y_pred = model.predict(X_total)
    
    # Hitung Akurasi
    from sklearn.metrics import accuracy_score
    acc_total = accuracy_score(y_total, y_pred)
    
    # Akurasi per bagian
    y_pred_real = model.predict(X_real)
    acc_real = accuracy_score(y_real, y_pred_real)
    
    y_pred_syn = model.predict(X_syn)
    acc_syn = accuracy_score(y_syn, y_pred_syn)
    
    print("\n--- HASIL PENGUJIAN ---")
    print(f"Akurasi Data Asli ({n_real:,} data)      : {acc_real*100:.2f}%")
    print(f"Akurasi Data Sintetik ({n_syn:,} data)  : {acc_syn*100:.2f}%")
    print("-" * 50)
    print(f"AKURASI TOTAL ({n_real + n_syn:,} data)     : {acc_total*100:.2f}%")
    
    if abs(acc_real - acc_syn) < 0.05:
        print("\nKESIMPULAN: Model SANGAT ROBUST (Konsisten).")
        print("Performa model stabil bahkan dengan adanya variasi data baru.")
    else:
        print("\nKESIMPULAN: Model Cukup Stabil (Ada sedikit penurunan/perubahan pada data baru).")

def main():
    clear_screen()
    print("==================================================")
    print("   SIMULATOR PREDIKSI HUJAN (WEATHER AUS)   ")
    print("==================================================")
    
    model, label_encoders, feature_columns, X_test_real = load_resources()
    
    while True:
        print("\nMenu Utama:")
        print("1. Simulasi Satu Data (Input Manual)")
        print("2. Simulasi Banyak Data (Batch Test)")
        print("3. Stress Test: DATA AUGMENTATION (Add 10k, 20k, 50k+ Data Baru)")
        print("4. Keluar")
        
        choice = input("Pilih menu (1-4): ").strip()
        
        if choice == '1':
            input_df = get_user_input(feature_columns, label_encoders)
            print("\nMelakukan prediksi...")
            pred = model.predict(input_df)[0]
            prob = model.predict_proba(input_df)[0]
            
            hasil = "AKAN HUJAN" if pred == 1 else "TIDAK HUJAN"
            chance = prob[1] * 100
            
            print(f"\n>>> HASIL PREDIKSI: {hasil}")
            print(f">>> Probabilitas Hujan: {chance:.2f}%")
            
            input("\nTekan Enter untuk kembali ke menu...")
            
        elif choice == '2':
            try:
                n = int(input("Masukkan jumlah data dummy yang ingin dites (contoh: 10, 50, 100): "))
                batch_simulation(model, X_test_real, feature_columns, n_samples=n)
            except ValueError:
                print("Input jumlah harus angka.")
            
            input("\nTekan Enter untuk kembali ke menu...")

        elif choice == '3':
            try:
                print("\nMasukkan jumlah data sintetik tambahan (Saran: 10000, 20000, 30000, 50000):")
                n_syn = int(input("Jumlah data: "))
                augmentation_stress_test(model, X_test_real, n_synthetic=n_syn)
            except ValueError:
                print("Input jumlah harus angka.")
            input("\nTekan Enter untuk kembali ke menu...")
            
        elif choice == '4':
            print("Terima kasih telah menggunakan simulator.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
