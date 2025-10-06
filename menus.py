### - - - - - - - - - - - - - - - - - - - - - - - - - - - ###
#                       Librerías                           #
### - - - - - - - - - - - - - - - - - - - - - - - - - - - ### 

from colorama import Fore, Back, Style, init
import os
import gzip
import cryptography
import utilidades
import utilidades_archivos
import gestion_archivos

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
                case _:
                    utilidades.pulsar_enter_para_continuar("", "normal")                    
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
                mostrar_menu_crear_registro()
            case '2':
                print(COLOR_TEXTO_VERDE + "\nLeer registro seleccionado ")
                mostrar_menu_leer_registro()
            case '3':
                print(COLOR_TEXTO_VERDE + "\nModificar registro seleccionado ")
                mostrar_menu_modificar_registro()
            case '4':
                print(COLOR_TEXTO_ROJO + "\nEliminar registro seleccionado ")
                mostrar_menu_eliminar_registro()
            case '5':
                print(COLOR_TEXTO_MAGENTA + "\nFinalizando sesión... ¡Hasta pronto!")
                exit()
            case _:
                utilidades.pulsar_enter_para_continuar("\nOpción inválida. Por favor, elige un número del 1 al 5.","error")

def mostrar_menu_crear_registro()->None:
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
    
    estructura_datos = gestion_archivos.escribir_archivo((dni, nombre, edad, email), "mi_contraseña_segura")
    if estructura_datos:
        utilidades.pulsar_enter_para_continuar("Se ha creado un nuevo registro.", "normal")
        utilidades.limpiar_consola()
        return
    utilidades.pulsar_enter_para_continuar("Error al modificar el archivo.", "error")
    return

def mostrar_menu_leer_registro()->None:
    '''Dada una estructura de datos previamente cargada y un DNI se debe filtrar su registro.'''
    dni = introducir_campo("DNI", "Introduzca un DNI válido (Ej: 21137083Z) >>> ")
    if dni is None:
        utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
        return
    estructura_datos = gestion_archivos.leer_archivo("mi_contraseña_segura")
    print(estructura_datos)
    if estructura_datos:
        registro = utilidades.buscar_registro_especificado(estructura_datos, dni)
        print(registro)
        if registro:
            utilidades.limpiar_consola()
            utilidades.mostrar_registros([registro])
            utilidades.pulsar_enter_para_continuar("Operación completada.", "normal")
            return
        utilidades.pulsar_enter_para_continuar("El registro especificado no existe.", "advertencia")
        return
    utilidades.pulsar_enter_para_continuar("La estructura de datos no existe aún.", "advertencia")
    return

def mostrar_menu_modificar_registro()->None:
    '''Campo modificacion'''
    # dni = introducir_campo("DNI", "Introduzca un DNI válido (Ej: 21137083Z) >>> ")
    
    # if dni is None:
    #     utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
    #     return
    # utilidades.modificar_campos_registro(dni)
    gestion_archivos.escribir_archivo(("21137083Z", "Angel Melchor", 23, "melchor@algo.pro"), "mi_contraseña_segura")
    registros = gestion_archivos.leer_archivo("mi_contraseña_segura")
    utilidades.mostrar_registros(registros)
    utilidades.pulsar_enter_para_continuar("")

def mostrar_menu_eliminar_registro()->None:
    '''Eliminar, DNI'''
    dni = introducir_campo("DNI", "Introduzca un DNI válido (Ej: 21137083Z) >>> ")
    if dni is None:
        utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
        return
    estructura_de_datos = gestion_archivos.leer_archivo("mi_contraseña_segura")
    if estructura_de_datos:
        registro = utilidades.buscar_registro_especificado(estructura_de_datos, dni)
        if registro:
            utilidades.mostrar_registros([registro])
            confirmado = input("¿Desea eliminar el registro? [S]|[N] >>> ")
            match confirmado:
                case 'S':
                    nueva_estructura = []
                    for reg in estructura_de_datos:
                        if reg[0] != dni:
                            nueva_estructura.append(reg)
                    #vamos a borrar el archivo y luego sobreescribirlo con un ciclo for
                    try: 
                        if os.path.exists(gestion_archivos.BIN_PATH):
                            os.remove(gestion_archivos.BIN_PATH)  
                        for reg in nueva_estructura:
                            gestion_archivos.escribir_archivo(reg, "mi_contraseña_segura")  
                        utilidades.pulsar_enter_para_continuar("Registro eliminado correctamente.", "normal")
                    except Exception as e:
                        utilidades.pulsar_enter_para_continuar(f"Error al eliminar el registro: {e}", "error")
                case 'N':
                    utilidades.pulsar_enter_para_continuar("Cancelando operación.", "normal")
                case _:
                    pass
        pass
    pass

if __name__ == '__main__':
    mostrar_menu_principal()
