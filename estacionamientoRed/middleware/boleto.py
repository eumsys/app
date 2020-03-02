import psycopg2
from datetime import datetime
import time
import math

tam_buffer = 200
tiempoSalida = 15
class Boleto:

    #Constructor del objeto boleto
    def __init__(self, idBoleto = None,idExpedidora = None, fechaExpedicion = None, idEstado = None, idTipoDescuento = None, idSalida = None, idCaj = None, medioPago = None, monto = None, monedas = None, billetes = None, fechaPago = None, idPago = None, cambio = None):
        self.idBoleto = idBoleto
        self.idExpedidora = idExpedidora
        self.fechaExpedicion = fechaExpedicion
        self.idEstado = idEstado
        self.idTipoDescuento = idTipoDescuento
        self.idSalida = idSalida
        self.idCaj = idCaj
        self.medioPago = medioPago
        self.monto = monto
        self.monedas = monedas
        self.billetes = billetes
        self.fechaPago = fechaPago
        self.idPago = idPago
        self.cambio = cambio

    def __repr__(self):
        return "idBoleto:{}, idExpedidora:{}, fechaExpedicion:{}, idEstado:{}, idTipoDescuento:{}, idSalida:{}, idCaj:{}, medioPago:{}, monto:{}, monedas:{}, billetes:{}, cambio:{}, fechaPago:{}, idPago:{}".format(self.idBoleto,self.idExpedidora, self.fechaExpedicion, self.idEstado, self.idTipoDescuento, self.idSalida, self.idCaj, self.medioPago, self.monto, self.monedas, self.billetes, self.cambio, self.fechaPago, self.idPago)

    def saveBD(self):
        try:
            connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac', host='localhost')
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO boleto (idboleto, idexpedidora, fechaexpedicion, idestado, idtipodescuento,idsalida) VALUES ( %s, %s, %s, %s, %s, %s)',
                    (self.idBoleto, self.idExpedidora, self.fechaExpedicion, self.idEstado, self.idTipoDescuento, self.idSalida))
                #cursor.execute('INSERT INTO pagos (idcaj,idboleto, idexpedidora, fechaexpedicion, mediopago, monto, monedas, billetes, fechapago) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)  RETURNING idpago;', (self.idCaj, self.idBoleto, self.idExpedidora, self.fechaExpedicion, self.medioPago, self.monto, self.monedas, self.billetes, self.fechaPago))
                #idPago = cursor.fetchall()[0]
                #print("idPago: {}".format(idPago))
                #cursor.execute('INSERT INTO tarifaaplicada (idpago,idtarifa) VALUES (%s, %s);', (idPago, self.idTarifa))
            connection.commit()
            connection.close()
            print("Boleto Insertado con id:{} por la expedidora:{} con fecha:{}, estado:{}, descuento:{} y salida:{}\n".format
            	(self.idBoleto, self.idExpedidora, self.fechaExpedicion, self.idEstado, self.idTipoDescuento, self.idSalida))
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print("Exception: saveBD\n")
            print(error)
            connection.close()
            return False
        finally:
            if connection is not None:
                connection.close()

    def obtieneBoleto(self, canal):
        try:
            connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac',
                                          host='localhost')

            #print("Busqueda: {} {} {}".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
            with connection.cursor() as cursor:
                cursor.execute(
                    ' SELECT B.fechaexpedicion, B.idestado, P.fechapago, P.idpago FROM boleto B INNER JOIN pagos P ON  B.idboleto = P.idboleto and B.idexpedidora = P.idexpedidora and B.fechaexpedicion = P.fechaexpedicion AND idpago IN (SELECT MAX(idpago) from pagos WHERE pagos.idboleto = %s and pagos.idexpedidora = %s and pagos.fechaexpedicion = %s);',(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                row = cursor.fetchone()
                if row is not None:
                    #print("columns: {}, {}, {}".format(row[0], row[1], row[2]))

                    # Se obtiene el estado del boleto en la BD
                    if (row[1] == 1):
                        #print("Estado 1")
                        canal.conn.send("salida no autorizada: boleto no pagado".encode('utf-8'))
                        print("\nSalida No autorizada para el boleto: {} {} {}. Boleto NO Pagado".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                    elif (row[1] == 2):
                        #print("Estado 2")
                        autoriza = calcularTiempoSalida(row[2].strftime("%Y-%m-%d %H:%M:%S"))
                        #print("autoriza: {}".format(autoriza))
                        if autoriza < 900:
                            cursor.execute(
                                'UPDATE boleto SET idestado = %s, idsalida = %s WHERE idboleto = %s and idexpedidora = %s and fechaexpedicion = %s',
                                (4, self.idSalida, self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                            #canal.conn.send(("salida autorizada: boleto pagado" + "," + str(row[2])).encode('utf-8'))
                            canal.conn.send("salida autorizada: boleto pagado".encode('utf-8'))
                            print("\nSalida autorizada para el boleto: {} {} {}. Boleto Pagado".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                        else:
                            cursor.execute('UPDATE boleto SET idestado = %s WHERE idboleto = %s and idexpedidora = %s and fechaexpedicion = %s', (3, self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                            canal.conn.send("salida no autorizada: tiempo de salida excedido".encode('utf-8'))
                            print("\nSalida No autorizada para el boleto: {} {} {}. Tiempo de salida Excedido".format(self.idBoleto,
                                                                                                         self.idExpedidora,
                                                                                                         self.fechaExpedicion))
                    elif (row[1] == 3):
                        canal.conn.send("salida no autorizada: tiempo de salida excedido".encode('utf-8'))
                        print("\nSalida No autorizada para el boleto: {} {} {}. Tiempo de Salida excedido".format(self.idBoleto,
                                                                                                       self.idExpedidora,
                                                                                                       self.fechaExpedicion))
                    elif (row[1] == 4):
                        canal.conn.send("Salida no autorizada: boleto obsoleto".encode('utf-8'))
                        print("\nSalida No autorizada para el boleto: {} {} {}. Boleto Obsoleto".format(self.idBoleto,
                                                                                                   self.idExpedidora,
                                                                                                   self.fechaExpedicion))

                    #Se aplican los cambios a la BD y se cierra la conexion
                    connection.commit()
                    connection.close()
                else:
                    print("\nNo se encontro el boleto o aun no ha sido pagado")
                    canal.conn.send("boleto no localizado".encode('utf-8'))
        except (Exception) as error:
            print("\nException: ObtieneBoleto")
            print(error)
            connection.close()

        finally:
            if connection is not None:
                connection.close()

    def updateBD(self):
        try:
            connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac',
                                          host='localhost')
            with connection.cursor() as cursor:
                cursor.execute('UPDATE boleto SET idestado = %s, idsalida = %s WHERE idboleto = %s and idexpedidora = %s and fechaexpedicion = %s',(self.idEstado, self.idSalida, self.idBoleto, self.idExpedidora, self.fechaExpedicion))

            connection.commit()
            connection.close()
            print("\nEstado del boleto {} {} {} actualizado a:{}".format
				(self.idSalida, self.idBoleto, self.idExpedidora, self.fechaExpedicion, self.idEstado))
        except (Exception, psycopg2.DatabaseError) as error:
            print("\nException: updateBD")
            print(error)
            connection.close()
        finally:
            if connection is not None:
                connection.close()

    def descuentoAplicar(self, canal):
        try:
            connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac',
                                          host='localhost')
            with connection.cursor() as cursor:
                #print("Busqueda: {} {} {}".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                # Se comprueba la existencia del boleto y se recuperan sus datos, y el ultimo pago realizado
                cursor.execute(
                    'SELECT  B.idtipodescuento, B.idestado, B.fechaexpedicion FROM boleto B WHERE B.idboleto = %s and B.idexpedidora = %s and B.fechaexpedicion = %s;',
                    (self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                row = cursor.fetchone()
                if row is not None:
                    #print("columns: {}, {}, {}".format(row[0], row[1], row[2]))
                    #si el id del descuento o el el estado
                    if((row[0] == 1) and (row[1] == 1)):
                        # Se cambia el estado del boleto a pagado (2)
                        cursor.execute(
                        'UPDATE boleto SET idtipodescuento = %s WHERE idboleto = %s and idexpedidora = %s and fechaexpedicion = %s',
                        (self.idTipoDescuento, self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                        connection.commit()
                        connection.close()
                        canal.conn.send("Descuento aplicado".encode('utf-8'))
                        print("Descuento aplicado al Boleto {} {} {}\n".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                    else:
                        canal.conn.send("No se aplico descuento, descuento o pago previo aplicado".encode('utf-8'))
                        print("No se aplico descuento al boleto {} {} {}: descuento o pago previo aplicado\n".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                else:
                    print("Boleto {} {} {} no encontrado\n".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                    canal.conn.send("Boleto no encontrado".encode('utf-8'))

        except Exception as e:
            canal.conn.send("no se registro el pago del boleto".encode('utf8'))  # mesaje de resultado
            print("\n Excepcion: Descuento Aplicar")
            connection.close()

    def solicitudDescuento(self,canal):
        try:
            connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac',
                                          host='localhost')
            with connection.cursor() as cursor:
                #print("Busqueda: {} {} {}".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                # Se comprueba la existencia del boleto y se recuperan sus datos, y el ultimo pago realizado
                cursor.execute(
                    'SELECT  B.idtipodescuento, B.idestado, B.fechaexpedicion FROM boleto B WHERE B.idboleto = %s and B.idexpedidora = %s and B.fechaexpedicion = %s;',
                    (self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                row = cursor.fetchone()
                if row is not None:
                    #print("columns: {}, {}, {}".format(row[0], row[1], row[2]))
                    if (row[1] == 1):
                        #print("ultimoPago: {} idEstado:{}".format(row[2], row[1]))
                        # idDescuento,idEstadoActual, fechaExpedicion
                        canal.conn.send((str(row[0]) + "," + str(row[1]) + "," + str(row[2])).encode('utf-8'))
                        print("\n Envio de datos para el pago del boleto {} {} {}, con estado {}".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion, str(row[1])))
                    if (row[1] == 2):
                        # Verificar si aun puede realizar su salida o ya debe pagar por tiempo excedido
                        cursor.execute(' SELECT B.idtipodescuento, B.idestado, P.fechapago, P.idpago FROM boleto B INNER JOIN pagos P ON  B.idboleto = P.idboleto and B.idexpedidora = P.idexpedidora and B.fechaexpedicion = P.fechaexpedicion AND idpago IN (SELECT MAX(idpago) from pagos WHERE pagos.idboleto = %s and pagos.idexpedidora = %s and pagos.fechaexpedicion = %s);',(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                        rowPago = cursor.fetchone()
                        if rowPago is not None:
                            #print("columns Pago: {}, {}, {}".format(rowPago[0], rowPago[1], rowPago[2]))
                            autoriza = calcularTiempoSalida(rowPago[2].strftime("%Y-%m-%d %H:%M:%S"))
                            #print("tiempo: {}".format(autoriza))
                            if (autoriza < 900):
                                tiempoSalida = int((900-autoriza)/60)
                                print("\nNo se puede pagar el boleto {} {} {}, aun tienes {} minutos para salir".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion, tiempoSalida))
                                canal.conn.send((str(rowPago[0]) + "," + str(rowPago[1]) + "," + str(tiempoSalida)).encode('utf-8'))
                                #print("Paso envio 2******")
                            else:
                                #Se actualiza el estado a tiempo excedido
                                cursor.execute(
                                    'UPDATE boleto SET idestado = %s WHERE idboleto = %s and idexpedidora = %s and fechaexpedicion = %s',
                                    (3, self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                                #idDescuento,idEstadoActual, fechaExpedicion
                                fechaPago = datetime.strftime(rowPago[2], '%Y-%m-%d %H:%M:%S')
                                canal.conn.send((str(rowPago[0]) + "," + str(3) + "," + fechaPago).encode('utf-8'))
                                print("\n Envio de datos para el pago del boleto {} {} {}, con estado 3".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                            connection.commit()
                            connection.close()

                    if (int(row[1]) == 3):
                        # Verificar si aun puede realizar su salida o ya debe pagar por tiempo excedido
                        cursor.execute(
                            ' SELECT B.idtipodescuento, B.idestado, P.fechapago, P.idpago FROM boleto B INNER JOIN pagos P ON  B.idboleto = P.idboleto and B.idexpedidora = P.idexpedidora and B.fechaexpedicion = P.fechaexpedicion AND idpago IN (SELECT MAX(idpago) from pagos WHERE pagos.idboleto = %s and pagos.idexpedidora = %s and pagos.fechaexpedicion = %s);',
                            (self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                        rowPago = cursor.fetchone()
                        if rowPago is not None:
                            # idDescuento,idEstadoActual, fechaExpedicion
                            fechaPago = datetime.strftime(rowPago[2], '%Y-%m-%d %H:%M:%S')
                            canal.conn.send( (str(rowPago[0]) + "," + str(rowPago[1]) + "," + fechaPago).encode('utf-8'))
                            print("\n Envio de datos para el pago del boleto {} {} {}, con estado {}".format(str(rowPago[1], self.idBoleto, self.idExpedidora, self.fechaExpedicion)))

                    if (int(row[1]) == 4):
                        canal.conn.send((str("0") + "," + str(4) + "," + "x").encode('utf-8'))
                        print("\nBoleto {} {} {}: Obsoleto".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                else:
                    canal.conn.send("boleto no localizado".encode('utf-8'))
                    print("\nNo se Encontro el Boleto {} {} {}".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))

        except Exception as e:
            canal.conn.send("error en la operacion".encode('utf8'))  # mesaje de resultado
            print("\nException: Solicitud Descuento")
            print(e)
            connection.close()

    #Metodo transaccional, si falla en alguna operacion deshace todos los cambios en la BD
    def pagoBoleto(self,canal):
        try:
            connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac',
                                          host='localhost')
        except (Exception, psycopg2.DatabaseError) as error:
            print("\nException Connection Pago Boleto")
            print(error)
            connection.close()

        with connection.cursor() as cursor:
            try:
                #se envia ok por recibir datos del boleto
                canal.conn.send("ack".encode('utf-8'))
                # quedo a la espera de todos los datos del boleto, para registrarlos junto con el pago
                data = canal.conn.recv(tam_buffer)
                if data:
                    # se convierten los datos a string
                    datosCodif = data.decode('utf-8')
                    print("***datosCodif: {} ".format(datosCodif))
                    # Separacion de la cadena recibida, idBoleto,ideExpedidora,fechaExpedicion,id caj, mediopago, monto, monedas, billetes, tarifas
                    words = [i for i in str(datosCodif).split(';')]
                    print("words: {}".format(words))
                    tarifas = [i for i in str(words[6]).split(',')]
                    #print("tarifas: {}".format(tarifas))

                    self.idCaj = words[0]
                    self.medioPago = words[1]
                    self.monto = words[2]
                    self.monedas = words[3]
                    self.billetes = words[4]
                    self.cambio = words[5]
                    self.idTarifa = tarifas

                    cursor.execute('INSERT INTO pagos (idboleto, idexpedidora,fechaexpedicion,idcaj, mediopago, monto, monedas, billetes, cambio, fechapago) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING idpago;',(self.idBoleto, self.idExpedidora, self.fechaExpedicion, self.idCaj, self.medioPago, self.monto, self.monedas, self.billetes, self.cambio, datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')))
                    idPago = cursor.fetchall()[0]
                    #print("idpago:{}".format(idPago))
                    for x in self.idTarifa:
                        cursor.execute('INSERT INTO tarifaaplicada (idpago,idtarifa) VALUES (%s,%s);',(idPago,x))


                    #Se cambia el estado del boleto a pagado (2)
                    cursor.execute(
                        'UPDATE boleto SET idestado = %s WHERE idboleto = %s and idexpedidora = %s and fechaexpedicion = %s',
                        (2, self.idBoleto, self.idExpedidora, self.fechaExpedicion))


                    # se persisten los cambios en la BD y se cierra la conexion
                    connection.commit()
                    connection.close()
                    #print("se cerro la conexion a la BD")
                    canal.conn.send("registro exitoso del pago".encode('utf8'))
                    print("\nRegistro el pago del boleto exitoso {} {} {}".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))
                else:
                    canal.conn.send("boleto no localizado".encode('utf-8'))
                    print("\nBoleto {} {} {}: No localizado".format(self.idBoleto, self.idExpedidora, self.fechaExpedicion))

            except Exception as e:
                canal.conn.send("error en la operacion".encode('utf8'))  # mesaje de resultado
                print("\nException Pago Boleto")
                connection.close()

def calcularTiempoSalida(fechaPago):
    ''''# CALCULAR si no ha agotado el tiempo de salida
    # Verificar si aun puede realizar su salida o ya debe pagar por tiempo excedido
    # fechaActual = datetime.now()
    fechaActual = datetime.today()
    print("tipo: {} - {}".format(type(fechaActual), fechaActual))
    print("tipo: {} - {}".format(type(fechaPago), fechaPago))
    dif = fechaActual - fechaPago
    tSalida = math.floor(dif.seconds / 60)
    print("tsalida: {}".format(tSalida))
    return tSalida'''
    tiempo_st = time.strptime(fechaPago, "%Y-%m-%d %H:%M:%S")
    resultado = time.mktime(time.localtime()) - time.mktime(tiempo_st)
    return resultado
