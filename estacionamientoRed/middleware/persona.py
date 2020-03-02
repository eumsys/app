import psycopg2
from datetime import datetime
import time
import math

tam_buffer = 200
class Persona:

    #Constructor del objeto persona
    def __init__(self, idPersona = None,nombre = None, apellidoPaterno = None, apellidoMaterno = None, curp = None, sexo = None, estadoCivil = None, idUsuario = None, password = None, idRol = None, nombreRol = None):
        self.idPersona = idPersona
        self.nombre = nombre
        self.apellidoPaterno = apellidoPaterno
        self.apellidoMaterno = apellidoMaterno
        self.curp = curp
        self.sexo = sexo
        self.estadoCivil = estadoCivil
        self.idUsuario = idUsuario
        self.password = password
        self.idRol = idRol
        self.nombreRol = nombreRol

    def __repr__(self):
        return "idPersona:{}, nombre:{}, apellidoPaterno:{}, apellidoMaterno:{}, curp:{}, sexo:{}, estadoCivil:{}, idUsuario:{}, password:{}, idRol:{}, nombreRol:{}"\
            .format(self.idPersona,self.nombre, self.apellidoPaterno, self.apellidoMaterno, self.curp, self.sexo, self.estadoCivil, self.idUsuario, self.password, self.idRol, self.nombreRol)

    def inicioSesion(self, canal):
        try:
            connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac',
                                          host='localhost')
            print("Busqueda: {} {}".format(self.idUsuario, self.password))

            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT P.nombre, P.apellidopaterno, P.apellidomaterno, U.turno FROM usuario AS U JOIN persona AS '
                    'P ON U.idpersona=P.idpersona WHERE U.idusuario=%s AND U.password=%s; ',(self.idUsuario, self.password))
                row = cursor.fetchone()
                if row is not None:
                    print("Usuario y password validos nombre:{}, apellido paterno:{}, apellido materno:{}".format(row[0], row[1], row[2]))
                    canal.conn.send((str(row[0]) + "," + str(row[1]) + "," + str(row[3])).encode('utf-8'))
                else:
                    print("Usuario y/o password no encontradas en la base de datos")
                    canal.conn.send("usuario y/o password incorrectas".encode('utf-8'))

        except (Exception, psycopg2.DatabaseError) as error:
            print("\nException Connection Inicio Sesion")
            print(error)
            canal.conn.send("no se puedo realizar la busqueda".encode('utf-8'))
            connection.close()

        finally:
            if connection is not None:
                connection.close()

