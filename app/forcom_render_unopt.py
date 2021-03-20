from collections import OrderedDict
import forcom_ast as ast


class UnoptimizedRenderer:

	def proc(self, node):

		subNodes = node.getChildren()
		for subNode in subNodes:
			numero = subNode.getNumero()
			subNode.dumpFlat()


	def dump(self):
		print("TODO")