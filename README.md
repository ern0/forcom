# forcom - Formula Compiler

## What is it

It's a strange compiler:
- purpose: bytebeat
- target platform: 16-bit instructions for modern x86 processors
- output: Assembly source (Fasm preferred)
- ABI: TomCat's engine

## Current state

Currently only unoptimized code generator is available. It generates very primitive, slow code from the AST.

The t (sample counter, aka. time) is 32-bit wide, and it's stored in BX:SI. Only SI is used for calculation, except:
- if left operand of div is t (e.g. t / 122),
- if left operand of right shift is t (e.g. t >> 4).
In these cases the operator will be converted to
DIV and BX:SI will be used.

All AST node intermedite result is stored in temporary memory.
Calculation size is 16-bit.

The result of the formula is AX.

## TODO 

### Tree Optimizer

- eliminate unary plus in tree

### Unoptimized Renderer

- shr: if arg1 is t -> div32 bx:si
- div: if arg2 is t -> div32 bx:si
- implement ternary
