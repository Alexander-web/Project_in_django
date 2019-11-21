from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4,landscape
import matplotlib
matplotlib.use('Agg')
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
import matplotlib.pyplot as plt
from reportlab.platypus.flowables import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import utils
import svgutils
import os

pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

class cr_PDF(Canvas):
	def __init__(self, filename='canvas.pdf', pagesize=landscape(A4), bottomup=0, 
		pageCompression=None, invariant=None, 
		verbosity=0, encrypt=None, 
		cropMarks=None, pdfVersion=None, 
		enforceColorSpace=None, initialFontName=None, 
		initialFontSize=10, initialLeading=None, 
		cropBox=None, artBox=None, 
		trimBox=None, bleedBox=None):
			super().__init__(filename, pagesize=pagesize, bottomup=bottomup, 
		pageCompression=pageCompression, invariant=invariant, 
		verbosity=verbosity, encrypt=encrypt, 
		cropMarks=cropMarks, pdfVersion=pdfVersion,
		enforceColorSpace=enforceColorSpace, initialFontName=initialFontName, 
		initialFontSize=initialFontSize, initialLeading=initialLeading,
		cropBox=cropBox, artBox=artBox,
		trimBox=trimBox, bleedBox=bleedBox)
	#Метод отвечает за рисование таблиц
	def draw_table(self, row=10, column=2, startX=0, startY=0, width=0):
		startY+=0.5*mm
		rowstep = self._fontsize*2.5
		#Эта часть отвечает за создание горизонтальных линий таблицы
		for i in range(row+1):
			self.line(startX, startY + rowstep * i, startX + width, startY + rowstep * i)
		# Эта часть отвечает за создание вертикальных строк таблицы 
		colstep = width / column
		for i in range(column+1):
			self.line(startX+colstep*i,startY,startX + colstep*i, startY + rowstep * row)
			
	def draw_title(self, row=10, column=2, startX=0, startY=0, width=0,rowstep = 2):
		startY+=0.5*mm
		#Эта часть отвечает за создание горизонтальных линий таблицы
		for i in range(row+1):
			self.line(startX, startY + rowstep * i, startX + width, startY + rowstep * i)

		colstep = width / column
		for i in range(column+1):
			self.line(startX+colstep*i,startY,startX + colstep*i, startY + rowstep * row)

	def draw_string(self,data,label,canvas_name,row=10,startX=10,startY=0,startX1=10):
		startY+=0.5*mm
		rowstep = self._fontsize*2.5
		num=range(row+1)
		for i,j in zip(label, num):
			x=startX
			y=startY + rowstep * j
			canvas_name.drawString(x, y, i)
		for i,j in zip(data, num):
			x=startX1
			y=startY + rowstep * j
			canvas_name.drawString(x, y, str(i))

	def simple_title(self, canvas_name,title,x,y):
		canvas_name.drawString(x, y, str(title))

	#Метод отвечает за сохранение нарисованного pdf
	def save_file(self, filename = 'simple_pdf'):
		self._filename = filename+'.pdf'
		self.showPage()
		self.save()

    #Масштабирование svg картинки
	def scale_svg(self,drawing):
		scaling_x = -0.9
		scaling_y = 0.9

		# drawing.width = drawing.width * scaling_x
		# drawing.height = drawing.height * scaling_y
		drawing.scale(scaling_x, scaling_y)
		return drawing
	#Добавление готовой svg картинки, созданной методом plot_graf_in_svg в pdf

	def add_svg_image(self,image_path,canvas_name):
		my_canvas = canvas_name
		drawing = svg2rlg(image_path)
		scaled_drawing = self.scale_svg(drawing)
		scaled_drawing.rotate(-180)
		f=renderPDF.draw(scaled_drawing, my_canvas, 95*mm, 185*mm)
		return f

	def del_svg(self,path):
		del path

	def add_simple_image(self, image_path,canvas_name):
		canvas_name.drawImage(image_path, 700, 30, width=120,height=100)

	#Общий метод для отрисовки тадлиц, картинок из графиков.
	def common(self,data,label,canvas_name,name,title):
		canvas_name.setFont('Arial', 10)

		dirname=os.path.dirname(__file__)
		main_dir=os.path.join(dirname, 'PDF_and_svg')
		image_dir=os.path.join(main_dir, 'ISS.png')
		
		self.draw_title(startX=10*mm, startY=30*mm, row=1, column=1, width = 230*mm,rowstep = 40)
		self.draw_title(startX=10*mm, startY=10*mm, row=1, column=1, width = 90*mm,rowstep = 30)
		self.draw_title(startX=125*mm, startY=10*mm, row=1, column=1, width = 115*mm,rowstep = 30)

		self.draw_table(startX=10*mm, startY=55*mm, row=10, column=2, width = 80*mm)
		self.draw_table(startX=10*mm, startY=145*mm, row=2, column=2, width = 80*mm)
		self.draw_table(startX=10*mm, startY=170*mm, row=3, column=2, width = 80*mm)
		self.draw_string(data,label,canvas_name,row=len(label),startX=12*mm,startY=60*mm,startX1=65*mm)
		
		canvas_name.setFont('Arial', 16)
		self.simple_title(canvas_name, title['measure_type'], x=170*mm, y=17*mm)
		self.simple_title(canvas_name, title['ssi_name'], x=130*mm, y=17*mm)
		self.simple_title(canvas_name, title['KA'], x=15*mm, y=17*mm)
		self.simple_title(canvas_name, title['ПН'], x=80*mm, y=17*mm)
		canvas_name.setFont('Arial', 10)
		self.simple_title(canvas_name, title['time_label'], x=120*mm, y=200*mm)

		self.add_simple_image(image_dir,canvas_name)
		self.add_svg_image(name+'.svg',canvas_name)
		self.del_svg(name+'.svg')


#Метод превращает входные данные в картинку svg для дальнейшего добавления в pdf
def plot_graf_in_svg(x_name, y_name,data,measure_type):
	x=[]
	y=[]
	for i in data:
		x.append(i['x'])
		y.append(i['y'])
	plt.plot(x, y)
	# plt.title('{}'.format(measure_type))
	plt.grid(True)
	plt.xlabel(x_name, fontsize=12)
	plt.ylabel(y_name, fontsize=12)
	plt.savefig(fname='{}'.format(measure_type +'.svg'), format='svg')
	plt.close()


