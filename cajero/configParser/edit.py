#!/usr/bin/python3
import configparser
import codecs
from os import system, name
from time import sleep

categorias = []
opciones = []

config = configparser.ConfigParser()

leido = config.read('configuracion.ini')

for section_name in config.sections():
	categorias += [section_name]
	opciones += [config.options(section_name)]


	

'''print("\t\tEditar archivo")
print("\t    Seleccione la categoria")
for i in range(0, len(categorias)):
	print("{} - {}".format((i+1), categorias[i]))

opcion = int(input("Ingrese opcion:"))
while( opcion > len(categorias) or opcion < 1):
	opcion = int(input("Ingrese una opcion valida:"))

sleep(0.3)
system('clear')
print("\t\tEditar archivo")
print("\t",categorias[(opcion-1)])
for x in range(0, len(opciones[(opcion-1)])):
	print("{} - {}".format((x+1), opciones[(opcion-1)][x]))
print("0 - Regresar")
opcion2 = int(input("Ingrese opcion:"))
while( opcion2 > len(opciones[(opcion-1)]) ):
	opcion2 = int(input("Ingrese una opcion valida:"))

sleep(0.3)
system('clear')
print("\t\tEditar archivo")
print("\t",categorias[(opcion-1)])
campo = opciones[(opcion-1)][(opcion2-1)]
print('{} = {}'.format(opciones[(opcion-1)][(opcion2-1)], config.get(str(categorias[(opcion-1)]), str(campo))))
print("0 - Regresar")'''





'''import configparser

config = configparser.ConfigParser()
config.read('FILE.INI')
print(config['DEFAULT']['path'])     # -> "/path/name/"
config['DEFAULT']['path'] = '/var/shared/'    # update
config['DEFAULT']['default_message'] = 'Hey! help me!!'   # create

with open('FILE.INI', 'w') as configfile:    # save
    config.write(configfile)'''