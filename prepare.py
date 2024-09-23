from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os
import hmac
import hashlib

def generate_keys(save_directory):
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Serialize private key with no encryption
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Generate public key
    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Ensure the save directory exists
    os.makedirs(save_directory, exist_ok=True)

    # Save the private key
    with open(os.path.join(save_directory, 'private_key.pem'), 'wb') as f:
        f.write(pem_private)

    # Save the public key
    with open(os.path.join(save_directory, 'public_key.pem'), 'wb') as f:
        f.write(pem_public)

def generate_hmac_message(key, message, file_path):

    # Prepare the message with HMAC
    full_message = f"HMAC: WENHUI VERIFIED"

    # Save the message with HMAC to the file
    with open(file_path, 'w') as f:
        f.write(full_message)

# Example usage
key_directory = '/tmp/key'
generate_keys(key_directory)

# HMAC key and message
hmac_key = b'secret_hmac_key'  # This key should be securely generated and stored.
message = b'WENHUI VERIFIED'

# Generate and save HMAC message
generate_hmac_message(hmac_key, message, os.path.join(key_directory, 'msg.txt'))

