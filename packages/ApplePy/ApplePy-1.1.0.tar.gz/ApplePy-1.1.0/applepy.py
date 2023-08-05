""" This is the "recipe.py" module, and it provides a list of os.system commands shortcude."""
def clear ():
	""" This function clears the screen """
	import os
	os.system('clear')

def pwd ():
	""" This function displays current working directory """
	import os
	os.getcwd()

def chdir (dir):
	""" This function will change the current directory to the "dir" """
	import os
	os.chdir(dir)
	os.getcwd()
