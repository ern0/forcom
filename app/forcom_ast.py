import forcom_lex as lex
import forcom_yacc as yacc
import sys


class Node:

	nextNumero = 1
	
	def __init__(self, nodeType = None):
		
		self.nodeType = nodeType
		self.value = None
		self.children = []
		self.error = None
		self.parsedValue = None
		self.formula = None
		self.numero = Node.nextNumero
		Node.nextNumero += 1


	def cloneFrom(self, node):
		
		self.nodeType = node.nodeType
		self.value = node.value
		self.children = node.children
		self.error = node.error
		self.parsedValue = node.parsedValue
		self.formula = node.formula
		self.numero = node.numero
		

	def setFormula(self, formula):
		self.formula = formula


	def getFormula(self):
		return self.formula


	def setNumero(self, numero):
		self.numero = numero

	
	def getNumero(self):
		return self.numero
		
		
	def setType(self, nodeType):
		self.nodeType = nodeType
		
	
	def getType(self):
		return self.nodeType
		
		
	def setValue(self, value, parsed = None):
		self.value = str(value)
		if parsed is not None: self.parsedValue = parsed
	

	def setParsedValue(self, value):
		self.setValue(value, value)
	
	
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
		

	def dumpFlat(self, indent = ""):

		if self.error is not None:
			quit(self.error)

		print(indent, end="")

		print(self.nodeType, end="")
		if self.nodeType == "EXPR" or self.nodeType == "DATA":
			print(" #" + str(self.numero), end="")
		print(": ", end="")

		print(self.parsedValue, end="")
		if self.parsedValue != self.value: 
			print(" (" + self.value, end = ")")		
		print("")


	def dump(self, indent = ""):
				
		self.dumpFlat(indent)

		indent += " "*2

		for child in self.children:
			child.dump(indent)