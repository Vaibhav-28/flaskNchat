from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
# app.secret_key = 'changeme'


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/room")
def chat():

    username = request.args.get('username')
    roomid = request.args.get('roomid')

    if username and roomid:
        return render_template('room.html', username=username, roomid=roomid)
    else:
        return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template('about.html')


@socketio.on('join_room')
def joinRoom(data):
    app.logger.info(f"{data['username']} has joined the room")
    join_room(data['room'])
    socketio.emit('joinBroadcast', data)


socketio.run(app, debug=True)
