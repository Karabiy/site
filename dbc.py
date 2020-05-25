from laba4.data import Session, User, Status, Role, Post, Activity
from functools import wraps
from flask import Flask, render_template, Response, request, redirect, send_from_directory, url_for, Response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

app = Flask(__name__)
app.config["SECRET_KEY"] = "kek"
session = Session(autocommit=True, autoflush=True)
app.app_context()

class LoginForm(FlaskForm):
	nickname = StringField('nickname')
	password = PasswordField('password')
	submit = SubmitField('submit')

'''
def authorization_hadlder(func):
	def wrapper(*args, **kwargs):
		print("authorized", user.nickname)
		func(*args, **kwargs)
	nickname = "s"
	password = "p"
	user = get_user(nickname)
	if validate_user(user, password):
		return authorization_hadlder
	
	else:
		return Response(), 401
'''

# returns user obj
def get_user(nickname):
	return session.query(User).filter(User.nickname == nickname).first()


# validates user credentials
def validate_user(user, password):
	if user:
		return user.password_check(password)
	else:
		return False


# to login
@app.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		nickname = form.nickname.data
		password = form.password.data
		user = get_user(nickname)
		if validate_user(user, password):
			status = user.login("127.0.0.1")
			request.headers['username'] = nickname
			request.headers['password'] = password
			return "LOGGED" + str(status)
		else:
			print("wrong pass")
	else:
		return render_template('authorization.html')

'''
@app.route('/login', methods=['POST', 'GET'])
@authorization_hadlder
def test():
	return Response(), 401
'''

app.run(debug=True)
