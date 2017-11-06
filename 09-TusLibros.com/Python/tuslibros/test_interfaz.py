import unittest
from datetime import date
from interfaz import InterfazRest

CLIENTE = 'Cliente'
OTRO_CLIENTE = 'Otro Cliente'
CONTRASENIA = 'contraseña'

LIBRO = 'Libro'
OTRO_LIBRO = 'Otro Libro'
UN_TERCER_LIBRO = 'Un 3er Libro'

CATALOGO_VACIO = {}
CATALOGO_DE_UN_ELEMENTO = { LIBRO: 17 }
CATALOGO_DE_MULTIPLES_ELEMENTOS = { LIBRO: 17, OTRO_LIBRO: 33, UN_TERCER_LIBRO: 42 }

LISTA_DE_USUARIOS_VACIA = {}
LISTA_DE_USUARIOS_CON_UN_USUARIO = { CLIENTE: CONTRASENIA }
LISTA_DE_USUARIOS_CON_MULTIPLES_USUARIO = { CLIENTE: CONTRASENIA, OTRO_CLIENTE: CONTRASENIA }

class SimuladorMerchantProcessor(object):
    def debit(self, tarjeta, monto):
        return 2

MP = SimuladorMerchantProcessor()
FECHA = date(2017, 1, 1)

class TestInterfaz(unittest.TestCase):
    def test01(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_VACIA, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        try:
            id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)

    def test02(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        self.assertEqual(interfaz.list_cart(id_carrito), [])
        self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))

    def test03(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        try:
            id_carrito = interfaz.create_cart(CLIENTE, 'contraseña inválida')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)

    def test04(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 1)
        self.assertEqual(interfaz.list_cart(id_carrito), [(LIBRO, 1)])
        self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))

    def test05(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 2)
        self.assertEqual(interfaz.list_cart(id_carrito), [(LIBRO, 2)])
        self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))

    def test06(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        try:
            interfaz.add_to_cart(42, LIBRO, 2)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.CARRITO_INVALIDO)

    def test07(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        try:
            interfaz.add_to_cart(1, LIBRO, 2)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.CARRITO_INVALIDO)



    # TODO: No se pueden agregar cosas a un carrito checkauteado
    # TODO: Testear timeout

    def test08(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        id_carrito1 = interfaz.create_cart(CLIENTE, CONTRASENIA)
        id_carrito2 = interfaz.create_cart(CLIENTE, CONTRASENIA)

        interfaz.add_to_cart(id_carrito1, LIBRO, 1)
        interfaz.add_to_cart(id_carrito2, LIBRO, 3)

        self.assertEqual(interfaz.list_cart(id_carrito1), [(LIBRO, 1)])
        self.assertEqual(interfaz.list_cart(id_carrito2), [(LIBRO, 3)])

        self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))

    def test09(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        id_carrito1 = interfaz.create_cart(CLIENTE, CONTRASENIA)
        id_carrito2 = interfaz.create_cart(CLIENTE, CONTRASENIA)

        interfaz.add_to_cart(id_carrito1, LIBRO, 1)
        interfaz.add_to_cart(id_carrito2, LIBRO, 3)

        self.assertEqual(interfaz.list_cart(id_carrito1), [(LIBRO, 1)])
        self.assertEqual(interfaz.list_cart(id_carrito2), [(LIBRO, 3)])

        self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))

    def test10(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        try:
            interfaz.list_cart(42)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.CARRITO_INVALIDO)

    def test11(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)

        try:
            interfaz.checkout(id_carrito, '2' * 16, '012019', 'duenio')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.CHECKOUT_CARRITO_VACIO)
            self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))


    def test12(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 1)

        try:
            interfaz.checkout(id_carrito, '2' * 16, '12019', 'duenio')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.FECHA_INVALIDA)
            self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))

    def test13(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        try:
            interfaz.list_purchases('Cliente inexistente', CONTRASENIA)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)

    def test14(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        try:
            interfaz.checkout(42, '2' * 16, '122019', 'duenio')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.CARRITO_INVALIDO)

    def test15(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 1)
        transaction_id = interfaz.checkout(id_carrito, '2' * 16, '122019', 'duenio')

        self.assertEqual(transaction_id, 2)
        self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([(LIBRO, 1)], 17))

    def test16(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, FECHA, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 3)
        interfaz.add_to_cart(id_carrito, OTRO_LIBRO, 2)
        interfaz.checkout(id_carrito, '2' * 16, '122019', 'duenio')

        compras, total = interfaz.list_purchases(CLIENTE, CONTRASENIA)
        self.assertEqual(total, 3*17 + 2*33)
        self.assertEqual(len(compras), 2)
        self.assertTrue((LIBRO, 3) in compras)
        self.assertTrue((OTRO_LIBRO, 2) in compras)

    def test17(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, FECHA, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 3)
        interfaz.checkout(id_carrito, '2' * 16, '122019', 'duenio')

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 3)
        interfaz.checkout(id_carrito, '2' * 16, '122019', 'duenio')

        compras, total = interfaz.list_purchases(CLIENTE, CONTRASENIA)
        self.assertEqual(total, 3*17 + 3*17)
        self.assertEqual(len(compras), 1)
        self.assertTrue((LIBRO, 6) in compras)

    def test18(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_MULTIPLES_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, FECHA, MP)

        id_carrito_1 = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito_1, LIBRO, 3)
        interfaz.checkout(id_carrito_1, '2' * 16, '122019', 'duenio')

        id_carrito_2 = interfaz.create_cart(OTRO_CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito_2, OTRO_LIBRO, 1)
        interfaz.checkout(id_carrito_2, '2' * 16, '122019', 'duenio')

        compras, total = interfaz.list_purchases(CLIENTE, CONTRASENIA)
        self.assertEqual(total, 3*17)
        self.assertEqual(len(compras), 1)
        self.assertTrue((LIBRO, 3) in compras)

        compras, total = interfaz.list_purchases(OTRO_CLIENTE, CONTRASENIA)
        self.assertEqual(total, 33)
        self.assertEqual(len(compras), 1)
        self.assertTrue((OTRO_LIBRO, 1) in compras)

    def test19(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, FECHA, MP)

        try:
            id_carrito = interfaz.list_purchases(CLIENTE, 'contraseña inválida')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)

    def test20(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_MULTIPLES_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, FECHA, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 3)
        interfaz.checkout(id_carrito, '2' * 16, '122019', 'duenio')

        try:
            interfaz.list_cart(id_carrito)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.CARRITO_INVALIDO)

    def test21(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_MULTIPLES_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, FECHA, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 3)
        interfaz.checkout(id_carrito, '2' * 16, '122019', 'duenio')

        compras, total = interfaz.list_purchases(CLIENTE, CONTRASENIA)
        self.assertEqual(total, 3*17)
        self.assertEqual(len(compras), 1)
        self.assertTrue((LIBRO, 3) in compras)

        try:
            interfaz.add_to_cart(id_carrito, LIBRO, 2)
            self.fail()
        except Exception as e:
            self.assertTrue(str(e), InterfazRest.CARRITO_INVALIDO)
            compras, total = interfaz.list_purchases(CLIENTE, CONTRASENIA)
            self.assertEqual(total, 3*17)
            self.assertEqual(len(compras), 1)
            self.assertTrue((LIBRO, 3) in compras)
