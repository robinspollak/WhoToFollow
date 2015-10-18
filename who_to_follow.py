from flask import Flask, url_for, render_template,request
from wtforms import Form, BooleanField, TextField, PasswordField, validators

app = Flask(__name__)



@app.route('/')
def index():
	return render_template("index.html")

@app.route('/results',methods=['POST'])
def backend():
	hashtags = request.form
	print(hashtags)
	return "hi"



if __name__=='__main__':
	app.run(debug=True)