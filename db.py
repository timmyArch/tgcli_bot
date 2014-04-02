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
		try:
			if not type(user) is tuple:
				raise TypeError('only tuples!!111ELF') 
			cur = BotDatabase.__con.cursor()
			cur.execute("INSERT INTO members (number, name) VALUES (%s,%s)", user)
			BotDatabase.__con.commit()	
			return True

		except psycopg2.DatabaseError, e: 	
			if BotDatabase.__con:
				BotDatabase.__con.rollback()
			return False

	def removeMember(self, user):
		try:
			cur = BotDatabase.__con.cursor()
			if type(user) is int or (type(user) is str and user.isdigit()):
				cur.execute("DELETE FROM members_commands WHERE members_id = %s", (str(user),)) 
				cur.execute("DELETE FROM members WHERE members_id = %s ", (str(user),))
			else:
				cur.execute("DELETE FROM members_commands WHERE members_id = ( " +
						"SELECT members_id FROM members WHERE name = %s " + 
					")", (str(user),))
				cur.execute("DELETE FROM members WHERE name = %s ", (user,))
			BotDatabase.__con.commit()	
			return True
		
		except psycopg2.DatabaseError, e: 	
			if BotDatabase.__con:
				BotDatabase.__con.rollback()
			return False

	def getCommands(self):
		try:
			cur = BotDatabase.__con.cursor()
			cur.execute("SELECT * FROM commands")
			return cur.fetchall()

		except psycopg2.DatabaseError, e: 	
			if BotDatabase.__con:
				BotDatabase.__con.rollback()
			return False

	def getTasksByUserId(self,user_id):
		try:
			cur = BotDatabase.__con.cursor()
			cur.execute("SELECT * FROM tasks WHERE members_id = %s ", (user_id,))
			return cur.fetchall()
			
		except psycopg2.DatabaseError, e: 	
			if BotDatabase.__con:
				BotDatabase.__con.rollback()
			return False

	def getUserCommandsByUserId(self,user_id):
		try:
			cur = BotDatabase.__con.cursor()
			retTuple = tuple()
			cur.execute(
				"SELECT command " + 
				"FROM commands " + 
				"WHERE commands_id IN ( " + 
					"SELECT commands_id FROM members_commands WHERE members_id = %s " + 
				")", (user_id,)
			)
			result = cur.fetchall()
			if not result:
				return False
			for i in result:
				retTuple += (i[0],)
			return retTuple
			
		except psycopg2.DatabaseError, e: 	
			if BotDatabase.__con:
				BotDatabase.__con.rollback()
			return False

	def getUserCommandsByUserNames(self,user_names):
		try:
			if type(user_names) is str:
				user_names = (user_names,)
			elif not type(user_names) is tuple:
				raise TypeError('tuple , Monkey !!')
			retDict = dict()
			cur = BotDatabase.__con.cursor()
			for i in user_names:
				cur.execute("SELECT members_id FROM members WHERE name = %s ", (i,))
				retDict[i[0]] = self.getUserCommandsByUserId(cur.fetchone())
			return retDict
		
		except psycopg2.DatabaseError, e: 	
			if BotDatabase.__con:
				BotDatabase.__con.rollback()
			return False
	
	def getUsersWithCommands(self):
		try:	
			buf = tuple()
			cur = BotDatabase.__con.cursor()
			cur.execute("SELECT name FROM members")
			result = cur.fetchall()
			if not result:
				return False
			for i in result:
				 buf += (i,)
			return self.getUserCommandsByUserNames(buf)
		
		except psycopg2.DatabaseError, e: 	
			if BotDatabase.__con:
				BotDatabase.__con.rollback()
			return False


