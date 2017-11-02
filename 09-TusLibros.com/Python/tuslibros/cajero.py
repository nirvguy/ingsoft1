class Cajero(object):
    CHECKOUT_CARRITO_VACIO = "No se puede hacer checkout de un carrito vacio!"
    PRODUCTO_NO_ESTA_EN_CATALOGO = 'El producto no esta en el catalogo!'
    TARJETA_EXPIRADA = 'La tarjeta esta expirada!'

    def __init__(self, catalogo, carrito, tarjeta, fecha):
        self._catalogo = catalogo
        self._carrito = carrito
        self._tarjeta = tarjeta
        self._fecha = fecha

    def precio(self, producto):
        if producto not in self._catalogo:
            raise Exception(Cajero.PRODUCTO_NO_ESTA_EN_CATALOGO)
        return self._catalogo[producto]

    def checkout(self):
        if self._carrito.vacio():
            raise Exception(self.CHECKOUT_CARRITO_VACIO)

        if self._tarjeta.expiro(self._fecha):
            raise Exception(self.TARJETA_EXPIRADA)

        return sum(self.precio(producto) * self._carrito.unidades(producto)
                   for producto in self._carrito.productos())
