import sqlite3
from api_calls import *

DB_FILE = "wordGame.db"

# Create the database file
def dbsetup():
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	# with date
	# c.execute("DROP TABLE IF EXISTS words")
	# command = "CREATE TABLE cache (word TEXT PRIMARY KEY, Date TEXT NOT NULL, Definition TEXT NOT NULL, Synonyms TEXT NOT NULL, WikipediaLinks TEXT NOT NULL)"
	# c.execute(command)

	c.execute("DROP TABLE IF EXISTS words")
	command = "CREATE TABLE cache (word TEXT PRIMARY KEY, Definition TEXT NOT NULL, Synonyms TEXT NOT NULL, WikipediaLinks TEXT NOT NULL)"
	c.execute(command)

	c.execute ("DROP TABLE IF EXISTS users")
	command = "CREATE TABLE users (userID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, passowrd TEXT NOT NULL)"
	c.execute(command)

	c.execute("DROP TABLE IF EXISTS leaderboar")
	command = "CREATE TABLE leaderboard (hash TEXT PRIMARY KEY, word1 TEXT NOT NULL, word2 TEXT NOT NULL, targetWord TEXT NOT NULL, scores TEXT NOT NULL)"
	c.execute(command)

	db.commit()
	db.close()

# gets words from api calls and puts them into the database
def insert_words(searched):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	for word in searched:
		# get the definition
		definition = get_word_definition(word)
		# get the synonyms
		synonyms = get_word_synonyms(word)
		# get the wikipedia links
		wikipedia_links = get_wikipedia_links(word)

		# get the date
		# date = get_date()

		# with date
		# command = "INSERT INTO cache (word, Date, Definition, Synonyms, WikipediaLinks) VALUES (?, ?, ?, ?, ?)"
		# c.execute(command, (word, date, definition, synonyms, wikipedia_links))

		command = "INSERT INTO cache (word, Definition, Synonyms, WikipediaLinks) VALUES (?, ?, ?, ?, ?)"
		c.execute(command, (word, definition, synonyms, wikipedia_links))

	db.commit()
	db.close()

# checks if a word already exists in the cache
def check_word_exists(word):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	command = "SELECT word FROM cache WHERE word = ?"
	c.execute(command, (word,))
	result = c.fetchone()

	db.close()

	if result is None:
		return False
	else:
		return True
