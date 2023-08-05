# -*-coding:Latin-1 -*

from ui_object import *
import logging

class kanban(ui_kanban, object):
	""" Kanban object
	"""
	empty = 0
	running = 1
	full = 2
	half_full = 3
	
	def __init__(self, item, qty, loop = None):
		"""Initialisation
			- item					:	the produced product (item object)
			- qty					:	qty of item per kanban
			- loop					:	parent loop
		"""
		self.item = item
		self.qty = qty
		self.loop = loop
		self.running_operation = None
		self.status = kanban.empty
		self._stock = 0
		self.next_time_change = None
		self.fkanban = None
		logging.debug("Creation of : %s"%(self))
		ui_kanban.__init__(self)
		
	@property
	def stock(self):
		return self._stock
	@stock.setter
	def stock(self, stk):
		self._stock = stk
		self.ui_change_label()
	
	
	def __str__(self):
		if self.status == kanban.empty:
			status = "empty"
		elif self.status == kanban.running:
			status = "running(->%s)"%(self.next_time_change)
		elif self.status == kanban.half_full:
			status = "half-full:%s"%(self.stock)
		else:
			status = "full"
		return "kanban(%s, qty:%s, %s)"%(self.item.name, self.qty, status)
	
	@property
	def name(self):
		# TODO améliorer pour UI
		return str(self)
	
	def consume(self, qty = None):
		''' Consume the kanban
			- qty	:	qty to consume
		'''
		assert self.status >= kanban.full, "Can't consume empty or running kanban! %s"%(self)
		if qty != None:
			assert self.stock >= qty, "Can't consume %s in %s : stock not enough."%(qty, self)
			self.stock -= qty
		else:
			self.stock = 0
		if self.stock == 0:
			self.status = kanban.empty
			logging.info("%s is entirely consumed!"%(self))
		else:
			self.status = kanban.half_full
			logging.info("%s is partially consumed!"%(self))
		self.ui_update()
		
	def produce(self):
		'''Start production of the kanban
		'''
		first_ope = self.item.operations[0]
		first_ope.consume(self.qty)
		self.status = kanban.running
		self.running_operation = 0
		self.next_time_change = self.fkanban.time + \
								first_ope.setup_time + \
								int(self.qty / first_ope.qty_per_hour)
		logging.info("Start production of %s. 1st operation is %s. It will be finish at %s"% \
					(self.item, first_ope, self.next_time_change))
		self.ui_update()
	
	def push(self):
		'''If kanban is running and operation is finished, the kanban is pushed to the next operation
		return True if something done
		'''
		#logging.debug(str(self))
		if self.status == kanban.running:
			#logging.debug("It's running! next_time_change=%s | time = %s"%(self.next_time_change,self.fkanban.time))
			if self.next_time_change < self.fkanban.time:
				logging.info("%s is finished"%(self.item.operations[self.running_operation]))
				if self.running_operation + 1 == len(self.item.operations):
					self.status = kanban.full
					self.stock = self.qty
					self.running_operation = None
					self.next_time_change = None
					self.loop.kb_finish(self)
					logging.info("Kanban finished : %s"%(self))
					self.ui_update()
					return True
				else:
					next_ope = self.item.operations[self.running_operation+1]
					if next_ope.consume(self.qty):
						self.running_operation +=1
						self.next_time_change = self.fkanban.time + \
												next_ope.setup_time + \
												int(self.qty / next_ope.qty_per_hour)
						self.ui_update()
						return True
		return False
	
	def inventory(self):
		'''Calculate the stock cost in the kanban
		'''
		if self.status != kanban.running:
			return self.stock * self.item.cost
		else:
			# Add the cost of all operations produced or running
			cost = 0
			ope_no = 0
			while ope_no < len(self.item.operations):
				cost += self.qty*self.item.operations[ope_no].inventory()
				if self.running_operation == self.item.operations[ope_no]:
					break
				ope_no += 1
			return cost
					
					
					
					