#!/usr/bin/env python3 -B

import forcom_lex as lex
import forcom_yacc as yacc
import logging
logging.disable(logging.CRITICAL)
logging.disable(logging.NOTSET)


def main():

	if False:
		yacc.proc(" (t << (4 + 2) * 8 < 2 ? t : t/2) ")

	if True:
		yacc.proc(" [3,4,8,1][t & 3] + 'XYZX'[t & 3]")
		yacc.proc(" ( t % 2 ? 255 : t / 2 ) ")

	if False:
		yacc.proc(" 3-2 ")
		yacc.proc(" 3--2 ")
		yacc.proc(" 3+-2 ")
		yacc.proc(" 3++2 ")

	if False:
		lex.proc(' "1234"[t] ')
		lex.proc("(t<<3)*[8/9,1,9/8,6/5,4/3,3/2,0][[0xd2d2c8,0xce4088,0xca32c8,0x8e4009][t>>14&3]>>(0x3dbe4688>>((t>>10&15)>9?18:t>>10&15)*3&7)*3&7]")
		lex.proc("(t/4|t+3&t|t<<5&t+t-7%t12|t%9>>13|t(t%21)/13&t+(t/15))&t>>7")
		lex.proc("t/5|t*2&t/20>>1|45*t*-t/666|t/12|t/666>>2")
		lex.proc("0x41 $41 041H")
		lex.proc("t + 21")
		lex.proc("t << 3 + t ^ 0x40")
		lex.proc("\"sd d dfdsd\" & 'sd sds s& '")

if __name__ == "__main__": main()
