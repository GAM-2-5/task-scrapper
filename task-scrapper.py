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

path = ""
tekst = ""
pages = []
info = [] #type, year, name, start, end

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


def openPDF():
	root = tk.Tk()
	root.withdraw()
	path = filedialog.askopenfilename()
	fp = open("path.txt", "w")
	fp.write(path)

def load():
	global path
	fp = open("path.txt", "r")
	path = fp.readline()

def get_pdf():
	print("Otvori novi PDF? [y/n]")
	ans = input()
	if (ans[0] == 'y'):
		openPDF()
	load()

def get_info():
	type = input("HONI ili Infokup? [h/i]\n");
	info.append(type)

	year = int(input("Koja godina? [Ako je HONI i npr. sezona 2019/2020 stavi \"2020\"]\n"))
	info.append(year)

	task_name = input("Ime zadatka? [Onako kako je napisano npr. \"MANIPULATOR\" i \"Skandi\"]\n");
	info.append(task_name)

	l, r = input("Od koje do koje stranice? [npr. \"6 9\" i \"1 1\"]\n").split()
	l = int(l) - 1
	r = int(r)
	info.append(l)
	info.append(r)

def solve():
	l = info[-2]
	r = info[-1]
	if info[0] == 'h': #ako su honi zadaci
		if (info[1] == 2020): # 2020 godina
			fp = codecs.open("parsed.txt", "w", "utf-8")
			text = ""
			for i in range(l, r):
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

				text += page + '\n'

			sol = text.split('\n')
			sol = sol[1:]

			parsed = []
			izlaz = 0
			for line in sol: #pretvaranje parsiranih linija u markdown type
				if line.startswith("Ulazni podaci"):
					parsed.append( "##" + line )
				elif line.startswith("Izlazni podaci"):
					parsed.append( "##" + line )
				elif line.startswith("Bodovanje"):
					parsed.append( "##" + line )
				elif line.startswith("ulaz"):
					if (izlaz):
						parsed.append("```")
					parsed.append( "###" + line )
					parsed.append( "```" )
				elif line.startswith("izlaz"):
					parsed.append( "```" )
					parsed.append( "###" + line )
					parsed.append( "```" )
					izlaz = 1
				elif line.startswith("Probni primjeri"):
					parsed.append( "##" + line )
				elif line.startswith("Pojašnjenje "):
					if izlaz:
						parsed.append( "```")
					izlaz = 0
					for j in range(0, len(line)):
						if (line[j] == ':'):
							parsed.append("###" + line[:j + 1])
							parsed.append(line[j + 1:])
							break;
				else:
					parsed.append(line)
			if (izlaz):
				parsed.append("```")

			sol = "\n".join(parsed)
			fp.write(sol)

	else: #infokup4life
		if (info[1] == 2020):
			fp = codecs.open("parsed.txt", "w", "utf-8")
			text = ""
			for i in range(l, r):
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

				text += page + '\n'

			sol = text.split('\n')
			sol = sol[1:]

			parsed = []
			izlaz = 0

			for line in sol: #pretvaranje parsiranih linija u markdown type
				if line.startswith("Ulazni podatci"):
					parsed.append( "##" + line )
				elif line.startswith("Izlazni podatci"):
					parsed.append( "##" + line )
				elif line.startswith("Bodovanje"):
					parsed.append( "##" + line )
				elif line.startswith("ulaz"):
					if (izlaz):
						parsed.append("```")
					parsed.append( "###" + line )
					parsed.append( "```" )
				elif line.startswith("izlaz"):
					parsed.append( "```" )
					parsed.append( "###" + line )
					parsed.append( "```" )
					izlaz = 1
				elif line.startswith("Probni primjeri"):
					parsed.append( "##" + line )
				elif line.startswith("Pojašnjenje "):
					if izlaz:
						parsed.append( "```")
					izlaz = 0
					for j in range(0, len(line)):
						if (line[j] == ':'):
							parsed.append("###" + line[:j + 1])
							parsed.append(line[j + 1:])
							break;
				else:
					parsed.append(line)
			if (izlaz):
				parsed.append("```")

			sol = "\n".join(parsed)
			fp.write(sol)

	webbrowser.open("parsed.txt")


get_pdf()
parsiraj()
get_info() 
solve()