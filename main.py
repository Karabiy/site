from flask import Flask, render_template, Response, request, redirect, send_from_directory, url_for, Response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField



app = Flask(__name__)
app.config["SECRET_KEY"] = 'key'

entity1 = {"name":"John","surname":"Cage","details":"programmer"}
entity2 =  {"name":"Lina","surname":"Cage","details":"programmer"}
entities = [entity1,entity2]

class userForm(FlaskForm):
	name = StringField('name')
	surname = StringField('surname')
	details = StringField('details')
	
def get_entity(name):
	for i in entities:
		if(i['name'] == name):
			return i
	return None

def change_entity(name, data):
	for i in range(len(entities)):
		if(entities[i]['name'] == name):
			entities[i] = data
	print(entities)

@app.route('/api/<action>', methods = ['POST', 'GET'])
def controller_handler(action):
	if request.method == 'GET':
		if action == "all":
			return str(entities)
		else:
			entity = get_entity(action)
			if entity:
				return render_template("get_data.html",entity=entity,action=action)
			else:
				return ("this is 404, entity with the name: " + str(action) + " - is not found. The next names can be used: " + str([i['name'] for i in entities])), 404


@app.route('/api/post/<action>', methods = ['POST'])
def controller_handler_post(action):
	form = userForm()
	print(form.name.data)
	entity = {'name':form.name.data, 'surname': form.surname.data,  'details': form.details.data}
	print(entity)
	change_entity(action,entity)
	return Response(), 200

@app.errorhandler(404)
def error_404(e):
	return str(e), 404


app.run(debug = True)
