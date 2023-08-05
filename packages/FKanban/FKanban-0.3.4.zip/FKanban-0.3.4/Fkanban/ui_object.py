# -*-coding:Latin-1 -*
import Tkinter
import logging
from ui_stat import *

class ui_object (Tkinter.Frame):
	""" Object for Graphical Interface for FKanban
	"""
	ui_color = 'grey'
	ui_out_of_stock_color = 'firebrick'
	ui_nb_max_kanban_rows = 25
	def __init__(self, *args, **kwargs):
		self.ui_init(*args, **kwargs)

	def __str__(self):
		return "(%s)"%(self.ui_label)
	
	def ui_init(self, parent=None, column=0, row=0, ui_title = None, title_font = ('arial', 8), nb_columns = 1):
		'''Initialisation
			- parent	:	Tkinter parent (ex : ui_Fkanban)
		'''
		self.parent = parent
		Tkinter.Frame.__init__(self, parent, borderwidth=2, relief=Tkinter.GROOVE, bg = self.ui_color)
		self.grid(column=column, row=row, sticky = Tkinter.N)
		if not ui_title:
			ui_title = self.name
		self.ui_label = Tkinter.Label(self,text = ui_title, bg = self.ui_color, wraplength = 40,  font = title_font)
		self.ui_label.grid(column = 0, row = 0, columnspan = nb_columns)
		self.next_row = 1
	
	def ui_change_label(self, txt=""):
		'''Change the label
		'''
		try:
			self.ui_label['text'] = txt
		except AttributeError:
			pass
	
	def ui_add_text(self, text, title_font = ('arial', 8)):
		Tkinter.Label(self,text = text, bg = self.ui_color, wraplength = 70, anchor=Tkinter.W, justify=Tkinter.LEFT, font = title_font).grid(column = 0, row = self.next_row)
		self.next_row +=1
	
	def place_kanbans(self, kbs = [], nb_columns = 1):
		'''Place the Kanbans
		'''
		i = 0
		nb_rows = len(kbs)/nb_columns
		row = self.next_row
		for kb in kbs:
			column = i / nb_rows
			row = self.next_row + i%nb_rows
			kb.ui_init(self, column = column, row = row)
			i +=1
		self.next_row = row + 1
	
class ui_loop(ui_object):
	'''a kanban loop
	'''
	ui_color = 'yellow'
	def __init__(self, *args, **kwargs):
		self.out_frame = None
		operations_frame = None
	
	def ui_init(self, parent=None, column=0, row=0):
		ui_object.ui_init(self, parent, column, row)
		self.bt_stat = Tkinter.Button(self, text=u'Stat.', command=self.on_bt_stat)
		self.bt_stat.grid(column=0, row=1)
		## a frame for Output
		self.out_frame = ui_output_frame(self, column=0, row = 2, nb_columns = self.nb_columns)
		self.out_frame.place_kanbans(self.kanbans, self.nb_columns)
		## a frame for operations
		self.operations_frame = ui_operations_frame(self, column=0, row = 3)
		# with operations
		row = len(self.item.operations)*2
		self.operations_frame.next_row = row +1
		for operation in self.item.operations:
			operation.ui_init(self.operations_frame, 0, row, nb_columns = self.nb_columns)
			if row > 1:
				Tkinter.Label(self.operations_frame, text = '↑').grid(column = 0, row = row-1)
			row -=2
	
	def ui_out_of_stock(self, out_of_stock = True):
		''' 
		'''
		if out_of_stock:
			self.out_frame['bg'] = self.out_frame.ui_out_of_stock_color
		else:
			self.out_frame['bg'] = self.out_frame.ui_color
	
	def on_bt_stat(self):
		ui_stat(self)
	
	@property
	def nb_columns(self):
		return 1 + ((len(self.item.operations)+2) * self.nb_kanban())/self.ui_nb_max_kanban_rows
	
class ui_fab_kloop(ui_loop):
	'''A fab kanban loop
	'''
	def __init__(self, *args, **kwargs):
		ui_loop.__init__(self, *args, **kwargs)
		self.board_frame = None
	
	def ui_init(self, parent=None, column=0, row=0):
		ui_loop.ui_init(self, parent, column, row)
		self.board_frame = ui_board_frame(self, column=0, row = 4, nb_columns = self.nb_columns)
		self.board_frame.place_kanbans(self.kanbans, self.nb_columns)


class ui_customer_kloop(ui_loop):
	'''A customer kanban loop
	'''
	def ui_init(self, parent=None, column=0, row=0):
		ui_loop.ui_init(self, parent, column, row)

class ui_board_frame(ui_object):
	'''A board kanban frame
	'''
	ui_color = 'skyblue'
	def __init__(self, *args, **kwargs):
		ui_object.__init__(self, *args, ui_title = 'K-Board', **kwargs)

class ui_output_frame(ui_object):
	'''A board kanban frame
	'''
	ui_color = 'pale green'
	def __init__(self, *args, **kwargs):
		ui_object.__init__(self, *args, ui_title = 'Output', **kwargs)

class ui_operations_frame(ui_object):
	'''A board kanban frame
	'''
	def __init__(self, *args, **kwargs):
		ui_object.__init__(self, *args, ui_title = 'Oper.', **kwargs)

class ui_operation(ui_object):
	'''Operation
	'''
	ui_color = 'snow3'
	def ui_init(self, *args, **kwargs):
		ui_object.ui_init(self, *args, **kwargs)
		self.place_kanbans(self.parent.parent.kanbans, self.parent.parent.nb_columns)
	
	def ui_out_of_stock(self, out_of_stock = True):
		if out_of_stock:
			self['bg'] = self.ui_out_of_stock_color
		else:
			self['bg'] = self.ui_color
		
class ui_kanban():
	'''Kanban
	'''
	ui_color = 'bisque'
	def __init__(self):
		self.ui_objects={}
	
	def ui_init(self, parent=None, column=0, row=0):
		self.ui_objects[parent]=ui_kanban_instance(parent, column, row, ui_title = self.ui_title(), title_font=('courrier', 6))
	
	def ui_title(self):
		return str(self.stock).zfill(len(str(self.qty)))
		#return "%s/%s"%(self.stock, self.qty)
		
	def ui_change_label(self):
		'''Change the label
		'''
		for kb_instance in self.ui_objects.values():
			kb_instance.ui_change_label(self.ui_title())
		
	def ui_update(self):
		'''Update the colors of differents instance of the kanban (board_frame, output_frame, operations_frames)
		'''
		if self.status == 0: #empty kanban
			for parent in self.ui_objects:
				if isinstance(parent,ui_board_frame):
					self.ui_objects[parent].ui_label.configure(bg = 'bisque')
					self.ui_objects[parent].ui_label.configure(fg = 'black')
				else:
					self.ui_objects[parent].ui_label.configure(bg = 'bisque')
					self.ui_objects[parent].ui_label.configure(fg = 'bisque')
		elif self.status == 2: #full kanban
			for parent in self.ui_objects:
				if isinstance(parent,ui_output_frame):
					self.ui_objects[parent].ui_label.configure(bg = 'navy')
					self.ui_objects[parent].ui_label.configure(fg = 'white')
				else:
					self.ui_objects[parent].ui_label.configure(bg = 'bisque')
					self.ui_objects[parent].ui_label.configure(fg = 'bisque')
		elif self.status == 3:# half full kanban
			for parent in self.ui_objects:
				if isinstance(parent,ui_output_frame):
					self.ui_objects[parent].ui_label.configure(bg = 'turquoise')
					self.ui_objects[parent].ui_label.configure(fg = 'black')
				elif isinstance(parent,ui_board_frame):
					self.ui_objects[parent].ui_label.configure(bg = 'turquoise')
					self.ui_objects[parent].ui_label.configure(fg = 'black')
				else:
					self.ui_objects[parent].ui_label.configure(bg = 'bisque')
					self.ui_objects[parent].ui_label.configure(fg = 'bisque')
		else: # Running kanban
			for parent in self.ui_objects:
				if parent==self.item.operations[self.running_operation]:
					self.ui_objects[parent].ui_label.configure(bg = 'salmon')
					self.ui_objects[parent].ui_label.configure(fg = 'black')
				else:
					self.ui_objects[parent].ui_label.configure(bg = 'bisque')
					self.ui_objects[parent].ui_label.configure(fg = 'bisque')

class ui_kanban_instance(ui_object):
	''' Instance de kanban
	'''
	ui_color = 'ivory'
