import hashlib
from cryptography.fernet import Fernet
import base64
import requests
import bcrypt
import uuid
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#Use this functions for encryption


class Cryptography():
    def generate_unique_id(self, length=16):
        u = uuid.uuid4()
        short_uuid = base64.urlsafe_b64encode(u.bytes).decode('utf-8').rstrip('=')
        return short_uuid[:length]

    def generate_key(self, plain_password: str) -> str:
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8') 
    
    def verify_key(self, plain_password: str, hashed_password: str) -> bool:
        print("Plain Password:", plain_password.encode('utf-8'))
        print("Hashed Password:", hashed_password.encode('utf-8'))
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')

        )   

    def hash_this(self, data):  
        hash_object = hashlib.sha256(data.encode())
        return hash_object.hexdigest()


