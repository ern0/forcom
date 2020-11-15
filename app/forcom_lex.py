#!/usr/bin/env python3 -B

import sys
try: import ply.lex as lex
except: quit("FATAL: install module ply")


tokens = (
	"ATOM_TEE", "ATOM_INT", "ATOM_FLOAT",
	"ATOM_PL_HEX_C", "ATOM_PL_HEX_I", "ATOM_PL_HEX_M",
	"ATOM_MI_HEX_C", "ATOM_MI_HEX_I", "ATOM_MI_HEX_M",
	"ATOM_QUOTED",
	"ATOM_QUOTED_SINGLE", "ATOM_QUOTED_DOUBLE",
	"OP_PLUS", "OP_MINUS", "OP_MUL", "OP_DIV", "OP_MOD",
	"OP_SHL", "OP_SHR",
	"OP_OR", "OP_AND", "OP_XOR", "OP_NOT",
	"OP_EQ", "OP_NE", "OP_LT", "OP_LE", "OP_GT", "OP_GE",
	"BRACE_ROUND_OPEN", "BRACE_ROUND_CLOSE",
	"BRACE_SQUARE_OPEN", "BRACE_SQUARE_CLOSE",
	"SEP_QUESTION", "SEP_COLON", "SEP_COMMA"
)

t_ignore_SPACE = r"\ "
t_ignore_TAB = r"\t"
t_ignore_CR = r"\r"
t_ignore_LF = r"\n"
t_ignore_COMMENT_BETWEEN = r'\/\*.*\*\/'
t_ignore_COMMENT_LINE = r'\/\/.*$'

t_ATOM_TEE = r"t"
t_OP_PLUS = r"\+"
t_OP_MINUS = r"\-"
t_OP_MUL = r"\*"
t_OP_DIV = r"\/"
t_OP_MOD = r"\%"
t_OP_SHL = r"\<\<"
t_OP_SHR = r"\>\>"
t_OP_OR = r"\|"
t_OP_AND = r"\&"
t_OP_XOR = r"\^"
t_OP_NOT = r"\~"
t_OP_EQ = r"\=\="
t_OP_NE = r"\<\>|\!\="
t_OP_LT = r"\<"
t_OP_LE = r"\<\="
t_OP_GT = r"\>"
t_OP_GE = r"\>\="
t_BRACE_ROUND_OPEN = r"\("
t_BRACE_ROUND_CLOSE = r"\)"
t_BRACE_SQUARE_OPEN = r"\["
t_BRACE_SQUARE_CLOSE = r"\]"
t_SEP_QUESTION = r"\?"
t_SEP_COLON = r"\:"
t_SEP_COMMA = r"\,"


def t_error(token): pass


def t_ATOM_QUOTED(token):
	r"nope^" 


def t_ATOM_QUOTED_SINGLE(token):
	r"'(.*?)'"
	
	token.type = "ATOM_QUOTED"
	token.value = token.value[1:-1]
	return token


def t_ATOM_QUOTED_DOUBLE(token):
	r'"(.*?)"'

	token.type = "ATOM_QUOTED"
	token.value = token.value[1:-1]
	return token


def t_ATOM_PL_HEX_C(token): 
	r"0[xX][0-9a-fA-F]+"
	
	token.type = "ATOM_INT"
	token.value = int( str(token.value), 0)
	return token


def t_ATOM_PL_HEX_I(token): 
	r"[0-9][0-9a-fA-F]+[hH]"		
	
	token.type = "ATOM_INT"
	token.value = int( str(token.value[:-1]), 16)
	return token
	

def t_ATOM_PL_HEX_M(token): 
	r"\$[0-9a-fA-F]+"
	
	token.type = "ATOM_INT"
	token.value = int( str(token.value[1:]), 16)
	return token
	

def t_ATOM_MI_HEX_C(token): 
	r"\-0[xX][0-9a-fA-F]+"
	
	token.type = "ATOM_INT"
	token.value = -1 * int( str(token.value[1:]), 0)
	return token


def t_ATOM_MI_HEX_I(token): 
	r"\-[0-9][0-9a-fA-F]+[hH]"		
	
	token.type = "ATOM_INT"
	token.value = -1 * int( str(token.value[1:-1]), 16)
	return token
	

def t_ATOM_MI_HEX_M(token): 
	r"\-\$[0-9a-fA-F]+"
	
	token.type = "ATOM_INT"
	token.value = -1 * int( str(token.value[2:]), 16)
	return token


def t_ATOM_FLOAT(token):
	r"[0-9]+[\.][0-9]+"
	return token


def t_ATOM_INT(token):
	r"[0-9]+[0-9]?"
	return token


def build(text):
	lexer = lex.lex()
	lex.input(text)
	
	return lexer
	

def proc(text):

	try:
		lexer = build(text)

		while True:
			token = lex.token()
			if not token: break
			print("  " + token.type + ": " + str(token.value))
			# also: token.lineno, token.lexpos

	except lex.LexError as e:
		print("error: " + e.args[0] + " - " + e.text)
		return None

