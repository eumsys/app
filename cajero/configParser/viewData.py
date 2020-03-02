#!/usr/bin/python3
import configparser
import codecs
from os import system, name
from time import sleep
import sys,os



ruta =  os.path.join(os.path.dirname(os.path.abspath(__file__)))
ruta = ruta + "/"
def obtenerUsuario(ruta):
	lista = ruta.split("/")
	return "/"+lista[1]+"/"+lista[2]+"/"	
rutaUsuario = obtenerUsuario(ruta)
print(rutaUsuario)



class viewData():
	def __init__(self,archivo):
		self.archivo = archivo
		self.categorias = []
		self.opciones = []

		self.config = configparser.ConfigParser()
		self.config.read(ruta+self.archivo)

		for section_name in self.config.sections():
			self.categorias += [section_name]
			self.opciones += [self.config.options(section_name)]
		print("opc",self.opciones)

	def menuCategorias(self):

		sleep(0.3)
		system('clear')
		print("\t\tEditar archivo")
		print("\t    Seleccione la categoria")
		for i in range(0, len(self.categorias)):
			print("{} - {}".format((i+1), self.categorias[i]))
		print("0 - Salir")

		opcion = int(input("\nIngrese opcion: "))
		while( opcion > len(self.categorias) ):
			opcion = int(input("\nIngrese una opcion valida: "))

		if( opcion == 0 ):
			sys.exit(0)
		else:
			self.menuElemento(opcion)		


	def menuElemento(self, opcion):


		sleep(0.3)
		system('clear')
		print("\t\tEditar archivo")
		print("\t    Seleccione el elemento")
		print("\t",self.categorias[(opcion-1)])
		for x in range(0, len(self.opciones[(opcion-1)])):
			print("{} - {}".format((x+1), self.opciones[(opcion-1)][x]))
		print("0 - Regresar")

		opcion2 = int(input("\nIngrese opcion: "))
		while( opcion2 > len(self.opciones[(opcion-1)]) ):
			opcion2 = int(input("\nIngrese una opcion valida: "))

		if( opcion2 == 0 ):
			self.menuCategorias()
		else:
			self.printElemento(opcion, opcion2)


	def printElemento(self, opcion, opcion2):
		sleep(0.3)
		system('clear')
		print("\t\tEditar archivo")
		print("\t",categorias[(opcion-1)])
		campo = self.opciones[(opcion-1)][(opcion2-1)]
		print('{} = {}'.format(self.opciones[(opcion-1)][(opcion2-1)], self.config.get(str(self.categorias[(opcion-1)]), str(campo))))
		print("\n1 - Editar")
		print("0 - Regresar")

		opcion3 = int(input("\nIngrese opcion: "))
		while( opcion3 > 1 ):
			opcion3 = int(input("\nIngrese una opcion valida: "))

		if( opcion3 == 1 ):
			self.editarElemento(campo, opcion, opcion2)
		elif( opcion3 == 0 ):
			self.menuElemento(opcion)



	def editarElemento(self, campo, opcion, opcion2):
		global config
		print("\nIngrese nuevo valor para ", campo, ": ")
		update = str(input())
		config[(self.categorias[(opcion-1)])][self.opciones[(opcion-1)][(opcion2-1)]] = update
		with open(ruta+self.archivo, 'w') as configFile:
			config.write(configFile)
		self.printElemento(opcion, opcion2)


	def getValue(self, categoria, opcion):
		try:
			valor = self.config.get(str(categoria), str(opcion))
			#print(valor)
		except:
			print("No se encontro el valor")
			valor = ""
		return valor


	def editValue(self, categoria, opcion, update):
		#print("\nIngrese nuevo valor para ", opcion, ": ")
		#update = str(input())
		self.config[str(categoria)][str(opcion)] = update
		with open(ruta+self.archivo, 'w') as configFile:
			self.config.write(configFile)


def main():
	vizualizar = viewData()
	vizualizar.getInfo()
	vizualizar.getValue('RED','gateway')
	vizualizar.editValue('RED','gateway')
	#vizualizar.menuCategorias()


if __name__ == "__main__":
    main()