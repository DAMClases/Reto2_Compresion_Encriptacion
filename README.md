# Reto_2_Compresion_Encriptacion
Programa que gestiona un archivo binario de forma segura utilizando compresión y encriptación


*AÑADIR DESCRIPCION DEL PROGRAMA Y TECNOLOGIA, LIBRERIAS ETC*

# Descripción técnica del programa

lorem ipsum....

# Reto 2 - Alberto, Cristopher, Jerónimo
## Ficheros Binarios con Compresión y Encriptación: Gestión Segura de Archivos
**Descripción:** El grupo debe desarrollar un programa que gestione un archivo binario de forma segura utilizando compresión y encriptación. El objetivo es manejar datos sensibles (por ejemplo, información personal o empresarial), asegurándose de que la información esté comprimida y encriptada cuando se almacene, y se pueda descomprimir y desencriptar al leerla.

El programa debe permitir:

● **Crear un archivo binario comprimido y encriptado:** Almacenar registros que contengan un ID, nombre, edad y correo electrónico. Estos datos deben
comprimirse antes de almacenarlos.

● **Leer y mostrar un archivo descomprimido y desencriptado:** El programa debe descomprimir y desencriptar los datos antes de mostrarlos al usuario.

● **Modificar un registro:** Permitir que el usuario modifique un registro, aplicando nuevamente compresión y encriptación.

● **Eliminar un registro:** Permitir que el usuario elimine un registro, asegurándose de que el archivo esté correctamente comprimido tras la eliminación.

## Requisitos

1. **Compresión de datos:** Usa el módulo zlib o gzip para comprimir los datos antes de almacenarlos en el archivo binario.
2. **Encriptación de datos:** Utiliza el módulo cryptography para encriptar y desencriptar los datos almacenados.
3. **Estructura de los registros:** Los registros deben empaquetarse utilizando struct, y luego ser comprimidos y encriptados.
4. **Acceso aleatorio:** El acceso a los registros debe ser aleatorio utilizando seek() y tell() después de desencriptar y descomprimir los datos.
5. **Manejo de excepciones:** Maneja correctamente las excepciones al trabajar con encriptación, compresión y acceso aleatorio. 

## Recursos Adicionales

● Documentación de zlib para compresión.

● Documentación de cryptography para encriptación de datos.

## Ejemplo de Flujo del Programa
1. **Crear Registro:** El programa solicita al usuario que ingrese un ID, nombre, edad y correo. Luego, comprime y encripta los datos antes de almacenarlos.
2. **Leer Registro:** Descomprime y desencripta el registro seleccionado para mostrarlo al usuario.
3. **Modificar Registro:** Permite modificar un registro existente, aplicando nuevamente la compresión y encriptación antes de almacenarlo.
4. **Eliminar Registro:** Elimina el registro seleccionado y reorganiza el archivo binario comprimido.

## Desafíos Extras (Opcionales)

● Implementar un sistema de autenticación por contraseña para desencriptar los datos.

● Implementar una funcionalidad para exportar los datos desencriptados a un archivo de texto o JSON.




# Descripción técnica del programa

El programa permite al usuario almacenar datos de forma encriptada y comprimida utilizando las librerías cryptography y zlib. El programa se compone principalmente de dos menús:

### Menu de login

El menú de login permite crear un solo usuario con una contraseña en la primera ejecución del programa. En posteriores ejecuciones se deberá de acceder con la clave de usuario y la clave de contraseña. 

**Nota**: Solo puede existir para esta versión del programa un solo usuario y una contraseña asociada. 

**A tener en cuenta**: Los registros de los archivos están asociados a la clave de la contraseña, ya que se usa para desencriptar los datos posteriormente, para ello consiguiendo la clave de descifrado.

```
══════════════════════════════════════════════════
                  Iniciar Sesión                  
══════════════════════════════════════════════════

Introduce tu usuario:
Introduce tu contraseña: 
```

El menu de login da paso al menu principal y sus funcionalidades, que será el main de la aplicación.

### Menu principal

El menú principal que contiene las diferentes opciones a elegir.

```
══════════════════════════════════════════════════
                  MENÚ PRINCIPAL
══════════════════════════════════════════════════

 [1] ➤ Crear registro
 [2] ➤ Leer registro(s)
 [3] ➤ Modificar registro
 [4] ➤ Eliminar registro
 [5] ➤ Finalizar sesión

══════════════════════════════════════════════════

Seleccione una opción (1-5) >>> 
```

El usuario debe introducir un número indicado para cada opción. Si se equivoca, hay un mensaje amistoso que informa al usuario y refresca nuevamente la pantalla.
```
Opción inválida. Por favor, elige un número del 1 al 5.
Pulse enter para continuar...
```
### 1. Crear registro

La secuencia para crear un registro comienza de la siguiente manera:

1. El usuario introduce un DNI - se valida mediante funciones auxiliares y si es válido y no existe ya en el registro, continua con el proceso.
2. El usuario introduce un nombre limitado a 50 caracteres de longitud. Si es válido, continua con el proceso.
3. El usuario introduce una edad acotada en el rango de 1-99 años. Si es válida, continua con el proceso.
4. El usuario introduce un correo electrónico. Si la función interna la valida, da paso a la creación de un nuevo registro haciendo las pertinentes llamadas de funciones.

Un ejemplo completo de ejecución de la función podría ser la siguiente:

```
Opción actual: crear registro
Introduzca un DNI válido (Ej: 21137083Z) >>> 21137083z
Introduzca un nombre >>> Cristopher Tester
Introduzca una edad acotada entre 1-99 años >>> 25
Introduzca un email válido (Ej: jero@gmail.com / alberto@outlook.es) >>> cristotester@gmail.com
Se ha creado un nuevo registro.
Pulse enter para continuar...
```

En caso de error de validación en cada uno de los campos el programa lanzará mensajes amistosos al usuario. Veamos un par de ejemplos:

```
Opción actual: crear registro
//CASO DNI
Introduzca un DNI válido (Ej: 21137083Z) >>> 2113
Formato no reconocido: el valor introducido no parece ser un DNI, NIE o CIF válido.
Pulse enter para continuar...
//CASO NOMBRE
Introduzca un nombre >>>  
El nombre no puede estar vacío.
Pulse enter para continuar...
//CASO EDAD
Introduzca una edad acotada entre 1-99 años >>> a
El dato introducido debe ser obligatoriamente numérico de tipo entero.
Pulse enter para continuar...
//CASO CORREO
Introduzca un email válido (Ej: jero@gmail.com / alberto@outlook.es) >>> jero
Un email válido debe tener una parte reservada para el usuario y otra para el dominio.
Pulse enter para continuar...
```

La primera vez que se accede a esta funcionalidad y se completan todos los campos, se crea un archivo data.bin que contiene la estructura de datos ya encriptada y comprimida. 

Si se utiliza en otras ocasiones, la secuencia final consiste en el siguiente algoritmo: 

Si existe: lee → descifra → descomprime → añade → recomprime → cifra → sobrescribe.

<b>Nota:</b> Se puede cancelar la operación en todo momento pulsando <b>CTRL-B.</b>
# Instalación de las librerías

## Instalación de la librería cryptography

En una terminal cmd (Windows) o en la propia terminal de Visual Studio Code ejecutamos el siguiente comando:

```
pip install cryptography
```
## Instalación de la librería colorama

En una terminal cmd (Windows) o en la propia terminal de Visual Studio Code ejecutamos el siguiente comando:

```
pip install colorama
```
