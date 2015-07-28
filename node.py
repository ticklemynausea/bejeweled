class Node(object):
#  def __init__(self, state, children):
#    self.state = state
#    self.children = children

  def __init__(self, board):
    self.children = []  #child nodes
    self.parent = None
    self.board = board

  def addchild(self, child):
    child.setparent(self)
    self.children.append(child)

  def setparent(self, parent):
    self.parent = parent

  def __repr__(self):
    def print_child(node, n):
      if (node.parent is None):
        print "\t" * n, "node (children: %s)" % (len(node.children))
      else:
        print "\t" * n, "node (children: %s) (move: %s) (score: %s) (bursted: %s)" % (len(node.children), 
          node.board.move, node.board.score, node.board.count)

    def print_children(node, n):
      print_child(node, n)
      for child in node.children:
        print_children(child, n+1)

    print_children(self, 0)
    return ""
