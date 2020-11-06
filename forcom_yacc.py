#!/usr/bin/env python3 -B

import sys
try: 
	import ply.lex as lex
	import ply.yacc as yacc
except: 
	quit("FATAL: install module ply")
	
import forcom_lex
from forcom_lex import tokens


precedence = (
	("left", "OP_PLUS", "OP_MINUS"),
	("left", "OP_MUL", "OP_DIV", "OP_MOD"),
	#("right", "OP_U_MINUS", "OP_U_PLUS"),
)

def p_error(p):
	quit("yacc error: " + str(p))


def p_expression_number(p):
	'''expression : ATOM_NUM'''
	p[0] = ("ATOM", p[1])


def p_expression_binop(p):
	'''expression : expression OP_PLUS expression
                | expression OP_MINUS expression
                | expression OP_MUL expression
                | expression OP_DIV expression
	'''
	p[0] = ('EXP', 2, p[2], (p[1], p[3]))


def proc(text):

	print("Parse: \"" + text + "\"")

	try:
		lexer = forcom_lex.build(text)
		parser = yacc.yacc()
		result = parser.parse(text)
		
	except lex.LexError as e:
		print("lex error: " + e.args[0] + " - " + e.text)
		quit()	
		
	except yacc.YaccError as e:
		print("yacc error: " + str(e))
		quit()

	render(result)


def render(item, indent = ""):
	
	indent += "  "
	print(indent,end="")
	
	itemType = item[0]
	if itemType == "ATOM":
		
		atomValue = item[1]
		print("ATOM: " + str(atomValue))
		
	elif itemType == "EXP":
		
		expMemberCount = item[1]
		expType = item[2]
		expMemberList = item[3]

		print(
			"EXP(" 
			+ str(expMemberCount) 
			+ "): " 
			+ str(expType) 
		)
		
		for member in expMemberList: 
			render(member, indent)
		
	else: pass
