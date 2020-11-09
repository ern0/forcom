#!/usr/bin/env python3 -B

import forcom_lex as lex
import forcom_yacc as yacc
import sys


class Node:
	
	def __init__(self, nodeType = None):
		
		self.nodeType = nodeType
		self.value = None
		self.children = []
		self.error = None

	
	def setValue(self, value):
		self.value = str(value)
		
	
	def setError(self, error):
		self.error = error
	
	
	def fail(self):
		return self.error is not None
		
	
	def addChild(self, node):		
		self.children.append(node)
		
	
	def getChildrenCount(self):
		return len(self.children)
		
	
	def dump(self, indent = ""):
		
		if self.error is not None:
			quit(self.error)
		
		print(
			indent
			+ self.nodeType
			+ ": "
			+ self.value
		)

		indent += "    "

		for child in self.children:
			child.dump(indent)

