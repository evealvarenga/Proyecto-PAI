import json

class Domicilio():
    def __init__(self, calle, ciudad, provincia, cp, depto):
        self.calle = calle
        self.ciudad = ciudad
        self.provincia = provincia
        self.cp = cp
        self.depto = depto
    
    def mostrarDomi(self):
        domicilio = { "Calle" : self.calle, 
                     "Depto" : self.depto, 
                     "Ciudad" : self.ciudad, 
                     "Provincia": self.provincia, 
                     "Codigo Postal": self.cp
                     }
        return(domicilio)

class Persona():
    def __init__(self, dni, nombre, domicilio):
        self.dni = dni
        self.nombre = nombre
        self.domiLegal = domicilio

class Cliente(Persona):
    def __init__(self,id, dni, nombre, domicilio, telefono):
        Persona.__init__(self, dni,nombre, domicilio)
        self.id = id
        self.telefono = telefono
        self.guardarCliente()
    
    def guardarCliente(self):
        base = []
        try:
            with open("data/clientes.json", 'r') as archivo:
                datoviejo = json.load(archivo)
            for cliente in datoviejo:
                base.append(cliente)
            archivo.close()
            datos = {
            "ID" : self.id,
            "DNI" : self.dni,
            "Nombre" : self.nombre,
            "Telefono" : self.telefono,
            "Domicilio Legal" : self.domiLegal,
            }
            base.append(datos)
            with open("data/clientes.json","w") as archivo:
                json.dump(base, archivo)
            archivo.close()
        except FileNotFoundError:
            datos = {
            "ID" : self.id,
            "DNI" : self.dni,
            "Nombre" : self.nombre,
            "Telefono" : self.telefono,
            "Domicilio Legal" : self.domiLegal,
            }
            base.append(datos)
            with open("data/clientes.json","a") as archivo:
                json.dump(base, archivo)
            archivo.close()         

class Vendedor(Persona):
    def __init__(self, usuario, contrasena, dni, nombre, domicilio):
        Persona.__init__(self, dni,nombre, domicilio)
        self.usuario = usuario
        self.contrasena = contrasena
        self.guardarVendedor()
    
    def guardarVendedor(self):
        base = []
        try:
            with open("data/usuarios.json", 'r') as archivo:
                datoviejo = json.load(archivo)
            for usuario in datoviejo:
                base.append(usuario)
            archivo.close()
            datos = {
            "User" : self.usuario,
            "Password" : self.contrasena,
            "DNI" : self.dni,
            "Nombre" : self.nombre,
            "Domicilio" : self.domiLegal
            }
            base.append(datos)
            with open("data/usuarios.json","w") as archivo:
                json.dump(base, archivo)
            archivo.close()
        except FileNotFoundError:
            datos = {
            "User" : self.usuario,
            "Password" : self.contrasena,
            "DNI" : self.dni,
            "Nombre" : self.nombre,
            "Domicilio" : self.domiLegal
            }
            base.append(datos)
            with open("data/usuarios.json","a") as archivo:
                json.dump(base, archivo)
            archivo.close()    

class Proveedor():
    def __init__(self, CUIL, razonsocial):
        self.CUIL = CUIL
        self.razonsocial = razonsocial
        self.guardarProveedor()
        
    def guardarProveedor(self):
        base = []
        try:
            with open("data/proveedores.json", 'r') as archivo:
                datoviejo = json.load(archivo)
            for proveedores in datoviejo:
                base.append(proveedores)
            archivo.close()
            datos = {
            "CUIT" : int(self.CUIL),
            "Razon social" : self.razonsocial,
            }
            base.append(datos)
            with open("data/proveedores.json","w") as archivo:
                json.dump(base, archivo)
            archivo.close()
        except FileNotFoundError:
            datos = {
            "CUIL" : self.CUIL,
            "Razon social" : self.razonsocial,
            }
            base.append(datos)
            with open("data/proveedores.json","a") as archivo:
                json.dump(base, archivo)
            archivo.close()

class Producto():
    def __init__(self, id, nombre, descripcion, precio, proveedor, cantidad):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = float(precio)
        self.proveedor = proveedor
        self.cantidad = int(cantidad)
        self.guardarProducto()
    
    def guardarProducto(self):
        base = []
        try:
            with open("data/productos.json", 'r') as archivo:
                datoviejo = json.load(archivo)
            for producto in datoviejo:
                base.append(producto)
            archivo.close()
            datos = {
            "ID" : self.id,
            "Nombre" : self.nombre,
            "Descripcion" : self.descripcion,
            "Precio" : self.precio,
            "Proveedor" : self.proveedor,
            "Cantidad" : self.cantidad
            }
            base.append(datos)
            with open("data/productos.json","w") as archivo:
                json.dump(base, archivo)
            archivo.close()
        except FileNotFoundError:
            datos = {
            "ID" : self.id,
            "Nombre" : self.nombre,
            "Descripcion" : self.descripcion,
            "Precio" : self.precio,
            "Proveedor" : self.proveedor,
            "Cantidad" : self.cantidad
            }
            base.append(datos)
            with open("data/productos.json","a") as archivo:
                json.dump(base, archivo)
            archivo.close()

###
from funciones import metodoPago
from funciones import validador
from funciones import validadorStock
from funciones import restar_stock
from funciones import obtenerDatoIndividual

class Venta():
    def __init__(self,ID, vendedor, cliente):
        self.ID = ID
        self.vendedor = vendedor
        self.cliente = cliente
        self.listaProducto = []
        self.total = 0
        self.pagoRealizado = []
        self.realizarVenta()

    def realizarVenta(self):
        self.agregarProducto()
        print(self.listaProducto)
        try:
            if len(self.listaProducto) >= 1:
                self.calcularTotal()
                print("__________________________\n\nSubtotal: $" + str(self.total) + "\n__________________________")
                self.pago()
                self.guardarVenta()

                print("\nVenta generada con éxito.\n")
            else:
                print("El carrito está vacío.\n")
        except AttributeError:
            print("Hubo un error al generar el carrito.")

    def pago(self):
        self.pagoRealizado = metodoPago(self.total)
        
    def agregarProducto(self):
        opcion = "SI"
        while opcion == "SI":
            producto = input("Seleccione el ID del producto: ")
            if validador(producto,"data/productos.json","ID"):
                cantidad = input("Seleccione la cantidad: ")
                if validadorStock(int(producto), int(cantidad)):
                    precio = obtenerDatoIndividual(int(producto), "Precio")
                    precio2 = float(precio) * int(cantidad)
                    produ = {"ID Producto" : int(producto),
                            "Cantidad" : int(cantidad),
                            "Precio Unitario": precio,
                            "Precio Total" : precio2,
                    }
                    self.listaProducto.append(produ)
                    restar_stock(int(producto), int(cantidad))
                else:
                    print("Cantidad no disponible.")
            opcion = (input("¿Desea agregar otro producto más al carrito? Si / No : ")).upper()
            while opcion != "SI" and opcion != "NO":
                print("No hemos comprendido la opción ingresada.")
                opcion = (input("¿Desea agregar algún otro producto más al carrito? Si / No : ")).upper()
    
    def calcularTotal(self):
        precio = float(0)
        for producto in self.listaProducto:
            if producto in self.listaProducto:
                precio = producto["Precio Total"]
                self.total += float(precio)
    
    def guardarVenta(self):
        base = []
        try:
            with open("data/ventas.json", 'r') as archivo:
                datoviejo = json.load(archivo)
            for producto in datoviejo:
                base.append(producto)
            archivo.close()
            datos = {
            "ID": self.ID,
            "Vendedor" : self.vendedor,
            "Cliente" : self.cliente,
            "Productos" : self.listaProducto,
            "Importe total" : self.total,
            "Tipo de pago" : self.pagoRealizado
            }
            base.append(datos)
            with open("data/ventas.json","w") as archivo:
                json.dump(base, archivo)
            archivo.close()
        except FileNotFoundError:
            datos = {
            "ID": self.ID,
            "Vendedor" : self.vendedor,
            "Cliente" : self.cliente,
            "Productos" : self.listaProducto,
            "Importe total" : self.total,
            "Tipo de pago" : self.pagoRealizado
            }
            base.append(datos)
            with open("data/ventas.json","a") as archivo:
                json.dump(base, archivo)
            archivo.close()

    
    
