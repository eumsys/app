# -*- coding: utf-8 -*-
"""
Estacionamientos unicos de México
Este archivo es para remplaar a acceso4.py
Funcion: 		Funcion de imprimir boleto
Descripcion:	

Funciones que se pueden usar:
	1) imprimirBoletoT tiempo corto formato largo
	2) imprimirBoleto  tiempo largo formato pequeño

"""
#from escposprinter import *#original funcional
import tratarImagen as imagen
import configuracionEXP as archivoConfiguracion
import time
import psycopg2, psycopg2.extras
import fechaUTC as hora
import fpdf 
from fpdf import FPDF
import os

PATH_NOMBRE_PLAZA=str(archivoConfiguracion.getName()).replace('\n','')
PATH_NUMERO_TERMINAL=str(archivoConfiguracion.getNumTer()).replace('\n','')
PATH_CODIGOS_QR="/home/pi/Documents/EUM_EXPE/CodigosQR/outputQR.png"

conn = psycopg2.connect(database='CajerOk',user='postgres',password='Postgres3UMd6', host='localhost')
cur = conn.cursor()

#Generic = printer.Usb(0x0519,0x0001)

def imprimirHeader():
	Generic = printer.Usb(0x0519,0x0001)
	Generic.set(size='2x', align='center')
	Generic.text('Bienvenido \n'+str(PATH_NOMBRE_PLAZA)+'\n')
	Generic.set(size='normal',align='center')
	Generic.text("La empresa no se hace responsable por objetos\npersonales,fallas mecanicas  y/o  electricas,\nsiestros ocasionados por derrumbes,temblores,\nterremotos o fenomenos naturales,asi como ro-\nbo de accesorios o vandalismo en su vehiculo.\n")
	Generic.text("Por robo total de acuerdo a los terminos  del\nseguro contratado.Boleto Perdido.Se entregara\nel  vehiculo  a quien acredite la  propiedad.\nCosto del boleto perdido es de $100.00\n")
	Generic.text("Al recibir este boleto acepta las condiciones\ndel seguro contra robo total. PARKING TIP S.A\nDE  C.V.  -R.F.C PTI120210571. Escobillera 13\nCol.Paseos de Churubusco Iztapalapa CDMX C.P.\n09030 Horario de Lunes-Domingo de 7 a 22 hrs \n")

def imprimirQR(noBol,terminalEnt,fechaIn,horaEnt):
	Generic = printer.Usb(0x0519,0x0001)
	Generic.text('Expedidora #'+PATH_NUMERO_TERMINAL+'\n')
	Generic.text('Folio: GM'+str(noBol)+' '+fechaIn+' '+horaEnt +'\n')
	Generic.qr(noBol+"\n"+terminalEnt+"\n"+fechaIn+"\n"+horaEnt)
	Generic.cut()

#imprimirHeader()
#imprimirQR("GM:12","3","21/03/2017","8:00:00")

def imprimirBoletoT(folio,terminal,fecha):
	Generic = printer.Usb(0x0519,0x0001)
	codQR=imagen.cambiarTamQR(PATH_CODIGOS_QR)
	
	Generic = printer.Usb(0x0519,0x0001)
	Generic.set(size='2x', align='center')
	Generic.text('Bienvenido \n'+str(PATH_NOMBRE_PLAZA)+'\n')
	Generic.set(size='normal',align='center')
	Generic.text("La empresa no se hace responsable por objetos\npersonales,fallas mecanicas  y/o  electricas,\nsiestros ocasionados por derrumbes,temblores,\nterremotos o fenomenos naturales,asi como ro-\nbo de accesorios o vandalismo en su vehiculo.\n")
	Generic.text("Por robo total de acuerdo a los terminos  del\nseguro contratado.Boleto Perdido.Se entregara\nel  vehiculo  a quien acredite la  propiedad.\nCosto del boleto perdido es de $100.00\n")
	Generic.text("Al recibir este boleto acepta las condiciones\ndel seguro contra robo total. PARKING TIP S.A\nDE  C.V.  -R.F.C PTI120210571. Escobillera 13\nCol.Paseos de Churubusco Iztapalapa CDMX C.P.\n09030 Horario de Lunes-Domingo de 7 a 22 hrs \n")
	horaActual= time.strftime("%H:%M:%S")
	Generic.text('Folio: '+str(folio)+'\n')
	Generic.text('Expedirora #'+PATH_NUMERO_TERMINAL+' '+fecha+' '+horaActual +'\n')
	Generic.image(codQR)
	Generic.cut()
	
	
def imprimirBoletoC2(fecha,horaEntrada,costillo,folio,expedidora):
	global Generic
	#Generic = printer.Usb(0x0519,0x0001)
	print ("Bienvenido \n "+PATH_NOMBRE_PLAZA+"\n")
	print ("Expedirora: "+PATH_NUMERO_TERMINAL+"\n")
	print (fecha +"\n")
	#Generic = printer.Usb(0x0519,0x0001)
	Generic.set(size='2x', align='center')
	Generic.text(str(PATH_NOMBRE_PLAZA)+'\n\n')
	Generic.set(size='normal',align='center')
	
	#Generic.text('--------------------------------\n')
	#Generic.text("La empresa no se hace responsable por objetos\npersonales,fallas mecanicas  y/o  electricas,\nsiestros ocasionados por derrumbes,temblores,\nterremotos o fenomenos naturales,asi como ro-\nbo de accesorios o vandalismo en su vehiculo.\n")
	#Generic.text("Por robo total de acuerdo a los terminos  del\nseguro contratado.Boleto Perdido.Se entregara\nel  vehiculo  a quien acredite la  propiedad.\nCosto del boleto perdido es de $100.00\n")
	#Generic.text("Al recibir este boleto acepta las condiciones\ndel seguro contra robo total. PARKING TIP S.A\nDE  C.V.  -R.F.C PTI120210571. Escobillera 13\nCol.Paseos de Churubusco Iztapalapa CDMX C.P.\n09030 Horario de Lunes-Domingo de 7 a 22 hrs \n")
	horaActual= time.strftime("%H:%M:%S")
	Generic.text('Hora de entrada:'+horaEntrada +'    '+'Fecha: '+fecha+'\n'+'Hora de Pago:'+horaActual+'      '+'Pagado: $'+str(costillo)+'.00\n')	#Generic.image(codQR)
	Generic.qr(folio+"\n"+expedidora+"\n"+fecha+"\n"+horaEntrada+"\n"+horaActual+"\n"+str(costillo)+"\n")
	Generic.set(size='normal',align='center')
	Generic.text('\nPresentar al salir. Valido por 15 minutos\n')
	Generic.set(size='2x', align='center')
	Generic.text('Gracias por su visita!')
	Generic.cut()
	
	
def imprimirBoletoC(folio,terminal,fecha):
	Generic = printer.Usb(0x0519,0x0001)
	codQR=imagen.cambiarTamQR(PATH_CODIGOS_QR)
	print ("Bienvenido \n "+PATH_NOMBRE_PLAZA+"\n")
	print ("Terminos y condiciones")
	print ("Folio: "+str(folio)+"\n")
	print ("Expedirora: "+PATH_NUMERO_TERMINAL+"\n")
	print (fecha +"\n")
	print ("CODIGO QR: "+str(codQR))
	Generic = printer.Usb(0x0519,0x0001)
	Generic.set(size='2x', align='center')
	Generic.text(str(PATH_NOMBRE_PLAZA)+'\n\n')
	Generic.set(size='normal',align='center')
	
	#Generic.text('--------------------------------\n')
	#Generic.text("La empresa no se hace responsable por objetos\npersonales,fallas mecanicas  y/o  electricas,\nsiestros ocasionados por derrumbes,temblores,\nterremotos o fenomenos naturales,asi como ro-\nbo de accesorios o vandalismo en su vehiculo.\n")
	#Generic.text("Por robo total de acuerdo a los terminos  del\nseguro contratado.Boleto Perdido.Se entregara\nel  vehiculo  a quien acredite la  propiedad.\nCosto del boleto perdido es de $100.00\n")
	#Generic.text("Al recibir este boleto acepta las condiciones\ndel seguro contra robo total. PARKING TIP S.A\nDE  C.V.  -R.F.C PTI120210571. Escobillera 13\nCol.Paseos de Churubusco Iztapalapa CDMX C.P.\n09030 Horario de Lunes-Domingo de 7 a 22 hrs \n")
	horaActual= time.strftime("%H:%M:%S")
	Generic.text('Entrada:'+horaActual +'    '+'Fecha: '+fecha+'\n'+'Salida:'+horaActual+'    '+'Pagado: $100.00\n')
	Generic.image(codQR)
	
	Generic.set(size='normal',align='center')
	Generic.text('\nPresentar al salir. Valido por 15 minutos\n')
	Generic.set(size='2x', align='center')
	Generic.text('Gracias por su visita!')
	
	Generic.cut()


def imprimirBoleto(folio,terminal,fecha):
	Generic.set(size='2x', align='center')
	codQR=imagen.cambiarTamQR("output.png")
	Generic.set(size='2x',align='center')
	Generic.text("Macro Plaza"+"\n")
	Generic.text(" TECAMAC"+"\n")
	Generic.image("3.jpg")	
	Generic.set(size='normal')	
	Generic.text("Folio: "+str(folio)+"\n")
	Generic.text("Entrada: "+str(terminal)+"\n")
	Generic.text(fecha +"\n")
	Generic.set(size='2x', align='center')
	Generic.image(codQR)
	Generic.cut()
	pass


def header():
	Generic = printer.Usb(0x0519,0x0001)
	Generic.set(size='2x', align='center')
	Generic.text('Bienvenido \n'+str(PATH_NOMBRE_PLAZA))
	Generic.set(size='normal',align='center')

def footer():
	Generic.cut()

def informacionEXT():
	Generic.set(size='normal', align='center')
	Generic.text("Bienvenido\n\n")
	
def checale(fecha1,fecha2):
	global cur,generic
	fecha=hora.mostrarFechayHora()
	archivo = open("/home/pi/Documents/NoCajero.txt", "r")
	idCajero=str(archivo.readline().rstrip("\n"))
	archivo.close()
	
	pdf=FPDF()
	pdf.add_page()
	pdf.set_font('Arial','B',48)
	pdf.cell(30,10,'Reporte de Eventos\n')
	pdf.ln()
	pdf.ln()
	pdf.set_font('Arial','B',24)
	pdf.cell(30,10,fecha1.rstrip(' 00:00:00')+' - '+fecha2.rstrip(' 23:59:59'))
	fechaA=str(fecha1.rstrip(' 00:00:00')).replace("/","-")
	fechaB=str(fecha2.rstrip(' 23:59:59')).replace("/","-")
	pdf.ln()
	pdf.cell(30,10,"Cajero: "+str(idCajero))
	pdf.ln()
	pdf.ln()
	pdf.set_font('Arial','B',14)
	pdf.cell(45,10,'Fecha',1)
	pdf.cell(45,10,'Usuario',1)
	pdf.cell(45,10,'Evento',1)
	pdf.cell(55,10,'Detalle',1)
	pdf.set_font('Arial','',12)
	pdf.ln()
	cur.execute("select \"USUARIO\".nombre,\"LOG\".nombre,fecha,detalle from \"USUARIO_LOG\" left join \"USUARIO\" on \"USUARIO_LOG\".usuario=\"idUsuario\" left join \"LOG\" on \"USUARIO_LOG\".log=\"idLog\" WHERE fecha BETWEEN '"+fecha1+"' and '"+fecha2+"' order by fecha")
	for reg in cur: 
		print(reg[0],reg[1])
		pdf.cell(45,10,str(reg[2]),1)
		pdf.cell(45,10,str(reg[0]),1)
		pdf.cell(45,10,str(reg[1]),1)
		pdf.cell(55,10,str(reg[3]),1)
		pdf.ln()
	#pdf.output('reporteEventos.pdf','F')
	os.system("ls /media/pi/ > /home/pi/Documents/usbPath.txt")
	leerArch = open("/home/pi/Documents/usbPath.txt", "r")
	linea=leerArch.readline().rstrip("\n")
	if(linea!=''):
		print(linea)
		pdf.output('/media/pi/'+linea+'/reportes/reporteEventosDEL'+fechaA+'AL'+fechaB+'.pdf','F')
	else:
		print("MEMORIA NO CONECTADA")
leerArch = open("/home/pi/Documents/fechaEventos.txt", "r")
sp=leerArch.readline().split(',',2)
fecha1=sp[0]
fecha2=sp[1]
leerArch.close()
leerArch = open("/home/pi/Documents/fechaEventos.txt", "w")
leerArch.write('')
leerArch.close()
checale(fecha1,fecha2)
#imprimirBoletoC2(fe,he,str(costo),str(folio),str(expedidora))
