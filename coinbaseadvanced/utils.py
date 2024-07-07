import time
import jwt
import hashlib
import os
from cryptography.hazmat.primitives import serialization

def generate_jwt(api_key, signing_key):
    private_key_bytes = signing_key.encode('utf-8')
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
    payload = {
        "iss": "coinbase-cloud",
        "nbf": int(time.time()),
        "exp": int(time.time()) + 120,
        "sub": api_key,
    }
    headers = {
        "kid": api_key,
        "nonce": hashlib.sha256(os.urandom(16)).hexdigest()
    }
    token = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)
    return token