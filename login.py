import gestion_archivos as ga
import os

USER_DATA_PATH = "./user_data.bin"

def login():
    user_input = input("Introduce tu usuario: ")
    password_input = input("Introduce tu contraseña: ")
    if not os.path.exists(USER_DATA_PATH):
        ga.escribir_datos_usuario((user_input, password_input))
    else:
        user, password = ga.leer_datos_usuario()
        while user_input != user or password_input != password:
            print("Usuario o contraseña incorrectos")
            user_input = input("Introduce tu usuario: ")
            password_input = input("Introduce tu contraseña: ")
    return password

