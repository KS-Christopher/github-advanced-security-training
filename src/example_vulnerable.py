import os
import subprocess
import json
from flask import Flask, request

app = Flask(__name__)

# Hardcoded credentials
USERNAME = 'admin'
PASSWORD = 'password'

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

if __name__ == '__main__':
    app.run(debug=True)
