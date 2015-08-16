# -*- coding: utf-8 -*-

import board
import player
import sys
import output

class Logic(object):

  def __init__(self, *args, **kwargs):

    def getPlayer(name):

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

      return playeroptions[name]

    def getListOfPossibleMoves(rows, columns):

      moves = []

      #horizontals
      for i_a in range(0, rows):
        for j_a in range(0, columns-1):
          moves.append(((i_a, j_a), (i_a, j_a+1)))

      #verticals
      for i_a in range(0, rows-1):
        for j_a in range(0, columns):
          moves.append(((i_a, j_a), (i_a+1, j_a)))

      #output.log("For this %sx%s board, there are a total of %s possible moves " % (rows, columns, len(moves)), module = 'Logic')
      return moves

    self.pauses = kwargs.get('pause', False)
    self.shorten = kwargs.get('shorten', False)
    self.limit = kwargs.get('limit')
    self.depth = kwargs.get('depth')
    self.minenergy = kwargs.get('minenergy', 2)
    self.energythreshold = kwargs.get('energythreshold')

    boardfile = kwargs.get('boardfile', None)
    refillfile = kwargs.get('refillfile', None)

    if boardfile is None:
      columns = kwargs.get('columns')
      rows = kwargs.get('rows')
      colours = kwargs.get('colours')
      self.moves = getListOfPossibleMoves(columns, rows)
      self.board = board.Board(columns, rows, colours)

      self.player  = getPlayer(kwargs.get('player'))

      output.log("**************************************", module = 'Logic')
      output.log("* Welcome to AI Bejeweled", module = 'Logic')
      output.log("* Rules:", module = 'Logic')
      output.log("*\t%sx%sx%s (%s possible moves)" % (columns, rows, colours, len(self.moves)), module = 'Logic')
      output.log("*\tUsing IA Agent %s " % self.player, module = 'Logic')
      output.log("*\tWill terminate after %s moves" % (self.limit), module = 'Logic')
      output.log("**************************************", module = 'Logic')

      self.board.sanitize()

    else:
      try:
        self.board = board.Board.LoadBoard(boardfile)
        self.board.refillboard = board.Board.LoadRefill(refillfile)
      except Exception as e:
        output.log("Error: ", e, module = 'Logic')
        sys.exit(0)

      self.moves = getListOfPossibleMoves(self.board.rows, self.board.columns)
      self.player  = getPlayer(kwargs.get('player'))

      output.log("**************************************", module = 'Logic')
      output.log("* Welcome to AI Bejeweled", module = 'Logic')
      output.log("* Rules:", module = 'Logic')
      output.log("*\tUsing board from %s and refill from %s " % (boardfile, refillfile), module = 'Logic')
      output.log("*\t%sx%sx%s (%s possible moves)" % (self.board.columns, self.board.rows, self.board.colors, len(self.moves)), module = 'Logic')
      output.log("*\tUsing IA Agent %s " % self.player, module = 'Logic')
      output.log("*\tWill terminate after %s moves" % (self.limit), module = 'Logic')
      output.log("**************************************", module = 'Logic')

  # método play implementa a logica de jogo como uma máquina de estados.
  # os sub métodos são o código implementado por cada estado
  # o resto do código trata das transições entre estados
  # e passagem de argumentos

  def playGame(self):

    def stateBegin():

      output.log("***********************", module = 'Logic')
      output.log("* begin iteration %s " %  self.iteration, module = 'Logic')
      output.log("***********************", module = 'Logic')
      output.log("Board:", module = 'Logic' )
      output.log(self.board.state, module = 'Logic', printModule = False)

    def stateMove():
      move = self.player.getMove(self.board)

      if (move == None):
        return True
      else:

        result = self.board.makeMove(move)
        output.log("Move selected: %s " % str(move), module = 'Logic')
        if result is False:
            output.log("Player asked me to perform an invalid move.", module = 'Logic')
            output.log("Probably he is a path follower. Please ignore this.", module = 'Logic')
        else:
          output.log(self.board.state.reprConsoleMarkMoves(list(move)), module = 'Logic', printModule = False)

        return False

    def stateExplode():
      ### STATE_EXPLODE ###
      (patterns, exploded) = self.board.explodePatterns()
      if (exploded != 0):
        if not self.shorten:
          output.log("Patterns:", module = 'Logic')
          output.log(patterns, module = 'Logic', printModule = False)
          #output.log("Board state: before gravity", module = 'Logic')
          #output.log(self.board.state, module = 'Logic', printModule = False)

      return exploded

    def stateGravity():
      #STATE_GRAVITY
      gravities = 0
      while not self.board.simulateGravity():
        gravities += 1
      #if (gravities > 0):
      #  if not self.shorten:
      #    output.log("Board state: after gravity", module = 'Logic')
      #    output.log(self.board.state, module = 'Logic', printModule = False)

    def stateRefill():
      (refill,_) = self.board.refillBoard()
      if not self.shorten:
        output.log("Refill:", module = 'Logic')
        output.log(refill, module = 'Logic', printModule = False)
        output.log("Refilled:", module = 'Logic')
        output.log(self.board.state, module = 'Logic', printModule = False)

    self.iteration = 1
    count = 0
    chain = 0
    totalcount = 0
    totalchain = 0
    score = 0

    #STATES
    STATE_BEGIN, STATE_MOVE, STATE_EXPLODE, STATE_GRAVITY, STATE_REFILL, STATE_TERMINATE = range(6)

    while self.iteration <= self.limit or self.limit == 0:
      stateBegin()

      self.state = STATE_MOVE
      while self.state != STATE_BEGIN:
        if (self.state == STATE_MOVE):

          #chain starts at -1 because the first time pieces explode, points should be multiplied by 2^0.
          chain = -1
          score = 0
          jewels = []
          result = stateMove()
          if result:
            output.log("Terminal state achieved in iteration %s.\nScore: %s: " % (self.iteration, self.player.score), module = 'Logic')
            output.log(self.board.state, module = 'Logic', printModule = False)
            self.state = STATE_TERMINATE
            break

          self.state = STATE_EXPLODE
        elif (self.state == STATE_EXPLODE):
          exploded = stateExplode()
          count += exploded
          jewels.append(exploded)
          totalcount += exploded
          chain += 1
          totalchain += chain
          self.lastscore = self.player.updateScore(exploded, chain)
          score += self.lastscore
          self.state = STATE_GRAVITY
        elif (self.state == STATE_GRAVITY):
          stateGravity()
          patterns = self.board.getPatterns()
          if self.board.hasOnes(patterns):
            self.state = STATE_EXPLODE
          else:
            self.state = STATE_REFILL
        elif (self.state == STATE_REFILL):
          stateRefill()
          patterns = self.board.getPatterns()
          if self.board.hasOnes(patterns):
            self.state = STATE_EXPLODE
          else:
            output.log("Local Chain: %s\tJewels: %s: %s\tScore: %s" % (chain, jewels, sum(jewels), score), module = 'Logic')
            output.log("Total Chain: %s\tJewels: %s\tScore: %s" % (totalchain, totalcount, self.player.score), module = 'Logic')
            self.state = STATE_BEGIN

      if (self.state == STATE_TERMINATE):
        break

      self.iteration += 1

      if (self.pauses):
        raw_input("Press enter to continue.")

    output.log("****************************************************************", module = 'Logic')
    output.log("* Simulation terminated after %s moves" % (self.iteration - 1), module = 'Logic')
    output.log("****************************************************************", module = 'Logic')
    output.log("* Total Chain: %s\tJewels: %s\tScore: %s" % (totalchain, totalcount, self.player.score), module = 'Logic')
    output.log("****************************************************************", module = 'Logic')

    return (self.iteration - 1, totalchain, totalcount, self.player.score)
