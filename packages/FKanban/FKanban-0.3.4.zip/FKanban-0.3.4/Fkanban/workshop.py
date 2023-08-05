# -*-coding:Latin-1 -*
from ui_object import *

class workshop(ui_object):
	''' a workshop with kanbans
	'''
	def __init__(self, name):
		'''Initialisation
			- name
		'''
		self.name = name
		
	
	def __str__(self):
		return self.name