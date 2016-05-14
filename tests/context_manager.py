import sys
from StringIO import StringIO
from contextlib import contextmanager

@contextmanager
def capture(command, *args, **kwargs):
	"""
	Invokes a function given as parameter and captures output of stdout

	Keyword arguments:
	command -- the name of function to be called
	*args -- optional, holds parameters to be passed to command
	**kwargs -- optional, holds a second parameter for command
	"""
	out, sys.stdout = sys.stdout, StringIO()
	command(*args, **kwargs)
	sys.stdout.seek(0)
	yield sys.stdout.read()
	sys.stdout = out