# -*- coding: utf-8 -*-

moduleLog = {

	'Player' : True,
	'Board' : True,
	'Logic' : True

}

def log(text, module = None):
	if module is None:
		print text
	elif module in moduleLog.keys():
		if moduleLog[module]:
			print "[%s] %s" % (module, text)
	else:
		raise ValueError("Unknown module %s" % module)

def logBoard(boardText, module = None):
	log("\n" + boardText, module)