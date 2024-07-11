import datetime
from pymongo.mongo_client import MongoClient
from bson import ObjectId

#uri = os.getenv("uri")
uri = "mongodb+srv://usuario:usuario@proyectomongodb.fpedozi.mongodb.net/?retryWrites=true&w=majority&appName=ProyectoMongoDB"

cliente = MongoClient(uri)
db = cliente.LaComedia
ventas = db.Ventas
productos = db.Productos
pedidos = db.Pedidos

def probarconexion():
    try:
        cliente.admin.command('ping')
        print("\nConexión exitosa a la base de datos.\nPuede comenzar a usar el programa.")
    except Exception as e:
        print(e)

def cerrarcliente():
    cliente.close()

def find(coleccion,documento,filtro,orden):
    try:
        cursor = coleccion.find(documento,filtro)
        if orden != 0:
            cursor = coleccion.find(documento,filtro).sort(orden)
        else:
            cursor = coleccion.find(documento,filtro)
    except Exception as e:
        print("Error en la consulta.\n" + str(e))
    return cursor

def buscar_id(nombre):
    coleccion = productos
    documento = ({"Nombre":nombre})
    filtro = {"_id":1}
    cursor = find(coleccion,documento,filtro,0)
    for documento in cursor:
        id=documento["_id"]
    return id

def listarproductos():
    coleccion = productos
    documento = ({})
    filtro = {"Nombre": 1, "_id": 1}
    orden = {"Categoria": 1}
    cursor = find(coleccion,documento,filtro,orden)
    listaproductos = []
    for documento in cursor:
        listaproductos.append(documento)
    return listaproductos
        
def producto(nombre, cantidad):
    id = buscar_id(nombre)
    productos["_id"]=id
    productos["Nombre"]=nombre
    productos["Cantidad"]=cantidad
    return productos
    
def actualizar_stock(venta):
    try:
        for producto in venta:
            nombre = producto["Nombre"]
            cantidad = producto["Cantidad"]
            documento = {"Nombre": nombre}
            actualizar = {"$inc": {"Stock": cantidad}}
            productos.update_one(documento, actualizar)
        return 0
    except:
        return 1

def nueva_venta(productos):
    try:
        fecha=datetime.datetime.now()
        documento = {
            "Fecha": fecha,
            "Productos": productos
        }
        ventas.insert_one(documento)
        stock = actualizar_stock(productos)
        if stock == 0:
            return 0
        else:
            return 1
    except:
        return 1
    
def nuevo_pedido(productos):
    try:
        fecha=datetime.datetime.now()
        documento = {
            "Fecha": fecha,
            "Productos": productos,
            "Recibido": False
        }
        pedidos.insert_one(documento)
        return 0
    except:
        return 1
    
def actualizar_stock(venta):
    try:
        for producto in venta:
            nombre = producto["Nombre"]
            cantidad = producto["Cantidad"]
            documento = {"Nombre": nombre}
            actualizar = {"$inc": {"Stock": cantidad}}
            productos.update_one(documento, actualizar)
        return 0
    except:
        return 1

def ver_pedidos():
    try:
        coleccion = pedidos
        documento = ({"Recibido":False})
        filtro = {}
        cursor = find(coleccion,documento,filtro,0)
        listapedidos = []
        for documento in cursor:
            listapedidos.append(documento)
        return listapedidos
    except:
        return 1

def ultimo_pedido():
    try:
        cursor = pedidos.find()
        fecha_previa = datetime.datetime(2020,1,1)
        for documento in cursor:
            fecha = documento["Fecha"]
            if fecha > fecha_previa:
                guardado = documento
        return guardado
    except Exception as e:
        print("Error al buscar el último pedido.",e)

def ventas_desde_ultimo_pedido():
    try:
        cursor = ventas.find()
        ultimopedido = ultimo_pedido()
        fecha_ultimo_pedido = ultimopedido["Fecha"]
        documentos = []
        for documento in cursor:
            if documento["Fecha"] >= fecha_ultimo_pedido:
                documentos.append(documento)
        print(documentos)
    except:
        print("Error al buscar las ventas desde el último pedido.")

def pedido_recibido(id):
    try:
        _id = ObjectId(str(id))
        documento = {"_id": _id}
        actualizar = {"$set": {"Recibido": True}}
        pedidos.update_one(documento, actualizar)
        return 0
    except:
        return 1

def insertar_producto(nombre,precio,stock,umbral_pedido,categoria):
    try:
        documento = {
            "Nombre": nombre,
            "Precio": precio,
            "Stock": stock,
            "Umbral_Pedido": umbral_pedido,
            "Categoria": categoria,
        }
        productos.insert_one(documento)
        return 0
    except:
        return 1
    
def actualizar_producto(nombre,precio,stock,umbral_pedido,categoria):
    try:
        id = buscar_id(nombre)
        documento = {"_id": id}
        actualizar = {"$set": {"Precio": float(precio),"Stock": int(stock), "Umbral_Pedido": int(umbral_pedido), "Categoria": categoria}}
        productos.update_one(documento, actualizar)
        return 0
    except:
        return 1
    
def eliminar_producto (id):
    try:
        _id = ObjectId(str(id))
        documento = {"_id": _id}
        productos.delete_one(documento)
        return 0
    except:
        return 1