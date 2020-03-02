import unittest
import pytest
import os,sys,time
from Dispensador import Dispensador
from Mei import Mei


raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
sys.path.append(raiz)

from PuertoSerie import PuertoSerie


ser = PuertoSerie ("PuertoSerie",dispositivo = PuertoSerie.ARDUINO_MICRO)
ser.abrirPuerto()
Mei = Mei(ser)


@pytest.mark.repeat(0)
def test_vuelve_intentar_dar_cambio():
        """
        Test that it can sum a list of integers
        """
        #for i in range(5):
        #Mei = Mei(ser)
        cassete_antes = Mei.estatusTubos()
        
        cambio_a_dispensar = 3

        cambio_dispensado,intentos = Mei.dispensarCambio(cambio_a_dispensar)

        assert cambio_dispensado == cambio_a_dispensar


'''
@pytest.mark.repeat(1)
def test_dispensar_un_peso():
        """
        Test that it can sum a list of integers
        """
        #for i in range(5):
        #Mei = Mei(ser)
        cassete_antes = Mei.estatusTubos()
        #for i in range(0, 5):
        print("TEST:")
        Mei.darCambio(1)
        time.sleep(1)
        cassete_despues = Mei.estatusTubos()
        assert cassete_antes[0]-1 == cassete_despues[0]
'''

'''
@pytest.mark.repeat(35)
def test_valores_en_tubos_diferentes():
    """
    Comprobar que los valores en los tubos no cambian
    """
    #for i in range(0, 10):
    cassete_antes = Mei.estatusTubos()
    time.sleep(1)

    assert cassete_antes == [11, 5, 2, 3]
'''





    
