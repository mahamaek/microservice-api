from datetime import datetime, timedelta
from pathlib import Path
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate


def generate_jwt():
    now = datetime.utcnow()
    payload = {
        "iss": "https://auth.coffeemesh.io/",
        "sub": "ec7bbccf-ca89-4af3-82ac-b41e4831a962",
        "aud": "http://127.0.0.1:8000/orders",
        # "iat": now.timestamp(),
        "exp": (now + timedelta(hours=24)).timestamp(),
        "scope": "openid",
    }

    private_key_text = Path("private_key.pem").read_text()

    private_key = serialization.load_pem_private_key(
        private_key_text.encode(),
        password=None,
    )

    return jwt.encode(payload=payload, key=private_key, algorithm='RS256')


def validate_jwt(token):
    try:
        payload = jwt.decode(
            token,
            key=PUBLIC_KEY,
            algorithms=['RS256'],
            audience=["http://127.0.0.1:8000/orders"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError as e:
        return {"error": f"Invalid token: {str(e)}"}


# Load and parse ONCE at startup
try:
    CERT_TEXT = Path("public_key.pem").read_text()
    PUBLIC_KEY = load_pem_x509_certificate(
        CERT_TEXT.encode('utf-8')).public_key()
except Exception as e:
    # Handle missing file or bad cert format
    raise RuntimeError(f"Could not load public key: {e}")

access_token = generate_jwt()
print(access_token)
print(validate_jwt(access_token))
