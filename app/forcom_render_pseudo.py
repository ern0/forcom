#!/usr/bin/env python3 -B

import forcom_ast as ast


class Instruction:

	def __init__(self, lvalue, op, rvalueLeft, rvalueRight):
		
		self.lvalue = lvalue
		self.op = op
		self.rvalueLeft = rvalueLeft
		self.rvalueRight = rvalueRight
		
		if len(self.rvalueLeft) == 0:
			self.parms = 1
		else:
			self.parms = 2
	
	
	def render(self):
		
		bracet = False
		if "=" in self.op: bracet = True
		if "<" in self.op: bracet = True
		if ">" in self.op: bracet = True
		
		result = self.lvalue + " = "
		
		if bracet: 
			result += "("
		
		if self.parms == 1:
			result += self.op + self.rvalueRight
			
		else:
			result += self.rvalueLeft + " "
			result += self.op + " " + self.rvalueRight
		
		if bracet:
			result += ")"
		
		return result + "\n"


class Ternary:
	
	def __init__(self, lvalue, cond, tval, fval):
	
		self.lvalue = lvalue
		self.cond = cond
		self.tval = tval
		self.fval = fval
	
	
	def render(self):
		
		result = "if " + self.cond + " then \n"
		result += "  " + self.lvalue + " = " + self.tval + "\n"
		result += "else \n"
		result += "  " + self.lvalue + " = " + self.fval + "\n"
		result += "endif \n"

		return result


class Data:

	def __init__(self, lvalue, dataName, dataValue):

		self.lvalue = lvalue
		self.dataName = dataName
		self.dataValue = dataValue


	def render(self):

		result = self.lvalue + " = "
		result += self.dataName
		result += "[" + self.lvalue + "]\n"
		
		return result


	def renderData(self):

		values = self.dataValue
		values = values.replace("[","")
		values = values.replace("]","")
		values = values.strip()

		result = self.dataName + ":"
		result += "\tdb " + values + "\n"

		return result


class PseudoRenderer:
	
	def __init__(self):

		self.instructionItems = []
		self.dataItems = []
		self.varId = 0
	
	
	def dump(self):
		print(self.render(), end="")


	def nextVar(self):
		
		while True:

			result = chr(ord('a') + self.varId)
			self.varId += 1

			if result == "t": continue
			break
			
		return result


	def nextDataName(self):

		numero = len(self.dataItems) + 1
		return "data" + str(numero)


	def createInstruction(self, lvalue, opStr, rvalueLeft, rvalueRight):

		item = Instruction(lvalue, opStr, rvalueLeft, rvalueRight)
		self.instructionItems.append(item)

	
	def createTernary(self, lvalue, cond, tvalue, fvalue):
		
		item = Ternary(lvalue, cond, tvalue, fvalue)
		self.instructionItems.append(item)
		

	def createData(self, lvalue, dataValue):

		dataName = self.nextDataName()

		item = Data(lvalue, dataName, dataValue)
		self.instructionItems.append(item)
		self.dataItems.append(item)
		

	def render(self):
		
		result = ""
		for dataItem in self.dataItems:
			result += dataItem.renderData()
		
		if result.strip() != "":
			result += "\n"

		for instructionItem in self.instructionItems:
			result += instructionItem.render()
			
		if result.strip() == "": 
			result = "t\n"
		
		return result

	
	def proc(self, node):
		
		for subNode in node.getChildren():
			self.proc(subNode)

		self.procNode(node)
	
	
	def procNode(self, node):
		
		nodeType = node.getType()
		
		if nodeType == "ATOM":
			return
			
		elif nodeType == "EXPR":
			self.procExpr(node)
			
		elif nodeType == "DATA":
			self.procData(node)

		else:
			print("INTERNAL: no renderer for node type: " + nodeType)
			node.dump()
			quit()


	def procExpr(self, node):
				
		v = node.getValue()
		if v.split("_")[0] == "OP": 
			self.procOpExpr(node)
		
		else:
			print("INTERNAL: no renderer for expression type")
			node.dump()
			quit()
		
	
	def procOpExpr(self, node):
		
		v = node.getValue()
		op = v[v.find("_") + 1:]

		if op == "PLUS": 
			self.procOp2(node, "+")

		elif op == "MINUS":
			self.procOp2(node, "-")

		elif op == "MUL":
			self.procOp2(node, "*")

		elif op == "DIV":
			self.procOp2(node, "/")

		elif op == "MOD":
			self.procOp2(node, "%")

		elif op == "SHL":
			self.procOp2(node, "<<")

		elif op == "SHR":
			self.procOp2(node, ">>")

		elif op == "AND":
			self.procOp2(node, "&")

		elif op == "OR":
			self.procOp2(node, "|")

		elif op == "XOR":
			self.procOp2(node, "^")

		elif op == "EQ":
			self.procOp2(node, "==")
		
		elif op == "NE":
			self.procOp2(node, "!=")
		
		elif op == "LT":
			self.procOp2(node, "<")

		elif op == "LE":
			self.procOp2(node, "<=")

		elif op == "GT":
			self.procOp2(node, ">")

		elif op == "GE":
			self.procOp2(node, ">=")

		elif op == "UNARY_MINUS":
			self.procOp1(node, "-")

		elif op == "UNARY_PLUS":
			self.procOp1(node, "+")

		elif op == "TERNARY":
			self.procOpTernary(node)
			
		else:
			print("INTERNAL: no renderer for operand type")
			node.dump()
			quit()
			
	
	def procOp1(self, node, opStr):
		
		if opStr == "+": return
		
		child = node.getChildren()[0]
		rtype = node.getType()
		rvalue = child.getValue()
		
		if rtype == "EXPR":
			lvalue = rvalue
		else:
			lvalue = self.nextVar()
		
		node.setValue(lvalue)
		
		self.createInstruction(lvalue, opStr, "", rvalue)
		
			
	def procOp2(self, node, opStr):

		children = node.getChildren()
		rtypeLeft = children[0].getType() 
		rtypeRight = children[1].getType() 
		rvalueLeft = children[0].getValue()
		rvalueRight = children[1].getValue()

		if rtypeLeft == "EXPR":
			lvalue = rvalueLeft
		elif rtypeRight == "EXPR":
			lvalue = rvalueRight
		else:
			lvalue = self.nextVar()	

		node.setValue(lvalue)
		
		self.createInstruction(lvalue, opStr, rvalueLeft, rvalueRight)


	def procOpTernary(self, node):
		
		children = node.getChildren()

		condType = children[0].getType()
		condValue = children[0].getValue()
		trueType = children[1].getType()
		trueValue = children[1].getValue()
		falseType = children[2].getType()
		falseValue = children[2].getValue()

		if condType == "EXPR":
			lvalue = condValue
		elif trueType == "EXPR":
			lvalue = trueValue
		elif falseType == "EXPR":
			lvalue = falseValue
		else:
			lvalue = self.nextVar()

		node.setValue(lvalue)

		self.createTernary(lvalue, condValue, trueValue, falseValue)


	def procData(self, node):

		child = node.getChildren()[0]

		dataValue = node.getValue()
		lvalue = child.getValue()

		self.createData(lvalue, dataValue)