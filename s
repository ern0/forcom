#!/bin/bash

clear
python3 -B app/forcom.py song/test.txt graph
rm -f parser.out
rm -fr app/__pycache__
