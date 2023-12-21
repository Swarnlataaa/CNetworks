import requests
import os

SERVER_URL = 'http://127.0.0.1:5000'
UPLOAD_FOLDER = 'uploads'

def upload_file(file_path):
    files = {'file': open(file_path, 'rb')}
    response = requests.post(f'{SERVER_URL}/upload', files=files)

    if response.status_code == 200:
        print('File uploaded successfully')
    else:
        print(f'Error uploading file: {response.json()}')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    while True:
        print('Options:')
        print('1. Upload file')
        print('2. Exit')

        choice = input('Enter choice (1/2): ')

        if choice == '1':
            file_path = input('Enter the path of the file to upload: ')
            upload_file(file_path)
        elif choice == '2':
            break
        else:
            print('Invalid choice. Please enter 1 or 2.')
