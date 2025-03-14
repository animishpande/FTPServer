# web_ui.py
import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
# IMPORTANT: Set a secret key to secure sessions.
app.secret_key = "3112025"  # In production, store this securely!

# The shared folder for FTP files.
FTP_ROOT = os.path.abspath("ftp_root")

# ---------------------------------------------------
# Helper: Login required decorator
# ---------------------------------------------------
def login_required(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        # If the user is not logged in, redirect them to the login page.
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapped_function

# ---------------------------------------------------
# Route: Login
# ---------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        # Retrieve username and password from submitted form.
        username = request.form.get("username")
        password = request.form.get("password")
        # Here, we use the same credentials as defined in the FTP server ("user" and "12345").
        if username == "myfamily" and password == "sweetfamily":
            session["logged_in"] = True  # Mark the user as logged in.  
            return redirect(url_for("index"))
        else:
            error = "Invalid credentials. Please try again."
    return render_template("login.html", error=error)

# ---------------------------------------------------
# Route: Logout
# ---------------------------------------------------
@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)  # Remove the session flag.
    return redirect(url_for("login"))

# ---------------------------------------------------
# Route: Index (File List)
# ---------------------------------------------------
@app.route("/")
@login_required
def index():
    try:
        files = os.listdir(FTP_ROOT)
    except Exception as e:
        files = []
        print("Error reading directory:", e)
    return render_template("index.html", files=files)

# ---------------------------------------------------
# Route: File Download
# ---------------------------------------------------
@app.route("/download/<path:filename>")
@login_required
def download(filename):
    return send_from_directory(FTP_ROOT, filename, as_attachment=True)

# ---------------------------------------------------
# Route: File Upload
# ---------------------------------------------------
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part in the request", 400
        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400
        # Save the file in the FTP_ROOT folder.
        file_path = os.path.join(FTP_ROOT, file.filename)
        file.save(file_path)
        return redirect(url_for("index"))
    return render_template("upload.html")

# ---------------------------------------------------
# New Route: Delete File
# ---------------------------------------------------
@app.route("/delete/<path:filename>", methods=["POST"])
@login_required
def delete(filename):
    file_path = os.path.join(FTP_ROOT, filename)
    # Ensure the file exists and is a file (not a directory).
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print("Error deleting file:", e)
    else:
        print("File does not exist or is not a valid file:", file_path)
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Run the Flask app on port 5000.
    app.run(host="0.0.0.0", port=5000, debug=True)
