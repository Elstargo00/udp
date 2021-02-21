from flask import render_template, session, redirect, url_for, request
from . import main
from .. import db
from . import functions



@main.route('/')
def index():
    return render_template('index.html')