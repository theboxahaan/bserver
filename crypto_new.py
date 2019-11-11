import base64
import logging

from cryptography.exceptions import InvalidSignature
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_pair():
	private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096, backend=default_backend())
	public_key = private_key.public_key()
	return [public_key, private_key]

def sign(plain_text):
	signature = private_key.sign(data=plain_text.encode('utf-8'),padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),algorithm=hashes.SHA256())
	logger.info("Signature: %s", base64.urlsafe_b64encode(signature))
	return signature

def verify_sig(signature):
	try:
		public_key.verify(signature=signature,data=plain_text.encode('utf-8'),padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),algorithm=hashes.SHA256())
		is_signature_correct = True
	except InvalidSignature:
		is_signature_correct = False
		logger.info("Signature is correct: %s", is_signature_correct)
	except UnsupportedAlgorithm:
		logger.exception("Signing failed")
