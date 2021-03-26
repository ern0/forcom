from forcom_ast import Node


def proc(node):
	
	procRemoveUnaryPlus(node)
	procChangeInlineConsts(node)
	
	for i in range(1,100):
		changeCount = procResolveConstPairs(node)
		changeCount += procResolveSingleAtomInBrace(node)
		if changeCount == 0: break
	

def procRemoveUnaryPlus(node):

	for subNode in node.getChildren():
		procRemoveUnaryPlus(subNode)

	if node.getType() != "EXPR": return
	if node.getValue() != "OP_UNARY_PLUS": return

	node.cloneFrom(node.getChildren()[0])
	

def procChangeInlineConsts(node):
	
	for subNode in node.getChildren():
		procChangeInlineConsts(subNode)
	
	if node.getType() != "ATOM": return
	
	value = node.getValue()
	
	if "*" in value: 
		a = value.split("*")
		v1 = float(a[0].strip())
		v2 = float(a[1].strip())
		result = v1 * v2

	elif "/" in value: 
		a = value.split("/")
		v1 = float(a[0].strip())
		v2 = float(a[1].strip())
		result = v1 / v2

	else:
		return
		
	if result == int(result):
		node.setParsedValue(int(result))
		return

	if "/" in value: result = round(result, 2)
	node.setError("invalid constant: " + node.getValue() + " = " + str(result))
	

def procResolveConstPairs(node):
	
	if _prcpHasTwoLeafConstChildren(node):
		return _prcpUnifyLeafChildren(node)
	
	else:
		return _prcpProcChildren(node)


def _prcpHasTwoLeafConstChildren(node):
		
	if node.getChildrenCount() != 2: return False
	if not node.getChild(0).isLeaf(): return False
	if "t" in node.getChild(0).getValue(): return False
	if not node.getChild(1).isLeaf(): return False
	if "t" in node.getChild(1).getValue(): return False
	
	return True
			

def _prcpUnifyLeafChildren(node):

	if node.getType() != "EXPR": return 0
	
	a = node.getValue().split("_")
	if a[0] != "OP": return 0

	op = a[1]
	v0 = int( node.getChild(0).getValue() )
	v1 = int( node.getChild(1).getValue() )
	
	if op == "PLUS":
		result = v0 + v1
	elif op == "MINUS":
		result = v0 - v1
	elif op == "MUL":
		result = v0 * v1
	elif op == "DIV":
		result = v0 / v1
	elif op == "MOD":
		result = v0 % v1
	elif op == "SHL":
		result = v0 << v1
	elif op == "SHR":
		result = v0 >> v1
	else:
		return 0
	
	node.setType("ATOM")
	node.setValue(result, "OPTIMIZED")
	node.removeChildren()
	return 1
	

def _prcpProcChildren(node):

	changeCount = 0;
	
	for subNode in node.getChildren():
		changeCount += procResolveConstPairs(subNode)
	
	return changeCount


def procResolveSingleAtomInBrace(node):
	
	changeCount = _rsaibCloneChildren(node)
	if changeCount != 0: return changeCount 
		
	for subNode in node.getChildren():
		changeCount += procResolveSingleAtomInBrace(subNode)
	
	return changeCount
	

def _rsaibCloneChildren(node):

	if node.getType() != "EXPR": return 0
	if node.getValue() != "BRACED": return 0
	#if node.getChildrenCount() != 1: return 0
	
	child = node.getChild(0)
	#if child.getType() != "ATOM": return 0
	
	node.cloneFrom(child)
	return 1
