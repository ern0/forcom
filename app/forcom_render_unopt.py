from collections import OrderedDict
import forcom_ast as ast


class UnoptimizedRenderer:

	reg_t = "BX"


	def proc(self, node):

		self.code = []
		self.bss = []

		self.procRecursive(node)
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
			inst = "MOV AX," + self.getRepr(children[0])
			self.addInst(inst)
			inst = "ADD AX," + self.getRepr(children[1])
			self.addInst(inst)
			self.addStor(node)

		if node.getValue() == "OP_MINUS":
			inst = "MOV AX," + self.getRepr(children[0])
			self.addInst(inst)
			inst = "SUB AX," + self.getRepr(children[1])
			self.addInst(inst)
			self.addStor(node)

		if node.getValue() == "OP_SHR":
			inst = "MOV AX," + self.getRepr(children[0])
			self.addInst(inst)
			inst = "SHR AX," + self.getRepr(children[1])
			self.addInst(inst)
			self.addStor(node)

		if node.getValue() == "OP_SHL":
			inst = "MOV AX," + self.getRepr(children[0])
			self.addInst(inst)
			inst = "SHL AX," + self.getRepr(children[1])
			self.addInst(inst)
			self.addStor(node)




	def addInst(self, inst):
		self.code.append("\t" + inst)


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
			return UnoptimizedRenderer.reg_t
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
