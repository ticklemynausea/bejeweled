# -*- coding: utf-8 -*-

class Node(object):

  def __init__(self, board):
    self.children = []  #child nodes
    self.parent = None
    self.board = board

  def __repr__(self):
    outStr = ""
    if (node.parent is None):
      outStr += "\t" * n, "node (children: %s)" % (len(node.children))
    else:
      outStr += "\t" * n, "node (children: %s) (move: %s) (score: %s) (bursted: %s)" % \
        (len(node.children), node.board.move, node.board.score, node.board.count)

    def printChildren(node, n):
      printChild(node, n)
      for child in node.children:
        printChildren(child, n+1)

    printChildren(self, 0)
    return outStr

  def setParent(self, parent):
    self.parent = parent

  def addChild(self, child):
    child.setParent(self)
    self.children.append(child)