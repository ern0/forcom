from collections import OrderedDict
import forcom_ast as ast


class UnoptimizedRenderer:


	def proc(self, node):

		self.code = []
		self.bss = []

		debug = True

		if debug:
			self.addInst("ORG 100H")
			self.addInst("")
			self.addInst("MOV SI,12")
			self.addInst("")
		else:
			self.addLabel("formula")

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

	def addLabel(self, label):
		if ":" not in label: label += ":"
		self.code.append(label)
		
	def addStor(self, node):
		
		inst = "MOV "+ self.getVarRef(node) + ",AX"
		self.addInst(inst)

		stor = self.getVarDef(node) + "\tDW 0"
		self.bss.append(stor)


	def getSymbolName(self, node, prefix):
		return prefix + str(node.getNumero())


	def getVarRef(self, node):

		if node.getType() == "ATOM": 
			if node.getValue() == "t": 
				return "SI"
			else: 
				return str(node.getValue())
		if node.getType() == "EXPR":
			return "[" + self.getSymbolName(node, "VAR") + "]"
	
	def getVarDef(self, node):
		return self.getSymbolName(node, "VAR") + ":"

	def getLabelRef(self, node):
		return self.getSymbolName(node, "LBL")

	def getLabelDef(self, node):
		return self.getSymbolName(node, "LBL") + ":"
	

	def render(self, node):

		print("; " + node.getFormula())
		print()

		for inst in self.code: print(inst)
		print()
		for var in self.bss: print(var)


	def procOpPlus(self, node): self.procOpBase(node, "ADD")
	def procOpMinus(self, node): self.procOpBase(node, "SUB")
	def procOpShl(self, node): self.procOpBase(node, "SHL")
	def procOpShr(self, node): self.procOpBase(node, "SHR")

	def procOpBase(self, node, op):
		children = node.getChildren()
		inst = "MOV AX," + self.getVarRef(children[0])
		self.addInst(inst)
		inst = op + " AX," + self.getVarRef(children[1])
		self.addInst(inst)
		self.addStor(node)


	def procOpMul(self, node): self.procOpSlow(node, "MUL", False)
	def procOpDiv(self, node): self.procOpSlow(node, "DIV", False)
	def procOpMod(self, node): self.procOpSlow(node, "DIV", True)

	def procOpSlow(self, node, op, useDx):
		children = node.getChildren()
		inst = "MOV AX," + self.getVarRef(children[0])
		self.addInst(inst)
		inst = "CWD"
		self.addInst(inst)
		inst = "MOV CX," + self.getVarRef(children[1])
		self.addInst(inst)
		inst = op + " CX"
		self.addInst(inst)
		if useDx:
			inst = "MOV AX,DX"
			self.addInst(inst)
		self.addStor(node)


	def procOpEq(self, node): self.procOpCond(node, "JE")
	def procOpNe(self, node): self.procOpCond(node, "JNE")
	def procOpLt(self, node): self.procOpCond(node, "JL")
	def procOpLe(self, node): self.procOpCond(node, "JLE")
	def procOpGt(self, node): self.procOpCond(node, "JG")
	def procOpGe(self, node): self.procOpCond(node, "JGE")

	def procOpCond(self, node, jcc):
		children = node.getChildren()
		inst = "MOV AX,1"
		self.addInst(inst)
		inst = "MOV DX," + self.getVarRef(children[0])
		self.addInst(inst)
		inst = "CMP DX," + self.getVarRef(children[1])
		self.addInst(inst)
		inst = jcc + " " + self.getLabelRef(node)
		self.addInst(inst)
		inst = "XOR AX,AX"
		self.addInst(inst)
		self.addLabel(self.getLabelDef(node))
		self.addStor(node)
