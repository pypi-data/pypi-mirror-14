# -*-coding:Latin-1 -*
from ui_object import *

class item(ui_object):
	""" Product
	"""
	def __init__(self, name, operations = [], cost = None):
		""" Initialisation
			- name
			- operations		:	list of operations
		"""
		self.name = name
		self.operations = operations
		if cost != None:
			self.cost = cost
		else:
			self.cost = self.calculate_cost()
	
	def __str__(self):
		return "item(%s)"%(self.name)
		
	def last_operation(self):
		''' return the last operation of the item (ie the output one)
		'''
		if len(self.operations)>0:
			return self.operations[-1]
		else:
			return None
	
	def calculate_cost(self):
		'''calculate the cost of the item
		'''
		return 1 # TODO
