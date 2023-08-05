from ..constructor import *
import sys
from components import *
class Oscar:
	def __init__(self, args):
		if len(args) < 1:
			print "You did not provide a package name: \n Oscar's available packages are: \n bootsrap_form --- \t simple bootstrap form\n materialize_form --- \t simple materialize form" 
		else: 
			self.c = Construct()
			self.arg = args
			self.check_components()

	def check_components(self):
		self.f = self.c.create_file()
		print self.arg
		if self.arg[0] == 'bootstrap_form':
			self.c.create_head(self.f, 'bootstrap')
			b_form(self.f, self.arg)
			self.c.create_bottom(self.f, 'bootstrap')

