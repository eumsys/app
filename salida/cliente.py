
import sys
import socket
import argparse
import datetime
import os
import validacion as valida

tam_buffer = 150
host = '192.168.1.129'
port = 2324

def autorizaSalida(s, operacion, mensaje):
	# operacion de salida del automovil
	s.send(operacion.encode('utf-8'))
	# espera una trama de confirmacion
	if (s.recv(tam_buffer) == b'ack'):
		# Protocolo de comunicacion (idBoleto, idexpedidora, fecha boleto)
		s.send(mensaje.encode('utf-8'))
		#espera la respuesta de autorizacion de salida
		data = s.recv(tam_buffer)
		if (data != b'boleto no localizado'):
			datosDecoded = data.decode('utf-8')
			print("data: {}".format(datosDecoded))
			if(datosDecoded == "salida no autorizada: boleto no pagado"):
				##### Aqui va mensaje hacial el cliente indicando que realice el pago
				print("Favor de realizar su pago")
				respuesta = "pago no realizado"
			elif(datosDecoded == "salida autorizada: boleto pagado"):
				##### Aqui va mensaje hacia el cliente indicando que puede salir
				print("Gracias por su visita")
				respuesta = "finalizado"
			elif(datosDecoded == "salida no autorizada: tiempo de salida excedido"):
				##### Aqui va mensaje hacia el cliente indicando que el tiempo de salida se agoto, por lo tanto requiere volver a pagar
				print("Tiempo de salida excedido, favor de pagar")
				respuesta = "volver a pagar"
			elif (datosDecoded == "salida no autorizada: boleto obsoleto"):
				##### Aqui va mensaje hacia el cliente indicando que el tiempo de salida se agoto, por lo tanto requiere volver a pagar
				print("salida no autorizada, boleto obsoleto")
				respuesta = "boleto obsoleto"
			else:
				print("Pago no realizado, favor de realizar su pago")
				respuesta = "pago no realizado"
		else:
			print("Boleto No encontrado o no pagado")
			respuesta = "boleto no encontrado"
	else:
		print("NO se entrego la operacion")
		respuesta = "sin comunicacion servidor"
		s.close()
	return respuesta

def logSalida(s,operacion,mensaje):
	# operacion de inicio de sesion
	s.send(operacion.encode('utf-8'))
	# Espera una trama de confirmacion
	if (s.recv(tam_buffer) == b'ack'):
		# Realiza el envio de los datos del boleto a buscar
		s.send(mensaje.encode('utf-8'))
		data = s.recv(tam_buffer)
		print(data)
		if (data == b'log salida registrado'):
			respuesta = "Fin_log registrado"
		else:
			respuesta = "Error en registro log"
	else:
		respuesta = "NO se entrego la operacion"
	s.close()
	return respuesta

def configSocket(operacion,mensaje):
	global host,ip
	#Parseo de argumentos, identifico que se tiene que pasar 2 parametros por consola host:127.0.0.1 puerto: 1234
	'''parser = argparse.ArgumentParser(description='Socket Error Examples')
	parser.add_argument('--host', action="store", dest="host", required=True)
	parser.add_argument('--port', action="store", dest="port", type=int, required=True)
	given_args = parser.parse_args()
	host = given_args.host
	port = given_args.port'''


	# Bloque try - catch para crear el socket
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as e:
		print("Error al crear el socket: {}".format(e))
		sys.exit(1)

	# Bloque try - catch para conectarse al servidor
	try:
		conn = s.connect((host,port))
		print("Conexion al host: {} en el puerto: {}".format(host,port))
		print("--> conn {}".format(conn))
	except socket.gaierror as e:
		print("Error al conectar con el servidor: {}".format(e))
		return "error"
		sys.exit(1)
	except socket.error as e:
		print("Error de Conexion: {}".format(e))
		return "error"
		sys.exit(1)
	if operacion == "autorizacion salida":
		respuesta = autorizaSalida(s,operacion, mensaje)
	else:
		respuesta = logSalida(s,operacion, mensaje)
	s.close()
	return respuesta
