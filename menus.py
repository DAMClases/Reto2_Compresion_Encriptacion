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
key = ""
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
def introducir_campo(campo:str, input_sistema:str, actualizando:bool = False)-> str | int | None:
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
                    if actualizando and nombre == '':
                        return None
                    if utilidades.validar_nombre(nombre):
                        return nombre
                case 'edad':
                    try:
                        edad = input(COLOR_TEXTO_CIAN + input_sistema)
                        if actualizando and edad == '':
                            return None
                        edad = int(edad)
                        if utilidades.validar_edad(edad):
                            return edad
                    except ValueError:
                        utilidades.pulsar_enter_para_continuar("El dato introducido debe ser obligatoriamente numérico de tipo entero.", "error")                    
                case 'email':
                    email = input(COLOR_TEXTO_CIAN + input_sistema)
                    if actualizando and email == '':
                        return None
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
        print(COLOR_TEXTO_AMARILLO + " [2]" + COLOR_TEXTO_BLANCO + " ➤ Leer registro(s)")
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
    utilidades.limpiar_consola()
    print(COLOR_TEXTO_AMARILLO + "Opción actual: crear registro")   
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
    
    estructura_datos = gestion_archivos.escribir_archivo((dni, nombre, edad, email), key)
    if estructura_datos:
        utilidades.pulsar_enter_para_continuar("Se ha creado un nuevo registro.", "normal")
        utilidades.limpiar_consola()
        return
    utilidades.pulsar_enter_para_continuar("Error al modificar el archivo.", "error")
    return

def mostrar_menu_leer_registro()->None:
    '''Dada una estructura de datos previamente cargada y un DNI se debe filtrar su registro.'''
    while True:
        try:
            print(COLOR_TEXTO_AMARILLO + "Opción actual: leer registro(s)")   
            print(COLOR_TEXTO_AMARILLO + " [1]" + COLOR_TEXTO_BLANCO + " ➤ Leer todos los registros")
            print(COLOR_TEXTO_AMARILLO + " [2]" + COLOR_TEXTO_BLANCO + " ➤ Leer registro específico")
            opciones = input(COLOR_TEXTO_AMARILLO + "Seleccione la opción pertinente >>> ")
        except KeyboardInterrupt:
            return 
        match opciones:
            case '1':
                utilidades.limpiar_consola()
                estructura_datos = gestion_archivos.leer_archivo(key)
                if estructura_datos:
                    utilidades.mostrar_registros(estructura_datos)
                    if estructura_datos:
                        while True:
                            try:
                                confirmacion = input(COLOR_TEXTO_CIAN + "\n¿Desea exportar los datos a formato JSON? [S]|[N] >>> ").upper()
                            except KeyboardInterrupt:
                                utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
                                break
                            if confirmacion == 'S':
                                utilidades_archivos.exportar_json(estructura_datos)
                                break
                            elif confirmacion == 'N':
                                utilidades.pulsar_enter_para_continuar("Operación completada.", "normal")
                                break
                    return
                else:
                    utilidades.pulsar_enter_para_continuar("La estructura de datos no existe aún.", "advertencia")
                    return
                
            case '2':
                utilidades.limpiar_consola()
                dni = introducir_campo("DNI", "Introduzca un DNI válido (Ej: 21137083Z) >>> ")
                if dni is None:
                    utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
                    return
                estructura_datos = gestion_archivos.leer_archivo(key)
                if estructura_datos:
                    registro = utilidades.buscar_registro_especificado(estructura_datos, dni)
                    if registro:
                        utilidades.limpiar_consola()
                        utilidades.mostrar_registros([registro])
                        if registro:
                            while True:
                                try:
                                    confirmacion = input(COLOR_TEXTO_CIAN + "\n¿Desea exportar los datos a formato JSON? [S]|[N] >>> ").upper()
                                except KeyboardInterrupt:
                                    utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
                                    break
                                if confirmacion == 'S':
                                    utilidades_archivos.exportar_json([registro])
                                    break
                                elif confirmacion == 'N':
                                    utilidades.pulsar_enter_para_continuar("Operación completada.", "normal")
                                    break
                        return
                    else:
                        utilidades.pulsar_enter_para_continuar("El registro especificado no existe.", "advertencia")
                        return
                utilidades.pulsar_enter_para_continuar("La estructura de datos no existe aún.", "advertencia")
                return
            case _:
                utilidades.pulsar_enter_para_continuar("Tecla incorrecta. Volviendo al menú principal.", "advertencia")
                return
            

def mostrar_menu_modificar_registro()->None:
    '''Campo modificacion'''
    utilidades.limpiar_consola()
    print(COLOR_TEXTO_AMARILLO + "Opción actual: modificar registro")   
    dni = introducir_campo("DNI", "Introduzca un DNI válido (Ej: 21137083Z) >>> ")
    utilidades.limpiar_consola()
    if dni is None:
        utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
        return
    estructura_de_datos = gestion_archivos.leer_archivo(key)
    if estructura_de_datos:
        registro = utilidades.buscar_registro_especificado(estructura_de_datos, dni)
        if registro:
            utilidades.mostrar_registros([registro])
            print(COLOR_TEXTO_AMARILLO + "Se ha encontrado el registro.\nInstrucciones: \n[1]. Pulse ENTER para dejar el valor actual sin modificar. \n[2]. Introduzca nuevas opciones y pulse ENTER para continuar con otro campo.")
            nuevo_nombre = introducir_campo("nombre", "Introduzca un nuevo nombre >>> ", True)
            if nuevo_nombre is None:
                nuevo_nombre = registro[1]
            nueva_edad = introducir_campo("edad", "Introduzca una nueva edad acotada entre 1-99 años >>> ", True)
            if nueva_edad is None:
                nueva_edad = registro[2]
            nuevo_email = introducir_campo("email", "Introduzca un nuevo email válido (Ej: jero@gmail.com / alberto@outlook.es) >>> ", True)
            if nuevo_email is None:
                nuevo_email = registro[3]
            registro = (dni, nuevo_nombre, nueva_edad, nuevo_email)
            gestion_archivos.escribir_archivo(registro, key)
            utilidades.pulsar_enter_para_continuar("Registro modificado correctamente.", "normal")
            return
        utilidades.pulsar_enter_para_continuar("No se ha encontrado el registro.", "advertencia")
        return
    utilidades.pulsar_enter_para_continuar("La estructura de datos no existe.", "error")
    return

def mostrar_menu_eliminar_registro()->None:
    '''Eliminar, DNI'''
    utilidades.limpiar_consola()
    print(COLOR_TEXTO_AMARILLO + "Opción actual: eliminar registro")   
    dni = introducir_campo("DNI", "Introduzca un DNI válido (Ej: 21137083Z) >>> ")
    if dni is None:
        utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
        return
    estructura_de_datos = gestion_archivos.leer_archivo(key)
    if estructura_de_datos:
        registro = utilidades.buscar_registro_especificado(estructura_de_datos, dni)
        if registro:
            utilidades.mostrar_registros([registro])
            try:
                confirmado = input("¿Desea eliminar el registro? [S]|[N] >>> ").upper()
            except KeyboardInterrupt:
                utilidades.pulsar_enter_para_continuar("Operación cancelada.", 'normal')
                return
            match confirmado:
                case 'S':
                    nueva_estructura = []
                    for reg in estructura_de_datos:
                        if reg[0] != dni:
                            nueva_estructura.append(reg)
                    try: 
                        if os.path.exists(gestion_archivos.BIN_PATH):
                            os.remove(gestion_archivos.BIN_PATH)  
                        for reg in nueva_estructura:
                            gestion_archivos.escribir_archivo(reg, key)  
                        utilidades.pulsar_enter_para_continuar("Registro eliminado correctamente.", "normal")
                        return
                    except Exception as e:
                        utilidades.pulsar_enter_para_continuar(f"Error al eliminar el registro: {e}", "error")
                        return
                case 'N':
                    utilidades.pulsar_enter_para_continuar("Cancelando operación.", "normal")
                    return
                case _:
                    utilidades.pulsar_enter_para_continuar("Cancelando operación.", "normal")
                    return

        pass
    pass

def mostrar_menu_login()->str:
    '''Despliega el menú de login con un diseño intuitivo en consola'''
    import login
    global key
    key =  str(login.login())
    if key:
        mostrar_menu_principal()