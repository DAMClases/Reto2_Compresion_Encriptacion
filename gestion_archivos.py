import utilidades_archivos as ez
import os
import struct

BIN_PATH = "./data.bin"

def leer_archivo(password: str) -> list[tuple[str, str, int, str]] | None:
    """Lee el archivo binario, lo descifra y descomprime.
    Devuelve una lista de tuplas con los registros o None si hay error."""
    try:
        # Si no existe, devuelve lista vacía
        if not os.path.exists(BIN_PATH):
            return []

        # Lo primero es descifrar y descomprimir
        with open(BIN_PATH, 'rb') as file:
            binario = file.read()

        data_raw = ez.desencriptar_bytes(binario, password)
        if data_raw is None:
            raise ValueError("No se pudo descifrar el archivo.")

        data_raw = ez.descomprimir_bytes(data_raw)
        if data_raw is None:
            raise ValueError("No se pudo descomprimir el archivo.")
        
        # Ahora leemos los registros saltando de tamaño en tamaño
        records = []
        size = ez.record_size()

        offset = 0
        total = len(data_raw)
        while offset + size <= total:
            chunk = data_raw[offset: offset + size]
            offset += size
            # Por tanto, aquí ya tenemos un “chunk” de tamaño correcto que desempaquetamos
            rec = ez.desempaquetar_registro(chunk)
            if rec:
                records.append(rec)

        # Si hay “sobrantes”, el fichero estaba corrupto o formato cambió
        if offset != total:
            print("Advertencia: bytes residuales no alineados a tamaño de registro.")

        return records

    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def escribir_archivo(data: tuple[str, str, int, str], password: str) -> bool:
    """
    Añade UN registro al contenedor:
    - Si existe: lee → descifra → descomprime → añade → recomprime → cifra → sobrescribe.
    - Si no existe: crea con un único registro.
    """
    try:
        if not data or len(data) != 4: raise ValueError("Los datos a escribir deben contener 4 elementos: ID, nombre, edad y correo electrónico.")

        paquete_registro_nuevo = ez.empaquetar_registro(*data)
        if paquete_registro_nuevo is None:
            raise ValueError("Falló el empaquetado del registro.")

        # Carga actual si hay fichero
        if os.path.exists(BIN_PATH):
            with open(BIN_PATH, 'rb') as f:
                binario = f.read()

            datos_archivo = ez.desencriptar_bytes(binario, password)
            if datos_archivo is None:
                raise ValueError("No se pudo descifrar el contenedor existente.")

            datos_archivo = ez.descomprimir_bytes(datos_archivo)
            if datos_archivo is None:
                raise ValueError("No se pudo descomprimir el contenedor existente.")
        else:
            datos_archivo = b""

        # COmprobamos si existe (por ID) y actualizamos si coincide
        actualizando = False
        borrando = False
        for i in range(0, len(datos_archivo), ez.record_size()):
            existing = ez.desempaquetar_registro(datos_archivo[i:i + ez.record_size()])
            if existing and existing[0] == data[0]:
                # Si la edad es -1 es la condición de eliminado, por lo que saltamos estos bytes
                if data[2] == -1:
                    borrando = True
                    datos_archivo = datos_archivo[:i] + datos_archivo[i + ez.record_size():]
                    input("Registro borrado. Pulsa Enter para continuar...")
                    break
                # Si no, actualizamos con los bytes de la actualización
                datos_archivo = datos_archivo[:i] + paquete_registro_nuevo + datos_archivo[i + ez.record_size():]
                actualizando = True
                break
        # Concatenamos si no estamos actualizando ni borrando
        if not actualizando and not borrando:
            datos_final = datos_archivo + paquete_registro_nuevo
        else:
            datos_final = datos_archivo
        # Liberamos memoria de los datos antiguos cuando ya estén usados, por si aumenta demasiado los registros
        del(datos_archivo)
        datos_comprimidos = ez.comprimir_bytes(datos_final)
        del(datos_final)
        if datos_comprimidos is None:
            raise ValueError("No se pudo comprimir el contenedor.")

        datos_encriptados = ez.encriptar_bytes(datos_comprimidos, password)
        if datos_encriptados is None:
            raise ValueError("No se pudo cifrar el contenedor.")

        with open(BIN_PATH, 'wb') as f:
            f.write(datos_encriptados)

        del(datos_encriptados)
        return True
    except TypeError as te:
        print(f"Error con los tipos de datos introducidos. {te}")
    except AttributeError as ae:
        print(f"importación circular: {ae}")
    except ValueError as ve:
        print(f"ErrorA. {ve}")
    except Exception as e:
        print(f"Error al escribir el archivo: {e}")
        return False

def escribir_datos_usuario(user: str, password: str) -> bool:
    """Escribe los datos encriptados del usuario en un archivo cifrado usando la contraseña introducida por el usuario como llave.
    En este se guarda el nombre de usuario y la clave de cifrado de los datos personales."""
    try:
        with open("./user_data.bin", "wb") as f:
            f.write(ez.encriptar_user_data(user, password) )
            return True
    except Exception as e:
        print(f"Error al escribir el archivo: {e}")
        return False
    
def leer_datos_usuario(password:str) -> tuple[str, bytes] | None:
    """Lee los datos del archivo de usuario. Usa la constraña introducida para descifrar.
     Devuelve (usuario, clave) o None si falla."""
    try:
        with open("./user_data.bin", "rb") as f:
            return ez.desencriptar_user_data(f.read(), password)
    except TypeError:
        print("Error: Contraseña incorrecta.")
        return None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None