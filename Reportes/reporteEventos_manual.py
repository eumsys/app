import time
import threading
import psycopg2, psycopg2.extras
import time
import fpdf 
from fpdf import FPDF
import os,sys,getopt
import shutil

connection = psycopg2.connect(user='postgres', password='Postgres3UMd6', database='CajerOk', host='localhost')
cursor = connection.cursor()


from datetime import datetime, date, timedelta
import time


ruta =  os.path.join(os.path.dirname(os.path.abspath(__file__)))
ruta = ruta + "/"
def obtenerUsuario(ruta):
	lista = ruta.split("/")
	return "/"+lista[1]+"/"+lista[2]+"/"	
rutaUsuario = obtenerUsuario(ruta)
print(rutaUsuario)



#fecha_hoy = '2017-11-26'
fecha_hoy = str(date.today())

#fechaQuery1="2017-11-26 07:00:00"
#fechaQuery2="2017-11-26 22:00:00"

fecha_inicio = "2010-03-07 07:00:00"
fecha_hora_actual = "2020-03-08 22:00:00"


class PDF():
    def __init__(self, nombre, fecha1, fecha2,descripcion = "" ):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha1 = fecha1
        self.fecha2 = fecha2

        self.pdf=FPDF()
        self.pdf.add_page('L')
        #self.pdf=FPDF()
        #self.pdf.add_page()
        self.pdf.set_font('Arial','',32)
        self.pdf.cell(30,10,self.nombre)
        self.pdf.ln()
        self.pdf.ln()
        self.pdf.set_font('Arial','',18)
        #self.pdf.cell(30,10,self.fecha1.rstrip(' 00:00:00')+' - '+self.fecha2.rstrip(' 23:59:59'))
        self.pdf.cell(30,10,self.fecha1+' - '+self.fecha2)
        #fechaA=str(fecha1.rstrip(' 00:00:00')).replace("/","-")
        #fechaB=str(fecha2.rstrip(' 23:59:59')).replace("/","-")
        #self.pdf.ln()
        #self.pdf.cell(30,10,"Cajero: "+str(idCajero))
        self.agregarSubtitulo('Generado: '+str(time.strftime("%Y/%m/%d  %H:%M:%S")))
        self.agregarSubtitulo('Tipo: General')

        #self.pdf.ln()
        
        '''self.pdf.cell(45,10,'Fecha',1)
        self.pdf.cell(45,10,'Usuario',1)
        self.pdf.cell(45,10,'Evento',1)
        self.pdf.cell(55,10,'Detalle',1)
        self.pdf.set_font('Arial','',12)
        self.pdf.ln()'''
    def agregarSubtitulo(self,nombre):
        self.pdf.ln()
        #self.pdf.ln()
        self.pdf.set_font('Arial','',18)
        self.pdf.cell(30,10,nombre)
        self.pdf.ln()

    def generarPdf(self,idCajero,idSucursal):
        #self.pdf.output('reportes/'+self.nombre+'_'+self.fecha2[:10]+'.pdf','F')
        nombre_archivo = "S"+str(idSucursal)+"_"+"C"+str(idCajero)+"_"+self.fecha1[10:].replace(':','-').replace(' ','')+'_'+self.fecha2[:10]+'.pdf'
        print("generando pdf: ",nombre_archivo)
        self.pdf.output(ruta+'reportes/'+nombre_archivo,'F')
        #os.system("./"+ruta.replace(rutaUsuario,"")+"reportes.sh "+nombre_archivo)
        os.system(""+ruta+"reportes.sh "+nombre_archivo)

    def establecerRangoFechas(self,fecha1,fecha2):
        self.fecha1 = fecha1
        self.fecha2 = fecha2
    def obtenerRangoFechas(self,fecha1,fecha2):
        return self.fecha1,self.fecha2
    def establecerFuente(self,fuente,tipo,tamano):
        self.pdf.set_font(fuente,tipo,tamano)
    def dibujarCelda(self,ancho,alto,nombre,dato):
        self.pdf.cell(ancho,alto,nombre,dato)
    def dibujarSalto(self):
        self.pdf.ln()


class Tabla():

    def __init__(self, pdf,nombre, descripcion = ""):


            self.pdf=pdf
            #self.agregarPagina()
            #self.pdf.set_font('Arial','B',48)
            #pdf.cell(30,10,'Reporte de Eventos\n')
            #self.pdf.cell(30,10,nombre+'\n')
            self.query = ''

            self.nombre = nombre
            self.descripcion = descripcion

            self.fecha1 = ''
            self.fecha2 = ''

            self.encabezados = []
            self.celdas = []


    def agregarPagina (self):
        self.pdf.add_page()


    def establecerFuente(self,fuente,tipo,tamano):
        self.pdf.set_font(fuente,tipo,tamano)

    def agregarCeldas(self,nombre,dato):
        celda = [nombre,dato]
        self.celdas.append(celda)

        #self.pdf.cell(ancho,alto,nombre,dato)


    def agregarEncabezado(self,ancho,alto,nombre,dato):
        encabezado = [ancho,alto,nombre,dato]
        self.encabezados.append(encabezado)
        #self.pdf.cell(ancho,alto,nombre,dato)

    def agregarSubtitulo(self,nombre):
        self.pdf.ln()
        #self.pdf.ln()
        self.pdf.set_font('Arial','',18)
        self.pdf.cell(30,10,nombre)
        self.pdf.ln()


    def dibujarTabla(self):
        distribucion = len(self.celdas)/len(self.encabezados)
        i=0
        #self.pdf.cell(45,10,'Fecha',1)
        
        if distribucion:
            self.pdf.establecerFuente('Arial','B',8)
            for encabezado in self.encabezados:
                print(encabezado)
                self.pdf.dibujarCelda(encabezado[0],encabezado[1],encabezado[2],encabezado[3])

            self.pdf.dibujarSalto()
            self.pdf.establecerFuente('Arial','',8)
            for celda in self.celdas:
                if i >= len(self.encabezados) :
                    i = 0
                    self.pdf.dibujarSalto()

                ancho = self.encabezados[i][0]
                alto = self.encabezados[i][1]
                self.pdf.dibujarCelda(ancho,alto,celda[0],celda[1])
                i=i+1
        else:
            print('tabla malformada')

    def establecerQuery(self,query):
        self.query = query

    def establecerRangoFechas(self):
        fechas = self.pdf.obtenerRangoFechas()
        fechas.split(',')
        self.fecha1 = fechas[0]
        self.fecha2 = fechas[1]

    def establecerRangoFechas(self,fecha1,fecha2):
        self.fecha1 = fecha1
        self.fecha2 = fecha2

    
        

    def cabecera(self):
        #self.pdf=FPDF()
        #self.pdf.add_page()
        self.pdf.set_font('Arial','',32)
        self.pdf.cell(30,10,self.nombre)
        self.pdf.ln()
        self.pdf.ln()
        self.pdf.set_font('Arial','',18)
        #self.pdf.cell(30,10,self.fecha1.rstrip(' 00:00:00')+' - '+self.fecha2.rstrip(' 23:59:59'))
        self.pdf.cell(30,10,self.fecha1+' - '+self.fecha2)
        #fechaA=str(fecha1.rstrip(' 00:00:00')).replace("/","-")
        #fechaB=str(fecha2.rstrip(' 23:59:59')).replace("/","-")
        #self.pdf.ln()
        #self.pdf.cell(30,10,"Cajero: "+str(idCajero))
        self.agregarSubtitulo('Generado: '+str(time.strftime("%Y/%m/%d  %H:%M:%S")))
        self.agregarSubtitulo('Tipo: General')

        #self.pdf.ln()
        
        '''self.pdf.cell(45,10,'Fecha',1)
        self.pdf.cell(45,10,'Usuario',1)
        self.pdf.cell(45,10,'Evento',1)
        self.pdf.cell(55,10,'Detalle',1)
        self.pdf.set_font('Arial','',12)
        self.pdf.ln()'''




def incidencias(pdf):
    fechaQuery1 = pdf.fecha1
    fechaQuery2 = pdf.fecha2

    tablaBoletaje = Tabla(pdf,'CC\n','') 
    tablaBoletaje.agregarEncabezado(32,5,'Cobrados',1)
    tablaBoletaje.agregarEncabezado(32,5,'Cancelados',1)
    tablaBoletaje.agregarEncabezado(32,5,'Registrados',1)
    tablaBoletaje.agregarEncabezado(32,5,'Exitosos',1)
    tablaBoletaje.agregarEncabezado(32,5,'Incidencias',1)
    tablaBoletaje.agregarEncabezado(36,5,'Importe',1)
    tablaBoletaje.agregarEncabezado(32,5,'Excedente',1)
    tablaBoletaje.agregarEncabezado(32,5,'No registrados',1)



    queryCobrados = "select count(\"idPagos\") from  \"PAGOS\" where  \"fechaExpedicion\" between '{0}' and '{1}' and codigo<5".format(fechaQuery1,fechaQuery2)
    queryCancelados = "select count(\"idPagos\") from  \"PAGOS\" where  \"fechaExpedicion\" between '{0}' and '{1}' and codigo>4".format(fechaQuery1,fechaQuery2)
    queryRegistrados = "select count(\"idPagos\") from  \"PAGOS\" where  \"fechaExpedicion\" between '{0}' and '{1}' and registrado=1".format(fechaQuery1,fechaQuery2)
    queryExitosos = "select count(\"idPagos\") from  \"PAGOS\" where  \"fechaExpedicion\" between '{0}' and '{1}' and codigo=1".format(fechaQuery1,fechaQuery2)
    queryIncidencias = "select count(\"idPagos\") from  \"PAGOS\" where  \"fechaExpedicion\" between '{0}' and '{1}' and codigo!=1 and codigo!=5".format(fechaQuery1,fechaQuery2)
    #queryTolerancias = "select count(\"idPagos\") from boleto where   \"fechaExpedicion\" between '{0}' and '{1}' and idestado=6".format(fechaQuery1,fechaQuery2)
    queryImporte = "select sum(monto) from \"PAGOS\" where   \"fechaExpedicion\" between '{0}' and '{1}' and codigo<5".format(fechaQuery1,fechaQuery2)
    queryExcedente = "select sum(monto) from \"PAGOS\" where   \"fechaExpedicion\" between '{0}' and '{1}' and (codigo=2 or codigo=3 or codigo=6 or codigo=7)".format(fechaQuery1,fechaQuery2)
    queryNoRegistrados = "select count(\"idPagos\") from  \"PAGOS\" where  \"fechaExpedicion\" between '{0}' and '{1}' and registrado=0".format(fechaQuery1,fechaQuery2)

    
    cobrados = consultaBD(1,queryCobrados)
    cancelados = consultaBD(1,queryCancelados)
    registrados = consultaBD(1,queryRegistrados)
    exitosos = consultaBD(1,queryExitosos)
    incidencias = consultaBD(1,queryIncidencias)
    importe = consultaBD(1,queryImporte)
    excedente = consultaBD(1,queryExcedente)
    noRegistrados = consultaBD(1,queryNoRegistrados)

    if(not cobrados):
        cobrados=0
    if(not cancelados):
        cancelados=0
    if(not registrados):
        registrados=0
    if(not exitosos):
        exitosos=0
    if(not incidencias):
        incidencias=0
    if(not incidencias):
        incidencias=0
    if(not importe):
        importe=0
    if(not excedente):
        excedente=0
    if(not noRegistrados):
        noRegistrados=0
    
    print(fechaQuery1,fechaQuery2)
    print(cobrados)
    print(cancelados)
    print(registrados)
    print(exitosos)
    print(incidencias)
    print(importe)
    print(noRegistrados)
    
    tablaBoletaje.agregarCeldas(str(cobrados),1)
    tablaBoletaje.agregarCeldas(str(cancelados),1)
    tablaBoletaje.agregarCeldas(str(registrados),1)
    tablaBoletaje.agregarCeldas(str(exitosos),1)
    tablaBoletaje.agregarCeldas(str(incidencias),1)
    tablaBoletaje.agregarCeldas(str(importe),1)
    tablaBoletaje.agregarCeldas(str(excedente),1)
    tablaBoletaje.agregarCeldas(str(noRegistrados),1)
    


    tablaBoletaje.dibujarTabla()


    generarDesglose(fechaQuery1,fechaQuery2,pdf,1)

    
    









    queryNoRegistrado = "select \"idBoleto\",\"fechaExpedicion\",codigo,registrado,monto,cambio,monedas,billetes,cambio_entregado from \"PAGOS\" where \"fechaExpedicion\" between '{0}' and '{1}' and registrado=0 and codigo!=5".format(fechaQuery1,fechaQuery2)
    queryCambioIncompleto = "select \"idBoleto\",\"fechaExpedicion\",codigo,registrado,monto,cambio,monedas,billetes,cambio_entregado from \"PAGOS\" where \"fechaExpedicion\" between '{0}' and '{1}' and codigo=2".format(fechaQuery1,fechaQuery2)
    queryCambioIncompletoSuspendido = "select \"idBoleto\",\"fechaExpedicion\",codigo,registrado,monto,cambio,monedas,billetes,cambio_entregado from \"PAGOS\" where \"fechaExpedicion\" between '{0}' and '{1}' and codigo=3".format(fechaQuery1,fechaQuery2)
    queryCompletadaSuspendido = "select \"idBoleto\",\"fechaExpedicion\",codigo,registrado,monto,cambio,monedas,billetes,cambio_entregado from \"PAGOS\" where \"fechaExpedicion\" between '{0}' and '{1}' and codigo=4".format(fechaQuery1,fechaQuery2)
    queryCancelada = "select \"idBoleto\",\"fechaExpedicion\",codigo,registrado,monto,cambio,monedas,billetes,cambio_entregado from \"PAGOS\" where \"fechaExpedicion\" between '{0}' and '{1}' and codigo=5".format(fechaQuery1,fechaQuery2)
    queryCanceladaCambioIncompleto = "select \"idBoleto\",\"fechaExpedicion\",codigo,registrado,monto,cambio,monedas,billetes,cambio_entregado from \"PAGOS\" where \"fechaExpedicion\" between '{0}' and '{1}' and codigo=6".format(fechaQuery1,fechaQuery2)
    queryCanceladaCambioIncompletoSuspendido = "select \"idBoleto\",\"fechaExpedicion\",codigo,registrado,monto,cambio,monedas,billetes,cambio_entregado from \"PAGOS\" where \"fechaExpedicion\" between '{0}' and '{1}' and codigo=7".format(fechaQuery1,fechaQuery2)
    queryCanceladaSuspendido = "select \"idBoleto\",\"fechaExpedicion\",codigo,registrado,monto,cambio,monedas,billetes,cambio_entregado from \"PAGOS\" where \"fechaExpedicion\" between '{0}' and '{1}' and codigo=8".format(fechaQuery1,fechaQuery2)
    
    

    tablas = []
    subtitulos = []
    querys = []
    t1 = Tabla(pdf,'No registrados\n','')
    t2 = Tabla(pdf,'Cambio incompleto\n','')
    t3 = Tabla(pdf,'Cambio incompleto Suspendido\n','')
    t4 = Tabla(pdf,'Completada Suspendido\n','')
    t4 = Tabla(pdf,'Completada Cancelada\n','')
    t5 = Tabla(pdf,'Cancelada Cambio incompleto\n','')
    t6 = Tabla(pdf,'Cancelada Cambio incompleto Suspendido\n','')
    t7 = Tabla(pdf,'Cancelada Suspendido\n','')
    tablas.append(t1)
    tablas.append(t2)
    tablas.append(t3)
    tablas.append(t4)
    tablas.append(t5)
    tablas.append(t6)
    tablas.append(t7)
    subtitulos.append("No registrados")
    subtitulos.append("Cambio incompleto")
    subtitulos.append("Cambio incompleto Suspendido")
    subtitulos.append("Completada Suspendido")
    subtitulos.append("Cancelado")
    subtitulos.append("Cancelada Cambio incompleto")
    subtitulos.append("Cancelada Cambio incompleto Suspendido")
    subtitulos.append("Cancelada Suspendido")
    querys.append(queryNoRegistrado)
    querys.append(queryCambioIncompleto)
    querys.append(queryCambioIncompletoSuspendido)
    querys.append(queryCompletadaSuspendido)
    querys.append(queryCancelada)
    querys.append(queryCanceladaCambioIncompleto)
    querys.append(queryCanceladaCambioIncompletoSuspendido)
    querys.append(queryCanceladaSuspendido)


    for i, tabla in enumerate(tablas):
        tabla.agregarEncabezado(20,5,'Folio',1)
        tabla.agregarEncabezado(40,5,'Fecha',1)
        tabla.agregarEncabezado(20,5,'Codigo',1)
        tabla.agregarEncabezado(20,5,'Registrado',1)
        tabla.agregarEncabezado(20,5,'Monto',1)
        tabla.agregarEncabezado(35,5,'Cambio',1)
        tabla.agregarEncabezado(35,5,'Monedas',1)
        tabla.agregarEncabezado(35,5,'Billetes',1)
        tabla.agregarEncabezado(35,5,'Cambio entregado',1)
        pdf.agregarSubtitulo(subtitulos[i])

        result = consultaBD(2,querys[i])
        for regs in result:
            for i, reg in enumerate(regs):
                tabla.agregarCeldas(str(reg),1)
        tabla.dibujarTabla()







    pdf.generarPdf(obtenerIdCajero(),obtenerIdSucursal())

def sumarBilletes(result):
    cantidad_billetes = {1:0,2:0,5:0}
    print("result",result)
    for reg in result:
        print("reg*************",reg[0])
        valores = reg[0].split(",")
        for valor in valores:
            print("**",valor)
            billetes = valor.split(":")
            #print(billetes)
            try:
                #print("####",billetes,cantidad_billetes[int(billetes[1])],cantidad_billetes.get(int(billetes[1])),billetes[0])
                '''
                print("####",billetes)
                print("####",cantidad_billetes[int(billetes[1])])
                print("####",cantidad_billetes.get(int(billetes[1])))
                print("####",billetes[0])
                '''
                cantidad_billetes[int(billetes[1])] = cantidad_billetes.get(int(billetes[1])) + int(billetes[0])
            except:
                print("No se pudo hacer la sumatoria *******************************************************")
                pass
    print("Billetes: *******************************************************",cantidad_billetes)
    return cantidad_billetes
    



def consultaBD(tipoQuery,query):
    if tipoQuery == 1:
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result
    elif tipoQuery == 2:
        cursor.execute(query)

        return cursor
    elif tipoQuery == 3:
        cursor.execute(query)
        importe = ""
        for reg in cursor:
            importe += str(reg[1])+"x"+str(reg[0])+" "
        return importe
    elif tipoQuery == 4:
        cursor.execute(query)
        billetes = sumarBilletes(cursor)
        return billetes




def generarDesglose(fechaQuery1,fechaQuery2,pdf,numero):
    tablaCorteCajero = Tabla(pdf,'CC\n','')
    pdf.agregarSubtitulo("Detalles")
    tablaCorteCajero.agregarEncabezado(10,15,'Cajero',1)
    #tablaCorteCajero.agregarEncabezado(15,15,'Boletos',1)
    #tablaCorteCajero.agregarEncabezado(20,15,'Ingreso',1)
    tablaCorteCajero.agregarEncabezado(5,15,'$1',1)
    tablaCorteCajero.agregarEncabezado(5,15,'$2',1)
    tablaCorteCajero.agregarEncabezado(5,15,'$5',1)
    tablaCorteCajero.agregarEncabezado(7,15,'$10',1)
    tablaCorteCajero.agregarEncabezado(7,15,'$20',1)
    tablaCorteCajero.agregarEncabezado(7,15,'$50',1)
    tablaCorteCajero.agregarEncabezado(8,15,'$100',1)
    tablaCorteCajero.agregarEncabezado(200,15,'Desglose',1)


    #queryCobrados = "select count(idpago) from pagos where fechaexpedicion between '{0}' and '{1}' and idcaj={2}".format(fechaQuery1,fechaQuery2,numero)
    #queryCorteCaja = "select sum(monto) from pagos where fechaexpedicion between '{0}' and '{1}' and idcaj={2}".format(fechaQuery1,fechaQuery2,numero)
    queryDetallesCorte = "select monto,count(monto) from \"PAGOS\" where \"fechaExpedicion\" between '{0}' and '{1}' and codigo<5 group by monto".format(fechaQuery1,fechaQuery2)

    '''
    Billetes
    '''

    queryBilletes = "select billetes from \"PAGOS\" where \"fechaExpedicion\" between '{0}' and '{1}' and codigo<5 and billetes!='0:0'".format(fechaQuery1,fechaQuery2)
    detallesBilletes = consultaBD(4,queryBilletes)
    print("detallesBilletes",detallesBilletes,"ok")
    billete_20 = 0
    billete_50 = 0
    billete_100 = 0

    try:
        billete_20 = detallesBilletes.get(1)
        billete_50 = detallesBilletes.get(2)
        billete_100 = detallesBilletes.get(5)
    except:
        print("No se pudieron obtener los valores de los billetes")
    '''
    Billetes
    '''


    #cobrados = consultaBD(1,queryCobrados)
    #corteCaja = consultaBD(1,queryCorteCaja)
    #detallesCorte = consultaBD(3,queryDetallesCorte)+detallesBilletes+detallesBilletes+detallesBilletes+detallesBilletes+detallesBilletes
    

    tablaCorteCajero.agregarCeldas(str(numero),1)
    #tablaCorteCajero.agregarCeldas(str('-'),1)
    #tablaCorteCajero.agregarCeldas(str('-'),1)
    tablaCorteCajero.agregarCeldas(str('-'),1)
    tablaCorteCajero.agregarCeldas(str('-'),1)
    tablaCorteCajero.agregarCeldas(str('-'),1)
    tablaCorteCajero.agregarCeldas(str('-'),1)
    tablaCorteCajero.agregarCeldas(str(billete_20),1)
    tablaCorteCajero.agregarCeldas(str(billete_50),1)
    tablaCorteCajero.agregarCeldas(str(billete_100),1)
    tablaCorteCajero.agregarCeldas(str('-'),1)

    tablaCorteCajero.dibujarTabla()

def obtenerIdCajero():
    NoCajero = 1
    try:
        infile = open(rutaUsuario+"eum.conf", 'r')
        NoCajero=infile.readline()
        NoCajero=NoCajero.split(",")
        NoCajero=NoCajero[0]
        print("Cajero ",NoCajero)
        infile.close()
    except:
        print("No se pudo obtener el idCajero: id=1")
        NoCajero = 1
    return NoCajero

def obtenerIdSucursal():
    idSucursal = 1
    try:
        infile = open(rutaUsuario+"eum.conf", 'r')
        idSucursal=infile.readline()
        idSucursal=idSucursal.split(",")
        idSucursal=idSucursal[1]
        print("Sucursal ",idSucursal)
        infile.close()
    except:
        print("No se pudo obtener el idSucursal; id=1")
        idSucursal = 1
    return idSucursal


def resumenBoletaje(pdf):
    """pdf1=FPDF()
    pdf1.add_page()
    tablaBoletaje = Tabla(pdf1,'CC\n','')
    tablaBoletaje.establecerRangoFechas('2019-09-01 07:00:00','2019-09-10 22:00:00')
    tablaBoletaje.cabecera()
    """

    fechaQuery1 = pdf.fecha1
    fechaQuery2 = pdf.fecha2
    tablaBoletaje = Tabla(pdf,'CC\n','') 
    tablaBoletaje.agregarEncabezado(17,5,'Cobrados',1)
    tablaBoletaje.agregarEncabezado(17,5,'Registrados',1)
    tablaBoletaje.agregarEncabezado(17,5,'Exitosos',1)
    tablaBoletaje.agregarEncabezado(17,5,'Incidencias',1)
    tablaBoletaje.agregarEncabezado(25,5,'Importe',1)
    tablaBoletaje.agregarEncabezado(17,5,'Excedente',1)



    queryCobrados = "select count(idPagos) from pagos where fechaexpedicion between '{0}' and '{1}'".format(fechaQuery1,fechaQuery2)
    queryRegistrados = "select count(idboleto) from pagos where fechaexpedicion between '{0}' and '{1}'".format(fechaQuery1,fechaQuery2)
    queryExitosos = "select count(idboleto) from boleto where fechaexpedicion between '{0}' and '{1}' and idestado=4".format(fechaQuery1,fechaQuery2)
    queryIncidencias = "select count(idboleto) from boleto where fechaexpedicion between '{0}' and '{1}' and idestado=6".format(fechaQuery1,fechaQuery2)
    #queryTolerancias = "select count(idboleto) from boleto where fechaexpedicion between '{0}' and '{1}' and idestado=6".format(fechaQuery1,fechaQuery2)
    queryImporte = "select sum(monto) from pagos where fechaexpedicion between '{0}' and '{1}'".format(fechaQuery1,fechaQuery2)
    queryExcedente = "select monto,count(monto) from pagos where fechaexpedicion between '{0}' and '{1}' group by monto".format(fechaQuery1,fechaQuery2)
    queryNoRegistrados = "select * from pagos where fechaexpedicion between '{0}' and '{1}' and registrado=0 group by monto".format(fechaQuery1,fechaQuery2)
    #queryIncidencias = "select count(boleto.idboleto) from boleto left JOIN pagos on boleto.idboleto = pagos.idboleto and boleto.idexpedidora = pagos.idexpedidora and boleto.fechaexpedicion=pagos.fechaexpedicion where boleto.fechaexpedicion between '{0}' and '{1}' and pagos.idboleto ISNULL".format(fechaQuery1,fechaQuery2)
    #queryIncidencias2 = "select count(boleto.idboleto) from boleto left JOIN pagos on boleto.idboleto = pagos.idboleto and boleto.idexpedidora = pagos.idexpedidora and boleto.fechaexpedicion=pagos.fechaexpedicion where boleto.fechaexpedicion between '{0}' and '{1}' ".format(fechaQuery1,fechaQuery2)
    
    cobrados = consultaBD(1,queryCobrados)
    registrados = consultaBD(1,queryRegistrados)
    exitosos = consultaBD(1,queryExitosos)
    incidencias = consultaBD(1,queryIncidencias)
    importe = consultaBD(1,queryImporte)
    excedente = consultaBD(1,queryExcedente)
    noRegistrados = consultaBD(3,queryNoRegistrados)
    
    tablaCorteCajero.dibujarTabla()
    pdf.generarPdf(obtenerIdCajero(),obtenerIdSucursal())


def cortePorCajero(pdf,tablaCorteCajero,numero):
    

    fechaQuery1 = pdf.fecha1
    fechaQuery2 = pdf.fecha2
    #querycobrados = "select count(idboleto) from boleto where fechaexpedicion between '{0}' and '{1}'".format(fechaQuery1,fechaQuery2)
    queryCobrados = "select count(idpago) from pagos where fechaexpedicion between '{0}' and '{1}' and idcaj={2}".format(fechaQuery1,fechaQuery2,numero)
    queryincidencias = "select sum(monto) from pagos where fechaexpedicion between '{0}' and '{1}' and idcaj={2}".format(fechaQuery1,fechaQuery2,numero)

    queryimporte = "select monto,count(monto) from pagos where fechaexpedicion between '{0}' and '{1}' and idcaj={2} group by monto".format(fechaQuery1,fechaQuery2,numero)

    cobrados = consultaBD(1,queryCobrados)
    incidencias = consultaBD(1,queryincidencias)
    importe = consultaBD(3,queryimporte)

    tablaCorteCajero.agregarCeldas(str(numero),1)
    tablaCorteCajero.agregarCeldas(str(cobrados),1)
    tablaCorteCajero.agregarCeldas(str(incidencias),1)
    tablaCorteCajero.agregarCeldas(str('-'),1)
    tablaCorteCajero.agregarCeldas(str('-'),1)
    tablaCorteCajero.agregarCeldas(str('-'),1)
    tablaCorteCajero.agregarCeldas(str('-'),1)
    tablaCorteCajero.agregarCeldas(str('-'),1)
    tablaCorteCajero.agregarCeldas(str('-'),1)
    tablaCorteCajero.agregarCeldas(str('-'),1)
    tablaCorteCajero.agregarCeldas(str(importe),1)

    

    

    
def main (argv):
    f_inicio = ''
    f_fin = ''
    tipo = ''

    horario_inicio = ""
    horario_fin = ""

    horario_matutino = "06:30:00"
    horario_vespertino = "14:30:00"
    horario_nocturno = "22:30:00"

    #fecha_hoy = str(date.today())
    fecha_ayer = str(datetime.strptime(fecha_hoy,"%Y-%m-%d").date() - timedelta(days=1))


    ###### CORTE MATUTINO #######
    datetime_matutino_hoy_inicio = fecha_hoy+' '+horario_matutino
    datetime_matutino_hoy_fin = fecha_hoy+' '+horario_vespertino

    datetime_matutino_ayer_inicio = fecha_ayer+' '+horario_matutino
    datetime_matutino_ayer_fin = fecha_ayer+' '+horario_vespertino

    ###### CORTE VESPERTINO #######
    datetime_vespertino_hoy_inicio = fecha_hoy+' '+horario_vespertino
    datetime_vespertino_hoy_fin = fecha_hoy+' '+horario_nocturno

    datetime_vespertino_ayer_inicio = fecha_ayer+' '+horario_vespertino
    datetime_vespertino_ayer_fin = fecha_ayer+' '+horario_nocturno

    ###### CORTE NOCTURNO #######
    datetime_nocturno_hoy_inicio = fecha_hoy+' '+horario_nocturno
    datetime_nocturno_hoy_fin = fecha_hoy+' '+horario_matutino

    datetime_nocturno_ayer_inicio = fecha_ayer+' '+horario_nocturno
    datetime_nocturno_ayer_fin = fecha_ayer+' '+horario_matutino

    """
    #datetime_matutino_ayer = 
    print(datetime_matutino_hoy_inicio,datetime_matutino_hoy_fin,datetime_matutino_ayer_inicio,datetime_matutino_ayer_fin)
    exit(0)
    hora_actual = time.strftime("%H:%M:%S")
    hoy = date.today()
    ayer = hoy - timedelta(days=1)
    print(hoy,ayer)
    """



    try:
        opts, args = getopt.getopt(argv,"hi:f:t",["fechaInicio=","fechaFin=","tipo="])
    except getopt.GetoptError:
        print ('test.py -i <fechaInicio> -f <fechaFin> -t <tipo>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <fechaInicio> -f <fechaFin>')
            sys.exit()
        elif opt in ("-i", "--fechaInicio"):
            f_inicio = arg
        elif opt in ("-f", "--fechaFin"):
            f_fin = arg
        elif opt in ("-t", "--tipo"):
            tipo = arg
    print ('fechaInicio: "', datetime_matutino_hoy_fin , type(datetime_matutino_hoy_fin))
    print ('fechaFin "', f_fin)
    print ('tipo "', tipo)
    


    #if(tipo == 'm'):
        #pdfIncidenciasM = PDF('Incidencias Matutinon\n',"2017-11-26 07:00:00","2017-11-26 07:01:00",'')
    pdfResumenBoletaje = PDF('Resumen Boletaje Matutino',datetime_matutino_hoy_inicio,datetime_matutino_hoy_fin,'')


    '''
    infile = open(ruta+"fechaDeCorte.txt", 'r')
    fecha_inicio=infile.readline().rstrip("\n")
    #fecha_inicio=infile.readline()
    infile.close()
    
    fecha_actual = str(datetime.strptime(fecha_hoy.date(),"%Y-%m-%d") )
    hora_actual = time.strftime("%H:%M:%S")
    #fecha_hora_actual = fecha_hoy + " " + hora_actual
    '''
    pdfIncidencias = PDF('Incidencias',fecha_inicio,fecha_hora_actual,'')
    incidencias(pdfIncidencias)


    
    #print("fechas:: ",fecha_inicio,fecha_hoy,fecha_hora_actual)
    shutil.copy(ruta+"fechaDeCorte.txt", ruta+"fechaDeCorte_intervalo_de_inicio.txt")
    infile = open(ruta+"fechaDeCorte.txt", 'w')
    infile.write(str(fecha_hora_actual))
    infile.close()



    #resumenBoletaje(pdfResumenBoletaje)
    '''    
    elif(tipo == 'v'):
        pdfResumenBoletaje = PDF('Resumen Boletaje Vespertino\n',datetime_vespertino_hoy_inicio,datetime_vespertino_hoy_fin,'')
        pdfIncidencias = PDF('Incidencias\n',datetime_vespertino_ayer_inicio,datetime_vespertino_ayer_fin,'')
    elif(tipo == 'n'):
        pdfResumenBoletaje = PDF('Resumen Boletaje Nocturno\n',datetime_nocturno_hoy_inicio,datetime_nocturno_hoy_fin,'')
        pdfIncidencias = PDF('Incidencias\n',datetime_nocturno_ayer_inicio,datetime_nocturno_ayer_fin,'')

    Incidencias(pdfIncidencias)
    resumenBoletaje(pdfResumenBoletaje)
    '''
    exit(0)
    #pdfIncidenciasM = PDF('Incidencias Matutino\n',"2017-11-26 07:00:00","2017-11-26 07:01:00",'')
    #pdfIncidenciasV = PDF('Incidencias Vespertino\n',"2017-11-26 15:00:00","2017-11-26 23:00:00",'')
    #pdfIncidenciasN = PDF('Incidencias\n',"2017-11-26 23:00:00","2017-11-26 07:00:00",'')
    #pdfResumenBoletajeM = PDF('Resumen Boletaje Matutino\n',"2017-11-26 07:00:00","2017-11-26 22:00:00",'')
    #pdfResumenBoletajeV = PDF('Resumen Boletaje Vespertino\n',"2017-11-26 07:00:00","2017-11-26 22:00:00",'')
    #pdfResumenBoletajeN = PDF('Resumen Boletaje\n',"2017-11-26 07:00:00","2017-11-26 22:00:00",'')
    
    #pdfIncidencias.establecerRangoFechas("2017-11-26 07:00:00","2017-11-26 22:00:00")
    #pdfResumenBoletaje.establecerRangoFechas("2017-11-26 07:00:00","2017-11-26 22:00:00")
    #Incidencias(pdfIncidenciasM)
    #Incidencias(pdfIncidenciasV)
    #resumenBoletaje(pdfResumenBoletajeM)
    #resumenBoletaje(pdfResumenBoletajeV)
    
    
if __name__ == "__main__":
    main (sys.argv[1:])
    
