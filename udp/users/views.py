# udp/users/views.py

from flask import render_template, request, url_for, redirect, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from udp import db
from udp.dbs_handler import User
from udp.users.forms import LoginForm, RegistrationForm, UpdateUserForm 
from udp.users.picture_handler import add_profile_picture

users = Blueprint('users', __name__)

# logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('cores.index'))

# register
@users.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        form.check_email(form)
        form.check_username(form)
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    
    return render_template('registration.html', form=form)


# login
@users.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('cores.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            
            if next == None or not next[0]=='/':
                next = url_for('cores.index')
            return redirect(next)
    return render_template('login.html', form=form)

# account
@users.route('/account')
@login_required
def account():
    profile_picture = url_for('static', filename='profile_pictures/'+ current_user.profile_picture)
    form = UpdateUserForm()
    if form.validate_on_submit():
        
        if form.picture.data:
            username = current_user.username
            pic = add_profile_picture(form.picture.data, username)
            current_user.profile_picture = pic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('users.account'))
        
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
            
    
    return render_template('account.html', profile_picture=profile_picture, form=form)

