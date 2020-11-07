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
	("left", "OP_OR"),
	("left", "OP_XOR"),
	("left", "OP_AND"),
	("left", "OP_EQ", "OP_NE"),
	("left", "OP_LT", "OP_LE", "OP_GT", "OP_GE"),
	("left", "OP_SHL", "OP_SHR"),
	("left", "OP_PLUS", "OP_MINUS"),
	("left", "OP_MUL", "OP_DIV", "OP_MOD")
)

def p_error(p):
	quit("yacc error: " + str(p))


def tt(p, pos):
	return p.slice[pos].type


def p_expr_atom(p):
	'''expr : ATOM_NUM
          | ATOM_TEE
	'''
	p[0] = ("ATOM", p[1])


def p_expr_unop(p):
	'''expr : OP_PLUS expr
					| OP_MINUS expr
					| OP_NOT expr
	'''
	op = tt(p,1).replace("OP_","OP_UNARY_")
	p[0] = ("EXPR", 1, op, (p[2],))


def p_expr_binop(p):
	'''expr : expr OP_PLUS expr
					| expr OP_MINUS expr
					| expr OP_MUL expr
					| expr OP_DIV expr
					| expr OP_MOD expr
					| expr OP_SHL expr
					| expr OP_SHR expr 
					| expr OP_OR expr  
					| expr OP_XOR expr  
					| expr OP_AND expr  
					| expr OP_EQ expr  
					| expr OP_NE expr  
					| expr OP_LT expr  
					| expr OP_LE expr  
					| expr OP_GT expr  
					| expr OP_GE expr  
	'''
	p[0] = ('EXPR', 2, tt(p,2), (p[1], p[3]))


def p_expr_ternary(p):
	'''expr : BRACE_ROUND_OPEN expr SEP_QUESTION expr SEP_COLON expr BRACE_ROUND_CLOSE
	'''
	p[0] = ("EXPR", 3, "OP_TERNARY", (p[2], p[4], p[6]))


def p_list_naked_is_expr(p):
	'''expr : list_naked 	
	'''
	p[0] = p[1] 


def p_list_is_expr(p):
	'''expr : list 	
	'''
	p[0] = p[1] 
	

def p_list_num_naked(p):
	'''list_naked : ATOM_NUM SEP_COMMA ATOM_NUM
	              | ATOM_NUM SEP_COMMA list_naked
	'''
	p[0] = ("LIST", "naked", (p[1], p[3]))


def p_list_num(p):
	'''list : BRACE_SQUARE_OPEN list_naked BRACE_SQUARE_CLOSE
	'''
	p[0] = ("LIST", "num", (p[2],))
	
	
def p_list_str(p):
	'''list : ATOM_QUOTED
	'''
	p[0] = ("LIST", "str", (p[1],))
	
	
def p_array(p):
	'''expr : list BRACE_SQUARE_OPEN expr BRACE_SQUARE_CLOSE
	'''
	p[0] = ("ARRAY", (p[1], p[3]))
	
	
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


def items2str(item):
	
	list_str = ""
	while True:

		value = item[2][0]
		if list_str is not "": list_str += ","
		list_str += str(value)
		
		value = item[2][1]
		if type(value) != tuple:
			list_str += "," + str(value)
			break
		
		item = value
		
	return list_str
	

def render(item, indent = ""):
	
	indent += "  "
	print(indent,end="")
	dataNamePostfix = 1

	itemType = item[0]	
	
	if itemType == "ATOM": 
		renderAtom(item)
	
	elif itemType == "EXPR": 
		renderExpr(item, indent)
	
	elif itemType == "LIST": 
		renderListError(item)
	
	elif itemType == "ARRAY": 
		name = "data" + str(dataNamePostfix)
		dataNamePostfix += 1
		renderArray(item, indent, name)
	
	else: 
		quit("INTERNAL: item type: " + itemType)
	

def renderAtom(item):
		
	atomValue = item[1]
	print("ATOM: " + str(atomValue))
		
		
def renderExpr(item, indent):
		
	expMemberCount = item[1]
	expType = item[2]
	expMemberList = item[3]

	print(
		"EXPR(" 
		+ str(expMemberCount) 
		+ "): " 
		+ str(expType) 
	)

	for memberItem in expMemberList: 
		render(memberItem, indent)	

	
def renderListError(item):
		
	subType = item[1]
	
	if subType == "naked":			 
		quit("FATAL: value list outside array: " + items2str(item))
	
	if subType == "num":
		quit("FATAL: standalone value array: [" + items2str(item[2][0]) + "]")

	if subType == "str":
		quit("FATAL: standalone value string: \"" + item[2][0] + "\"")

	if subType == "array":
		quit("FATAL: string in array: \"" + item[2][2][0] + "\"")
		
	quit("INTERNAL: item LIST, subtype: " + subType)
		

def renderArray(item, indent, name):
	
	subType = item[1][0][1]
	if subType == "num":
		values = "[" + items2str( item[1][0][2][0] ) + "]"
	else: 
		values = "\"" + item[1][0][2][0] + "\""
	index = item[1][1]
	
	print(
		"DATA(1):"
		+ " name="
		+ name
		+ " values="
		+ values
	)
	
	render(index, indent)
	
