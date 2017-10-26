import unittest

from carrito import Carrito

class CarritoTest(unittest.TestCase):
    def test01_carrito_recien_creado_esta_vacio(self):
        carrito = Carrito(set())
        libro = 'libro'

        self.assertTrue(carrito.vacio())
        self.assertFalse(carrito.contiene(libro))

    def test02_carrito_con_un_elemento_no_esta_vacio(self):
        libro = 'libro'
        catalogo = set([libro])
        carrito = Carrito(catalogo)

        carrito.agregar(libro)

        self.assertFalse(carrito.vacio())
        self.assertTrue(carrito.contiene(libro))

    def test03_no_se_puede_agregar_un_producto_que_no_esta_en_el_catalogo(self):
        libro = 'libro'
        otro_libro = 'otro libro'
        catalogo = set([libro])
        carrito = Carrito(catalogo)

        try:
            carrito.agregar(otro_libro)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Carrito.PRODUCTO_NO_ESTA_EN_CATALOGO)
            self.assertTrue(carrito.vacio())
            self.assertFalse(carrito.contiene(otro_libro))
