# 🔐 File Encryptor - Trapdoor Function Demo

Program enkripsi file yang mendemonstrasikan konsep **trapdoor function** menggunakan RSA dan AES.

## 🎯 Apa itu Trapdoor Function?

**Trapdoor function** adalah fungsi matematika yang:
- ✅ **MUDAH** dihitung dalam satu arah
- ❌ **SANGAT SULIT** dihitung dalam arah sebaliknya (tanpa informasi rahasia)

### Analogi Sederhana:
```
Perkalian Bilangan Prima (Trapdoor Function):
├─ Arah Mudah: 89 × 97 = 8,633 ✓
└─ Arah Sulit: 8,633 = ? × ? (coba cari faktornya!) ✗
```

## 🏗️ Arsitektur Program

Program ini menggunakan **Hybrid Encryption** untuk efisiensi:

```
┌─────────────────────────────────────────────────────┐
│              HYBRID ENCRYPTION                       │
├─────────────────────────────────────────────────────┤
│                                                       │
│  1. RSA (Trapdoor Function)                          │
│     └─ Enkripsi kunci AES (hanya 32 bytes)          │
│     └─ Public key: enkripsi MUDAH                    │
│     └─ Private key: dekripsi BUTUH SECRET            │
│                                                       │
│  2. AES (Symmetric Encryption)                       │
│     └─ Enkripsi file (cepat untuk data besar)       │
│     └─ Proses chunk 64KB (efisien untuk file besar) │
│                                                       │
└─────────────────────────────────────────────────────┘
```

### Kenapa Hybrid?
- **RSA** lambat untuk data besar, tapi aman untuk kunci kecil
- **AES** cepat untuk data besar, tapi butuh cara aman kirim kunci
- **Solusi**: AES enkripsi file, RSA enkripsi kunci AES!

## 📦 Instalasi

```bash
# Install library yang diperlukan
pip install cryptography
```

## 🚀 Cara Menggunakan

### 1. Generate Key Pair (Sekali saja)

```bash
python file_encryptor.py generate
```

Output:
- `private_key.pem` - 🔒 **RAHASIA!** Jangan dibagikan
- `public_key.pem` - 🔓 Boleh dibagikan ke siapa saja

### 2. Enkripsi File

```bash
# Enkripsi file apapun
python file_encryptor.py encrypt rahasia.txt rahasia.enc
python file_encryptor.py encrypt dokumen.pdf dokumen.enc
python file_encryptor.py encrypt video.mp4 video.enc
```

**Proses:**
1. Generate random AES key (256-bit)
2. Enkripsi file dengan AES (cepat!)
3. Enkripsi AES key dengan RSA public key (trapdoor!)
4. Simpan semuanya dalam satu file

### 3. Dekripsi File

```bash
# Dekripsi file (butuh private key!)
python file_encryptor.py decrypt rahasia.enc rahasia_asli.txt
```

**Proses:**
1. Load file terenkripsi
2. Dekripsi AES key dengan RSA private key (butuh secret!)
3. Dekripsi file dengan AES key
4. Simpan file hasil dekripsi

## 🔬 Contoh Demo

```bash
# 1. Generate keys
python file_encryptor.py generate

# 2. Buat file test
echo "Data rahasia: password123" > secret.txt

# 3. Enkripsi
python file_encryptor.py encrypt secret.txt secret.enc

# 4. Lihat file terenkripsi (tidak bisa dibaca!)
cat secret.enc

# 5. Dekripsi
python file_encryptor.py decrypt secret.enc secret_decrypted.txt

# 6. Verifikasi
cat secret_decrypted.txt
```

## ⚡ Performa untuk File Besar

Program ini dioptimasi untuk file besar:
- ✅ Proses chunk 64KB (tidak load seluruh file ke memory)
- ✅ Tested dengan file 5MB+
- ✅ Bisa handle file ratusan MB hingga GB

**Test dengan file 5MB:**
```bash
# Buat file 5MB
dd if=/dev/urandom of=big_file.bin bs=1M count=5

# Enkripsi (cepat!)
python file_encryptor.py encrypt big_file.bin big_file.enc

# Dekripsi
python file_encryptor.py decrypt big_file.enc big_file_restored.bin

# Verifikasi integrity
md5sum big_file.bin big_file_restored.bin
```

## 🔐 Keamanan

### Level Keamanan:
- **RSA 2048-bit**: Standar industri, aman hingga 2030+
- **AES 256-bit**: Standar militer (military-grade)
- **Padding OAEP**: Mencegah serangan chosen ciphertext

### Demonstrasi Trapdoor:
```python
# ✓ MUDAH: Enkripsi dengan public key
encrypted = public_key.encrypt(data)

# ✗ MUSTAHIL: Dekripsi tanpa private key
# Butuh 2^128 operasi = lebih lama dari umur alam semesta!
decrypted = ??? # Tidak ada cara!

# ✓ MUDAH: Dekripsi dengan private key (rahasia)
decrypted = private_key.decrypt(encrypted)
```

## 🎓 Konsep yang Diterapkan

1. **Trapdoor Function (RSA)**
   - Public key: Siapa saja bisa enkripsi
   - Private key: Hanya pemilik bisa dekripsi
   
2. **Symmetric Encryption (AES)**
   - Satu kunci untuk enkripsi & dekripsi
   - Sangat cepat untuk data besar
   
3. **Hybrid Encryption**
   - Best of both worlds
   - Keamanan RSA + kecepatan AES

## ⚠️ Peringatan

1. **Private key HARUS dijaga!**
   - Jangan upload ke internet
   - Jangan share ke orang lain
   - Jika hilang, data tidak bisa dikembalikan
   
2. **Password protect private key**
   - Default password: `password123`
   - Ganti dengan password kuat Anda!
   
3. **Backup keys**
   - Simpan private key di tempat aman
   - Backup di USB/hard disk terpisah

## 🎯 Use Cases

✅ Enkripsi dokumen sensitif
✅ Backup data terenkripsi
✅ Kirim file rahasia (kirim file .enc + share public key)
✅ Proteksi file besar (video, database, dll)
✅ Demo konsep kriptografi untuk pembelajaran

## 🧪 Testing

```bash
# Test enkripsi-dekripsi
echo "Hello World" > test.txt
python file_encryptor.py encrypt test.txt test.enc
python file_encryptor.py decrypt test.enc test2.txt
diff test.txt test2.txt  # Harus identik!

# Test file besar
dd if=/dev/urandom of=large.bin bs=1M count=10
python file_encryptor.py encrypt large.bin large.enc
python file_encryptor.py decrypt large.enc large2.bin
md5sum large.bin large2.bin  # Checksum harus sama!
```

## 📚 Referensi

- RSA Cryptosystem: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
- AES Encryption: https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
- Hybrid Cryptosystem: https://en.wikipedia.org/wiki/Hybrid_cryptosystem
- Python Cryptography: https://cryptography.io/

## 🤝 Kontribusi

Program ini dibuat untuk tujuan edukasi dan demonstrasi konsep trapdoor function.

---

**💡 Ingat:** Trapdoor function adalah fondasi dari kriptografi modern. 
Enkripsi mudah, dekripsi mustahil (tanpa secret) - itulah yang membuat internet aman! 🔒
"# file_encryptor" 
