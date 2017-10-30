import unittest
from carrito import Carrito
from cajero import Cajero

LIBRO = 'Libro'
OTRO_LIBRO = 'Otro Libro'
UN_TERCER_LIBRO = 'Un 3er Libro'

CATALOGO_VACIO = {}
CATALOGO_DE_UN_ELEMENTO = { LIBRO: 17 }
CATALOGO_DE_MULTIPLES_ELEMENTOS = { LIBRO: 17, OTRO_LIBRO: 33, UN_TERCER_LIBRO: 42 }

class CajeroTest(unittest.TestCase):
    def test01(self):
        carrito = Carrito(CATALOGO_VACIO)
        cajero = Cajero(CATALOGO_VACIO)

        try:
            precio = cajero.checkout(carrito=carrito,
                                     numero_tarjeta=0,
                                     expiracion_tarjeta=(1, 2),
                                     duenio_tarjeta='alguien')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Cajero.CHECKOUT_CARRITO_VACIO)

    def test02(self):
        carrito = Carrito(CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(CATALOGO_DE_UN_ELEMENTO)

        carrito.agregar(LIBRO)
        precio = cajero.checkout(carrito=carrito,
                                 numero_tarjeta=0,
                                 expiracion_tarjeta=(1, 2),
                                 duenio_tarjeta='alguien')

        self.assertEqual(precio, 17)

    def test03(self):
        carrito = Carrito(CATALOGO_DE_MULTIPLES_ELEMENTOS)
        cajero = Cajero(CATALOGO_DE_MULTIPLES_ELEMENTOS)

        carrito.agregar(LIBRO)
        carrito.agregar(OTRO_LIBRO)
        precio = cajero.checkout(carrito=carrito,
                                 numero_tarjeta=0,
                                 expiracion_tarjeta=(1, 2),
                                 duenio_tarjeta='alguien')

        self.assertEqual(precio, 17 + 33)

    def test04(self):
        carrito = Carrito(CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(CATALOGO_DE_UN_ELEMENTO)

        carrito.agregar(LIBRO)
        carrito.agregar(LIBRO)
        precio = cajero.checkout(carrito=carrito,
                                 numero_tarjeta=0,
                                 expiracion_tarjeta=(1, 2),
                                 duenio_tarjeta='alguien')

        self.assertEqual(precio, 2*17)
