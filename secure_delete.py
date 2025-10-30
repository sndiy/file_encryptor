#!/usr/bin/env python3
"""
Secure File Shredder - Penghapus File Super Aman
Menimpa data berkali-kali sebelum dihapus agar tidak bisa di-recover
"""

import os
import sys
import random
import hashlib
from pathlib import Path
import argparse

class SecureFileShredder:
    def __init__(self):
        self.chunk_size = 4096  # 4KB per chunk
    
    def get_file_size(self, filepath):
        """Dapatkan ukuran file"""
        return os.path.getsize(filepath)
    
    def overwrite_with_pattern(self, filepath, pattern, pass_number, total_passes):
        """Timpa file dengan pattern tertentu"""
        file_size = self.get_file_size(filepath)
        bytes_written = 0
        
        with open(filepath, 'rb+') as f:
            while bytes_written < file_size:
                chunk_size = min(self.chunk_size, file_size - bytes_written)
                
                if pattern == 'random':
                    data = os.urandom(chunk_size)
                elif pattern == 'zeros':
                    data = b'\x00' * chunk_size
                elif pattern == 'ones':
                    data = b'\xff' * chunk_size
                else:
                    data = pattern * chunk_size
                
                f.write(data[:chunk_size])
                bytes_written += chunk_size
                
                # Progress bar
                progress = (bytes_written / file_size) * 100
                self._print_progress(pass_number, total_passes, progress)
            
            f.flush()
            os.fsync(f.fileno())  # Force write ke disk
        
        print()  # New line setelah progress bar
    
    def _print_progress(self, pass_num, total_passes, progress):
        """Cetak progress bar"""
        bar_length = 40
        filled = int(bar_length * progress / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f'\r  Pass {pass_num}/{total_passes}: [{bar}] {progress:.1f}%', end='', flush=True)
    
    def dod_method(self, filepath):
        """
        DoD 5220.22-M Method (US Department of Defense)
        - Pass 1: Tulis 0
        - Pass 2: Tulis 1
        - Pass 3: Random data
        Standard militer AS untuk menghapus data sensitif
        """
        print("\n🛡️  DoD 5220.22-M Method (3 passes)")
        print("   Standard US Department of Defense")
        print(f"   File: {filepath}")
        print(f"   Size: {self._format_size(self.get_file_size(filepath))}\n")
        
        # Pass 1: Zeros
        print("  🔄 Pass 1/3: Overwriting with zeros...")
        self.overwrite_with_pattern(filepath, 'zeros', 1, 3)
        
        # Pass 2: Ones
        print("  🔄 Pass 2/3: Overwriting with ones...")
        self.overwrite_with_pattern(filepath, 'ones', 2, 3)
        
        # Pass 3: Random
        print("  🔄 Pass 3/3: Overwriting with random data...")
        self.overwrite_with_pattern(filepath, 'random', 3, 3)
        
        print("  ✅ DoD overwrite complete!")
    
    def gutmann_method(self, filepath):
        """
        Gutmann Method (35 passes)
        Metode paling aman, tapi paling lama
        Dirancang untuk menghapus data dari berbagai jenis hard disk
        """
        print("\n🔐 Gutmann Method (35 passes)")
        print("   Most secure method - Maximum security")
        print(f"   File: {filepath}")
        print(f"   Size: {self._format_size(self.get_file_size(filepath))}\n")
        
        patterns = [
            'random', 'random', 'random', 'random',  # Pass 1-4: Random
            b'\x55', b'\xaa',  # Pass 5-6: Alternating bits
            b'\x92\x49\x24', b'\x49\x24\x92', b'\x24\x92\x49',  # Pass 7-9: Special patterns
            b'\x00', b'\x11', b'\x22', b'\x33', b'\x44',  # Pass 10-14
            b'\x55', b'\x66', b'\x77', b'\x88', b'\x99',  # Pass 15-19
            b'\xaa', b'\xbb', b'\xcc', b'\xdd', b'\xee',  # Pass 20-24
            b'\xff', b'\x92\x49\x24', b'\x49\x24\x92',  # Pass 25-27
            b'\x24\x92\x49', b'\x6d\xb6\xdb', b'\xb6\xdb\x6d',  # Pass 28-30
            b'\xdb\x6d\xb6',  # Pass 31
            'random', 'random', 'random', 'random'  # Pass 32-35: Random
        ]
        
        for i, pattern in enumerate(patterns, 1):
            print(f"  🔄 Pass {i}/35: ", end='')
            if pattern == 'random':
                print("Random data...")
            else:
                print(f"Pattern 0x{pattern.hex()}...")
            self.overwrite_with_pattern(filepath, pattern, i, 35)
        
        print("  ✅ Gutmann overwrite complete!")
    
    def quick_method(self, filepath, passes=7):
        """
        Quick Method (7 passes random)
        Balance antara keamanan dan kecepatan
        Cocok untuk penggunaan umum
        """
        print(f"\n⚡ Quick Method ({passes} passes)")
        print("   Balanced security and speed")
        print(f"   File: {filepath}")
        print(f"   Size: {self._format_size(self.get_file_size(filepath))}\n")
        
        for i in range(1, passes + 1):
            print(f"  🔄 Pass {i}/{passes}: Random data...")
            self.overwrite_with_pattern(filepath, 'random', i, passes)
        
        print("  ✅ Quick overwrite complete!")
    
    def simple_method(self, filepath, passes=3):
        """
        Simple Method (3 passes)
        Cepat, cukup aman untuk kebutuhan umum
        """
        print(f"\n🚀 Simple Method ({passes} passes)")
        print("   Fast and sufficient for general use")
        print(f"   File: {filepath}")
        print(f"   Size: {self._format_size(self.get_file_size(filepath))}\n")
        
        for i in range(1, passes + 1):
            print(f"  🔄 Pass {i}/{passes}: Random data...")
            self.overwrite_with_pattern(filepath, 'random', i, passes)
        
        print("  ✅ Simple overwrite complete!")
    
    def rename_file(self, filepath):
        """Rename file dengan nama random sebelum dihapus"""
        directory = os.path.dirname(filepath)
        random_name = hashlib.md5(os.urandom(32)).hexdigest()
        new_path = os.path.join(directory, random_name)
        
        try:
            os.rename(filepath, new_path)
            return new_path
        except:
            return filepath
    
    def delete_file(self, filepath):
        """Hapus file dari filesystem"""
        try:
            os.remove(filepath)
            return True
        except Exception as e:
            print(f"  ⚠️  Warning: Could not delete file: {e}")
            return False
    
    def shred_file(self, filepath, method='quick'):
        """
        Main function untuk shred file
        """
        if not os.path.exists(filepath):
            print(f"❌ Error: File '{filepath}' not found!")
            return False
        
        if not os.path.isfile(filepath):
            print(f"❌ Error: '{filepath}' is not a file!")
            return False
        
        print("=" * 70)
        print("🗑️  SECURE FILE SHREDDER")
        print("=" * 70)
        
        # Pilih method
        if method == 'dod':
            self.dod_method(filepath)
        elif method == 'gutmann':
            self.gutmann_method(filepath)
        elif method == 'quick':
            self.quick_method(filepath, passes=7)
        elif method == 'simple':
            self.simple_method(filepath, passes=3)
        else:
            print(f"❌ Unknown method: {method}")
            return False
        
        # Rename file dengan nama random
        print("\n  🔀 Renaming file to random name...")
        new_path = self.rename_file(filepath)
        if new_path != filepath:
            print(f"  ✅ Renamed to: {os.path.basename(new_path)}")
        
        # Hapus file
        print("  🗑️  Deleting file from filesystem...")
        if self.delete_file(new_path):
            print("  ✅ File deleted successfully!")
        
        print("\n" + "=" * 70)
        print("✅ SECURE DELETION COMPLETE!")
        print("=" * 70)
        print("\n💡 File telah dihapus secara permanen dan tidak dapat di-recover!")
        print("   Data sudah ditimpa berkali-kali dengan random data.\n")
        
        return True
    
    def shred_directory(self, dirpath, method='quick', recursive=False):
        """Shred semua file dalam directory"""
        if not os.path.exists(dirpath):
            print(f"❌ Error: Directory '{dirpath}' not found!")
            return False
        
        if not os.path.isdir(dirpath):
            print(f"❌ Error: '{dirpath}' is not a directory!")
            return False
        
        print(f"\n🗂️  Shredding directory: {dirpath}")
        print(f"   Recursive: {recursive}")
        print(f"   Method: {method}\n")
        
        files_to_shred = []
        
        if recursive:
            for root, dirs, files in os.walk(dirpath):
                for filename in files:
                    files_to_shred.append(os.path.join(root, filename))
        else:
            for item in os.listdir(dirpath):
                item_path = os.path.join(dirpath, item)
                if os.path.isfile(item_path):
                    files_to_shred.append(item_path)
        
        if not files_to_shred:
            print("⚠️  No files found to shred!")
            return False
        
        print(f"📋 Found {len(files_to_shred)} file(s) to shred\n")
        
        for i, filepath in enumerate(files_to_shred, 1):
            print(f"\n[{i}/{len(files_to_shred)}] Processing: {os.path.basename(filepath)}")
            self.shred_file(filepath, method)
        
        print(f"\n✅ All {len(files_to_shred)} file(s) shredded successfully!")
        
        return True
    
    def _format_size(self, size_bytes):
        """Format ukuran file ke human-readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"


def main():
    parser = argparse.ArgumentParser(
        description='Secure File Shredder - Hapus file dengan sangat aman',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Methods:
  simple   - 3 passes random (Fast, good for general use)
  quick    - 7 passes random (Balanced security and speed) [DEFAULT]
  dod      - 3 passes DoD 5220.22-M (US Military standard)
  gutmann  - 35 passes (Maximum security, very slow)

Examples:
  # Shred single file (quick method)
  python secure_delete.py secret.txt
  
  # Shred with DoD method
  python secure_delete.py --method dod secret.txt
  
  # Shred with maximum security
  python secure_delete.py --method gutmann top_secret.pdf
  
  # Shred all files in directory
  python secure_delete.py --directory ./temp_files
  
  # Shred directory recursively
  python secure_delete.py --directory ./secrets --recursive

⚠️  WARNING: This operation is IRREVERSIBLE!
   Files will be permanently destroyed and cannot be recovered.
        '''
    )
    
    parser.add_argument('path', nargs='?', help='File or directory to shred')
    parser.add_argument('-m', '--method', 
                       choices=['simple', 'quick', 'dod', 'gutmann'],
                       default='quick',
                       help='Shredding method (default: quick)')
    parser.add_argument('-d', '--directory',
                       action='store_true',
                       help='Shred all files in directory')
    parser.add_argument('-r', '--recursive',
                       action='store_true',
                       help='Shred directory recursively')
    parser.add_argument('-y', '--yes',
                       action='store_true',
                       help='Skip confirmation prompt')
    
    args = parser.parse_args()
    
    if not args.path:
        parser.print_help()
        return
    
    # Konfirmasi
    if not args.yes:
        print("\n⚠️  WARNING: This will PERMANENTLY destroy the file(s)!")
        print("   This operation CANNOT be undone!\n")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("\n❌ Operation cancelled.")
            return
    
    shredder = SecureFileShredder()
    
    if args.directory:
        shredder.shred_directory(args.path, method=args.method, recursive=args.recursive)
    else:
        shredder.shred_file(args.path, method=args.method)


if __name__ == "__main__":
    main()
