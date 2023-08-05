# -*-coding:Latin-1 -*

from operation import *
from ui_object import *
from place import *
from kanban import *
import logging
import random

class kloop(object):
	''' Kanban loop or customer consumption
	'''
	def __init__(self, fkanban = None, name = "unnamed", item = None):
		''' Initialisation
			- fkanban	:	parent environment (Fkanban object)
			- name		:	name of the loop
			- item		:	produced item
		'''
		self.fkanban = fkanban
		self.name = name
		self.item = item
		self.time_stock_in = [(0,0)]
		logging.debug('Creation of : %s'%(self))
		
	def __str__(self):
		return "kloop(%s)"%(self.name)
	
	def stat(self):
		''' Return the statistics informations
		'''
		stats = []
		for stat in self.time_stock_in:
			stats.append("time = %s : production = %s"%stat)
		return stats
	
class fab_kloop(kloop, ui_fab_kloop):
	''' A Kanban loop for fabrication
	'''
	def __init__(self, fkanban = None, name = "unnamed", item = None, \
				batch = 1, customer_shop = None, kanbans_nb = 0, kanbans_qty = 1, red_zone=1, \
				):
		''' Initialisation
			- fkanban	:	parent environment (Fkanban object)
			- name		:	name of the loop
			- item		:	produced item
			- batch			:	batch qty of kanbans
			- customer_shop	:	output shop
			- kanbans		:	list of kanbans (facultatif)
			- kanbans_nb	:	if kanbans=[] number of kanbans
			- kanbans_qty	:	if kanbans=[] qty per kanbans
			- red_zone		:	qty of kanban in red zone (produce when nb_kanban_not_empty < red_zone)
		'''
		kloop.__init__(self, fkanban, name, item)
		self.batch = batch
		self.customer_shop = customer_shop
		self.kanbans = []
		ui_fab_kloop.__init__(self)
		for k in range(0,kanbans_nb):
			self.kanbans.append(kanban(item, kanbans_qty, self))
		self.red_zone = red_zone
	
	def produce_if_needed(self):
		'''Check if produce is need et make actions
			return the number of actions done
		'''
		logging.debug("test production %s : nb_vide=%s , nb_entame=%s/ red_zone = %s"%(self, self.nb_kanban(kanban.empty), self.nb_kanban(kanban.half_full), self.red_zone))
		if (self.nb_kanban() - self.nb_kanban(kanban.empty)-self.nb_kanban(kanban.half_full))<=self.red_zone:
			logging.info("%s : need production"%(self))
			assert len(self.item.operations)>0, "Error %s has no operation!"%(self)
			if self.item.operations[0]._consume(self.batch, False):
				self.produce()
		return 0
	
	def produce(self):
		'''Produce the item
		'''
		qty = self.batch
		i_kb = 0
		while qty >0 and i_kb < len(self.kanbans):
			kb = self.kanbans[i_kb]
			if kb.status == kanban.empty:
				qty -= kb.qty
				kb.produce()
			i_kb+=1
		if qty>0:
			logging.warning("Not enougth kanbans in %s to produce the batch. Produce only %s vs %s"%(self, self.batch-qty, self.batch))
			
	
	def last_operation(self):
		''' return the last operation of the loop (ie the output one)
		'''
		return self.item.last_operation()
	
	@property
	def workshop(self):
		''' Return the last operation workshop
		'''
		return self.last_operation().workshop
	
	def stock(self):
		'''return the stock of item (**OBSOLETE???*)
			(qty, nb_kanban)
		'''
		qty = 0
		nb = 0
		for kb in self.kanbans:
			if kb.status==kanban.full:
				nb+=1
				qty+=kb.qty
		return (qty, nb)
		
	def nb_kanban(self, status = None):
		'''Return the number of kanbans in the loop with status (None: all)
		'''
		nb = 0
		for kb in self.kanbans:
			if (status == None) or (kb.status == status):
				nb+=1
		return nb
		
	def kanbans_if(self, status=None):
		''' Return the liste of kanbans witch status is status
		'''
		if status == None:
			return self.kanbans
		kanbans = []
		for k in self.kanbans:
			if k.status == status:
				kanbans.append(k)
		return kanbans
	
	def kb_finish(self, kb):
		'''Add statistique when a kanban is produced
		'''
		logging.debug("########")
		if self.time_stock_in[-1][0] == self.fkanban.time:
			self.time_stock_in[-1] = (self.fkanban.time, self.time_stock_in[-1][1]+kb.qty)
		else:
			self.time_stock_in.append((self.fkanban.time, kb.qty))
	
	def inventory(self):
		'''Calculate the stock cost in the loop
		'''
		cost = 0
		for kb in self.kanbans:
			cost += kb.inventory()
		return cost
					
		
class customer_kloop(kloop, ui_customer_kloop):
	''' a loop for simulate the customer consumption
	'''
	def __init__(self,  fkanban = None, name = "unnamed", item = None, workshop = None, period = 1, qty = 1, period_alea_rate = 1., qty_alea_range = 0, manual = False):
		'''Initialisation
			- fkanban	:	parent environment (Fkanban object)
			- name				:	name of the loop
			- item				:	produced item
			- shop				:	shop where item is consumed
			- period			:	number of hour between two consumption
			- qty				:	qty of each consumption
			- period_alea_rate	:	1. = every period, the qty is consumed
									0.5 = 50% chance, qty is consumed
									0. = never consumption
			- qty_alea_rate		:	qty consumed = qty + random.randint(-qty_alea_range,qty_alea_range)
			- manual			:	
		'''
		kloop.__init__(self, fkanban, name, item)
		self.workshop = workshop
		self.period = period
		self.qty = qty
		self.period_alea_rate = period_alea_rate
		self.qty_alea_range = qty_alea_range
		self.last_output = 0
		self.manual = manual
	
	@property
	def kanbans(self):
		return []
	
	def produce_if_needed(self):
		'''Check if produce is need et make actions
			return the number of actions done
		'''
		if self.last_output < self.fkanban.time:
			if self.last_output + self.period <= self.fkanban.time:
				if random.random()< self.period_alea_rate:
					qty = self.qty + random.randint(-self.qty_alea_range, self.qty_alea_range)
					if self.consume(qty):
						#self.last_output +=self.period
						self.last_output = self.fkanban.time
						logging.info("%s => consomption %s of %s ."%(self, self.item, qty))
						return 1
		return 0
	
	def consume(self, qty):
		''' Consume the nomenclature of the item if possible
			return True is producing is possible, else return False
		'''
		logging.debug("Try to produce %s %s. Consume the nomenclature..."%(qty, self.item))
		possible = True
		for ope in self.item.operations:
			possible = possible and ope._consume(qty, False)
		if possible:
			for ope in self.item.operations:
				ope._consume(qty)
				ope.ui_add_text("%s at t=%s"%(qty, self.fkanban.time))
			return True
		else:
			logging.warning("Produce of %s fail."%(self.item))
			return False
			
	def inventory(self):
		'''Calculate the stock cost in the loop
		'''
		return 0
		
	def nb_kanban(self, status = None):
		return 0