# coding=utf-8
__author__ = "SIGFRIDO"
__date__ = "$20-may-2019 17:00:10$"

from Botones import Botones, PuertoDeComunicacion, obtenerNombreDelPuerto

import time

def main ():
    
    
    #Se crea el constructor e inicia el puerto de comunicación
    
    #botones = Botones("COM7", 3, 2)
    #botones = Botones("/dev/ttyUSB0", 3, 3)
    #botones = Botones(3, 3, dispositivo = Botones.PUERTO_ARDUINO)
    #botones = Botones("/dev/ttyUSB6", 3, 3, dispositivo = Botones.PUERTO_ARDUINO)
    
    a = obtenerNombreDelPuerto(dispositivo = Botones.PUERTO_ARDUINO)
    print (a)
    
    #Ejemplo de Lectura
    """
    while True:
        a = botones.X[0].obtenerValor()
        b = botones.X[1].obtenerValor()
        c = botones.X[2].obtenerValor()
        print (a, b, c)
        
        time.sleep (0.1)
        
	"""

    """
    #Ejemplo de escritura
    
    time.sleep(4)
    botones.Y[0].establecerValor(1)
    time.sleep(2)
    botones.Y[1].establecerValor(1)
    
    time.sleep(2)
    botones.Y[0].establecerValor(0)
    time.sleep(2)
    botones.Y[1].establecerValor(0)"""
    

    #Para cerrar el puerto de comunicación
    #botones.cerrarPuerto()


if __name__ == "__main__":
    main ()
