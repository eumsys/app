import time

def validar15min(fechaValidar):	
	tiempo_st = time.strptime(fechaValidar , "%Y-%m-%d %H:%M:%S")
	print(tiempo_st)
	resultado = time.mktime(time.localtime()) - time.mktime(tiempo_st)
	if resultado > 900:
		respuesta = "fuera"
	else:
		respuesta = "dentro"
	return respuesta

validar15min("2017-02-21 21:02:21")