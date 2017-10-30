from collections import Counter

class Carrito(object):
    PRODUCTO_NO_ESTA_EN_CATALOGO = 'El producto no esta en el catalogo!'

    def __init__(self, catalogo):
        self._productos = Counter()
        self._catalogo = catalogo

    def vacio(self):
        return len(self._productos) == 0

    def __contains__(self, producto):
        return producto in self._productos

    def agregar(self, producto):
        if producto not in self._catalogo:
            raise Exception(self.PRODUCTO_NO_ESTA_EN_CATALOGO)
        self._productos[producto] += 1

    def unidades(self, producto):
        if producto not in self._catalogo:
            raise Exception(self.PRODUCTO_NO_ESTA_EN_CATALOGO)
        return self._productos[producto]

    def productos(self):
        return list(self._productos.keys())
