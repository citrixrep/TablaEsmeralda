import re
from resources.func.thread import *
from chempy import Substance



BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[1;94m', '\033[1;91m', '\33[1;97m', '\33[1;93m', '\033[1;35m', '\033[1;32m', '\033[0m'
ORANGE  = '\033[1;33m' # orange


Gparam1 = 'false'
Gparam2 = 'en'


def coreOptions():
	options = [["langin", "Translation Lang  In", "en"],["langout", "Translation Lang  Out", "es"]]
	return options

## Extend command usage instructions 
def ExtendCommands():
	commands = [["tonum","get number"],["test","test"]]
	return commands


def core(moduleOptions):
	print('Command run disabled on current module')

def setOptions(moduleOptions):
	global Gparam1, Gparam2
	Gparam1 = moduleOptions[0][2]
	Gparam2 = moduleOptions[1][2]
	#threads = moduleOptions[2][2]
	#ptrans = moduleOptions[3][2]
	#tracert = moduleOptions[4][2]


def test(args):

	ferricyanide = Substance.from_formula('Fe(CN)6-3')
	ferricyanide.composition == {0: -3, 26: 1, 6: 6, 7: 6}  # 0 for charge
	print(ferricyanide.unicode_name)
	#Fe(CN)
	print(ferricyanide.latex_name + ", " + ferricyanide.html_name)
	#Fe(CN)_{6}^{3-}, Fe(CN)<sub>6</sub><sup>3-</sup>
	print('%.3f' % ferricyanide.mass)