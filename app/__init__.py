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
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))
@app.route('/map')
def map():
    return render_template('map.html', title="Map", url=os.getenv("URL"))
@app.route('/experience')
def experience():
    work_experience = [
        {"name": "Intern @ Motorboat Mechanics", "time": "May 2026-Present", "img": "img1.jpg", "description": "I currently work as an intern at Motorboat Mechanics, I help with various tasks such as automation, setting up appointments for customers, and building a website to track company data."},
        {"name": "Intern @ Motorboat Mechanics", "time": "Dec 2024-Oct 2025", "img": "img2.jpg", "description": "As a restaurant team member at Tim Hortons, I would do a variety of tasks such as taking orders, preparing food, and making coffee and other drinks."},
        {"name": "Instructor @ iD Tech Columbia", "time": "Jun 2025-Aug 2025", "img": "img3.jpg", "description": "I was an instructor at iD Tech at Columbia University, where I taught classes on Machine Learning, Scratch, and Minecraft Modding to students ages 6-17."},
    ]
    return render_template('hobbies.html', title="Experience", url=os.getenv("URL"))