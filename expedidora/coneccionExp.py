import psycopg2

class Conexion():
	def __init__(self):
		self.con = None
		self.cursor = None
		self.dbname = "eumDataExp"
		self.user = "ardgz"
		self.host = "localhost"
		self.password = "n0m3l0"
		self.port = "5432"
		try:
			self.con = psycopg2.connect("dbname='"+self.dbname+"' user='"+self.user +"' host='"+self.host+"' password='"+self.password+"' port='"+self.port+"'")
			#self.con = psycopg2.connect(dbname='eumDataExp',user='ag')
			print("Conexion Establecida")
		except psycopg2.Error as e:
			print('Error: %s' % e)
			
	def doQuery(self, q):
		try:
			self.cursor = self.con.cursor()
			self.cursor.execute(""+str(q))
			self.con.commit()
			registros= self.cursor.fetchall()
			return registros
			
		except psycopg2.Error as e:
			print('Error: %s' % e)
			return -1;
			
	def execQuery(self, q):
		try:
			self.cursor = self.con.cursor()
			self.cursor.execute(""+str(q))
			self.con.commit()
			return 1
			
		except psycopg2.Error as e:
			print('Error: %s' % e)
			return -1;		
			
	def __del__(self):
		try:
			self.con.close()
			print("Conexion Cerrada")
		except psycopg2.Error as e:
			print('Error: %s' % e)			
		
def main():
	con = Conexion()
	q = "SELECT * FROM boletoexpedidora"
	#e = "INSERT INTO usuario (usr_usuario, usr_passwd_usuario"
	registros = con.doQuery(q)
	
	print(registros[0][2])
	print (registros)
#main()
	
