# -*- coding: utf-8 -*-

import board
import player
import sys
import output

class Logic(object):

    def __init__(self, *args, **kwargs):

        def getPlayer(name):

            playeroptions = {

             'Human':
                player.Human(self.moves, self.name, self.inputStream),

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

        self.boardfile = kwargs.get('boardfile', None)
        self.refillfile = kwargs.get('refillfile', None)

        # Human Player
        self.name = None
        self.inputStream = sys.stdin

        # Main loop terminates when this is set True
        self.forceEnd = False

        # generate a new game
        if self.boardfile is None:
            columns = kwargs.get('columns')
            rows = kwargs.get('rows')
            colours = kwargs.get('colours')
            self.moves = getListOfPossibleMoves(columns, rows)
            self.board = board.Board(columns, rows, colours)
            self.board.sanitize()

        # load a saved board
        else:
            try:
                self.board = board.Board.LoadBoard(self.boardfile)
                self.board.refillboard = board.Board.LoadRefill(self.refillfile)
            except Exception as e:
                output.log("Error: ", e, module = 'Logic')
                sys.exit(0)

            self.moves = getListOfPossibleMoves(self.board.rows, self.board.columns)

        self.player  = getPlayer(kwargs.get('player'))

    # the playGame method implements the game logic using a state machine
    # each state_* method defined inside playGame implements the code in each state
    # the method body code does the transitions between states

    def playGame(self):

        STATE_BEGIN, STATE_MOVE, STATE_EXPLODE, STATE_GRAVITY, STATE_REFILL, STATE_TERMINATE = range(6)

        def stateBegin():

            output.event('logic_stateBegin', {
              'iteration' : self.iteration,
              'board_state' : self.board.state
            })

            return STATE_MOVE

        def stateMove():
            move = self.player.getMove(self.board)

            if (move == None):
                return True
            else:

                result = self.board.makeMove(move)

                output.event('logic_stateMove', {
                  'move' : str(move),
                  'marked_board' : self.board.state.reprConsoleMarkMoves(list(move)),
                  'move_result' : result
                })
                return False

        def stateExplode():

            (patterns, exploded) = self.board.explodePatterns()

            output.event('logic_stateExplode', {
              'patterns' : patterns,
              'exploded' : exploded,
              'board_state' : self.board.state,
              'shorten' : self.shorten
            })

            return exploded

        def stateGravity():

            fallCount = 0
            while not self.board.simulateGravity():
                fallCount += 1

            output.event('logic_stateGravity', {
              'board_state' : self.board.state,
              'fall_count' : fallCount,
              'shorten' : self.shorten
            })

        def stateRefill():
            (refill,_) = self.board.refillBoard()

            output.event('logic_stateRefill', {
              'board_state' : self.board.state,
              'refill' : refill,
              'shorten' : self.shorten
            })

        count = 0
        chain = 0
        totalcount = 0
        totalchain = 0
        score = 0

        self.iteration = 1
        while not self.forceEnd and (self.iteration <= self.limit or self.limit == 0):

            self.state = stateBegin()

            while self.state != STATE_BEGIN:
                if (self.state == STATE_MOVE):

                    #chain starts at -1 because the first time pieces explode, points should be multiplied by 2^0.
                    chain = -1
                    score = 0
                    jewels = []

                    result = stateMove()
                    if result:
                        output.log("Terminal state achieved in iteration %s. Score: %s." % (self.iteration, self.player.score), module = 'Logic')
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

        return {
          'iterations' : self.iteration - 1,
          'totalChains' : totalchain,
          'totalJewels' : totalcount,
          'score' : self.player.score
        }

    def endGame(self):
        self.forceEnd = True
