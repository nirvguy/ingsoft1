from carrito import Carrito
from cajero import Cajero
from tarjeta import Tarjeta
from collections import Counter, defaultdict

class SesionCarrito(object):
    def __init__(self, carrito, usuario):
        self._carrito = carrito
        self._usuario = usuario

    def carrito(self):
        return self._carrito

    def usuario(self):
        return self._usuario

class InterfazRest(object):
    COMBINACION_USUARIO_Y_CLAVE_INVALIDA = 'El usuario o la clave son invalidos!'
    CARRITO_INVALIDO = 'El carrito es invalido!'
    CHECKOUT_CARRITO_VACIO = 'No se puede hacer checkout de un carrito vacio!'
    FECHA_INVALIDA = 'Fecha de vencimiento invalida!'

    def __init__(self, usuarios, catalogo, fecha, mp):
        self._usuarios = usuarios
        self._catalogo = catalogo
        self._libros_de_ventas = defaultdict(list)
        self._sesiones = dict()
        self._last_id = 0
        self._fecha = fecha
        self._mp = mp

    def create_cart(self, usuario, contrasenia):
        if usuario not in self._usuarios or self._usuarios[usuario] != contrasenia:
            raise Exception(self.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)

        carrito = Carrito(self._catalogo)

        self._last_id += 1
        self._sesiones[self._last_id] = SesionCarrito(carrito, usuario)

        return self._last_id

    def add_to_cart(self, id_carrito, producto, cantidad):
        if id_carrito not in self._sesiones:
            raise Exception(self.CARRITO_INVALIDO)

        for _ in range(cantidad):
            self._sesiones[id_carrito].carrito().agregar(producto)

    def list_cart(self, id_carrito):
        if id_carrito not in self._sesiones:
            raise Exception(self.CARRITO_INVALIDO)

        carrito = self._sesiones[id_carrito].carrito()
        return [ (p, carrito.unidades(p)) for p in carrito.productos() ]

    def list_purchases(self, usuario, contrasenia):
        if usuario not in self._usuarios or self._usuarios[usuario] != contrasenia:
            raise Exception(self.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)

        cantidades = Counter()
        for v in self._libros_de_ventas[usuario]:
            for p, c in v.productos():
                cantidades[p] += c
        total = sum(v.total() for v in self._libros_de_ventas[usuario])

        return list(cantidades.items()), total

    def checkout(self, id_carrito, nro_tarjeta, fecha_expiracion, duenio):
        if len(fecha_expiracion) != 6:
            raise Exception(self.FECHA_INVALIDA)
        if id_carrito not in self._sesiones:
            raise Exception(self.CARRITO_INVALIDO)
        if self._sesiones[id_carrito].carrito().vacio():
            raise Exception(self.CHECKOUT_CARRITO_VACIO)

        mes_expiracion = int(fecha_expiracion[0:2])
        anio_expiracion = int(fecha_expiracion[2:6])
        usuario = self._sesiones[id_carrito].usuario()

        carrito = self._sesiones[id_carrito].carrito()
        tarjeta = Tarjeta(nro_tarjeta, mes_expiracion, anio_expiracion, duenio)

        cajero = Cajero(self._catalogo, carrito, tarjeta, self._fecha, self._mp, self._libros_de_ventas[usuario])
        transaction_id = cajero.checkout()

        del self._sesiones[id_carrito]

        return transaction_id
