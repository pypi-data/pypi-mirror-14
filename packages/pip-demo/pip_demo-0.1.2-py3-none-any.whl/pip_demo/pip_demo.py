__version__ = "0.1.2"
from shutil import copyfile
import sys
class awesome_module:
	def __init__(self):
		if len(sys.argv) > 1:
			# If the user types in --create
			if sys.argv[1] == '--create':
				print("Hello, let's begin!")
				copyfile('pip_demo/mysqlconnection.py', 'mysqlconnection.py')
		else:
			f = open('README.rst', 'r')
			print('\n' + f.read())
			f.close()       