import gestion_archivos as ga
import os
from colorama import Back, Fore, Style
from getpass import getpass
import utilidades

COLOR_FONDO_AZUL = Back.BLUE
COLOR_TEXTO_AMARILLO = Fore.YELLOW
COLOR_TEXTO_BLANCO = Fore.WHITE
COLOR_TEXTO_CIAN = Fore.CYAN
COLOR_TEXTO_VERDE = Fore.GREEN
COLOR_TEXTO_ROJO = Fore.RED
COLOR_TEXTO_MAGENTA = Fore.MAGENTA
USER_DATA_PATH = "./user_data.bin"

def login():
    print(COLOR_FONDO_AZUL + COLOR_TEXTO_BLANCO + "═" * 50)
    print(COLOR_FONDO_AZUL + COLOR_TEXTO_BLANCO + f"{' Iniciar Sesión ':^50}")#centramos en 50 caracteres de ancho
    print(COLOR_FONDO_AZUL + COLOR_TEXTO_BLANCO + "═" * 50 + Style.RESET_ALL)
    print()
    while True:
        user_input = input(COLOR_TEXTO_AMARILLO + "Introduce tu usuario: " )
        password_input = getpass(COLOR_TEXTO_AMARILLO + "Introduce tu contraseña: ")
        if not os.path.exists(USER_DATA_PATH):
            ga.escribir_datos_usuario(user_input, password_input)
        else:
            key = ""
            try:
                user, key = ga.leer_datos_usuario(password_input)                
                if user_input != user:
                    utilidades.pulsar_enter_para_continuar("Error de autenticación1")
                    continue
                else:
                    break
                
            except Exception as e:
                utilidades.pulsar_enter_para_continuar(f"Error de autenticación2 {e}")
    utilidades.pulsar_enter_para_continuar(f"Exito")
    return key

login()

