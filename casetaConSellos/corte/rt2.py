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
from escposprinter import *#original funcional
import tratarImagen as imagen
import configuracionEXP as archivoConfiguracion
import time
import psycopg2, psycopg2.extras
import fechaUTC as hora
import datetime
import qrcode



PATH_NOMBRE_PLAZA=str(archivoConfiguracion.getName()).replace('\n','')
PATH_NUMERO_TERMINAL=str(archivoConfiguracion.getNumTer()).replace('\n','')
PATH_CODIGOS_QR="/home/pi/Documents/eum/app/caseta/EUM_EXPE/CodigosQR/outputQR.png"
dats=''
conn = psycopg2.connect(database='CajerOk',user='postgres',password='Postgres3UMd6', host='localhost')
cur = conn.cursor()


tipos=[0,0,0,0,0,0,0,0]
#Generic = printer.Usb(0x0519,0x0001)
#Generic = printer.Usb(0x04b8,0x0202)

def imprimirHeader():
	Generic = printer.Usb(0x0519,0x0001)

	Generic.set(size='2x', align='center')
	Generic.text('Bienvenido \n'+str(PATH_NOMBRE_PLAZA)+'\n')
	Generic.set(size='normal',align='center')
	Generic.text("La empresa no se hace responsable por objetos\npersonales,fallas mecanicas  y/o  electricas,\nsiestros ocasionados por derrumedbes,temblores,\nterremotos o fenomenos naturales,asi como ro-\nbo de accesorios o vandalismo en su vehiculo.\n")
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
	
def checale(fecha1,fecha2,turno,folio):
	global cur,generic,dats,tipos
	boletaje=''
	fecha=hora.mostrarFechayHora()
	archivo = open("/home/pi/Documents/eum/app/caseta/NoCajero.txt", "r")
	idCajero=str(archivo.readline().rstrip("\n"))
	archivo.close()
	"""Generic.set(size='2x', align='center')
	Generic.text("INGRESO ")
	Generic.text("VESPERTINO \n")
	Generic.text("CAJA "+str(idCajero)+"\n\n")
	Generic.set(size='normal', align='center')
	Generic.text("Ultimo corte: "+fecha1)
	Generic.text("\nHora actual: "+fecha+"\n\n")
	Generic.set(size='normal', align='left')
	"""
	tot=''
	cur.execute("select costo,COUNT(\"idBoleto\") from \"BOLETO\" where \"fechaExpedicion\" BETWEEN '"+fecha1+"' and '"+fecha2+"' group by costo ")
	for reg in cur: 
		#print(reg[0],reg[1])
		#Generic.text('Boletos de '+str(reg[0])+' --> '+str(reg[1])+'\n')
		boletaje=boletaje+str(reg[1])+':'+str(int(reg[0]))+'\n'
	print(boletaje)
		
	cur.execute("select SUM(\"costo\") from \"BOLETO\" where \"fechaExpedicion\" BETWEEN '"+fecha1+"' and '"+fecha2+"'")
	for reg in cur: 
		#print("AAAS"reg[0])
		#Generic.text('\nDinero total:'+str(reg[0])+'\n\n')
		tot=str(reg[0])
		if(tot=='None'):
			tot=0
		else:
			tot=int(reg[0])
	#print(dats)
	conn = psycopg2.connect(database='CajerOk',user='postgres',password='Postgres3UMd6', host='localhost')
	cur = conn.cursor()
	cur2 = conn.cursor()
	print(fecha1,fecha2)
	cur.execute("select tipo,COUNT(\"idBoleto\") from \"BOLETO\" where \"fechaExpedicion\" BETWEEN '"+fecha1+"' and '"+fecha2+"' group by tipo ")
	for rega in cur: 
		print("tipazos",rega[0],rega[1])
		cur2.execute("select nombre from \"TIPO\" where \"idTipo\"="+str(rega[0])+"")
		for reg in cur2: 
			print(reg[0])
			
		#Generic.text('Pagos '+str(reg[0])+' --> '+str(rega[1])+'\n')
		print("TIPOSSSSSSSSSSSSSSSSS1",tipos)
		print("TIPOSSSSSSSSSSSSSSSSS2",rega[0],rega[1])
		
		tipos[int(rega[0])-1]=(rega[1])
		print("TIPOSSSSSSSSSSSSSSSSS3",tipos)
		dats=dats+'Pagos '+str(reg[0])+' --> '+str(rega[1])+'\n'
		
	#print(dats)
	cur.execute("select SUM(\"costo\") from \"BOLETO\" where \"fechaExpedicion\" BETWEEN '"+fecha1+"' and '"+fecha2+"'")
	for reg in cur: 
		print(reg[0])
		#Generic.text('Dinero total:'+str(reg[0])+'\n\n')

	#Generic.cut()
	##tipos[5]:Cobrados,tipos6:Incompletos,tipos4:propina, tipos7:s/propina, tipos2: Perdidos
	sinSello='0'
	locales='0'
	cancelados='0'
	proovedores='0'
	tolerancias='0'
	
	cortesias='0'
	gastos='0'
	nomina='0'
	bonos='0'
	dobletes='0'
	anticipoDeDepositos='0'
	
	dats=folio+";"+"Quintana"+"; ;"+fecha+";"+str(idCajero)+";"+turno+";"+str(sinSello)+";"+str(tipos[5])+";"+str(tipos[6])+";"+str(tipos[4])+";"+str(tipos[7])+";"+locales+";"+cancelados+";"+proovedores+";"+tolerancias+";"+str(tipos[2])+";"+str(tot)+";"+boletaje+";"+cortesias+";"+gastos+";"+nomina+";"+bonos+";"+dobletes+";"+anticipoDeDepositos
	qr= qrcode.QRCode(
		version=4,
		box_size=7,
		border=4,
	)
	qr.add_data(dats)
	qr.make(fit=True)
	img= qr.make_image(back_color='black')
	f = open("/home/pi/Documents/eum/app/iconos/outputQR2.png", "wb")
	img.save(f)
	f.close()




hoy=datetime.datetime.today()
ayer=hoy+datetime.timedelta(days=-1)
m=str(ayer).split(" ")
n=m[0].split("-")
fechaayer=n[2]+"/"+n[1]+"/"+n[0]


hoy=datetime.datetime.today()
a=str(hoy).split(" ")
b=a[0].split("-")
fec=b[2]+"/"+b[1]+"/"+b[0]


#horaEnt=time.strftime("%H:%M:%S")
#fec=fec+','+horaEnt+','+str(aux_tarifa)
#fecha1=fec+" 15:00:00"
#fecha2=fec+" 22:00:00"
horaEnt=time.strftime("%H:%M:%S")
infile = open("/home/pi/Documents/eum/app/caseta/archivos_config/fechaDeCorte.txt", 'r')
c=infile.readline()
infile.close()
c=c.split(',')

fecha2=fec+" "+str(horaEnt)
fecha1=c[0]
turno=c[1]
folio=c[2]
print(fecha1,fecha2)
#checale(fecha1,fecha2)
checale(fecha1,fecha2,str(turno),str(folio))
#checale(fecha1,fecha2,turno)
#imprimirBoletoC2(fe,he,str(costo),str(folio),str(expedidora))
