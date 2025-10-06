from colorama import Fore, init
import os

init(autoreset=True)

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

def validar_nombre(nombre:str)->bool:
    '''Función de validación de nombre'''
    if nombre:
        if len(nombre)>50:
            print("La longitud del nombre no puede ser mayor a 50.")
            return False
        nombre = nombre.strip(" ")
        if nombre.isalpha():
            return True
        print('No se permiten caracteres numéricos')
        return False
    print("El nombre no puede estar vacío.")
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
                return False
           
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
                return (control == LETRAS_CONTROL[digito_control], False)
            elif letra in "ABEH":
                return (control == str(digito_control), False)
            else:
                return ((control == str(digito_control) or control == LETRAS_CONTROL[digito_control]), False)  # Ambos posibles
        else:
            return (False, False)
   
    elif len(dni) == 9 and dni[-1].isalpha():
        #Validación de NIE
        if((dni[0].upper() in LETRAS_NIE) and dni[1:-1].isdigit()):
            combinado = int(str(LETRAS_NIE.index(dni[0])) + dni[1:-1])
            if (dni[-1] == LETRAS_NIF[(combinado%23)]):
                return (True, True)
        #Validación de NIF
        elif (dni[:-1].isdigit()):
            if dni[-1] == LETRAS_NIF[(int(dni[:-1]) % 23)]:
                return (True, True)
        else:
            return (False, False)
    return (False, False)


def validar_edad(edad:int)->bool:
    '''Función que valida la edad. Devuelve un valor booleano.'''
    try:
        if edad > 99 or edad < 1:
            print("La edad debe estar comprendida entre 1-99 años.")
            return False
        return True
    except:
        print("La edad debe ser un número entero.")
        return False

def validar_correo(email:str)->bool:
    '''Función que valida el correo electrónico. Devuelve un valor booleano.'''
    if len(email) > 100:
        return False
    
    partes = email.split('@')
    if len(partes) != 2:
        return False
   
    nombre_usuario, dominio_completo = partes
    dominio_partes = dominio_completo.split('.')
   
    # Validar nombre de usuario
    caracteres_validos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
    if nombre_usuario[0] == '.' or nombre_usuario[-1] == '.' or '..' in nombre_usuario:
        return False


    for i in range(len(nombre_usuario)):
        if nombre_usuario[i] not in caracteres_validos:
            return False
        if nombre_usuario[i] in "._-" and (i == len(nombre_usuario) - 1 or nombre_usuario[i + 1] in "._-"):
            return False
   
    # Validar dominio
    if len(dominio_partes) < 2:
        return False
   
    for parte in dominio_partes:
        if not parte or parte[0] == '-' or parte[-1] == '-' or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-" for c in parte):
            return False
    # Validar extensión
    extension = dominio_partes[-1]
    if len(extension) < 2:
        return False
       
    return True

