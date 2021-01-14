from chatriya import app,socketio

# @socketio.on('join_room')
# def joinRoom(data):
#     app.logger.info(f"{data['username']} has joined the room")
#     join_room(data['room'])
#     socketio.emit('joinBroadcast', data)


if __name__ == "__main__":
    socketio.run(app, debug=True)
