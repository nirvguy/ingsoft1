class Venta(object):
    VENTA_SIN_PRODUCTOS = 'Venta sin productos!'

    def __init__(self, productos, total):
        if len(productos) == 0:
            raise Exception(self.VENTA_SIN_PRODUCTOS)

        self._productos = productos
        self._total = total

    def __eq__(self, other):
        return self._productos == other._productos and self._total == other._total

    def productos(self):
        return list(self._productos.items())

    def total(self):
        return self._total
