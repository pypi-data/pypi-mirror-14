# -*-coding:Latin-1 -*


from kloop import *
from item import *
from kanban import *
from place import *
from operation import *
from workshop import *
from nomenclature import *
#from ui_Fkanban import *

import time
import logging

class Fkanban():
	''' A Kanban environment
	'''
	name = "Fkanban"
	def __init__(self, workshops = [], loops = [], speed = 1):
		''' Initialisation
			- workshops		:	list of workshop
			- loops			:	list of loop
		'''
		self.workshops = workshops #inutil!!!
		self.loops = loops
		for loop in self.loops:
			loop.fkanban = self
			for ope in loop.item.operations:
				ope.fkanban = self
		for kb in self.kanbans:
			kb.fkanban = self
		
		self.time = 0
		self.speed = speed #speed in hour per seconde or per manual click
		self.automatic_time = False
		self.actions = [self.run_kanbans, self.run_loops, self.chg_time]
		self.next_action = self.run_kanbans
		self.time_stock = []
		
	@property
	def kanbans(self):
		''' Return the list of all kangans
		'''
		kbs = []
		for loop in self.loops:
			kbs+=loop.kanbans
		return kbs
	
	def run_kanbans(self):
		'''Update kanbans (producing)
		'''
		logging.debug("Update kanbans...")
		nb_actions = 0
		for kb in self.kanbans:
			nb_actions += kb.push()
		logging.debug("%s actions done"%(nb_actions))
		return nb_actions
	
	def run_loops(self):
		'''Update loops
		'''
		logging.debug("Update loops...")
		nb_actions = 0
		for loop in self.loops:
			logging.debug("Check loop %s"%(loop))
			nb_actions += loop.produce_if_needed()
		logging.debug("%s actions done"%(nb_actions))
		return nb_actions
	
	def chg_time(self):
		stock = self.inventory()
		self.bt_stat_stock['text']="Stk:%i€"%(stock)
		self.time_stock.append((self.time, stock))
		self.time +=1
		logging.debug("time change. It is %s"%(self.time))
		return False
		
	def run_actions(self):
		''' run one action
		'''
		if self.next_action()==0:
			self.next_action=self.next_next_action()
			
	def auto_run(self):
		''' on button run pushed
		'''
		if not self.automatic_time:
			self.automatic_time = True
			while self.automatic_time:
				self.run_actions()
				self.ui_update_kanbans()
				self.update()
				time.sleep(1./self.speed/2)
		else:
			self.automatic_time = False
	
	def next_next_action(self):
		''' return the next next_action
		'''
		return self.actions[(self.actions.index(self.next_action)+1)%len(self.actions)]
		
	def first_match_loop(self, item, shop= None):
		''' Return the first loop with item
		'''
		i = 0
		while i<len(self.loops):
			if isinstance(self.loops[i],fab_kloop):
				#if self.loops[i].customer_shop==shop:
				if self.loops[i].item == item:
					return self.loops[i]
			i+=1
			
	def inventory(self):
		'''Calculate the stock cost in the loops
		'''
		cost = 0
		for loop in self.loops:
			cost += loop.inventory()
		return cost
	
	def stat(self):
		''' Return the statistics informations
		'''
		stats = []
		for stat in self.time_stock:
			stats.append("time = %s : stock = %s"%stat)
		return stats