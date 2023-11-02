from flask import session
from flask import Flask, request, redirect, url_for, render_template, make_response, abort, jsonify
from markupsafe import escape
import IPython

app = Flask(__name__)


@app.route("/")
def home():
    return "Oh elo, Harry! Not getting up to much trouble now are yeh?"


@app.route("/<nope>")
def redirect_all(nope):
    return redirect(url_for('home'))


@app.route('/history')
def history():
    return "Oh, elo Harry. Soon you'll be able to see all your spell enhancements in 'ere. Do come back again soon"


@app.route('/api')
def api():
    return [1, 2, 3]


@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('404.html'), 404)
    resp.set_cookie('secret-cookie', 'nomnom')
    return resp
    return "Oh dear, Harry, looks like that spell was no more than a rumour", 404


# Set the secret key to some random bytes. Keep this really secret!
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# @app.route('/')
# def index():
#     if 'username' in session:
#         return f'Logged in as {session["username"]}'
#     return 'You are not logged in'


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#         <form method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''


# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))


"""
TESTING
"""

with app.test_request_context('/history', method='GET'):
    assert request.path == '/history'
