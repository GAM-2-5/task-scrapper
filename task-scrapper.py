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

path = ""
tekst = ""
pages = []

def parsiraj():
	# Open a PDF file.
	fp = open('C:/Users/Boris/Documents/task-scrapper/kolo6_zadaci.pdf', 'rb')

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
	#print(path)

get_pdf()
parsiraj()
print(pages[1])
