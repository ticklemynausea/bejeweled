# coding=UTF8

import board
import player
import sys



class Logic(object):

		
	def __init__(self, *args, **kwargs):
		def getplayer(name):
			playeroptions = {
					 'BestScore':
						player.BestScore(self.moves, self.depth),
					 'BestEnergy':
						player.BestEnergy(self.moves, self.depth),
					 'BestScoreBetterEnergy':
						player.BestScoreBetterEnergy(self.moves, self.depth, self.minenergy),					
					 'EnergyVSEntropy':
					 	player.EnergyVSEntropy(self.moves, self.depth, self.energythreshold),
					 'EnergyVSEntropyReversed':
					 	player.EnergyVSEntropyReversed(self.moves, self.depth, self.energythreshold),					 	
					 'GreedyEnergyVSEntropy':
					 	player.GreedyEnergyVSEntropy(self.moves, self.energythreshold)					 	
						}
			return  playeroptions[name]		
			
		def getlistofmoves(rows, columns):
			moves = []
			#horizontals
			for i_a in range(0, rows):
				for j_a in range(0, columns-1):
					moves.append(((i_a, j_a), (i_a, j_a+1)))
			#verticals
			for i_a in range(0, rows-1):
				for j_a in range(0, columns):
					moves.append(((i_a, j_a), (i_a+1, j_a)))	

			#print "For this %sx%s board, there are a total of %s possible moves " % (rows, columns, len(moves))
			return moves	
		
		self.pauses = kwargs.get('pause', False)
		self.shorten = kwargs.get('shorten', False)
		boardfile = kwargs.get('boardfile', None)
		refillfile = kwargs.get('refillfile', None)		
		self.limit = kwargs.get('limit')
		self.depth = kwargs.get('depth')
		self.minenergy = kwargs.get('minenergy', 2)
		self.energythreshold = kwargs.get('energythreshold')
		if boardfile is None:
			columns = kwargs.get('columns')
			rows = kwargs.get('rows')
			colours = kwargs.get('colours')
			self.moves = getlistofmoves(columns, rows)
			self.board = board.Board(columns, rows, colours)

							 		
			self.player	= getplayer(kwargs.get('player'))	
			
			print "**************************************"
			print "* Welcome to AI Bejeweled"
			print "* Rules:"			
			print "*\t%sx%sx%s (%s possible moves)" % (columns, rows, colours, len(self.moves))
			print "*\tUsing IA Agent %s " % self.player
			print "*\tWill terminate after %s moves" % (self.limit)
			print "**************************************"	
			
			self.board.sanitize()

		else:
			try:
				self.board = board.Board.LoadBoard(boardfile)
				self.board.refillboard = board.Board.LoadRefill(refillfile)
			except Exception as e:
				print "Error: ", e
				sys.exit(0)
			
			self.moves = getlistofmoves(self.board.rows, self.board.columns)
			self.player	= getplayer(kwargs.get('player'))		
				
			print "**************************************"
			print "* Welcome to AI Bejeweled"
			print "* Rules:"		
			print "*\tUsing board from %s and refill from %s " % (boardfile, refillfile)
			print "*\t%sx%sx%s (%s possible moves)" % (self.board.columns, self.board.rows, self.board.colors, len(self.moves))
			print "*\tUsing IA Agent %s " % self.player
			print "*\tWill terminate after %s moves" % (self.limit)			
			print "**************************************"								


		
	# método play implementa a logica de jogo como uma máquina de estados.
	# os sub métodos são o código implementado por cada estado
	# o resto do código trata das transições entre estados
	# e passagem de argumentos
	
	def play(self):
		def begin_iteration():
			print "***********************"
			print "* begin iteration ", self.iteration
			print "***********************"
			print self.board.state
				
		def state_move():
			move = self.player.getmove(self.board)

			if (move == None):
				return True
			else:	
			
				result = self.board.play(move)

				print "Move selected: ", move
				if result is False:
						print "Player asked me to perform an invalid move."
						print "Probably he is a path follower. Please ignore this."
				else:
					print self.board.state.markrepr(list(move))

				return False

		def state_explode():
			### EXPLODE ###
			(patterns, exploded) = self.board.explode()
			if (exploded != 0):
				if not self.shorten:
					print "Patterns:"
					print patterns
					print "Board state: before gravity"
					print self.board.state

			return exploded
				
		def state_gravity():		
			#GRAVITY
			gravities = 0
			while not self.board.gravity():
				gravities += 1
			if (gravities > 0):
				if not self.shorten:
					print "Board state: after gravity"
					print self.board.state
		
		def state_refill():	
			(refill,_) = self.board.refill()
			if not self.shorten:
				print "Refill:"
				print refill
				print "Refilled:"
				print self.board.state
			
		self.iteration = 1
		count = 0
		chain = 0
		totalcount = 0
		totalchain = 0
		score = 0
		#STATES
		BEGIN, MOVE, EXPLODE, GRAVITY, REFILL, TERMINATE_FORCIBLY = range(6)
		
		while self.iteration <= self.limit:	
			begin_iteration()
			
			self.state = MOVE
			while self.state != BEGIN:
				if (self.state == MOVE):		
					#chain starts at -1 because the first time pieces explode, points should be multiplied by 2^0.
					#if 
					chain = -1
					score = 0
					jewels = []
					result = state_move()
					if result:
						print "Terminal state achieved in iteration %s.\nScore: %s: " % (self.iteration, self.player.score)
						print self.board.state			
						self.state = TERMINATE_FORCIBLY	
						break

					self.state = EXPLODE
				elif (self.state == EXPLODE):
					exploded = state_explode()
					count += exploded
					jewels.append(exploded)
					totalcount += exploded
					chain += 1
					totalchain += chain
					self.lastscore = self.player.updatescore(exploded, chain)	
					score += self.lastscore	
					self.state = GRAVITY
				elif (self.state == GRAVITY):
					state_gravity()
					patterns = self.board.getpatterns()
					if self.board.hasones(patterns):
						self.state = EXPLODE
					else:
						self.state = REFILL
				elif (self.state == REFILL):
					state_refill()
					patterns = self.board.getpatterns()
					if self.board.hasones(patterns):
						self.state = EXPLODE
					else:
						print "Local Chain: %s\tJewels: %s: %s\tScore: %s" % (chain, jewels, sum(jewels), score)			
						print "Total Chain: %s\tJewels: %s\tScore: %s" % (totalchain, totalcount, self.player.score)
						self.state = BEGIN
					
				
			
			if (self.state == TERMINATE_FORCIBLY):					
				break
	

			self.iteration += 1
			
			if (self.pauses):
				raw_input("Press enter to continue.")
	

		print "****************************************************************"
		print "* Simulation terminated after %s moves" % (self.iteration - 1)
		print "****************************************************************"	
		print "* Total Chain: %s\tJewels: %s\tScore: %s" % (totalchain, totalcount, self.player.score)
		print "****************************************************************"		
		
		return (self.iteration-1,totalchain, totalcount, self.player.score)
		
			
