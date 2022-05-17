import base64
import string
import time
from datetime import datetime

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class SecurityGuard:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def __base64_transform(self, input: str, encode=True):
        """
        Use to decode/encode bytes to base64.
        """
        if encode:  # encode
            return base64.b64encode(input).decode("UTF-8")

        else:  # decode
            return base64.b64decode(input.encode("UTF-8"))

    def generate_key(self):
        key = get_random_bytes(32)
        key = self.__base64_transform(key)
        return key

    def decode_key(self, key: str):
        return self.__base64_transform(key, encode=False)

    def __encrypt(self, message: str, base64_key: str):
        bytes_message = message.encode("UTF-8")
        key = self.decode_key(base64_key)
        cipher = AES.new(key, AES.MODE_CFB)

        ciphered_meesage = cipher.encrypt(bytes_message)
        base64_ciphered_meesage = self.__base64_transform(ciphered_meesage)
        base64_iv = self.__base64_transform(cipher.iv)

        return (base64_iv, base64_ciphered_meesage)

    def __decrypt(self, base64_iv: str, base64_ciphered_meesage: str, base64_key: str):
        iv = self.__base64_transform(base64_iv, encode=False)
        ciphered_meesage = self.__base64_transform(
            base64_ciphered_meesage, encode=False
        )
        key = self.decode_key(base64_key)

        cipher = AES.new(key, AES.MODE_CFB, iv=iv)

        bytes_message = cipher.decrypt(ciphered_meesage)
        message = bytes_message.decode("UTF-8")

        return message

    def authentication(
        self, base_64_iv, base64_ciphered_meesage: string, base64_key: string
    ):
        """
        The received message will be "<encrypted 'message-timestamp'>"
        <message>, <timestamp> are encoded in the form of base64
        <encrypted 'message-timestamp'> is encrypted by AES.
        If the decrypted timestamp is within an acceptable time range, the verification is passed.
        """
        return_msg = {"success": False, "msg": "", "data": ""}
        current_timestamp = time.time()

        try:
            message_with_timestamp = self.__decrypt(
                base_64_iv, base64_ciphered_meesage, base64_key
            )
            message, timestamp = tuple(message_with_timestamp.split("-"))
            if current_timestamp - float(timestamp) > 60:
                return_msg["msg"] = "time limit exceeded"
                return return_msg

        except Exception as error:
            print(error)
            return_msg["msg"] = "decode error"
            return return_msg

        return_msg["data"] = message
        return_msg["success"] = True
        return return_msg

    def encrypt_message(self, message: str, base64_key: str):
        """
        Use this method to get a ciphered message that can be used for authentication.
        """
        timestamp = time.time()
        return self.__encrypt(f"{message}-{str(timestamp)}", base64_key)
