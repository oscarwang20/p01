from flask import Flask, render_template, request, url_for, session, redirect
from get_links import *
import db_builder

app = Flask(__name__)
app.secret_key = "a very ADVENTageous key"

# Landing page for new users and logged out users
@app.route('/')
def index():
	db_builder.dbsetup()
	logged_in = 'username' in session
	points = -1
	if logged_in:
		points = db_builder.get_points(session['username'])
	return render_template(
		'index.html',
		logged_in = logged_in,
		points = points
	)

# Redirection to the login page and handles the login
@app.route('/login', methods=['GET', 'POST'])
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
		if db_builder.check_password_matches(username, password):
			session['username'] = username
			return redirect(url_for('index'))
		else:
			return render_template(
				'login.html',
				fail = True	
			)

# Redirection to the registration page and handles the registration
@app.route('/register', methods=['GET', 'POST'])
def display_register():
	method = request.method

	# Viewing the registration page
	if method == 'GET':
		return render_template(
			'register.html',
			pass_match = True,
			unique_name = True
		)

	# User registration and session creation
	elif method == 'POST':
		username = request.form['username']
		password = request.form['password']
		confirm = request.form['confirm']

		unique_name = not db_builder.check_user_exists(username)
		password_match = password == confirm

		if password_match and unique_name:
			db_builder.insert_user(username, password)
			return redirect(url_for('display_login'))
		else:
			return render_template(
				'register.html',
				pass_match = password_match,
				unique_name = unique_name
			)

# Logout the user and redirect to the main page
@app.route('/logout')
def display_logout():
	session.pop('username')
	return redirect('/')

@app.route('/game', methods=['GET'])
def display_new_word_page():
	word_set = generate_start_end()
	word = word_set[0]
	target = word_set[1]
#	starting_options = get_random_words(3)

	session['turns'] = 0
	session['words'] = list()
	session['target'] = target

	return render_template(
		'word_page.html',
		word = word,
		target = target,
		target_definition = get_definition(target),
		definition = get_definition(word),
		synonyms = get_synonyms(word),
		links = get_wikipedia_links(word),
		turn_number = 1
	)

# Subsequent game pages with the current word
@app.route('/game/<word>', methods=['GET'])
def display_word_page(word):
	if word == session['target']:
		points = int(100000 / session['turns'])
		db_builder.add_points(session['username'], points)
		return render_template(
			'result.html',
			turn_number = session['turns'],
			points = points
		)
	else:
		session['turns'] += 1
		session['words'].append(word)

		return render_template(
			'word_page.html',
			word = word,
			target = session['target'],
			target_definition = get_definition(session['target']),
			definition = get_definition(word),
			synonyms = get_synonyms(word),
			links = get_wikipedia_links(word),
			turn_number = session['turns'] + 1
		)

@app.route('/leaderboard')
def display_leaderboard():
	return render_template(
		'leaderboard.html',
		top_100 = [
			{'name': 'user', 'points': 123456789, 'ranking': 1},
			{'name': 'other', 'points': 12345678, 'ranking': 2}
		]
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
	app.run(host="localhost", port=8000, debug=True)
