class Cajero(object):
    CHECKOUT_CARRITO_VACIO = "No se puede hacer checkout de un carrito vacio!"
    PRODUCTO_NO_ESTA_EN_CATALOGO = 'El producto no esta en el catalogo!'

    def __init__(self, catalogo):
        self._catalogo = catalogo

    def precio(self, producto):
        if producto not in self._catalogo:
            raise Exception(self.PRODUCTO_NO_ESTA_EN_CATALOGO)

        return self._catalogo[producto]

    def checkout(self, carrito, numero_tarjeta, expiracion_tarjeta, duenio_tarjeta):
        if carrito.vacio():
            raise Exception(self.CHECKOUT_CARRITO_VACIO)

        return sum(self.precio(producto) * carrito.unidades(producto) for producto in carrito.productos())
