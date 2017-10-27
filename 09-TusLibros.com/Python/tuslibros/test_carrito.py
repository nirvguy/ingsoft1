import unittest

from carrito import Carrito

class CarritoTest(unittest.TestCase):
    def setUp(self):
        self.libro = 'libro'
        self.catalogo_con_un_solo_libro = set([self.libro])

    def test01_carrito_recien_creado_esta_vacio(self):
        carrito = Carrito(set())

        self.assertTrue(carrito.vacio())
        self.assertFalse(self.libro in carrito)

    def test02_carrito_con_un_elemento_no_esta_vacio(self):
        carrito = Carrito(self.catalogo_con_un_solo_libro)

        carrito.agregar(self.libro)

        self.assertFalse(carrito.vacio())
        self.assertTrue(self.libro in carrito)

    def test03_no_se_puede_agregar_un_producto_que_no_esta_en_el_catalogo(self):
        otro_libro = 'otro libro'
        carrito = Carrito(self.catalogo_con_un_solo_libro)

        try:
            carrito.agregar(otro_libro)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Carrito.PRODUCTO_NO_ESTA_EN_CATALOGO)
            self.assertTrue(carrito.vacio())
            self.assertTrue(otro_libro not in carrito)

    def test04_el_producto_agregado_una_vez_tiene_una_sola_unidad(self):
        carrito = Carrito(self.catalogo_con_un_solo_libro)

        carrito.agregar(self.libro)

        self.assertEqual(carrito.unidades(self.libro), 1)

    def test05_el_producto_agregado_multiples_veces_tiene_esa_cantidad_de_unidades(self):
        carrito = Carrito(self.catalogo_con_un_solo_libro)

        carrito.agregar(self.libro)
        carrito.agregar(self.libro)

        self.assertEqual(carrito.unidades(self.libro), 2)

    def test06_no_se_puede_consultar_la_cantidad_de_unidades_de_un_producto_que_no_esta_en_el_carro(self):
        carrito = Carrito(set())

        try:
            unidades = carrito.unidades(self.libro)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Carrito.PRODUCTO_NO_ESTA_EN_CATALOGO)
            self.assertTrue(carrito.vacio())
