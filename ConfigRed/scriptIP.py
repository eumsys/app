import psycopg2

def obtenerDatos():
    connection = psycopg2.connect(user='eumdb', password='Ingenieria3UMd6', database='dbeum_tecamac', host='localhost')
    with connection.cursor() as cursor:

        #Segmento de codigo para insertar las IP's de la expedidora
        cursor.execute(' SELECT nombre,direccion_ip FROM cat_expedidora')  # ,(self.idPlaza))
        archivo = open("archivo.txt", "w")
        for reg in cursor:
            print(reg[0], reg[1])
            num_expe=reg[0].split('_')
            archivo.write(reg[0] + "," + reg[1] + "," + "UPDATE datos_expedidora SET num_expedidora = " + num_expe[1] + " WHERE id_expedidora = 1;" + "\n")

        # Segmento de codigo para insertar las IP's de la barrera de salida
        cursor.execute(' SELECT nombre,direccion_ip FROM cat_barrerasalida')  # ,(self.idPlaza))
        for reg2 in cursor:
            print(reg2[0], reg2[1])
            if(reg2[0]!="sin asignar"):
                num_barrera = reg2[0].split('_')
                print(num_barrera)
                archivo.write(reg2[0] + "," + reg2[1] + "," + "UPDATE datos_salida SET num_salida = " + num_barrera[1] + " WHERE id_salida = 1;" + "\n")

        # Segmento de codigo para insertar las IP's del cajero
        cursor.execute(' SELECT nombre,direccion_ip FROM cat_casetacajero')  # ,(self.idPlaza))
        for reg3 in cursor:
            print("++"+reg3[0]+"++", reg3[1])

            if (reg3[0] != "Sin asignar"):
                num_cajero = reg3[0].split('_')
                archivo.write(reg3[0] + "," + reg3[1] + "," + "UPDATE \"CAJERO\" SET \"idCajero\" = " + num_cajero[1] + " WHERE id_cajero = 1;" + "\n")

                    # Segmento de codigo para insertar las IP's de la rasp de publicidad
        cursor.execute(' SELECT nombre,direccion_ip FROM cat_rasppublicidad')  # ,(self.idPlaza))
        for reg4 in cursor:
            print(reg4[0], reg4[1])
            if (reg4[0] != "Sin asignar"):
                num_publicidad = reg4[0].split('_')
                archivo.write(reg4[0] + "," + reg4[1] + "," + "UPDATE cat_rasppublicidad SET iddispositivo = " + num_publicidad[1] + " WHERE iddispositivo = 1;" + "\n")

        archivo.close()

obtenerDatos()
