# -*- coding: utf-8 -*-

import matrix
import random
from node import Node
from collections import deque, namedtuple
import code
import output

class Player(object):

  def __init__(self, moves):
    self.moves = moves
    self.score = 0

  def getListOfPossibleBoards(self, board):

    def getPossibleBoards():
      for move in self.moves:
        newboard = board.makeMoveAndReturnNewBoard(move)
        if (newboard is not None):
          yield newboard

    return list(getPossibleBoards())

  #get game tree
  def getGameTree(self, board, depth):

    def expandNode(node):
      branches = self.getListOfPossibleBoards(node.board)
      for branch in branches:
        if (branch is not None):
          node.addChild(Node(branch))

    def recursiveExpansion(node, depth):
      if (depth == 0):
        return node
      else:
        expandNode(node)
        for child in node.children:
          recursiveExpansion(child, depth - 1)
        return node

    root = Node(board)
    return recursiveExpansion(root, depth)

  def getPath(self, board):
    abstract

  def getMove(self, board):
    abstract

  def updateScore(self, jewels, chains):
    s = jewels * 100 * (2 ** chains)
    self.score += s
    return s

class GreedyEnergyVSEntropy(Player):

  def __init__(self, moves, energythreshold):
    Player.__init__(self, moves)
    self.energythreshold = energythreshold

  def __repr__(self):
    return "Greedy: Energy VS Entropy (EnergyThreshold: %s) " % (self.energythreshold)

  def getMove(self, board):
    output.log('Player', "Selecting move...", module = 'Player')
    tree = self.getGameTree(board, 1)
    energy = len(tree.children)

    moves = [x.board.move for x in tree.children]

    if len(moves) == 0:
      return None

    if energy < self.energythreshold:
      output.log("Energy %s is lower than %s, so I'll play near the bottom" %  (energy, self.energythreshold), module = 'Player')
      move1 = min(moves, key = lambda x : x[0][0]) #choose nearest to the top
      move2 = min(moves, key = lambda x : x[1][0])
      move = min(move1, move2)
    else:
      output.log("Energy %s is higher or equal to %s, so I'll play near the top" %  (energy, self.energythreshold), module = 'Player')
      move1 = max(moves, key = lambda x : x[0][0]) #choose nearest to the top
      move2 = max(moves, key = lambda x : x[1][0])
      move = max(move1, move2)

    output.log(move, module = 'Player')

    output.log("Move is ", move, module = 'Player')
    return move

""" What """

class EnergyVSEntropyReversed(Player):

  def __init__(self, moves, depth, energythreshold):
    Player.__init__(self, moves)
    self.depth = depth
    self.energythreshold = energythreshold
    self.BestYet = namedtuple("BestYet", "energy path")

  def __repr__(self):
    return "Energy VS Entropy Reversed (EnergyPerDepthLevelThreshold %s) (MaxDepth: %s)" % (self.energythreshold, self.depth)

  def getPath(self, tree):

    #output.log(module = 'Player', bestyet.score)
    def depthFirst(node, energy, path):

      if node.parent is not None:
        thisenergy = energy + len(node.children)
        thispath = path + (node.board.move,)
      else:
        thisenergy = 0
        thispath = ()

      bestyet = self.BestYet(energy=thisenergy, path=thispath)
      if len(node.children) > 0:
        def bestChild():
          for child in node.children:
            yield depthFirst(child, thisenergy, thispath)

        bestyet = max(bestChild(), key=lambda x: x.energy)
      return bestyet

    return depthFirst(tree, 0, ())

  def getMove(self, board):
    output.log("Calculating tree up to %s levels..." % self.depth, module = 'Player')
    tree = self.getGameTree(board, self.depth)
    output.log("Calculating best path...", module = 'Player')
    (totalenergy, path) = self.getPath(tree)

    energyperdepthlevel =  (totalenergy / self.depth)

    if len(path) > 0:
      if energyperdepthlevel >= self.energythreshold:
        output.log("Energy per depth level is %s, above the threshold of %s" % (energyperdepthlevel, self.energythreshold), module = 'Player')
        output.log("Will attempt to preserve this and play near the top", module = 'Player')

        moves = [x.board.move for x in tree.children]

        move1 = max(moves, key = lambda x : x[0][0]) #choose nearest to the top
        move2 = max(moves, key = lambda x : x[1][0])
        move = max(move1, move2)
        return move

      else:
        output.log("Energy per depth level is %s, below the threshold of %s" % (energyperdepthlevel, self.energythreshold), module = 'Player')
        output.log('Player', "Path is %s (Energy: %s). Will take first step and recalculate." % (path, totalenergy), module = 'Player')
        move = path[0]

        return move
    else:
      return None

class EnergyVSEntropy(Player):

  def __init__(self, moves, depth, energythreshold):
    Player.__init__(self, moves)
    self.depth = depth
    self.energythreshold = energythreshold
    self.BestYet = namedtuple("BestYet", "energy path")

  def __repr__(self):
    return "Energy VS Entropy (EnergyPerDepthLevelThreshold %s) (MaxDepth: %s)" % (self.energythreshold, self.depth)

  def getPath(self, tree):

    #output.log(module = 'Player', bestyet.score)
    def depthFirst(node, energy, path):

      if node.parent is not None:
        thisenergy = energy + len(node.children)
        thispath = path + (node.board.move,)
      else:
        thisenergy = 0
        thispath = ()

      bestyet = self.BestYet(energy=thisenergy, path=thispath)
      if len(node.children) > 0:
        def bestChild():
          for child in node.children:
            yield depthFirst(child, thisenergy, thispath)

        bestyet = max(bestChild(), key=lambda x: x.energy)
      return bestyet

    return depthFirst(tree, 0, ())

  def getMove(self, board):
    output.log("Calculating tree up to %s levels..." % self.depth, module = 'Player')
    tree = self.getGameTree(board, self.depth)
    output.log("Calculating best path...", module = 'Player')
    (totalenergy, path) = self.getPath(tree)

    energyperdepthlevel =  (totalenergy / self.depth)

    if len(path) > 0:
      if energyperdepthlevel < self.energythreshold:
        output.log("Energy per depth level is %s, below the threshold of %s" % (energyperdepthlevel, self.energythreshold), module = 'Player')
        output.log("Will attempt to get lucky and play near the bottom", module = 'Player')

        moves = [x.board.move for x in tree.children]

        move1 = min(moves, key = lambda x : x[0][0]) #choose nearest to the bottom
        move2 = min(moves, key = lambda x : x[1][0])
        move = min(move1, move2)
        return move

      else:
        output.log("Energy per depth level is %s, above the threshold of %s" % (energyperdepthlevel, self.energythreshold), module = 'Player')
        output.log("Path is %s (Energy: %s). Will take first step and recalculate." % (path, totalenergy), module = 'Player')
        move = path[0]

        return move
    else:
      return None

class BestScoreBetterEnergy(Player):

  def __repr__(self):
    return "BestScore/BetterEnergy (MaxDepth: %s) (MinEnergy: %s) " % (self.depth, self.minenergy)

  def __init__(self, moves, depth, minenergy):
    Player.__init__(self, moves)
    self.depth = depth
    self.minenergy = minenergy
    self.sequence = deque([])
    self.BestYet = namedtuple("BestYet", "score energy path")

  def getPath(self, tree):

    #output.log(module = 'Player', bestyet.score)
    def depthFirst(node, score, energy, path):

      if node.parent is not None:
        thisscore = score + node.board.score
        thisenergy = energy + len(node.children)
        thispath = path + (node.board.move,)
      else:
        thisscore = 0
        thisenergy = 0
        thispath = ()

      bestyet = self.BestYet(score=thisscore, energy=thisenergy, path=thispath)
      if len(node.children) > 0:
        def bestChild():
          for child in node.children:
            yield depthFirst(child, thisscore, thisenergy, thispath)
        candidates = []

        for child in bestChild():
          candidates.append(child)

        electables = [candidate for candidate in candidates if candidate.energy >= self.minenergy]
        if len(electables) > 0:
          bestyet = max(electables, key=lambda x: x.score)
        else:
          bestyet = max(candidates, key=lambda x: x.energy)

      return bestyet

    return depthFirst(tree, 0, 0, ())

  def getMove(self, board):
    output.log("Calculating tree up to %s levels..." % self.depth, module = 'Player')
    tree = self.getGameTree(board, self.depth)
    output.log("Calculating path...", module = 'Player')
    (score, energy, path) = self.getPath(tree)
    output.log("Path is %s (Score: %s) (Energy: %s). Will take first step and recalculate." % (path, score, energy), module = 'Player')
    if len(path) > 0:
      return path[0]
    else:
      return None

class BestEnergy(Player):

  def __init__(self, moves, depth):
    Player.__init__(self, moves)
    self.depth = depth
    self.BestYet = namedtuple("BestYet", "energy path")

  def __repr__(self):
    return "Best Energy (MaxDepth: %s)" % (self.depth)

  def getPath(self, tree):

    #output.log(module = 'Player', bestyet.score)
    def depthFirst(node, energy, path):

      if node.parent is not None:
        thisenergy = energy + len(node.children)
        thispath = path + (node.board.move,)
      else:
        thisenergy = 0
        thispath = ()

      bestyet = self.BestYet(energy=thisenergy, path=thispath)
      if len(node.children) > 0:
        def bestChild():
          for child in node.children:
            yield depthFirst(child, thisenergy, thispath)

        bestyet = max(bestChild(), key=lambda x: x.energy)
      return bestyet

    return depthFirst(tree, 0, ())

  def getMove(self, board):
    output.log("Calculating tree up to %s levels..." % self.depth, module = 'Player')
    tree = self.getGameTree(board, self.depth)
    output.log("Calculating path...", module = 'Player')
    (energy, path) = self.getPath(tree)
    output.log("Path is %s (Energy: %s). Will take first step and recalculate." % (path, energy), module = 'Player')
    if len(path) > 0:
      return path[0]
    else:
      return None

class BestScore(Player):
  def __repr__(self):
    return "Best Score (MaxDepth: %s)" % (self.depth)

  def __init__(self, moves, depth):
    Player.__init__(self, moves)
    self.depth = depth
    self.sequence = deque([])
    self.BestYet = namedtuple("BestYet", "score path")

  def getPath(self, tree):

    #output.log(module = 'Player', bestyet.score)
    def depthFirst(node, score, path):

      if node.parent is not None:
        thisscore = score + node.board.score
        thispath = path + (node.board.move,)
      else:
        thisscore = 0
        thispath = ()

      bestyet = self.BestYet(score=thisscore, path=thispath)
      if len(node.children) > 0:
        def bestChild():
          for child in node.children:
            yield depthFirst(child, thisscore, thispath)

        bestyet = max(bestChild(), key=lambda x: x.score)
      return bestyet

    return depthFirst(tree, 0, ())

  def getMove(self, board):
    output.log("Calculating tree up to %s levels..." % self.depth, module = 'Player')
    tree = self.getGameTree(board, self.depth)
    output.log("Calculating path...", module = 'Player')
    (score, path) = self.getPath(tree)
    output.log("Path is %s (Score: %s). Will take first step and recalculate." % (path, score), module = 'Player')
    if len(path) > 0:
      return path[0]
    else:
      return None
