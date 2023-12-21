from flask import Flask, request, jsonify
import uuid
import threading
import time

app = Flask(__name__)
sessions = {}

def cleanup_sessions():
    while True:
        current_time = time.time()
        expired_sessions = [session_id for session_id, session in sessions.items() if current_time - session['last_access'] > 60]
        for session_id in expired_sessions:
            del sessions[session_id]
            print(f"Session {session_id} expired and removed.")
        time.sleep(10)

cleanup_thread = threading.Thread(target=cleanup_sessions)
cleanup_thread.start()

@app.route('/start_session', methods=['POST'])
def start_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {'last_access': time.time()}
    return jsonify({'session_id': session_id})

@app.route('/keep_alive', methods=['POST'])
def keep_alive():
    session_id = request.json['session_id']
    if session_id in sessions:
        sessions[session_id]['last_access'] = time.time()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid session ID'})

if __name__ == '__main__':
    app.run(debug=True)
