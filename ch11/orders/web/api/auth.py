from pathlib import Path
import jwt

from cryptography.x509 import load_pem_x509_certificate

# read public key from ch11 project root
key_path = Path(__file__).resolve().parents[3] / "public_key.pem"
if not key_path.exists():
    raise FileNotFoundError(
        f"public_key.pem not found at {key_path}.\n"
        "Create it in the project root (see ch11/readme.txt) using:\n"
        "openssl req -x509 -nodes -newkey rsa:2048 -keyout private_key.pem -out public_key.pem -subj \"/CN=coffeemesh\""
    )
public_key_text = key_path.read_text()
public_key = load_pem_x509_certificate(public_key_text.encode()).public_key()


def decode_and_validate_token(access_token):
    """
    Validates an access token. If the token is valid, it returns the token payload.
    """
    return jwt.decode(
        access_token,
        key=public_key,
        algorithms=["RS256"],
        audience=["http://127.0.0.1:8000/orders"],
    )
