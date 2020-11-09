#!/usr/bin/env python3 -B

import forcom_yacc as yacc
import forcom_ast as ast


def main():

	node = yacc.proc("t * 1000 / 12")
	node.dump()


if __name__ == "__main__": 
	main()
