'''from crccheck.crc import CrcKermit


# Procsss multiple data buffers
data2 = bytes.fromhex("FC0511")  # Python 3 only, use bytearray for older versi$
crcinst = CrcKermit()
crcinst.process(data2)
crchex = crcinst.finalhex()


crchex_l = crchex[2:] 
crchex_h = crchex[:2] 

print("Dec: ",int(crchex_l,16),int(crchex_h,16))
print("Hex: ",crchex_l,crchex_h)



'''
##-------------------------


class CRC():
    def __init__(self,numeros):
        self.numeroInicial = 0
        self.sumar(numeros)
        
    def sumar(self,numeros):
        #print (numero, self.numeroInicial>>1 )
       	for numero in numeros: 
	        for i in range (8):
	            bit =  (numero>>i)&1^self.numeroInicial&1
	            #print (bit, end=" ")
	            self.numeroInicial = (self.numeroInicial>>1)^bit<<15^bit<<10^bit<<3

    
    def imprimirNumero(self):
        print ("{0:b}".format(self.numeroInicial).rjust( 16 ), hex(self.numeroInicial) )

    def crc_l(self):
            return int(hex(self.numeroInicial)[2:][2:],16)

    def crc_h(self):
            return int(hex(self.numeroInicial)[2:][:2],16)

    def obtenerNumero(self):
    	if byte == 1:
    		return hex(self.numeroInicial)[2:][:2]
    	elif byte == 2:
    		return hex(self.numeroInicial)[2:][2:]
    	else:
    		return False
 
def main ():
    prueba = CheckSum3()


   #prueba.sumar([252,5,17])

    #REQUEST SOFTWARE VERSION
    #prueba.sumar([252,7,240,32,147]) # a2 b6 / 162 182
    #UNIT
    prueba.sumar([252,5,146]) # b4 e0 / 180 224
    #prueba.sumar(5)
    #prueba.sumar(17)
    #prueba.imprimirNumero()
    crc_h = prueba.obtenerNumero(1)
    crc_l = prueba.obtenerNumero(2)
    print(crc_l,crc_h,int(crc_l,16),int(crc_h,16))

    
if __name__ == "__main__":
    #main()
    pass


##-------------------------