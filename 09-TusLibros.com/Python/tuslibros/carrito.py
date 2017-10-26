class Carrito(object):
    PRODUCTO_NO_ESTA_EN_CATALOGO = 'El producto no esta en el catalogo!'

    def __init__(self, catalogo):
        self._productos = set()
        self._catalogo = catalogo

    def vacio(self):
        return len(self._productos) == 0

    def contiene(self, producto):
        return producto in self._productos

    def agregar(self, producto):
        if producto not in self._catalogo:
            raise Exception(self.PRODUCTO_NO_ESTA_EN_CATALOGO)
        self._productos.add(producto)


