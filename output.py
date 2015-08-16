# -*- coding: utf-8 -*-

moduleLog = {

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
				print "[%s] %s" % (module, text)
			else:
				print "%s" % (text)
	else:
		raise ValueError("Unknown module %s" % module)