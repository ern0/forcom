from collections import OrderedDict
import forcom_ast as ast


class RpnRenderer:


	def proc(self, node):

		self.node = node
		self.data = []
		self.code = []
		self.ops = {}
		self.procSwap(node)
		self.procNode(node)
		self.render()
	

	def procSwap(self, node):

		if node.getType() == "EXPR":
			self.swap(node, "OP_GT", "OP_LT")
			self.swap(node, "OP_GE", "OP_LE")

		children = node.getChildren()
		for child in children: 
			self.procSwap(child)


	def swap(self, node, opChangeFrom, opChangeTo):

		if node.getValue() != opChangeFrom: return

		node.swapChildren()
		node.setValue(opChangeTo, opChangeTo)
	

	def procNode(self, node):

		children = node.getChildren()
		for child in children: 
			self.procNode(child)
	
		if node.getType() == "ATOM":
			self.appendPush(node.getValue())
		
		if node.getType() == "EXPR":
			self.appendOp(node.getValue())
	

	def appendPush(self, value):

		if value == "t":
			self.appendOp("PUSH_T")
		else:
			self.code.append("push " + str(value))

	
	def appendOp(self, op):

		self.code.append(op)
		self.ops[op] = None

	
	def render(self):

		print(self.node.getFormula(), end="\n--\n")

		print("CODE:")
		for token in self.code:
			print("  " + token)

		print("OP-LIST:")
		for op in self.ops:
			print("  " + op)