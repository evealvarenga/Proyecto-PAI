import json
from clases import *
from funciones import *

class Interfaz:
    def __init__(self):
        self.datos_usuarios = None
        self.usuario = None

    def cargar_datos_usuarios(self):
        datos = {}
        try:
            with open("data/usuarios.json", 'r') as archivo:
                datoviejo = json.load(archivo)
            
            for usuario in datoviejo:
                datos[usuario["User"]] = usuario["Password"]
                
            archivo.close()
            self.datos_usuarios = datos
        except FileNotFoundError:
            return {}

    def registrar_usuario(self):
        if crearUsuario():
            self.menuPrincipal()
        else:
            self.iniciar_sesion()

    def iniciar_sesion(self, usuario, contrasena):
        if usuario in self.datos_usuarios and self.datos_usuarios[usuario] == contrasena:
            print("\nInicio de sesión exitoso.\n")
            self.usuario = usuario
            self.menuPrincipal()
        else:
            print("\nNombre de usuario o contraseña incorrectos.\n")
            
    def menuPrincipal(self):
        opcion = input("1. Clientes\n2. Proveedores\n3. Productos\n4. Registrar una venta\n\nSeleccione una opción: ")
        if opcion == "1":
            interfaz.seccionClientes()
        elif opcion == "2":
            interfaz.seccionProveedores()
        elif opcion == "3":
            interfaz.seccionProductos()
        elif opcion == "4":
            interfaz.seccionVenta()
        else:
            print("Opción inválida.\n\n")
            self.menuPrincipal()
    
    def seccionClientes(self):
        opcion = input("1. Crear nuevo cliente\n2. Volver al menú principal\n\nSeleccione una opción: ")
        if opcion == "1":
            crearCliente()
            self.retorno("cliente")
        elif opcion == "2":
            interfaz.menuPrincipal()
        else:
            print("Opción inválida.")

    def seccionProductos(self):
        opcion = input("1. Ingresar un nuevo producto\n2. Detalle de productos\n3. Agregar stock \n4. Volver al menú principal\n\nSeleccione una opción: ")
        if opcion == "1":
            cuit = int(input("Ingrese CUIT del proveedor del producto a ingresar: "))
            try:
                if validador(int(cuit), "data/proveedores.json", "CUIT"):
                    crearProducto(cuit)
                else:
                    crearProducto(crearProveedor())
            except FileNotFoundError:
                crearProducto(crearProveedor())
            except ValueError:
                print("Error en alguno de los valores ingresados. \nFavor de volver a realizar la carga")

            self.retorno("productos")
        elif opcion == "2":
            productos = obtenerDatos("data/productos.json")
            if productos:
                print("__________________________\n\nLista de productos.")
                id = 1
                for producto in productos:
                    nombre = obtenerDatoIndividual(id, "Nombre")
                    print(str(id) +". "+ nombre)
                    id +=1
                print("__________________________\n")
                try: 
                    pOpcion = int(input("Si desea ver el detalle de algún producto en particular ingrese el ID de dicho producto.\nSi desea regresar a alguno de los menús anteriores, ingrese 0\n\nIngrese opción seleccionada: "))
                    if validador(pOpcion,"data/productos.json", "ID"):
                        nombre = obtenerDatoIndividual(pOpcion, "Nombre")
                        descripcion = obtenerDatoIndividual(pOpcion, "Descripcion")
                        precio = obtenerDatoIndividual(pOpcion, "Precio")
                        cantidad = obtenerDatoIndividual(pOpcion, "Cantidad")
                        print("__________________________\n" + nombre + "\nPrecio: $" + str(precio) + "\nCantidad en stock: " + str(cantidad) + "\n"+ descripcion + "\n__________________________\n")                      
                    elif pOpcion == 0:
                        self.retorno("productos")
                    else: 
                        print("Has ingresado un ID inexistente.")
                except ValueError:
                    print("Error en el valor ingresado.")
            else:
                print("No hay datos registrados.\n\n")
                self.seccionProductos()
            self.retorno("productos")
        elif opcion == "3":
            try:
                id = int(input("Ingrese ID del producto: "))
                if validador(id, "data/productos.json", "ID"):
                    cantidad = int(input("Ingrese cantidad de stock a agregar: "))
                    agregar_stock(id, cantidad)
                else:
                    print("Producto no encontrado.")
            except:
                print("Error en el valor ingresado.")
        elif opcion == "4":
            interfaz.menuPrincipal()
        else:
            print("Opción inválida.")

    def seccionProveedores(self):
        opcion = input("1. Crear nuevo proveedor\n2. Visualizar proveedores\n3. Volver al menú principal\n\nSeleccione una opción: ")
        if opcion == "1":
            crearProveedor()
            self.retorno("proveedores")
        elif opcion == "2":
            proveedores = obtenerDatos("data/proveedores.json")
            if proveedores:
                for proveedor in proveedores:
                    print(proveedor)
            else:
                print("No hay datos registrados.\n\n")
                self.seccionProveedores()
            self.retorno("proveedores")
        elif opcion == "3":
            interfaz.menuPrincipal()
        else:
            print("Opción inválida.")
        
    def seccionVenta(self):
        dni = input("Ingrese DNI del cliente: ")
        if validador(dni,"data/clientes.json", "DNI"):
            ID = (obtenerID("data/ventas.json"))
            venta = Venta(ID, self.usuario, dni)
        else:
            crearCliente()

        self.retorno("venta")
    
    def retorno(self, place):
        opcion = int(input("\n1. Regresar al menú anterior\n2. Regresar al menú princiapl\n3. Cerrar sesión\n\nSeleccione una opción: "))
        if opcion == 1:
            if place == "cliente":
                self.seccionClientes()
            elif place == "proveedores":
                self.seccionProveedores()
            elif place == "productos":
                self.seccionProductos()
            elif place == "venta":
                self.seccionVenta()
        elif opcion == 2:
            self.menuPrincipal()
        elif opcion == 3:
            print ("Sesión cerrada con éxito.")


# Inicialización
interfaz = Interfaz()
interfaz.cargar_datos_usuarios()

opcion = input("1. Registrarse\n2. Iniciar sesión\nSeleccione una opción: ")

if opcion == "1":
    interfaz.registrar_usuario()
elif opcion == "2":
    usuario = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")
    interfaz.iniciar_sesion(usuario, contraseña)
else:
    print("Opción inválida.")