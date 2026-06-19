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
    hobbies = [
        {"name": "Cooking", "img": "img1.jpg","description": "I only recently started cooking since I started college, but I really enjoy finding new recipes to try out! My favorite foods to make right now are carbonara and porkchops with baked potatoes!"},
        {"name": "Baking", "img": "img2.jpg","description": "I've been baking for longer than I can remember. My grandmother taught me how to make chocolate chip cookies when I was a kid and I've been baking ever since. My favorite thing to bake are my chocolate chip and sugar cookie brookies!"},
        {"name": "Gaming", "img": "img3.jpg","description": "My gaming interests started in second grade with Pokemon and Tomodachi Life on the 3DS. I still play both to this day, but I've also gotten into Valorant, Stardew Valley, Siege, and more!"},
        {"name": "Drawing", "img": "img4.jpg","description": "I've been drawing literally forever. I was going to be a Graphic Designer before I switched to Comp Sci. I was active in my Art Honors Society and still draw and make art on occasion!"},
        {"name": "Skiing", "img": "img5.jpg","description": "Skiing is life. There is no better way to destroy my calfs and knees. I started skiing at 13, and it's been a tradition in my friend group to go skiing every winter break for the past 4 years! Shoutout Killington!"},
    ]
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))

@app.route('/map')
def map():
    return render_template('map.html', title="Map", url=os.getenv("URL"))