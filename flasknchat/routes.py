from time import localtime, strftime
from flask import render_template, request, redirect, url_for, flash
from flask_socketio import send, join_room, leave_room
from . import app, socketio
from .forms import *
from .models import *
from flask_login import login_user, current_user, login_required, logout_user
import random
import string

rooms = []

def generate_room_code():
    length = 10

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if code not in rooms:
            break
    return code

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/enter")
def enter():
    if not current_user.is_authenticated:
        flash('Please login first', 'danger')
        return redirect(url_for('login')) 
    return render_template('enter.html')

@app.route("/create")
def create():
    if not current_user.is_authenticated:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    else:
        room = generate_room_code()
        rooms.append(room)
        return render_template('preroom.html', room=room)

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
        flash(f'Registration for user {username} is successful!','success')
        return redirect(url_for('login'))

    return render_template('register.html', form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        login_user(user)
        flash(f'logged in as { current_user.username } ','success')
        return redirect(url_for('home'))
    return render_template('login.html', form=login_form)

@app.route("/room")
def room():
    room = request.args.get('room') 
    if not current_user.is_authenticated:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))  
    if room not in rooms:
        flash(f'No such room exists!','warning')
        return redirect(url_for('enter'))
    else:
        return render_template('room.html', username=current_user.username, room =room)
        

@app.route("/logout",methods=['GET'])
def logout():
    logout_user()
    flash('logged out successfully','success')
    return redirect('login')

@socketio.on('message')
def message(data):
    data['time'] = strftime('%B, %d : %I:%M%p',localtime())
    socketio.emit('sendMessage', data, room=data['room'])

@socketio.on('join')
def join(data):
    join_room(data['room'])
    socketio.emit('joinBroad',data)

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])


@socketio.on('client_disconnecting')
def disconnect_details(data):
    socketio.emit('leaveBroad', data)

