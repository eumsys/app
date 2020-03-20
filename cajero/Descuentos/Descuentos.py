import os,sys

class Descuentos:
	"""
    Clase utulizada para validar y registrar descuentos
	"""

	def __init__(self,cursor):
        self.cursor = cursor
        self.modo_operacion = 1
        self.codigo_walmart = 1234
        self.mensaje = ""

    def establecer_modo_operacion(modo_operacion):
        self.modo_operacion = modo_operacion
        
    def validar_descuento(boleto):
        if self.modo_operacion == 1:
            self.validar_boleto_walmart(boleto)

    def validar_boleto_walmart(boleto):
        if self.codigo_walmart in boleto:
            self.mensaje = "Descuento valido: Walmart"
            print(self.mensaje)
        try:
            result=0
            validador = "SELECT 1 FROM \"DESCUENTO\" WHERE nombre = "+str(boleto)
            self.cursor.execute(validador)
            for reg in self.cursor:
                result=reg[0]

            if result:
                self.mensaje = "Descuento invalido: Ya fue previamente aplicado"
                print(self.mensaje)
            else:
                self.registrar_descuento(boleto)
                

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.mensaje = "Descuento no registrado: Ocurrio un error al registrar el decuento"
            print(self.mensaje)

        
        #-------------------------------- REGISTRA BOLETO EN BD -------------------------------------------
        if(tipo==1):
            if(result==1):
                mensajeBoletoUsado=1
					print("FOLIO YA REGISTRADO")
        pass

    def registrar_descuento(boleto):
        consu="insert into \"DESCUENTO\" (nombre) values("+str(boleto)+")"
        print(consu)
        cur.execute(consu)
        conn.commit()
        print("Descuento registrado: Se realizo el descuento correctamente")


    
