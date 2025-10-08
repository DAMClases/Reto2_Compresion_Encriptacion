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

def login() -> str | None:
    """Muestra un menú para ingresar usuario y contraseña.
    Si el archivo de datos del usuario no existe, lo crea con los datos introducidos.
    Si existe, verifica las credenciales y devuelve la clave de cifrado si son correctas.
    Devuelve None si el usuario cancela la operación o si las credenciales son incorrectas"""
    print(COLOR_FONDO_AZUL + COLOR_TEXTO_BLANCO + "═" * 50)
    print(COLOR_FONDO_AZUL + COLOR_TEXTO_BLANCO + f"{' Iniciar Sesión ':^50}")#centramos en 50 caracteres de ancho
    print(COLOR_FONDO_AZUL + COLOR_TEXTO_BLANCO + "═" * 50 + Style.RESET_ALL)
    print()
    while True:
        # Entrada de usuario y contraseña
        utilidades.limpiar_consola()
        if not os.path.exists(USER_DATA_PATH):
            print(COLOR_TEXTO_CIAN + "No se han encontrado datos de usuario. Se procederá a crear una nueva cuenta." + Style.RESET_ALL)
        print("Por favor, introduce tus credenciales." + COLOR_TEXTO_VERDE + "(Ctrl+C para cancelar)" + Style.RESET_ALL)
        try:
            user_input = input(COLOR_TEXTO_AMARILLO + "Introduce tu usuario: " )
        except KeyboardInterrupt:
            print(COLOR_TEXTO_ROJO + "\nOperación cancelada por el usuario." + Style.RESET_ALL)
            return None
        try:
            password_input = getpass(COLOR_TEXTO_AMARILLO + "Introduce tu contraseña: ")
        except KeyboardInterrupt:
            print(COLOR_TEXTO_ROJO + "\nOperación cancelada por el usuario." + Style.RESET_ALL)
            return None
        # Si no existe el archivo de datos del usuario, lo crea
        if not os.path.exists(USER_DATA_PATH):
            ga.escribir_datos_usuario(user_input, password_input)
            utilidades.pulsar_enter_para_continuar(COLOR_TEXTO_VERDE + "Cuenta creada exitosamente. " + COLOR_TEXTO_AMARILLO + "Por favor, inicia sesión." ) 
            continue
        # Si existe, verifica las credenciales con los datos almacenados
        else:
            key = ""
            try:
                user, key = ga.leer_datos_usuario(password_input)
                # Aquí ya tendríamos la clave de cifrado si la contraseña es correcta, pero comprobamos el usuario
                if user_input != user:
                    utilidades.pulsar_enter_para_continuar("Credenciales incorrectas, inténtalo de nuevo.")
                    continue
                else:
                    break
            except TypeError:
                utilidades.pulsar_enter_para_continuar("Error de autenticación")
            except Exception as e:
                utilidades.pulsar_enter_para_continuar(f"Error de autenticación2 {e}")
    utilidades.pulsar_enter_para_continuar(f"Login exitoso.")
    return key
