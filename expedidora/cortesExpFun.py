# -*- coding: utf-8 -*-
#cortesExpFun

from datetime import datetime
import time, os
import fechaUTC as tiempo
#import commands
import sys
#import psycopg2	
#from escposprinter import *
import coneccionExp as con
import leerTXTconfiguracion as configTXT

import configuracionEXP as archivoConfiguracion
PATH_NOMBRE_PLAZA=str(archivoConfiguracion.getName())
DIRECCION_PLAZA=str(archivoConfiguracion.getDireccion())
terminalEnt=int(archivoConfiguracion.getNumTer())


"""
Generic = printer.Usb(0x0519,0x0001)
def header():
	
	Generic.set(size='2x', align='center')
	Generic.text('Bienvenido \n Plaza del Sauz \n')
	Generic.set(size='normal')
"""
def elijeCorte(tipoCorte, mifechacorte1, mifechacorte2, miterminalcorte, user):
	if tipoCorte==1:
		corteDeCaja(mifechacorte1,miterminalcorte,user)		
	if tipoCorte==2:
		cortePorTarifa(mifechacorte1,mifechacorte2,miterminalcorte,user)		
	if tipoCorte==3:
		corteEntreFechas(mifechacorte1,mifechacorte2,miterminalcorte,user)

def corteDeCaja(fin,miterminalcorte,user):
	var1=str(fin)
	var2=str(miterminalcorte)

	query="SELECT sum(tot_bol) as total FROM \"Boleto\"   WHERE out_fec_bol  like'"+var1+"' and out_ter_bol ='"+var2+"'"
	objetoConexion = con.Conexion()
	resultado=objetoConexion.doQuery(str(query))
	
	if resultado==-1:
		print (" ERRO DE QUERY")
		pass
	else:
		print ("Usuario: "+str(user)+" Caja:"+str(miterminalcorte)+"\nFecha: ["+var1+"]\nTotal: ["+str(resultado)+"]")
	#header()
	#Generic.set(size='normal', align='center')
	#Generic.text("Usuario: "+str(user)+" Caja:"+str(miterminalcorte)+"\nFecha: ["+var1+"]\nTotal: ["+str(resultado)+"]")
	#footer()
	pass

def cortePorTarifa(fin,fout,t,user):
	var1=str(fin)
	var2=str(fout)
	var3=str(t)
	#TARIFA 1
	query="SELECT sum(tot_bol) as total FROM \"Boleto\"  WHERE id_tar_bol =1 and out_fec_bol between'"+var1+"' and '"+var2+"' and out_ter_bol='"+var3+"'"
	#uery="SELECT sum(tot_bol) as total, Boleto.id_tar_bol FROM \"Boleto\"  WHERE out_fec_bol between'"+var1+"' and '"+var2+"' and out_ter_bol='"+var3+"'"
	objetoConexion = con.Conexion()
	resultado=objetoConexion.doQuery(str(query))
	print("Usuario: "+str(user)+" Caja:"+str(var3))
	#header()
	#Generic.text("Usuario: "+str(user)+" Caja:"+str(var3))

	if resultado==-1:
		print (" ERRO DE QUERY")
		pass
	else:
		print ("Tarifa [1] Total["+str(resultado)+"]")
		#Generic.text("Tarifa [1] Total["+str(resultado)+"]")
	#TARIFA 2
	query="SELECT sum(tot_bol) as total FROM \"Boleto\"  WHERE id_tar_bol =2 and out_fec_bol between'"+var1+"' and '"+var2+"' and out_ter_bol='"+var3+"'"
	#objetoConexion = con.Conexion()
	resultado=objetoConexion.doQuery(str(query))
	if resultado==-1:
		print (" ERRO DE QUERY")
		pass
	else:
		print ("Tarifa [2] Total["+str(resultado)+"]")
		#Generic.text("Tarifa [3] Total["+str(resultado)+"]")

	#TARIFA 3
	query="SELECT sum(tot_bol) as total FROM \"Boleto\"  WHERE id_tar_bol =3 and out_fec_bol between'"+var1+"' and '"+var2+"' and out_ter_bol='"+var3+"'"
	#objetoConexion = con.Conexion()
	resultado=objetoConexion.doQuery(str(query))
	if resultado==-1:
		print (" ERRO DE QUERY")
		pass
	else:
		print ("Tarifa [3] Total["+str(resultado)+"]")
		#Generic.text("Tarifa [3] Total["+str(resultado)+"]")
	#TARIFA 3
	query="SELECT sum(tot_bol) as total FROM \"Boleto\"  WHERE id_tar_bol =4 and out_fec_bol between'"+var1+"' and '"+var2+"' and out_ter_bol='"+var3+"'"
	#objetoConexion = con.Conexion()
	resultado=objetoConexion.doQuery(str(query))
	if resultado==-1:
		print (" ERRO DE QUERY")
		pass
	else:
		print ("Tarifa [4] Total["+str(resultado)+"]")
		#Generic.text("Tarifa [4] Total["+str(resultado)+"]")
	#TARIFA 3
	query="SELECT sum(tot_bol) as total FROM \"Boleto\"  WHERE id_tar_bol =5 and out_fec_bol between'"+var1+"' and '"+var2+"' and out_ter_bol='"+var3+"'"
	#objetoConexion = con.Conexion()
	resultado=objetoConexion.doQuery(str(query))
	if resultado==-1:
		print (" ERRO DE QUERY")
		pass
	else:
		print ("Tarifa [5] Total["+str(resultado)+"]")
		#Generic.text("Tarifa [5] Total["+str(resultado)+"]")
	#TARIFA 3
	query="SELECT sum(tot_bol) as total FROM \"Boleto\"  WHERE id_tar_bol =6 and out_fec_bol between'"+var1+"' and '"+var2+"' and out_ter_bol='"+var3+"'"
	#objetoConexion = con.Conexion()
	resultado=objetoConexion.doQuery(str(query))
	if resultado==-1:
		print (" ERRO DE QUERY")
		pass
	else:
		print ("Tarifa [6] Total["+str(resultado)+"]")
		#Generic.text("Tarifa [6] Total["+str(resultado)+"]")
		
	#footer()
pass


def corteEntreFechas(fin,fout,t,user):
	var1=str(fin)
	var2=str(fout)
	var3=str(t)
	query="SELECT sum(tot_bol) as total FROM \"Boleto\"  WHERE out_fec_bol between'"+var1+"' and '"+var2+"' and out_ter_bol='"+var3+"'"
	objetoConexion = con.Conexion()
	resultado=objetoConexion.doQuery(str(query))
	if resultado==-1:
		print (" ERRO DE QUERY")
		pass
	else:
		#header()
		print ("Usuario: "+str(user)+" Caja:"+str(var3)+" \nFecha desde: ["+var1+"] Fecha hasta: ["+var2+"]\nTotal:["+str(resultado)+"]")
		#Generic.text("Usuario: "+str(user)+" Caja:"+str(var3)+" \nFecha desde: ["+var1+"] Fecha hasta: ["+var2+"]\nTotal:["+str(resultado)+"]")
		#footer()
	pass

pass


"""
Query's de Insertar la configuracion en la base de datos
"""
def agregarCentroComercial(nombrePlaza,localidad_Estado,localidad_Muni,numeroTerminal):
	direccionCentroComercial=localidad_Muni+" "+localidad_Estado
	print ("Nombre de la plaza: "+ nombrePlaza )
	print ("Direccion de la plaza: "+direccionCentroComercial)
	print ("Numero de terminal: "+ numeroTerminal)

	#fALTAN VALIDACIONES DE CONSISTENCIA DE DATOS

	#Insertamos en la tabla Centro Comercial
	query="INSERT INTO \"CentroComercial\" ( cen_com_nom, cen_com_dir) VALUES ('"+nombrePlaza+"',  '"+direccionCentroComercial+"');"
	#print(query)
	print ("\t Comienza el query...")
	objetoConexion = con.Conexion()
	f = objetoConexion.execQuery(query)
	if(f<0):
		print("Error: Los datos no se guardaron en Centro comercial")
	else:
		print ("\t----Exito al insertar en centro comercial")
		#Insertamos en la expedidora primero necesitamos saber cual es el ID DE CENTRO COMERCIAL QUE LE PUSIMOS
		query="SELECT id_cen_com  FROM \"CentroComercial\" WHERE cen_com_nom='"+nombrePlaza+"';"
		objetoConexion = con.Conexion()
		resultado=objetoConexion.doQuery(str(query))
		if resultado==-1:
			print (" ERRO DE QUERY")
			pass
		else:
			print ("\t----EL Id de centro comercial: "+str(resultado[0][0]))
			ID_cen_com_querybase=int(resultado[0][0])
			pass
			query="INSERT INTO \"Expedidora\"(id_exp, id_exp_cc)VALUES ('"+str(numeroTerminal)+"','"+str(ID_cen_com_querybase)+"') ;"
			#print(query)
			objetoConexion = con.Conexion()
			f = objetoConexion.execQuery(query)
			if(f<0):
				print("Error: El dato no se guardo en expendidora")
			else:
				print ("\t----Exito al insertar en expedidora")
	print ("\t Termina el query...")

	
"""
Cortes de la expedidora
Por día:
	Corte 1
		2017-02-13
Entre fechas:	
	Corte 2
		2017-02-13
		2017-02-13
"""

def elijeCorte1PorDia(fechaDia):
	query="SELECT count( id_bol_exp)  FROM \"boletoexpedidora\" WHERE fec_bol_exp BETWEEN '"+fechaDia+"' AND '"+fechaDia+"' ;"
	objetoConexion = con.Conexion()
	resultado=objetoConexion.doQuery(str(query))
	if resultado==-1:
		print ("***********ERRO DE QUERY en CORTE POR FECHA")
		pass
	else:
		print ("\t----Los boletos totales: "+str(resultado[0][0]))
		pass

def elijeCorte2EntreFecha(fechaInicio,fechaFin):
	query="SELECT count( id_bol_exp)  FROM \"boletoexpedidora\" WHERE fec_bol_exp BETWEEN '"+fechaInicio+"' AND '"+fechaFin+"' ;"
	objetoConexion = con.Conexion()
	resultado=objetoConexion.doQuery(str(query))
	if resultado==-1:
		print ("***********ERRO DE QUERY en CORTE ENTRE FECHAS")
		pass
	else:
		print ("\t----Los boletos totales: "+str(resultado[0][0]))
		pass
	pass

def checarFecha():
	query="select max(fec_bol_exp) from boletoExpedidora;"
	objetoConexion = con.Conexion()
	f = objetoConexion.doQuery(query)
	r = f[0][0].strftime("%d-%m-%Y")
	print(r)
	print(tiempo.fechaConFormato())
	if r != tiempo.fechaConFormato():
		escribeArch = open("/home/pi/Documents/eum/app/expedidora/archivos_config/UltimoFolio.txt","w")
		res = 0
		escribeArch.write(str(res)+"\n")
		escribeArch.close()	

def insertarBoleto(nombrePlaza,numeroTerminal,folio,fechaIn,placa):
	nombrePlaza=nombrePlaza.replace('\n','')
	print ("Nombre de la plaza: "+ nombrePlaza )
	print ("Numero de terminal: "+ str(numeroTerminal))
	print ("Folio "+folio)
	print ("Fecha in: "+fechaIn)
	print ("Placa "+placa)
	#Insertamos en la tabla Centro Comercial
	query="INSERT INTO \"boletoexpedidora\"( fol_bol_exp, fec_bol_exp, pla_bol_exp) VALUES ( '"+folio+"', '"+fechaIn+"','"+placa+"');"
	print ("\t Comienza el query...")
	objetoConexion = con.Conexion()
	f = objetoConexion.execQuery(query)
	if(f<0):
		print("Error: Los datos no se guardaron en Centro comercial")
	else:
		print ("\t----Exito al insertar en Boleto expedidora")
		#Insertamos en la expedidora primero necesitamos saber cual es el ID DE CENTRO COMERCIAL QUE LE PUSIMOS
		query="SELECT id_cen_com  FROM \"CentroComercial\"  WHERE cen_com_nom='"+nombrePlaza+"' ;"
		objetoConexion = con.Conexion()
		resultado=objetoConexion.doQuery(query)
		print(resultado)
		if resultado==-1:
			print (" ERROR DE QUERY")
			pass
		else:
			#print ("\t----EL Id de centro comercial: "+str(resultado[0][0]))
			ID_cen_com_querybase=int(resultado[0][0])
			q = "SELECT MAX(id_bol_exp) FROM \"boletoexpedidora\";"
			conexion = con.Conexion()
			q = conexion.doQuery(q)
			if q==-1:
				print ("ERROR QUERY 3")
			else:
				print (str(q[0][0]))
				id_bol_last=str(q[0][0])
				query="UPDATE \"Expedidora\"   SET id_exp_bol='"+str(id_bol_last)+"'  WHERE id_exp='"+str(numeroTerminal)+"' AND id_exp_cc='"+str(ID_cen_com_querybase)+"';"
				objetoConexion = con.Conexion()
				f = objetoConexion.execQuery(query)
				if(f<0):
					print("Error: El boleto no se guardo en expendidora")
				else:
					print ("\t----Exito al insertar en expedidora")
	print( "\t Termina el query...")

print ("Nombre de la Plaza "+str(PATH_NOMBRE_PLAZA))
print ("Numero de Expedidora "+str(terminalEnt))
#insertarBoleto(PATH_NOMBRE_PLAZA,terminalEnt,"AG:300",'12/02/2017','JJJO')
#elijeCorte1PorDia("2017-01-03")

""""
def footer():
	Generic.set(align='left')
	Generic.text("    					  \n")
	Generic.text("     Firma Supervisor        Firma Usuario\n")
	Generic.text("    					  \n")
	Generic.text("    					  \n")
	Generic.text("   ===================	  ======================\n")
	Generic.cut()
"""
