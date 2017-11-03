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

TARJETA = Tarjeta(numero='0123456789012345', mes_expiracion=1, anio_expiracion=2020, duenio='Duenio')

FECHA = date(2017, 1, 1)

class SimuladorMerchantProcessor(object):
    def debit(self, tarjeta, monto):
        pass

class MPRegistrador(SimuladorMerchantProcessor):
    def __init__(self):
        self._monto = None
        self._tarjeta = None

    def debit(self, tarjeta, monto):
        self._monto = monto
        self._tarjeta = tarjeta

    def monto(self):
        return self._monto

    def tarjeta(self):
        return self._tarjeta

class CajeroTest(unittest.TestCase):
    def setUp(self):
        self.MP_REGISTRADOR = MPRegistrador()

    def test01(self):
        carrito = Carrito(CATALOGO_VACIO)
        cajero = Cajero(catalogo=CATALOGO_VACIO, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=self.MP_REGISTRADOR)

        try:
            precio = cajero.checkout()
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Cajero.CHECKOUT_CARRITO_VACIO)
            self.assertEqual(self.MP_REGISTRADOR.monto(), None)
            self.assertEqual(self.MP_REGISTRADOR.tarjeta(), None)

    def test02(self):
        carrito = Carrito(CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=self.MP_REGISTRADOR)

        carrito.agregar(LIBRO)
        precio = cajero.checkout()

        self.assertEqual(precio, 17)
        self.assertEqual(self.MP_REGISTRADOR.monto(), 17)
        self.assertEqual(self.MP_REGISTRADOR.tarjeta(), TARJETA)

    def test03(self):
        carrito = Carrito(CATALOGO_DE_MULTIPLES_ELEMENTOS)
        cajero = Cajero(catalogo=CATALOGO_DE_MULTIPLES_ELEMENTOS, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=self.MP_REGISTRADOR)

        carrito.agregar(LIBRO)
        carrito.agregar(OTRO_LIBRO)
        precio = cajero.checkout()

        self.assertEqual(precio, 17 + 33)
        self.assertEqual(self.MP_REGISTRADOR.monto(), 17 + 33)
        self.assertEqual(self.MP_REGISTRADOR.tarjeta(), TARJETA)

    def test04(self):
        carrito = Carrito(CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=self.MP_REGISTRADOR)

        carrito.agregar(LIBRO)
        carrito.agregar(LIBRO)
        precio = cajero.checkout()

        self.assertEqual(precio, 2*17)
        self.assertEqual(self.MP_REGISTRADOR.monto(), 2*17)
        self.assertEqual(self.MP_REGISTRADOR.tarjeta(), TARJETA)

    def test05(self):
        carrito = Carrito(catalogo=CATALOGO_DE_MULTIPLES_ELEMENTOS)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=self.MP_REGISTRADOR)

        carrito.agregar(LIBRO)
        carrito.agregar(OTRO_LIBRO)

        try:
            precio = cajero.checkout()
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Cajero.PRODUCTO_NO_ESTA_EN_CATALOGO)
            self.assertEqual(self.MP_REGISTRADOR.monto(), None)
            self.assertEqual(self.MP_REGISTRADOR.tarjeta(), None)

    def test06_no_se_puede_hacer_checkout_con_tarjeta_invalida(self):
        carrito = Carrito(catalogo=CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA, fecha=date(2021, 1, 1), mp=self.MP_REGISTRADOR)

        carrito.agregar(LIBRO)

        try:
            precio = cajero.checkout()
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Cajero.TARJETA_EXPIRADA)
            self.assertEqual(self.MP_REGISTRADOR.monto(), None)
            self.assertEqual(self.MP_REGISTRADOR.tarjeta(), None)

    def test07(self):
        carrito = Carrito(catalogo=CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=self.MP_REGISTRADOR)

        carrito.agregar(LIBRO)

        precio = cajero.checkout()
        self.assertEqual(self.MP_REGISTRADOR.monto(), 17)
        self.assertEqual(self.MP_REGISTRADOR.tarjeta(), TARJETA)
