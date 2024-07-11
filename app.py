import funciones, os, requests
from flask import Flask, render_template, abort, redirect, request, session

app = Flask(__name__)
port = os.getenv("PORT")
user = os.getenv("usuario")
passwd = os.getenv("passwd")
app.secret_key = os.getenv("secret_key")

def crearventa():
    productos = funciones.listarproductos()
    venta = []
    for producto in productos:
        elemento = {}
        cantidad = int(request.form.get(producto["Nombre"]))
        if cantidad > 0:
            elemento["Nombre"] = producto["Nombre"]
            elemento["_id"] = producto["_id"]
            elemento["Cantidad"] = cantidad
            venta.append(elemento)
    return venta

@app.route('/', methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("inicio.html")
    else:
        usuario = request.form.get("usuario")
        contraseña = request.form.get("passwd")
        if usuario == user and contraseña == passwd:
            session["usuario"] = usuario
            return redirect("/inicio")
        else:
            return render_template("error_login.html")
        
@app.route('/inicio')
def inicio():
    return render_template("menu.html")

@app.route('/nuevaventa', methods=["GET","POST"])
def nuevaventa():
    if request.method == "GET":
        productos = funciones.listarproductos()
        return render_template("nuevaventa.html",productos=productos)
    else:
        global venta
        venta=crearventa()
        return render_template("nuevaventa.html",venta=venta)
    
@app.route("/venta")
def confirmarventa():
    resultado = funciones.nueva_venta(venta)
    if resultado == 0:
        return render_template("ventaexito.html",venta=venta)
    elif resultado == 1:
        return render_template("errorventa.html",venta=venta)
    else:
        redirect(abort)

@app.route("/nuevopedido", methods=["GET","POST"])
def nuevopedido():
    if request.method == "GET":
        productos = funciones.listarproductos()
        return render_template("nuevopedido.html",productos=productos)
    else:
        global pedido
        pedido=crearventa()
        return render_template("nuevopedido.html",pedido=pedido)
    
@app.route("/pedido")
def confirmarpedido():
    resultado = funciones.nuevo_pedido(pedido)
    if resultado == 0:
        return render_template("pedidoexito.html",pedido=pedido)
    elif resultado == 1:
        return render_template("errorpedido.html",pedido=pedido)
    else:
        redirect(abort)

@app.route("/pedidos", methods=["GET","POST"])
def listarpedidos():
    if request.method == "GET":
        pedidos = funciones.ver_pedidos()
        return render_template("pedidos.html",pedidos=pedidos)
    else:
        id = request.form.get("_id")
        resultado = funciones.pedido_recibido(id)
        return render_template ("pedidos.html", resultado=resultado)
    
@app.route("/productos")
def productos():
    return render_template("productos.html")

@app.route("/nuevoproducto", methods=["GET","POST"])
def nuevoproducto():
    if request.method == "GET":
        return render_template("nuevoproducto.html")
    else:
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        stock = request.form.get("stock")
        umbral_pedido = request.form.get("umbral")
        categoria = request.form.get("categoria")
        resultado = funciones.insertar_producto(nombre,precio,stock,umbral_pedido,categoria)
        if resultado == 0:
            return redirect("/productos")
        elif resultado == 1:
            return abort

@app.route("/actualizarproducto", methods=["GET","POST"])
def actualizarproducto():
    if request.method == "GET":
        return render_template("actualizarproducto.html")
    else:
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        stock = request.form.get("stock")
        umbral_pedido = request.form.get("umbral")
        categoria = request.form.get("categoria")
        resultado = funciones.actualizar_producto(nombre,precio,stock,umbral_pedido,categoria)
        if resultado == 0:
            return redirect("/productos")
        elif resultado == 1:
            return abort

@app.route("/eliminarproducto", methods=["GET","POST"])
def eliminarproducto():
    if request.method == "GET":
        productos = funciones.listarproductos()
        return render_template("eliminarproducto.html",productos=productos)
    else:
        _id = request.form.get("producto")
        print(_id)
        resultado = funciones.eliminar_producto(_id)
        if resultado == 0:
            return redirect("/productos")
        elif resultado == 1:
            return abort

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/")

@app.before_request
def antes_de_cada_peticion():
    ruta = request.path
    # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
    if not 'usuario' in session and ruta != "/" and ruta != "/logout" and not ruta.startswith("/static"):
        return redirect("/")
    # Si ya ha iniciado, no hacemos nada, es decir lo dejamos pasar

app.run("0.0.0.0",port,debug=False)