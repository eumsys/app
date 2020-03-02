
import sys,os,time

raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
sys.path.append(raiz)
from Comunicacion import Comunicacion
from Variables.Temporizador import Temporizador

class Mei():
    """
    Clase utilizada para comunicarse con el monedero MEI CF7000
    """

    def __init__(self, puerto):

        ESTADO_DESHABILITADO = 0
        ESTADO_HABILITADO = 1

        self.comunicacion = Comunicacion ()
        self.nombre = ""
        self.ser = puerto
        self.cambio = ""
        self.codigo = ""
        self.diferencia = ""
        self.descripcionDiferencia = ""
        self.nivelDeCambio = 0
        self.MONEDAS_HABILITADAS_MDB = [ESTADO_HABILITADO,ESTADO_HABILITADO,ESTADO_HABILITADO,ESTADO_HABILITADO]
        

    

    def darCambio(self,monto):
        TON_01 = Temporizador("dar cambio", 2)
        TON_02 = Temporizador("dar canbio 2", 2)
        self.ser.limpiar()
        #while(1):
        #print("Dar Cambio:")
        global total,cambio
        factorDeEscala = .10
        dar=monto/factorDeEscala
        #print(dar)
        ba = [0x0F, 0x02, int(dar)]
        ckInt = self.checkSum(ba)

        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 2, 0, int(dar), 0, int(ckInt), 0])
        self.ser.write(a);
        time.sleep(.01)
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
        self.ser.write(a);
        time.sleep(.01)
        k = self.ser.read(3)
        
        if(k):
            print(k)
            return k
            if(len(k) >= 2):

                if(k[0]==2 or k[1]==2):
                    print("Comenzando pago..",k)
                    #ESTADO_BILLETERO = 1
                    #break
        else:
            if self.iniciarTemporizador(TON_01):
                pass
                #ESTADO_BILLETERO = 0
                #break

    def darCambio2(self,monto):
        TON_01 = Temporizador("dar cambio", 25)
        TON_02 = Temporizador("dar canbio 2", 25)
        while(1):
            print("NO")
            global total,cambio
            #print(monto)
            dar=monto/factorDeEscala
            print(dar)
            ba = [0x0F, 0x02, int(dar)]
            ckInt = checkSum(ba)
            #print("cambio->", cambio, "check->", ckInt)


            """
            ser.parity = change_parity(0x0F, 1)
            ser.write(b'\x0F')
            ser.parity = change_parity(0x02, 0)
            ser.write(b'\x02')
            ser.parity = change_parity(int(dar), 0)
            ser.write(bytes([int(dar)]))
            ser.parity = change_parity(int(ckInt), 0)
            ser.write(bytes([int(ckInt)]))
            time.sleep(.009)
            ser.parity = change_parity(0x0B, 1)
            ser.write(b'\x0B')
            ser.parity = change_parity(0x0B, 0)
            ser.write(b'\x0B')
            time.sleep(.005)
            """
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
                        #ESTADO_BILLETERO = 1
                        break

    def procesar_cambio(self,cambio):
        while(1):
            if(cambio<=20):
                if(cambio!=0):
                    self.darCambio(cambio)
                    cambio = 0 
                break
            else:
                self.darCambio(20)
                cambio=cambio-20

    def dispensarCambio(self,cambio_solicitado):
            #print("hay cambio")
            
            cambio_dispensado = 0
            time.sleep(1)
            codigo_error = 0
            intentos = 0
            cambio_a_dispensar = cambio_solicitado
            
            for intentos in range(1,3):
                if intentos > 1:
                    print("Error #{0}: Intentando entregar ${1} de cambio".format(str(intentos),str(cambio_solicitado)))
                
                
                cassete_antes = self.estatusTubos()
            
                self.procesar_cambio(cambio_a_dispensar) # Dosifica el cambio en peticiones de maximo 20 pesos
                time.sleep(1) #Tiempo de espera para que monedero recuente sus monedas

                cassete_despues = self.estatusTubos()
                
                cambio_dispensado = self.obtener_cambio_dispensado(cassete_antes,cassete_despues,[1,2,5,10])
                diferencia_en_cambio = cambio_a_dispensar - cambio_dispensado

                print("Diferencia cambio: {} ".format(diferencia_en_cambio))
                if diferencia_en_cambio == 0: 
                    cambio_a_dispensar = diferencia_en_cambio
                    break
                    
                elif diferencia_en_cambio > 0:
                    codigo_error = 11 # Se entrego cambio de menos
                    cambio_a_dispensar = diferencia_en_cambio

                elif diferencia_en_cambio < 0:
                    codigo_error = 12 # Se entrego cambio de mas
                    break


            cambio_total_dispensado = cambio_solicitado - cambio_a_dispensar # Donde cambio_solicitado es el cambio solicitado y cambio_a_dispensar representa el cambio faltante 
            return  cambio_total_dispensado,intentos   # Donde cam

            '''
            print("Diferencia cambio: {}".format(diferencia_en_cambio))
            if diferencia_en_cambio > 0:
                codigo_error = 11 # Se entrego cambio de menos
                cambio = diferencia_en_cambio
            elif diferencia_en_cambio < 0:
                codigo_error = 12 # Se entrego cambio de mas
                break
            else: # Se entrego cambio de mas
                codigo_error = 0
                break
            '''
            #print("Error #{0}: al dispensar cambio".format(codigo_error))
            #return cambio_dispensado,intentos


    
    def obtener_cambio_dispensado(self,cassete_antes,cassete_despues,denominaciones):
        cambio_dispensado = 0
        for i,denominacion in enumerate(denominaciones):
            
            cambio_dispensado =  cambio_dispensado + (cassete_antes[i] - cassete_despues[i])*denominacion
        print("i: ",cambio_dispensado)
        return cambio_dispensado


    def checkSum(self,arr):
        j=0
        sum=0
        tam=arr.__len__()
        while(j<tam):
            #print(j, tam)
            sum=sum+arr[j]
            #print(sum)
            j=j+1	
        return 255&sum

    def iniciarTemporizador(self,TON):
        TON.entrada = True
        TON.actualizar()
        print("tiempo transcurrido: ",TON.tiempoActual,TON.salida,TON.tiempo)
        if TON.salida:
            print("secuencia no completada: ",TON.nombre)
            return True
        else:
            return False


    def estatusTubos(self):
        #ESTATUS TUBOS
        global MONEDAS_POR_SW,suspenderCajero,cajeroSuspendido
        TUBOS = [0,0,0,0]
        TON = Temporizador("estatusTubos", 6)
        while(1):
            TON.actualizar()
            self.ser.limpiar()
            tuboVacio = 0
            time.sleep(.1) #Para completar los 500 ms
            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [10, 1, 10, 0])
            self.ser.write(a);
            time.sleep(.01)
            r = self.ser.read(18) #Verificar en el simulador se ven 19
            #print("estatusTubos",r)
            if(len(r)>8):
                #print("h", r[4],r[5],r[6],r[7],r)
                TUBOS[0] = r[4]
                TUBOS[1] = r[5]
                TUBOS[2] = r[6]
                TUBOS[3] = r[7]



                if (r[0] == 0):  # Verificar la respuesta <----------
                    if(r.__sizeof__()>=30):
                        for i,tubo in enumerate(TUBOS):
                            if tubo == 0 and self.MONEDAS_HABILITADAS_MDB[i] == 1:
                                #print("tubo: ",i,"cantidad:",tubo,"Habilitado:",MONEDAS_HABILITADAS_MDB[i])
                                tuboVacio = 1
                                if(tubo<20):
                                    nivelDeCambio=1
                                if(tubo<10):
                                    nivelDeCambio=1
                                    #suspenderCajero=1

                        #if((r[4] == 0 and MONEDAS_HABILITADAS_MDB[0]) or (r[5] == 0 and MONEDAS_HABILITADAS_MDB[1]) or (r[6] == 0 and MONEDAS_HABILITADAS_MDB[2]) or (r[7] == 0 and MONEDAS_HABILITADAS_MDB[3])):
                        #if tuboVacio:
                        if 0:
                            print("errinfo...")
                            if self.iniciarTemporizador(TON):
                                cajeroSuspendido = 1
                                cs2=0
                                return TUBOS
                            
                            '''
                            suspenderCajero=1
                            if(cajeroSuspendido==1):
                                suspenderCajero=0
                                cs2=0
                                return TUBOS
                            '''


                        else:
                            TON.entrada = 0
                            TON.actualizar()
                            suspenderCajero=0
                            cs2=0
                            cajeroSuspendido=0
                            #print("Estatus de Llenado de Tubo: ", r[0], r[1]) #Verificar si se debe imprimir en Decimal o Ascii
                            #print("TUBOS: ", TUBOS) #Verificar si se debe imprimir en Decimal o Ascii
                            mm1=r[4]
                            mm2=r[5]
                            mm3=r[6]
                            mm4=r[7]

                            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
                            self.ser.write(a);
                            return TUBOS			
                    
            else:
                if self.iniciarTemporizador(TON):
                    cajeroSuspendido = 1
                    return TUBOS

    
    def darCambioManual(self,valor):
        while(1):
            time.sleep(.05)
            print(valor,"<--- aDar")
            ba = [0x0D, int(valor)]
            ckInt = self.checkSum(ba)

            """
            ser.parity = change_parity(0x0D, 1)
            ser.write(b'\x0D')
            ser.parity = change_parity(int(valor), 0)
            ser.write(bytes([int(valor)]))
            ser.parity = change_parity(int(ckInt), 0)
            ser.write(bytes([int(ckInt)]))

            time.sleep(.05)
            ser.parity = change_parity(0x0B, 1)
            ser.write(b'\x0B')
            ser.parity = change_parity(0x0B, 0)
            ser.write(b'\x0B')
            time.sleep(.005)
            """

            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [13, 1, valor, 0, ckInt, 0])
            self.ser.write(a);
            time.sleep(.01)

            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
            self.ser.write(a);
            time.sleep(.01)



            k = self.ser.read(4)
            if(k):
                print(k)
                if(k.__sizeof__()==18):
                    if(k[0]==2):
                        print("insistir",k)
                        break
                if(k.__sizeof__()==19):
                    if(k[0]==2 or k[1]==2):
                        print("insistir",k)
                        break
                if(k.__sizeof__()==20):
                    if(k[0]==2 or k[1]==2 or k[2]==2):
                        print("insistir",k)
                        break
        while(1):
            """
            ser.parity = change_parity(0x0B, 1)
            ser.write(b'\x0B')
            ser.parity = change_parity(0x0B, 0)
            ser.write(b'\x0B')
            time.sleep(.005)
            """
            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
            self.ser.write(a);
            time.sleep(.01)


            k = self.ser.read(3)
            print("poll",k)
            if(k):
                if(k[0]==0):
                    print("roto")
                    time.sleep(.005)
                    break


    def poll(self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
        self.ser.write(a)
        time.sleep(.01)
        k = self.ser.read(3)
        print("poll",k)
        if(k):
            if(k[0]==0):
                print("roto")
                time.sleep(.005)
                

    def inicializar(self):
        self.ser.limpiar()
        while (1):
            #ser.limpiar()
            ##ser.flushInput()
            """
            ser.parity = change_parity(0x08, 1)
            ser.write(b'\x08')
            ser.parity = change_parity(0x08, 0)
            ser.write(b'\x08')
            """
            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [8, 1, 8, 0])
            #ser.escribir(a)
            #time.sleep(0.1)


            self.ser.write(a);
            time.sleep(.01)

            
            r = self.ser.read(1)
            print("RE,",r)
            if(r):
                if (r[0] == 0):
                    break
            
        while (1):
            """
            ser.parity = change_parity(0x0F, 1)
            ser.write(b'\x0F')
            ser.parity = change_parity(0x00, 0)
            ser.write(b'\x00')
            ser.parity = change_parity(0x0F, 0)
            ser.write(b'\x0F')
            """
            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 0, 0, 15, 0])
            self.ser.write(a);
            time.sleep(.1)

            r = self.ser.read(33)  # Verificar en el simulador se ve que devuelve 34
            print(r)
            if (r):
                #print(r[0])
                if (r[0] == 77):  # Verificar la respuesta (4D = M, 45 = E, 49 = I) <----------
                    """
                    ser.parity = change_parity(0x00, 0)
                    ser.write(b'\x00')  # Devuelve ACK
                    """
                    a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
                    self.ser.write(a);
                    time.sleep(.01)

                    #print ("Se llego hasta aqui _ 01")

                    break

        #self.ser.flushInput()
        self.ser.limpiar()
        self.disable_coin()
        cont=0
        while(1):
            """
            ser.parity = change_parity(0x0F, 1)
            ser.write(b'\x0F')
            ser.parity = change_parity(0x05, 0)
            ser.write(b'\x05')
            ser.parity = change_parity(0x14, 0)
            ser.write(b'\x14')
            """
            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 5, 0, 20, 0])
            self.ser.write(a);
            time.sleep(.01)


            #time.sleep(.02)
            r = self.ser.read(2)
            if(r):
                print("rrrrr__:",r)
                if(cont==2):
                    print("LISTO!---")
                    break
                else:
                    cont=cont+1
                    print("DESHINIBIENDO!---",cont)
                    self.enable_coin()
                    time.sleep(2)


    def enable_coin(self):
        global mona,mond
        mona=60
        mond=60
        ba = [0x0C, mona, mond]
        ckInt = self.checkSum(ba)
        print("vals...>>>",mona,mond,ckInt)
        #time.sleep(1)
        while (1):
            #print("asdddd")
            """
            ser.parity = change_parity(0x0C, 1)
            ser.write(b'\x0C')
            ser.parity = change_parity(0x00, 0)
            ser.write(b'\x00')
            ser.parity = change_parity(mona, 0)
            ser.write(bytes([int(mona)]))
            ser.parity = change_parity(0x00, 0)
            ser.write(b'\x00')
            ser.parity = change_parity(mond, 0)
            ser.write(bytes([int(mond)]))
            ser.parity = change_parity(ckInt, 0)
            ser.write(bytes([int(ckInt)]))
            """

            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [12, 1, 0, 0, mona, 0, 0, 0, mond, 0, ckInt, 0])
            self.ser.write(a);
            time.sleep(.01)



            #time.sleep(.05)
            r = self.ser.read(1)
            print(r)

            #print ("Se llego hasta aqui _ 03")
            if(r):
                if (r[0] == 0):  # Verificar la respuesta <----------
                    print("Habilitacion de Monedas Exitosa")
                    time.sleep(.005)
                    return r
                    break


    def disable_coin(self):

        while (1):
            #print("asdddd")
            """
            ser.parity = change_parity(0x0C, 1)
            ser.write(b'\x0C')
            ser.parity = change_parity(0x00, 0)
            ser.write(b'\x00')
            ser.parity = change_parity(0x00, 0)
            ser.write(b'\x00')
            ser.parity = change_parity(0x00, 0)
            ser.write(b'\x00')
            ser.parity = change_parity(0x00, 0)
            ser.write(b'\x00')
            ser.parity = change_parity(0x0C, 0)
            ser.write(b'\x0C')
            """
            print("Deshabilitando Monedero...")
            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [12, 1, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0])
            #ser.close();
            #exit(0)
            self.ser.write(a);
            time.sleep(.01)
            r = self.ser.read(1)


            print(r)

            #print ("Se llego hasta aqui _ 02")
            if(r):
                if (r[0] == 0):  # Verificar la respuesta <----------
                    print("Deshabilitacion de Monedas Exitosa")
                    time.sleep(.005)
                    break