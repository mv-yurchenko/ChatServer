from cryptography.fernet import Fernet
import base64


class Cryptography:
    """Модуль шифрования данных, отправляемых от клиента на сервер"""

    def __init__(self, key_seed: bytes):
        self.cipher = Fernet(key_seed)

    def encrypt_string(self, msg: str):
        return self.cipher.encrypt(msg.encode("utf-8")).decode("utf-8")

    def decrypt_string(self, encrypted_msg: bytes):
        return self.cipher.decrypt(encrypted_msg).decode('utf-8')
