import paramiko
import psycopg2

comando_postgres = 'PGPASSWORD=Postgres3UMd6 psql dbeum_tecamac -h localhost -U postgres -c '
comando_postgres_cajero = 'PGPASSWORD=Postgres3UMd6 psql CajerOk -h localhost -U postgres -c '


def plaza_exp_val_kio(host, usuario, contrasenia):
    try:
        connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac', host='localhost')
        with connection.cursor() as cursor:
            cursor.execute(
                ' SELECT * FROM cat_plaza AS cpa JOIN cat_pais AS cpla ON cpa.idpais = cpla.idpais JOIN cat_continente AS ccon ON ccon.idcontinente = cpla.idcontinente JOIN cat_estados AS cest ON cest.idestado = cpa.idestado WHERE idplaza = 1;')  # ,(self.idPlaza))
            row = cursor.fetchone()
            if row is not None:
                # Primer query a la base de datos remota tabla CAT_PLAZA
                query = "UPDATE Plaza SET estado='{}', pais='{}', continente='{}', nombre_plaza='{}', calle='{}', colonia='{}', delegacion='{}', cp={}, numinterior='{}', numexterior='{}', telefonolocal='{}', extension='{}', email='{}', celular='{}' WHERE idplaza=1;".format(
                        str(row[24]), str(row[18]), str(row[20]),
                        str(row[4]), str(row[5]), str(row[6]), str(row[7]), str(row[8]), str(row[9]), str(row[10]),
                        str(row[11]), str(row[12]), str(row[13]), str(row[14]))
                query2 = "INSERT INTO Plaza (idplaza,estado,pais,continente,nombre_plaza,calle,colonia,delegacion,cp,numinterior,numexterior,telefonolocal,extension,email,celular) VALUES ({},'{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}','{}')".format(
                    "1", str(row[24]), str(row[18]), str(row[20]), str(row[4]), str(row[5]), str(row[6]), str(row[7]),
                    str(row[8]), str(row[9]), str(row[10]), str(row[11]), str(row[12]), str(row[13]), str(row[14]))
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, username=usuario, password=contrasenia)
                entrada, salida, error = ssh.exec_command(comando_postgres + '"' + query + '"')
                falla = error.read().decode('utf-8')
                if falla != "":
                    print(falla)
                validar = salida.read().decode('utf-8')
                if validar != "":
                    if validar[7] == "0":
                        entrada, salida, error = ssh.exec_command(comando_postgres + '"' + query2 + '"')
                        falla2 = error.read().decode('utf-8')
                        if falla2 != "":
                            print(falla2)
                connection.commit()
                ssh.close()
                connection.close()
            else:
                print("Registro no encontrado")
    except Exception as error:
        connection.close()
        ssh.close()
        print(error)


def plaza_caj(host, usuario, contrasenia):
    try:
        connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac', host='localhost')
        with connection.cursor() as cursor:
            cursor.execute(
                ' SELECT * FROM cat_plaza AS cpa JOIN cat_pais AS cpla ON cpa.idpais = cpla.idpais JOIN cat_continente AS ccon ON ccon.idcontinente = cpla.idcontinente JOIN cat_estados AS cest ON cest.idestado = cpa.idestado WHERE idplaza = 1;')  # ,(self.idPlaza))
            row = cursor.fetchone()
            if row is not None:
                query = "UPDATE Plaza SET estado='{}', pais='{}', continente='{}', nombre_plaza='{}', calle='{}', colonia='{}', delegacion='{}', cp={}, numinterior='{}', numexterior='{}', telefonolocal='{}', extension='{}', email='{}', celular='{}' WHERE idplaza=1;".format(
                        str(row[24]), str(row[18]), str(row[20]),
                        str(row[4]), str(row[5]), str(row[6]), str(row[7]), str(row[8]), str(row[9]), str(row[10]),
                        str(row[11]), str(row[12]), str(row[13]), str(row[14]))
                query2 = "INSERT INTO Plaza (idplaza,estado,pais,continente,nombre_plaza,calle,colonia,delegacion,cp,numinterior,numexterior,telefonolocal,extension,email,celular) VALUES ({},'{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}','{}')".format(
                    "1", str(row[24]), str(row[18]), str(row[20]), str(row[4]), str(row[5]), str(row[6]), str(row[7]),
                    str(row[8]), str(row[9]), str(row[10]), str(row[11]), str(row[12]), str(row[13]), str(row[14]))
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, username=usuario, password=contrasenia)
                entrada, salida, error = ssh.exec_command(comando_postgres_cajero + '"' + query + '"')
                falla = error.read().decode('utf-8')
                if falla != "":
                    print(falla)
                validar = salida.read().decode('utf-8')
                if validar != "":
                    if validar[7] == "0":
                        entrada, salida, error = ssh.exec_command(comando_postgres_cajero + '"' + query2 + '"')
                        falla2 = error.read().decode('utf-8')
                        if falla2 != "":
                            print(falla2)
                connection.commit()
                ssh.close()
                connection.close()
            else:
                print("Registro no encontrado")
    except Exception as error:
        connection.close()
        ssh.close()
        print(error)


def politicas(host, usuario, contrasenia):
    try:
        connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac', host='localhost')
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT politicaboleto FROM cat_plaza;')
            row = cursor.fetchone()
            if row is not None:
                query = "UPDATE politicas SET descripcion='{}' WHERE idpoliticas=1;".format(str(row[0]))
                query2 = "INSERT INTO politicas (idpoliticas,plaza,descripcion) VALUES ({},{},'{}');".format("1", "1", str(row[0]))
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, username=usuario, password=contrasenia)
                entrada, salida, error = ssh.exec_command(comando_postgres + '"' + query + '"')
                falla = error.read().decode('utf-8')
                if falla != "":
                    print(falla)
                validar = salida.read().decode('utf-8')
                if validar != "":
                    if validar[7] == "0":
                        entrada, salida, error = ssh.exec_command(comando_postgres + '"' + query2 + '"')
                        falla2 = error.read().decode('utf-8')
                        if falla2 != "":
                            print(falla2)
                connection.commit()
                ssh.close()
                connection.close()
            else:
                print("Registro no encontrado")
    except Exception as error:
        connection.close()
        ssh.close()
        print(error)


def tarifas(host, usuario, contrasenia):
    try:
        connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac', host='localhost')
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM cat_tarifa where idtarifa=1;')
            row = cursor.fetchone()
            if row is not None:
                query = 'UPDATE "TARIFA" '"SET plaza={},fec_ini='{}',fec_fin='{}',dia_sem='{}',des_tar='{}',costo={},int_1={},int_2={},estado={},prioridad={},descuento={}"' WHERE "idTarifa"={};'.format(int(row[4]), str(row[8]), str(row[9]), str(row[11]), str(row[10]), int(row[12]), int(row[6]), int(row[7]), int(row[13]), int(row[14]), int(row[5]), "1")
                query2 = 'INSERT INTO "TARIFA" VALUES("idTarifa",plaza,fec_ini,fec_fin,dia_sem,des_tar,costo,int_1,int_2,estado,prioridad,descuento) VALUES '"({},{},'{}','{}','{}','{}',{},{},{},{},{},{})".format("19", int(row[4]), str(row[8]), str(row[9]), str(row[11]), str(row[10]), int(row[12]), int(row[6]), int(row[7]), int(row[13]), int(row[14]), int(row[5]))
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, username=usuario, password=contrasenia)
                entrada, salida, error = ssh.exec_command(comando_postgres_cajero + '"' + query + '"')
                falla = error.read().decode('utf-8')
                if falla != "":
                    print(falla)
                validar = salida.read().decode('utf-8')
                if validar != "":
                    if validar[7] == "0":
                        entrada, salida, error = ssh.exec_command(comando_postgres_cajero + '"' + query2 + '"')
                        falla2 = error.read().decode('utf-8')
                        if falla2 != "":
                            print(falla2)
                connection.commit()
                ssh.close()
                connection.close()
            else:
                print("Registro no encontrado")
    except Exception as error:
        connection.close()
        ssh.close()
        print(error)


def conexion_apagado(host, usuario, contrasenia):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=usuario, password=contrasenia)
        ssh.exec_command("sudo shutdown 0")
        ssh.close()
    except Exception as error:
        ssh.close()

conexion_apagado('192.168.1.136', 'pi', 'pi')
