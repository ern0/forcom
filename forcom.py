#!/usr/bin/env python3 -B

import forcom_yacc as yacc
import forcom_ast as ast
import forcom_tree_opt as opt


def main():

	node = yacc.proc("t * 1000 / 3")
	node.dump()
	print("--")
	opt.proc(node)
	print("--")
	node.dump()


if __name__ == "__main__": 
	main()
