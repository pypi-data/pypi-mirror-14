import os
import sys
import shutil
import errno

class main:
	def __init__(self):
		if len(sys.argv) > 1:
			print len(sys.argv)
			print sys.argv
			if str(sys.argv[1]) == "new":
				if len(sys.argv) > 2:
					self.create_pylot(str(sys.argv[2]))
				else: 
					self.create_pylot('pylot')
			else:
				raise ValueError('To create a new pylot project run pylot new project_name')
		
	def ignore_function(self, ignore):
		def _ignore_(path, names):
			ignored_names = []
			if ignore in names:
				ignored_names.append(ignore)
			return set(ignored_names)
		return _ignore_

	def create_pylot(self, dest):
		try:
			current = os.path.dirname(os.path.realpath(__file__))
			src = current + "/Pylot"
			shutil.copytree(src, dest, ignore=self.ignore_function('.git'))
		except OSError as e:
			if e.errno == errno.ENOTDIR:
				shutil.copy(src, dest, ignore=self.ignore_function('.git'))
			else:
				if e is not None:
					print('Directory not copied. Error: %s' % e)
				else:
					print('Directory not copied. Error: %s' % e)


