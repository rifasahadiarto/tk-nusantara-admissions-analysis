-- ====================================================================
-- PROJECT: TK Nusantara - Admissions & Tuition Fee Subsidy Analysis
-- AUTHOR : Rifasa Hadiarto
-- ROLE   : Data Analyst
-- TARGET : Database PostgreSQL / MySQL / SQLite
-- ====================================================================

-- 1. IDENTIFIKASI DATA DUPLIKAT DENGAN WINDOW FUNCTION
-- Mengambil pendaftaran terbaru untuk setiap calon siswa
WITH RankedRegistrations AS (
    SELECT 
        id_siswa,
        nama_siswa,
        jenis_kelamin,
        tanggal_lahir,
        usia_tahun,
        pilihan_kelas,
        pekerjaan_ayah,
        pendidikan_ayah,
        anak_ke,
        kelurahan_domisili,
        ROW_NUMBER() OVER (
            PARTITION BY LOWER(TRIM(nama_siswa)) 
            ORDER BY tanggal_pendaftaran DESC
        ) as rn
    FROM raw_pendaftaran_tk
)
SELECT * 
FROM RankedRegistrations
WHERE rn = 1;


-- 2. ANALISIS AKUISISI PEMASARAN (MARKETING CHANNEL EFFECTIVENESS)
-- Menghitung persentase saluran informasi yang paling dominan
SELECT 
    saluran_pemasaran,
    COUNT(*) AS total_pendaftar,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS persentase_kontribusi
FROM students_clean
GROUP BY saluran_pemasaran
ORDER BY total_pendaftar DESC;


-- 3. ANALISIS KAPASITAS KELAS & KESIAPAN USIA SISWA
-- Memeriksa rata-rata usia dan rasio pendaftar Kelas A vs Kelas B
SELECT 
    pilihan_kelas,
    COUNT(*) AS total_siswa,
    ROUND(AVG(usia_tahun), 2) AS rata_rata_usia,
    MIN(usia_tahun) AS usia_termuda,
    MAX(usia_tahun) AS usia_tertua
FROM students_clean
GROUP BY pilihan_kelas
ORDER BY pilihan_kelas ASC;


-- 4. ANALISIS KELAYAKAN SUBSIDI SPP (SOSIO-EKONOMI & BEBAN KELUARGA)
-- Segmentasi calon penerima subsidi silang berdasarkan pekerjaan ayah dan jumlah tanggungan
SELECT 
    nama_siswa,
    pilihan_kelas,
    pekerjaan_ayah,
    pendidikan_ayah,
    anak_ke,
    CASE 
        WHEN LOWER(pekerjaan_ayah) LIKE '%almarhum%' OR LOWER(pekerjaan_ayah) LIKE '%tidak ada%' THEN 'Prioritas 1: Subsidi Penuh (Yatim/Dhuafa)'
        WHEN pekerjaan_ayah = 'Buruh Harian Lepas' AND anak_ke >= 3 THEN 'Prioritas 1: Subsidi Penuh (Rentan Finansial)'
        WHEN pekerjaan_ayah = 'Buruh Harian Lepas' OR anak_ke >= 3 THEN 'Prioritas 2: Subsidi Parsial (Keringanan Biaya)'
        WHEN pekerjaan_ayah IN ('PNS / ASN', 'Guru / Tenaga Pendidik') OR pendidikan_ayah = 'S1 / Sarjana' THEN 'Kategori Mandiri / Donatur Subsidi Silang'
        ELSE 'Kategori Reguler'
    END AS rekomendasi_skema_spp
FROM students_clean
ORDER BY anak_ke DESC, pekerjaan_ayah ASC;


-- 5. REKAPITULASI KELOMPOK SUBSIDI SPP UNTUK MANAJEMEN YAYASAN
SELECT 
    CASE 
        WHEN LOWER(pekerjaan_ayah) LIKE '%almarhum%' OR (pekerjaan_ayah = 'Buruh Harian Lepas' AND anak_ke >= 3) THEN 'Subsidi Penuh'
        WHEN pekerjaan_ayah = 'Buruh Harian Lepas' OR anak_ke >= 3 THEN 'Subsidi Sebagian'
        WHEN pekerjaan_ayah IN ('PNS / ASN', 'Guru / Tenaga Pendidik') OR pendidikan_ayah = 'S1 / Sarjana' THEN 'Mandiri / Donatur'
        ELSE 'Reguler'
    END AS kategori_spp,
    COUNT(*) AS jumlah_murid,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS persentase_total
FROM students_clean
GROUP BY 1
ORDER BY jumlah_murid DESC;


-- 6. ANALISIS ZONASI & JANGKAUAN GEOGRAFIS (RADIUS PENDAFTAR)
SELECT 
    kelurahan_domisili,
    kecamatan_domisili,
    COUNT(*) AS jumlah_siswa,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pangsa_pasar_persen
FROM students_clean
GROUP BY kelurahan_domisili, kecamatan_domisili
ORDER BY jumlah_siswa DESC;


-- 7. DETEKSI DINI & MITIGASI RISIKO MEDIS SISWA BARU
SELECT 
    id_siswa,
    nama_siswa,
    pilihan_kelas,
    kondisi_kesehatan_alergi
FROM students_clean
WHERE kondisi_kesehatan_alergi NOT LIKE '%Sehat%'
ORDER BY pilihan_kelas ASC;
