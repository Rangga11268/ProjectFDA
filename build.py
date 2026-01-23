import os
import requests
import sys

# Konfigurasi URL Model (GANTI URL INI DENGAN LINK DIRECT DOWNLOAD ANDA)
# Contoh: Link Google Drive, Dropbox, atau S3 yang bisa didownload langsung (wget/curl friendly)
# Jika pakai GDrive, pastikan permission 'Anyone with link' dan gunakan link download resminya.
MODEL_URL = "https://example.com/path/to/random_forest_model.pkl" 
ENCODER_URL = "https://example.com/path/to/label_encoders.pkl"
FEATURE_URL = "https://example.com/path/to/feature_columns.pkl"

# Folder Tujuan
DEST_FOLDER = "models"

def download_file(url, dest_path):
    if os.path.exists(dest_path):
        print(f"✅ File sudah ada: {dest_path}")
        return

    print(f"⬇️ Downloading {url} to {dest_path}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Download selesai: {dest_path}")
    except Exception as e:
        print(f"❌ Gagal download {dest_path}: {e}")
        # Di environment production, kita mungkin ingin fail build jika model penting gagal
        # sys.exit(1) 

def main():
    if not os.path.exists(DEST_FOLDER):
        os.makedirs(DEST_FOLDER)
    
    # KARENA KITA BELUM PUNYA LINK ASLI, SAYA COMMENT DULU AGAR TIDAK ERROR SAAT TEST
    # download_file(MODEL_URL, os.path.join(DEST_FOLDER, "random_forest_model.pkl"))
    # download_file(ENCODER_URL, os.path.join(DEST_FOLDER, "label_encoders.pkl"))
    # download_file(FEATURE_URL, os.path.join(DEST_FOLDER, "feature_columns.pkl"))
    
    print("ℹ️ Script download selesai. (Placeholder Mode)")
    print("⚠️  PENTING: Edit file 'build.py' dan masukkan URL download model asli Anda!")

if __name__ == "__main__":
    main()
