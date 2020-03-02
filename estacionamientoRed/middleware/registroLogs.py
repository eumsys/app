import psycopg2
from datetime import datetime
import time
import math

tam_buffer = 200
class Log:

    #Constructor del objeto log
    def __init__(self, idPersona = None,idCajero = None, idTipoMantenimiento = None, inicioMonedasMonedero = None, inicioBilletesBilletero = None, edoOperacion = None, descripcionFinal = None, idSalida =None, idExpedidora = None ):
        self.idPersona = idPersona
        self.idCajero = idCajero
        self.idTipoMantenimiento = idTipoMantenimiento
        self.inicioMonedasMonedero = inicioMonedasMonedero
        self.inicioBilletesBilletero = inicioBilletesBilletero
        self.edoOperacion = edoOperacion
        self.descripcionFinal = descripcionFinal
        self.idSalida = idSalida
        self.idExpedidora = idExpedidora

    def __repr__(self):
        return "idPersona:{}, idCajero:{}, idTipoMantenimiento:{}, inicioMonedasMonedero:{}, inicioBilletesBilletero:{}, edoOperacion:{}, descripcionFinal:{}, idSalida:{}, idExpedidora:{}"\
            .format(self.idPersona,self.idCajero, self.idTipoMantenimiento, self.inicioMonedasMonedero, self.inicioBilletesBilletero, self.edoOperacion, self.descripcionFinal, self.idSalida, self.idExpedidora)

    def logInicial(self, canal):
        try:
            connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac', host='localhost')
            #print("Busqueda: {} {} {} {} {} ".format(self.idCajero, self.idPersona, self.idTipoMantenimiento, self.inicioMonedasMonedero, self.inicioBilletesBilletero))

            with connection.cursor() as cursor:
                fechaOperacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute('INSERT INTO log_inicial(idpersona, idcaj, idtipo, monedas_previas, billetes_previas, fechamantenimiento) VALUES (%s, %s, %s, %s, %s, %s);'
                    ,(self.idPersona, self.idCajero, self.idTipoMantenimiento,self.inicioMonedasMonedero,self.inicioBilletesBilletero,fechaOperacion))
            connection.commit()
            connection.close()
            canal.conn.send("inicio_log registrado".encode('utf-8'))
            print("--> Log Inicial insertado en el cajero:{} por el usuario:{} de tipo:{} con monedas:{} y billetes:{} con fecha:{}".format(self.idCajero, self.idPersona, self.idTipoMantenimiento,self.inicioMonedasMonedero,self.inicioBilletesBilletero,fechaOperacion))
            return True

        except (Exception, psycopg2.DatabaseError) as error:
            print("\nException connection: logInicial")
            print(error)
            canal.conn.send("no se pudo acceder a la base de datos".encode('utf-8'))
            connection.close()

        finally:
            if connection is not None:
                connection.close()

    def logFinal(self, canal):
        try:
            connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac', host='localhost')
            #print("Busqueda: {} {} {} {} {} ".format(self.idCajero, self.idPersona, self.idTipoMantenimiento, self.inicioMonedasMonedero, self.inicioBilletesBilletero))

            with connection.cursor() as cursor:
                fechaOperacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute('INSERT INTO log_final(idcaj, idestado, idpersona, fechamantenimiento, descripcion) VALUES (%s, %s, %s, %s, %s);'
                    ,(self.idCajero, self.edoOperacion,self.idPersona,fechaOperacion,self.descripcionFinal))
            connection.commit()
            connection.close()
            canal.conn.send("fin_log registrado".encode('utf-8'))
            print("--> Log Final insertado en el cajero:{} por el usuario:{} con estado:{}, fecha:{} y descripcion:{}".format
                (self.idCajero, self.idPersona, self.edoOperacion,self.fechaOperacion,self.descripcionFinal))
            return True

        except (Exception, psycopg2.DatabaseError) as error:
            print("\nException connection: logFinal")
            print(error)
            canal.conn.send("no se pudo acceder a la base de datos".encode('utf-8'))
            connection.close()

        finally:
            if connection is not None:
                connection.close()

    def logSalida(self, canal):
        try:
            connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac', host='localhost')
            #print("Busqueda: {} {} {} {} {} ".format(self.idCajero, self.idPersona, self.idTipoMantenimiento, self.inicioMonedasMonedero, self.inicioBilletesBilletero))

            with connection.cursor() as cursor:
                #fechaOperacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                fechaOperacion = datetime.now().strftime("%Y-%m-%d")
                cursor.execute('INSERT INTO logs_barrerasalida(idsalida, idtipo, estado_operacion, fecha) VALUES (%s, %s, %s, %s);'
                    ,(self.idSalida, self.idTipoMantenimiento, self.edoOperacion,fechaOperacion))
            connection.commit()
            connection.close()
            canal.conn.send("log salida registrado".encode('utf-8'))
            print("--> Log de Salida insertado en la salida:{} de tipo:{} con estado:{} y fecha:{}".format
                (self.idSalida, self.idTipoMantenimiento, self.edoOperacion,fechaOperacion))
            return True

        except (Exception, psycopg2.DatabaseError) as error:
            print("\nException connection: logSalida")
            print(error)
            canal.conn.send("no se pudo acceder a la base de datos".encode('utf-8'))
            connection.close()

        finally:
            if connection is not None:
                connection.close()

    def logExpedidora(self, canal):
        try:
            connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac', host='localhost')
            #print("Busqueda: {} {} {} {} {} ".format(self.idCajero, self.idPersona, self.idTipoMantenimiento, self.inicioMonedasMonedero, self.inicioBilletesBilletero))

            with connection.cursor() as cursor:
                #fechaOperacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                fechaOperacion = datetime.now().strftime("%Y-%m-%d")
                cursor.execute('INSERT INTO logs_expedidora(idexpedidora, idtipo, estado_operacion,feha) VALUES (%s, %s, %s, %s);'
                    ,(self.idExpedidora, self.idTipoMantenimiento, self.edoOperacion,fechaOperacion))
            connection.commit()
            connection.close()
            canal.conn.send("log expedidora registrado".encode('utf-8'))
            print("--> Log de Expedidora insertado en la expedidora:{} de tipo:{} con estado:{} y fecha:{}".format
                (self.idExpedidora, self.idTipoMantenimiento, self.edoOperacion,fechaOperacion))
            return True

        except (Exception, psycopg2.DatabaseError) as error:
            print("\nException connection: logExpedidora")
            print(error)
            canal.conn.send("no se pudo acceder a la base de datos".encode('utf-8'))
            connection.close()

        finally:
            if connection is not None:
                connection.close()
