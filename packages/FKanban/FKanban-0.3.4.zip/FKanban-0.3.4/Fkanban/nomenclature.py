# -*-coding:Latin-1 -*

class nomenclature_link:
	'''Nomenclature link of item
	'''
	def __init__(self, component, qty=1, kanban_use = True):
		''' Initialisation
			- component		: 	(item) component
			- qty			:	qty of component to make the compound item
			- kanban_use	:	True if component is managed by kanban
		'''
		self.component = component
		self.qty = qty
		self.kanban_use = kanban_use
	def __str__(self):
		return "nomenclature_link(%s, %s)"%(self.component, self.qty)
	
	def inventory(self):
		'''Calculate the stock cost in the nomenclature link
		'''
		cost = 0
		if self.kanban_use:
			return self.qty * self.component.cost
		else:
			return 0