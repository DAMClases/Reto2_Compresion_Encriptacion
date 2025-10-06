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
def introducir_campo(campo:str, input_sistema:str)-> str | int | None:
    '''Función que recoge y valida la entrada de datos del usuario.'''
    while True:
        try:
            match campo:
                case 'DNI':
                    dni = input(COLOR_TEXTO_CIAN + input_sistema).upper()
                    if utilidades.validar_dni(dni)[0]:
                        return dni
                case 'nombre':
                    nombre = input(COLOR_TEXTO_CIAN + input_sistema)
                    if utilidades.validar_nombre(nombre):
                        return nombre
                case 'edad':
                    try:
                        edad = int(input(COLOR_TEXTO_CIAN + input_sistema))
                        if utilidades.validar_edad(edad):
                            return edad
                    except ValueError:
                        utilidades.pulsar_enter_para_continuar("El dato introducido debe ser obligatoriamente numérico de tipo entero.", "error")                    
                case 'email':
                    email = input(COLOR_TEXTO_CIAN + input_sistema)
                    if utilidades.validar_correo(email):
                        return email
        except KeyboardInterrupt:
            return None
                
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
    '''Mediante la entrada de datos de los usuarios y las validaciones pertinentes se crea un nuevo registro'''    
    dni = introducir_campo("DNI", "Introduzca un DNI válido (Ej: 21137083Z) >>> ")
    if dni is None:
        utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
        return
    nombre = introducir_campo("nombre", "Introduzca un nombre >>> ")
    if nombre is None:
        utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
        return
    edad = introducir_campo("edad", "Introduzca una edad acotada entre 1-99 años >>> ")
    if edad is None:
        utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
        return
    email = introducir_campo("email", "Introduzca un email válido (Ej: jero@gmail.com / alberto@outlook.es) >>> ")
    if email is None:
        utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
        return
    pass
    #Logica ya de creación
def mostrar_registro()->None:
    '''DNI'''
    dni = introducir_campo("DNI", "Introduzca un DNI válido (Ej: 21137083Z) >>> ")
    if dni is None:
        utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
        return
    #logica de mostrar registro
    print("Aquí iría la lógica.")

def modificar_registro()->None:
    '''Campo modificacion'''
    dni = introducir_campo("DNI", "Introduzca un DNI válido (Ej: 21137083Z) >>> ")
    if dni is None:
        utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
        return
    print("Aquí iría la lógica.")

def eliminar_registro()->None:
    '''Eliminar, DNI'''
    dni = introducir_campo("DNI", "Introduzca un DNI válido (Ej: 21137083Z) >>> ")
    if dni is None:
        utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
        return
    print("Aquí iría la lógica.")

if __name__ == '__main__':
    mostrar_menu_principal()
