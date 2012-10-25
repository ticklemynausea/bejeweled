import random
from termcolor import colored
import code

class Matrix(object):
	__slots__ = ['cols', 'rows', 'matrix']
	cmap = {1:'red', 2:'blue', 3:'green', 4:'yellow', 5:'cyan', 6:'magenta', 7:'white'}	
	bmap = {1:'on_red', 2:'on_blue', 3:'on_green', 4:'on_yellow', 5:'on_cyan', 6:'on_magenta', 7:'on_white'}

	@staticmethod
	def CopyMatrix(matrix):
		cols = len(matrix[0])
		rows = len(matrix)
		m = Matrix(cols, rows)
				
		for i in range(rows):
			for j in range(cols):
				m.matrix[i][j] = matrix[i][j]
		
		return m
		
	def __init__(self, cols, rows, colors = None):
		self.cols = cols
		self.rows = rows
		self.matrix = [[0] * cols for _ in range(0, rows)]
		
		if colors is not None:
			for i in range(rows):
				for j in range(cols):
					self.matrix[i][j] = random.choice(range(1, colors+1))


	def setitem(self, col, row, v):
		self.matrix[col][row] = v
 
 
 	
	def getitem(self, col, row):
		return self.matrix[col][row]

 		
 
	def __repr__(self):
#		def linerepr(line):
#			outStr = ""
#			for i in line:
#				if (i == 0):
#					outStr += "  "
#				else:
#					outStr += colored("%s " % i, self.cmap[i], self.bmap[i])
#			return "[%s]" % outStr
#				
#		outStr = ""
#		
#		for i in range(self.rows):
#		    outStr += '%s\n' % (linerepr(self.matrix[i]))

		outStr = ""
		for i in range(self.rows-1, -1, -1):
			outStr += "%s [" % i
			l = len(self.matrix[i])
			for j in range(l):
				c = self.matrix[i][j]
				if c == 0:
					outStr += "  "
				else:
					outStr += colored("%s " % c, self.cmap[c], self.bmap[c])
					
			outStr += "]\n"
		outStr += "   "
		for i in range(0, self.cols):
			outStr += "%s " % i
		outStr += "\n"
		return outStr
		
	def markrepr(self, moves):
					
		markers = [[0] * self.cols for _ in range(0, self.rows)]
		
		for move in moves:
			coord_x1 = move[1]
			coord_y1 = move[0]
			
			markers[coord_y1][coord_x1] = 1
			
		outStr = ""
		for i in range(self.rows-1, -1, -1):
			outStr += "%s [" % i
			l = len(self.matrix[i])
			for j in range(l):
				c = self.matrix[i][j]
				if markers[i][j] == 1:
					if c == 0:
						outStr += "!!"
					else:
						outStr += colored("!!", 'white', self.bmap[c], ['bold'])					
				else:
					if c == 0:
						outStr += "  "
					else:
						outStr += colored("%s " % c, self.cmap[c], self.bmap[c])
			outStr += "]\n"
			
		outStr += "   "
		for i in range(0, self.cols):
			outStr += "%s " % i
		outStr += "\n"
		
		return outStr
		
		
			
