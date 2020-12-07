#!/usr/bin/env python3 -B

import forcom_ast as ast


class AsmRenderer:


	def proc(self, node):

		self.root = node



	def dump(self):
		print(self.root.getFormula())
		print("--")
		print("TODO")