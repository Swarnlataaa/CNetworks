from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def create_ftp_server():
    # Create a DummyAuthorizer for managing users
    authorizer = DummyAuthorizer()

    # Add a user with a specific username, password, and home directory
    authorizer.add_user("user", "password", "/path/to/home", perm="elradfmw")

    # Add anonymous user with read-only access to the specified directory
    authorizer.add_anonymous("/path/to/anonymous", perm="elr")

    # Create an FTPHandler and associate the authorizer
    handler = FTPHandler
    handler.authorizer = authorizer

    # Create an FTPServer and bind it to a specific address and port
    server = FTPServer(("127.0.0.1", 21), handler)

    return server

if __name__ == "__main__":
    ftp_server = create_ftp_server()

    print("FTP Server running on 127.0.0.1:21")

    try:
        # Start the FTP server
        ftp_server.serve_forever()
    except KeyboardInterrupt:
        # Gracefully shut down the server on Ctrl+C
        print("FTP Server terminated.")
        ftp_server.close_all()
