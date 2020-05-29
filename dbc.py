from data import Session, User, Status, Role, Post, Activity
from functools import wraps
from flask import Flask, render_template, Response, request, redirect, send_from_directory, url_for, Response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_login import LoginManager, login_required, login_user, current_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "kek"
session = Session(autocommit=True, autoflush=True)
app.app_context()
login_manager = LoginManager()
login_manager.init_app(app)

class LoginForm(FlaskForm):
	nickname = StringField('nickname')
	password = PasswordField('password')
	submit = SubmitField('submit')


@login_manager.user_loader
def load_user(id):
	return session.query(User).filter(User.id == id).first()

# returns user obj
@app.route('/api/get/user/<nickname>')
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
			login_user(user)
			return redirect("/index")
		else:
			redirect(login)
	else:
		return render_template('authorization.html')

@app.route('/', methods =["GET"])
@app.route('/index', methods =["GET"])
@app.errorhandler(404)
def index():
	posts = get_post()
	return render_template("title.html", posts=posts)

@app.route('/api/post/post', methods = ['POST','GET'])
@login_required
def post():
	if request.method == 'POST':
		new_post = Post(current_user,request.form['text'])
		print(new_post.body)
		session.add(new_post)
		return redirect("/index")
	return render_template('post.html')

def get_post():
	return session.query(Post).order_by(Post.date).limit(5).all()


'''
@app.route('/login', methods=['POST', 'GET'])
@login_required
def test():
	return Response(), 401
'''

app.run(debug=True)
