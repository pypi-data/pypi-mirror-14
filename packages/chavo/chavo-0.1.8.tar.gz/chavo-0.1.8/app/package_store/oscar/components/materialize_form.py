class m_form:
	def __init__(self, f, arg):
		self.file = f
		if len(arg) > 1:
			self.inputs = arg[1:]
		else: 
			self.inputs = False
		self.set_values()
		self.create_form()

	def set_values(self):
		self.action = raw_input("Form action?  ")
		self.button = raw_input("Button value?  ")

	def create_form(self):
		self.create_top()
		if self.inputs:
			for x in self.inputs:
				self.create_field_set(x)
		self.create_bottom()

	def create_label(self, label):
		l = label.replace('_', ' ')
		la = l.title()
		return la

	def create_field_set(self, x):
		if ':' in x:
			arr = x.split(":", 1)
			if len(arr) > 0:
				name = arr[0]
				typeOf = arr[1]
			else:
				name = x
				typeOf = 'text'
		else:
			name = x
			typeOf = 'text'
			print "you didn't specify type of input so we will use text"
		label = self.create_label(name)
		self.file.write("\t\t\t<div class = 'row'>\n")
		self.file.write("\t\t\t\t<div class = 'input-field col s12 l6'>\n")
		if typeOf != 'date':	
			self.file.write("\t\t\t\t\t<label for ='" + name + "'>" + label + "</label>\n")
		self.file.write("\t\t\t\t\t<input id = '" + name + "' name = '" + name + "' type = '" + typeOf + "' class='validate'>\n")
		self.file.write("\t\t\t\t</div>\n")
		self.file.write("\t\t\t</div>\n")

	def create_top(self):
		self.file.write("<div class='col m6'>\n")
		self.file.write("\t<div class = 'row'>\n")
		self.file.write("\t\t<form class = 'col s12' method = 'post' action = '" + self.action + "'>\n")

	def create_bottom(self):
		self.file.write("\t\t\t<div class='divider'></div>\n")
		self.file.write("\t\t\t<div class = 'row'>\n")
		self.file.write("\t\t\t\t<div class = 'col md12'>\n")
		self.file.write("\t\t\t\t\t<p class='right-align'><button class='btn btn-large waves-effect waves-light' type='button' name='action'>" + self.button +"</button></p>\n")
		self.file.write("\t\t\t\t</div>\n")
		self.file.write("\t\t\t</div>\n")
		self.file.write("\t\t</form>\n")
		self.file.write("\t</div>\n")
		self.file.write("</div>\n")

	def getFile(self):
		print 'getting file '
		print self.file.read()
		for x in self.file.readlines():
			print x
		return self.file

