import unittest
from src.math.matrices import *

class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_mat4Mul(self):
        m = Mat4([num for num in range(1,17)])
        m2 = Mat4([num for num in range(17,33)])
        m3 = m*m2

        self.assertIsNotNone(m3)
        # resultat de https://matrix.reshish.com/fr/matrix-multiplication/
        self.assertEqual(m3, Mat4([250,260,270,280,618,644,670,696,986,1028,1070,1112,1354,1412,1470,1528]))

    def test_mat4Add(self):
        m = Mat4([num for num in range(1, 17)])
        m2 = Mat4([num for num in range(17, 33)])
        m3 = m+m2
        self.assertIsNotNone(m3)
        self.assertEqual(m3, Mat4([18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48]))

    def test_mat3Mul(self):
        m = Mat3([num for num in range(1,10)])
        m2 = Mat3([num for num in range(10,19)])
        m3 = m*m2

        self.assertIsNotNone(m3)
        # resultat de https://matrix.reshish.com/fr/matrix-multiplication/
        self.assertEqual(m3, Mat3([84,90,96,201,216,231,318,342,366]))

    def test_mat3Add(self):
        m = Mat3([num for num in range(1, 10)])
        m2 = Mat3([num for num in range(10, 19)])
        m3 = m+m2
        self.assertIsNotNone(m3)
        self.assertEqual(m3, Mat3([11,13,15,17,19,21,23,25,27]))

if __name__ == '__main__':
    unittest.main()
