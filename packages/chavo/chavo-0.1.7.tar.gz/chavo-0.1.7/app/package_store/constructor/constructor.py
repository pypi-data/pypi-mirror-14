import os
import sys
class main:
	def __init__(self):
		self.started = True

	def create_file(self):
		filename = raw_input("Filename? ")
		os.system('touch ' + filename)
		f = open(filename, 'w')
		return f

	def create_head(self, f, front_end=False, custom_style=False):
		f.write("<!DOCTYPE html>\n")
		f.write("<html>\n")
		f.write("<head>\n")
		f.write("\t<meta charset='UTF-8'>\n")
		title = raw_input("Title? ")
		f.write("\t<title>" + title + "</title>\n")
		if front_end:
			if front_end == 'bootstrap':
				self.bootstrap(f)
			elif front_end == 'materialize':
				self.materialize(f)
			else:
				print 'only bootstrap and materialize for now'
		if custom_style:
			f.write(custom_style)
		f.write("</head>\n")
		f.write("<body>\n")

	def create_bottom(self, f, front_end=False, custom_js=False):
		if front_end:
			self.jquery(f)
			if front_end == 'bootstrap':
				self.bootstrapjs(f)
			elif front_end == 'materialize':
				self.materializejs(f)
		if custom_js:
			f.write(custom_js)
		f.write("</body>\n")
		f.write("</html>")

	def bootstrap(self, f):
		f.write("\t<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css' integrity='sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7' crossorigin='anonymous'>\n")
		self.front_end = "bootstrap"

	def materialize(self, f):
		f.write("\t<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.5/css/materialize.css'>\n")
		self.front_end = "materialize"
	
	def foundation(self, f):
		f.write("\t<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/foundation/6.1.1/foundation.css'>\n")
		self.front_end = "foundation"

	def jquery(self, f, front_end=False):
		f.write("\t<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.1/jquery.js'></script>\n")

	def bootstrapjs(self, f):
		f.write("\t<script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js'></script>\n")

	def materializejs(self, f):
		f.write("\t<script src='https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.5/js/materialize.min.js'></script>\n")

	def foundationjs(self, f):
		f.write("\t<script src = 'https://cdnjs.cloudflare.com/ajax/libs/foundation/6.2.0/foundation.min.js'></script>\n")
