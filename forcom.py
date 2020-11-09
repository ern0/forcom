#!/usr/bin/env python3 -B

import forcom_yacc as yacc
import forcom_ast as ast


def main():

	node = yacc.proc("(t/4|t+3&t|t<<5&t+t-7%t*12|t%9>>13|t*(t%21)/13&t+(t/15))&t>>7")
	node.dump()


if __name__ == "__main__": 
	main()
