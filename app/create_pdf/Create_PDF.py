from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4,landscape
import matplotlib.pyplot as pyplot
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
import matplotlib.pyplot as plt
import os

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
		rowstep = self._fontsize*1.15
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

	#Метод отвечает за сохранение нарисованного pdf
	def save_file(self, filename = 'simple_pdf'):
		self._filename = filename+'.pdf'
		self.showPage()
		self.save()

    #Масштабирование svg картинки
	# def scale(self,drawing, scaling_factor):
	# 	scaling_x = scaling_factor
	# 	scaling_y = scaling_factor
		
	# 	drawing.width = drawing.width * scaling_x
	# 	drawing.height = drawing.height * scaling_y
	# 	drawing.scale(scaling_x, scaling_y)
	# 	return drawing
	#Добавление готовой svg картинки, созданной методом plot_graf_in_svg в pdf

	def add_svg_image(self,image_path,canvas_name,scaling_factor):
		my_canvas = canvas_name
		drawing = svg2rlg(image_path)
		# scaled_drawing = self.scale(drawing, scaling_factor)
		f=renderPDF.draw(drawing, my_canvas, 60*mm, 30*mm)
		return f


	def add_simple_image(self, image_path,canvas_name):
		canvas_name.drawImage(image_path, 700, 10, width=120,height=100)
	#Общий метод для отрисовки тадлиц, картинок из графиков.
	def common(self,canvas_name):
		self.draw_title(startX=10*mm, startY=30*mm, row=1, column=1, width = 230*mm,rowstep = 40)
		self.draw_title(startX=10*mm, startY=10*mm, row=1, column=1, width = 90*mm,rowstep = 30)
		self.draw_title(startX=125*mm, startY=10*mm, row=1, column=1, width = 115*mm,rowstep = 30)
		self.draw_table(startX=10*mm, startY=60*mm, row=13, column=2, width = 60*mm)
		self.draw_table(startX=10*mm, startY=120*mm, row=10, column=2, width = 60*mm)
		self.draw_table(startX=10*mm, startY=170*mm, row=5, column=2, width = 60*mm)
		dirname=os.path.dirname(__file__)
		main_dir=os.path.join(dirname, 'PDF_and_svg')
		image_dir=os.path.join(main_dir, 'ISS.png')
		self.add_simple_image(image_dir,canvas_name)
		self.add_svg_image('АЧХ.svg',canvas_name, scaling_factor=1.1)

#Метод превращает входные данные в картинку svg для дальнейшего добавления в pdf
def plot_graf_in_svg(x_name, y_name,data,measure_type):
	x=[]
	y=[]
	for i in data:
		x.append(i['x'])
		y.append(i['y'])
	plt.plot(x, y)
	plt.title('{}'.format(measure_type))
	plt.grid(True)
	plt.xlabel(x_name, fontsize=12)
	plt.ylabel(y_name, fontsize=12)
	dirname=os.path.dirname(__file__)
	main_dir=os.path.join(dirname, 'create_pdf')
	pdfs_save_dir=os.path.join(main_dir, 'PDF_and_svg')
	plt.savefig(fname='{}'.format(measure_type +'.svg'), format='svg')
	# plt.show()


if __name__ == '__main__':
	d=cr_PDF()

	d.common()
	d.save_file()


	# def add_svg_to_pdf(self,image_path, output_path):
	#         drawing = svg2rlg(image_path)
	#         renderPDF.drawToFile(drawing, output_path)

	# d.add_svg_to_pdf('afc.svg', 'svg_in_pdf.pdf')