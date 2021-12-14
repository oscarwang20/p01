from flask import Flask, render_template, request, url_for
from get_links import *

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def display_login():
	return render_template(
		'login.html'
	)

@app.route('/game', methods=['GET', 'POST'])
def new_game():
	return render_template(
		'new_game.html',

	)

@app.route('/game/<word>', methods=['GET'])
def display_word_page(word):
	return render_template(
		'word_page.html',
		word = word,
		definition = get_definition(word),
		synonyms = get_synonyms(word),
		links = get_wikipedia_links(word)
	)

if __name__ == '__main__': #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
