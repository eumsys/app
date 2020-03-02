
import sys
import socket
import argparse
from datetime import datetime, date, time
import os

tam_buffer = 150

def autorizaSalida(s, operacion, mensaje):
    # operacion de salida del automovil
    s.send(operacion.encode('utf-8'))
    # espera una trama de confirmacion
    if (s.recv(tam_buffer) == b'ack'):
        # Protocolo de comunicacion (idBoleto, idexpedidora, fecha boleto)
        s.send(mensaje.encode('utf-8'))
        #espera la respuesta de autorizacion de salida
        data = s.recv(tam_buffer)
        if (data != b'boleto no localizado'):
            datosDecoded = data.decode('utf-8')
            print("data: {}".format(datosDecoded))
            if(datosDecoded == "salida no autorizada: boleto no pagado"):
                ##### Aqui va mensaje hacial el cliente indicando que realice el pago
                print("Favor de realizar su pago")
            elif(datosDecoded == "salida autorizada: boleto pagado"):
                ##### Aqui va mensaje hacia el cliente indicando que puede salir
                print("Gracias por su visita")
            elif(datosDecoded == "salida no autorizada: tiempo de salida excedido"):
                ##### Aqui va mensaje hacia el cliente indicando que el tiempo de salida se agoto, por lo tanto requiere volver a pagar
                print("Tiempo de salida excedido, favor de pagar")
            elif (datosDecoded == "salida no autorizada: boleto obsoleto"):
                ##### Aqui va mensaje hacia el cliente indicando que el tiempo de salida se agoto, por lo tanto requiere volver a pagar
                print("salida no autorizada, boleto obsoleto")
                
            else:
                print("Pago no realizado, favor de realizar su pago")
        else:
            print("Boleto sin Pago o Boleto No encontrado ")
    else:
        print("NO se entrego la operacion")
        s.close()

def registroBoleto(s,operacion,mensaje):
    #operacion de registro de boleto desde la expedidora
    s.send(operacion.encode('utf-8'))
    # Espera una trama de confirmacion
    if(s.recv(tam_buffer) == b'ack'):
        #Realiza el envio de los datos del boleto a buscar
        s.send(mensaje.encode('utf-8'))
        if(s.recv(tam_buffer) == b'registro exitoso del pago'):
            print("Registro Exitoso")
        else:
            print("Registro Incorrecto")
    else:
        print("NO se entrego la operacion")
    s.close()

def solicitudDescuento(s,operacion,mensaje):
    # operacion de pago de boleto
    s.send(operacion.encode('utf-8'))
    # espera una trama de confirmacion
    if (s.recv(tam_buffer) == b'ack'):
        # hace el envio del boleto a localizar
        s.send(mensaje.encode('utf-8'))
        data = s.recv(tam_buffer)
        print("data: {}".format(data))
        if (data != b'boleto no localizado'):
            print("--> datos recibidos: {}".format(data))
            # se convierten los datos a string
            datosCodif = data.decode('utf-8')
            # Separacion de la cadena recibida, para que sea almacenada en el objeto boleto
            words = [i for i in str(datosCodif).split(',')]
            print("words: {}".format(words))
            ret = True
        else:
            print(data)
            ret = False
    else:
        print(data)
        ret = False

    if ret:
        print("retorno words")
        return words

    else:
        print("retorno None")
        return None

    s.close()

def pagoBoleto(s,operacion,mensaje):
    #operacion de pago de boleto
    s.send(operacion.encode('utf-8'))
    # espera una trama de confirmacion
    if(s.recv(tam_buffer) == b'ack'):
        #hace el envio del boleto a localizar
        s.send(mensaje.encode('utf-8'))
        data = s.recv(tam_buffer)
        print("data: {}".format(data))
        if (data != b'boleto no localizado') :
            print("--> datos recibidos: {}".format(data))
            #idcaj,mediopago,monto, descripcion de las monedas pagadas, descripcion de los billetes pagados, tarifas implementadas
            s.send("1;1;20.00;2:5,1:10;0:0;2,5".encode('utf-8'))

            #se recibe la respuesta final del registro del boleto
            data = s.recv(tam_buffer)
            if(data == b'registro exitoso del pago'):
                print("El Pago del boleto se registro de manera correcta")
            else:
                print("El pago del boleto NO se registro de manera correcta")
        else:
            print("Datos: tipo, estado y fecha No recibidos")
    else:
        print("NO se entrego la operacion")
    s.close()

def descuentoAplicar(s,operacion,mensaje):
    # operacion de registro de boleto desde la expedidora
    s.send(operacion.encode('utf-8'))
    # Espera una trama de confirmacion
    if (s.recv(tam_buffer) == b'ack'):
        # Realiza el envio de los datos del boleto a buscar
        s.send(mensaje.encode('utf-8'))
        data = s.recv(tam_buffer)
        if (data == b'Descuento aplicado'):
            print("Registro de Descuento Exitoso")
        else:
            print("Registro de Descuento Incorrecto")
            print(data)
    else:
        print("NO se entrego la operacion")
    s.close()

def inicioSesion(s,operacion,mensaje):
    # operacion de inicio de sesion
    s.send(operacion.encode('utf-8'))
    # Espera una trama de confirmacion
    if (s.recv(tam_buffer) == b'ack'):
        # Realiza el envio de los datos del boleto a buscar
        s.send(mensaje.encode('utf-8'))
        data = s.recv(tam_buffer)
        if (data != b'usuario y/o password incorrectas'):
            print("Incio de sesion exitoso")
        else:
            print("Incio de sesion incorrecto:")
            print(data)
    else:
        print("NO se entrego la operacion")
    s.close()

def logInicial(s,operacion,mensaje):
    # operacion de inicio de sesion
    s.send(operacion.encode('utf-8'))
    # Espera una trama de confirmacion
    if (s.recv(tam_buffer) == b'ack'):
        # Realiza el envio de los datos del boleto a buscar
        s.send(mensaje.encode('utf-8'))
        data = s.recv(tam_buffer)
        print(data)
        #separar los datos
        #if (data != b'inicio_log registrado):
        if (data == b'inicio_log registrado'):
            print("Incicio log registrado")
        else:
            print("Error en el inicio log:")
            print(data)
    else:
        print("NO se entrego la operacion")
    s.close()

def logFinal(s,operacion,mensaje):
    # operacion de inicio de sesion
    s.send(operacion.encode('utf-8'))
    # Espera una trama de confirmacion
    if (s.recv(tam_buffer) == b'ack'):
        # Realiza el envio de los datos del boleto a buscar
        s.send(mensaje.encode('utf-8'))
        data = s.recv(tam_buffer)
        print(data)
        if (data == b'fin_log registrado'):
            print("Fin_log registrado")
        else:
            print("Error en registro log:")
            print(data)
    else:
        print("NO se entrego la operacion")
    s.close()

def logSalida(s,operacion,mensaje):
    # operacion de inicio de sesion
    s.send(operacion.encode('utf-8'))
    # Espera una trama de confirmacion
    if (s.recv(tam_buffer) == b'ack'):
        # Realiza el envio de los datos del boleto a buscar
        s.send(mensaje.encode('utf-8'))
        data = s.recv(tam_buffer)
        print(data)
        if (data == b'log salida registrado'):
            print("Fin_log registrado")
        else:
            print("Error en registro log:")
            print(data)
    else:
        print("NO se entrego la operacion")
    s.close()

def logExpedidora(s,operacion,mensaje):
    # operacion de inicio de sesion
    s.send(operacion.encode('utf-8'))
    # Espera una trama de confirmacion
    if (s.recv(tam_buffer) == b'ack'):
        # Realiza el envio de los datos del boleto a buscar
        s.send(mensaje.encode('utf-8'))
        data = s.recv(tam_buffer)
        print(data)
        if (data == b'log expedidora registrado'):
            print("Fin_log registrado")
        else:
            print("Error en registro log:")
            print(data)
    else:
        print("NO se entrego la operacion")
    s.close()

def menu():
    os.system('clear')
    print("Selecciona una opción")
    print("\t1 - Expedicion de Boleto")
    print("\t2 - Pago de Boleto")
    print("\t3 - Autorizacion de Salida")
    print("\t4 - Solicitud Descuento")
    print("\t5 - Descuento a aplicar")
    print("\t6 - Inicio de sesion")
    print("\t7 - Log inicial")
    print("\t8 - Log final")
    print("\t9 - Log salida")
    print("\t10- Log expedidora")
    #print("\t9 - salir")



def configSocket():
    #Parseo de argumentos, identifico que se tiene que pasar 2 parametros por consola host:127.0.0.1 puerto: 1234
    '''parser = argparse.ArgumentParser(description='Socket Error Examples')
    parser.add_argument('--host', action="store", dest="host", required=True)
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port'''
    host = "192.168.1.70"
    port = 2324

    # Bloque try - catch para crear el socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Error al crear el socket: {}".format(e))
        sys.exit(1)

    # Bloque try - catch para conectarse al servidor
    try:
        conn = s.connect((host,port))
        print("Conexion al host: {} en el puerto: {}".format(host,port))
        print("--> conn {}".format(conn))
    except socket.gaierror as e:
        print("Error al conectar con el servidor: {}".format(e))
        sys.exit(1)
    except socket.error as e:
        print("Error de Conexion: {}".format(e))
        sys.exit(1)

    #Bloque try - catch para la recepcion de datos
    try:

        #Se muestra el menu
        menu()

        #se solicita una opcion al usuario
        opcionMenu = input("Selecciona una opcion >> ")
        if opcionMenu=="1":
            ''' Operacion 1.- Registro de boleto'''
            #convierte un datetime en un string
            fechaActual = datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')
            #mensaje = (idBoleto,idExpedidora,FechaExpedicion, idestado, idtipodescuento, idSalida)
            mensaje = str(1) + "," + str(1) + "," + fechaActual + "," + str(1) + "," + str(0) + "," + str(0)
            registroBoleto(s,"registro boleto", mensaje)
        elif opcionMenu == "2":
            '''Operacion 2.- Pago de Boleto'''
            # mensaje = (idBoleto, idexpedidora, fecha boleto)
            mensaje = str(1) + "," + str(1) + "," + '2017-07-27 21:35:35'
            pagoBoleto(s, "pago boleto", mensaje)
        elif opcionMenu=="3":
            ''' Operacion 1.- Autorizacion de salida'''
            #mensaje = (idBoleto,idExpedidora,fechaExpedicion, idSalida)
            mensaje = str(1) + "," + str(1) + "," + '2017-07-27 20:04:26' + "," + str(1)
            autorizaSalida(s, "autorizacion salida", mensaje)
            # Finalizada la operacion se cierra la comunicacion con el servidor
        elif opcionMenu =="4":
            #solicitud de descuento(idBoleto, idExpedidora, fechaExpedicion)s
            mensaje = str(1) + "," + str(1) + "," + '2017-07-27 01:08:11'
            solicitudDescuento(s, "solicitud de descuento", mensaje)

        elif opcionMenu =="5":
            #asigna el tipo de descuento
            mensaje = str(1) + "," + str(1) + "," + '2017-07-27 01:27:45' + "," + str(1)
            descuentoAplicar(s, "descuento a aplicar", mensaje)

        elif opcionMenu =="6":
            #busca al usuario inicio de sesion
            mensaje = "1234" + "," + "1235"
            inicioSesion(s, "inicio sesion", mensaje)

        elif opcionMenu =="7":
            #log inicial
            #mensaje = idUsuario + idCajero + idTipoMantenimiento + inicioMonedasMonedero + inicioBilletesBilletero {atributos Log}
            #mensaje = idpersona + idcaj + idtipo + monedas_previas + billetes_previas {columnas BD}
            mensaje = "turnom@gmail.com" + "," + "1" + "," + "1" + "," + "0:0" + "," + "0:0"
            logInicial(s, "log inicial", mensaje)

        elif opcionMenu =="8":
            #log final
            #mensaje = "turnom@gmail.com" + "," + "1" + "," + "1" + "," + "Esta es una descripcion final de pueba"(Esta descripcion no la manda el cajero; la manda el servidor)
            #mensaje = idUsuario + idCajero + edoOperacion {atributos Log}
            #mensaje = idpersona + idcaj + idestado {columnas BD}
            mensaje = "turnom@gmail.com" + "," + "1" + "," + "1"

            logFinal(s, "log final", mensaje)

        elif opcionMenu =="9":
            #log final
            #mensaje = idSalida + idTipoMantenimiento + edoOperacion {atributos Log}
            #mensaje = idsalida + idtipo + estado_operacion {columnas BD}
            mensaje = "5" + "," + "1" + "," + "estadoPruebaSal"
            logSalida(s, "log salida", mensaje)

        elif opcionMenu =="10":
            #log final
            #mensaje = idExpedidora + idTipoMantenimiento + edoOperacion {atributos Log}
            #mensaje = idexpedidora + idtipo + estado_operacion {columnas BD}
            mensaje = "5" + "," + "1" + "," + "estadoPruebaExp"
            logExpedidora(s, "log expedidora", mensaje)

    except socket.error as e:
        print("Error zona de comunicacion: {}".format(e))
        sys.exit(1)
    finally:
        s.close()

configSocket()