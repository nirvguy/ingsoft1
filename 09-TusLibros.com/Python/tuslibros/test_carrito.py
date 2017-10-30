import unittest

from carrito import Carrito

libro = 'Libro'
otro_libro = 'Otro Libro'
un_tercer_libro = 'Un 3er Libro'

def crear_carrito_con_catalogo_vacio():
    return Carrito(set())

def crear_carrito_con_catalogo_de_un_solo_elemento():
    return Carrito(set([libro]))

def crear_carrito_con_catalogo_de_varios_elementos():
    return Carrito(set([libro, otro_libro, un_tercer_libro]))

class CarritoTest(unittest.TestCase):
    def test01_carrito_recien_creado_esta_vacio(self):
        carrito = crear_carrito_con_catalogo_vacio()

        self.assertTrue(carrito.vacio())
        self.assertFalse(libro in carrito)

    def test02_carrito_con_un_elemento_no_esta_vacio(self):
        carrito = crear_carrito_con_catalogo_de_un_solo_elemento()

        carrito.agregar(libro)

        self.assertFalse(carrito.vacio())
        self.assertTrue(libro in carrito)

    def test03_no_se_puede_agregar_un_producto_que_no_esta_en_el_catalogo(self):
        carrito = crear_carrito_con_catalogo_de_un_solo_elemento()

        try:
            carrito.agregar(otro_libro)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Carrito.PRODUCTO_NO_ESTA_EN_CATALOGO)
            self.assertTrue(carrito.vacio())
            self.assertTrue(otro_libro not in carrito)

    def test04_el_producto_agregado_una_vez_tiene_una_sola_unidad(self):
        carrito = crear_carrito_con_catalogo_de_un_solo_elemento()

        carrito.agregar(libro)

        self.assertEqual(carrito.unidades(libro), 1)

    def test05_el_producto_agregado_multiples_veces_tiene_esa_cantidad_de_unidades(self):
        carrito = crear_carrito_con_catalogo_de_un_solo_elemento()

        carrito.agregar(libro)
        carrito.agregar(libro)

        self.assertEqual(carrito.unidades(libro), 2)

    def test06_no_se_puede_consultar_la_cantidad_de_unidades_de_un_producto_que_no_esta_en_el_carro(self):
        carrito = crear_carrito_con_catalogo_vacio()

        try:
            unidades = carrito.unidades(libro)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Carrito.PRODUCTO_NO_ESTA_EN_CATALOGO)
            self.assertTrue(carrito.vacio())
