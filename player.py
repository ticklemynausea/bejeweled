import matrix
import random
from node import Node
from collections import deque,namedtuple
import code

class Player(object):

  def __init__(self, moves):
    self.moves = moves
    self.score = 0

  def getlistofvalidboards(self, board):
    def getvalidboards():
      for move in self.moves:
        newboard = board.moveandnewboard(move)
        if (newboard is not None):
          yield newboard

    validboards = list(getvalidboards())
    return validboards

  #get game tree
  def getgametree(self, board, depth):

    def expand_node(node):
      branches = self.getlistofvalidboards(node.board)
      for branch in branches:
        if (branch is not None):
          node.addchild(Node(branch))

    def recursive_expansion(node, depth):
      if (depth == 0):
        return node
      else:
        expand_node(node)
        for child in node.children:
          recursive_expansion(child, depth - 1)
        return node

    root = Node(board)
    return recursive_expansion(root, depth)

  def getpath(self, board):
    abstract

  def getmove(self, board):
    abstract

  def updatescore(self, jewels, chains):
    s = jewels * 100 * (2 ** chains)
    self.score += s
    return s

class GreedyEnergyVSEntropy(Player):

  def __repr__(self):
    return "Greedy: Energy VS Entropy (EnergyThreshold: %s) " % (self.energythreshold)

  def __init__(self, moves, energythreshold):
    Player.__init__(self, moves)
    self.energythreshold = energythreshold

  def getmove(self, board):
    print "Selecting move..."
    tree = self.getgametree(board, 1)
    energy = len(tree.children)

    moves = [x.board.move for x in tree.children]

    if len(moves) == 0:
      return None

    if energy < self.energythreshold:
      print "Energy %s is lower than %s, so I'll play near the bottom" %  (energy, self.energythreshold)
      move1 = min(moves, key = lambda x : x[0][0]) #choose nearest to the top
      move2 = min(moves, key = lambda x : x[1][0])
      move = min(move1, move2)
    else:
      print "Energy %s is higher or equal to %s, so I'll play near the top" %  (energy, self.energythreshold)
      move1 = max(moves, key = lambda x : x[0][0]) #choose nearest to the top
      move2 = max(moves, key = lambda x : x[1][0])
      move = max(move1, move2)

    print move

    print "Move is ", move
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

  def getpath(self, tree):

    #print bestyet.score
    def depthfirst(node, energy, path):

      if node.parent is not None:
        thisenergy = energy + len(node.children)
        thispath = path + (node.board.move,)
      else:
        thisenergy = 0
        thispath = ()

      bestyet = self.BestYet(energy=thisenergy, path=thispath)
      if len(node.children) > 0:
        def bestchild():
          for child in node.children:
            yield depthfirst(child, thisenergy, thispath)

        bestyet = max(bestchild(), key=lambda x: x.energy)
      return bestyet

    return depthfirst(tree, 0, ())

  def getmove(self, board):
    print "Calculating tree up to %s levels..." % self.depth
    tree = self.getgametree(board, self.depth)
    print "Calculating best path..."
    (totalenergy, path) = self.getpath(tree)

    energyperdepthlevel =  (totalenergy / self.depth)

    if len(path) > 0:
      if energyperdepthlevel >= self.energythreshold:
        print "Energy per depth level is %s, above the threshold of %s" % (energyperdepthlevel, self.energythreshold)
        print "Will attempt to preserve this and play near the top"

        moves = [x.board.move for x in tree.children]

        move1 = max(moves, key = lambda x : x[0][0]) #choose nearest to the top
        move2 = max(moves, key = lambda x : x[1][0])
        move = max(move1, move2)
        return move

      else:
        print "Energy per depth level is %s, below the threshold of %s" % (energyperdepthlevel, self.energythreshold)
        print "Path is %s (Energy: %s). Will take first step and recalculate." % (path, totalenergy)
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

  def getpath(self, tree):

    #print bestyet.score
    def depthfirst(node, energy, path):

      if node.parent is not None:
        thisenergy = energy + len(node.children)
        thispath = path + (node.board.move,)
      else:
        thisenergy = 0
        thispath = ()

      bestyet = self.BestYet(energy=thisenergy, path=thispath)
      if len(node.children) > 0:
        def bestchild():
          for child in node.children:
            yield depthfirst(child, thisenergy, thispath)

        bestyet = max(bestchild(), key=lambda x: x.energy)
      return bestyet

    return depthfirst(tree, 0, ())

  def getmove(self, board):
    print "Calculating tree up to %s levels..." % self.depth
    tree = self.getgametree(board, self.depth)
    print "Calculating best path..."
    (totalenergy, path) = self.getpath(tree)

    energyperdepthlevel =  (totalenergy / self.depth)

    if len(path) > 0:
      if energyperdepthlevel < self.energythreshold:
        print "Energy per depth level is %s, below the threshold of %s" % (energyperdepthlevel, self.energythreshold)
        print "Will attempt to get lucky and play near the bottom"

        moves = [x.board.move for x in tree.children]

        move1 = min(moves, key = lambda x : x[0][0]) #choose nearest to the bottom
        move2 = min(moves, key = lambda x : x[1][0])
        move = min(move1, move2)
        return move

      else:
        print "Energy per depth level is %s, above the threshold of %s" % (energyperdepthlevel, self.energythreshold)
        print "Path is %s (Energy: %s). Will take first step and recalculate." % (path, totalenergy)
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

  def getpath(self, tree):

    #print bestyet.score
    def depthfirst(node, score, energy, path):

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
        def bestchild():
          for child in node.children:
            yield depthfirst(child, thisscore, thisenergy, thispath)
        candidates = []

        for child in bestchild():
          candidates.append(child)

        electables = [candidate for candidate in candidates if candidate.energy >= self.minenergy]
        if len(electables) > 0:
          bestyet = max(electables, key=lambda x: x.score)
        else:
          bestyet = max(candidates, key=lambda x: x.energy)

      return bestyet

    return depthfirst(tree, 0, 0, ())

  def getmove(self, board):
    print "Calculating tree up to %s levels..." % self.depth
    tree = self.getgametree(board, self.depth)
    print "Calculating path..."
    (score, energy, path) = self.getpath(tree)
    print "Path is %s (Score: %s) (Energy: %s). Will take first step and recalculate." % (path, score, energy)
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

  def getpath(self, tree):

    #print bestyet.score
    def depthfirst(node, energy, path):

      if node.parent is not None:
        thisenergy = energy + len(node.children)
        thispath = path + (node.board.move,)
      else:
        thisenergy = 0
        thispath = ()

      bestyet = self.BestYet(energy=thisenergy, path=thispath)
      if len(node.children) > 0:
        def bestchild():
          for child in node.children:
            yield depthfirst(child, thisenergy, thispath)

        bestyet = max(bestchild(), key=lambda x: x.energy)
      return bestyet

    return depthfirst(tree, 0, ())

  def getmove(self, board):
    print "Calculating tree up to %s levels..." % self.depth
    tree = self.getgametree(board, self.depth)
    print "Calculating path..."
    (energy, path) = self.getpath(tree)
    print "Path is %s (Energy: %s). Will take first step and recalculate." % (path, energy)
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

  def getpath(self, tree):

    #print bestyet.score
    def depthfirst(node, score, path):

      if node.parent is not None:
        thisscore = score + node.board.score
        thispath = path + (node.board.move,)
      else:
        thisscore = 0
        thispath = ()

      bestyet = self.BestYet(score=thisscore, path=thispath)
      if len(node.children) > 0:
        def bestchild():
          for child in node.children:
            yield depthfirst(child, thisscore, thispath)

        bestyet = max(bestchild(), key=lambda x: x.score)
      return bestyet

    return depthfirst(tree, 0, ())

  def getmove(self, board):
    print "Calculating tree up to %s levels..." % self.depth
    tree = self.getgametree(board, self.depth)
    print "Calculating path..."
    (score, path) = self.getpath(tree)
    print "Path is %s (Score: %s). Will take first step and recalculate." % (path, score)
    if len(path) > 0:
      return path[0]
    else:
      return None
