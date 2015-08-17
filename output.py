# -*- coding: utf-8 -*-

moduleLog = {

	'Main' : True,
	'Player' : True,
	'Board' : True,
	'Logic' : True

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