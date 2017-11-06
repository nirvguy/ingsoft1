import unittest
from datetime import date
from carrito import Carrito
from cajero import Cajero
from tarjeta import Tarjeta
from venta import Venta

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
        return 1

    def monto(self):
        return self._monto

    def tarjeta(self):
        return self._tarjeta

class MPXXX(SimuladorMerchantProcessor):
    def __init__(self, mensaje_excepcion):
        self._mensaje_excepcion = mensaje_excepcion

    def debit(self, tarjeta, monto):
        raise Exception(self._mensaje_excepcion)

class CajeroTest(unittest.TestCase):
    def setUp(self):
        self.MP_REGISTRADOR = MPRegistrador()
        self.LIBRO_DE_VENTAS = []

    def test01_no_se_puede_hacer_checkout_de_un_carrito_vacio(self):
        carrito = Carrito(CATALOGO_VACIO)
        cajero = Cajero(catalogo=CATALOGO_VACIO, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=self.MP_REGISTRADOR, libro=self.LIBRO_DE_VENTAS)

        try:
            transaction_id = cajero.checkout()
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Cajero.CHECKOUT_CARRITO_VACIO)
            self.assertEqual(self.MP_REGISTRADOR.monto(), None)
            self.assertEqual(self.MP_REGISTRADOR.tarjeta(), None)
            self.assertEqual(self.LIBRO_DE_VENTAS, [])

    def test02_el_checkout_de_un_solo_producto_se_agrega_al_libro_de_ventas(self):
        carrito = Carrito(CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=self.MP_REGISTRADOR, libro=self.LIBRO_DE_VENTAS)

        carrito.agregar(LIBRO)
        transaction_id = cajero.checkout()

        self.assertEqual(transaction_id, 1)
        self.assertEqual(self.MP_REGISTRADOR.monto(), 17)
        self.assertEqual(self.MP_REGISTRADOR.tarjeta(), TARJETA)
        self.assertEqual(self.LIBRO_DE_VENTAS, [Venta({LIBRO: 1}, 17)])

    def test03_el_monto_total_de_multiples_productos_de_una_unidad_checkaouteados_es_la_suma_del_monto_de_cada_producto(self):
        carrito = Carrito(CATALOGO_DE_MULTIPLES_ELEMENTOS)
        cajero = Cajero(catalogo=CATALOGO_DE_MULTIPLES_ELEMENTOS, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=self.MP_REGISTRADOR, libro=self.LIBRO_DE_VENTAS)

        carrito.agregar(LIBRO)
        carrito.agregar(OTRO_LIBRO)
        cajero.checkout()

        self.assertEqual(self.MP_REGISTRADOR.monto(), 17 + 33)
        self.assertEqual(self.MP_REGISTRADOR.tarjeta(), TARJETA)
        self.assertEqual(self.LIBRO_DE_VENTAS, [Venta({LIBRO: 1, OTRO_LIBRO: 1}, 17 + 33)])

    def test04_el_monto_total_de_un_producto_de_multiples_unidades_comprados_es_el_producto_de_las_unidades_por_el_monto(self):
        carrito = Carrito(CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=self.MP_REGISTRADOR, libro=self.LIBRO_DE_VENTAS)

        carrito.agregar(LIBRO)
        carrito.agregar(LIBRO)
        transaction_id = cajero.checkout()

        self.assertEqual(self.MP_REGISTRADOR.monto(), 2*17)
        self.assertEqual(self.MP_REGISTRADOR.tarjeta(), TARJETA)
        self.assertEqual(self.LIBRO_DE_VENTAS, [Venta({LIBRO: 2}, 2*17)])

    def test05_no_se_pueden_hacer_checkout_productos_inexistentes(self):
        carrito = Carrito(catalogo=CATALOGO_DE_MULTIPLES_ELEMENTOS)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=self.MP_REGISTRADOR, libro=self.LIBRO_DE_VENTAS)

        carrito.agregar(LIBRO)
        carrito.agregar(OTRO_LIBRO)

        try:
            transaction_id = cajero.checkout()
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Cajero.PRODUCTO_NO_ESTA_EN_CATALOGO)
            self.assertEqual(self.MP_REGISTRADOR.monto(), None)
            self.assertEqual(self.MP_REGISTRADOR.tarjeta(), None)
            self.assertEqual(self.LIBRO_DE_VENTAS, [])

    def test06_no_se_puede_hacer_checkout_con_tarjeta_invalida(self):
        carrito = Carrito(catalogo=CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA, fecha=date(2021, 1, 1), mp=self.MP_REGISTRADOR, libro=self.LIBRO_DE_VENTAS)

        carrito.agregar(LIBRO)

        try:
            transaction_id = cajero.checkout()
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Cajero.TARJETA_EXPIRADA)
            self.assertEqual(self.MP_REGISTRADOR.monto(), None)
            self.assertEqual(self.MP_REGISTRADOR.tarjeta(), None)
            self.assertEqual(self.LIBRO_DE_VENTAS, [])

    def test08_el_checkout_de_una_tarjeta_robada_no_afecta_el_libro_de_ventas(self):
        msg = 'Tarjeta robada!'
        mp = MPXXX(msg)
        carrito = Carrito(catalogo=CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=mp, libro=self.LIBRO_DE_VENTAS)

        carrito.agregar(LIBRO)

        try:
            transaction_id = cajero.checkout()
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), msg)
            self.assertEqual(self.LIBRO_DE_VENTAS, [])

    def test09_el_checkout_de_una_tarjeta_sin_fondo_no_afecta_el_libro_de_ventas(self):
        msg = 'Tarjeta sin fondo!'
        mp = MPXXX(msg)
        carrito = Carrito(catalogo=CATALOGO_DE_UN_ELEMENTO)
        cajero = Cajero(catalogo=CATALOGO_DE_UN_ELEMENTO, carrito=carrito, tarjeta=TARJETA, fecha=FECHA, mp=mp, libro=self.LIBRO_DE_VENTAS)

        carrito.agregar(LIBRO)

        try:
            transaction_id = cajero.checkout()
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), msg)
            self.assertEqual(self.LIBRO_DE_VENTAS, [])
