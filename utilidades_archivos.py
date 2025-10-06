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

COLOR_LETRA_CYAN = colorama.Fore.CYAN
COLOR_LETRA_AMARILLO = colorama.Fore.YELLOW
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

def buscar_registro_especificado(estructura_datos:list[tuple[str,str,int,str]], dni:int)->None:
    """Muestra los registros introducidos en formato tabla"""
    for registro in estructura_datos:
        for subelemento in registro:
            if subelemento[0] == dni:
                return subelemento
    return None

def modificar_campos_registro(estructura_datos:list[tuple[str,str,int,str]], dni:int)->None:
    """Muestra los registros introducidos en formato tabla"""
    for registro in estructura_datos:
        for subelemento in registro:
            if subelemento[0] == dni:
                print (f"|{subelemento[0]:10d}|{subelemento[1].ljust(20)}|{subelemento[2]:6d}|{subelemento[3].ljust(30)}|")
                while True:
                    try:
                        modificar = input(COLOR_LETRA_CYAN + "¿Desea modificar el registro? [S]|[N] >>> ").upper()
                        match modificar:
                            case 'S':
                                while True:
                                    nuevo_dni = modificar_campo_dni()
                                    nuevo_nombre = modificar_campo_nombre()
                                    nueva_edad = modificar_campo_edad()
                                    nuevo_correo = modificar_campo_correo()
                            case 'N':
                                utilidades.pulsar_enter_para_continuar("Cancelando operación.", "normal")
                                return None
                            case _:
                                print(COLOR_LETRA_AMARILLO + "Debe seleccionar entre [S]|[N].")
                    except KeyboardInterrupt:
                        utilidades.pulsar_enter_para_continuar("Operación cancelada.", "normal")
    print("+"+"-"*10 +"+"+ "-"*20 +"+"+ "-"*6 +"+"+ "-"*30 +"+")
def eliminar_registro_especificado(estructura_datos:list[tuple[str,str,int,str]], dni:int)->None:
    """Elimina un registro específico de entre los registros actuales"""
    #suponiendo que tenemos una estructura y un registro
    print("+"+"-"*10 +"+"+ "-"*20 +"+"+ "-"*6 +"+"+ "-"*30 +"+")
    print(f"|{'ID'.center(10)}|{'Nombre'.center(20)}|{'Edad'.center(6)}|{'Correo electrónico'.center(30)}|")
    print("+"+"-"*10 +"+"+ "-"*20 +"+"+ "-"*6 +"+"+ "-"*30 +"+")
    for registro in estructura_datos:
        for subelemento in registro:
            if subelemento[0] == dni:
                print (f"|{subelemento[0]:10d}|{subelemento[1].ljust(20)}|{subelemento[2]:6d}|{subelemento[3].ljust(30)}|")
                while True:
                    eliminar = input(COLOR_LETRA_CYAN + "¿Desea eliminar este fichero? [S]|[N] >>> ").upper()
                    match eliminar:
                        case 'S':
                            registro.remove(subelemento)
                            # encryptBytes(subelemento[0])
                            # zipBytes()
                            #
                            pass
                        case 'N':
                            utilidades.pulsar_enter_para_continuar("Cancelando operación.", "normal")
                            return
                        case _:
                            print(COLOR_LETRA_CYAN + "Debe seleccionar entre [S]|[N].")
        print("+"+"-"*10 +"+"+ "-"*20 +"+"+ "-"*6 +"+"+ "-"*30 +"+")

def modificar_campo_correo():
    pass

def modificar_campo_dni():
    pass

def modificar_campo_nombre():
    pass

def modificar_campo_edad():
    pass