from flask import Flask, render_template, request, url_for
from listify import *

@app.route('/login', methods=['GET', 'POST'])
def display_login():
	return render_template(
		'login.html'
	)
