import struct
import zlib
import base64
import os
import menus
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
import utilidades

# Formato binario fijo: ID(10s), nombre(50s), edad(h), email(100s)
CONFIGURACION_PAQUETES = '10s50sh100s'
TAMAÑO_REGISTRO = struct.calcsize(CONFIGURACION_PAQUETES)

# Parámetros KDF
SALT_BYTES = 16
ITERACIONES = 200_000

def generar_key(password: str, salt: bytes) -> bytes:
    """Esta función deriva una clave criptográfica a partir de una contraseña y una sal (salt) usando PBKDF2-HMAC-SHA256.
    Luego la codifica en un formato adecuado para usar con Fernet (un sistema de cifrado simétrico)"""

    # La mejor explicación la puedo sacar de la documentación en sí:
    # The PBKDF2HMAC() function derives a key from a password using a salt and iteration count as specified in RFC 2898.ç
    # Increasing the iter parameter slows down the algorithm which makes it harder for an attacker to perform a brute force attack using a large number of candidate passwords.
    # This function makes no assumption regarding the given password. It will be treated as a byte sequence.

    # https://docs.rocketsoftware.com/es-ES/bundle/unidataunibasiccommands_rg_824/page/vmn1685024690247.html
    try:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=ITERACIONES,
        )
        # Por tanto, con esta derivamos la clave con el password (codificado a bytes)
        key = kdf.derive(password.encode('utf-8'))
        # Y devolvemos la clave en formato base64 urlsafe
        return base64.urlsafe_b64encode(key)
    except Exception as ex:
        print(f"Error. {ex}")
        return
    
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
            # Se decodifica y se eliminan los bytes nulos de relleno
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
    """Comprime los bytes introducidos con zlib y los devuelve."""
    try:
        if not isinstance(input_bytes, bytes) or not input_bytes:
            raise ValueError("Los datos a comprimir deben ser bytes y no vacíos.")
        return zlib.compress(input_bytes, level=9)
    except Exception as e:
        print(f"Error al comprimir los datos: {e}")
        return None

def descomprimir_bytes(input_bytes: bytes) -> bytes:
    """Descomprime bytes con zlib y los devuelve."""
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
    except ValueError as ve:
        print(f"Error de valor desencriptando: {ve}")
        return None
    except Exception as e:
        print(f"Error al desencriptar: {e}")
        return None

# -----------------------------
# Utilidades de “record stream”
# -----------------------------

def record_size() -> int:
    """Devuelve el tamaño fijo en bytes de cada registro empaquetado."""
    return TAMAÑO_REGISTRO


def encriptar_user_data(user:str, contrasena:str) -> bytes:
    """Encripta los datos del usuario (nombre de usuario y clave de cifrado) con la contraseña introducida."""
    try:
        key = Fernet.generate_key()
        return encriptar_bytes(struct.pack('20s', user.encode("utf-8"))+ key, contrasena)
    
    except AttributeError as ae:
        print(f"Error. {ae}")
        return
    except TypeError as te:
        print(f"Error en el desempaquetamiento. {te}")
        return
    except Exception as ex:
        print(f"Error. {ex}")
        return

def desencriptar_user_data(byts: bytes, password) -> str:
    """Desencripta los datos del usuario, devuelve (usuario, clave) o None si falla."""
    try:
        desempaquetado = desencriptar_bytes(byts, password)
        return struct.unpack('20s', desempaquetado[:20])[0].decode("utf-8").rstrip('\x00'), desempaquetado[20:]
    except TypeError as te:
        print(f"Error en el desempaquetamiento. {te}")
        return
    except Exception as ex:
        print(f"Error. {ex}")
        return
    

def exportar_json(registros:list[tuple]):
    """Exporta los registros a un archivo JSON llamado 'datos.json'."""
    try:
        with open('datos.json','wb') as datos:
            lista_registros = []
            for registro in registros:
                lista_registros.append({
                    "DNI": registro[0],
                    "Nombre": registro[1],
                    "Edad": registro[2],
                    "Email": registro[3]
                })
            datos.write(json.dumps(lista_registros, indent=4).encode('utf-8'))
        utilidades.pulsar_enter_para_continuar("Datos exportados a 'datos.json'. Pulsa Enter para continuar...")
    except IOError as ioe:
        print(f"Error. {ioe}")
    except PermissionError:
        print(f"Error. No tiene permisos para crear el archivo.")
    except Exception as ex:
        print(f"Error. {ex}")

    