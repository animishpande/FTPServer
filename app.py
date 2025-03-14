# import os

# from pyftpdlib.authorizers import DummyAuthorizer
# from pyftpdlib.handlers import FTPHandler
# from pyftpdlib.servers import FTPServer


# def main():
#     # Set the absolute or relative path for your shared directory
#     ftp_root = os.path.abspath("ftp_root")

#     # Create an authorizer instance. In production, you might want a proper authentication system.
#     authorizer = DummyAuthorizer()
    
#     # Create a user with full permissions.
#     # Permissions available:
#     #   "elradfmwMT" stands for: 
#     #      e - change directory (CWD, CDUP commands)
#     #      l - list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)
#     #      r - retrieve file from the server (RETR command)
#     #      a - append data to an existing file (APPE command)
#     #      d - delete file or directory (DELE, RMD commands)
#     #      f - rename file or directory (RNFR, RNTO commands)
#     #      m - create directory (MKD command)
#     #      w - store a file on the server (STOR, STOU commands)
#     #      M - change file mode/permission (SITE CHMOD command)
#     #      T - update file modification time (SITE UTIME command)
#     authorizer.add_user("myfamily", "sweetfamily", ftp_root, perm="elradfmwMT")
    
#     # Optionally allow anonymous access (read-only by default)
#     authorizer.add_anonymous(ftp_root, perm="elr")  # only list/search & download

#     # Set up the FTP handler with our auth settings
#     handler = FTPHandler
#     handler.authorizer = authorizer
    
#     # Change the address and port if needed.
#     # Binding to "0.0.0.0" makes the server accessible on any network interface.
#     address = ("0.0.0.0", 2121)  # using 2121 can avoid permission issues that sometimes occur with port 21
    
#     server = FTPServer(address, handler)
#     print(f"FTP server running on {address[0]}:{address[1]}")
#     server.serve_forever()
    
# if __name__ == '__main__':
#     main()

#!/usr/bin/env python3
import os
import sys
import signal
import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def monitor_input(server):
    """
    A helper function to monitor the command-line input.
    When the user types 'q' or 'quit', the FTP server will be closed gracefully.
    """
    while True:
        cmd = input("Enter 'q' or 'quit' to stop the FTP server: ")
        if cmd.strip().lower() in ['q', 'quit']:
            print("Shutting down FTP server as per user request...")
            server.close_all()
            break

def main():
    # Determine the absolute path for the shared FTP directory.
    ftp_root = os.path.abspath("ftp_root")

    # Create an authorizer instance using a simple authentication mechanism.
    authorizer = DummyAuthorizer()
    # Add a user with full permissions
    authorizer.add_user("user", "12345", ftp_root, perm="elradfmwMT")
    # Enable readonly anonymous access.
    authorizer.add_anonymous(ftp_root, perm="elr")

    # Set up the FTP handler with the authorizer.
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define the IP and port for the server to bind to.
    address = ("0.0.0.0", 2121)  # Listen on all interfaces, port 2121.
    server = FTPServer(address, handler)

    # Define a signal handler to gracefully shutdown the server on signals.
    def handle_signal(signum, frame):
        print(f"Received signal {signum}, shutting down FTP server...")
        server.close_all()
        sys.exit(0)

    # Register the signal handler for SIGINT (Ctrl+C) and SIGTERM.
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # Start a separate thread to listen for shutdown command from the console.
    input_thread = threading.Thread(target=monitor_input, args=(server,))
    input_thread.daemon = True
    input_thread.start()

    print(f"FTP server running on {address[0]}:{address[1]}")
    server.serve_forever()

if __name__ == "__main__":
    main()
