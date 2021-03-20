#!/bin/bash
clear

#python3 -B app/forcom.py song/test.txt graph
python3 -B app/forcom.py song/single.txt unopt

rm -f parser.out
rm -fr app/__pycache__
