import time
import hashlib
import os
import jwt
from cryptography.hazmat.primitives import serialization


def generate_jwt(api_key: str, signing_key: str) -> str:
    """
    Generates a JSON Web Token (JWT) for authenticating with the Coinbase API.

    :param api_key: The API key for Coinbase.
    :param signing_key: The signing key in PEM format used to sign the JWT.
    :return: A JWT token as a string.
    :raises ValueError: If there is an issue with loading the private key or encoding the JWT.
    """
    # Load the private key from the signing key string
    try:
        private_key_bytes = signing_key.encode('utf-8')
        private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
    except Exception as e:
        raise ValueError(f"Failed to load private key: {e}") from e

    # Create the JWT payload with issuer, not before, expiry, and subject claims
    payload = {
        "iss": "coinbase-cloud",
        "nbf": int(time.time()),
        "exp": int(time.time()) + 120,
        "sub": api_key,
    }

    # Create JWT headers with key ID and nonce
    headers = {
        "kid": api_key,
        "nonce": hashlib.sha256(os.urandom(16)).hexdigest()
    }

    # Encode the JWT using the ES256 algorithm
    try:
        token = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)
    except Exception as e:
        raise ValueError(f"Failed to encode JWT: {e}")

    return token
