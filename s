#!/bin/bash

clear
python3 -B app/forcom.py song/a.txt
rm -f parser.out
rm -fr app/__pycache__
