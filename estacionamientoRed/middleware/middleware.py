import socket
import argparse
import sys
import avisosAyuda as aviso
from threading import Thread
from boleto import Boleto
from persona import Persona
from registroLogs import Log

import time
import datetime

tam_buffer = 200
global mensajeAyuda

class Client(Thread):
    #Servidor echo reenvia lo recibido

    def __init__(self, conn, addr):
        #inicializa la clase padre
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self): 
        try:
            #recibir datos del Cliente
            operacion = self.conn.recv(tam_buffer)
            ###Mensaje 1 de 7
            ##print("--> Operacion: {}".format(operacion))
            if operacion:
                #Confirmacion y separacion de los datos recibidos
                if(operacion == b'registro boleto' or operacion == b'pago boleto' or operacion == b'autorizacion salida'
                   or operacion == b'solicitud de descuento' or operacion == b'descuento a aplicar' or operacion== b'inicio sesion' or operacion == b'log final'
                   or operacion == b'log inicial' or operacion == b'log salida' or operacion == b'log expedidora'):
                    self.conn.send("ack".encode('utf-8'))
                    ###Mensaje 2 de 7
                    #print("operacion: {}".format(operacion))
                    # recibe los datos del obejeto a verificar
                    data = self.conn.recv(tam_buffer)
                    if data:
                        ###Mensaje 3 de 7
                        print("--> Mensaje recibido2****: {}".format(data))
                        # se convierten los datos a string
                        datosCodif = data.decode('utf-8')
                        # Separacion de la cadena recibida, para que sea almacenada en el objeto boleto
                        words = [i for i in str(datosCodif).split(',')]
                        ###Mensaje 4 de 7
                        #print("words: {}".format(words))
                        '''Operaciones que el Middleware puede realizar '''
                        # 1.- Registro de boleto
                        if (operacion == b'registro boleto'):
                            registroBoleto(self, words)

                        # 2.- Pago de boleto
                        if (operacion == b'pago boleto'):
                            pagarBoleto(self, words)

                        # 3.- Autorizacion salida
                        if (operacion == b'autorizacion salida'):
                            autorizacionSalida(self, words)

                        # 4.- solicitud de descuento
                        if (operacion == b'solicitud de descuento'):
                            solicitudDescuento(self, words)

                        # 5.- descuento a aplicar
                        if (operacion == b'descuento a aplicar'):
                            descuentoAplicar(self, words)

                        # 6.- iniciar sesion
                        if (operacion == b'inicio sesion'):
                            inicioSesion(self, words)

                        # 7.- log inicial
                        if (operacion == b'log inicial'):
                            logInicial(self, words)

                        # 8.- log final
                        if (operacion == b'log final'):
                            logFinal(self, words)

                        # 9.- log salida
                        if (operacion == b'log salida'):
                            logSalida(self, words)

                        # 10.- log expedidora
                        if (operacion == b'log expedidora'):
                            logExpedidora(self, words)

                    else:
                        print("\nlos datos del boleto no fueron recibidos")
                        self.conn.send("datos de boleto no recibidos".encode('utf-8'))
                else:
                    self.conn.send("operacion no valida".encode('utf-8'))
                    print("\nla operacion recibida no es valida")

            else:
                print("\nlos datos de la operacion no fueron recibidos")
                self.conn.send("operacion no recibida")

        except self.conn.error:
            print("\n[%s] Error de lectura." % self.name)


def registroBoleto(self, words):
    #(idBoleto,idExpedidora,FechaExpedicion, idestado, idtipodescuento, idSalida)

    boleto = Boleto(int(words[0]), int(words[1]), words[2], int(words[3]), int(words[4]),int(words[5]))
    ###Mensaje 5 de 7
    #print("-->boleto: {}".format(boleto))
    # Se almacena el boleto en la BD
    if (boleto.saveBD()):
        self.conn.send("registro exitoso del pago".encode('utf-8'))
    else:
        self.conn.send("Registro incorrecto".encode('utf-8'))

def solicitudDescuento(self, words):
    boleto = Boleto(int(words[0]), int(words[1]), words[2])
    ###Mensaje 5 de 7
    #print("-->boleto: {}".format(boleto))
    boleto.solicitudDescuento(self)

def pagarBoleto(self, words):
    boleto = Boleto(int(words[0]), int(words[1]), words[2])
    ###Mensaje 5 de 7
    #print("-->boleto: {}".format(boleto))
    boleto.pagoBoleto(self)

def descuentoAplicar(self, words):
    boleto = Boleto(int(words[0]), int(words[1]), words[2], None, words[3])
    ###Mensaje 5 de 7
    #print("-->boleto: {}".format(boleto))
    boleto.descuentoAplicar(self)

def logInicial(self, words):
    global mensajeAyuda
    log = Log(words[0], int(words[1]), int(words[2]), words[3], words[4])
    if(int(words[2])==3):
        aviso.avisoCajero()
        if(int(words[1])==0):
            aviso.cero()
        elif(int(words[1])==1):
            aviso.uno()
        elif(int(words[1])==2):
            aviso.dos()
        elif(int(words[1])==3):
            aviso.tres()
        elif(int(words[1])==4):
            aviso.cuatro()
        elif(int(words[1])==5):
            aviso.cinco()
        elif(int(words[1])==6):
            aviso.seis()
        elif(int(words[1])==7):
            aviso.siete()
        elif(int(words[1])==8):
            aviso.ocho()
        elif(int(words[1])==9):
            aviso.nueve()
    ###Mensaje 5 de 7
    #print("-->log: {}".format(log))
    log.logInicial(self)

def logFinal(self, words):
    global ayuda
    log = Log(words[0], int(words[1]),None,None,None,int(words[2]))
    ###Mensaje 5 de 7
    #print("-->log: {}".format(log))
    log.logFinal(self)

def logSalida(self, words):
    global mensajeAyuda
    log = Log(None, None, int(words[1]), None, None, words[2], None, int(words[0]))
    if(int(words[1])==1):
        aviso.avisoSalida()
        if(int(words[0])==0):
            aviso.cero()
        elif(int(words[0])==1):
            aviso.uno()
        elif(int(words[0])==2):
            aviso.dos()
        elif(int(words[0])==3):
            aviso.tres()
        elif(int(words[0])==4):
            aviso.cuatro()
        elif(int(words[0])==5):
            aviso.cinco()
        elif(int(words[0])==6):
            aviso.seis()
        elif(int(words[0])==7):
            aviso.siete()
        elif(int(words[0])==8):
            aviso.ocho()
        elif(int(words[0])==9):
            aviso.nueve()
    ###Mensaje 5 de 7
    #print("-->log: {}".format(log))
    log.logSalida(self)

def logExpedidora(self, words):
    global mensajeAyuda
    log = Log(None, None, int(words[1]), None, None, words[2], None, None, int(words[0]))
    if(int(words[1])==1):
        aviso.avisoEntrada()
        if(int(words[0])==0):
            aviso.cero()
        elif(int(words[0])==1):
            aviso.uno()
        elif(int(words[0])==2):
            aviso.dos()
        elif(int(words[0])==3):
            aviso.tres()
        elif(int(words[0])==4):
            aviso.cuatro()
        elif(int(words[0])==5):
            aviso.cinco()
        elif(int(words[0])==6):
            aviso.seis()
        elif(int(words[0])==7):
            aviso.siete()
        elif(int(words[0])==8):
            aviso.ocho()
        elif(int(words[0])==9):
            aviso.nueve()

    ###Mensaje 5 de 7
    #print("-->log: {}".format(log))
    log.logExpedidora(self)

def inicioSesion(self, words):
    persona = Persona(None,None,None,None,None,None,None,words[0],words[1])
    ###Mensaje 5 de 7
    #print("-->log: {}".format(persona))
    persona.inicioSesion(self)

def autorizacionSalida(self, words):
    # se llena el objeto boleto
    boleto = Boleto(int(words[0]), int(words[1]), words[2],None ,None , words[3])
    ###Mensaje 5 de 7
    #print("-->boleto: {}".format(boleto))
    # Se verifica que el boleto este registrado en la BD
    boleto.obtieneBoleto(self)

#Metodo principal
def main():
    '''parser = argparse.ArgumentParser(description='Socket Error Examples')
    parser.add_argument('--host', action="store", dest="host", required=True)
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    #Obtencion de los parametros por consola
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port'''
    backlog = 30
    #host = "192.168.1.66"
    host = "192.168.1.65"
    port = 2324


    print("\nPuerto: {} host: {}".format(port,host))
    # Bloque try - catch para crear el socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("\nError al crear el socket: {}".format(e))
        sys.exit(1)

    # Bloque try - catch para reutilizar la dir IP y puerto
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as e:
        print("\nError al reutilizar el Puerto y la dir IP: {}".format(e))

    #Bloque try - catch para publicar el servicio
    try:
        server_address = (host,port)
        s.bind(server_address)
        s.listen(backlog)
        print("Escuchando en el puerto: {}\n".format(port))
    except socket.error as e:
        print("\nError l publicar el servicio: {}".format(e))
        sys.exit(1)

    #Aceptando conexiones
    while True:
        try:
            client,address = s.accept()
            # end connection
            #client.close()
            cliente = Client(client, address)
            cliente.start()
            print("\n%s:%d se ha conectado." % address)
        except Exception as error:
            print(error)

if __name__ == "__main__":
    #main()
    thread1 = Thread(target=main, args=())

    try:
        thread1.start()
    except Exception as e:
        pass

    while (thread1.is_alive()):
        kill = 0
    kill = 1

