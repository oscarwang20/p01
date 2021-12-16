import json
import sqlite3
from api_calls import *

def debug(statement:str, DEBUG=True):
	if DEBUG:
		print(statement)

# Create the database file
class Cache_manager:
	def __init__(self, db_file:str = 'words_cache.db'):
		'''Sets up requisite db file'''
		self.db_file = db_file
		self.db = sqlite3.connect(self.db_file)
		self.c = self.db.cursor()

		command = "CREATE TABLE IF NOT EXISTS cache (word TEXT PRIMARY KEY, Definition TEXT NOT NULL, Synonyms TEXT NOT NULL, WikipediaLinks TEXT NOT NULL)"
		self.c.execute(command)

		command = "CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, passowrd TEXT NOT NULL)"
		self.c.execute(command)

		command = "CREATE TABLE IF NOT EXISTS leaderboard (hash TEXT PRIMARY KEY, word1 TEXT NOT NULL, word2 TEXT NOT NULL, targetWord TEXT NOT NULL, scores TEXT NOT NULL)"
		self.c.execute(command)
		self.db.commit()

	def insert_word(self, word:str):
		'''Inserts the word into the cache from api calls so no api calls need to be made in the future.

		Keyword arguments:
		word -- the word to be cached'''

		debug("Caching: " + word)

		definition = get_word_definition(word)
		synonyms = json.dumps(get_word_synonyms(word)) #turns output into a json for sqlite
		wikipedia_links = json.dumps(get_wikipedia_links(word))#turns wikipedia output into json for SQLite

		#debug("Def: " + definition)
		#debug("Synonyms: " + synonyms)
		debug("Wikipedia: " + wikipedia_links)

		command = "INSERT INTO cache (word, Definition, Synonyms, WikipediaLinks) VALUES (?, ?, ?, ?)"
		self.c.execute(command, (word, definition, synonyms, wikipedia_links))

		self.db.commit()

	def is_cached(self, word:str) -> bool:
		command = "SELECT word FROM cache WHERE word = ?"
		self.c.execute(command, (word,))
		result = self.c.fetchone()

		return result is not None

	def retrieve(self, word:str) -> tuple:
		'''Gets all the information for a given word'''
		self.c.execute("SELECT * FROM cache WHERE word = ?", (word,))

		return tuple(self.c.fetchall()[0]) #gets cursor selected items and then tuples and returns it. Selects the first row as we're only selecting 1 row, not multiple.

	def define(self, word:str) -> str:
		'''Returns the definition for a given word'''
		self.c.execute("SELECT Definition FROM cache WHERE word = ?", (word,))

		return self.c.fetchall()[0][0] #gets the cursor items and then extracts the string from the tuple inside a list.

	def synonyms(self, word:str) -> list:
		'''returns the synonyms for a given word'''
		self.c.execute("SELECT Synonyms FROM cache WHERE word = ?", (word,))
		#extracts and returns JSON string
		JSON = self.c.fetchall()[0][0]
		JSON = json.loads(JSON)

		return JSON

	def wikipedia_links(self, word:str) -> list:
		'''returns the wikipedia links for a given word'''
		self.c.execute("SELECT Synonyms FROM cache WHERE word = ?", (word,))
		#extracts and returns JSON string then converts to python classes.
		JSON = self.c.fetchall()[0][0]
		JSON = json.loads(JSON)

		return JSON

	def __del__(self):
		'''Saves everything before destructing'''
		self.db.commit()
		self.db.close()
