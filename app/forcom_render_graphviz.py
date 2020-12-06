#!/usr/bin/env python3 -B

try: import graphviz
except: quit("FATAL: install module graphviz")
import forcom_ast as ast


class GraphvizRenderer:


	def proc(self, node):

		self.root = node

		formula = self.root.getFormula() 
		self.dot = graphviz.Digraph(comment = formula)
		self.id = 0

		self.renderNode(None, self.root)


	def renderNode(self, parentNode, node):
		
		nodeType = node.getType()
		if nodeType == "DATA": return

		self.id += 1
		name = "node_" + str(self.id)
		node.setName(name)

		self.dot.node(name, nodeType)
		if parentNode is not None:
			self.dot.edge(name, parentNode.getName())

		for subNode in node.getChildren():
			self.renderNode(node, subNode)


	def dump(self):
		self.dot.render(view=True)

