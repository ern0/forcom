#!/bin/bash
clear

#python3 -B app/forcom.py song/test.txt lex ; echo --
#python3 -B app/forcom.py song/test.txt pseudo ; exit
python3 -B app/forcom.py song/test.txt graph ; exit
#python3 -B app/forcom.py song/test.txt unopt ; exit

#python3 -B app/forcom.py song/single.txt unopt > simple.asm
cat simple.asm
fasm simple.asm
rm -f simple.bin

rm -f parser.out
rm -fr app/__pycache__
