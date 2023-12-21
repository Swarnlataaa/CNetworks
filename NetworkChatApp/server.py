from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Dictionary to store users and their corresponding rooms
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat/<username>/<room>')
def chat(username, room):
    return render_template('chat.html', username=username, room=room)

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']

    users[request.sid] = {'username': username, 'room': room}

    join_message = f"{username} has joined the room."
    emit('message', {'username': 'System', 'message': join_message}, room=room)

@socketio.on('message')
def handle_message(data):
    username = users[request.sid]['username']
    room = users[request.sid]['room']

    emit('message', {'username': username, 'message': data['message']}, room=room)

@socketio.on('file')
def handle_file(data):
    username = users[request.sid]['username']
    room = users[request.sid]['room']

    filename = os.path.join('uploads', data['filename'])
    with open(filename, 'wb') as file:
        file.write(data['file'])

    emit('file', {'username': username, 'filename': data['filename']}, room=room)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    socketio.run(app, debug=True)
