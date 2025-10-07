import struct
import zlib
import base64
import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Formato binario fijo: ID(10s), nombre(50s), edad(h), email(100s)
CONFIGURACION_PAQUETES = '10s50sh100s'
TAMAÑO_REGISTRO = struct.calcsize(CONFIGURACION_PAQUETES)

# Parámetros KDF
SALT_BYTES = 16
ITERACIONES = 200_000

def generar_key(password: str, salt: bytes) -> bytes:
    """Deriva una clave Fernet (base64 urlsafe) a partir de password+salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERACIONES,
    )
    key = kdf.derive(password.encode('utf-8'))
    return base64.urlsafe_b64encode(key)

# ------------------------
# Empaquetado de registros
# ------------------------

def empaquetar_registro(id: str, name: str, age: int, email: str) -> bytes:
    """Empaqueta los datos en un formato binario fijo."""
    try:
        return struct.pack(
            CONFIGURACION_PAQUETES,
            id.encode('utf-8'),
            name.encode('utf-8'),
            age,
            email.encode('utf-8')
        )
    except struct.error as e:
        print(f"Error al empaquetar los datos: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al empaquetar los datos: {e}")
        return None

def desempaquetar_registro(record_bytes: bytes) -> tuple[str, str, int, str]:
    """Desempaqueta un registro binario a tupla tipada."""
    try:
        id_b, name_b, age, email_b = struct.unpack(CONFIGURACION_PAQUETES, record_bytes)
        return (
            id_b.decode('utf-8').rstrip('\x00'),
            name_b.decode('utf-8').rstrip('\x00'),
            age,
            email_b.decode('utf-8').rstrip('\x00')
        )
    except struct.error as e:
        print(f"Error al desempaquetar los datos: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al desempaquetar los datos: {e}")
        return None

# ------------
# Compresión
# ------------

def comprimir_bytes(input_bytes: bytes) -> bytes:
    try:
        if not isinstance(input_bytes, bytes) or not input_bytes:
            raise ValueError("Los datos a comprimir deben ser bytes y no vacíos.")
        return zlib.compress(input_bytes, level=9)
    except Exception as e:
        print(f"Error al comprimir los datos: {e}")
        return None

def descomprimir_bytes(input_bytes: bytes) -> bytes:
    """Descomprime bytes con zlib."""
    try:
        if not isinstance(input_bytes, bytes) or not input_bytes:
            raise ValueError("Los datos a descomprimir deben ser bytes y no vacíos.")
        return zlib.decompress(input_bytes)
    except Exception as e:
        print(f"Error al descomprimir los datos: {e}")
        return None

# ------------
# Criptografía
# ------------

def encriptar_bytes(input_bytes: bytes, password: str) -> bytes:
    """
    Cifra bytes con contraseña:
    - Genera salt aleatorio (16B)
    - Deriva clave Fernet con PBKDF2-HMAC-SHA256
    - Devuelve: salt + token_fernet
    """
    try:
        if not isinstance(input_bytes, bytes) or not input_bytes:
            raise ValueError("Los datos a encriptar deben ser bytes y no vacíos.")
        salt = os.urandom(SALT_BYTES)
        key = generar_key(password, salt)
        f = Fernet(key)
        token = f.encrypt(input_bytes)
        return salt + token
    except Exception as e:
        print(f"Error al encriptar los datos: {e}")
        return None

def desencriptar_bytes(input_bytes: bytes, password: str) -> bytes:
    """
    Descifra bytes con contraseña:
    - Extrae salt (16B) del inicio
    - Deriva clave y descifra token Fernet
    """
    try:
        if not isinstance(input_bytes, bytes) or len(input_bytes) <= SALT_BYTES:
            raise ValueError("Blob inválido: faltan datos/salt.")
        salt, token = input_bytes[:SALT_BYTES], input_bytes[SALT_BYTES:]
        key = generar_key(password, salt)
        f = Fernet(key)
        return f.decrypt(token)
    except InvalidToken:
        print("Contraseña incorrecta o datos corruptos")
        return None
    except Exception as e:
        print(f"Error al desencriptar: {e}")
        return None

# -----------------------------
# Utilidades de “record stream”
# -----------------------------

def record_size() -> int:
    return TAMAÑO_REGISTRO


def encriptar_user_data(user:str, contrasena: str) -> bytes:
    return encriptar_bytes(struct.pack('20s40s', user, contrasena),'contrasena')

def desencriptar_user_data(bytes: bytes) -> str:
    return struct.unpack('20s40s', desencriptar_bytes(bytes, 'contrasena'))
