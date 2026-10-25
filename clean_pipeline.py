import csv
import re
import os
from datetime import datetime

raw_path = r"C:\Users\rifas\.gemini\antigravity\scratch\portfolio_tk\raw_tk.csv"
clean_path_scratch = r"C:\Users\rifas\.gemini\antigravity\scratch\portfolio_tk\tk_nusantara_clean.csv"
clean_path_downloads = r"C:\Users\rifas\Downloads\tk_nusantara_clean.csv"

def normalize_name(name):
    n = name.lower()
    n = re.sub(r'[^a-z0-9]', '', n)
    return n

def clean_height(val, default_val=110):
    if not val:
        return default_val
    s = str(val).lower().strip()
    if 'tidak' in s or 'belum' in s or 'lupa' in s or s == '-':
        return default_val
    if 'meter' in s:
        nums = re.findall(r'\d+(?:[\.,]\d+)?', s)
        if nums:
            return round(float(nums[0].replace(',', '.')) * 100)
    if '1.2' in s or '1,22' in s or '1,43' in s:
        nums = re.findall(r'\d+(?:[\.,]\d+)?', s)
        if nums:
            f = float(nums[0].replace(',', '.'))
            if f < 3:
                return round(f * 100)
    nums = re.findall(r'\d+(?:[\.,]\d+)?', s)
    if nums:
        h = float(nums[0].replace(',', '.'))
        if h < 50:
            return default_val
        return round(h)
    return default_val

def clean_weight(val, default_val=17.0):
    if not val:
        return default_val
    s = str(val).lower().strip()
    if 'tidak' in s or 'belum' in s or 'lupa' in s or s == '-':
        return default_val
    s = s.replace('kilo', 'kg').replace('cm', '')
    nums = re.findall(r'\d+(?:[\.,]\d+)?', s)
    if nums:
        w = float(nums[0].replace(',', '.'))
        if 8 <= w <= 50:
            return round(w, 1)
    return default_val

def clean_birth_date(val, nik, default_date="2020-07-01"):
    if not val:
        val = ""
    s = str(val).strip()
    if s.startswith("2026-05-27"):
        return "2020-05-27"
    if s.startswith("2026-12-13"):
        return "2020-12-13"
    if s.startswith("2026-08-09") or s.startswith("2026-08-06"):
        if nik and len(nik) >= 12:
            pass
        return "2020-08-06"
    if "0021" in s or "3/29" in s:
        return "2021-03-29"
    if not re.match(r'^\d{4}-\d{2}-\d{2}', s):
        # try extract from NIK
        if nik and len(nik) >= 12:
            try:
                d = int(nik[6:8])
                if d > 40: d -= 40
                m = int(nik[8:10])
                y = int(nik[10:12]) + 2000
                return f"{y:04d}-{m:02d}-{d:02d}"
            except:
                pass
        return default_date
    return s[:10]

def clean_birth_order(val):
    s = str(val).lower().strip()
    mapping = {
        'satu': 1, 'ke 1': 1, '1 (satu)': 1, 'ke satu': 1, 'anak ke 1': 1, '1': 1,
        'dua': 2, 'ke 2': 2, '2 (dua)': 2, 'kedua': 2, 'anak ke dua(2)': 2, 'anak ke 2': 2, '2': 2,
        'tiga': 3, 'ke 3': 3, '3 (tiga)': 3, '3 ( tiga )': 3, '3': 3,
        'empat': 4, 'ke 4': 4, '4': 4,
        'lima': 5, 'ke 5': 5, '5': 5
    }
    for k, v in mapping.items():
        if k in s:
            return v
    nums = re.findall(r'\d+', s)
    if nums:
        return int(nums[0])
    return 1

def clean_job(val, is_father=True):
    s = str(val).lower().strip()
    if not s or s in ['-', 'tidak ada', 'tidak tau', 'almarhum', 'sudah almarhum', '_', 'udh pisah jdi ga tau']:
        return "Almarhum / Tidak Tercatat" if "almarhum" in s or "alm" in s else "Lainnya / Tidak Tercatat"
    if 'buruh' in s or 'bangunan' in s or 'butuh harian' in s or 'kuli' in s:
        return "Buruh Harian Lepas"
    if 'karyawan swasta' in s or 'pegawai swasta' in s or 'karyawan swata' in s or 'pabrik' in s or 'industri' in s:
        return "Karyawan Swasta / Pabrik"
    if 'wiraswasta' in s or 'pedagang' in s or 'catering' in s or 'jualan' in s or 'konfeksi' in s or 'pengrajin' in s:
        return "Wiraswasta / Pedagang"
    if 'asn' in s or 'pegawai negeri' in s or 'pns' in s:
        return "PNS / ASN"
    if 'guru' in s or 'ngajar' in s:
        return "Guru / Tenaga Pendidik"
    if 'security' in s or 'scurity' in s or 'satpam' in s:
        return "Petugas Keamanan (Satpam)"
    if 'supir' in s or 'sopir' in s or 'ojol' in s or 'shope food' in s:
        return "Pengemudi / Driver Ojol"
    if 'ibu rumah tangga' in s or 'irt' in s or 'mengurus rumah tangga' in s or 'i.r.t' in s:
        return "Ibu Rumah Tangga (IRT)"
    return "Wiraswasta / Lainnya" if is_father else "Ibu Rumah Tangga (IRT)"

def clean_education(val):
    s = str(val).upper().strip()
    if not s or s in ['-', 'TIDAK TAU', 'TIDAK PUNYA', '_']:
        return "SMA / SMK Sederajat"
    if 'S1' in s or 'SARJANA' in s:
        return "S1 / Sarjana"
    if 'D4' in s or 'D3' in s or 'D1' in s or 'DIPLOMA' in s:
        return "Diploma (D1-D4)"
    if 'SMK' in s or 'SMA' in s or 'SLTA' in s or 'SMU' in s:
        return "SMA / SMK Sederajat"
    if 'SMP' in s or 'SLTP' in s or 'MTS' in s:
        return "SMP Sederajat"
    if 'SD' in s:
        return "SD Sederajat"
    return "SMA / SMK Sederajat"

def clean_channel(val):
    s = str(val).strip()
    if 'Rekomendasi' in s:
        return "Rekomendasi Teman/Keluarga"
    if 'Spanduk' in s or 'Iklan' in s:
        return "Iklan / Spanduk"
    return "Lainnya"

def clean_health(val):
    s = str(val).strip()
    if not s or s.lower() in ['tidak ada', 'tidak', 'ga ada', 'gaada', '-', 'sehat', 'aman', 'tidak punya apergi', 'tidak punya alergi', 'baik tidak ada alergi', 'normal', 'sehat jasmani rohani', '0']:
        return "Sehat / Tidak Ada Alergi"
    return s

def extract_domicile(val):
    s = str(val).lower()
    kel = "Cihanjuang"
    if "sariwangi" in s:
        kel = "Sariwangi"
    elif "cibabat" in s or "cimahi" in s:
        kel = "Cibabat"
    elif "cihanjuang rahayu" in s:
        kel = "Cihanjuang Rahayu"
    elif "ciwaruga" in s or "parigilame" in s:
        kel = "Ciwaruga"
    elif "karyawangi" in s:
        kel = "Karyawangi"
    elif "margaasih" in s:
        kel = "Margaasih"
    
    kec = "Parongpong"
    if kel in ["Cibabat"]:
        kec = "Cimahi Utara"
    elif kel in ["Margaasih"]:
        kec = "Margaasih"
    
    return kel, kec

# Process data
students = {}

with open(raw_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name_raw = row['Nama Lengkap Calon Murid (Sesuai Akta Kelahiran)'].strip()
        if not name_raw:
            continue
        key = normalize_name(name_raw)
        
        # We prefer row with more filled columns or later timestamp
        if key not in students:
            students[key] = row
        else:
            # Check if this row has 'Pilihan Kelas' filled
            curr_class = students[key].get('Pilihan Kelas', '').strip()
            new_class = row.get('Pilihan Kelas', '').strip()
            if not curr_class and new_class:
                students[key] = row
            elif new_class and row['Timestamp'] > students[key]['Timestamp']:
                students[key] = row

clean_rows = []
for idx, (k, r) in enumerate(students.items(), 1):
    raw_name = r['Nama Lengkap Calon Murid (Sesuai Akta Kelahiran)'].strip()
    name_clean = " ".join([w.capitalize() for w in raw_name.split()])
    gender = r['Jenis Kelamin'].strip()
    if not gender or gender not in ['Laki-laki', 'Perempuan']:
        gender = 'Laki-laki' if any(m in name_clean.lower() for m in ['muhammad', 'athaf', 'm.', 'adam', 'riski', 'raffa', 'bilal', 'firza', 'altezza', 'rifki', 'arkan', 'rafa', 'kaiden', 'hasbi', 'reyhan', 'rauf', 'rama', 'dani', 'prabu']) else 'Perempuan'
    
    nik = re.sub(r'[^0-9]', '', r.get('Nomor Induk Kependudukan (NIK) Anak: ', ''))
    bdate = clean_birth_date(r['Tanggal Lahir Calon Murid'], nik)
    
    # Calculate age as of July 2026
    byear = int(bdate[:4])
    bmonth = int(bdate[5:7])
    age_years = round(2026.5 - (byear + bmonth/12.0), 1)
    
    pilihan_kelas = r.get('Pilihan Kelas', '').strip()
    if not pilihan_kelas:
        pilihan_kelas = 'Kelas B' if age_years >= 5.0 else 'Kelas A'
    
    h_cm = clean_height(r.get('Tinggi Badan', ''))
    w_kg = clean_weight(r.get('Berat Badan', ''))
    anak_ke = clean_birth_order(r.get('Anak Ke- : ', '1'))
    
    f_job = clean_job(r.get('Pekerjaan Ayah', ''), is_father=True)
    m_job = clean_job(r.get('Pekerjaan Ibu', ''), is_father=False)
    
    f_edu = clean_education(r.get('Pendidikan Ayah', ''))
    m_edu = clean_education(r.get('Pendidikan Terakhir Ibu', ''))
    
    channel = clean_channel(r.get('Dari mana Anda mengetahui tentang TK Nusantara?', ''))
    health = clean_health(r.get('Informasi Kesehatan dan Alergi Calon Murid (Jika Ada)', ''))
    kel, kec = extract_domicile(r.get('Alamat Lengkap (Termasuk RT/RW, Kelurahan, dan Kecamatan)', ''))
    
    clean_rows.append({
        'ID_Siswa': f"TKN-{idx:03d}",
        'Nama_Siswa': name_clean,
        'Jenis_Kelamin': gender,
        'Tanggal_Lahir': bdate,
        'Usia_Tahun': age_years,
        'Pilihan_Kelas': pilihan_kelas,
        'Tinggi_Badan_cm': h_cm,
        'Berat_Badan_kg': w_kg,
        'Anak_Ke': anak_ke,
        'Kondisi_Kesehatan_Alergi': health,
        'Pekerjaan_Ayah': f_job,
        'Pendidikan_Ayah': f_edu,
        'Pekerjaan_Ibu': m_job,
        'Pendidikan_Ibu': m_edu,
        'Saluran_Pemasaran': channel,
        'Kelurahan_Domisili': kel,
        'Kecamatan_Domisili': kec,
        'Tanggal_Pendaftaran': r['Timestamp'][:10]
    })

fieldnames = [
    'ID_Siswa', 'Nama_Siswa', 'Jenis_Kelamin', 'Tanggal_Lahir', 'Usia_Tahun', 
    'Pilihan_Kelas', 'Tinggi_Badan_cm', 'Berat_Badan_kg', 'Anak_Ke', 
    'Kondisi_Kesehatan_Alergi', 'Pekerjaan_Ayah', 'Pendidikan_Ayah', 
    'Pekerjaan_Ibu', 'Pendidikan_Ibu', 'Saluran_Pemasaran', 
    'Kelurahan_Domisili', 'Kecamatan_Domisili', 'Tanggal_Pendaftaran'
]

# Write to scratch
with open(clean_path_scratch, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(clean_rows)

print(f"BERHASIL! Total data unik bersih: {len(clean_rows)} siswa disimpan di {clean_path_scratch}")

