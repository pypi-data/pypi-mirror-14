import os
class boot_nav:
	def __init__(self, f, arg):
		self.file = f
		if len(arg) > 1:
			self.inputs = arg[1:]
		self.set_values()
		self.create_nav()

	def set_values(self):
		self.brand = raw_input("Brand Name?  ")

	def create_nav(self):
		newFile = open(os.path.dirname(__file__) + '/html_box/nav.html', 'r+').read().format(brandname=self.brand)
		for x in newFile:
			self.file.write(x)

	def create_style(self, css):
		print 'creating style'
		newFile = open(os.path.dirname(__file__) + '/css_box/nav.css', 'r+').read()
		for x in newFile:
			css.write(x)