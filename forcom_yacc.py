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
	'''expression : ATOM_NUM
	              | ATOM_TEE
	'''
	p[0] = ("ATOM", p[1])


def p_expression_unop(p):
	'''expression : OP_PLUS expression
	              | OP_MINUS expression
	              | OP_NOT expression
	'''
	p[0] = ("EXP", 1, p[1], (p[2],))


def p_expression_binop(p):
	'''expression : expression OP_PLUS expression
                | expression OP_MINUS expression
                | expression OP_MUL expression
                | expression OP_DIV expression
                | expression OP_MOD expression
                | expression OP_SHL expression
                | expression OP_SHR expression 
                | expression OP_OR expression  
                | expression OP_XOR expression  
                | expression OP_AND expression  
                | expression OP_EQ expression  
                | expression OP_NE_1 expression  
                | expression OP_NE_2 expression  
                | expression OP_LT expression  
                | expression OP_LE expression  
                | expression OP_GT expression  
                | expression OP_GE expression  
	'''
	p[0] = ('EXP', 2, p[2], (p[1], p[3]))


def p_expression_ternary(p):
	'''expression : BRACE_ROUND_OPEN expression SEP_QUESTION expression SEP_COLON expression BRACE_ROUND_CLOSE
	'''
	p[0] = ("EXP", 3, p[3], (p[2], p[4], p[6]))


def p_expression_braced(p):
	'''expression : BRACE_ROUND_OPEN expression BRACE_ROUND_CLOSE
	'''
	p[0] = ("EXP", 1, p[1], (p[2],))


def proc(text):

	print("YACC: \"" + text + "\"")

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
