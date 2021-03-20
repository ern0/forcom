#!/usr/bin/env python3 -B

from collections import OrderedDict
import forcom_ast as ast


class Entry:

	pass


class AsmRenderer:

	def proc(self, node):

		self.entryDict = OrderedDict()
		self.createEntry(node)



	def dump(self):
		print("TODO")