import fechaUTC as tiempo

PATH_EXTRAER_ULTIMO_FOLIO="/home/pi/Documents/eum/app/expedidora/archivos_config/UltimoFolio.txt"
PATH_BITACORA_FOLIOS="/home/pi/Documents/EUM_EXPE/Tickets/foliosBitacoras.txt"

def saberFolio():
	archi = open(PATH_EXTRAER_ULTIMO_FOLIO,"r")
	linea = archi.readline()
	archi.close()
	return str(int(linea)+1)
	pass

def escribirArchivoFolios(idB):
	escribeArch = open(PATH_EXTRAER_ULTIMO_FOLIO,"w")
	escribeArch.write(str(idB)+"\n")
	escribeArch.close()
	pass
