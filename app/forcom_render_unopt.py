from collections import OrderedDict
import forcom_ast as ast


class UnoptimizedRenderer:


	def proc(self, node):

		self.code = []
		self.bss = []

		debug = True

		self.addInst("ORG 100H")
		self.addInst("")

		if debug:
			self.addInst("MOV BX,5")
			self.addInst("")

		self.procRecursive(node)
		self.addInst("")

		if debug:
			self.addInst("INT3")
		
		self.addInst("RET")


	def procRecursive(self, node):

		self.procSubs(node)
		self.procActual(node)
	

	def procSubs(self,node):

		subNodes = node.getChildren()
		for subNode in subNodes:
			self.procRecursive(subNode)


	def procActual(self, node):
		
		if node.getType() == "ATOM": return

		#self.addInst("; node #" + str(node.getNumero()))
		children = node.getChildren()

		if node.getValue() == "OP_PLUS": 
			self.procOpPlus(node)
		if node.getValue() == "OP_MINUS":
			self.procOpMinus(node)

		if node.getValue() == "OP_SHR":
			self.procOpShr(node)
		if node.getValue() == "OP_SHL":
			self.procOpShl(node)

		if node.getValue() == "OP_MUL":
			self.procOpMul(node)
		if node.getValue() == "OP_DIV":
			self.procOpDiv(node)
		if node.getValue() == "OP_MOD":
			self.procOpMod(node)

		if node.getValue() == "OP_OR":
			self.procOpOr(node)
		if node.getValue() == "OP_XOR":
			self.procOpXor(node)
		if node.getValue() == "OP_AND":
			self.procOpAnd(node)

		if node.getValue() == "OP_EQ":
			self.procOpEq(node)
		if node.getValue() == "OP_NE":
			self.procOpNe(node)
		if node.getValue() == "OP_LT":
			self.procOpLt(node)
		if node.getValue() == "OP_LE":
			self.procOpLe(node)
		if node.getValue() == "OP_GT":
			self.procOpGt(node)
		if node.getValue() == "OP_GE":
			self.procOpGe(node)


	def addInst(self, inst):
		
		if inst != "": inst = "\t" + inst
		self.code.append(inst)


	def addStor(self, node):
		
		name = self.getLabel(node)

		inst = "MOV [" + name + "],AX"
		self.addInst(inst)

		stor = name + ":\tDW 0"
		self.bss.append(stor)


	def getLabel(self, node):
		return "var" + str(node.getNumero())


	def getRepr(self, node):

		if node.getType() == "ATOM": 
			return self.getReprAtom(node)
		if node.getType() == "EXPR":
			return self.getReprExpr(node)
	

	def getReprAtom(self, node):

		if node.getValue() == "t": 
			return "BX"
		else:
			return str(node.getValue())


	def getReprExpr(self, node):
		return "[" + self.getLabel(node) + "]"
	

	def render(self, node):

		print("; " + node.getFormula())
		print()

		for inst in self.code: print(inst)
		print()
		for var in self.bss: print(var)


	def procOpPlus(self, node):
		children = node.getChildren()
		inst = "MOV AX," + self.getRepr(children[0])
		self.addInst(inst)
		inst = "ADD AX," + self.getRepr(children[1])
		self.addInst(inst)
		self.addStor(node)

	def procOpMinus(self, node):
		children = node.getChildren()
		inst = "MOV AX," + self.getRepr(children[0])
		self.addInst(inst)
		inst = "SUB AX," + self.getRepr(children[1])
		self.addInst(inst)
		self.addStor(node)

	def procOpShr(self, node):
		children = node.getChildren()
		inst = "MOV AX," + self.getRepr(children[0])
		self.addInst(inst)
		inst = "SHR AX," + self.getRepr(children[1])
		self.addInst(inst)
		self.addStor(node)

	def procOpShl(self, node):
		children = node.getChildren()
		inst = "MOV AX," + self.getRepr(children[0])
		self.addInst(inst)
		inst = "SHL AX," + self.getRepr(children[1])
		self.addInst(inst)
		self.addStor(node)

	def procOpMul(self, node):
		children = node.getChildren()
		inst = "MOV AX," + self.getRepr(children[0])
		self.addInst(inst)
		inst = "MOV CX," + self.getRepr(children[1])
		self.addInst(inst)
		inst = "MUL CX"
		self.addInst(inst)
		self.addStor(node)

	def procOpDiv(self, node):
		children = node.getChildren()
		inst = "MOV AX," + self.getRepr(children[0])
		self.addInst(inst)
		inst = "CDW"
		self.addInst(inst)
		inst = "MOV CX," + self.getRepr(children[1])
		self.addInst(inst)
		inst = "DIV CX"
		self.addInst(inst)
		self.addStor(node)

	def procOpMod(self, node):
		children = node.getChildren()
		inst = "MOV AX," + self.getRepr(children[0])
		self.addInst(inst)
		inst = "CDW"
		self.addInst(inst)
		inst = "MOV CX," + self.getRepr(children[1])
		self.addInst(inst)
		inst = "DIV CX"
		self.addInst(inst)
		inst = "MOV AX,DX"
		self.addInst(inst)
		self.addStor(node)
