#!/usr/bin/env python
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

import psycopg2
import sys
import ConfigParser

class BotDatabase(object):
	
	__database=	""
	__password=	""
	__user=			""
	__host=			""
	__con = 		None

	def __init__(self):
		self.__readConfig()
		self._connect()
			
	def __readConfig(self):
		try:
			config = ConfigParser.RawConfigParser()
			config.read('bot.cfg')
			BotDatabase.__database=config.get('Database','db_name')
			BotDatabase.__password=config.get('Database','password')
			BotDatabase.__user		=config.get('Database','user')
			BotDatabase.__host		=config.get('Database','host')
		except:
			raise 'please check bot.cfg'

	def _connect(self):
		if not BotDatabase.__con:
			BotDatabase.__con = psycopg2.connect(
				database=BotDatabase.__database, 
				user=BotDatabase.__user, 
				password=BotDatabase.__password,
				host=BotDatabase.__host)

	def addMember(self,user):
		if not type(user) is tuple:
			raise TypeError('user must be a tuple (number, name)') 
		return self._insert_del("INSERT INTO members (number, name) VALUES (%s,%s)", user)

	def removeMember(self, user):
		if type(user) is int or (type(user) is str and user.isdigit()):
			a = self._insert_del("DELETE FROM members_commands WHERE members_id = %s", (user,)) 
			b = self._insert_del("DELETE FROM members WHERE members_id = %s ", (user,))
		else:
			a = self._insert_del("DELETE FROM members_commands WHERE members_id = ( " +
					"SELECT members_id FROM members WHERE name = %s " + 
				")", (user,))
			b = self._insert_del("DELETE FROM members WHERE name = %s ", (user,))
		return (False, True)[bool(a and b)]

	def addMemberCommandByMemberId(self, user_id, command):
		if not type(command) is int and not (type(command) is str or command.isdigit()):
			command = self._select("SELECT commands_id FROM commands WHERE command = %s LIMIT 1" , (command,) , True)
		return self._insert_del("INSERT INTO members_commands (members_id, commands_id) VALUES ( %s , %s )", 
			(user_id, command))

	def addMemberCommandByMemberName(self, user_name, command):
		user_name = self._select("SELECT members_id FROM members " +
			"WHERE name = %s LIMIT 1" , (user_name,), True)
		return(False, True)[bool(self.addMemberCommandByMemberId(user_name,command))]

	def getCommands(self):
		return self._select("SELECT command FROM commands",False,False)
	
	def addCommand(self,dataset):
		if type(dataset) is tuple and len(dataset) == 3:
			return self._insert_del("INSERT INTO commands (command, short_hint, description) VALUES (%s,%s,%s)", dataset)
		else:
			raise TypeError('tuple needed (command, short_hint, descrition)')
	
	def removeCommand(self,command):
		if type(command) is int or (type(command) is str and command.isdigit()):
			a = self._insert_del("DELETE FROM members_commands WHERE commands_id = %s", (command,)) 
			b = self._insert_del("DELETE FROM commands WHERE commands_id = %s ", (command,))
		else:
			a = self._insert_del("DELETE FROM members_commands WHERE commands_id = ( " +
					"SELECT commands_id FROM commands WHERE command = %s " + 
				")", (command,))
			b = self._insert_del("DELETE FROM commands WHERE command = %s ", (command,))
		return (False, True)[bool(a and b)]

	def getHintByCommand(self,command):
		buf = self._select("SELECT short_hint FROM commands WHERE command = %s ", (command,), True)
		return (False , buf[0])[bool(buf[0])]
			
	def getDescriptionByCommand(self,command):
		buf = self._select("SELECT description FROM commands WHERE command = %s ", (command,),True)
		return (False , buf[0])[bool(buf[0])]

	def getTasksByMemberId(self,user_id):
		return self._select("SELECT * FROM tasks WHERE members_id = %s ", (user_id,), False)

	def getMembers(self):
		return self._select("SELECT * FROM members", False, False)

	def getMemberCommandsByMemberId(self,user_id):
		retTuple = tuple()
		result = self._select("SELECT command FROM commands WHERE commands_id IN ( " + 
				"SELECT commands_id FROM members_commands WHERE members_id = %s " + 
			")", (user_id,) , False)
		if not result:
			return False
		for i in result:
			retTuple += (i[0],)
		return retTuple

	def getMemberCommandsByMemberNames(self,user_names):
		if type(user_names) is str:
			user_names = (user_names,)
		elif not type(user_names) is tuple:
			raise TypeError('tuple , Monkey !!')
		retDict = dict()
		for i in user_names:
			res = self._select("SELECT members_id FROM members WHERE name = %s ", (i,), True)
			buf=self.getMemberCommandsByMemberId(res)
			if buf:
				retDict[i[0]] = buf
		return retDict
		
	def getMembersWithCommands(self):
		buf = tuple()
		result = self._select("SELECT name FROM members", False, False)
		if not result:
			return False
		for i in result:
			 buf += (i,)
		return self.getMemberCommandsByMemberNames(buf)

	def _select (self, query, values, onlyOneResult ):
		try:
			cur = BotDatabase.__con.cursor()
			if values:
				cur.execute(query, values)
			else:
				cur.execute(query) 
			if onlyOneResult:
				return cur.fetchone()
			else:
				return cur.fetchall()
	
		except psycopg2.DatabaseError, e: 	
			if BotDatabase.__con:
				BotDatabase.__con.rollback()
			return False

	def _insert_del(self, query , values):
		try:
			cur = BotDatabase.__con.cursor()
			cur.execute(query, values) 
			result=BotDatabase.__con.commit()	
			return True
	
		except psycopg2.DatabaseError, e: 	
			if BotDatabase.__con:
				BotDatabase.__con.rollback()
			return False
						

