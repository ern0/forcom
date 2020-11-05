#!/usr/bin/env python3 -B

import sys
try: import ply.lex as lex
except: quit("FATAL: install module ply")


tokens = (
	"ATOM_T",
	"ATOM_N_DEC", "ATOM_N_HEX_C", "ATOM_N_HEX_I", "ATOM_N_HEX_M",
	"OP_PLUS", "OP_MINUS", "OP_MUL", "OP_DIV", "OP_MOD",
	"OP_SHL", "OP_SHR",
	"OP_OR", "OP_AND", "OP_XOR", "OP_NOT"
)

t_ignore_SPACE = r"\ "
t_ignore_TAB = r"\t"
t_ignore_CR = r"\r"
t_ignore_LF = r"\n"

t_ATOM_T = r"t"
t_ATOM_N_DEC = r"\d+"
t_ATOM_N_HEX_C = r"0[xX][0-9a-fA-F]+"
t_ATOM_N_HEX_I = r"[0-9][0-9a-fA-F]+[hH]"
t_ATOM_N_HEX_M = r"\$[0-9a-fA-F]+"
t_OP_PLUS = r"\+"
t_OP_MINUS = r"\-"
t_OP_MUL = r"\*"
t_OP_DIV = r"\/"
t_OP_MOD = r"\%"
t_OP_SHL = r"\<<"
t_OP_SHR = r"\>>"
t_OP_OR = r"\|"
t_OP_AND = r"\&"
t_OP_XOR = r"\^"
t_OP_NOT = r"\~"

def t_error(t):	pass


def performLex(text):

	print("LEX: \"" + text + "\"")

	try:
		lex.lex()
		lex.input(text)

		while True:
			token = lex.token()
			if not token: break
			print("  " + token.type + ": " + token.value) #, token.lineno, token.lexpos)

	except lex.LexError as e:
		print("error: " + e.args[0] + " - " + e.text)
		quit()


def main():
	performLex("t + 21")
	performLex("t << 3 + t ^ 0x40")


if __name__ == "__main__": main()
