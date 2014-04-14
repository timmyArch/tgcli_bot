#!/usr/bin/env python2
"""

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.

"""

import cmd
import random
import re
import pycurl
from StringIO import StringIO
from optparse import OptionParser
from db import BotTasks

#variable declaration
botDatabase = BotTasks()
parser = OptionParser(usage = "usage: %prog [options] arg1 arg2")
parser.add_option("-n",
									"--name",
									dest="name",
									type="string",
									default=False,
									help="name of the sender")
parser.add_option("-m",
									"--message",
									dest="message",
									type="string",
									default=False,
									help="message from telegram")
(options, args) = parser.parse_args()
sName = options.name
sMessage = options.message
fSallutation = "content_files/sallutation.txt"
fBOFH = "content_files/bofhquotes.txt"

def __checkMessage():
	__membercommands = botDatabase.getMemberCommandsByMemberNames(sName)
	if __membercommands and sMessage.split(' ')[0][1:] in __membercommands:
		return __performCommand(sMessage)
	else:
		if sMessage in botDatabase.getCommands():
			return "Permission denied!"
		else:
			if cmd.__checkSallutation(sMessage, fSallutation):
				return cmd.__getSallutation(fSallutation)
			if cmd.__checkHttpTitle(sMessage):
				return cmd.__getHttpTitle(sMessage)

def __performCommand(sMessage):
	__aArgs = sMessage.split(" ")
	if __aArgs[0] == ",ping" or __aArgs[0] == "!ping":
		return(cmd.__ping(__aArgs[1]))
	elif __aArgs[0] == ",uptime" or __aArgs[0] == "!uptime":
		return(cmd.__getUptime())
	elif __aArgs[0] == ",load" or __aArgs[0] == "!load":
		return(cmd.__getLoad())
	elif __aArgs[0] == ",mem" or __aArgs[0] == "!mem":
		return(cmd.__getUsedMem())
	elif __aArgs[0] == ",disk" or __aArgs[0] == "!disk":
		return(cmd.__getDiskUsage())
	elif __aArgs[0] == ",list" or __aArgs[0] == "!list":
		return(cmd.__listCommands(sName))
	elif __aArgs[0] == ",hint" or __aArgs[0] == "!hint":
		return(cmd.__hint(sMessage))
	#elif __aArgs[0] == ",showAllTasks" or __aArgs[0] == "!showAllTasks":
	#	return(cmd.__showAllTasks())
	#elif __aArgs[0] == ",showTasks" or __aArgs[0] == "!showTasks":
	#	return(cmd.__showTasks())
	#elif __aArgs[0] == ",addTask" or __aArgs[0] == "!addTask":
	#	return(cmd.__addTasks())
	#elif __aArgs[0] == ",delTask" or __aArgs[0] == "!delTask":
	#	return(cmd.__delTasks(__aArgs[1]))
	#elif __aArgs[0] == ",bofh" or __aArgs[0] == "!bofh":
	#	return(cmd.__bofh(fBOFH))
	#elif __aArgs[0] == ",listMemes" or __aArgs[0] == "!listMemes":
	#	return(cmd.__listMemes())
	##elif __aArgs[0] == ",meme" or __aArgs[0] == "!meme":
	#	return(cmd.__meme(__aArgs[1]))

a=__checkMessage()
if a and not a == "":
	print(a)
