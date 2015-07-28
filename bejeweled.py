#!/usr/bin/python
# coding=UTF8

import logic
import sys
import board
from optparse import OptionParser, OptionGroup

usage = "usage: %prog [options]"

parser = OptionParser(usage)

parser.add_option("-g", "--generate", action="store",
          type="int", nargs=3, dest="generate", 
          help="Generates and outputs to stdout a board with given columns, rows and colours before terminating.")

parser.add_option("-s", "--size", action="store", 
          type="int", nargs=3, dest="size", 
          help="Generates a random board and then runs a simulation according to given parameters. Default is %default.",             default=[8,8,7])

parser.add_option("--shorten", action="store_true", dest="shorten", help="Shortens the game's output, showing less information")

parser.add_option("--pause", action="store_true", dest="pause", help="Pauses game when each iteration is completed.")

parser.add_option("-l", "--load", action="store", 
          type="string", nargs=2 ,dest="filename", 
          help="Loads two boards from FILENAME: One with the initial state and another that will be used to refill gaps. Then runs a simulation according to given parameters.")

parser.add_option("-n", "--limit", action="store", 
          type="int", dest="limit", 
          help="Limits the number of iterations to LIMIT. Default is %default.", default=20000)

group_player = OptionGroup(parser, "Player Agent Settings")

playerchoices = ["BestScore", "BestEnergy", "BestScoreBetterEnergy", "EnergyVSEntropy", "GreedyEnergyVSEntropy", "EnergyVSEntropyReversed"]
group_player.add_option("--minenergy", action="store", 
          type="int", dest="minenergy", 
          help="Used by BestScoreBetterEnergy. Determines the minimum level of energy in which is safe to find the best score. Default is %default", default=5)

group_player.add_option("-p", "--player", action="store", 
          type="choice", choices=playerchoices, dest="player", 
          help=("Specify player type. Default is BestScore. Choices are %r" % playerchoices), default="BestEnergy")

group_player.add_option("--depth", action="store", 
          type="int", dest="depth", 
          help="Calculate trees of given depth. Default is %default.", default=2)

group_player.add_option("--energythreshold", action="store", 
          type="int", dest="energythreshold", 
          help="Energy threshold level used by EnergyVSEntropy agents. Default is %default", default=10)

parser.add_option_group(group_player)

(options, args) = parser.parse_args()

b_pause = options.pause
b_shorten = options.shorten

if options.generate:
  b_rows = options.generate[0]
  b_cols = options.generate[1]
  b_colours = options.generate[2]

  b = board.Board(columns=b_cols, rows=b_rows, colors=b_colours)
  b.sanitize(False)

  for line in b.state.matrix:
    print line.__repr__().replace(' ', '').replace('[', '').replace(']', '')

  sys.exit(0)

if options.filename:
  b_limit = options.limit
  b_depth = options.depth
  b_boardfile = options.filename[0]
  b_refillfile = options.filename[1]
  b_player = options.player
  b_minenergy = options.minenergy
  b_energythreshold = options.energythreshold

  if b_player == "BestEnergy" or b_player == "BestScoreBetterEnergy" or b_player == "EnergyVSEntropy" or b_player == "EnergyVSEntropyReversed":
    if b_depth <= 1:
      print "%s can only be used with a depth level of at least 2" % b_player
      sys.exit(0)

  game = logic.Logic(boardfile=b_boardfile, refillfile=b_refillfile, limit=b_limit, player=b_player, 
    depth=b_depth, minenergy=b_minenergy, pause=b_pause,
    energythreshold=b_energythreshold, shorten=b_shorten)

else:
  b_limit = options.limit
  b_depth = options.depth
  b_rows = options.size[0]
  b_cols = options.size[1]
  b_colours = options.size[2]
  b_player = options.player
  b_minenergy = options.minenergy  
  b_energythreshold = options.energythreshold

  if b_player == "BestEnergy" or b_player == "BestScoreBetterEnergy" or b_player == "EnergyVSEntropy" or b_player == "EnergyVSEntropyReversed":
    if b_depth <= 1:
      print "%s can only be used with a depth level of at least 2" % b_player
      sys.exit(0)

  game = logic.Logic(limit=b_limit, player=b_player, columns=b_cols, rows=b_rows, 
    colours=b_colours, depth=b_depth, minenergy=b_minenergy, pause=b_pause,
    energythreshold=b_energythreshold, shorten=b_shorten)

game.play()
