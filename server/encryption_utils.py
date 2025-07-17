from cryptography.fernet import Fernet
import os

def load_key():
    # Try to load from file (best practice for prototype)
    if os.path.exists("fernet.key"):
        with open("fernet.key", "rb") as file:
            return file.read()
    else:
        # First-time setup: generate and save
        key = Fernet.generate_key()
        with open("fernet.key", "wb") as file:
            file.write(key)
        return key

# Set up cipher instance
key = load_key()
cipher = Fernet(key)

def encrypt_text(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()