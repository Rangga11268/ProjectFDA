Tentu, ini adalah bagian yang paling penting untuk membuktikan bahwa model Anda berhasil. Bab 5 adalah tempat Anda mengevaluasi hasil (`y_pred`) yang didapat dari Bab 4.

Berdasarkan `panduanFDA.pdf` ("...uraian evaluasi dari hasil yang telah dicapai, penilaian terkait kualitas dan efektifitas-nya") dan temuan **`Class Imbalance`** di Bab 2, *outline* berikut akan memberikan evaluasi yang paling kuat dan profesional.

---

### **OUTLINE BAB 5: EVALUASI**

**Judul Bab: BAB 5: EVALUASI**

**(Paragraf Pembuka)**
* Paragraf singkat yang menjelaskan bahwa Bab 5 akan mengevaluasi hasil prediksi (`y_pred`) dari Bab 4 terhadap data aktual (`y_test`).
* Menyatakan bahwa tujuan evaluasi ini adalah untuk menilai **kualitas** dan **efektivitas** model Random Forest secara objektif.
* **Poin Kunci:** Tekankan bahwa karena adanya **ketidakseimbangan kelas** (ditemukan di Bab 2), kita tidak bisa hanya mengandalkan metrik Akurasi. Kita perlu menggunakan metrik yang lebih mendalam seperti *Confusion Matrix*, *Precision*, dan *Recall*.

---

#### **5.1 Skor Akurasi (Accuracy Score)**

* **Tujuan:** Menampilkan metrik evaluasi yang paling umum sebagai gambaran awal.
* **Penjelasan:** Akurasi mengukur persentase total prediksi yang benar (baik 'Hujan' maupun 'Tidak Hujan') dari keseluruhan data uji.
* **Implementasi:** Tampilkan kode `accuracy_score(y_test, y_pred)` dan hasilnya.
* **Analisis Awal:** Sebutkan skor akurasi (misal: "Model mencapai akurasi 85%"). **Segera** berikan catatan kritis: "Meskipun angka ini tinggi, akurasi bisa menyesatkan. Karena 78% data kita adalah 'Tidak Hujan', model yang hanya menebak 'Tidak Hujan' saja sudah bisa mendapat akurasi 78%. Oleh karena itu, kita perlu analisis lebih lanjut."

---

#### **5.2 Confusion Matrix**

* **Tujuan:** Membedah kinerja model secara visual untuk melihat di mana letak kesalahan model.
* **Penjelasan:** Jelaskan 4 komponen dari *confusion matrix* dalam konteks masalah ini:
    * **True Positive (TP):** Model memprediksi 'Hujan', dan kenyataannya memang 'Hujan'. (Prediksi **tepat**)
    * **True Negative (TN):** Model memprediksi 'Tidak Hujan', dan kenyataannya 'Tidak Hujan'. (Prediksi **tepat**)
    * **False Positive (FP):** Model memprediksi 'Hujan', padahal 'Tidak Hujan'. (Alarm palsu)
    * **False Negative (FN):** Model memprediksi 'Tidak Hujan', padahal kenyataannya 'Hujan'. (Ini adalah kesalahan paling fatal dalam kasus ini).
* **Implementasi & Visualisasi:** Tampilkan kode `confusion_matrix()` dan (yang paling penting) **visualisasikan sebagai *Heatmap*** menggunakan `seaborn.heatmap()`. 
* **Analisis:** "Dari *heatmap*, kita bisa melihat model berhasil memprediksi [X] hari hujan dengan benar (TP), namun masih salah menebak [Y] hari sebagai 'Tidak Hujan' padahal seharusnya 'Hujan' (FN)."

---

#### **5.3 Laporan Klasifikasi (Precision, Recall, F1-Score)**

* **Tujuan:** Mengukur **efektivitas** model dalam memprediksi kelas minoritas ('Hujan'), yang merupakan tujuan utama kita setelah melakukan SMOTE.
* **Penjelasan:** Jelaskan ketiga metrik ini secara sederhana, khususnya untuk kelas 'Hujan':
    * **Precision (Presisi):** Dari semua yang diprediksi 'Hujan' oleh model, berapa persen yang benar-benar 'Hujan'? (Tinggi = Model tidak banyak memberi alarm palsu).
    * **Recall (Sensitivitas):** Dari semua kejadian 'Hujan' yang *sebenarnya*, berapa persen yang berhasil "ditangkap" oleh model? (Tinggi = Model tidak banyak melewatkan kejadian hujan).
    * **F1-Score:** Rata-rata harmonis dari Precision dan Recall. Ini adalah metrik terbaik untuk menilai *keseimbangan* performa model pada data yang tidak seimbang.
* **Implementasi:** Tampilkan kode `classification_report(y_test, y_pred)` dan hasilnya (ini sudah ada di *notebook* Bab 4 Anda).
* **Analisis Kualitas & Efektivitas:** Ini adalah inti dari evaluasi Anda. Fokus pada baris "Hujan". "Meskipun akurasi 85%, **F1-Score** untuk kelas 'Hujan' adalah [misal: 0.64]. Ini menunjukkan bahwa model kita **cukup efektif** dalam memprediksi hujan, jauh lebih baik daripada jika kita tidak menangani *class imbalance*."

---

#### **5.4 Identifikasi Fitur Penting (Feature Importance)**

* **Tujuan:** Menjawab **Rumusan Masalah** dari Bab 1 ("Faktor apa yang paling berpengaruh?"). Ini adalah nilai tambah utama dari Random Forest.
* **Penjelasan:** Jelaskan bahwa Random Forest dapat memberi peringkat fitur mana yang paling banyak berkontribusi dalam membuat keputusan.
* **Implementasi & Visualisasi:** Tampilkan kode untuk mendapatkan `model.feature_importances_` dan **visualisasikan sebagai *horizontal bar chart*** untuk menunjukkan 10 fitur teratas. 
* **Analisis:** "Berdasarkan analisis *feature importance*, ditemukan bahwa faktor paling dominan dalam memprediksi hujan adalah `KelembabanJam3`, diikuti oleh `TekananUdaraJam3` dan `KecepatanAnginKencang`..."

---

**(Paragraf Penutup)**
* Paragraf yang merangkum semua temuan evaluasi.
* Simpulkan bahwa model Random Forest, setelah melalui persiapan data yang tepat (termasuk SMOTE), terbukti **efektif** (tidak hanya akurat) dalam memprediksi hujan.
* Menyatakan bahwa tujuan penelitian telah tercapai, dan wawasan utama akan dirangkum dalam Bab 6 (Kesimpulan).