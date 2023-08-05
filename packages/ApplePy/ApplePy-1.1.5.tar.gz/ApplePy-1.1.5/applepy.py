""" This is the "applepy.py" module, and it provides a list of os.system commands shortcude.
	cls= This code was found on the stackoveflow thread below:
	http://stackoverflow.com/questions/517970/how-to-clear-python-interpreter-console """
import os
class Cls(object):
    def __repr__(self):
        os.system('clear')
        return ''
"""" usage: type cls """
cls = Cls()