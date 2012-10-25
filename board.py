# encoding=UTF8

import matrix
import random
import copy
import code

class Board(object):

	#el inito
	def __init__(self, columns, rows, colors, state = None):
		self.rows = rows
		self.columns = columns
		self.colors = colors
		
		#used in tree calculation
		self.move = None 
		self.count = None
		
		self.refillboard = None
		
		if (state is None):
			self.state = matrix.Matrix(self.rows, self.columns, self.colors)
		else:
			self.state = matrix.Matrix.CopyMatrix(state.matrix)
			#self.state = copy.deepcopy(state)
	
	@staticmethod
	def LoadBoard(filename):
		val = []
		data = open(filename, "r")
		for line in data.readlines():
			treated = line.strip().split(",")
			numbers = map(int, treated)
			val.append(numbers)


		columns = len(val[0])
		rows = len(val)
		colours = max(map(max, val))

		m = matrix.Matrix(rows, columns)
		for i in range(rows):
			for j in range(columns):
				m.matrix[j][i] = val[i][j]
		
		return Board(columns, rows, colours, m)	
		
	@staticmethod
	def LoadRefill(filename):
		val = []
		data = open(filename, "r")
		for line in data.readlines():
			treated = line.strip().split(",")
			numbers = map(int, treated)
			val.append(numbers)


		columns = len(val[0])
		rows = len(val)
		colours = max(map(max, val))

		m = matrix.Matrix(rows, columns)
		for i in range(rows):
			for j in range(columns):
				m.matrix[j][i] = val[i][j]
		
		return m
		
	#sanitizes a board, removing all ready to explode patterns by exploding and refilling them
	#until it is 'sane', and safe to use at the beginning of the game.
	def sanitize(self, verbose=True):
		if verbose:
			print "Sanitizing board..."
		
		def testrefill(refill):
			for i in range(0, self.columns):
				for j in range(0, self.rows):
					if (refill[0].getitem(i, j) > 0):
						return False
			return True					
		
		
		#WARNING: the snippet below does not correctly simmulate the game's logic
		donesanitizing = False
		while not donesanitizing:
			donegravity = False
			while not donegravity:
				self.explode()
				donegravity = self.gravity()
				
			donesanitizing = testrefill(self.refill())
		
		if verbose:
			print "Done sanitizing."
	
		
	#returns a matrix of marked patterns
	#when the same color is three or more times in a row	
	def getpatterns(self):
		marked = matrix.Matrix(self.rows, self.columns)
				
		#mark columns
		for i in range(0, self.columns):	#iterate thru rows
			for j in range(0, self.rows):	#iterate thru columns
				if (j - 1 >= 0) and (j + 1 <= self.rows - 1):
					if (self.state.getitem(i,j) != 0):
						if (self.state.getitem(i,j) == self.state.getitem(i,j + 1)):
							if (self.state.getitem(i,j) == self.state.getitem(i,j - 1)):
								color = self.state.getitem(i,j)
								marked.setitem(i, j    , color)
								marked.setitem(i, j + 1, color)	
								marked.setitem(i, j - 1, color)		
		
		#mark rows
		for i in range(0, self.columns):	#iterate thru rows
			for j in range(0, self.rows):	#iterate thru columns
				if (i - 1 >= 0) and (i + 1 <= self.columns - 1):
					if (self.state.getitem(i,j) != 0):
						if (self.state.getitem(i,j) == self.state.getitem(i + 1, j)):
							if (self.state.getitem(i,j) == self.state.getitem(i - 1,j)):
								color = self.state.getitem(i,j)
								marked.setitem(i, j   , color)
								marked.setitem(i + 1, j, color)	
								marked.setitem(i - 1, j, color)		
		
		return marked


						
	#simulate gravity (returns True when there's nothing left to fall)
	#must be called several times until it returns True.
#	def gravity_sideways(self):	
#		def shiftcolumn(column, row):
#			for i in range(row, self.rows - 1):
#				self.state.setitem(column, i, self.state.getitem(column, i + 1))
#			self.state.setitem(column, self.rows - 1, 0)

#		for i in range(0, self.columns):
#			for j in range(0, self.rows):
#				if (j+1 <= self.rows - 1):
#					if (self.state.getitem(i, j) == 0) and (self.state.getitem(i, j + 1) != 0):
#						shiftcolumn(i, j)
#						return False
#		return True
			
	#simulate gravity (returns True when there's nothing left to fall)
	#must be called several times until it returns True.

	def gravity(self):
	
		realrows = self.columns
		realcolumns = self.rows
			
		def shiftcolumn(row, column):
			for i in range(row, realrows - 1):
				self.state.matrix[i][column] = self.state.matrix[i+1][column]
			self.state.matrix[realrows - 1][column] = 0
		

		
		for i in range(0, realrows):
			for j in range(0, realcolumns):
				if (i + 1 < realrows):
					#print "(%s < %s) (%s < %s)" % (i+1, realrows, j, realcolumns)
					#print len(self.state.matrix), "==", realrows
					#print len(self.state.matrix[i+1]), "==", realcolumns
					if (self.state.matrix[i][j] == 0) and (self.state.matrix[i+1][j] != 0):
						shiftcolumn(i, j)
						return False
		return True		

	#removes all patterned pieces, returning a tuple with all patterns and their count				
	def explode(self):	
		patterns = self.getpatterns()
		count = 0
		for i in range(0, self.columns):
			for j in range(0, self.rows):
				if (patterns.getitem(i, j) > 0):
					self.state.setitem(i, j, 0)
					count += 1
		return (patterns, count)
	
	
	

	#refills a board with gaps
	def refill(self):
		count = 0
		newcolors = matrix.Matrix(self.rows, self.columns)
		for i in range(0, self.columns):	#iterate thru rows
			for j in range(0, self.rows):	#iterate thru columns
				if (self.state.getitem(i, j) == 0):
					count += 1
					
					if self.refillboard is None:
						newcolor = random.choice(range(1, self.colors+1))
					else:
						newcolor = self.refillboard.matrix[i][j]
						
					newcolors.setitem(i, j, newcolor)
					self.state.setitem(i, j, newcolor)
					
		return (newcolors, count)




	#tries to make a move. returns True if it applies, False if it doesn't	
	def play(self, move):
		if (self.validate(move)):
			self.applymove(move)
			return True
		else:
			return False

	#manipulates the board directly.
	#should be inside matrix class but whatever
	def applymove(self, move):
		piece_a = move[0]
		piece_b = move[1]
		
		temp = self.state.getitem(piece_a[0], piece_a[1])
		self.state.setitem(piece_a[0], piece_a[1], self.state.getitem(piece_b[0], piece_b[1]))
		self.state.setitem(piece_b[0], piece_b[1], temp)

	
	#given a board and a move, validate it. apply move, storing in the board object
	#	- the move
	#	- the score caused
	def moveandnewboard(self, move):
		#print move
		#print self.rows, self.columns
		#raw_input()
		board = Board(self.columns, self.rows, self.colors, self.state)
		if (board.play(move)):
			count = 0
			score = 0
			chain = -1
			donechaining = False #FAIL
			while not donechaining:
				(patterns, exploded) = board.explode()
				while not board.gravity():
					pass
				
				if (exploded == 0):
					donechaining = True
				else:
					chain +=1
					count += exploded
					score += exploded * 100 * (2 ** chain)

				
			board.move = move
			board.score = score
			board.count = count
			return board
		else:
			return None

	def hasones(self, patterns):
		for i in range(0, self.columns):
			for j in range(0, self.rows):
				if (patterns.getitem(i, j) > 0):
					return True
		return False
	
	#validates a move. returns True/False
	def validate(self, move):
		newboard = Board(self.columns, self.rows, self.colors, self.state)
		newboard.applymove(move)
		patterns = newboard.getpatterns()
		return self.hasones(patterns)
		

				
