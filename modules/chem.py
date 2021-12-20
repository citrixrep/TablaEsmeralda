import re
from resources.func.thread import *
from chempy import Substance
from chemformula import ChemFormula
from prettytable import PrettyTable
import json
from chempy.properties.water_density_tanaka_2001 import water_density as rho
from chempy.units import to_unitless, default_units as u

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[1;94m', '\033[1;91m', '\33[1;97m', '\33[1;93m', '\033[1;35m', '\033[1;32m', '\033[0m'
ORANGE  = '\033[1;33m' # orange


Gparam1 = 'false'
Gparam2 = 'en'
Gtemperature_min = '11'
Gtemperature_max = '22'
table_mix = PrettyTable()


class CheckElement():
	def __init__(self):
		with open('resources/data/notes.json') as f:
			self.data = json.load(f)

	def symbol(self,istr):

		try:
			for i in range(0, len(self.data["elements"])):

				numberA = self.data["elements"][i]["symbol"]
				if istr == numberA:
					return self.data["elements"][i]["note"]
		except:
			return ''
		return ''

class PeriodicTable():
	def __init__(self):
		with open('resources/data/periodic_table.json') as f:
			self.data = json.load(f)
			self.CheckElement = CheckElement()

	def atom(self,number):

		for i in range(0, len(self.data["elements"])):

			numberA = self.data["elements"][i]["number"]
			if number == numberA:
				return self.data["elements"][i]

	def symbol(self,symbol):

		for i in range(0, len(self.data["elements"])):

			numberA = self.data["elements"][i]["symbol"]
			if symbol == numberA:
				return self.data["elements"][i]




class TablaEsmeralda():
	def __init__(self):
		self.com = ''

	def composition2(self, element):
		elemento = ChemFormula(element)
		print("\n--- Formula Depictions ---")
		print(f" Formula:       {elemento.formula}")
		print(f" Original:      {elemento}")
		print(f" Charged:       {elemento.charged}")
		print(f" Charge (int):  {elemento.charge}")
		print(f" LaTeX:         {elemento.latex}")
		print(f" HTML:          {elemento.html}")
		print(f" Custom format: {elemento.format_formula('--> ', '', '', '_<', '>', ' <--', '', '', ' * ')}")
		print(f" Sum formula:   {elemento.sum_formula}")
		print(f" Hill formula:  {elemento.hill_formula}")


	def composition(self, element):
		elemento = ChemFormula(element)
		ret = ''

		data = {}
		data['element'] = []
		

		for stringElementSymbol, floatElementFraction in elemento.mass_fraction.items():
			#print(f"   {stringElementSymbol:<2}: {floatElementFraction * 100:>5.2f} %")
			#retp = f'"{stringElementSymbol}":"{floatElementFraction * 100:.2f} %",'
			data['element'].append({'name': stringElementSymbol, 'perc': f'{floatElementFraction * 100:.2f} %'})
			#ret = ret + retp
		#ret = '{'+ret+'}'
		#ret = ret.replace('",}', '"}')
		#ret = json.dump(ret)
		#print(ret["H"])
		return data['element']
	def composition_e(self, element):
		elemento = ChemFormula(element)
		ret = []

		for stringElementSymbol, floatElementFraction in elemento.mass_fraction.items():
			#print(f"   {stringElementSymbol:<2}: {floatElementFraction * 100:>5.2f} %")
			#ret = ret + stringElementSymbol
			ret.append(stringElementSymbol)
		return ret
	def compose(self, element1, element2):
			return ChemFormula(f"{element1}.{element2}").sum_formula

	def radioactive(self, element):
			out = ChemFormula(element)
			return out.radioactive



TE = TablaEsmeralda()
PT = PeriodicTable()

def printg(str1):

	return GREEN+str(str1)+END

def printb(str1):

	return BLUE+str(str1)+END

def printbol(bol):
	if bol:
		return RED+ str(bol)+END
	return GREEN+str(bol)+END

def printy(str1):

	return YELLOW+str(str1)+END

def printy2(str1, str2):
	print(BLUE, str(str1), END, YELLOW, str(str2), END)

def coreOptions():
	options = [
	["asas", "Translation Lang  In", "en"],
	["langout", "Translation Lang  Out", "es"],
	["tempmin", "Temperature (ex: 20)", "20"],
	["tempmax", "Temperature (ex: 40)", "40"]
	]
	return options

## Extend command usage instructions 
def ExtendCommands():
	commands = [
	["formula","Parsing formulae"],
	["mix","mix H2 O"],
	["calentar","calentar H2O"],
	["numberatomic","Ex (numberatomic 8)"],
	["test","test"]]
	return commands


def setOptions(moduleOptions):
	global Gparam1, Gtemperature_min, Gtemperature_max
	Gparam1 = moduleOptions[0][2]
	Gparam2 = moduleOptions[1][2]
	Gtemperature_min = moduleOptions[2][2]
	Gtemperature_max = moduleOptions[3][2]
	#ptrans = moduleOptions[3][2]
	#tracert = moduleOptions[4][2]

def calentar(args):
	global Gtemperature_min, Gtemperature_max
	#print (type(Gtemperature))
	#Gtemperature = 15, 25, 35, 40
	#print (type(Gtemperature))
	water = Substance.from_formula(str(args[0]))
	for T_C in range(int(Gtemperature_min), int(Gtemperature_max)+ 1):
		concentration_H2O = rho(T=(273.15 + T_C)*u.kelvin, units=u)/water.molar_mass(units=u)
		o_el = '%.2f M (at %d °C)' % (to_unitless(concentration_H2O, u.molar), T_C)
		#o_in = 
		#print('[H2O] = %.2f M (at %d °C)' % (to_unitless(concentration_H2O, u.molar), T_C))
		printy2(f'[{str(args[0])}]', o_el)


def element(args):
	retinfo = PT.atom(int(args[0]))
	table_tmp = PrettyTable()
	table_tmp.field_names = [printb("Name"), printb("Symbol"), printb("Category"), printb("Phase"), printb("Atomic_mass")]
	table_tmp.add_row([printy(retinfo["name"]), printy(retinfo["symbol"]), printy(retinfo["category"]), printy(retinfo["phase"]), printy(retinfo["atomic_mass"])])
	print(table_tmp)


def numberatomic(args):
	retinfo = PT.atom(int(args[0]))
	table_tmp = PrettyTable()
	table_tmp.field_names = [printb("Name"), printb("Symbol"), printb("Category"), printb("Phase"), printb("Atomic_mass")]
	table_tmp.add_row([printy(retinfo["name"]), printy(retinfo["symbol"]), printy(retinfo["category"]), printy(retinfo["phase"]), printy(retinfo["atomic_mass"])])
	print(table_tmp)

	#print(retinfo["name"])

def formula(args):
	#print(args)
	table_formula = PrettyTable()
	table_formula_e = PrettyTable()
	formula = args[0]
	ferricyanide = Substance.from_formula(formula) # Fe(CN)6-3

	table_formula.field_names = [printb("Unicode"), printb("Formula"), printb("Latex"), printb("Mass")]
	table_formula_e.field_names = [printb("Name"), printb("Symbol"), printb("Percentaje"), printb("Category"), printb("Phase"), printb("Atomic_mass"), printb("Notes")]

#retnote = pt.CheckElement.symbol('He')
#print(retnote["note"])
	tecf = TE.composition(formula)
	for comp in tecf:
		retinfo = PT.symbol(comp["name"])
		retnote = PT.CheckElement.symbol(comp["name"])
		table_formula_e.add_row([printy(retinfo["name"]), printy(retinfo["symbol"]), printy(comp["perc"]), printy(retinfo["category"]), printy(retinfo["phase"]), printy(retinfo["atomic_mass"]), printy(str(retnote))])

	table_formula.add_row([printy(ferricyanide.unicode_name),printy(ferricyanide.unicode_name), printy(ferricyanide.latex_name + ", " + ferricyanide.html_name), printbol('%.3f' % ferricyanide.mass)])
	print(table_formula)
	print(printg(table_formula_e.get_string(title="Composition Elements")))


def mix(args):
	table_mix.field_names = [printb("Element 1"), printb("Element 2"), printb("Result"), printb("Radioactive")]

	out = TE.compose(args[0], args[1])
	table_mix.add_row([printy(args[0]), printy(args[1]), printy(out), printbol(TE.radioactive(out))])
	#print(out)
	#TE.composition2(out)
	#TE.composition(out)

	#print(table_mix)
	print(printg(table_mix.get_string(title="Mix Elements")))
	formula([str(out)])
