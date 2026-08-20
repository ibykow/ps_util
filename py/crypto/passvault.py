import argparse
import base64
import getpass
import os
import random
import string
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

def secure_wipe(filepath: str, passes: int = 3):
    """Overwrites a file with random data and deletes it."""
    if not os.path.isfile(filepath):
        return
    file_size = os.path.getsize(filepath)
    with open(filepath, "ba+", buffering=0) as f:
        for _ in range(passes):
            f.seek(0)
            f.write(os.urandom(file_size))
            f.flush()
            os.fsync(f.fileno())
    # Obfuscate filename before deletion
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    new_path = os.path.join(os.path.dirname(filepath), random_name)
    os.rename(filepath, new_path)
    os.remove(new_path)
    print(f"[!] Securely wiped: {filepath}")

def encrypt_file(filepath: str, password: str, wipe: bool):
    with open(filepath, "r", encoding="utf-8") as f:
        plaintext = f.read()
        
    salt = os.urandom(16)
    key = derive_key(password, salt)
    f_cipher = Fernet(key)
    
    # Encrypt and combine with salt
    token = f_cipher.encrypt(plaintext.encode())
    payload = salt + token
    
    # Base64 encode the entire bundle for easy transport via email/text
    b64_payload = base64.b64encode(payload).decode('utf-8')
    
    out_path = filepath + ".enc"
    with open(out_path, "w") as f:
        f.write(b64_payload)
    
    print(f"[+] Success: Encrypted string saved to {out_path}")
    
    if wipe:
        secure_wipe(filepath)

def decrypt_file(filepath: str, password: str):
    with open(filepath, "r") as f:
        b64_payload = f.read()
    
    # Undo Base64 to get the salt + token
    try:
        payload = base64.b64decode(b64_payload)
        salt = payload[:16]
        token = payload[16:]
        
        key = derive_key(password, salt)
        f_cipher = Fernet(key)
        
        decrypted_data = f_cipher.decrypt(token).decode("utf-8")
        
        out_path = filepath.replace(".enc", "") + ".dec"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(decrypted_data)
        print(f"[+] Success: Decrypted file saved to {out_path}")
    except Exception as e:
        print(f"[-] Error: Decryption failed ({e}). Check your password.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Secure AES-256 Text Vault")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", action="store_true")
    group.add_argument("-d", "--decrypt", action="store_true")
    parser.add_argument("filename")
    parser.add_argument("-w", "--wipe", action="store_true", help="Wipe original after encryption")
    
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        print("[-] File not found.")
        sys.exit(1)
        
    password = getpass.getpass("Master Password: ")
    
    if args.encrypt:
        encrypt_file(args.filename, password, args.wipe)
    else:
        decrypt_file(args.filename, password)

if __name__ == "__main__":
    main()