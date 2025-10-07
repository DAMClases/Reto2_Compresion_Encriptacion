from colorama import Fore, init
import os
import re

init(autoreset=True)

COLOR_LETRA_CYAN = Fore.CYAN
COLOR_LETRA_AMARILLO = Fore.YELLOW

def pulsar_enter_para_continuar(mensaje = '', tipo = 'normal'):
    match tipo:
        case "normal":
            color = Fore.WHITE
        case "advertencia":
            color = Fore.YELLOW
        case "error":
            color = Fore.RED
        case _:
            color = Fore.WHITE

    if mensaje:
        print(color +  mensaje)
    try:
        input("Pulse enter para continuar...")
    except KeyboardInterrupt:
        pass

def limpiar_consola():
    '''Función para limpiar consola y blablabla'''
    os.system("cls" if os.name == 'nt' else "clear")

def validar_nombre(nombre: str) -> bool:
    '''Función de validación de un nombre:
        1. Valida si está vacío.
        2. Si su longitud es menor a 50 caracteres.
        3. Si se han usado caracteres numéricos o especiales.
        4. Si la composición de la cadena coincide con la regex.'''
    if not nombre:
        pulsar_enter_para_continuar("El nombre no puede estar vacío.", "advertencia")
        return False
    nombre = nombre.strip()
    if len(nombre) > 50:
        pulsar_enter_para_continuar("La longitud del nombre no puede ser mayor a 50.", "advertencia")
        return False
    
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s'-]+$" #Comentario: Regex que acepta letras, espacios, guiones y apóstrofes, ya que pueden haber nombres compuestos o extranjeros
    if re.match(patron, nombre):
        return True
    pulsar_enter_para_continuar("No se permiten caracteres numéricos o especiales.", "advertencia")
    return False

def validar_dni(dni:str)->tuple[bool,bool]:
    '''Función de validación del DNI.
    Comprueba si un DNI, NIE o CIF es correcto.
    El primer valor es si es correcto, el segundo si es un CIF.'''
    LETRAS_NIF = "TRWAGMYFPDXBNJZSQVHLCKE"
    LETRAS_NIE = "XYZ"
    LETRAS_CIF = "ABCDEFGHJNPQRSUVW"
    LETRAS_CONTROL = "JABCDEFGHI"
    #Validación de CIF
    if len(dni) == 9 and dni[0].upper() in LETRAS_CIF:
        if(((dni[0].isalpha()) and dni[1:-1].isdigit())):
            cif = dni.upper().strip()
            if len(cif) != 9 or not cif[1:8].isdigit():
                pulsar_enter_para_continuar("Formato incorrecto: el CIF debe tener 1 letra inicial, 7 dígitos y 1 carácter de control.", "advertencia")
                return (False, False)

            letra = cif[0]
            numeros = list(map(int, cif[1:8]))
            control = cif[8]

            #Cálculo del dígito de control
            suma_pares = sum(numeros[1::2])
            suma_impares = 0
            for digito in numeros[0::2]:
                suma_impares += (2 * digito // 10) + (2 * digito % 10)
            total = suma_pares + suma_impares
            digito_control = (10 - (total % 10)) % 10
            #Dependiendo del tipo de entidad, el control puede ser número o letra
            if letra in "PQRSNW":
                if control != LETRAS_CONTROL[digito_control]:
                    pulsar_enter_para_continuar("El CIF no es válido: letra de control incorrecta.", "advertencia")
                    return (False, False)
                return (True, False)
            elif letra in "ABEH":
                if control != str(digito_control):
                    pulsar_enter_para_continuar("El CIF no es válido: dígito de control incorrecto.", "advertencia")
                    return (False, False)
                return (True, False)
            else:
                if control != str(digito_control) and control != LETRAS_CONTROL[digito_control]:
                    pulsar_enter_para_continuar("El CIF no es válido: carácter de control incorrecto.", "advertencia")
                    return (False, False)
                return (True, False)
        else:
            pulsar_enter_para_continuar("Formato incorrecto: el CIF debe comenzar con una letra válida y contener solo números después.", "advertencia")
            return (False, False)
    elif len(dni) == 9 and dni[-1].isalpha():
        #Validación de NIE
        if((dni[0].upper() in LETRAS_NIE) and dni[1:-1].isdigit()):
            combinado = int(str(LETRAS_NIE.index(dni[0])) + dni[1:-1])
            if (dni[-1] == LETRAS_NIF[(combinado%23)]):
                return (True, True)
            pulsar_enter_para_continuar("El NIE no es válido: letra de control incorrecta.", "advertencia")
            return (False, False)
        #Validación de NIF
        elif (dni[:-1].isdigit()):
            if dni[-1] == LETRAS_NIF[(int(dni[:-1]) % 23)]:
                return (True, True)
            pulsar_enter_para_continuar("El DNI no es válido: letra de control incorrecta.", "advertencia")
            return (False, False)
        else:
            pulsar_enter_para_continuar("Formato incorrecto: el DNI/NIE debe tener 8 dígitos y una letra final.", "advertencia")
            return (False, False)
    pulsar_enter_para_continuar("Formato no reconocido: el valor introducido no parece ser un DNI, NIE o CIF válido.", "advertencia")
    return (False, False)



def validar_edad(edad:int)->bool:
    '''Función que valida la edad. Devuelve un valor booleano.'''
    try:
        if edad > 99 or edad < 1:
            pulsar_enter_para_continuar("La edad debe estar comprendida entre 1-99 años.", "advertencia")
            return False
        return True
    except:
        pulsar_enter_para_continuar("La edad debe ser un número entero.", "error")
        return False

def validar_correo(email:str)->bool:
    '''Función que valida el correo electrónico. Devuelve un valor booleano.'''
    if len(email) > 100:
        pulsar_enter_para_continuar("La longitud del email no puede ser superior a 100 caracteres.", "advertencia")    
        return False
    
    partes = email.split('@')
    if len(partes) != 2:
        pulsar_enter_para_continuar("Un email válido debe tener una parte reservada para el usuario y otra para el dominio.", "advertencia")    
        return False
   
    nombre_usuario, dominio_completo = partes
    dominio_partes = dominio_completo.split('.')
   
    # Validar nombre de usuario
    caracteres_validos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
    if nombre_usuario[0] == '.' or nombre_usuario[-1] == '.' or '..' in nombre_usuario:
        pulsar_enter_para_continuar("Caracteres inválidos al inicio, final o doble uso del caracter '.'.", "advertencia")    
        return False


    for i in range(len(nombre_usuario)):
        if nombre_usuario[i] not in caracteres_validos:
            pulsar_enter_para_continuar("Caracteres inválidos detectados.", "advertencia")    
            return False
        if nombre_usuario[i] in "._-" and (i == len(nombre_usuario) - 1 or nombre_usuario[i + 1] in "._-"):
            pulsar_enter_para_continuar("Caracteres inválidos detectados.", "advertencia")    
   
    # Validar dominio
    if len(dominio_partes) < 2:
        pulsar_enter_para_continuar("Un email válido debe tener una parte reservada para el usuario y otra para el dominio.", "advertencia")    
        return False
   
    for parte in dominio_partes:
        if not parte or parte[0] == '-' or parte[-1] == '-' or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-" for c in parte):
            pulsar_enter_para_continuar("Caracteres inválidos detectados.", "advertencia")    
            return False
    # Validar extensión
    extension = dominio_partes[-1]
    if len(extension) < 2:
        return False
       
    return True

def buscar_registro_especificado(estructura_datos:list[tuple[str,str,int,str]], dni:str)->None:
    """Muestra los registros introducidos en formato tabla"""
    for registro in estructura_datos:
        if registro[0] == str(dni):
                return registro
    return None


def mostrar_registros(registros:tuple) -> None:
    """Muestra los registros introducidos en formato tabla"""
    print(COLOR_LETRA_AMARILLO + "Mostrando los registros actuales encontrados")
    max_dni_length = 3
    max_nombre_length = 6
    max_correo_length = 18
    max_digitos_edad = 4
    for registro in registros:
        max_digitos_edad = max(max_digitos_edad, len(str(registro[2])))
        max_dni_length = max(max_dni_length, len(registro[0]))
        max_nombre_length = max(max_nombre_length, len(registro[1]))
        max_correo_length = max(max_correo_length, len(registro[3]))
    print("+" + "-"* (max_dni_length +2) + "+" + "-"*(max_nombre_length +2) + "+" + "-"*(max_digitos_edad +2) + "+" + "-"*(max_correo_length +2) + "+")
    print(f"| {'DNI'.center(max_dni_length)} | {'Nombre'.center(max_nombre_length)} | {'Edad'.center(max_digitos_edad)} | {'Correo electrónico'.center(max_correo_length)} |")
    print("+" + "-"* (max_dni_length +2) + "+" + "-"*(max_nombre_length +2) + "+" + "-"*(max_digitos_edad +2) + "+" + "-"*(max_correo_length +2) + "+")
    for registro in registros:
        print(f"| {registro[0].rjust(max_dni_length)} | {registro[1]:<{max_nombre_length}} | {registro[2]:<{max_digitos_edad}} | {registro[3]:<{max_correo_length}} |")
    
    print("+" + "-"* (max_dni_length +2) + "+" + "-"*(max_nombre_length +2) + "+" + "-"*(max_digitos_edad +2) + "+" + "-"*(max_correo_length +2) + "+")
    
    