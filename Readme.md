# FTP Server Application

This project is a simple FTP server application built using Python and the `pyftpdlib` library. It allows users to connect to the server, upload, and download files.

## Features

- Supports user authentication with full permissions.
- Allows anonymous access with read-only permissions.
- Monitors command-line input to gracefully shut down the server.
- Handles signals for graceful shutdown on `SIGINT` (Ctrl+C) and `SIGTERM`.

## Requirements

- Python 3.x
- `pyftpdlib` library

## Installation

1. **Install Python**: Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Install `pyftpdlib`**: Install the `pyftpdlib` library using `pip`. Open a terminal or command prompt and run:
    ```sh
    pip install pyftpdlib
    ```

## Running the Application

1. **Navigate to the Project Directory**: Change your directory to the location of your `app.py` file. Open a terminal or command prompt and run:
    ```sh
    cd d:\PersonalProjects\FTPServer
    ```

2. **Run the Application**: Execute the `app.py` script using Python. In the terminal or command prompt, run:
    ```sh
    python app.py
    ```

3. **Interact with the FTP Server**:
    - You can use an FTP client like FileZilla or the command-line FTP client to connect to the server.
    - Use the following credentials to connect:
        - **Host**: `localhost`
        - **Port**: `2121`
        - **Username**: `user`
        - **Password**: `12345`
    - Anonymous access is also allowed with read-only permissions.

## Shutting Down the Server

- To gracefully shut down the server, type `q` or `quit` in the terminal where the server is running.
