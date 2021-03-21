; t * 2

	ORG 100H

	MOV BX,5

	MOV AX,BX
	MOV CX,2
	MUL CX
	MOV [var2],AX

	INT3
	RET

var2:	DW 0
