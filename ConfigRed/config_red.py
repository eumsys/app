#!/usr/bin/env python

#Se importa el modulo netifaces
import os, sys


PASSWORD = "pi"
PUERTAENLACE = "148.204.57.254"


#instala la biblioteca python-netifaces
os.system("echo " + PASSWORD + " | sudo -S  apt install python-netifaces")
#se instala las herramientas de wireless
os.system("echo " + PASSWORD + " | sudo -S apt install wireless-tools")
        

import netifaces



''' Comandos para configurar red inalambrica
    ifconfig wlan0 up
    iwconfig wlan0 essid ESSID key CONTRASENA
    dhclient wlan0 
'''

''' Comandos para configurar red
    os.system("echo" + PASSWORD + " | sudo -S ifconfig " + i + " down")
    os.system("echo" + PASSWORD + " | sudo -S ifconfig " + i + " 192.168.1.10 netmask 255.255.255.0")
    os.system("echo" + PASSWORD + " | sudo -S route add default gw 192.168.1.254 " + i)
    os.system("echo" + PASSWORD + " | sudo -S " + i + " up")
'''

'''
datos = ["# This file describes the network interfaces available on your system\n",
                "auto " + interfaz + " \n", "iface " + interfaz + " inet static\n",
                "address " + dirIp + " \n", "netmask " + "255.255.255.0 \n",
                "network " + NETWORK + " \n", "broadcast " + BROADCAST + " \n",
                "gateway " + PUERTAENLACE + " \n"]
                '''

def CambioNombre(nomDispositivo):
    try:
        # se abre el archivo para ir obteniendo las cadenas de configuracion de los dispositivos
        a = open("/etc/hosts", "r")
        # se obtiene e contenido del archivo
        hosts = a.readlines()
        # Se cierra el archivo
        a.close()

        # Se vuelve a abrir el archivo pero en modo escritura para que se elimine su contenido y se escriban los cambios realizados
        a = open("/etc/hosts", "w")
        for linea in hosts:
            if (linea.find('127.0.1.1') != -1):
                print("\nencontro la linea: {}".format(nomDispositivo))
                linea = "127.0.1.1 \t" + nomDispositivo + " \n"
            a.write(linea)
        # se cierra el archivo
        a.close()
     
        ##Despues se asigna el mismo nombre en el archivo hostname
        # Se vuelve a abrir el archivo pero en modo escritura para que se elimine su contenido y se escriban los cambios realizados
        a = open("/etc/hostname", "w")
        a.write(nomDispositivo + " \n")
        a.close()

        #Se ambia el valor de la variable de entorno $HOSTNAME
        os.system("echo " + PASSWORD + " | sudo -S export $HOSTNAME="+nomDispositivo)
        #Se actualiza e servicio de hostname
        os.system("echo " + PASSWORD + " | sudo -S /etc/init.d/hostname.sh")
        
        print("\n---- Se cambio correctamente el nombre del host a: " + nomDispositivo +" ----\n")

    except OSError as err:
        print("Error OS: {0}".format(err))
    except:
        print("Error inesperado:", sys.exc_info()[0])
        raise

def AsignaIp(dirIp, interfaz):
    try:
        # se abre el archivo en modo lectura
        a = open("/etc/network/interfaces", "r")
        #se obtiene e contenido del archivo
        contenido = a.readlines()
        #Cierra el archivo
        a.close()
        
        datos = ["\n\n#Configuracion estatica\n",
        "interface " + interfaz + "\n",
        "static ip_address=" + dirIp + "/24 \n",
        "static routers=" + PUERTAENLACE + " \n", 
        "static domain_name_servers=8.8.8.8 \n",
        "static domain_search=8.8.4.4 \n",
        "inform " + interfaz + "\n"]
        
        # se abre el archivo en modo escritura para limpiar el archivo y escribir el nuevo contenido
        a = open("/etc/dhcpcd.conf", "a")
        #se agregan los datos
        for i in datos:
            a.write(i)
          
        #Cierra el archivo
        a.close()

        #Se reinicia el servicio de networking
        os.system("echo " + PASSWORD + " | sudo -S /etc/init.d/networking restart")
        os.system("echo " + PASSWORD + " | sudo -S ifconfig " + interfaz + " down")
        os.system("echo " + PASSWORD + " | sudo -S ifconfig " + interfaz + " up")
        os.system("echo " + PASSWORD + " | sudo -S ifconfig wlan0 down")
        os.system("echo " + PASSWORD + " | sudo -S ifconfig wlan0 up")
        print("\n---- Se cambio correctamente la direccion IP de Ethernet a: " + dirIp +" ----\n")
    except OSError as err:
        print("Error OS: {0}".format(err))
    except:
        print("Error inesperado:", sys.exc_info()[0])
        raise

def InsertaBD(instrucciones):
    try:
        res = os.system("PGPASSWORD=Postgres3UMd6 psql dbeum_tecamac -h localhost -U postgres -c \'" + instrucciones[2] + "\'")
        if (res != 0):
            print("---- No se realizo la insercion del dispositivo: " + instrucciones[0] + " en la BD local ----\n")
        else:
		    print("\n---- Se agrego correctamente el nombre del dispositivo: " + instrucciones[0] + " a la BD local ----\n")	
    except OSError as err:
        print("Error OS: {0}".format(err))
    except:
        print("Error inesperado:", sys.exc_info()[0])
        raise

if __name__ == "__main__":
    if (len(sys.argv) < 1):
        print("\n Falta un agregar parametro en la ejecucion: ./config_res.py archivo.txt")
        exit(1)
    try:
       
        #Se captura la lista de interfaces en el equipo
        interfaces = netifaces.interfaces()
        #Se muestra las interfaces
        #print ("\ninterfaces: {}").format(interfaces)

        for i in interfaces:
            if i == 'eth0':
                #se abre el archivo para ir obteniendo las cadenas de configuracion de los dispositivos
                archivo = open(sys.argv[1], "r")
                #se obtiene e contenido del archivo
                contenido = archivo.readlines()
                #Se cierra el archivo
                archivo.close()
                #Se valida que el archivo no este vacio
                if (len(contenido) == 0):
				    print("\n*****El archivo esta vacio, ya no hay configuraciones por hacer*******\n")
                else:
					#Se obtiene el contenido de la primera linea del archivo, esta posteriormente sera eliminada
					instrucciones = contenido[0].split(",")
					
					# Se elimina la primera linea
					contenido.pop(0)
					#se abre el archivo en modo escritura para borrar su contenido
					archivo = open(sys.argv[1], "w")
					#se escribe el arreglo en el archivo
					for linea in contenido:
						archivo.write(linea)
					#Se cierra el archivo
					archivo.close()
					
					#**********  Comienzan las operaciones de configuraion de los dispositivos ********************
					#funcion que cambia el nombre del dispositivo a nivel SO
					CambioNombre(instrucciones[0])
			
					#funcion que asigna la direccion IP
					AsignaIp(instrucciones[1], i)

					#Escribe dispositivo en la BD local
					InsertaBD(instrucciones)
            
            if (i == "wlan0"):
                 pass 
                 
        print("\n ********   Finalizo la ejecucion del script **************** ")
        print("\n **** NOTA: Favor de verificar los mensajes generados en la pantalla para asegurarse que no se generaron errores.  ****")
        print("\n\n ------- Introduce un Enter para continuar y reiniciar el equipo  ------")
        raw_input()
        os.system("echo " + PASSWORD + " | sudo -S reboot")   
    except OSError as err:
        print("Error OS: {0}".format(err))
    except:
        print("Error inesperado:", sys.exc_info()[0])
        raise

        

