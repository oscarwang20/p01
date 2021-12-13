from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def display_login():
    return render_template(
        'login.html'
    )

if __name__ == "__main__":
    app.run(debug=True)



