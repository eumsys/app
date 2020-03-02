
import time
import threading


class Temporizador():


	def __init__(self, nombre, tiempo):
		self.nombre = nombre

		
		self.entrada = False
		self.salida = False
		self.tiempo = tiempo
		self.tiempoActual = 0

		self.bandera = False
		self.tiempo_Aux1 = 0
		self.tiempo_Aux2 = 0

		"""
		self.hiloFuncionando = False
		hilo1 = threading.Thread(target=self.actualizarHilo)
		print ("Iniciado hilo TON")
		hilo1.start()""" 

	def iniciar (self, energizar):
		self.energizar = energizar
		#self.hiloFuncionando = False
		hilo1 = threading.Thread(target=self.actualizarHilo)
		print ("Iniciado hilo TON")
		hilo1.start()


	def actualizar (self):

		if self.entrada:
			if not self.bandera:
				self.bandera = True
				self.tiempo_Aux1 = time.time()
			self.tiempo_Aux2 = time.time()
			self.tiempoActual = self.tiempo_Aux2 - self.tiempo_Aux1

			if self.tiempoActual > self.tiempo:
				self.salida = True
		else:
			self.salida = False
			self.bandera = False

	def actualizarHilo (self):
		self.hiloFuncionando = True
		while self.hiloFuncionando:
			self.actualizar()
			time.sleep (0.001)

			if not self.energizar.energizar:
				self.hiloFuncionando = False
			print ("TON ", self.entrada, self.tiempo, self.tiempoActual, self.salida)
		print ("Hilo terminado ", self.nombre)
			
			#print ("TON ", self.salida, self.tiempoActual)

	def stop (self):
		self.self.hiloFuncionando = False


def main ():
    
    TON_01 = Temporizador("TON_01", 16)
    
    TON_02 = Temporizador("TON_02", 2)
    TON_03 = Temporizador("TON_03", 2)

    while True:
    	TON_01.entrada = 1
    	TON_01.actualizar()
        
        
    	#TON_02.entrada = TON_01.salida & (not TON_02.salida)
    	#TON_02.actualizar()
        
        

    	print (TON_01.entrada, TON_01.salida, TON_01.tiempoActual, TON_01.tiempo)
    	#print (TON_02.entrada, TON_02.salida, TON_02.tiempoActual, TON_02.tiempo, "\n")
        
    	






if __name__ == "__main__":
    main ()
