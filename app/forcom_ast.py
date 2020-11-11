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


	def cloneFrom(self, node):
		
		self.nodeType = node.nodeType
		self.value = node.value
		self.children = node.children
		self.error = node.error
		

	def setType(self, nodeType):
		self.nodeType = nodeType
		
	
	def getType(self):
		return self.nodeType
		
		
	def setValue(self, value):
		self.value = str(value)
	
	
	def getValue(self):
		return self.value
		
	
	def setError(self, error):
		self.error = error
	
	
	def fail(self):
		return self.error is not None
		
	
	def addChild(self, node):		
		self.children.append(node)
		
	
	def getChildrenCount(self):
		return len(self.children)
	
	
	def isLeaf(self):
		return len(self.children) == 0
	
	
	def getChildren(self):
		return self.children
		
	
	def getChild(self, index):
		return self.children[index]
		
	
	def removeChildren(self):
		self.children = []
		
	
	def dump(self, indent = ""):
		
		if self.error is not None:
			quit(self.error)
		
		print(
			indent
			+ self.nodeType
			+ ": "
			+ self.value
		)

		indent += " "*2

		for child in self.children:
			child.dump(indent)

