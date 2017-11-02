import unittest
from datetime import date
from tarjeta import Tarjeta

DUENIO = 'fulano'

class TestTarjeta(unittest.TestCase):
    def test01(self):
        try:
            tarjeta = Tarjeta(numero='1', mes_expiracion=10, anio_expiracion=2015, duenio=DUENIO)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.NRO_INVALIDO)

    def test02(self):
        numero_tarjeta = '1' * 16
        tarjeta = Tarjeta(numero=numero_tarjeta, mes_expiracion=10, anio_expiracion=2015, duenio=DUENIO)
        self.assertEqual(tarjeta.duenio(), DUENIO)
        self.assertEqual(tarjeta.numero(), numero_tarjeta)
        self.assertEqual(tarjeta.mes_expiracion(), 10)
        self.assertEqual(tarjeta.anio_expiracion(), 2015)

    def test03(self):
        try:
            tarjeta = Tarjeta(numero='1' * 17, mes_expiracion=10, anio_expiracion=2015, duenio=DUENIO)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.NRO_INVALIDO)

    def test04(self):
        try:
            tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=10, anio_expiracion=2015, duenio='')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.DUENIO_VACIO)

    def test05(self):
        numero = '1234567891012134'
        tarjeta = Tarjeta(numero=numero, mes_expiracion=1, anio_expiracion=2017, duenio='mengano')

        self.assertEqual(tarjeta.numero(), numero)
        self.assertEqual(tarjeta.duenio(), 'mengano')
        self.assertEqual(tarjeta.mes_expiracion(), 1)
        self.assertEqual(tarjeta.anio_expiracion(), 2017)

        self.assertFalse(tarjeta.expiro(date(2016, 1, 10)))
        self.assertTrue(tarjeta.expiro(date(2018, 1, 10)))

    def test06(self):
        tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=10, anio_expiracion=2012, duenio='mengano')

        self.assertFalse(tarjeta.expiro(date(2012, 9, 29)))
        self.assertTrue(tarjeta.expiro(date(2012, 11, 30)))

    def test06(self):
        tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=10, anio_expiracion=2012, duenio='mengano')

        self.assertFalse(tarjeta.expiro(date(2011, 9, 29)))
        self.assertFalse(tarjeta.expiro(date(2011, 11, 30)))
        self.assertTrue(tarjeta.expiro(date(2013, 9, 29)))
        self.assertTrue(tarjeta.expiro(date(2013, 11, 30)))

    def test07(self):
        try:
            tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=0, anio_expiracion=2015, duenio=DUENIO)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.MES_INVALIDO)

    def test08(self):
        try:
            tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=13, anio_expiracion=2015, duenio=DUENIO)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.MES_INVALIDO)

    def test09(self):
        try:
            tarjeta = Tarjeta(numero='1' * 16, mes_expiracion=10, anio_expiracion=2017, duenio=' ')
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Tarjeta.DUENIO_VACIO)
