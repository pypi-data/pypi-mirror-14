__version__ = "0.1.11"

import sys
import os
from package_store import *

class main:
	def __init__(self):
		if len(sys.argv) > 1:
			self.check_packages()
		else:
			print 'No function called, available packages:\n\toscar'

	def check_packages(self):
		if sys.argv[1] == 'oscar':
			Oscar(sys.argv[2:])