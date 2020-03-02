			USUARIO=''
			global USUARIO
			plaza=''
			localidad=''
			noEquipo=''
			self.bentrar.clicked.connect(self.validaLogin)
			conn = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			cur=conn.cursor()


def validaLogin(self):
			global cur,accesoAcaja,USUARIO,correoUSUARIO
			nom=self.lusu.text()
			rol_us=""
			indice=0
			contr=self.lcont.text()
			cur.execute("SELECT * FROM \"USUARIO\" WHERE usuario=%s and contra=%s order by \"idUsuario\" ASC",(nom,contr))

			print("nom,contr=",nom,contr)
			for reg in cur:
				print(reg[1],reg[2],reg[3],reg[4],reg[5],reg[6])
				rol_us=reg[1]
				indice=1
			if(indice==0):
				self.lerror1.setText("usuario o contraseña incorrectos")
				self.lerror1.setVisible(True)
			else:
				USUARIO=str(reg[0])
				self.cambia(5)






###############################
MODULO HORA Y FECHA
		
		self.bcambiarFecha.clicked.connect(self.cambiaFecha)



def cambiaFecha(self):
		a=self.dtime.dateTime()
		b=self.dtime.textFromDateTime(a)
		print(b,type(b))
		os.system("sudo date -s '"+b+"' ")
###############################


MODULO SUCURSAL


self.bguardar.clicked.connect(self.setConfig)
self.bsalirConfig.clicked.connect(self.salirConf)



def setConfig(self):
		global plaza,localidad,terminalEnt,pol,pol1,pol2,pol3,pol4,pol5,impresora,anchoPapel
		lenn=0
		plaza=str(self.lno.text())
		localidad=str(self.llo.text())
		terminalEnt=str(self.le.text())
		impresora=int(self.cimpresora2.currentIndex())
		anchoPapel=int(self.cpapel2.currentIndex())
		
		pol1=str(self.Lp1.toPlainText())
		pol2=str(self.Lp2.toPlainText())
		pol3=str(self.Lp3.toPlainText())
		pol4=str(self.Lp4.toPlainText())
		pol5=str(self.Lp5.toPlainText())
		pol=pol1+pol2+pol3+pol4+pol5
		
		image = Image.open('/home/pi/Documents/eum/app/expedidora/logo.png')
		draw = ImageDraw.Draw(image)
		font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf', size=16)
 		 
		(x, y) = (0, 40)
		message1 = plaza
		color = 'rgb(0, 0, 0)' # black color		 
		draw.text((x, y), message1, fill=color, font=font)
		(x, y) = (0, 60)
		message2 = localidad
		draw.text((x, y), message2, fill=color, font=font)
		(x, y) = (0, 10)
		message3 = "¡BIENVENIDO!"
		font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf', size=22)
		draw.text((x, y), message3, fill=color, font=font)
		image.save('/home/pi/Documents/eum/app/expedidora/logoPT.png')
		
		
		
		if(impresora==0):
			self.sustituye("/home/pi/.config/lxsession/LXDE-pi/autostart","@usr/bin/python3","@usr/bin/python3 /home/pi/Documents/eum/app/expedidora/firstMMM.py")
			if(anchoPapel==1):
				lista=pol.split("\n")
				pol=""
				for linea in lista:
					lenn += 1
					linea="   "+linea+"\n"
					pol=pol+linea
					print(lenn,linea)
				print("POOOOL",pol)
				
			if(anchoPapel==0):
				lista=pol.split("\n")
				pol=""
				for linea in lista:
					lenn += 1
					linea=""+linea+"\n"
					pol=pol+linea
					print(lenn,linea)
				print("POOOOL",pol)
				
			if(anchoPapel==2):
				lista=pol.split("\n")
				pol=""
				for linea in lista:
					lenn += 1
					linea="              "+linea+"\n"
					print(lenn,linea)
					pol=pol+linea
				print("POOOOL",pol)
		else:
			self.sustituye("/home/pi/.config/lxsession/LXDE-pi/autostart","@usr/bin/python3","@usr/bin/python3 /home/pi/Documents/eum/app/expedidoraEpson/firstMMM.py")
				
					
		print(plaza,localidad)
		dat=plaza+","+localidad+","+str(terminalEnt)+","+str(impresora)+","+str(anchoPapel)
		infile = open("/home/pi/Documents/eum/app/expedidora/datos.txt", 'w')
		c=infile.write(dat)
		
		infile.close()
		infile = open("/home/pi/Documents/eum/app/expedidora/datos/pols.txt", 'w')
		c=infile.write(str(""))
		c=infile.write(str(pol))
		infile.close()
		infile = open("/home/pi/Documents/eum/app/expedidora/datos/pols1.txt", 'w')
		c=infile.write(str(pol1))
		infile.close()
		infile = open("/home/pi/Documents/eum/app/expedidora/datos/pols2.txt", 'w')
		c=infile.write(str(pol2))
		infile.close()
		infile = open("/home/pi/Documents/eum/app/expedidora/datos/pols3.txt", 'w')
		c=infile.write(str(pol3))
		infile.close()
		infile = open("/home/pi/Documents/eum/app/expedidora/datos/pols4.txt", 'w')
		c=infile.write(str(pol4))
		infile.close()
		infile = open("/home/pi/Documents/eum/app/expedidora/datos/pols5.txt", 'w')
		c=infile.write(str(pol5))
		infile.close()
		
		
		self.datosEstacionamiento()
		self.cambia(1)
		
		
def salirConf(self):
	global panelConf
	panelConf=0
	self.cambia(1)

def panelConfig(self):
		global plaza,localidad,equipo
		infile = open('/home/pi/Documents/eum/app/expedidora/archivos_config','r')
		datos= infile.readline()
		arr=datos.split(',')
		sucursal=arr[0]
		localidad=arr[1]
		equipo=arr[2]

###############################

self.bconfirmarplaza.clicked.connect(self.cambiaNombre)
def cambiaNombre(self):
	global nom,loc,USUARIO
	fecha=hora.mostrarFechayHora()
	outfile = open("/home/pi/Documents/plaza.txt", 'w')
	nn=self.lnom.text()
	ln=self.llol.text()
	outfile.write(str(nn)+","+str(ln))
	outfile.close()

	nocaj=self.lcaj.text()

	outfile = open("/home/pi/Documents/NoCajero.txt", 'w')
	outfile.write(str(nocaj))
	outfile.close()
	host=self.lhost.text()
	ip=self.lip.text()

	self.sustituye("/home/pi/Documents/eum/app/cajeroF/cajero/cliente.py","192.168","	host = '"+host+"'")
	self.sustituye("/etc/dhcpcd.conf","ip_address","static ip_address="+ip+"/24")
	ip=ip.split(".")
	ip=ip[0]+"."+ip[1]+"."+ip[2]+".1"
	self.sustituye("/etc/dhcpcd.conf","routers","static routers="+ip)

	nom=self.lnom.text()
	loc=self.llol.text()
	self.cambia(9)
	consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",6,'"+str(nn)+","+str(ln)+"','"+fecha+"')"
	cur.execute(consu)
	conn.commit()
	
	
	
	
	########
			infile = open("/home/pi/Documents/eum/app/expedidora/archivos_config/datos.txt", 'w')

