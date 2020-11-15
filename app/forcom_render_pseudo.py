#!/usr/bin/env python3 -B

import forcom_ast as ast


class Instruction:

	def __init__(self):
		
		self.op = None
		self.lvalue = None
		self.rvalue = None
	
	
	def dump(self):
		print(self.instType)
	

class PseudoRenderer:
	
	def __init__(self):
		self.items = []
		self.varId = 0
	
	
	def nextVar(self):
		
		while True:

			result = chr(ord('a') + self.varId)
			self.varId += 1

			if result == "t": continue
			break
			
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
			
		else:
			quit("INTERNAL: no renderer for node type: " + nodeType)


	def procExpr(self, node):
		
		a = node.getValue().split("_")
		
		if a[0] == "OP": 
			self.procOpExpr(node)
		
		else:
			quit("INTERNAL: no renderer for expr type: " + a[0])
		
	
	def procOpExpr(self, node):
		
		op = node.getValue().split("_")[1]

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

		else:
			quit("INTERNAL: no renderer for op type: " + op)

			
	def procOp2(self, node, opStr):

		children = node.getChildren()
		lvalue = children[0].getValue()
		if lvalue == "t": lvalue = self.nextVar()
		rvalueLeft = children[0].getValue()
		rvalueRight = children[1].getValue()

		node.setValue(lvalue)
		
		print(
			lvalue
			+ " = "
			+ rvalueLeft
			+ " " + opStr + " "
			+ rvalueRight
		)



	def dump(self):
		
		for item in self.items:
			item.dump()
