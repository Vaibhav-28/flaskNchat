from flask import render_template, request, redirect, url_for
from . import app
from .forms import *
from .models import *
from flask_login import login_user, current_user, login_required, logout_user


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_password = pbkdf2_sha256.hash(password)

        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return "Success!!"

    return render_template('register.html', form=reg_form)

@app.route("/login",methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', form=login_form)

@app.route("/room")
def room():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('room.html')

@app.route("/logout",methods=['GET'])
def logout():
    logout_user()
    return "logged out"



