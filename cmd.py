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

import iptools
import itertools
import re
import psutil
import sys
import os
import pycurl
import random
import cStringIO
from datetime import timedelta
from optparse import OptionParser
from StringIO import StringIO
from uptime import uptime
from db import BotTasks
botDatabase = BotTasks()

def __readTextfile(__sFileName):
	__buffer = []
	__fTxtFile = open(__sFileName, "r")
	for line in __fTxtFile:
		__buffer.append(line)
	return (__buffer)

def __checkSallutation(__sMessage, __sFileName):
	__lFileContent = __readTextfile(__sFileName)
	for __sElement in __lFileContent:
		if __sMessage.lower() == __sElement.lower()[:-1]:
			return True

def __getSallutation(__sFileName):
	return random.choice(__readTextfile(__sFileName))

def __getHttpTitle(sMessage):
	__tContent = __getHttpContent(sMessage)
	__sResult = ""
	for __sElement in __tContent:
		__sResult += re.search('<title>(.*)</title>',__sElement, re.DOTALL,).group(1) + "\n"
		__sResult += "--------------------\n"
	return (__sResult[:-21])

def __checkURL(sMessage):
	__tMatchObj = re.findall("(https?://\S+)", sMessage, re.DOTALL)
	if __tMatchObj:
		return True

def __getBOFH(__sFilename):
	return random.choice(__readTextfile(__sFilename))

def __listCommands(__sName):
	return (' ; '.join(botDatabase.getMemberCommandsByMemberNames(__sName)))

def __hint(__sMessage):
	__aArgs = __sMessage.split(" ")
	__lCommands = botDatabase.getCommands()
	if len(__aArgs) > 1 and  __aArgs[1] != "":
		for s in __lCommands:
			if __aArgs[1] == s[0]:
				return (str(botDatabase.getHintByCommand(__sMessage.split(" ")[1])))
	else:
		return ("Keine zulaessigen Parameter angegeben!")

def __getDiskUsage():
	return (str(round(psutil.disk_usage('/').percent))+"%")

def __getUsedMem():
	return str((psutil.used_phymem() / 1024**2))+" MB used ..."

def __httpPing(url, reverseChecking=1):
  buf = buff = StringIO()
  c = pycurl.Curl()
  c.setopt(pycurl.CONNECTTIMEOUT, 1)
  c.setopt(pycurl.TIMEOUT, 1)
  c.setopt(pycurl.NOSIGNAL, 1)
  c.setopt(pycurl.FOLLOWLOCATION, 1)
  c.setopt(pycurl.URL, url)
  c.setopt(pycurl.SSL_VERIFYPEER, 0)
  c.setopt(pycurl.SSL_VERIFYHOST, 0)
  c.setopt(pycurl.WRITEFUNCTION, buff.write)
  c.setopt(pycurl.HEADERFUNCTION, buf.write)
  c.setopt(pycurl.HTTPGET, 1)
  c.perform()
  c.close() 
  retstring = buf.getvalue()
  if retstring and 'Status: 200 OK' in retstring:
    return url+" liefert Status OK"
  else:
    return url+" liefert keinen Status OK"

def __getHttpContent (sMessage):
	__tMatchObj = re.findall("(https?://\S+)", sMessage)
	__tContent =[]
	for __sElement in __tMatchObj:
		storage = StringIO()
		c = pycurl.Curl()
		c.setopt(c.URL, __sElement)
		c.setopt(c.WRITEFUNCTION, storage.write)
		c.setopt(pycurl.FOLLOWLOCATION, 1)
		c.perform()
		c.close()
		__tContent.append(storage.getvalue())
	return (__tContent)

def __ping(__sIP):
	__sPing = os.system("ping -c1 " + __sIP + " > /dev/null")
	if __sPing == 0:
		return (__sIP + " is up")
	if __sPing == 1 or __sPing == 256:
		return (__sIP + " is down")
	if __sPing == 2:
		return ("")

def __getUptime():
	__sSeconds = uptime()
	return str(timedelta(seconds=__sSeconds))

def __getLoad():
	return (os.getloadavg())

def __getUserID(__sName):
	__tMembers = botDatabase.getMembers()
	for __part in __tMembers:
		if __sName in __part:
			return (str(__part).split(",")[0][1:])

def __showTasks(__sName):
	__sUserID = __getUserID(__sName)
	__tTasks = botDatabase.getTasksByMemberId(__sUserID)
	__sOutput = ""
	for __part in __tTasks:
		if not __part[3] == None:
			__sOutput += str(__part[2]) + str(__part[3])[:19] + "\n"
	return (__sOutput[:-1])

#def __addTask():
	

def __delTask(__iTaskID):
	botDatabase.delTask(__iTaskID)
	return ("Task mit der ID " + str(__iTaskID) + " wurde geloescht")

def __meme(__sMeme, __dMeme):
	__tMemes = os.listdir(__dMeme)
	__lResults = []
	for __part in __tMemes:
		if __sMeme in __part:
			__lResults.append(str(__part))
	if __lResults:
		__iRnd = random.randint(1,len(__lResults))
		return ("{{photo}}"+__dMeme + str(__lResults[__iRnd]))
	else:
		return ("Kein passendes Meme gefunden")

def __correctTim(__sMessage, __fSmiley):
	__iRnd = random.randint(1,10)
	__tSmileys = __readTextfile(__fSmiley)
	if __iRnd % 3 == 0:
		for __sPart in __tSmileys:
			if __sMessage == str(__sPart).split("#")[0]:
				return (str(__sPart).split("#")[1][:-1])
