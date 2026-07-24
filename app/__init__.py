
import os
import hashlib
import re
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

@app.template_filter('gravatar_hash')
def gravatar_hash(email):
    return hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), 
                         user = os.getenv("MYSQL_USER"),
                        password=os.getenv("MYSQL_PASSWORD"), 
                        host=os.getenv("MYSQL_HOST"),
                        port=3306)
print(mydb)
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect(reuse_if_open=True)
mydb.create_tables([TimelinePost])

@app.route('/')
def index():
    return render_template('index.html', title="Alyssa Gannon", url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    hobbies = [
        {"name": "Cooking", "time": "3 years", "img": "app/static/img/hobby_imgs/img1.jpg", "description": "I only recently started cooking since I started college, but I really enjoy finding new recipes to try out! My favorite foods to make right now are carbonara and porkchops with baked potatoes!"},
        {"name": "Baking", "time": "10 years", "img": "app/static/img/hobby_imgs/img2.jpg","description": "I've been baking for longer than I can remember. My grandmother taught me how to make chocolate chip cookies when I was a kid and I've been baking ever since. My favorite thing to bake are my chocolate chip and sugar cookie brookies!"},
        {"name": "Gaming", "time": "7 years", "img": "app/static/img/hobby_imgs/img3.jpg","description": "My gaming interests started in second grade with Pokemon and Tomodachi Life on the 3DS. I still play both to this day, but I've also gotten into Valorant, Stardew Valley, Siege, and more!"},
        {"name": "Drawing", "time": "12 years", "img": "app/static/img/hobby_imgs/img4.jpg","description": "I've been drawing literally forever. I was going to be a Graphic Designer before I switched to Comp Sci. I was active in my Art Honors Society and still draw and make art on occasion!"},
        {"name": "Skiing", "time": "5 years", "img": "app/static/img/hobby_imgs/img5.jpg","description": "Skiing is life. There is no better way to destroy my calfs and knees. I started skiing at 13, and it's been a tradition in my friend group to go skiing every winter break for the past 4 years! Shoutout Killington!"},
    ]
    return render_template('base.html', title="Hobbies", items=hobbies, url=os.getenv("URL"))

@app.route('/map')
def map():
    return render_template('map.html', title="Map", url=os.getenv("URL"))

@app.route('/experience')
def experience():
    work_experience = [
        {"name": "Intern @ Motorboat Mechanics", "time": "May 2026-Present", "img": "app/static/img/work_imgs/motorboatlogo.jpg", "description": "I currently work as an intern at Motorboat Mechanics, I help with various tasks such as automation, setting up appointments for customers, and building a website to track company data."},
        {"name": "Restaurant Team Member @ Tim Hortons", "time": "Dec 2024-Oct 2025", "img": "app/static/img/work_imgs/timhortonslogo.png", "description": "As a restaurant team member at Tim Hortons, I would do a variety of tasks such as taking orders, preparing food, and making coffee and other drinks."},
        {"name": "Instructor @ iD Tech Columbia", "time": "Jun 2025-Aug 2025", "img": "app/static/img/work_imgs/idtechlogo.png", "description": "I was an instructor at iD Tech at Columbia University, where I taught classes on Machine Learning, Scratch, and Minecraft Modding to students ages 6-17."},
    ]
    return render_template('base.html', title="Experience", items=work_experience, url=os.getenv("URL"))

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = (request.form.get('name') or '').strip()
    email = (request.form.get('email') or '').strip()
    content = (request.form.get('content') or '').strip()

    if not name:
        return 'Invalid name', 400
    if not content:
        return 'Invalid content', 400
    if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        return 'Invalid email', 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)
@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
@app.route('/timeline')
def timeline():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return render_template('timeline-template.html', title="Timeline", url=os.getenv("URL"), posts=posts)