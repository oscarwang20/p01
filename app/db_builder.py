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

    command = "CREATE TABLE IF NOT EXISTS cache (word TEXT PRIMARY KEY, definition TEXT NOT NULL, synonyms TEXT NOT NULL, wikipediaLinks TEXT NOT NULL)"
    c.execute(command)

    command = "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL, points INTEGER)"
    c.execute(command)

    command = "CREATE TABLE IF NOT EXISTS leaderboard (hash TEXT PRIMARY KEY, word1 TEXT NOT NULL, word2 TEXT NOT NULL, targetWord TEXT NOT NULL, scores TEXT NOT NULL)"
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

def set_data(command, args):
    db = get_db()
    c = db.cursor()

    c.execute(command, args)

    db.commit()
    db.close()

def get_data(command, args):
    db = get_db()
    c = db.cursor()

    c.execute(command, args)
    result = c.fetchone()

    db.close()

    return result

# puts the username and password into the users table
def insert_user(username, password):
    set_data("INSERT INTO users VALUES (?, ?, ?)", (username, password, 0))

# checks if a word already exists in the cache
def check_word_exists(word):
    return get_data("SELECT 1 FROM cache WHERE word = ?", (word,)) != None

# checks if a username already exists in users
def check_user_exists(username):
    return get_data("SELECT 1 FROM users WHERE username = ?", (username,)) != None

def check_password_matches(username, password):
    correct_password = get_data("SELECT password FROM users WHERE username = ?", (username,))
    return correct_password and password == correct_password[0]

def get_points(username):
    return get_data("SELECT points FROM users WHERE username = ?", (username,))[0]

def add_points(username, new_points):
    points = get_points(username) + new_points
    set_data("UPDATE users SET points = ? WHERE username = ?", (points, username))