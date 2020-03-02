import unittest
import pytest
import os,sys,time
from Dispensador import Dispensador
from Mei import Mei


raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
sys.path.append(raiz)

from PuertoSerie import PuertoSerie


class TestSum(unittest.TestCase):
    global Mei
    ser = PuertoSerie ("PuertoSerie",dispositivo = PuertoSerie.ARDUINO_MICRO)
    ser.abrirPuerto()
    Mei = Mei(ser)
    
    
    def test_valores_en_tubos_diferentes(self):
        """
        Comprobar que los valores en los tubos no cambian
        """
        #for i in range(0, 10):
        cassete_antes = Mei.estatusTubos()
        time.sleep(1)

        self.assertEqual(cassete_antes, [0,5,2,3])

    
    def test_dispensar_un_peso(self):
        """
        Test that it can sum a list of integers
        """
        #for i in range(5):
        #Mei = Mei(ser)
        Mei.inicializar()
        Mei.disable_coin()
        cassete_antes = Mei.estatusTubos()
        for i in range(0, 5):
            print("TEST:",i)
            Mei.darCambio(3)
            Mei.poll()
            #time.sleep(1)
        time.sleep(1)
        cassete_despues = Mei.estatusTubos()

        self.assertEqual(cassete_antes[0]-5, cassete_despues[0])

    '''def test_cambioNoCompletado(self):
        """
        Test that it can sum a of integers
        """
        for i in range(5):
            Hopper = Dispensador("Hopper",[1,2,3,4])
            nombre = Hopper.get_nombre()
            self.assertEqual(nombre, "Hopper")
    

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    '''

if __name__ == '__main__':
    unittest.main()