

import requests
import json,os,sys,time
from datetime import datetime


#from urllib.request import urlopen



raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(raiz)

class Hopper():
    """
    Clase utilizada para guardar los datos 
    en caso un intento de conexion fallido
    """
    def __init__(self):
        self.nombre = ""
        self.cambio = ""
        self.codigo = ""
        self.diferencia = ""
        self.descripcionDiferencia = ""


class Dispensador():
    """
    Clase utilizada para guardar los datos 
    en caso un intento de conexion fallido
    """

    HOPPER = "USB2.0-Serial"
    MEI = "USB-Serial Controller"
    JCM = "Arduino Micro"

    DIC_DISPOSITIVOS = {"ARDUINO_NANO": "USB2.0-Serial", "ADAPTADOR": "USB-Serial Controller", "ARDUINO_MICRO" : "Arduino Micro"}


    def __init__(self,nombre,denominaciones):
        self.nombre = nombre
        self.denominaciones = denominaciones



    def get_nombre(self):
        return self.nombre
    def establecerDispositivo(self):
        return 0


    def dispensarCambio(self,cambio):
        if self.nombre == HOPPER: 
            self.dispensarHopper(cambio)
        if self.nombre == MEI: 
            self.dispensarMei(cambio)
        if self.nombre == JCM: 
            self.dispensarJcm(cambio)




    def dispensarMei(cambioSolicitado):
        intento = 0
        diferenciaCambio = 0
        aux_cambio = cambioSolicitado
        for intento in range(2):
            if intento > 0 :
                disable_sequence(ser)
                MONEDAS_TMP = estatusTubos(ser)
                #print("Monedas previo al cambio: ",MONEDAS_TMP)
                while(1):
                    if(cambio<=20):
                        #pagado=1
                        if(cambio!=0):
                            darCambio(ser,cambio)
                        killbill = 1
                        break
                    else:
                        darCambio(ser,20)
                        cambio=cambio-20
                MONEDAS_POR_HW = estatusTubos(ser)

                MONEDAS_TMP[0] = MONEDAS_TMP[0] - MONEDAS_POR_HW[0]
                MONEDAS_TMP[1] = MONEDAS_TMP[1] - MONEDAS_POR_HW[1]
                MONEDAS_TMP[2] = MONEDAS_TMP[2] - MONEDAS_POR_HW[2]
                MONEDAS_TMP[3] = MONEDAS_TMP[3] - MONEDAS_POR_HW[3]
                
                #print("Monedas dispensadas como cambio: ",MONEDAS_TMP)
                monedasCambio = MONEDAS_TMP
                diferenciaCambio = compararCambio(monedasCambio,aux_cambio)
                if diferenciaCambio:
                    intento = intento + 1
                else:
                    return diferenciaCambio
            else:
                return diferenciaCambio

            

    def dispensarHopper(cambioSolicitado):
        cambioEntregado10 = 0
        cambioEntregado5 = 0
        cambioEntregado1 = 0
        monedasDispensadas = 0
        estatus = 0
        
        HOPPER_MONEDAS_SOLICITADAS = {10:0,5:0,1:0}
        HOPPER_MONEDAS_DISPENSADAS = {10:0,5:0,1:0}
        #MONEDAS = [10,5,1]
        MONEDAS = [10,5]
        
        cambioRestante = cambioSolicitado
        #MONEDAS = HOPPER_MONEDAS_HABILITADAS_HOPPER.keys()
        i = 0
        print("------------- Cambio Solicitado: ",cambioSolicitado,"-------------------")
        for moneda in MONEDAS:
            repeticiones = MONEDAS.count(moneda)
            i = i +1 
            #print("reps: ",repeticiones, "iteracion: ", i)
            if(repeticiones > 2):

                #count(ser)
                break
                #exit(0)
                pass
            
            
            #print("Cambio Solicitado: ",cambioSolicitado)
            #print(moneda,cambio)
            cambio = int(cambioSolicitado/moneda)
            if(cambio):
                cambioSolicitado = cambioSolicitado%moneda
                print("\nMonedas solicitadas de ",moneda,": ",cambio)
                codigoCambio = cambioHopper(cambio,HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
                dispensandoCambio = 1
                #time.sleep(1)
                
                if codigoCambio == [0]:
                    while(dispensandoCambio):
                        time.sleep(.3)
                        estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
                        if estatus:
                            if estatus[1]:
                                #cambioRestante = (estatus[1]*moneda)+cambioSolicitado
                                print("*Entrgando Cambio*",(estatus[1]*moneda)+cambioSolicitado,"Restante")
                            else:
                                dispensandoCambio = 0
                    if estatus:
                        if estatus[0]:
                            monedasPorPagar = estatus[1]
                            monedasDispensadas = estatus[2]
                            monedasFaltantes = estatus[3]
                            if monedasFaltantes:
                                MONEDAS.append(moneda)
                                cambioSolicitado = cambioSolicitado + (monedasFaltantes*moneda)
                                #print("monedas por pagar de ",moneda,": ",monedasPorPagar)
                                print("monedas enrtegadas de ",moneda,": ",monedasDispensadas)
                                #HOPPER_MONEDAS_DISPENSADAS.update({moneda:monedasDispensadas})

                                cambioRestante = cambioRestante - (monedasDispensadas*moneda)
                                print("Cambio incompleto , faltan ",monedasFaltantes," de $",moneda, "Restante: ",cambioRestante)
                                resetHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
                                habilitarHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
                            else:
                                #print("monedas pendientes en el pago de ",moneda,": ",monedasDispensadas)
                                cambioRestante = cambioRestante - (monedasDispensadas*moneda)
                                print("monedas enrtegadas de ",moneda,": ",monedasDispensadas)
                                #HOPPER_MONEDAS_DISPENSADAS.update({moneda:monedasDispensadas})

                                print("monedas faltantes: ",monedasFaltantes," monedas",MONEDAS,"Cambio Restante:",cambioRestante)
                                #HOPPER_MONEDAS_DISPENSADAS.update({})

                        else: 
                            print("Hopper ",HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda],"No puede dar cambio: Deshabilitado")

                    else:
                        print("No se pudo obtener el status")
                else:
                        resetHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
                        habilitarHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
                        print("No se entrego el cambio, Hopper",HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda],"Deshabilitado,","Faltaron",cambio,"monedas de $",moneda)
                        #cambioRestante = cambioRestante+(cambio*moneda)
                print("Cambio restante...: ",cambioRestante)  
        print("Cambio restante: ",cambioRestante)
        return cambioRestante

    def dispensarCambioMei():
        return 0
    
    def dispensarCambioHopper():
        return 0

    def dispensarCambioJCM():
        return 0


    def darCambio(ser,monto):
        TON_01 = Temporizador("dar cambio", 25)
        TON_02 = Temporizador("dar canbio 2", 25)
        while(1):
            print("NO")
            global total,cambio
            dar=monto/factorDeEscala
            print(dar)
            ba = [0x0F, 0x02, int(dar)]
            ckInt = checkSum(ba)

            a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 2, 0, int(dar), 0, int(ckInt), 0])
            ser.write(a);
            time.sleep(.01)
            a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
            ser.write(a);
            time.sleep(.01)
            k = ser.read(3)
            if(k):
                print(k)
                if(len(k) >= 2):
                    if(k[0]==2 or k[1]==2):
                        print("Comenzando pago..",k)
                        break
                    else:
                        if iniciarTemporizador(TON_01):
                            #ESTADO_BILLETERO = 0
                            break
            else:
                if iniciarTemporizador(TON_01):
                    #ESTADO_BILLETERO = 0
                    break


        while(1):
            """
            ser.parity = change_parity(0x0B, 1)
            ser.write(b'\x0B')
            ser.parity = change_parity(0x0B, 0)
            ser.write(b'\x0B')
            time.sleep(.005)
            """

            a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
            ser.write(a);
            time.sleep(.01)

            k = ser.read(6)
            print("poLL",k)
            if(k):
                if(k[0]!=2):
                    palPoll(ser,k[0], k)
                    if(k[0]==0):
                        print("roto")
                        time.sleep(.005)
                        break
                    else:
                        #ser.flushOutput()
                        #ser.flushInput()
                        print("Error al finalizar el pago...")

                        a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
                        ser.write(a);
                        time.sleep(.01)
                        if iniciarTemporizador(TON_02):
                            #ESTADO_BILLETERO = ESTADO_DESHABILITADO
                            break
                        
            else:
                if iniciarTemporizador(TON_02):
                    #ESTADO_BILLETERO = ESTADO_DESHABILITADO
                    break



                #if(k[0]==0):
                #	break;
    def compararCambio(cambioEntregado,cambioSolicitado):
        valorCambio=0
        i=-1
        if(cambioEntregado[0]==0 and cambioEntregado[1]==0 and cambioEntregado[2]==0 and cambioEntregado[3]==0):
            valorCambio=0
        else:
            for item in cambioEntregado:
                i=i+1
                if(item!=0):
                    valorCambio=valorCambio+(item*valoresMonedas[i])
                    
        print("comparativa cambio solicitado/entregado: ", cambioSolicitado,valorCambio)
        return cambioSolicitado - valorCambio

        