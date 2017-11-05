import unittest
from venta import Venta

class TestVenta(unittest.TestCase):
    def test01(self):
        venta = Venta({1: 2, 3 : 4}, 10)

        self.assertEqual(venta.productos(), [(1, 2), (3, 4)])
        self.assertEqual(venta.total(), 10)

    def test02(self):
        venta1 = Venta({1: 2, 3: 4}, 10)
        venta2 = Venta({1: 2, 3: 4}, 10)

        self.assertEqual(venta1, venta2)

    def test03(self):
        venta1 = Venta({1: 2, 3: 4}, 10)
        venta2 = Venta({1: 2, 3: 8}, 10)

        self.assertNotEqual(venta1, venta2)

    def test04(self):
        try:
            Venta({}, 0)
            self.fail()
        except Exception as e:
            self.assertEqual(str(e), Venta.VENTA_SIN_PRODUCTOS)
