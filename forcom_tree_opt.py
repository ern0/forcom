#!/usr/bin/env python3 -B

from forcom_ast import Node


def proc(node):
	
	procChangeInlineConsts(node)
	
	
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
		node.setValue( str(int(result)) )
		return

	if "/" in value: result = round(result, 2)
	node.setError("invalid constant: " + node.getValue() + " = " + str(result))
	
