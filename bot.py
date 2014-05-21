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
import ConfigParser
import random
import re
import pycurl
import os,sys
from StringIO import StringIO
from optparse import OptionParser
from db import BotTasks

#variable declaration
botDatabase = BotTasks()
__parserOptions = OptionParser(usage = "usage: %prog [options] arg1 arg2")
__parserOptions.add_option("-n",
									"--name",
									dest="name",
									type="string",
									default=False,
									help="name of the chat")
__parserOptions.add_option("-m",
									"--message",
									dest="message",
									type="string",
									default=False,
									help="message from telegram")
__parserOptions.add_option("-s",
									"--sender",
									dest="sender",
									type="string",
									default=False,
									help="name of the sender")
__parserOptions.add_option("-t",
									"--task",
									action="store_true",
									dest="task",
									help="starts just the taskscheduler")
(options, args) = __parserOptions.parse_args()
sName = options.name
sMessage = options.message
sSender = options.sender
bTasks = options.task
__parserConfig = ConfigParser.ConfigParser()
__pathConfigFile = "/usr/local/etc/telpy/bot.cfg"
__parserConfig.read(__pathConfigFile)
fSallutation = __parserConfig.get('Files', 'sallutation')
fBOFH = __parserConfig.get('Files', 'bofh')
fSmiley = __parserConfig.get('Files', 'smiley')
dMeme = __parserConfig.get('Directory', 'memes')

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
			if cmd.__checkURL(sMessage):
				return cmd.__getHttpTitle(sMessage)
			if sSender.lower() == "tim_meusel":
				return cmd.__correctTim(sMessage, fSmiley)

def __performCommand(sMessage):
	__aArgs = sMessage.split(" ")
	if __aArgs[0] == ",ping" or __aArgs[0] == "!ping":
		return(cmd.__ping(__aArgs[1]))
	elif __aArgs[0] == ",http" or __aArgs[0] == "!http":
		return(cmd.__httpPing(__aArgs[1]))
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
	elif __aArgs[0] == ",showTasks" or __aArgs[0] == "!showTasks":
		return(cmd.__showTasks(sName))
	#elif __aArgs[0] == ",addTask" or __aArgs[0] == "!addTask":
	#	return(cmd.__addTasks())
	#elif __aArgs[0] == ",delTask" or __aArgs[0] == "!delTask":
	#	return(cmd.__delTasks(__aArgs[1]))
	elif __aArgs[0] == ",bofh" or __aArgs[0] == "!bofh":
		return(cmd.__getBOFH(fBOFH))
	elif __aArgs[0] == ",meme" or __aArgs[0] == "!meme":
		return(cmd.__meme(__aArgs[1], dMeme))

if bTasks:
	botDatabase.taskScheduler()
else:
	a=__checkMessage()
	if a and not a == "":
		print(a)
