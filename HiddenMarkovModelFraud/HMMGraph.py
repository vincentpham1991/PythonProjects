from pylab import *
import networkx as nx
from PIL import Image


def graphA(A):
	'''
	Graphs the transition matrix

	Parameters
	----------
	A: transition matrix

	Returns
	--------
	none
	'''
	a11, a12, a21, a22 = round(A[0][0], 3), round(A[0][1], 3), round(A[1][0], 3), round(A[1][1], 3)

	title("Transition Matrix")

	gca().get_xaxis().set_visible(False) # Removes x-axis from current figure
	gca().get_yaxis().set_visible(False) # Removes y-axis from current figure

	cir1 = Circle((0.25,0.5), radius=0.1, alpha = 0.8,  fc='r', label = 'state 1')
	cir2 = Circle((0.75,0.5), radius=0.1, alpha = 0.8, fc='b')

	arrow11 = Arrow(0.4, 0.55, 0.2, 0., width = 0.01)
	arrow12 = Arrow(0.6, 0.45, -0.2, 0, width = 0.01)

	text(0.45, 0.555, a12)
	text(0.45, 0.455, a21)

	text(0.2, 0.5, 's1')
	text(0.7, 0.5, 's2')

	text(0.03, 0.5, a11)
	text(0.92, 0.5, a22)

	gca().add_patch(cir1)
	gca().add_patch(cir2)
	gca().add_patch(arrow11)
	gca().add_patch(arrow12)

	annotate("",
            xy=(0.15, 0.55), xycoords='data',
            xytext=(0.1, 0.5), textcoords='data',
            arrowprops=dict(arrowstyle="-",
                            connectionstyle="angle3"),
            )


	annotate("",
            xy=(0.15, 0.45), xycoords='data',
            xytext=(0.1, 0.5), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="angle3"),
            )

	annotate("",
            xy=(0.85, 0.55), xycoords='data',
            xytext=(0.9, 0.5), textcoords='data',
            arrowprops=dict(arrowstyle="-",
                            connectionstyle="angle3"),
            )


	annotate("",
            xy=(0.85, 0.45), xycoords='data',
            xytext=(0.9, 0.5), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="angle3"),
            )
	savefig("./graphs/graphA")
	clf()
	return

def graphB(B):
	'''
	Graphs the emission matrix

	Parameters
	----------
	B: transition matrix

	Returns
	--------
	none
	'''
	G=nx.Graph()

	title("Emission Matrix B")

	x, y, w, z, v, r = round(B[0][0], 2), round(B[0][1], 2), round(B[0][2], 2), round(B[1][0], 2), round(B[1][1], 2), round(B[1][2], 2)
	a="s1"
	b="s2"
	c="l"
	d="m"
	e="h"
	f="l'"
	g="m'"
	h="h'"
	G.add_edge(a, c, len = 2)
	G.add_edge(a, d, len = 2)
	G.add_edge(a, e, len = 2)
	G.add_edge(b, f, len = 2)
	G.add_edge(b, g, len = 2)
	G.add_edge(b, h, len = 2)

	pos=nx.spring_layout(G) # positions for all nodes

	# nodes
	nx.draw_networkx_nodes(G,pos,node_size=300, node_color="red")

	# edges
	nx.draw_networkx_edges(G,pos,
	        width=1,alpha=1,edge_color='black')

	# labels
	nx.draw_networkx_labels(G,pos,font_size=12,font_family='Courier New')

	labels = {(a,c):x, (a,d):y, (a,e):w, (b,f):z, (b,g):v, (b,h):r}

	nx.draw_networkx_edge_labels(G,pos, labels)

	axis('off')
	savefig("./graphs/graphB")
	clf()
	return

def drawGraphs(A,B):
	graphA(A)
	graphB(B)
	return



