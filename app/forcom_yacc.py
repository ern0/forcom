import sys
try: 
	import ply.lex as lex
	import ply.yacc as yacc
except: 
	quit("FATAL: install module ply")
	
import forcom_lex
from forcom_lex import tokens
from forcom_ast import Node


precedence = (
	("left", "OP_OR"),
	("left", "OP_XOR"),
	("left", "OP_AND"),
	("left", "OP_EQ", "OP_NE"),
	("left", "OP_LT", "OP_LE", "OP_GT", "OP_GE"),
	("left", "OP_PLUS", "OP_MINUS"),
	("left", "OP_SHL", "OP_SHR"),
	("left", "OP_MUL", "OP_DIV", "OP_MOD")
)

def p_error(p):
	if p is None: p_error("empty source")
	quit("yacc error: " + str(p))


def tt(p, pos):
	return p.slice[pos].type


def p_expr_atom(p):
	'''expr : ATOM_INT
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
	p[0] = ('EXPR', 2, tt(p,2), (p[1], p[3],))


def p_expr_ternary(p):
	'''expr : BRACE_ROUND_OPEN expr SEP_QUESTION expr SEP_COLON expr BRACE_ROUND_CLOSE
	'''
	p[0] = ("EXPR", 3, "OP_TERNARY", (p[2], p[4], p[6],))


def p_expr_braced(p):
	'''expr : BRACE_ROUND_OPEN expr BRACE_ROUND_CLOSE
	'''
	p[0] = ("EXPR", 1, "BRACED", (p[2],))
	

def p_list_is_expr(p):
	'''expr : list 	
	'''
	p[0] = p[1] 
	

def p_list_num_naked(p):
	'''list_naked : ATOM_INT SEP_COMMA ATOM_INT
	              | ATOM_INT SEP_COMMA list_naked
	'''
	p[0] = ("LIST", "naked", (p[1], p[3],))


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
	p[0] = ("ARRAY", (p[1], p[3],))


def p_fn_min(p):
	'''fn : FN_MIN BRACE_ROUND_OPEN expr SEP_COMMA expr BRACE_ROUND_CLOSE
	'''
	p[0] = ("EXPR", 2, "FN_MIN", (p[3], p[5],))


def p_fn_max(p):
	'''fn : FN_MAX BRACE_ROUND_OPEN expr SEP_COMMA expr BRACE_ROUND_CLOSE
	'''
	p[0] = ("EXPR", 2, "FN_MAX", (p[3], p[5],))


def p_fn_is_expr(p):
	'''expr : fn 	
	'''
	p[0] = p[1] 


def proc(formula):

	node = Node()

	try:
		lexer = forcom_lex.build(formula)
		parser = yacc.yacc()
		result = parser.parse(formula)
		if result is None: 
			node.setError("yacc: parse error")
		
	except lex.LexError as e:
		node.setError("lex error: " + e.args[0] + " - " + e.text)
		
	except yacc.YaccError as e:
		node.setError("yacc error: " + str(e))
		
	if not node.fail(): 
		node = parse(result)
		node.setFormula(formula)

	return node


def items2str(item):
	
	list_str = ""
	while True:

		value = item[2][0]
		if list_str != "": list_str += ","
		list_str += str(value)
		
		value = item[2][1]
		if type(value) != tuple:
			list_str += "," + str(value)
			break
		
		item = value
		
	return list_str
	

def parse(item):
	
	itemType = item[0]	
	
	if itemType == "ATOM": 
		return parseAtom(item)
	
	elif itemType == "EXPR": 
		return parseExpr(item)
	
	elif itemType == "LIST": 
		return parseListError(item)
	
	elif itemType == "ARRAY": 
		return parseArray(item)
	
	else:
		node = Node(itemType)
		node.setError("INTERNAL: invalid item type: " + itemType)
		return node
		

def parseAtom(item):
		
	node = Node("ATOM")
	node.setParsedValue(item[1])
	
	return node
		
		
def parseExpr(item):
		
	expType = item[2]
	expMemberList = item[3]

	node = Node("EXPR")
	node.setParsedValue(expType)	

	for memberItem in expMemberList: 
		subNode = parse(memberItem)
		node.addChild(subNode)	
	
	return node

	
def parseListError(item):
		
	node = Node()
	subType = item[1]
	
	if subType == "naked":			 
		node.setError("FATAL: value list outside array: " + items2str(item))
	
	elif subType == "num":
		node.setError("FATAL: standalone value array: [" + items2str(item[2][0]) + "]")

	elif subType == "str":
		node.setError("FATAL: standalone value string: \"" + item[2][0] + "\"")

	elif subType == "array":
		node.setError("FATAL: string in array: \"" + item[2][2][0] + "\"")
		
	else:
		node.setError("INTERNAL: item LIST, subtype: " + subType)
		
	return node
	

def parseArray(item):
	
	subType = item[1][0][1]
	if subType == "num":
		values = "[" + items2str( item[1][0][2][0] ) + "]"
	else: 
		values = "\"" + item[1][0][2][0] + "\""
	index = item[1][1]
	
	node = Node("DATA")
	node.setParsedValue(values)

	subNode = parse(index)
	node.addChild(subNode)
	
	return node
	
