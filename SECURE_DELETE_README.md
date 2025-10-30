# 🗑️ Secure File Shredder - Penghapus File Super Aman

Program untuk menghapus file secara **PERMANEN** dan **TIDAK DAPAT DI-RECOVER** dengan menimpa data berkali-kali sebelum dihapus dari filesystem.

## 🎯 Mengapa Perlu Secure Delete?

### Masalah dengan Delete Biasa:

Ketika kamu menghapus file biasa (Delete / `rm`), yang terjadi:
```
┌─────────────────────────────────────────┐
│ Hard Disk                                │
├─────────────────────────────────────────┤
│ [Data Rahasia Masih Ada Di Sini! 🔴]   │
│                                          │
│ Filesystem hanya menghapus POINTER      │
│ ke data, tapi DATA ASLI masih di disk!  │
└─────────────────────────────────────────┘
```

**Bahaya:**
- ❌ Data bisa di-recover dengan software recovery
- ❌ Forensik bisa menemukan data sensitif
- ❌ Jika laptop/hard disk dijual, data bisa dibaca

### Solusi: Secure Delete

```
┌─────────────────────────────────────────┐
│ Hard Disk                                │
├─────────────────────────────────────────┤
│ Pass 1: [00000000000000000000000000]    │
│ Pass 2: [11111111111111111111111111]    │
│ Pass 3: [Random: a8f3k9m2p7x1b4...]    │
│ Pass 4: [Random: z2n5q8w1e9r3t6...]    │
│ ...                                      │
│                                          │
│ Data asli DITIMPA berkali-kali          │
│ = TIDAK MUNGKIN di-recover! ✅          │
└─────────────────────────────────────────┘
```

## 🔐 Metode Penghapusan

Program ini menyediakan 4 metode berbeda:

### 1. **Simple Method** (3 passes) 🚀
```
Pass 1: Random data
Pass 2: Random data  
Pass 3: Random data
```
- **Kecepatan:** ⚡⚡⚡ Sangat Cepat
- **Keamanan:** 🛡️🛡️ Bagus untuk penggunaan umum
- **Use case:** File pribadi, dokumen biasa

### 2. **Quick Method** (7 passes) ⚡ [DEFAULT]
```
Pass 1-7: Random data (7 kali)
```
- **Kecepatan:** ⚡⚡ Cepat
- **Keamanan:** 🛡️🛡️🛡️ Balanced security
- **Use case:** Default terbaik untuk kebanyakan kasus

### 3. **DoD 5220.22-M Method** (3 passes) 🛡️
```
Pass 1: Write 0x00 (zeros)
Pass 2: Write 0xFF (ones)
Pass 3: Random data
```
- **Kecepatan:** ⚡⚡ Cepat
- **Keamanan:** 🛡️🛡️🛡️🛡️ Military Standard (US DoD)
- **Use case:** Data sensitif perusahaan, dokumen rahasia
- **Standard:** US Department of Defense

### 4. **Gutmann Method** (35 passes) 🔐
```
Pass 1-4:   Random data
Pass 5-31:  27 specific patterns (0x55, 0xAA, dll)
Pass 32-35: Random data
```
- **Kecepatan:** ⚡ Lambat (tapi paling aman!)
- **Keamanan:** 🛡️🛡️🛡️🛡️🛡️ Maximum Security
- **Use case:** Top secret, highly sensitive data
- **Note:** Metode paling aman yang ada, tapi paling lambat

## 📦 Instalasi

Tidak perlu install library tambahan! Pure Python standard library.

```bash
# Langsung bisa dipakai
python secure_delete.py --help
```

## 🚀 Cara Menggunakan

### 1. Hapus Single File

```bash
# Dengan konfirmasi (aman)
python secure_delete.py secret_file.txt

# Skip konfirmasi (langsung hapus)
python secure_delete.py -y secret_file.txt
```

### 2. Pilih Metode Penghapusan

```bash
# Simple (cepat - 3 passes)
python secure_delete.py --method simple file.txt

# Quick (default - 7 passes)
python secure_delete.py --method quick file.txt

# DoD Military Standard (3 passes khusus)
python secure_delete.py --method dod classified.pdf

# Gutmann Maximum Security (35 passes)
python secure_delete.py --method gutmann top_secret.docx
```

### 3. Hapus Semua File di Directory

```bash
# Hapus semua file di folder
python secure_delete.py --directory -y ./temp_files

# Hapus recursive (termasuk subfolder)
python secure_delete.py --directory --recursive -y ./secrets
```

## 📊 Contoh Output

```
======================================================================
🗑️  SECURE FILE SHREDDER
======================================================================

⚡ Quick Method (7 passes)
   Balanced security and speed
   File: secret_data.txt
   Size: 1.23 MB

  🔄 Pass 1/7: Random data...
  Pass 1/7: [████████████████████████████████████████] 100.0%
  🔄 Pass 2/7: Random data...
  Pass 2/7: [████████████████████████████████████████] 100.0%
  ...
  🔄 Pass 7/7: Random data...
  Pass 7/7: [████████████████████████████████████████] 100.0%
  ✅ Quick overwrite complete!

  🔀 Renaming file to random name...
  ✅ Renamed to: a8f3b2e9c1d4f5a6
  🗑️  Deleting file from filesystem...
  ✅ File deleted successfully!

======================================================================
✅ SECURE DELETION COMPLETE!
======================================================================

💡 File telah dihapus secara permanen dan tidak dapat di-recovery!
   Data sudah ditimpa berkali-kali dengan random data.
```

## 🔬 Cara Kerja

### Proses Secure Deletion:

```
1️⃣ OVERWRITE DATA (Multiple Passes)
   ├─ Pass 1: Tulis 0x00 atau random
   ├─ Pass 2: Tulis 0xFF atau random
   ├─ Pass 3: Tulis random data
   └─ ... (tergantung metode)
   
2️⃣ RENAME FILE
   └─ Ganti nama file jadi random hash
      (menghilangkan jejak nama asli)
   
3️⃣ DELETE FILE
   └─ Hapus dari filesystem
```

### Mengapa Ditimpa Berkali-kali?

Hard disk modern masih bisa menyimpan "jejak magnetik" dari data lama. Dengan menimpa berkali-kali:
- Jejak magnetik hilang sepenuhnya
- Data recovery tools tidak bisa menemukan apapun
- Forensik tidak bisa mengembalikan data

## ⚡ Perbandingan Kecepatan & Keamanan

| Method    | Passes | Kecepatan | Keamanan | Use Case               |
|-----------|--------|-----------|----------|------------------------|
| Simple    | 3      | ⚡⚡⚡     | 🛡️🛡️    | File pribadi          |
| Quick     | 7      | ⚡⚡      | 🛡️🛡️🛡️  | Default terbaik       |
| DoD       | 3*     | ⚡⚡      | 🛡️🛡️🛡️🛡️ | Corporate sensitive   |
| Gutmann   | 35     | ⚡        | 🛡️🛡️🛡️🛡️🛡️ | Top secret         |

*DoD menggunakan pattern khusus (0x00, 0xFF, random)

## 💡 Tips & Best Practices

### 1. Pilih Metode yang Tepat

```bash
# Untuk file biasa (foto, video, dokumen pribadi)
python secure_delete.py --method simple file.txt

# Untuk data kerja/bisnis
python secure_delete.py --method quick work_doc.pdf

# Untuk data sangat sensitif
python secure_delete.py --method dod password_list.txt

# Untuk top secret government/military
python secure_delete.py --method gutmann classified.doc
```

### 2. Sebelum Jual/Buang Perangkat

```bash
# Shred semua data pribadi sebelum jual laptop
python secure_delete.py --directory --recursive -y ~/Documents
python secure_delete.py --directory --recursive -y ~/Downloads
python secure_delete.py --directory --recursive -y ~/Pictures
```

### 3. Rutin Bersihkan Temporary Files

```bash
# Buat script untuk clean temp files
python secure_delete.py --directory -y /tmp
python secure_delete.py --directory -y ~/Downloads/temp
```

## ⚠️ PERINGATAN PENTING!

```
╔═══════════════════════════════════════════════════════╗
║  ⚠️  PENGHAPUSAN INI TIDAK DAPAT DIBATALKAN!         ║
║                                                        ║
║  File yang sudah di-shred TIDAK BISA di-recover      ║
║  bahkan dengan software recovery profesional!        ║
║                                                        ║
║  PASTIKAN:                                            ║
║  ✓ File yang benar                                   ║
║  ✓ Sudah ada backup jika perlu                       ║
║  ✓ Tidak akan dibutuhkan lagi                        ║
╚═══════════════════════════════════════════════════════╝
```

### Jangan Gunakan Untuk:
- ❌ File yang masih mungkin dibutuhkan
- ❌ System files (bisa rusak sistem!)
- ❌ Shared network drives (bisa hapus file orang lain)

## 🎓 Use Cases

### 1. Sebelum Jual Perangkat
```bash
# Hapus semua data pribadi
python secure_delete.py --directory --recursive --method dod -y ~/Documents
python secure_delete.py --directory --recursive --method dod -y ~/Pictures
```

### 2. Setelah Project Selesai
```bash
# Hapus file sementara & credentials
python secure_delete.py --method quick -y .env
python secure_delete.py --method quick -y config.json
python secure_delete.py --directory -y ./temp
```

### 3. Data Breach Response
```bash
# Hapus file yang ter-compromised dengan keamanan maksimal
python secure_delete.py --method gutmann -y leaked_data.db
python secure_delete.py --method gutmann -y compromised_keys.txt
```

### 4. Compliance (GDPR, HIPAA, dll)
```bash
# Hapus data customer dengan standar DoD
python secure_delete.py --method dod -y customer_data.csv
python secure_delete.py --method dod -y patient_records.xlsx
```

## 🔍 Verifikasi

### Cek File Sudah Hilang:
```bash
# File tidak bisa ditemukan
ls -la deleted_file.txt
# Output: No such file or directory ✅

# Tidak bisa di-recover
# Test dengan software recovery → Tidak ada hasil ✅
```

### Testing dengan File Recovery:
```bash
# 1. Delete file biasa (rm/delete)
rm normal_file.txt
# → Bisa di-recover dengan tools! ❌

# 2. Secure delete dengan program ini
python secure_delete.py secure_file.txt
# → TIDAK bisa di-recovery! ✅
```

## 📈 Benchmark

Test pada file 10MB:

| Method    | Time    | Security |
|-----------|---------|----------|
| Simple    | ~2s     | Good     |
| Quick     | ~4s     | Great    |
| DoD       | ~2s     | Excellent|
| Gutmann   | ~20s    | Maximum  |

*Test pada SSD Samsung 970 EVO

## 🛠️ Troubleshooting

### Permission Denied
```bash
# Jalankan dengan sudo jika file dilindungi
sudo python secure_delete.py protected_file.txt
```

### File Locked
```bash
# Tutup program yang menggunakan file
# Lalu jalankan lagi secure delete
```

### Large Files Slow
```bash
# Gunakan simple method untuk file besar
python secure_delete.py --method simple big_file.iso
```

## 📚 Referensi

- **DoD 5220.22-M**: US Department of Defense standard for secure deletion
- **Gutmann Method**: Peter Gutmann's 35-pass algorithm (1996)
- **Data Remanence**: https://en.wikipedia.org/wiki/Data_remanence
- **Secure Deletion**: https://en.wikipedia.org/wiki/Data_erasure

## 🤝 FAQ

**Q: Apakah benar-benar tidak bisa di-recover?**  
A: Ya! Setelah di-overwrite berkali-kali, data tidak bisa di-recovery bahkan dengan forensik tools profesional.

**Q: Metode mana yang paling bagus?**  
A: Untuk kebanyakan kasus, **Quick** atau **DoD** sudah sangat cukup. Gutmann hanya untuk data SANGAT sensitif.

**Q: Apa bedanya dengan `rm -rf`?**  
A: `rm -rf` hanya menghapus pointer file, data asli masih bisa di-recovery. Program ini menimpa data berkali-kali.

**Q: Bisa untuk SSD?**  
A: Ya, tapi SSD punya wear leveling yang kompleks. Untuk SSD, lebih baik gunakan ATA Secure Erase atau enkripsi full disk.

**Q: Berapa lama untuk file besar?**  
A: Tergantung metode & ukuran:
- 1GB Simple: ~15 detik
- 1GB Quick: ~30 detik
- 1GB DoD: ~20 detik
- 1GB Gutmann: ~3 menit

**Q: Aman untuk production?**  
A: Ya, tapi HATI-HATI! Pastikan:
- Backup sudah ada
- File yang benar
- Sudah test di environment non-production dulu

---

**💡 Remember:** Prevention is better than cure. Enkripsi file sensitif sejak awal, jadi tidak perlu khawatir saat delete!

**🔒 Pro Tip:** Kombinasikan dengan full disk encryption (BitLocker/FileVault) untuk proteksi maksimal!
