# coding=utf-8
__author__ = "Rodrigo"
__date__ = "$10-jun-2019 14:00:10$"

from Conexiones.Conexiones import Conexiones
import time
from datetime import datetime


def main ():
    
    """
    #Ejemplo parseo de str a timestamp
    fechaEjemplo = "2019-06-12 13:18:38"
    fechaTstamp = datetime.strptime(fechaEjemplo, '%Y-%m-%d %H:%M:%S')
    print(fechaTstamp)
    print(fechaTstamp.day)
    print(fechaTstamp.second)
    """

    conexion = Conexiones()
    fecha = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    nodo = 21

    while True:

        logs =  conexion.obtenerLogs()
        print(logs) 
        time.sleep (5)
        



if __name__ == "__main__":
    main ()
