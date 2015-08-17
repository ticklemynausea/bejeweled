# -*- coding: utf-8 -*-

import sys

moduleLog = {

  'Main' : True,
  'Player' : True,
  'Board' : True,
  'Logic' : True,
  'Output' : True

}

def log(text, module = None, printModule = True):

    if module is None:
        print text

    elif module in moduleLog.keys():

        if moduleLog[module]:
            if printModule:
                print "[ %s ] %s" % (module.ljust(6), text)
            else:
                print "%s" % (text)

    else:
        raise ValueError("Unknown module %s" % module)


def console_logic_stateBegin(args):

    log("***********************", module = 'Logic')
    log("* begin iteration %s " %  args['iteration'], module = 'Logic')
    log("***********************", module = 'Logic')
    log("Board:", module = 'Logic')
    log(args['board_state'], module = 'Logic', printModule = False)


def console_logic_stateMove(args):
    log("Move selected: %s " % args['move'], module = 'Logic')
    log(args['marked_board'], module = 'Logic', printModule = False)

    if args['move_result'] is False:
        log("Player asked me to perform an invalid move.", module = 'Logic')
        log("Probably he is a human. Doing nothing.", module = 'Logic')

def console_logic_stateExplode(args):
    if (args['exploded'] != 0):
        if not args['shorten']:
            log("Patterns:", module = 'Logic')
            log(args['patterns'], module = 'Logic', printModule = False)
            log("Board state: before gravity", module = 'Logic')
            log(args['board_state'], module = 'Logic', printModule = False)

def console_logic_stateGravity(args):
    if (args['fall_count'] > 0):
        if not args['shorten']:
            log("Board state: after gravity", module = 'Logic')
            log(args['board_state'], module = 'Logic', printModule = False)

def console_logic_stateRefill(args):
    if not args['shorten']:
        log("Refill:", module = 'Logic')
        log(args['refill'], module = 'Logic', printModule = False)
        log("Refilled:", module = 'Logic')
        log(args['board_state'], module = 'Logic', printModule = False)



def event(name, args):

    events_console = {
      'logic_stateBegin' : console_logic_stateBegin,
      'logic_stateMove' : console_logic_stateMove,
      'logic_stateExplode' : console_logic_stateExplode,
      'logic_stateGravity' : console_logic_stateGravity,
      'logic_stateRefill' : console_logic_stateRefill,

    }

    events = events_console

    try:
        events[name](args)
    except IndexError:
        log("Event %s not defined" % name, module = 'Output')
