#!/usr/bin/env python3 -B

import sys
import forcom_yacc as yacc
import forcom_ast as ast
import forcom_tree_opt as opt
import forcom_render_pseudo as rp


def main():
	
	if True:
		return processText("[1,2,3,4][(t % 2 == 1 ? $ff : 0)]")

	if len(sys.argv) < 2:
		quit("specify file")

	processFile(sys.argv[1])


def processFile(fnam):

	fileHandle = open(fnam, mode="r")
	formula = fileHandle.read()
	formula = formula.replace("\n"," ")
	fileHandle.close()
	
	processText(formula)
	
	
def processText(formula):
	
	print(formula.strip())
	print("--")
	
	node = yacc.proc(formula)
	opt.proc(node)	
	
	renderer = rp.PseudoRenderer()
	renderer.proc(node)
	if False:
		node.dump()
		print("--")
	renderer.dump()

if __name__ == "__main__": 
	main()
