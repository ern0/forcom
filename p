#!/bin/bash
clear

#python3 -B app/forcom.py song/test.txt graph

python3 -B app/forcom.py song/single.txt unopt > simple.asm
cat simple.asm
fasm simple.asm
rm -f simple.bin

rm -f parser.out
rm -fr app/__pycache__
