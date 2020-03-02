# coding=utf-8

__author__ = "SIGFRIDO"
__date__ = "$02-jul-2019 17:07:46$"

from struct import *



class Comunicacion ():
    
    numeroConsecutivoDeInstruccion = 1000
    
    caracterDeInicio = '-';
    caracterDeFin = '*';



    # Tipo de instrucción 
    ADMINISTRACION = 1
    PROCESO = 2

    # Instrucciones para ADMINISTRACION


    # Instrucciones para PROCESO
    MDB_DATOS = 11
    
    BOTON_CANCELAR = 24
    
    
    def __init__ (self):
        
        self.arregloByte = 1
        self.tamanioInstruccion = 0
        pass
  
    def crearInstruccion (self, tipo = 0, instruccion = 1, *args, **kargs):
        self.tamanioInstruccion = 0
        
        #print ("Imprimiendo tipo, instruccion", tipo, instruccion)
        
        cadena = bytearray(30) #tamanio propuesto
        
        indice = 0

        self.anexarBytes(cadena, 0, pack('c', self.caracterDeInicio.encode('ascii')))
        self.anexarBytes(cadena, 1, pack('H', 258))
        self.anexarBytes(cadena, 3, pack('H', 1001))
        self.anexarBytes(cadena, 5, pack('<L', self.numeroConsecutivoDeInstruccion))
        self.numeroConsecutivoDeInstruccion +=1
        self.anexarBytes(cadena, 9, pack('H', tipo))
        self.anexarBytes(cadena, 11, pack('H', instruccion))
        
        self.anexarBytes(cadena, 13, pack('H', 0))    # Solo de relleno

        for item in args:
            #print (item)
            for i, item in enumerate(item):
                
                a = pack ('>B', item)
                #print (i, a)
                self.anexarBytes(cadena, 15 + i, a)
        """
        for item, value in kargs:
            print (item, value)
        """

        
        self.anexarBytes(cadena, self.tamanioInstruccion, pack('B', 0)) # Solo de relleno
            


        self.anexarBytes(cadena, self.tamanioInstruccion, pack('c', self.caracterDeFin.encode('ascii')))
        
        self.anexarBytes(cadena, 13, pack('H', self.tamanioInstruccion))
        self.tamanioInstruccion -=2
        
        verificacion = 0
        for i in range (self.tamanioInstruccion-2):
            verificacion ^= cadena[i]
            #print ( (verificacion).to_bytes(1, byteorder='big').hex())
            
        self.anexarBytes(cadena, self.tamanioInstruccion-2, pack('B', verificacion))
        self.tamanioInstruccion -=1
            
        #print ("           ",cadena, len(cadena), self.tamanioInstruccion)
        #print ("           ",cadena[0:self.tamanioInstruccion], len(cadena), self.tamanioInstruccion)
        
        return (cadena[0:self.tamanioInstruccion])
        
    
    def anexarBytes(self, arreglo, indice, a):
        #print ("AnexarBytes", arreglo, a)
        for i in range (len(a)):
            arreglo[indice + i] = a[i]
            self.tamanioInstruccion += 1
            #print ("TamanioInstruccion >>", self.tamanioInstruccion, "<<")
        
        #print ("           ", arreglo, "\n")
        

    def imprimirBuffer (self,instruccion ):
        print (instruccion)
        
    
    

    
def main ():
    comunicacion = Comunicacion ()

    a = comunicacion.crearInstruccion(ADMINISTRACION, MDB_DATOS, [30, 1, 26, 0])
    print (a)
    a = comunicacion.crearInstruccion(ADMINISTRACION, MDB_DATOS, [30, 1, 26, 0])
    print (a)

    
    #comunicacion.crearInstruccion3 (tipo = 3,instruccon = 5)


if __name__ == "__main__":
    main ()
