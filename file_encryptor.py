#!/usr/bin/env python3
"""
File Encryptor menggunakan Trapdoor Function (RSA + AES)
Untuk file besar, kita gunakan hybrid encryption:
- RSA (trapdoor function) untuk enkripsi kunci AES
- AES untuk enkripsi file (lebih cepat untuk data besar)
"""

import os
import sys
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import json

class FileEncryptor:
    def __init__(self):
        self.backend = default_backend()
        self.chunk_size = 64 * 1024  # 64KB chunks untuk file besar
    
    def generate_key_pair(self, key_size=2048):
        """
        Generate pasangan kunci RSA (trapdoor function)
        - Public key: untuk enkripsi (mudah)
        - Private key: untuk dekripsi (butuh informasi rahasia)
        """
        print(f"🔑 Generating RSA key pair ({key_size} bit)...")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=self.backend
        )
        public_key = private_key.public_key()
        print("✅ Key pair generated!")
        return private_key, public_key
    
    def save_keys(self, private_key, public_key, private_path="private_key.pem", public_path="public_key.pem"):
        """Simpan kunci ke file"""
        # Simpan private key (RAHASIA!)
        with open(private_path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(b'password123')
            ))
        print(f"🔒 Private key saved to: {private_path}")
        
        # Simpan public key (bisa dibagikan)
        with open(public_path, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        print(f"🔓 Public key saved to: {public_path}")
    
    def load_private_key(self, path="private_key.pem", password=b'password123'):
        """Load private key dari file"""
        with open(path, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=password,
                backend=self.backend
            )
        return private_key
    
    def load_public_key(self, path="public_key.pem"):
        """Load public key dari file"""
        with open(path, 'rb') as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
                backend=self.backend
            )
        return public_key
    
    def encrypt_file(self, input_file, output_file, public_key):
        """
        Enkripsi file menggunakan hybrid encryption:
        1. Generate random AES key (symmetric key)
        2. Enkripsi file dengan AES (cepat untuk file besar)
        3. Enkripsi AES key dengan RSA (trapdoor function)
        """
        print(f"\n🔐 Encrypting: {input_file}")
        
        # 1. Generate random AES key (256-bit)
        aes_key = os.urandom(32)
        iv = os.urandom(16)  # Initialization vector
        
        # 2. Enkripsi file dengan AES
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        
        file_size = os.path.getsize(input_file)
        encrypted_chunks = []
        
        print(f"📊 File size: {file_size:,} bytes")
        print("⏳ Encrypting with AES...")
        
        with open(input_file, 'rb') as f:
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                
                # Padding untuk chunk terakhir
                if len(chunk) % 16 != 0:
                    chunk += b'\x00' * (16 - len(chunk) % 16)
                
                encrypted_chunks.append(encryptor.update(chunk))
        
        encrypted_chunks.append(encryptor.finalize())
        encrypted_data = b''.join(encrypted_chunks)
        
        # 3. Enkripsi AES key dengan RSA (TRAPDOOR FUNCTION)
        print("🔒 Encrypting AES key with RSA (trapdoor function)...")
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # 4. Simpan semua ke file output
        output_data = {
            'encrypted_key': base64.b64encode(encrypted_aes_key).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'file_size': file_size,
            'encrypted_data': base64.b64encode(encrypted_data).decode('utf-8')
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f)
        
        print(f"✅ File encrypted successfully!")
        print(f"📁 Output: {output_file}")
        print(f"💡 AES key dienkripsi dengan RSA - hanya private key yang bisa dekripsi!")
    
    def decrypt_file(self, input_file, output_file, private_key):
        """
        Dekripsi file:
        1. Dekripsi AES key dengan RSA private key (trapdoor secret)
        2. Dekripsi file dengan AES key yang sudah didekripsi
        """
        print(f"\n🔓 Decrypting: {input_file}")
        
        # 1. Load encrypted data
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        encrypted_aes_key = base64.b64decode(data['encrypted_key'])
        iv = base64.b64decode(data['iv'])
        file_size = data['file_size']
        encrypted_data = base64.b64decode(data['encrypted_data'])
        
        # 2. Dekripsi AES key dengan RSA private key (TRAPDOOR SECRET)
        print("🔑 Decrypting AES key with RSA private key...")
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # 3. Dekripsi file dengan AES
        print("⏳ Decrypting file with AES...")
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Buang padding dan ambil hanya sesuai file_size asli
        decrypted_data = decrypted_data[:file_size]
        
        # 4. Simpan file hasil dekripsi
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
        
        print(f"✅ File decrypted successfully!")
        print(f"📁 Output: {output_file}")


def main():
    encryptor = FileEncryptor()
    
    print("=" * 60)
    print("🔐 FILE ENCRYPTOR - Trapdoor Function Demo")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  1. Generate keys:")
        print("     python file_encryptor.py generate")
        print("\n  2. Encrypt file:")
        print("     python file_encryptor.py encrypt <input_file> <output_file>")
        print("\n  3. Decrypt file:")
        print("     python file_encryptor.py decrypt <encrypted_file> <output_file>")
        return
    
    command = sys.argv[1]
    
    if command == "generate":
        # Generate key pair
        private_key, public_key = encryptor.generate_key_pair()
        encryptor.save_keys(private_key, public_key)
        print("\n💡 Penjelasan Trapdoor Function:")
        print("   - Public key (🔓): Siapa saja bisa enkripsi (MUDAH)")
        print("   - Private key (🔒): Hanya pemilik bisa dekripsi (BUTUH SECRET)")
        print("   - Tanpa private key, dekripsi hampir MUSTAHIL!")
    
    elif command == "encrypt":
        if len(sys.argv) < 4:
            print("❌ Error: Specify input and output files")
            print("   Example: python file_encryptor.py encrypt myfile.txt myfile.enc")
            return
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        
        if not os.path.exists(input_file):
            print(f"❌ Error: File '{input_file}' not found")
            return
        
        # Load public key
        if not os.path.exists("public_key.pem"):
            print("❌ Error: Public key not found. Run 'generate' first.")
            return
        
        public_key = encryptor.load_public_key()
        encryptor.encrypt_file(input_file, output_file, public_key)
    
    elif command == "decrypt":
        if len(sys.argv) < 4:
            print("❌ Error: Specify input and output files")
            print("   Example: python file_encryptor.py decrypt myfile.enc myfile_decrypted.txt")
            return
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        
        if not os.path.exists(input_file):
            print(f"❌ Error: File '{input_file}' not found")
            return
        
        # Load private key
        if not os.path.exists("private_key.pem"):
            print("❌ Error: Private key not found. Run 'generate' first.")
            return
        
        private_key = encryptor.load_private_key()
        encryptor.decrypt_file(input_file, output_file, private_key)
    
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()
