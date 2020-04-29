from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import tkinter as tk
from tkinter import filedialog
import webbrowser
import codecs
from parsing_parameters import pars_params

path = ""
tekst = ""
pages = []
num_of_tc = 0
info = [] #type, year, name, start, end
vec_parsiran = 0
pdf_or_text = 0

def parsiraj():
	# Open a PDF file.
	fp = open(path, 'rb')

	# Create a PDF parser object associated with the file object.
	parser = PDFParser(fp)

	# Create a PDF document object that stores the document structure.
	# Password for initialization as 2nd parameter
	document = PDFDocument(parser) 

	# Check if the document allows text extraction. If not, abort.
	if not document.is_extractable:
	    raise PDFTextExtractionNotAllowed

	# Create a PDF resource manager object that stores shared resources.
	rsrcmgr = PDFResourceManager()

	# Create a PDF device object.
	device = PDFDevice(rsrcmgr)

	# BEGIN LAYOUT ANALYSIS
	# Set parameters for analysis.
	laparams = LAParams()

	# Create a PDF page aggregator object.
	device = PDFPageAggregator(rsrcmgr, laparams=laparams)

	# Create a PDF interpreter object.
	interpreter = PDFPageInterpreter(rsrcmgr, device)

	global tekst
	tekst = ""
	def parse_obj(lt_objs):
		# loop over the object list
			for obj in lt_objs:
			# if it's a textbox, print text and location
				if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
				#print(obj.get_text())
					global tekst
					tekst += obj.get_text()
				# if it's a container, recurse
				elif isinstance(obj, pdfminer.layout.LTFigure):
					parse_obj(obj._objs)

	# loop over all pages in the document
	for page in PDFPage.create_pages(document):
		# read the page into a layout object
		tekst = ""
		interpreter.process_page(page)
		layout = device.get_result()

		# extract text from this object
		parse_obj(layout._objs)
		pages.append(tekst)

def get_path():
	root = tk.Tk()
	root.withdraw()
	path = filedialog.askopenfilename()
	fp = open("path.txt", "w")
	fp.write(path)

def load_pdf():
	global path
	fp = open("path.txt", "r")
	path = fp.readline()

def load_text():
	global path
	fp = open("path.txt", "r")
	path = fp.readline()

def get_pdf():
	# print("Otvori novi PDF? [y/n]")
	# ans = input()
	# if (ans[0] == 'y'):
	get_path()
	load_pdf()

def get_info():
	type = input("HONI ili Infokup? [h/i]\n");
	info.append(type)

	year = int(input("Koja godina? [Ako je HONI i npr. sezona 2019/2020 stavi \"2020\"]\n"))
	info.append(year)

	task_name = input("Ime zadatka? [Onako kako je napisano npr. \"MANIPULATOR\" i \"Skandi\"]\n");
	info.append(task_name)

	global pdf_or_text
	if pdf_or_text == 0:
		l, r = input("Od koje do koje stranice? [npr. \"6 9\" i \"1 1\"]\n").split()
		l = int(l) - 1
		r = int(r)
		info.append(l)
		info.append(r)
	else:
		info.append(0)
		info.append(1)

	# global num_of_tc
	# num_of_tc = int(input("Koliko test podataka unutar teksta zadatka?\n"))

def not_empty(line):
	for x in line:
		if (x != ' '):
			return 1
	return 0

def get_text():
	inp = input("Parsiranje iz .pdf ili .txt filea? [p/t]\n")
	global pdf_or_text
	if (inp[0] == 'p'):
		pdf_or_text = 0
		get_pdf()
		parsiraj()
	else:
		pdf_or_text = 1
		get_path()
		load_text()
		fp = codecs.open(path, "rb", "utf-8")
		tekst = fp.read()
		print(tekst)
		pages.append(tekst)

def solve():
	global pdf_or_text
	l = info[-2]
	r = info[-1]
	if info[0] == 'h': #ako su honi zadaci
		if (info[1] == 2020): # 2020 godina
			#uzimanje teksta
			fp = codecs.open("parsed.txt", "w", "utf-8")
			text = ""
			for i in range(l, r):
				if pdf_or_text == 0:
					rev = pages[i][::-1]
					lenght = len(pages[i])
					page = ""

					first = 0
					cnt = 0
					while (cnt < 4):
						if (pages[i][first] == '\n'):
							cnt += 1
						first += 1

					for j in range(lenght - 2, 0, -1):
						if (pages[i][j] == '\n'):
							page = pages[i][first:j]
							break
				else:
					page = pages[i]

				text += page + '\n'

			sol = text.split('\n')
			sol = sol[1:]

			#parametri
			parsed = []
			izlaz = 0
			ulaz = 0

			headings = pars_params["honi"][2020]["headings"].keys()
			io = pars_params["honi"][2020]["io"].keys()

			#dodatno namjestanje
			sol2 = []
			for line in sol:
				if (not_empty(line) == 0):
					continue
				if (line.startswith("Pojašnjenje")):
					prva_dt = 0
					for i in range(0, 1000):
						if (line[i] == ':'):
							prva_dt = i
							break
					sol2.append(line[:prva_dt + 1])
					sol2.append(line[prva_dt + 2:])
				else:
					sol2.append(line)
			sol = sol2

			#pretvaranje parsiranih linija u markdown type
			for line in sol: 
				done = 0
				for el in headings:
					if (line.startswith(el)):
						if (el == "Pojašnjenje " and (izlaz | ulaz) == 1):
							parsed.append("```")
						parsed.append(pars_params["honi"][2020]["headings"][el] + line)
						done = 1

				for el in io:
					if (line.startswith(el)):
						if (ulaz or izlaz):
							parsed.append("```")
						parsed.append(pars_params["honi"][2020]["io"][el] + line)
						parsed.append("```")
						done = 1
						if (el == "ulaz"):
							ulaz = 1
						if (el == "izlaz"):
							izlaz += 1
						parsed.append
				if done == 0:
					parsed.append(line)

			sol = "\n".join(parsed)
			fp.write(sol)

		else: #sve ostale, mogu samo s tekstom
			#uzimanje teksta
			fp = codecs.open("parsed.txt", "w", "utf-8")
			text = ""

			for i in range(l, r):
				if pdf_or_text == 0:
					print("Nemoguce parsirati pdf iz ove godine!")
					return
					rev = pages[i][::-1]
					lenght = len(pages[i])
					page = ""

					first = 0
					cnt = 0
					while (cnt < 4):
						if (pages[i][first] == '\n'):
							cnt += 1
						first += 1

					for j in range(lenght - 2, 0, -1):
						if (pages[i][j] == '\n'):
							page = pages[i][first:j]
							break
				else:
					page = pages[i]

				# for j in range(lenght - 2, 0, -1):
				# 	if (pages[i][j] == '\n'):
				# 		page = pages[i][first:j]
				# 		break
				#print(pages[i])
				#print(pages[i])
				text += page + '\n'

			sol = text.split('\n')

			#parametri
			parsed = []
			izlaz = 0
			ulaz = 0

			headings = pars_params["honi"][2019]["headings"].keys()
			io = pars_params["honi"][2019]["io"].keys()

			#dodatno namjestanje
			sol2 = []
			for line in sol:
				if (not_empty(line) == 0):
					continue
				if (line.startswith("PRIMJERI TEST PODATAKA")):
					continue
				if (line.startswith("Pojašnjenje ")):
					prva_dt = 0
					for i in range(0, 1000):
						if (line[i] == ':'):
							prva_dt = i
							break
					sol2.append(line[:prva_dt + 1])
					sol2.append(line[prva_dt + 2:])
				else:
					sol2.append(line)
			sol = sol2

			prvi = 0
			#pretvaranje parsiranih linija u markdown type
			for line in sol: 
				done = 0
				for el in headings:
					if (line.startswith(el)):
						if (el == "Pojašnjenje " and (ulaz + izlaz) != 0):
							parsed.append("```")
							ulaz = 0
							izlaz = 0
						if (el == "Pojašnjenje "):
							parsed.append(pars_params["honi"][2019]["headings"][el] + line)
						else:
							parsed.append(pars_params["honi"][2019]["headings"][el])
						done = 1

				for el in io:
					if (line.startswith(el)):
						if (ulaz or izlaz):
							parsed.append("```")
						if (prvi == 0):
							prvi = 1
							parsed.append("##Probni primjeri")
						parsed.append(pars_params["honi"][2019]["io"][el] + line)
						parsed.append("```")
						done = 1
						if (el == "ulaz"):
							ulaz = 1
						if (el == "izlaz"):
							izlaz = 1
						parsed.append
				if done == 0:
					parsed.append(line)

			if (izlaz == 1):
				parsed.append("```")
			sol = "\n".join(parsed)
			fp.write(sol)


	#INFOKUP

	else: #infokup4life
		if (info[1] == 2020):
			#uzimanje teksta
			fp = codecs.open("parsed.txt", "w", "utf-8")
			text = ""
			for i in range(l, r):
				if pdf_or_text == 0:
					rev = pages[i][::-1]
					lenght = len(pages[i])
					page = ""

					first = 0
					cnt = 0
					while (cnt < 4):
						if (pages[i][first] == '\n'):
							cnt += 1
						first += 1

					for j in range(lenght - 2, 0, -1):
						if (pages[i][j] == '\n'):
							page = pages[i][first:j]
							break
				else:
					page = pages[i]

			sol = text.split('\n')
			sol = sol[1:]

			#parametri
			parsed = []
			izlaz = 0
			ulaz = 0

			headings = pars_params["infokup"][2020]["headings"].keys()
			io = pars_params["infokup"][2020]["io"].keys()

			#dodatno namjestanje
			sol2 = []
			for line in sol:
				if (not_empty(line) == 0):
					continue
				if (line.startswith("Pojašnjenje")):
					prva_dt = 0
					for i in range(0, 1000):
						if (line[i] == ':'):
							prva_dt = i
							break
					sol2.append(line[:prva_dt + 1])
					sol2.append(line[prva_dt + 2:])
				else:
					sol2.append(line)
			sol = sol2

			#pretvaranje parsiranih linija u markdown type
			for line in sol: 
				done = 0
				for el in headings:
					if (line.startswith(el)):
						if (el == "Pojašnjenje " and izlaz == num_of_tc):
							parsed.append("```")
						parsed.append(pars_params["infokup"][2020]["headings"][el] + line)
						done = 1

				for el in io:
					if (line.startswith(el)):
						if (ulaz or izlaz):
							parsed.append("```")
						parsed.append(pars_params["infokup"][2020]["io"][el] + line)
						parsed.append("```")
						done = 1
						if (el == "ulaz"):
							ulaz = 1
						if (el == "izlaz"):
							izlaz += 1
						parsed.append
				if done == 0:
					parsed.append(line)

			sol = "\n".join(parsed)
			fp.write(sol)

	webbrowser.open("parsed.txt")

def print_all():
	global pages
	for x in pages:
		print(x)

get_text()
get_info() 
solve()


