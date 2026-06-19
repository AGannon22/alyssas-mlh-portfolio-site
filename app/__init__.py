import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    hobbies = {"Cooking": "img1",
               "Baking": "img2",
               "Gaming": "img3",
               "Drawing": "img4"}
    #eee
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))

@app.route('/map')
def map():
    return render_template('map.html', title="Map", url=os.getenv("URL"))