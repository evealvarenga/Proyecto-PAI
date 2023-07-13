from clases import *

def crearDomi():
    print("Ingrese los datos del domicilio.")
    calle = input("Ingrese la calle y altura: ")
    depto = input("Ingrese el n° de departamento: ")
    ciudad = input("Ingrese la ciudad: ") 
    provincia = input ("Ingrese la provincia: ")
    cp = input ("Ingrese el código postal: ")
    nuevoDomi = Domicilio(calle, ciudad, provincia, cp, depto)
    return nuevoDomi.mostrarDomi()
        
def crearUsuario():
    dni = input("Ingrese DNI: ")
    try: 
        if validador(dni,"data/usuarios.json", "DNI"):
            print("El DNI ingresado ya existe en nuestra base de datos.")
            return False
        else:
            usuario = input("Nombre de usuario: ")
            contrasena = input("Contraseña: ")
            nombre = input ("Ingrese nombre completo:")
            domicilio = crearDomi()
            usuario = Vendedor(usuario, contrasena, dni, nombre, domicilio)
            print("Usuario creado con exito.")
            return True
    except FileNotFoundError:
        usuario = input("Nombre de usuario: ")
        contrasena = input("Contraseña: ")
        nombre = input ("Ingrese nombre completo:")
        domicilio = crearDomi()
        usuario = Vendedor(usuario, contrasena, dni, nombre, domicilio)
        print("Usuario creado con exito.")
        return True

def crearCliente():
    dni = input("Número de DNI: ") 
    try:
        if validador(dni, "data/clientes.json", "DNI"):
            print("El DNI ingresado ya existe en nuestra base de datos.")
        else:
            ID = (obtenerID("data/clientes.json"))
            nombre = input("Ingrese nombre completo: ")  
            telefono = input ("Ingrese número de teléfono: ")
            domicilio = crearDomi()
            cliente = Cliente(ID, dni, nombre, domicilio, telefono)
            print("Cliente creado con exito.")
    except FileNotFoundError: 
        ID = (obtenerID("data/clientes.json"))
        nombre = input("Ingrese nombre completo: ")  
        telefono = input ("Ingrese número de teléfono: ")
        domicilio = crearDomi()
        cliente = Cliente(ID, dni, nombre, domicilio, telefono)
        print("Cliente creado con exito.")

def crearProveedor():
    cuit = int(input("Ingrese CUIT: "))
    try:
        if validador(int(cuit), "data/proveedores.json", "CUIT"):
            print("El CUIT ingresado ya existe en nuestra base de datos.")
        else: 
            nombre = input("Ingrese razón social: ")
            provedor = Proveedor(int(cuit), nombre)
            print("Proveedor creado con exito.")
            return cuit
    except FileNotFoundError:
        nombre = input("Ingrese razón social: ")
        provedor = Proveedor(int(cuit), nombre)
        print("Proveedor creado con exito.")
        return cuit

def crearProducto(proveedor):
    ID = (obtenerID("data/productos.json"))
    nombre = input("Ingrese nombre del producto: ")
    descripcion = input("Ingrese una breve descripción: ")
    precio = input("Ingrese precio del producto: $")
    cantidad = input("Ingrese el stock actual del producto: ")
    producto = Producto(ID, nombre, descripcion, precio, proveedor, cantidad)
    print("Producto creado con exito.")

def obtenerID(archivo):
    try:
        with open(archivo, 'r') as dato:
            datos = json.load(dato)
            return len(datos) + 1
    except (FileNotFoundError, json.JSONDecodeError):
        return 1

def obtenerDatos(archivo):
    dato = []
    try:
        with open(archivo, 'r') as archivo_json:
            datos = json.load(archivo_json)         
        for base in datos:
            dato.append(base)
        archivo_json.close()
        return dato
    except (FileNotFoundError, TypeError):
        return False

def obtenerDatoIndividual(id_producto, dato):
    with open("data/productos.json", 'r') as archivo:
        datos = json.load(archivo)
    for producto in datos:
        if producto["ID"] == id_producto:
            if dato in producto:
                return producto[dato]
            else:
                return None

def validador(dato, archivo, buscador):
    with open(archivo) as file:
        datos = json.load(file)
        if datos:
            lista = [str(d[buscador]) for d in datos]
            if str(dato) in lista:
                return True
    return False

def validadorStock(id_producto, cantidad):
    with open("data/productos.json", 'r') as archivo:
        datos = json.load(archivo)
    for producto in datos:
        if producto["ID"] == id_producto:
            if producto["Cantidad"] >= int(cantidad):
                return True
            else:
                return False
    return False

def restar_stock(id_producto, cantidad_restar):
    with open("data/productos.json", 'r') as archivo:
        datos = json.load(archivo)

    for producto in datos:
        if producto["ID"] == id_producto:
            producto["Cantidad"] -= cantidad_restar
    archivo.close()
    with open("data/productos.json", 'w') as archivo:
        json.dump(datos, archivo, indent=4)
    archivo.close()

def agregar_stock(id_producto, cantidad_restar):
    with open("data/productos.json", 'r') as archivo:
        datos = json.load(archivo)
    for producto in datos:
        if producto["ID"] == id_producto:
            producto["Cantidad"] += cantidad_restar
    archivo.close()
    with open("data/productos.json", 'w') as archivo:
        json.dump(datos, archivo, indent=4)
    archivo.close()

def opcionesMetodo():
    try:
        opcion = int(input("\n1. Efectivo\n2. Tarjeta de crédito \n3. Tarjeta de débito\n4. Depósito\n5. Transferencia \n\nIngrese la opción seleccionada:"))
        if opcion == 1:
            tipo = "Efectivo"
            return tipo
        elif opcion == 2:
            tipo = "Tarjeta de crédito"
            return tipo
        elif opcion == 3:
            tipo = "Tarjeta de débito"
            return tipo
        elif opcion == 4:
            tipo = "Depósito"
            return tipo
        elif opcion == 5:
            tipo = "Transferencia"
            return tipo
        while opcion not in (1, 2, 3, 4, 5):
            print("El valor ingresado no corresponde a uno indicado en la lista.")
            opcionesMetodo()
    except ValueError:
        print("Error en el valor agregado.")
        opcionesMetodo()

def metodoPago(total):
    print("Metodos de pago disponibles: ")
    opcion1 = opcionesMetodo()
    valor1 = float(input("Ingresa el valor a pagar por este medio: $"))
    if valor1 > total:
        print("El valor ingresado supera el monto total de la compra.")
    elif valor1 == total:
        eleccion = input("El valor ingresado es igual al monto total de la compra.\n¿Desea realizar la compra por un solo medio de pago? Si/No: ").upper()
        if eleccion == "SI":
            datos = [{"Metodo 1" : opcion1, "Importe": valor1}]
            return datos
        else:
            metodoPago(total)
    elif valor1 < total:
        valor2 = total - valor1
        print("Valor restante a abonar: $" + str(valor2))
        print("Metodos de pago disponibles para el valor restante: ")
        opcion2 = opcionesMetodo()
        datos = [{"Metodo 1" : opcion1, "Importe": valor1}, 
                {"Metodo 2": opcion2,"Importe": valor2}]
        return datos
