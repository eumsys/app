from threading import Thread
import os

archivo= "1.mp4"

#"lxterminal -e sudo python /home/pi/Desktop/Ticket/first.py   "
#omxplayer  --loop --win  \"500 0 1400 800\" /home/pi/Videos/admi/"+archivo+"
PATH_EJECUTAR_EXPE="/home/pi/Documents/EUM_EXPE/first.py"
PATH_EJECUTAR_VIDEO_EXP="/home/pi/Videos/admi/"

def  ejecutaTiket():
	os.system("lxterminal -e sudo python "+PATH_EJECUTAR_EXPE)


def  ejecutaVideo():
	os.system("omxplayer  --loop --win  \"500 0 1400 800\" "+PATH_EJECUTAR_VIDEO_EXP+archivo)


def Hilos():
	thread1 = Thread(target = ejecutaTiket, args=())
	thread2 = Thread(target = ejecutaVideo, args=())
	try:
		thread1.start()
		thread2.start()
		
	except Exception:
		pass
		
	while(thread1.is_alive):
		kill = 0
	kill = 1

Hilos()
