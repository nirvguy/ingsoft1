import unittest
from autenticador import Autenticador

CLIENTE = 'Cliente'
OTRO_CLIENTE = 'Otro Cliente'
CONTRASENIA = 'contrasenia'
OTRA_CONTRASENIA = 'otra_contrasenia'

LISTA_DE_USUARIOS_VACIA = {}
LISTA_DE_USUARIOS_CON_UN_USUARIO = { CLIENTE: CONTRASENIA }
LISTA_DE_USUARIOS_CON_MULTIPLES_USUARIO = { CLIENTE: CONTRASENIA, OTRO_CLIENTE: OTRA_CONTRASENIA }

class TestAutenticador(unittest.TestCase):
    def test01_no_se_puede_autenticar_un_usuario_no_registrado(self):
        autenticador = Autenticador(LISTA_DE_USUARIOS_VACIA)

        try:
            autenticador.login(CLIENTE, CONTRASENIA)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Autenticador.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)

    def test02_autenticar_correctamente_no_realiza_nada(self):
        autenticador = Autenticador(LISTA_DE_USUARIOS_CON_UN_USUARIO)

        autenticador.login(CLIENTE, CONTRASENIA)

    def test03_no_se_puede_autenticar_con_contrasenia_incorrecta(self):
        autenticador = Autenticador(LISTA_DE_USUARIOS_CON_UN_USUARIO)

        try:
            autenticador.login(CLIENTE, 'contrasenia invalida')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Autenticador.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)
