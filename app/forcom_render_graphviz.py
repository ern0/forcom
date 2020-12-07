#!/usr/bin/env python3 -B

try: import graphviz
except: quit("FATAL: install module graphviz")
import forcom_ast as ast


class GraphvizRenderer:


	def proc(self, node):

		self.root = node

		formula = self.root.getFormula() 
		self.dot = graphviz.Digraph(
			comment = formula
			,body = { 
				"\trankdir=\"BT\";"
				,"\tlabel=\"" + formula + "\";"
				,"\tlabelloc=top;"
    		,"\tlabeljust=left;"

			}
		)
		self.numero = 0

		self.renderNode(None, self.root)


	def renderNode(self, parentNode, node):
		
		nodeType = node.getType()
		if nodeType == "DATA": return

		self.numero += 1
		node.setNumero(self.numero)

		nodeId = self.mkId(node)
		self.dot.node(nodeId, self.mkTitle(node))

		if parentNode is not None:
			self.dot.edge(nodeId, self.mkId(parentNode)) 

		for subNode in node.getChildren():
			self.renderNode(node, subNode)


	def mkId(self, node):
		return "node_" + str(node.getNumero())

	def mkTitle(self, node):

		title = node.getType()
		title += ": "
		title += str(node.getValue())

		return title

	def dump(self):
		self.dot.render(
			view = True
			,cleanup = True
			,format = "png"
			,filename = "ast"
		)

