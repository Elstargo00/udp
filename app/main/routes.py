# import zone
from . import app, db
from flask import render_template, request, redirect, url_for, session
from . import functions


@app.route('/')
def index():
    return render_template('index.html')