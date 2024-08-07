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

# Critical: Remote Code Execution vulnerability
@app.route('/rce', methods=['POST'])
def rce():
    code = request.form['code']
    # Directly executing user input as code
    exec(code)
    return "Code executed"

# Critical: Use of eval() with untrusted input
@app.route('/eval', methods=['POST'])
def eval_code():
    expression = request.form['expression']
    # Evaluating user-provided expression
    result = eval(expression)
    return str(result)

# Unsafe file operations: Writing to a file based on user input
@app.route('/writefile', methods=['POST'])
def write_file():
    filename = request.form['filename']
    content = request.form['content']
    # Writing user input to a file without validation
    with open(filename, 'w') as file:
        file.write(content)
    return 'File written successfully'

# Lack of authentication and authorization checks
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    # Allowing access to admin operations without verifying user identity
    if request.method == 'POST':
        # Perform some admin operation
        action = request.form['action']
        # Execute action
        return f'Admin action {action} executed'
    return 'Admin Panel: POST to perform actions'

if __name__ == '__main__':
    app.run(debug=True)
