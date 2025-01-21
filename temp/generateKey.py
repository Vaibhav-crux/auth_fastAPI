from cryptography.fernet import Fernet
import base64

key = Fernet.generate_key()
print(base64.b64encode(key).decode())  # This will give you the base64 string without 'b' prefix