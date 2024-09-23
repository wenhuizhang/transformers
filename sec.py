from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hmac
import os

def load_keys_and_message():
    # Load private key
    with open('/tmp/key/private_key.pem', 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None  # Assuming the private key is not encrypted
        )

    # Load public key
    with open('/tmp/key/public_key.pem', 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
    
    # Load HMAC message
    with open('/tmp/key/msg.txt', 'rb') as msg_file:
        hmac_message = msg_file.read()
    
    return private_key, public_key, hmac_message

def encrypt_then_mac(data, public_key, hmac_message):
    # Encrypt data
    encrypted_data = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Generate HMAC
    h = hmac.HMAC(hmac_message, hashes.SHA256())
    h.update(encrypted_data)
    hmac_value = h.finalize()
    
    return encrypted_data, hmac_value

def verify_hmac_then_decrypt(encrypted_data, hmac_value, private_key, hmac_message):
    # Verify HMAC
    h = hmac.HMAC(hmac_message, hashes.SHA256())
    h.update(encrypted_data)
    try:
        h.verify(hmac_value)
        # HMAC verification successful, proceed to decrypt
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return h, decrypted_data
    except hmac.exceptions.InvalidSignature:
        # HMAC verification failed
        return None

# Load keys and HMAC message
private_key, public_key, hmac_message = load_keys_and_message()

# Encrypt data and generate HMAC
data = b'Hello, this is a secret message!'
encrypted_data, hmac_value = encrypt_then_mac(data, public_key, hmac_message)

print("data:", data)

print("encrypted_data:", encrypted_data)
print("hmac_value:", hmac_value)
print("hmac_message", hmac_message)

# Verify HMAC and decrypt data
h, decrypted_data = verify_hmac_then_decrypt(encrypted_data, hmac_value, private_key, hmac_message)
print("h_verify:", h)
print("decrypted_data", decrypted_data)
if decrypted_data:
    print("Decryption successful:", decrypted_data)
else:
    print("HMAC verification failed.")

