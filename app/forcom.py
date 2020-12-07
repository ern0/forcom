#!/usr/bin/env python3 -B

import sys
import forcom_yacc as yacc
import forcom_ast as ast
import forcom_tree_opt as opt
import forcom_render_pseudo as rp
import forcom_render_graphviz as rg
import forcom_render_asm as ra


def main():

	argError = True	
	if len(sys.argv) == 3: 
		if sys.argv[2] == "tree": argError = False
		if sys.argv[2] == "graph": argError = False
		if sys.argv[2] == "pseudo": argError = False
		if sys.argv[2] == "asm": argError = False
	if argError:
		quit("specify file (or '-' for stdin) and mode (tree|graph|pseudo|asm)")

	processFile(sys.argv[1], sys.argv[2])


def processFile(fnam, prod):

	if fnam == '-': fnam = "/dev/stdin"
	fileHandle = open(fnam, mode="r")
	formula = normalize( fileHandle.read() )
	fileHandle.close()
	
	processText(formula, prod)
	

def normalize(formula):

	formula = formula.replace("\r","")
	formula = formula.replace("\n"," ")
	formula = formula.replace("\t"," ")
	for i in range(0,4):
		formula = formula.replace("  "," ")
	formula = formula.replace("( (", "((")
	formula = formula.replace(") )", "))")
	formula = formula.strip()

	return formula


def processText(formula, prod):
	
	node = yacc.proc(formula)
	opt.proc(node)	

	if prod == "tree":
		node.dump()

	elif prod == "graph":
		graph = rg.GraphvizRenderer()
		graph.proc(node)
		graph.dump()
		node.dump()

	elif prod == "pseudo":
		pseudo = rp.PseudoRenderer()
		pseudo.proc(node)
		pseudo.dump()
		print()
		node.dump()
	
	elif prod == "asm":
		asm = ra.AsmRenderer()
		asm.proc(node)
		asm.dump()


if __name__ == "__main__": 
	main()
