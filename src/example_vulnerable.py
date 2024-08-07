import os
import subprocess
import json
from flask import Flask, request, redirect

app = Flask(__name__)

# Hardcoded credentials
USERNAME = 'admin'
PASSWORD = 'password'

# Hardcoded API key
API_KEY = '12345-abcdef-67890-ghijk'

# SQL Injection vulnerability
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    # Directly executing the query without any sanitization
    result = execute_query(query)
    return result

def execute_query(query):
    # Simulate a database query execution
    print(f"Executing query: {query}")
    return {"username": "admin", "data": "sensitive data"}

# Command Injection vulnerability
@app.route('/run', methods=['POST'])
def run_command():
    command = request.form['command']
    # Directly executing the command without any sanitization
    result = subprocess.check_output(command, shell=True)
    return result

# Insecure deserialization
@app.route('/deserialize', methods=['POST'])
def deserialize_data():
    data = request.data
    # Deserializing user-provided data without validation
    obj = json.loads(data)
    return obj

# Cross-Site Scripting (XSS) vulnerability
@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    # Directly embedding user input into HTML response
    return f"<h1>Hello, {name}!</h1>"

# Path Traversal vulnerability
@app.route('/readfile', methods=['GET'])
def read_file():
    filename = request.args.get('filename')
    # Reading a file specified by user input without validation
    with open(f'./files/{filename}', 'r') as file:
        content = file.read()
    return content

# Open Redirect vulnerability
@app.route('/redirect', methods=['GET'])
def open_redirect():
    url = request.args.get('url')
    # Redirecting to a user-specified URL without validation
    return redirect(url)

# Unrestricted file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Saving the uploaded file without validation
    file.save(os.path.join('./uploads', file.filename))
    return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
