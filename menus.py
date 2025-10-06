### - - - - - - - - - - - - - - - - - - - - - - - - - - - ###
#                       Librerías                           #
### - - - - - - - - - - - - - - - - - - - - - - - - - - - ### 

from colorama import Fore, Back, Style, init
import os
import gzip
import cryptography

#para el apartado gráfico debemos inicializar siempre colorama
init(autoreset=True)

### - - - - - - - - - - - - - - - - - - - - - - - - - - - ###
#                       Funciones                           #
### - - - - - - - - - - - - - - - - - - - - - - - - - - - ### 

def pulsar_enter_continuar()->None:
    '''Limpia la consola para mayor legibilidad'''
    encuadre_verde = Fore.LIGHTGREEN_EX
    input(encuadre_verde + "\nPresiona ENTER para continuar...")
    os.system('cls')

def mostrar_menu_principal()->None:
    '''Despliega el menú principal con un diseño intuitivo en consola'''
### - - - - - - - - - - - - - - - - - - - - - - - - - - - ###
#  Variables que intervienen en el diseño de la aplicación  #
### - - - - - - - - - - - - - - - - - - - - - - - - - - - ###    
    
    fondo_azul = Back.BLUE
    encuadre_amarillo = Fore.YELLOW
    encuadre_blanco = Fore.WHITE
    encuadre_cian = Fore.CYAN
    encuadre_verde = Fore.GREEN
    encuadre_rojo = Fore.RED
    encuadre_magenta = Fore.MAGENTA

    while True:
        os.system('cls') #limpiamos de forma básica la pantalla, sin necesidad de input
        print(fondo_azul + encuadre_blanco + "═" * 50)
        print(fondo_azul + encuadre_blanco + f"{' MENÚ PRINCIPAL ':^50}")#centramos en 50 caracteres de ancho
        print(fondo_azul + encuadre_blanco + "═" * 50 + Style.RESET_ALL)
        print()
        print(encuadre_amarillo + " [1]" + encuadre_blanco + " ➤ Crear registro")
        print(encuadre_amarillo + " [2]" + encuadre_blanco + " ➤ Leer registro")
        print(encuadre_amarillo + " [3]" + encuadre_blanco + " ➤ Modificar registro")
        print(encuadre_amarillo + " [4]" + encuadre_blanco + " ➤ Eliminar registro")
        print(encuadre_amarillo + " [5]" + encuadre_blanco + " ➤ Finalizar sesión")
        print()
        print(fondo_azul + encuadre_blanco + "═" * 50 + Style.RESET_ALL)
        opcion = input(encuadre_cian + "\nSeleccione una opción (1-5) >>> " + Style.RESET_ALL)

        match opcion:
            case '1':
                print(encuadre_verde + "\nCrear registro seleccionado ")
                crear_registro()
                pulsar_enter_continuar()
            case '2':
                print(encuadre_verde + "\nLeer registro seleccionado ")
                mostrar_registro()
                pulsar_enter_continuar()
            case '3':
                print(encuadre_verde + "\nModificar registro seleccionado ")
                modificar_registro()
                pulsar_enter_continuar()
            case '4':
                print(Fore.RED + "\nEliminar registro seleccionado ")
                eliminar_registro()
                pulsar_enter_continuar()
            case '5':
                print(encuadre_magenta + "\nFinalizando sesión... ¡Hasta pronto!")
                exit()
            case _:
                print(encuadre_rojo + "\nOpción inválida. Por favor, elige un número del 1 al 5.")
                pulsar_enter_continuar()

def crear_registro()->None:
    encuadre_amarillo = Fore.YELLOW
    print(encuadre_amarillo + "Función crear_registro() aún en construcción...")

def mostrar_registro()->None:
    encuadre_amarillo = Fore.YELLOW
    print(encuadre_amarillo + "Función mostrar_registro() aún en construcción...")

def modificar_registro()->None:
    encuadre_amarillo = Fore.YELLOW
    print(encuadre_amarillo + "Función modificar_registro() aún en construcción...")

def eliminar_registro()->None:
    encuadre_amarillo = Fore.YELLOW
    print(encuadre_amarillo + "Función eliminar_registro() aún en construcción...")

if __name__ == '__main__':
    mostrar_menu_principal()
