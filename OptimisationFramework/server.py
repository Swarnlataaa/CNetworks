<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Room</title>
</head>
<body>
    <h1>Chat Room: {{ room }}</h1>
    <div id="messages"></div>
    <input type="text" id="message_input" placeholder="Type your message...">
    <button onclick="sendMessage()">Send</button>
    <input type="file" id="file_input" onchange="sendFile()">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/3.0.4/socket.io.js"></script>
    <script>
        var socket = io.connect('http://' + document.domain + ':' + location.port);

        socket.emit('join', {username: '{{ username }}', room: '{{ room }}'});

        socket.on('message', function(data) {
            var messageDiv = document.createElement('div');
            messageDiv.innerHTML = '<b>' + data.username + '</b>: ' + data.message;
            document.getElementById('messages').appendChild(messageDiv);
        });

        socket.on('file', function(data) {
            var messageDiv = document.createElement('div');
            messageDiv.innerHTML = '<b>' + data.username + '</b> has shared a file: <a href="/uploads/' + data.filename + '" target="_blank">' + data.filename + '</a>';
            document.getElementById('messages').appendChild(messageDiv);
        });

        function sendMessage() {
            var messageInput = document.getElementById('message_input');
            var message = messageInput.value;
            if (message.trim() !== '') {
                socket.emit('message', {message: message});
                messageInput.value = '';
            }
        }

        function sendFile() {
            var fileInput = document.getElementById('file_input');
            var file = fileInput.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    socket.emit('file', {filename: file.name, file: e.target.result});
                };
                reader.readAsDataURL(file);
                fileInput.value = '';
            }
        }
    </script>
</body>
</html>
