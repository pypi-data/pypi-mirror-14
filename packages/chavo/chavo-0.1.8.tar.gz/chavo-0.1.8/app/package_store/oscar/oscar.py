from ..constructor import *
import sys
import tempfile
import fileinput
from components import *
class Oscar:
	def __init__(self, args):
		if len(args) < 1:
			print "You did not provide a package name: \n Oscar's available packages are: \n bootsrap_form ---> \t simple bootstrap form\n materialize_form ---> \t simple materialize form\n materialize_skeleton ---> \t simple materialize skeleton\n portfolio_page ---> \t Portfolio Template Materialize" 
		else: 
			self.c = Construct()
			self.arg = args
			self.check_components()

	def check_components(self):
		print 'its going in here'
		if self.arg[0] == 'bootstrap_form':
			self.f = self.c.create_file()
			self.boot_form()
		elif self.arg[0] == 'materialize_form':
			self.f = self.c.create_file()
			self.mate_form()
		elif self.arg[0] == 'materialize_skeleton':
			self.f = self.c.create_file()			
			self.materialize_skeleton()
		elif self.arg[0] == 'bootstrap_skeleton':
			self.f = self.c.create_file()			
			self.bootstrap_skeleton()
		elif self.arg[0] == 'portfolio_page':
			self.f = self.c.create_file()			
			self.portfolio_page()
		elif self.arg[0] == 'add':
			self.check_add_components()
		else:
			print 'package not found \n'
			print "Oscar's packages: \n Oscar's available packages are: \n bootsrap_form ---> \t simple bootstrap form\n materialize_form ---> \t simple materialize form\n materialize_skeleton ---> \t simple materialize skeleton\n portfolio_page ---> \t Portfolio Template Materialize\n add ---> \t Add html to an existing page" 


	def check_add_components(self):
		# what do I need so that I can make this work from my constructor?
			# the name of the file being edited
			# the class you are using to create the component
		if len(self.arg) < 3:
			print 'Too few arguments you must provide component name and html page you are altering in that order\n'
			print "Components you can add: \n bootsrap_form ---> \t simple bootstrap form\n materialize_form ---> \t simple materialize form\n"
		else: 
			if self.arg[1] == 'materialize_form':
				self.c.add_to_file(self.arg, m_form)
			elif self.arg[1] == 'bootstrap_form':
				self.c.add_to_file(self.arg, b_form)
			elif self.arg[1] == 'boot_box':
				self.c.add_to_file(self.arg, boot_box)
			elif self.arg[1] == 'boot_nav':
				self.c.add_to_file(self.arg, boot_nav, 'nav.css')
			# newFile = tempfile.TemporaryFile()
			# f = open(self.arg[2], 'r+')
			# for lines in f.readlines():
			# 	if '#chavo' in lines:
			# 		tempFile = tempfile.TemporaryFile()
			# 		element = m_form(tempFile, self.arg[2:])
			# 		tempFile.seek(0)
			# 		line = lines.strip('#chavo\n')
			# 		newFile.write(line + "<!-- ######### This is your new component ######### -->\n")
			# 		for newLine in tempFile.readlines():
			# 			newFile.write(line + newLine)
			# 		newFile.write(line + "<!-- ######### This is your new component ######### -->")
			# 		tempFile.close()
			# 	else:
			# 		newFile.write(lines)
			# f.seek(0)
			# newFile.seek(0)
			# f.truncate()
			# for doneLines in newFile.readlines():
			# 	f.write(doneLines)
			# f.close()
			# newFile.close()
	

	def boot_form(self):
		self.c.create_head(self.f, 'bootstrap')
		b_form(self.f, self.arg)
		self.c.create_bottom(self.f, 'bootstrap')

	def mate_form(self):
		self.c.create_head(self.f, 'materialize')
		m_form(self.f, self.arg)
		self.c.create_bottom(self.f, 'materialize')

	def materialize_skeleton(self):
		self.c.create_head(self.f, 'materialize')
		self.c.create_bottom(self.f, 'materialize')

	def bootstrap_skeleton(self):	
		self.c.create_head(self.f, 'materialize')
		self.c.create_bottom(self.f, 'materialize')

	def portfolio_page(self):
		style = "\t<link href='https://fonts.googleapis.com/icon?family=Material+Icons' rel='stylesheet'>\n\t<!-- This is the css overrides for the page, keep it here or extract it to a css page -->\n<style>\n nav ul a,\n nav .brand-logo {\n \tcolor: #444;\n }\n p {\n \tline-height: 2rem;\n }\n .button-collapse {\n \tcolor: #26a69a;\n }\n .parallax-container {\n \tmin-height: 380px;\n \tline-height: 0;\n \theight: auto;\n \tcolor: rgba(255,255,255,.9);\n }\n \t.parallax-container .section {\n \t\twidth: 100%;\n }\n @media only screen and (max-width : 992px) {\n \t.parallax-container .section {\n \t\tposition: absolute;\n \t\ttop: 40%;\n \t}\n \t#index-banner .section {\n \t\ttop: 10%;\n \t}\n }\n @media only screen and (max-width : 600px) {\n \t#index-banner .section {\n \t\ttop: 0;\n \t}\n }\n .icon-block {\n \tpadding: 0 15px;\n }\n .icon-block .material-icons {\n \tfont-size: inherit;\n }\n footer.page-footer {\n \tmargin: 0;\n }\n </style>\n\t<!-- This was the css overrides for the page, keep it here or extract it to a css page -->\n"
		customjs = "<script>\n// This is what sets up the parallax and side NAV extract this code to another page\n (function($){\n \t$(function(){\n \t\t$('.button-collapse').sideNav();\n \t\t$('.parallax').parallax();\n \t});\n })(jQuery);\n // This is what sets up the parallax and side NAV extract this code to another page\n</script>\n"
		self.c.create_head(self.f, 'materialize', style)
		portfolio_materialize(self.f, self.arg)
		self.c.create_bottom(self.f, 'materialize', customjs)


