import EncriptZip as ez
import os.path

def ReadFile(pswd: str) -> list[tuple[str, str, int, str]] | None:
    """Lee datos binarios de un archivo."""
    try:
        with open("./data.bin", 'rb') as file:
            data = file.read()
            print(data)
            data = ez.unpackRecord(ez.unzipBytes(ez.decryptBytes(data, pswd)))
        return data
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def WriteFile(data: list|tuple[str, str, int, str], pswd: str) -> bool:
    """Escribe datos binarios en un archivo."""
    try:
        if not data or len(data) != 4: raise ValueError("Los datos a escribir deben contener 4 elementos: ID, nombre, edad y correo electrónico.")
        if not isinstance(data, (list, tuple)): raise TypeError("Los datos a escribir deben ser una lista o una tupla.")
        data = ez.encryptBytes(ez.zipBytes(ez.packRecord([data])), pswd)
        print(ReadFile(pswd))
        print(data)
        if not os.path.exists("./data.bin"):
            with open("./data.bin", 'wb') as file:
                file.write(data)
        else:
            with open("./data.bin", 'ab') as file:
                file.write(data)
        return True
    except Exception as e:
        print(f"Error al escribir el archivo: {e}")
        return False
    
if __name__ == "__main__":
    pswd = "mi_contraseña_segura"
    data = ("51164528k", "Alberto", 18, "alberto@gmail.com")
    WriteFile(data, pswd)
    data = ReadFile(pswd)
    print(data)
