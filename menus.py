### - - - - - - - - - - - - - - - - - - - - - - - - - - - ###
#                       Librerías                           #
### - - - - - - - - - - - - - - - - - - - - - - - - - - - ### 

from colorama import Fore, Back, Style, init
import os
import gzip
import cryptography
import utilidades

#para el apartado gráfico debemos inicializar siempre colorama
init(autoreset=True)

### - - - - - - - - - - - - - - - - - - - - - - - - - - - ###
#  Constantes que intervienen en el diseño de la aplicación #
### - - - - - - - - - - - - - - - - - - - - - - - - - - - ###    

COLOR_FONDO_AZUL = Back.BLUE
COLOR_TEXTO_AMARILLO = Fore.YELLOW
COLOR_TEXTO_BLANCO = Fore.WHITE
COLOR_TEXTO_CIAN = Fore.CYAN
COLOR_TEXTO_VERDE = Fore.GREEN
COLOR_TEXTO_ROJO = Fore.RED
COLOR_TEXTO_MAGENTA = Fore.MAGENTA

### - - - - - - - - - - - - - - - - - - - - - - - - - - - ###
#                       Funciones                           #
### - - - - - - - - - - - - - - - - - - - - - - - - - - - ### 
def mostrar_menu_principal()->None:
    '''Despliega el menú principal con un diseño intuitivo en consola'''

    
    

    while True:
        os.system('cls') #limpiamos de forma básica la pantalla, sin necesidad de input
        print(COLOR_FONDO_AZUL + COLOR_TEXTO_BLANCO + "═" * 50)
        print(COLOR_FONDO_AZUL + COLOR_TEXTO_BLANCO + f"{' MENÚ PRINCIPAL ':^50}")#centramos en 50 caracteres de ancho
        print(COLOR_FONDO_AZUL + COLOR_TEXTO_BLANCO + "═" * 50 + Style.RESET_ALL)
        print()
        print(COLOR_TEXTO_AMARILLO + " [1]" + COLOR_TEXTO_BLANCO + " ➤ Crear registro")
        print(COLOR_TEXTO_AMARILLO + " [2]" + COLOR_TEXTO_BLANCO + " ➤ Leer registro")
        print(COLOR_TEXTO_AMARILLO + " [3]" + COLOR_TEXTO_BLANCO + " ➤ Modificar registro")
        print(COLOR_TEXTO_AMARILLO + " [4]" + COLOR_TEXTO_BLANCO + " ➤ Eliminar registro")
        print(COLOR_TEXTO_AMARILLO + " [5]" + COLOR_TEXTO_BLANCO + " ➤ Finalizar sesión")
        print()
        print(COLOR_FONDO_AZUL + COLOR_TEXTO_BLANCO + "═" * 50 + Style.RESET_ALL)
        opcion = input(COLOR_TEXTO_CIAN + "\nSeleccione una opción (1-5) >>> " + Style.RESET_ALL)

        match opcion:
            case '1':
                print(COLOR_TEXTO_VERDE + "\nCrear registro seleccionado ")
                crear_registro()
            case '2':
                print(COLOR_TEXTO_VERDE + "\nLeer registro seleccionado ")
                mostrar_registro()
            case '3':
                print(COLOR_TEXTO_VERDE + "\nModificar registro seleccionado ")
                modificar_registro()
            case '4':
                print(COLOR_TEXTO_ROJO + "\nEliminar registro seleccionado ")
                eliminar_registro()
            case '5':
                print(COLOR_TEXTO_MAGENTA + "\nFinalizando sesión... ¡Hasta pronto!")
                exit()
            case _:
                utilidades.pulsar_enter_para_continuar("\nOpción inválida. Por favor, elige un número del 1 al 5.","error")

def crear_registro()->None:
    print(COLOR_TEXTO_AMARILLO + "Función crear_registro() aún en construcción...")

def mostrar_registro()->None:
    print(COLOR_TEXTO_AMARILLO + "Función mostrar_registro() aún en construcción...")

def modificar_registro()->None:
    print(COLOR_TEXTO_AMARILLO + "Función modificar_registro() aún en construcción...")

def eliminar_registro()->None:
    print(COLOR_TEXTO_AMARILLO + "Función eliminar_registro() aún en construcción...")

if __name__ == '__main__':
    mostrar_menu_principal()
