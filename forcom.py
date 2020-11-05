#!/usr/bin/env python3 -B

import forcom_lex as lex


def main():
	lex.performLex("t + 21")
	lex.performLex("t << 3 + t ^ 0x40")
	lex.performLex("\"sd d dfdsd\" & 'sd sds s& '")


if __name__ == "__main__": main()
