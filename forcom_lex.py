#!/usr/bin/env python3 -B

import sys
try: import ply.lex as lex
except: quit("FATAL: install module ply")


tokens = (
	"ATOM_T", "ATOM_N",
	"ATOM_N_DEC", "ATOM_N_HEX_C", "ATOM_N_HEX_I", "ATOM_N_HEX_M",
	"ATOM_QUOTED_SINGLE", "ATOM_QUOTED_DOUBLE",
	"OP_PLUS", "OP_MINUS", "OP_MUL", "OP_DIV", "OP_MOD",
	"OP_SHL", "OP_SHR",
	"OP_OR", "OP_AND", "OP_XOR", "OP_NOT",
	"OP_EQ", "OP_NE_1", "OP_NE_2", "OP_LT", "OP_LE", "OP_GT", "OP_GE",
	"BRACE_ROUND_OPEN", "BRACE_ROUND_CLOSE",
	"BRACE_SQUARE_OPEN", "BRACE_SQUARE_CLOSE"
)

t_ignore_SPACE = r"\ "
t_ignore_TAB = r"\t"
t_ignore_CR = r"\r"
t_ignore_LF = r"\n"

t_ATOM_T = r"t"
t_ATOM_QUOTED_SINGLE = r"'(.*?)'"
t_ATOM_QUOTED_DOUBLE = r'"(.*?)"'
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
t_OP_EQ = r"\="
t_OP_NE_1 = r"\<\>"
t_OP_NE_2 = r"\!\="
t_OP_LT = r"\<"
t_OP_LE = r"\<\="
t_OP_GT = r"\>"
t_OP_GE = r"\>\="

def t_error(token): pass

def t_ATOM_N(token):
	r"nope^" 


def t_ATOM_N_HEX_C(token): 
	r"0[xX][0-9a-fA-F]+"
	
	token.type = "ATOM_N"
	token.value = int( str(token.value), 0)
	return token


def t_ATOM_N_HEX_I(token): 
	r"[0-9][0-9a-fA-F]+[hH]"		
	
	token.type = "ATOM_N"
	token.value = int( str(token.value[:-1]), 16)
	return token
	

def t_ATOM_N_HEX_M(token): 
	r"\$[0-9a-fA-F]+"
	
	token.type = "ATOM_N"
	token.value = int( str(token.value[1:]), 16)
	return token
	

def t_ATOM_N_DEC(token):
	r"\d+"
	return token
		

def performLex(text):

	print("LEX: \"" + text + "\"")

	try:
		lex.lex()
		lex.input(text)

		while True:
			token = lex.token()
			if not token: break
			print("  " + token.type + ": " + str(token.value))
			# also: token.lineno, token.lexpos

	except lex.LexError as e:
		print("error: " + e.args[0] + " - " + e.text)
		quit()

