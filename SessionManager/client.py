import requests
import time

def start_session():
    response = requests.post('http://127.0.0.1:5000/start_session')
    return response.json()['session_id']

def keep_alive(session_id):
    response = requests.post('http://127.0.0.1:5000/keep_alive', json={'session_id': session_id})
    return response.json()['status']

if __name__ == '__main__':
    session_id = start_session()
    print(f"Session ID: {session_id}")

    # Simulate keeping the session alive
    for _ in range(5):
        time.sleep(10)
        status = keep_alive(session_id)
        print(f"Keep alive status: {status}")
