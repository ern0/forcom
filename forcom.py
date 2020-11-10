#!/usr/bin/env python3 -B

import forcom_yacc as yacc
import forcom_ast as ast
import forcom_tree_opt as opt


def main():

	proc("1 * 2 * 3 * 4 * 5 + 1 * t")
	

def proc(f):
	
	print(f)
	node = yacc.proc(f)
	node.dump()
	print("--")
	opt.proc(node)
	print("--")
	node.dump()


if __name__ == "__main__": 
	main()
