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
		self.db = sqlite3.connect(DB_FILE)
		self.c = db.cursor()

		command = "CREATE TABLE IF NOT EXISTS cache (word TEXT PRIMARY KEY, Definition TEXT NOT NULL, Synonyms TEXT NOT NULL, WikipediaLinks TEXT NOT NULL)"
		c.execute(command)

		command = "CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, passowrd TEXT NOT NULL)"
		c.execute(command)

		command = "CREATE TABLE IF NOT EXISTS leaderboard (hash TEXT PRIMARY KEY, word1 TEXT NOT NULL, word2 TEXT NOT NULL, targetWord TEXT NOT NULL, scores TEXT NOT NULL)"
		c.execute(command)
		self.db.commit()

	def insert_word(self, word:str):
		'''Inserts the word into the cache from api calls so no api calls need to be made in the future.

		Keyword arguments:
		word -- the word to be cached'''

		debug("Caching: " + word)

		definition = get_word_definition(word)
		synonyms = get_word_synonyms(word)
		wikipedia_links = get_wikipedia_links(word)

		command = "INSERT INTO cache (word, Definition, Synonyms, WikipediaLinks) VALUES (?, ?, ?, ?, ?)"
		self.c.execute(command, (word, definition, synonyms, wikipedia_links))

		self.db.commit()

	def check_cache(word:str) -> bool:
		command = "SELECT word FROM cache WHERE word = ?"
		self.c.execute(command, (word,))
		result = self.c.fetchone()

		return result is not None

	def __del__(self):
		'''Saves everything before destructing'''
		self.db.commit()
		self.db.close()
