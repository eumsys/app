#-*- coding:utf-8 -*-
import os
import time
#from PyQt4 import QtCore, QtGui
from misEstilos import *
#Librerias reportlab a usar:
from reportlab.platypus import (BaseDocTemplate, Frame, Paragraph, Image, 
                    NextPageTemplate, PageBreak, PageTemplate)
##comente esta linea de abajo
#from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import A4

#Textos

boletoFecha=("Fecha: "+time.strftime("%d de %B de %Y"))
boletoHoraEntrada=("Hora de entrada: "+time.strftime("%H:%M:%S"))
boletoFolio=("Folio: 0001")
boletoExpedidora=("Expedidora: 3")

miEmpresaLogo=(Image("logoSauz.png", width=50*mm, height=20*mm))
miSucursal=("Plaza Heroes Tecamac")
#miEncabezado=("BIENVENIDO<br/>"+miSucursal)
miEncabezado2=("BIENVENIDO")
miTexto = ("La empresa no se hace responsable por objetos personales, fallas mecánicas y/o eléctricas, siniestros ocasionados por derrumbes, temblores, terremotos o fenómenos naturales, así como robo de accesorios o vandalismo en su vehículo. Por robo total de acuerdo a los térmicos del seguro contratado. Boleto perdido se entregara el vehículo a quien acredite la propiedad. Costo del boleto perdido es de <b> $100.00 </b> Al recibir este boleto acepta las condiciones del seguro contra robo total. PARKING TIP S.A de C.V. RFC. PTI120210571. Escobillera 13 Col. Paseos de Churubusco Iztapalapa CDMX. CP. 09030 Horario de Lunes a Domingo de 7 a 22 hrs.")

#imágenes
miQR=(Image("output.png", width=20*mm, height=20*mm))
miFlecha=(Image("flecha1.png", width=10*mm, height=4*mm))


#NIVEL 1: CREAMOS LOS CANVAS
#===========================   
#Creamos los canvas para el pie de página y encabezado, que serán fijos
def encabezado(canvas,doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, A4[1]-50, "Ejemplo de DocTemplate y PageTemplate")
    canvas.restoreState()
    
def pie(canvas,doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(mm, 0.75 * mm, "Page %d" % doc.page)
    canvas.restoreState()

#NIVEL 2: CREAMOS LOS FLOWABLES
#==============================
#Creamos la hoja de Estilo
estilo=getSampleStyleSheet()

#Iniciamos el platypus story
story=[]

#Añadimos al story los flowables. Hay que tener en cuenta que se inicia
#con el primer pageTemplate "UnaColumna"
#story.append(Paragraph("Esto es el texto del Frame normal del pagetemplate" +\
#                       " de una columna"* 500, estilo['Normal']))

story.append(Paragraph(miEncabezado2,estilo['Heading1']))
story.append(miEmpresaLogo)
story.append(Paragraph(miTexto,estilo['FijoTexto']))
story.append(Paragraph(boletoFolio,estilo['Heading2']))
story.append(Paragraph(boletoFecha,estilo['Heading2']))
story.append(Paragraph(boletoHoraEntrada,estilo['Heading2']))
story.append(Paragraph(boletoExpedidora,estilo['Heading2']))
story.append(miQR)
story.append(miFlecha)
                        
#story.append(NextPageTemplate('DosColumnas'))  # Cambio de PageTemplate
#story.append(PageBreak())  # Inicio en otra hoja
#story.append(Paragraph("Esto es el texto del Frame que pertenece al" +\
#                       " pagetemplate de dos columnas" * 500, estilo['Normal']))
                
#story.append(NextPageTemplate('UnaColumna'))
#story.append(PageBreak())
#story.append(Paragraph("Regresamos al texto del Frame normal del" +\
#                        " pagetemplate de dos columnas"*100, estilo['Normal']))

#NIVEL 3: CREAMOS LOS FRAMES, para luego asignarlos a un pagetemplate.
#===========================
#Frame (x1, y1, ancho, alto, leftPadding=6, bottomPadding=6, rightPadding=6,
# topPadding=6, id=None, showBoundary=0)

#1. Frame que contendrá a toda el contenido de una hoja
frameN = Frame(mm, mm, 220, 315, id='normal')


pagesize = (80*mm,110*mm)		
#c = canvas.Canvas("hello.pdf", pagesize=pagesize)
#2. Frame de columnas
#frame1 = Frame(inch, inch, 220, 697, id='col1')
#frame2 = Frame(inch + 230, inch, 220, 697, id='col2')

#NIVEL 4: CREAMOS LOS PAGETEMPLATE, le asignamos los frames y los canvas
#=================================
#PageTemplate(id=None,frames=[],onPage=_doNothing,onPageEnd=_doNothing)
#PTUnaColumna = PageTemplate(id='UnaColumna', frames=frameN, onPage=pie)
PTUnaColumna = PageTemplate(id='UnaColumna', frames=frameN)
#PTDosColumnas =  PageTemplate(id='DosColumnas', frames=[frame1,frame2],
#                        onPage=encabezado, onPageEnd=pie)

#NIVEL 5: CREAMOS EL DOCTEMPLATE, a partir del BaseDocTemplate
#===============================
doc = BaseDocTemplate('test.pdf', pageTemplates=[PTUnaColumna], 
        pagesize=pagesize)

#Construimos el PDF
doc.build(story)

os.system("test.pdf")
