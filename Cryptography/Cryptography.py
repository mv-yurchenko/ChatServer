from cryptography.fernet import Fernet
import base64


class Cryptography:
    """Модуль шифрования данных, отправляемых от клиента на сервер"""

    def __init__(self, key_seed: str):
        self.cipher = Fernet(key_seed)

    def encrypt_string(self, msg):
        return self.cipher.encrypt(msg)

    def decrypt_string(self, encrypted_msg):
        return self.cipher.decrypt(encrypted_msg)


a = Cryptography(base64.b64encode(bytes('123456789101112', 'utf-8')))