import unittest
from datetime import date, datetime, time, timedelta
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

FECHA = datetime(2017, 1, 1, 0, 0, 0)

class SimuladorMerchantProcessor(object):
    def debit(self, tarjeta, monto):
        return 2

MP = SimuladorMerchantProcessor()

class SimuladorReloj(object):
    def today(self):
        pass

    def avanzar_minutos(self, minutos):
        pass

class RelojEstacionario(SimuladorReloj):
    def today(self):
        return FECHA

class RelojMovil(SimuladorReloj):
    def __init__(self):
        self._fecha = FECHA

    def today(self):
        return self._fecha

    def avanzar_minutos(self, minutos):
        self._fecha += timedelta(minutes=minutos)

RELOJ_ESTACIONARIO = RelojEstacionario()

class TestInterfaz(unittest.TestCase):
    def test01_no_se_puede_crear_un_carrito_con_un_usuario_no_registrado(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_VACIA, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        try:
            id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)

    def test02_al_crear_un_carrito_vacio_la_lista_de_productos_del_carrito_debe_ser_vacia(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        self.assertEqual(interfaz.list_cart(id_carrito), [])
        self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))

    def test03_no_se_puede_crear_un_usuario_autenticandose_con_contrasenia_incorrecta(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        try:
            id_carrito = interfaz.create_cart(CLIENTE, 'contraseña inválida')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)

    def test04_agregar_un_producto_al_carrito_no_realiza_compras(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 1)
        self.assertEqual(interfaz.list_cart(id_carrito), [(LIBRO, 1)])
        self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))

    def test05_el_listado_de_un_carrito_con_un_producto_multiples_veces_se_informa_con_esa_cantidad(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 2)
        self.assertEqual(interfaz.list_cart(id_carrito), [(LIBRO, 2)])
        self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))

    def test06_no_se_puede_agregar_un_producto_a_un_carrito_inexistente(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        try:
            interfaz.add_to_cart(42, LIBRO, 2)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.CARRITO_INVALIDO)


    # TODO: Testear timeout

    def test08_distintos_carritos_con_distintos_productos_se_listan_de_manera_distinta(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        id_carrito1 = interfaz.create_cart(CLIENTE, CONTRASENIA)
        id_carrito2 = interfaz.create_cart(CLIENTE, CONTRASENIA)

        interfaz.add_to_cart(id_carrito1, LIBRO, 1)
        interfaz.add_to_cart(id_carrito2, LIBRO, 3)

        self.assertEqual(interfaz.list_cart(id_carrito1), [(LIBRO, 1)])
        self.assertEqual(interfaz.list_cart(id_carrito2), [(LIBRO, 3)])

        self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))

    def test10_no_se_pueden_listar_carritos_con_un_id_inexistente(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        try:
            interfaz.list_cart(42)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.CARRITO_INVALIDO)

    def test11_no_se_puede_realizar_checkout_de_un_carrito_vacio(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)

        try:
            interfaz.checkout(id_carrito, '2' * 16, '012019', 'duenio')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.CHECKOUT_CARRITO_VACIO)
            self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))


    def test12_no_se_puede_realizar_checkout_si_la_fecha_de_la_tarjeta_es_invalida(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 1)

        try:
            interfaz.checkout(id_carrito, '2' * 16, '12019', 'duenio')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.FECHA_INVALIDA)
            self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([], 0))

    def test13_no_se_pueden_listar_las_compras_de_un_cliente_inexistente(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        try:
            interfaz.list_purchases('Cliente inexistente', CONTRASENIA)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)

    def test14_no_se_puede_hacer_checkout_de_un_carrito_inexistente(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        try:
            interfaz.checkout(42, '2' * 16, '122019', 'duenio')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.CARRITO_INVALIDO)

    def test15_al_hacer_checkout_de_un_producto_este_figura_como_comprado(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 1)
        transaction_id = interfaz.checkout(id_carrito, '2' * 16, '122019', 'duenio')

        self.assertEqual(transaction_id, 2)
        self.assertEqual(interfaz.list_purchases(CLIENTE, CONTRASENIA), ([(LIBRO, 1)], 17))

    def test16_al_hacer_checkout_de_multiples_productos_estos_figuran_comprados(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, RELOJ_ESTACIONARIO, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 3)
        interfaz.add_to_cart(id_carrito, OTRO_LIBRO, 2)
        interfaz.checkout(id_carrito, '2' * 16, '122019', 'duenio')

        compras, total = interfaz.list_purchases(CLIENTE, CONTRASENIA)
        self.assertEqual(total, 3*17 + 2*33)
        self.assertEqual(len(compras), 2)
        self.assertTrue((LIBRO, 3) in compras)
        self.assertTrue((OTRO_LIBRO, 2) in compras)

    def test17_multiples_compras_de_un_producto_se_suman_en_la_lista_de_compras(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, RELOJ_ESTACIONARIO, MP)

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

    def test18_multiples_compras_de_usuarios_distintos_terminan_en_lista_de_compras_distintas(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_MULTIPLES_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, RELOJ_ESTACIONARIO, MP)

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

    def test19_no_se_pueden_listar_las_compras_con_un_usuario_mal_autenticado(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        try:
            id_carrito = interfaz.list_purchases(CLIENTE, 'contraseña inválida')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)

    def test20_no_se_pueden_lista_los_productos_de_un_carrito_ya_checkouteado(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_MULTIPLES_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, RELOJ_ESTACIONARIO, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 3)
        interfaz.checkout(id_carrito, '2' * 16, '122019', 'duenio')

        try:
            interfaz.list_cart(id_carrito)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.CARRITO_INVALIDO)

    def test21_no_se_puede_agregar_productos_a_un_carrito_ya_checkouteado(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_MULTIPLES_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, RELOJ_ESTACIONARIO, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 3)
        interfaz.checkout(id_carrito, '2' * 16, '122019', 'duenio')

        try:
            interfaz.add_to_cart(id_carrito, LIBRO, 2)
            self.fail()
        except Exception as e:
            self.assertTrue(str(e), InterfazRest.CARRITO_INVALIDO)
            compras, total = interfaz.list_purchases(CLIENTE, CONTRASENIA)
            self.assertEqual(total, 3*17)
            self.assertEqual(len(compras), 1)
            self.assertTrue((LIBRO, 3) in compras)

    def test22_no_se_puede_agregar_a_un_carrito_despues_de_31_minutos_de_inactividad(self):
        reloj = RelojMovil()
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_MULTIPLES_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, reloj, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        reloj.avanzar_minutos(31)

        try:
            interfaz.add_to_cart(id_carrito, LIBRO, 1)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.TIMEOUT_CARRITO)
            compras, total = interfaz.list_purchases(CLIENTE, CONTRASENIA)
            self.assertEqual(len(compras), 0)
            self.assertEqual(total, 0)

    def test23_no_se_puede_listar_un_carrito_despues_de_31_minutos_de_inactividad(self):
        reloj = RelojMovil()
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_MULTIPLES_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, reloj, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        reloj.avanzar_minutos(31)

        try:
            interfaz.list_cart(id_carrito)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.TIMEOUT_CARRITO)
            compras, total = interfaz.list_purchases(CLIENTE, CONTRASENIA)
            self.assertEqual(len(compras), 0)
            self.assertEqual(total, 0)

    def test24_no_se_puede_hacer_checkout_de_un_carrito_despues_de_31_minutos_de_inactividad(self):
        reloj = RelojMovil()
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_MULTIPLES_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, reloj, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito, LIBRO, 1)
        reloj.avanzar_minutos(31)

        try:
            interfaz.checkout(id_carrito, '2' * 16, '012019', 'duenio')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.TIMEOUT_CARRITO)
            compras, total = interfaz.list_purchases(CLIENTE, CONTRASENIA)
            self.assertEqual(len(compras), 0)
            self.assertEqual(total, 0)

    def test25_se_puede_vencer_un_carrito_y_otro_no(self):
        reloj = RelojMovil()
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_MULTIPLES_USUARIO, CATALOGO_DE_MULTIPLES_ELEMENTOS, reloj, MP)

        id_carrito_1 = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito_1, LIBRO, 1)
        reloj.avanzar_minutos(20)

        id_carrito_2 = interfaz.create_cart(CLIENTE, CONTRASENIA)
        interfaz.add_to_cart(id_carrito_2, OTRO_LIBRO, 2)
        reloj.avanzar_minutos(20)

        try:
            interfaz.list_cart(id_carrito_1)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.TIMEOUT_CARRITO)
            compras, total = interfaz.list_purchases(CLIENTE, CONTRASENIA)
            self.assertEqual(len(compras), 0)
            self.assertEqual(total, 0)
            productos_carrito = interfaz.list_cart(id_carrito_2)
            self.assertEqual(len(productos_carrito), 1)
            self.assertTrue((OTRO_LIBRO, 2) in productos_carrito)

    def test26_no_se_pueden_agregar_0_unidades_de_un_producto(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)

        interfaz.add_to_cart(id_carrito, LIBRO, 3)
        try:
            interfaz.add_to_cart(id_carrito, LIBRO, 0)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.UNIDADES_DEBEN_SER_POSITIVAS)
            productos_carrito = interfaz.list_cart(id_carrito)
            self.assertEqual(len(productos_carrito), 1)
            self.assertTrue((LIBRO, 3) in productos_carrito)

    def test27_no_se_pueden_agregar_una_cantidad_negativa_de_unidades_de_un_producto(self):
        interfaz = InterfazRest(LISTA_DE_USUARIOS_CON_UN_USUARIO, CATALOGO_DE_UN_ELEMENTO, RELOJ_ESTACIONARIO, MP)

        id_carrito = interfaz.create_cart(CLIENTE, CONTRASENIA)

        interfaz.add_to_cart(id_carrito, LIBRO, 3)
        try:
            interfaz.add_to_cart(id_carrito, LIBRO, -1)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), InterfazRest.UNIDADES_DEBEN_SER_POSITIVAS)
            productos_carrito = interfaz.list_cart(id_carrito)
            self.assertEqual(len(productos_carrito), 1)
            self.assertTrue((LIBRO, 3) in productos_carrito)
