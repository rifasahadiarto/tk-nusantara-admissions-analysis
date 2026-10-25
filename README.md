# 🎓 TK Nusantara — Admissions Analytics & Sliding-Scale Tuition Subsidy Modeling

![Tableau](https://img.shields.io/badge/Tableau-Public-E97627?style=for-the-badge&logo=Tableau&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=Python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Advanced%20Queries-4479A1?style=for-the-badge&logo=PostgreSQL&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-Power%20ETL-217346?style=for-the-badge&logo=Microsoft-Excel&logoColor=white)

---

## 📌 Executive Summary

Proyek ini menganalisis **285 data mentah pendaftaran siswa baru** di TK Nusantara (Kecamatan Parongpong, Kabupaten Bandung Barat). 

Karena institusi ini menerapkan **kebijakan biaya SPP berbasis kemampuan finansial (Skema Subsidi Silang)**, analisis ini bertujuan untuk:
1. Melakukan audit dan pembersihan data operasional Google Form yang sarat duplikasi serta inkonsistensi input manusia.
2. Memetakan profil sosio-ekonomi orang tua dan beban tanggungan anak untuk menentukan **kategori penerima subsidi SPP yang tepat sasaran**.
3. Menyajikan **Executive Business Intelligence Dashboard di Tableau** untuk membantu yayasan dan kepala sekolah dalam perencanaan kapasitas kelas dan alokasi anggaran promosi.

---

## 🔍 Masalah Bisnis & Kebutuhan Analisis

1. **Inkonsistensi & Duplikasi Data Lapangan:**  
   Pihak sekolah memperbarui formulir pendaftaran di tengah periode penerimaan murid (menambahkan pertanyaan NIK, kelas, dan pendidikan orang tua), mengakibatkan banyak wali murid mendaftar ulang berkali-kali.
2. **Kebutuhan Kebijakan Subsidi SPP yang Adil:**  
   Sekolah membutuhkan kriteria objektif berbasis data (pekerjaan orang tua, pendidikan, dan urutan kelahiran/tanggungan anak) untuk memisahkan siswa kategori **Subsidi Penuh**, **Subsidi Parsial**, dan **Mandiri/Reguler**.
3. **Ketidakseimbangan Kapasitas Kelas:**  
   Perlu validasi apakah minat masuk Kelas A dan Kelas B seimbang dengan rasio ketersediaan guru.

---

## 🛠️ Alur Kerja & Pipeline Data (ETL)

```
[Google Form Raw Data]
        │ (285 Baris Data Mentah & Kotor)
        ▼
[Python Cleaning & Sanitization Engine]
        ├── Deduplikasi berbasis Nama & NIK (Mempertahankan data terupdate Agustus)
        ├── Normalisasi Unit Numerik (Tinggi: cm, Berat: kg, Usia per Juli 2026)
        ├── Standarisasi Entitas Teks (Pekerjaan, Pendidikan, Domisili Wilayah)
        ▼
[Clean Structured Storage]
        ├── CSV Format (104 Siswa Unik Siap Analisis)
        └── Styled Excel (.xlsx) dengan Conditional Formatting & Visual Hierarchy
        ▼
[Interactive Analytics & BI]
        ├── Koleksi Query SQL Analitis (Window Functions, CTE, Case When)
        └── Tableau Public Executive Dashboard
```

---

## 📊 Temuan Kunci (Key Business Insights)

| No | Metrik / Aspek | Temuan Data | Dampak Bisnis |
| :---: | :--- | :--- | :--- |
| **1** | **Dominasi Saluran Promosi** | **87.5% (91 siswa)** mendaftar dari **Rekomendasi Teman & Keluarga** (*Word-of-Mouth*). | Biaya iklan luar ruang (spanduk/brosur) tidak efektif dan dapat dialihkan ke program apresiasi/insentif orang tua murid lama. |
| **2** | **Kebutuhan Subsidi SPP** | **57.7% (60 ayah)** bekerja sebagai **Buruh Harian Lepas**, dan **31.7% (33 siswa)** adalah anak ke-3 hingga ke-5. | Menandakan tingginya beban ekonomi keluarga; skema subsidi silang sangat krusial agar tidak terjadi putus sekolah di tengah jalan. |
| **3** | **Zonasi & Radius Jangkauan** | **79.8% (83 siswa)** berasal murni dari **Desa Cihanjuang**, dengan penetrasi kecil ke Cibabat (10 siswa) dan Sariwangi (8 siswa). | TK Nusantara berstatus *hyper-local champion*, radius pasar utama berada dalam jangkauan < 3 km. |
| **4** | **Ketimpangan Kapasitas Kelas** | **76% pendaftar** memilih **Kelas B** (usia 5–6 tahun), sementara Kelas A hanya 24%. | Beban kapasitas guru dan fasilitas terpusat di Kelas B; sekolah wajib membagi rombel Kelas B menjadi 2 sesi belajar. |

---

## 💡 Rekomendasi Strategis untuk Yayasan

1. **Implementasi Matriks Kategori SPP Subsidi Silang:**
   * **Prioritas 1 (Subsidi Penuh):** Siswa yatim/piatu ATAU ayah buruh harian lepas dengan tanggungan $\ge 3$ anak.
   * **Prioritas 2 (Subsidi Parsial / Cicilan Fleksibel):** Pekerja harian lepas dengan $\le 2$ anak, diberikan opsi cicilan SPP mingguan.
   * **Kategori Mandiri / Donatur:** Wali murid ASN/PNS, Guru, dan Sarjana dikenakan tarif standar penuh untuk mendanai subsidi silang.
2. **Alokasi Kelas & Guru:**
   * Membuka 2 rombongan belajar (rombel) untuk Kelas B guna menjaga rasio ideal 1 guru : 15 murid.
3. **Protokol Keselamatan Medis (SOP Alert):**
   * Memberikan catatan penanda khusus pada buku absensi guru untuk siswa dengan riwayat kejang saat demam tinggi (*febrile convulsion*) dan alergi dingin/telur.

---

## 📂 Struktur Repositori

```
├── README.md                 # Dokumentasi lengkap studi kasus & metodologi
├── tk_nusantara_clean.csv    # Dataset final bersih (104 siswa unik)
├── tk_nusantara_rapi.xlsx    # Dataset berformat korporat (.xlsx) dengan auto-styling
├── clean_pipeline.py         # Skrip otomasi pembersihan data & penanganan anomali (Python)
├── create_styled_excel.py    # Skrip formatting Excel openpyxl dengan conditional formatting
├── analysis_queries.sql      # Kumpulan query SQL analitis (Window function, aggregation)
└── raw_tk.csv                # Data mentah simulasi sebelum pembersihan
```

---

## 👤 Author & Profil Analis

* **Nama:** Rifasa Hadiarto
* **Sertifikasi:** Certified Data Analyst — Badan Nasional Sertifikasi Profesi (BNSP)
* **Keahlian:** Business Intelligence, Data Cleaning (Python/SQL), Dashboard Design (Tableau & Looker Studio), Process Automation (n8n).
