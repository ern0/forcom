try: import graphviz
except: quit("FATAL: install module graphviz")
import forcom_ast as ast


class GraphvizRenderer:


	def proc(self, node):

		self.root = node

		formula = self.root.getFormula().replace('"',"&quot;")
		self.dot = graphviz.Digraph(
			comment = formula
			,body = { 
				"\trankdir=\"BT\";"
				,"\tlabel=\"" + formula + "\";"
				,"\tlabelloc=top;"
    		,"\tlabeljust=left;"

			}
		)

		self.renderNode(None, self.root)


	def renderNode(self, parentNode, node):
		
		nodeType = node.getType()
		#if nodeType == "DATA": return

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
		if title == "EXPR" or title == "DATA": 
			title += " #" + str(node.getNumero())
		title += ": "
		title += str(node.getValue())

		return title


	def dump(self):
		
		print(self.dot.source)

		self.dot.render(
			view = True
			,cleanup = True
			,format = "png"
			,filename = "ast"
		)

