import unittest

from carrito import Carrito

LIBRO = 'Libro'
OTRO_LIBRO = 'Otro Libro'
UN_TERCER_LIBRO = 'Un 3er Libro'

CATALOGO_VACIO = {}
CATALOGO_DE_UN_ELEMENTO = { LIBRO: 17 }
CATALOGO_DE_MULTIPLES_ELEMENTOS = { LIBRO: 17, OTRO_LIBRO: 33, UN_TERCER_LIBRO: 42 }

class CarritoTest(unittest.TestCase):
    def test01_carrito_recien_creado_esta_vacio(self):
        carrito = Carrito(CATALOGO_VACIO)

        self.assertTrue(carrito.vacio())
        self.assertFalse(LIBRO in carrito)

    def test02_carrito_con_un_elemento_no_esta_vacio(self):
        carrito = Carrito(CATALOGO_DE_UN_ELEMENTO)

        carrito.agregar(LIBRO)

        self.assertFalse(carrito.vacio())
        self.assertTrue(LIBRO in carrito)

    def test03_no_se_puede_agregar_un_producto_que_no_esta_en_el_catalogo(self):
        carrito = Carrito(CATALOGO_DE_UN_ELEMENTO)

        try:
            carrito.agregar(OTRO_LIBRO)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Carrito.PRODUCTO_NO_ESTA_EN_CATALOGO)
            self.assertTrue(carrito.vacio())
            self.assertTrue(OTRO_LIBRO not in carrito)

    def test04_el_producto_agregado_una_vez_tiene_una_sola_unidad(self):
        carrito = Carrito(CATALOGO_DE_UN_ELEMENTO)

        carrito.agregar(LIBRO)

        self.assertEqual(carrito.unidades(LIBRO), 1)

    def test05_el_producto_agregado_multiples_veces_tiene_esa_cantidad_de_unidades(self):
        carrito = Carrito(CATALOGO_DE_UN_ELEMENTO)

        carrito.agregar(LIBRO)
        carrito.agregar(LIBRO)

        self.assertEqual(carrito.unidades(LIBRO), 2)

    def test06_no_se_puede_consultar_la_cantidad_de_unidades_de_un_producto_que_no_esta_en_el_carro(self):
        carrito = Carrito(CATALOGO_VACIO)

        try:
            unidades = carrito.unidades(LIBRO)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Carrito.PRODUCTO_NO_ESTA_EN_CATALOGO)
            self.assertTrue(carrito.vacio())

    def test07_se_pueden_listar_los_productos_de_un_carrito(self):
        carrito = Carrito(CATALOGO_DE_MULTIPLES_ELEMENTOS)

        carrito.agregar(LIBRO)
        carrito.agregar(LIBRO)
        carrito.agregar(OTRO_LIBRO)
        productos = carrito.productos()

        self.assertEqual(len(productos), 2)
        self.assertTrue(LIBRO in productos)
        self.assertTrue(OTRO_LIBRO in productos)
