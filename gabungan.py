import json

# Baca semua file
with open('Bab2DataUnderstanding.ipynb', 'r', encoding='utf-8') as f:
    bab2 = json.load(f)
with open('Bab3DataPreparation.ipynb', 'r', encoding='utf-8') as f:
    bab3 = json.load(f)
with open('Bab4ModellingFinal.ipynb', 'r', encoding='utf-8') as f:
    bab4 = json.load(f)
with open('Bab5Evaluation.ipynb', 'r', encoding='utf-8') as f:
    bab5 = json.load(f)

# Buat notebook gabungan
combined = {
    "cells": [],
    "metadata": bab2['metadata'],
    "nbformat": bab2['nbformat'],
    "nbformat_minor": bab2['nbformat_minor']
}

# Tambah judul
combined['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": ["# Project FDA Weather AUS - Complete Analysis\n\n"]
})

# Tambah Bab 2
combined['cells'].extend(bab2['cells'])

# Tambah Bab 3  
combined['cells'].extend(bab3['cells'])

# Tambah Bab 4 (kecuali cell 9 dan 10)
for i, cell in enumerate(bab4['cells']):
    if i not in [9, 10]:  # Skip evaluasi awal
        combined['cells'].append(cell)

# Tambah Bab 5
combined['cells'].extend(bab5['cells'])

# Simpan file
with open('ProjectFDAWeatherAUS.ipynb', 'w', encoding='utf-8') as f:
    json.dump(combined, f, indent=2, ensure_ascii=False)

print("File ProjectFDAWeatherAUS.ipynb berhasil dibuat!")
