@echo off
cls
echo off
python -B app/forcom.py song/a.txt
erase __pycache__ /s /q 2> nul
rmdir __pycache__ /q 2> nul
erase app\parser.out 2> nul
erase app\parsetab.py 2> nul
