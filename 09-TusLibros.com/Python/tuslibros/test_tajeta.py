import unittest
from datetime import date
from tarjeta import Tarjeta

DUENIO = 'fulano'

class TestTarjeta(unittest.TestCase):
    def test01_no_existen_tarjetas_con_menos_de_dieciseis_numeros(self):
        try:
            tarjeta = Tarjeta(numero='1', mes_expiracion=10, anio_expiracion=2015, duenio=DUENIO)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.NRO_INVALIDO)

    def test02_una_tarjeta_dice_su_duenio_numero_y_fecha_de_expiracion(self):
        numero_tarjeta = '1' * 16
        tarjeta = Tarjeta(numero=numero_tarjeta, mes_expiracion=10, anio_expiracion=2015, duenio=DUENIO)
        self.assertEqual(tarjeta.duenio(), DUENIO)
        self.assertEqual(tarjeta.numero(), numero_tarjeta)
        self.assertEqual(tarjeta.mes_expiracion(), 10)
        self.assertEqual(tarjeta.anio_expiracion(), 2015)

    def test03_no_existen_tarjetas_con_mas_de_dieciseis_numeros(self):
        try:
            tarjeta = Tarjeta(numero='1' * 17, mes_expiracion=10, anio_expiracion=2015, duenio=DUENIO)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.NRO_INVALIDO)

    def test04_no_existen_tarjetas_con_duenio_vacio(self):
        try:
            tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=10, anio_expiracion=2015, duenio='')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.DUENIO_VACIO)

    def test05_una_tarjeta_expira_cuando_el_anio_es_posterior_a_la_fecha_dada(self):
        numero = '1234567891012134'
        tarjeta = Tarjeta(numero=numero, mes_expiracion=1, anio_expiracion=2017, duenio='mengano')

        self.assertEqual(tarjeta.numero(), numero)
        self.assertEqual(tarjeta.duenio(), 'mengano')
        self.assertEqual(tarjeta.mes_expiracion(), 1)
        self.assertEqual(tarjeta.anio_expiracion(), 2017)

        self.assertFalse(tarjeta.expiro(date(2016, 1, 10)))
        self.assertTrue(tarjeta.expiro(date(2018, 1, 10)))

    def test06_una_tarjeta_expira_cuando_el_anio_es_el_mismo_pero_el_mes_es_posterior(self):
        tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=10, anio_expiracion=2012, duenio='mengano')

        self.assertFalse(tarjeta.expiro(date(2012, 9, 29)))
        self.assertTrue(tarjeta.expiro(date(2012, 11, 30)))

    def test06_una_tarjeta_expira_si_el_anio_es_posterior_aunque_el_mes_se_anterior(self):
        tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=10, anio_expiracion=2012, duenio='mengano')

        self.assertFalse(tarjeta.expiro(date(2011, 9, 29)))
        self.assertFalse(tarjeta.expiro(date(2011, 11, 30)))
        self.assertTrue(tarjeta.expiro(date(2013, 9, 29)))
        self.assertTrue(tarjeta.expiro(date(2013, 11, 30)))

    def test07_no_existe_mes_de_expiracion_0(self):
        try:
            tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=0, anio_expiracion=2015, duenio=DUENIO)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.MES_INVALIDO)

    def test08_no_existe_mes_de_expiracion_superior_a_12(self):
        try:
            tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=13, anio_expiracion=2015, duenio=DUENIO)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.MES_INVALIDO)

    def test09_no_existen_tarjetas_con_duenio_todo_con_espacios(self):
        try:
            tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=10, anio_expiracion=2017, duenio=' ')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.DUENIO_VACIO)

    def test10_no_existen_mes_de_expiracion_negativo(self):
        try:
            tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=-1, anio_expiracion=2015, duenio=DUENIO)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.MES_INVALIDO)
