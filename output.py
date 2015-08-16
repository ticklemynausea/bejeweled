# -*- coding: utf-8 -*-

LEVEL_DEBUG, LEVEL_NORMAL, LEVEL_IMPORTANT = range(3)

logLevel = LEVEL_DEBUG

def log(text, level = 1):
	if level >= logLevel:
		print text