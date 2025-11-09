3.4 Pemisahan Dataset (Data Splitting)
Penjelasan: Sebagai langkah persiapan akhir sebelum pemodelan, dataset yang sudah bersih ini perlu dibagi menjadi dua bagian: data latih (training set) dan data uji (testing set).

Data Latih (80%): Akan digunakan untuk "mengajari" model Random Forest.

Data Uji (20%): Akan "disembunyikan" dari model dan hanya digunakan satu kali di akhir untuk menguji seberapa baik kinerjanya pada data baru. Pertama, kita pisahkan antara fitur (X) dan target (y).

Implementasi: (Tampilkan kode untuk mendefinisikan X dan y) (Tampilkan kode train_test_split Anda di sini)

3.5 Penanganan Ketidakseimbangan Kelas (SMOTE)
Penjelasan: Seperti yang telah diidentifikasi pada Bab 2 (Gambar 2.9), dataset kita memiliki masalah class imbalance yang signifikan. Untuk memastikan model tidak bias dan mampu memprediksi kelas minoritas ('Hujan'), kita akan menerapkan teknik oversampling bernama SMOTE.

Catatan Penting: Untuk mencegah data leakage dan evaluasi yang bias, SMOTE hanya diterapkan pada data latih (X_train dan y_train) yang baru saja kita buat. Data uji (X_test dan y_test) dibiarkan apa adanya (tidak seimbang) untuk mensimulasikan kondisi data di dunia nyata.

Implementasi: (Tampilkan kode SMOTE Anda di sini, yang di-fit dan di-transform hanya pada X_train dan y_train).

(Paragraf Penutup Bab 3) Setelah melalui seluruh proses, kita kini memiliki set data latih yang bersih dan seimbang (X_train_smote, y_train_smote) serta set data uji (X_test, y_test). Data ini telah siap sepenuhnya untuk digunakan pada Bab 4: Modelling.