from carrito import Carrito
from cajero import Cajero
from tarjeta import Tarjeta
from collections import Counter, defaultdict

class SesionCarrito(object):
    def __init__(self, carrito, usuario, acceso):
        self._carrito = carrito
        self._usuario = usuario
        self._ultimo_acceso = acceso

    def carrito(self):
        return self._carrito

    def usuario(self):
        return self._usuario

    def ultimo_acceso(self):
        return self._ultimo_acceso

    def actualizar_ultimo_acceso(self, acceso):
        self._ultimo_acceso = acceso

    def expiro(self, acceso):
        return (acceso - self._ultimo_acceso).total_seconds() / 60 > 30

class InterfazRest(object):
    CARRITO_INVALIDO = 'El carrito es invalido!'
    CHECKOUT_CARRITO_VACIO = 'No se puede hacer checkout de un carrito vacio!'
    FECHA_INVALIDA = 'Fecha de vencimiento invalida!'
    TIMEOUT_CARRITO = 'El carrito expiro!'
    UNIDADES_DEBEN_SER_POSITIVAS = 'Las unidades a agregar a un carrito deben ser positivas!'

    def __init__(self, autenticador, catalogo, reloj, mp):
        self._autenticador = autenticador
        self._catalogo = catalogo
        self._libros_de_ventas = defaultdict(list)
        self._sesiones = dict()
        self._last_id = 0
        self._reloj = reloj
        self._mp = mp

    def create_cart(self, usuario, contrasenia):
        self._autenticador.login(usuario, contrasenia)

        carrito = Carrito(self._catalogo)

        self._last_id += 1
        self._sesiones[self._last_id] = SesionCarrito(carrito, usuario, self._reloj.today())

        return self._last_id

    def add_to_cart(self, id_carrito, producto, cantidad):
        if id_carrito not in self._sesiones:
            raise Exception(self.CARRITO_INVALIDO)
        if cantidad <= 0:
            raise Exception(self.UNIDADES_DEBEN_SER_POSITIVAS)
        if self._sesiones[id_carrito].expiro(self._reloj.today()):
            raise Exception(self.TIMEOUT_CARRITO)

        for _ in range(cantidad):
            self._sesiones[id_carrito].carrito().agregar(producto)
        self._sesiones[id_carrito].actualizar_ultimo_acceso(self._reloj.today())

    def list_cart(self, id_carrito):
        if id_carrito not in self._sesiones:
            raise Exception(self.CARRITO_INVALIDO)
        if self._sesiones[id_carrito].expiro(self._reloj.today()):
            raise Exception(self.TIMEOUT_CARRITO)

        carrito = self._sesiones[id_carrito].carrito()
        self._sesiones[id_carrito].actualizar_ultimo_acceso(self._reloj.today())
        return [ (p, carrito.unidades(p)) for p in carrito.productos() ]

    def list_purchases(self, usuario, contrasenia):
        self._autenticador.login(usuario, contrasenia)

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
        if self._sesiones[id_carrito].expiro(self._reloj.today()):
            raise Exception(self.TIMEOUT_CARRITO)

        mes_expiracion = int(fecha_expiracion[0:2])
        anio_expiracion = int(fecha_expiracion[2:6])
        usuario = self._sesiones[id_carrito].usuario()

        carrito = self._sesiones[id_carrito].carrito()
        tarjeta = Tarjeta(nro_tarjeta, mes_expiracion, anio_expiracion, duenio)

        cajero = Cajero(self._catalogo, carrito, tarjeta, self._reloj.today(), self._mp, self._libros_de_ventas[usuario])
        transaction_id = cajero.checkout()

        del self._sesiones[id_carrito]

        return transaction_id
