#!/bin/bash
clear

#python3 -B app/forcom.py song/test.txt graph

python3 -B app/forcom.py song/single.txt unopt > single.asm
cat single.asm
fasm single.asm
rm -f single.bin

rm -f parser.out
rm -fr app/__pycache__
