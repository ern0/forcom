#!/bin/bash
clear

#python3 -B app/forcom.py song/test.txt lex ; echo --
#python3 -B app/forcom.py song/test.txt pseudo ; exit
#python3 -B app/forcom.py song/test.txt graph ; exit
python3 -B app/forcom.py song/test.txt rpn ; exit

python3 -B app/forcom.py song/simple.txt unopt > simple.asm
cat simple.asm
fasm simple.asm
rm -f simple.bin

rm -f parser.out
rm -fr app/__pycache__
