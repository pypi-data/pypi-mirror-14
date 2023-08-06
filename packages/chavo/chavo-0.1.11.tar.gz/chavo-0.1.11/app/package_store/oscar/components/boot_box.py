import os
class boot_box:
	def __init__(self, f, arg):
		self.file = f
		if len(arg) > 1:
			self.inputs = arg[1:]
		self.set_values()
		self.create_box()

	def set_values(self):
		self.title = raw_input("Box Header?  ")

	def create_box(self):
		newFile = open(os.path.dirname(__file__) + '/html_box/box.html', 'r+').read().format(header=self.title)
		for x in newFile:
			self.file.write(x)
