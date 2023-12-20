from flask import Flask, render_template, request
from main import enter_prompt
import re

app = Flask(__name__)

response = ""

@app.route('/')
def index():
	#response = enter_prompt(artist, artist02, question)
	return render_template("index.html", bot_response = response)

@app.route('/', methods = ['POST'])
def index_post():
	f_artist = request.form['first_artist']
	s_artist = request.form['second_artist']
	question = request.form['question']
	
	response = enter_prompt(f_artist, s_artist, question)
	matches = re.findall(r'\((.*?)\)', response)

	#return render_template("index.html", bot_response = response, image_Link = matches[0])
	return render_template("index.html", bot_response = response)