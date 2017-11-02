import unittest
from datetime import date
from carrito import Carrito
from cajero import Cajero
from tarjeta import Tarjeta

LIBRO = 'Libro'
OTRO_LIBRO = 'Otro Libro'
UN_TERCER_LIBRO = 'Un 3er Libro'

CATALOGO_VACIO = {}
CATALOGO_DE_UN_ELEMENTO = { LIBRO: 17 }
CATALOGO_DE_MULTIPLES_ELEMENTOS = { LIBRO: 17, OTRO_LIBRO: 33, UN_TERCER_LIBRO: 42 }

TARJETA = 'tarjeta'

class CajeroTest(unittest.TestCase):
    def test01(self):
        carrito = Carrito(CATALOGO_VACIO)
        cajero = Cajero(catalogo=CATALOGO_VACIO, carrito=carrito, tarjeta=TARJETA)

        try:
            precio = cajero.checkout()
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Cajero.CHECKOUT_CARRITO_VACIO)

    def test02(self):
        carrito = Carrito(CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA)

        carrito.agregar(LIBRO)
        precio = cajero.checkout()

        self.assertEqual(precio, 17)

    def test03(self):
        carrito = Carrito(CATALOGO_DE_MULTIPLES_ELEMENTOS)
        cajero = Cajero(catalogo=CATALOGO_DE_MULTIPLES_ELEMENTOS, carrito=carrito, tarjeta=TARJETA)

        carrito.agregar(LIBRO)
        carrito.agregar(OTRO_LIBRO)
        precio = cajero.checkout()

        self.assertEqual(precio, 17 + 33)

    def test04(self):
        carrito = Carrito(CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA)

        carrito.agregar(LIBRO)
        carrito.agregar(LIBRO)
        precio = cajero.checkout()

        self.assertEqual(precio, 2*17)

    def test05(self):
        carrito = Carrito(catalogo=CATALOGO_DE_MULTIPLES_ELEMENTOS)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA)

        carrito.agregar(LIBRO)
        carrito.agregar(OTRO_LIBRO)

        try:
            precio = cajero.checkout()
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), cajero.PRODUCTO_NO_ESTA_EN_CATALOGO)

    def test06(self):
        tarjeta_expirada = Tarjeta(numero='1' * 16, mes_expiracion=1, anio_expiracion=1990, duenio='Duenio')
        carrito = Carrito(catalogo=CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=tarjeta_expirada, fecha=date(2017, 1, 1))

        carrito.agregar(LIBRO)

        try:
            precio = cajero.checkout()
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Cajero.TARJETA_EXPIRADA)
