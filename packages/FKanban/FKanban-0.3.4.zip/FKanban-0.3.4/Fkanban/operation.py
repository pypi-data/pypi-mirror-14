# -*-coding:Latin-1 -*

import logging
from operation import *
from ui_object import *
from kanban import *
from item import *
from ui_object import *

class operation(ui_operation):
	''' fabrication operation
	'''
	def __init__(self, workshop , nomenclature = [] , name = "unnamed", qty_per_hour = 999999, setup_time = 0, fkanban = None):
		'''Initialisation
			- workshop		:	workshop 
			- name			:	name of the operation
			- nomenclature	:	list of nomenclature_link
			- qty_per_hour	:	qty of item produced per a day (on one team)
			- setup_time	:	nb of setup hours 
			- fkanban		:	the parent envirronment
		'''
		self.workshop = workshop
		self.name = name
		self.nomenclature = nomenclature
		self.qty_per_hour = qty_per_hour
		self.setup_time = setup_time
		self.fkanban = fkanban
	
	def __str__(self):
		return "Operation(%s)"%(self.name)
	
	def _consume(self, qty, real = True):
		''' check if we have  has enouth stock to produce
			return True is producing is possible, else return False
			if real, do the consumption
		'''
		if real:
			logging.debug("Consumtion of %s %s"%(qty, self))
		else:
			logging.debug("Check possibility of comsumption of %s %s"%(qty, self))
		for link in self.nomenclature:
			logging.debug("nomenclature_link : %s"%(link))
			if link.kanban_use:
				provider_loop = self.fkanban.first_match_loop(link.component, self.workshop)
				if provider_loop:
					logging.debug("Provider loop found : %s"%(provider_loop))
					qty_needed = qty * link.qty
					#List of half-full and full kanbans (sorted)
					kbs = provider_loop.kanbans_if(kanban.half_full) + provider_loop.kanbans_if(kanban.full)
					for kb in kbs:
						if qty_needed>0:
							qty_to_consume_in_kb = min(qty_needed, kb.stock)
							if real:
								kb.consume(qty_to_consume_in_kb)
							qty_needed -= qty_to_consume_in_kb
					if qty_needed>0: #If not enough stock in kanbans
						logging.warning("Not enough stock in %s. %s parts are missing."%(provider_loop, qty_needed))
						logging.warning("Consumption is not possible")
						if not real:
							provider_loop.ui_out_of_stock(True)
							self.ui_out_of_stock(True)
						return False
					else:
						logging.info("Ok. Stock is enough in %s"%(provider_loop))
						if not real:
							provider_loop.ui_out_of_stock(False)
		logging.debug("Consumption is possible")
		if not real:
			self.ui_out_of_stock(False)
		return True
	
	def consume(self, qty):
		''' Consume the nomenclatyure of the item if possible
			return True is producing is possible, else return False
		'''
		logging.debug("Try to produce %s. Consume the nomenclature..."%(self))
		if self._consume(qty, False):
			logging.debug("Consumption is possible.")
			self._consume(qty)
			return True
		else:
			logging.warning("Produce of %s fail."%(self))
			return False
	
	def inventory(self):
		'''Calculate the stock cost in the operation
		'''
		cost = 0
		for link in self.nomenclature:
			cost += link.inventory()
		return cost
		