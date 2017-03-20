from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import binascii


def encrypt_with_public_key(plaintext, user):
    # A hash isn't included as we're not interested in the long term data security of what we send. And because I'm doing this in a hurry. Mostly the latter.
    rsa_key = RSA.importKey(user.public_key)
    cipher = PKCS1_v1_5.new(rsa_key)
    message = bytes(plaintext, encoding='utf-8')
    encrypted_bytes = cipher.encrypt(message)
    return str(binascii.b2a_base64(encrypted_bytes).rstrip())[2:-1]
