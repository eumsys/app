#!/usr/bin/python3
'''DL17'''
import base64
import qrcode
from CRC16 import CRC16

class codificar():
    def __init__(self):
        pass

    def codeInfoQR(self, informacion):        
        infoInBytes = bytes( informacion, 'utf-8')
        print(infoInBytes, file=open("InfoInBytes.txt", "a"))
        encoded = base64.b64encode(infoInBytes)
        print(encoded, file=open("InfoCoded.txt", "a"))
        return encoded

    def generarQR(self, infoCoded, expedidoraID, folio ):
        qr = qrcode.make(infoCoded)
        nombre = 'QR_' + str(expedidoraID)+ '_' + str(folio) + '.png' 
        qr.save( nombre )
        print(nombre, file=open("QRFiles.txt", "a"))
        return nombre

    def cleanCharQR( self, ticketQR ):
        limpiaAdmiracion = ticketQR.replace( '¿', '+' )
        limpiaComillas = limpiaAdmiracion.replace( "'", '-' )
        limpiaInterrogacion = limpiaComillas.replace( '¡', '=' )
        ticketQRFinal = limpiaInterrogacion
        print(ticketQRFinal, file=open("infoRead.txt", "a"))
        return ticketQRFinal

    def cleanDotQR( self, ticketQR ):
        limpiaPunto = ticketQR.replace( '.', '' )
        return limpiaPunto

    def decodeInfoQR(self, informacion):
        try:            
            decoded = base64.b64decode(informacion)
            infoInString = str( decoded, 'utf-8')
            print(infoInString, file=open("infoReadCoded.txt", "a"))
            return infoInString
        except:
            return -1

    def validarExist(self, infoIni, infoFin):
        if infoIni == infoFin:
            return True
        else:
            return False
    def validarCR7s(self, CR7, CR72):
        if CR7 == CR72:
            return True
        else:
            return False

    def calcularCR7(self, inFormacion):
        try:            
            strInformacion = str( inFormacion, 'utf-8')
            CR7 = CRC16().calculate(strInformacion)
            return str(CR7)
        except:
            return -1

    def procesamiento(self,informacion):
        try:
            infoTotal = informacion.split(',')
            print(infoTotal[0])
            print(infoTotal[1])
            ticketQRLimpio = self.cleanCharQR( infoTotal[0] )
            numberQRLimpio = self.cleanDotQR( infoTotal[1] )
            CRC2 = self.calcularCR7(bytes(ticketQRLimpio, 'utf-8'))
            ticketDecodificado = self.decodeInfoQR(ticketQRLimpio)
            if(self.validarCR7s(numberQRLimpio, CRC2)):
                return ticketDecodificado
            else:
                return 0
        except:
            return -1
