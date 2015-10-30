import glob
import imp

class Conductor:
	def __init__(self):
		# Create dictionaries of supported modules
		# empty until stuff loaded into them
		#stolen from Veil :)
		self.modules = {}
		self.dmodules = {}
		#load up modules on instance
		self.load_modules()

	def load_modules(self):
		#loop and assign key and name
		x = 1
		for name in glob.glob('Modules/*.py'):
			if name.endswith(".py") and ("__init__" not in name):
				loaded_modules = imp.load_source(name.replace("/", ".").rstrip('.py'), name)
				self.modules[name] = loaded_modules
				self.dmodules[x] = loaded_modules
				x += 1
		return self.dmodules
		return self.modules

	def title(self):
	print "\n\
		##############################\n\
		#   Simply Email Reconsance  #\n\
		#        KiLlSwiTch-GUI      #\n\
		##############################\n\
This tools is for simple yet powerful email enumeration\n "

