# -*-coding:Latin-1 -*
import Tkinter
import logging
from kloop import *

class ui_stat(Tkinter.Tk):
	'''Windows for stat.
	'''
	def __init__(self, obj):
		'''Initialisation
			- obj	:	a obj (loop or Fkanban) with stat function
		'''
		Tkinter.Tk.__init__(self, None)
		self.obj=obj
		self.title('Statistiques for %s'%(obj.name))
		self.bt_refresh = Tkinter.Button(self, text=u'Refresh', command=self.refresh)
		self.bt_refresh.pack()
		self.list = Tkinter.Listbox(self, width = 50)
		self.list.pack(fill=Tkinter.BOTH, expand=1)
		self.refresh()
		
	
	def refresh(self):
		'''Refresh the window
		'''
		self.list.delete(0,Tkinter.END)
		for stat in reversed(self.obj.stat()):
			self.list.insert(Tkinter.END, stat)