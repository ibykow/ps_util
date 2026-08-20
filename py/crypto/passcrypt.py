import argparse
import base64
import getpass
import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a 32-byte key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000, 
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(filepath: str, password: str):
    """Reads a file, encrypts it, and overwrites it or saves as .enc"""
    with open(filepath, "r", encoding="utf-8") as f:
        plaintext = f.read()
        
    salt = os.urandom(16)
    key = derive_key(password, salt)
    f_cipher = Fernet(key)
    
    token = f_cipher.encrypt(plaintext.encode())
    encrypted_data = salt + token
    
    out_path = filepath + ".enc"
    with open(out_path, "wb") as f:
        f.write(encrypted_data)
    print(f"[+] Success: Encrypted file saved to {out_path}")

def decrypt_file(filepath: str, password: str):
    """Reads an encrypted file, decrypts it, and saves it without the extension"""
    with open(filepath, "rb") as f:
        encrypted_bundle = f.read()
        
    salt = encrypted_bundle[:16]
    token = encrypted_bundle[16:]
    
    key = derive_key(password, salt)
    f_cipher = Fernet(key)
    
    try:
        decrypted_data = f_cipher.decrypt(token).decode("utf-8")
        
        # Determine output filename
        if filepath.endswith(".enc"):
            out_path = filepath[:-4]
        else:
            out_path = filepath + ".dec"
            
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(decrypted_data)
        print(f"[+] Success: Decrypted file saved to {out_path}")
        
    except Exception:
        print("[-] Error: Decryption failed. Wrong password or corrupted file.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Simple CLI tool to encrypt/decrypt text files using AES-256.")
    
    # Mutually exclusive group ensures you can't try to encrypt and decrypt at the same time
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the file")
    group.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the file")
    
    parser.add_argument("filename", help="The path to the file you want to process")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.filename):
        print(f"[-] Error: File '{args.filename}' not found.")
        sys.exit(1)
        
    # getpass hides the typed characters in the terminal
    password = getpass.getpass("Enter Master Password: ")
    
    if args.encrypt:
        encrypt_file(args.filename, password)
    elif args.decrypt:
        decrypt_file(args.filename, password)

if __name__ == "__main__":
    main()