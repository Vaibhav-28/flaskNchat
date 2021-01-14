from flask import render_template, request, redirect, url_for
from . import app
from .forms import *
from .models import *


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/room")
def room():

    roomid = request.args.get('roomid')

    if roomid:
        return render_template('room.html', roomid=roomid)
    else:
        return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Success!!"

    return render_template('register.html', form=reg_form)
