import struct
import zlib
import base64
import os
import menus
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import utilidades
import colorama

## ID, nombre, edad y correo electrónico

def packRecord(id:str, name:str, age:int, email:str) -> bytes | None:
    """Empaqueta los datos en un formato binario"""
    try:
        paquete = struct.pack('10s50sH100s', id.encode('utf-8'), name.encode('utf-8'), age, email.encode('utf-8'))
    except struct.error as e:
        print(f"Error al empaquetar los datos: {e}")
    except Exception as e:
        print(f"Error inesperado al empaquetar los datos: {e}")
    else:
        return paquete
    return None

def unpackRecord(record_bytes) -> tuple[int, str, int, str]: #corregir lo que realmente devuelve, id es un dni y está formateado en string
    """Desempaqueta los datos desde un formato binario"""
    try:
        id, name, age, email = struct.unpack('10s50sH100s', record_bytes)
    except Exception as e:
        print(f"Error inesperado al desempaquetar los datos: {e}")
    except struct.error as e:
        print(f"Error al desempaquetar los datos: {e}")
    else:
        return id.decode('utf-8').rstrip('\x00'), name.decode('utf-8').rstrip('\x00'), age, email.decode('utf-8').rstrip('\x00')
    return None

def zipBytes(byts:bytes) -> bytes | None:
    try:
        if not byts:
            raise ValueError("Los datos a comprimir no pueden estar vacíos.")
        if not isinstance(byts, bytes):
            raise TypeError("Los datos a comprimir deben ser de tipo bytes.")
        return zlib.compress(byts, level=9)
    except Exception as e:
        print(f"Error al comprimir los datos: {e}")
        return None

def unzipBytes(byts:bytes) -> bytes:
    """This function decompresses bytes using zlib."""
    try:
        if not byts:
            raise ValueError("Los datos a descomprimir no pueden estar vacíos.")
        if not isinstance(byts, bytes):
            raise TypeError("Los datos a descomprimir deben ser de tipo bytes.")
        return zlib.decompress(byts)
    except Exception as e:
        print(f"Error al descomprimir los datos: {e}")
        return None

def encryptBytes(byts:bytes, password:str) -> bytes:
    """This function encrypts bytes using a password and a randomly generated salt."""
    try:
        if not byts:
            raise ValueError("Los datos a encriptar no pueden estar vacíos.")
        if not isinstance(byts, bytes):
            raise TypeError("Los datos a encriptar deben ser de tipo bytes.")
        salt = os.urandom(16)
        # Derive the key from the password and salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1_200_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
        f = Fernet(key)
        with open("./salt.key", "wb") as file:
            file.write(salt)
        return f.encrypt(byts)
    except Exception as e:
        print(f"Error al encriptar los datos: {e}")
        return None

def decryptBytes(byts:bytes, password:str) -> bytes:
    """This function decrypts bytes using a password and a stored salt."""
    try:
        with open ("./salt.key", "rb") as file:
            salt = file.read()
        # Derive the key from the password and salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1_200_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
        f = Fernet(key)
        return f.decrypt(byts)
    except InvalidToken:
        print("Contraseña incorrecta")
        return None
    except FileNotFoundError:
        print("Error al desencriptar")
        return None

