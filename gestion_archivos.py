import utilidades_archivos as ez
import os

BIN_PATH = "./data.bin"

def leer_archivo(password: str) -> list[tuple[str, str, int, str]] | None:
    """Lee datos binarios de un archivo."""
    try:
        if not os.path.exists(BIN_PATH):
            return []

        with open(BIN_PATH, 'rb') as file:
            binario = file.read()

        data_raw = ez.desencriptar_bytes(binario, password)
        if data_raw is None:
            raise ValueError("No se pudo descifrar el archivo.")

        data_raw = ez.descomprimir_bytes(data_raw)
        if data_raw is None:
            raise ValueError("No se pudo descomprimir el archivo.")

        records = []
        size = ez.record_size()

        offset = 0
        total = len(data_raw)
        while offset + size <= total:
            chunk = data_raw[offset: offset + size]
            offset += size
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

        packed = ez.empaquetar_registro(*data)
        if packed is None:
            raise ValueError("Falló el empaquetado del registro.")

        # Carga actual si hay fichero
        if os.path.exists(BIN_PATH):
            with open(BIN_PATH, 'rb') as f:
                binario = f.read()

            current = ez.desencriptar_bytes(binario, password)
            if current is None:
                raise ValueError("No se pudo descifrar el contenedor existente.")

            current = ez.descomprimir_bytes(current)
            if current is None:
                raise ValueError("No se pudo descomprimir el contenedor existente.")
        else:
            current = b""

        # COmprobamos si existe (por ID) y actualizamos si coincide
        actualizando = False
        borrando = False
        for i in range(0, len(current), ez.record_size()):
            existing = ez.desempaquetar_registro(current[i:i + ez.record_size()])
            if existing and existing[0] == data[0]:
                if data[2] == -1:
                    borrando = True
                    current = current[:i] + current[i + ez.record_size():]
                    input("Registro borrado. Pulsa Enter para continuar...")
                    break
                current = current[:i] + packed + current[i + ez.record_size():]
                actualizando = True
                break
        # Añade y reempaqueta
        if not actualizando and not borrando:
            new_plain = current + packed
        else:
            new_plain = current

        zipped = ez.comprimir_bytes(new_plain)
        if zipped is None:
            raise ValueError("No se pudo comprimir el contenedor.")

        encrypted = ez.encriptar_bytes(zipped, password)
        if encrypted is None:
            raise ValueError("No se pudo cifrar el contenedor.")

        with open(BIN_PATH, 'wb') as f:
            f.write(encrypted)

        return True

    except Exception as e:
        print(f"Error al escribir el archivo: {e}")
        return False

if __name__ == "__main__":
    password = "mi_contraseña_segura"
    escribir_archivo(("51164528K", "Alberto", 18, "alberto@gmail.com"), password)
    escribir_archivo(("12312312D", "Jero", 35, "jero@gmail.com"), password)
    escribir_archivo(("81273918Z", "Cristo", 25, "cristo@gmail.com"), password)
    escribir_archivo(("12312312D", "Jeronimo", 23, "jeroedited@gmail.com"), password)
    print("DATA ON MAIN:", leer_archivo(password))
