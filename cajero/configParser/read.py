#!/usr/bin/python3
import configparser
import codecs

categorias = []
opciones = []
valores = []

config = configparser.ConfigParser()

config.read('configuracion.ini')

for section_name in config.sections():
	print(section_name)
	#print(config.options(section_name))
	for name, value in config.items(section_name):		
		print('	{} = {}'.format(name, value))