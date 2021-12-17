from flask import Flask, render_template, request, url_for, session
from get_links import *
import db_builder

app = Flask(__name__)
app.secret_key = "a very ADVENTageous key"

# Landing page for new users and logged out users
@app.route('/')
def index():
	return render_template(
		'index.html'
	)

# Redirection to the login page and handles the login
@app.route('/login')
def display_login():
	method = request.method

	# Viewing the login page
	if method == 'GET':
		return render_template(
			'login.html'
		)
	
	# User authentication and session creation
	elif method == 'POST':
		username = request.form['username']
		password = request.form['password']
		

# Redirection to the registration page
@app.route('/register')
def display_register():
	return render_template(
		'register.html'
	)

# Resister a new user and redirect successful registers to the main page
@app.route('/create_new_user', methods=['GET', 'POST'])
def register():
	return render_template(
		'base.html'
	)

# Logout the user and redirect to the main page
@app.route('/logout')
def display_logout():
	return render_template(
		'index.html'
	)

# Initial game page
@app.route('/game', methods=['GET', 'POST'])
def new_game():
	session['turns'] = 0
	session['words'] = list(get_random_word())

	return render_template(
		'new_game.html'
	)

# Subsequent game pages with the current word
@app.route('/game/<word>', methods=['GET'])
def display_word_page(word):
	session['turns'] += 1
	session['words'].append(word)

	return render_template(
		'word_page.html',
		word = word,
		definition = get_definition(word),
		synonyms = get_synonyms(word),
		links = get_wikipedia_links(word)
	)
# Handles errors when a user visits a page they're not supposed to
@app.errorhandler(404)
def page_not_found(e):
	return render_template(
		'404.html'
	), 404

if __name__ == '__main__': #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
