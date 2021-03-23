from collections import OrderedDict
import forcom_ast as ast


class UnoptimizedRenderer:


	def proc(self, node):

		self.code = []
		self.data = []
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
		value = node.getValue()

		if value == "OP_PLUS": 
			self.procOpPlus(node)
		elif value == "OP_MINUS":
			self.procOpMinus(node)

		elif value == "OP_SHR":
			self.procOpShr(node)
		elif value == "OP_SHL":
			self.procOpShl(node)

		elif value == "OP_MUL":
			self.procOpMul(node)
		elif value == "OP_DIV":
			self.procOpDiv(node)
		elif value == "OP_MOD":
			self.procOpMod(node)

		elif value == "OP_OR":
			self.procOpOr(node)
		elif value == "OP_XOR":
			self.procOpXor(node)
		elif value == "OP_AND":
			self.procOpAnd(node)

		elif value == "OP_EQ":
			self.procOpEq(node)
		elif value == "OP_NE":
			self.procOpNe(node)
		elif value == "OP_LT":
			self.procOpLt(node)
		elif value == "OP_LE":
			self.procOpLe(node)
		elif value == "OP_GT":
			self.procOpGt(node)
		elif value == "OP_GE":
			self.procOpGe(node)

		elif value == "OP_UNARY_MINUS":
			self.procOpNeg(node)
		elif value == "OP_UNARY_NOT":
			self.procOpNot(node)

		else:
			quit("internal error: unimplemented " + value)

	def addInst(self, inst):		
		if inst != "": inst = "\t" + inst
		self.code.append(inst)

	def addLabel(self, label):
		if ":" not in label: label += ":"
		self.code.append(label)
		
	def addStor(self, node):
		
		inst = "MOV "+ self.getVarRef(node) + ",AX"
		self.addInst(inst)

		stor = self.getVarDef(node) + "\tDW ?"
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
	def procOpOr(self, node): self.procOpBase(node, "OR")
	def procOpXor(self, node): self.procOpBase(node, "XOR")
	def procOpAnd(self, node): self.procOpBase(node, "AND")

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
		if op == "DIV":
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


	def procOpNeg(self, node): self.procOpUnary(node, "NEG")
	def procOpNot(self, node): self.procOpUnary(node, "NOT")

	def procOpUnary(self, node, op):
		child = node.getChildren()[0]
		inst = "MOV AX," + self.getVarRef(child)
		self.addInst(inst)
		inst = op + " AX"
		self.addInst(inst)
		self.addStor(node)
