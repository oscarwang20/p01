import sqlite3
from api_calls import *

def get_db():
    return sqlite3.connect("wordGame.db")

# Create the database file
def dbsetup():
    db = get_db()
    c = db.cursor()

    # with date
    # c.execute("DROP TABLE IF EXISTS words")
    # command = "CREATE TABLE cache (word TEXT PRIMARY KEY, Date TEXT NOT NULL, Definition TEXT NOT NULL, Synonyms TEXT NOT NULL, WikipediaLinks TEXT NOT NULL)"
    # c.execute(command)

    c.execute("DROP TABLE IF EXISTS cache")
    command = "CREATE TABLE cache (word TEXT PRIMARY KEY, definition TEXT NOT NULL, synonyms TEXT NOT NULL, wikipediaLinks TEXT NOT NULL)"
    c.execute(command)

    c.execute ("DROP TABLE IF EXISTS users")
    command = "CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL)"
    c.execute(command)

    c.execute("DROP TABLE IF EXISTS leaderboard")
    command = "CREATE TABLE leaderboard (hash TEXT PRIMARY KEY, word1 TEXT NOT NULL, word2 TEXT NOT NULL, targetWord TEXT NOT NULL, scores TEXT NOT NULL)"
    c.execute(command)

    db.commit()
    db.close()

# gets words from api calls and puts them into the database
def insert_words(searched):
    db = get_db()
    c = db.cursor()

    for word in searched:
        # get the definition
        definition = get_word_definition(word)
        # get the synonyms
        synonyms = get_word_thesaurus_raw(word)
        # get the wikipedia links
        wikipedia_links = get_wikipedia_links(word)

        # get the date
        # date = get_date()

        # with date
        # command = "INSERT INTO cache (word, Date, Definition, Synonyms, WikipediaLinks) VALUES (?, ?, ?, ?, ?)"
        # c.execute(command, (word, date, definition, synonyms, wikipedia_links))

        command = "INSERT INTO cache (word, definition, synonyms, wikipediaLinks) VALUES (?, ?, ?, ?)"
        c.execute(command, (word, definition, synonyms, wikipedia_links))

    db.commit()
    db.close()

def check_item_exists(table, field, item):
    db = get_db()
    c = db.cursor()

    command = f"SELECT {field} from {table} WHERE {field} = ?"
    c.execute(command, (item,))
    result = c.fetchone()
    print("result is " + str(result))

    db.close()

    return result is not None

# puts the username and password into the users table
def insert_user(username, password):
    db = get_db()
    c = db.cursor()

    command = "INSERT INTO users VALUES (?, ?)"
    c.execute(command, (username, password))

    db.close()

# checks if a word already exists in the cache
def check_word_exists(word):
    return check_item_exists("cache", "word", word)

# checks if a username already exists in users
def check_user_exists(username):
    return check_item_exists("users", "username", username)
