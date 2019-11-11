from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.assymetric import rsa


def gen_key():
    private_key = rsa.generate(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
    )
    public_key = private_key.public_key()

