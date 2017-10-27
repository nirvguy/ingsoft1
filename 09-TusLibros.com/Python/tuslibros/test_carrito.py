import unittest

from carrito import Carrito

class CarritoTest(unittest.TestCase):
    def test01_carrito_recien_creado_esta_vacio(self):
        carrito = Carrito(set())
        libro = 'libro'

        self.assertTrue(carrito.vacio())
        self.assertFalse(libro in carrito)

    def test02_carrito_con_un_elemento_no_esta_vacio(self):
        libro = 'libro'
        catalogo = set([libro])
        carrito = Carrito(catalogo)

        carrito.agregar(libro)

        self.assertFalse(carrito.vacio())
        self.assertTrue(libro in carrito)

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
            self.assertTrue(otro_libro not in carrito)

    def test04_el_producto_agregado_una_vez_tiene_una_sola_unidad(self):
        libro = 'libro'
        catalogo = set([libro])
        carrito = Carrito(catalogo)

        carrito.agregar(libro)

        self.assertEqual(carrito.unidades(libro), 1)

    def test05_el_producto_agregado_multiples_veces_tiene_esa_cantidad_de_unidades(self):
        libro = 'libro'
        catalogo = set([libro])
        carrito = Carrito(catalogo)

        carrito.agregar(libro)
        carrito.agregar(libro)

        self.assertEqual(carrito.unidades(libro), 2)

    def test06_no_se_puede_consultar_la_cantidad_de_unidades_de_un_producto_que_no_esta_en_el_carro(self):
        libro = 'libro'
        carrito = Carrito(set())

        try:
            unidades = carrito.unidades(libro)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Carrito.PRODUCTO_NO_ESTA_EN_CATALOGO)
            self.assertTrue(carrito.vacio())
