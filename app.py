import base64
import os
import subprocess

from flask import Flask, request

app = Flask(__name__)

# Insecure practices that Trivy would detect:
HARDCODED_PASSWORD = "super_secret_password123"  # Hardcoded credentials
API_KEY = "sk_live_51HV9qZGQLm3uY2aPkiLQJLhVDabC457y"  # Exposed API key

@app.route('/execute', methods=['POST'])
def execute_command():
    # Command injection vulnerability
    command = request.form.get('command')
    result = subprocess.run(command, shell=True, capture_output=True)
    return result.stdout.decode()

@app.route('/file', methods=['GET'])
def read_file():
    # Path traversal vulnerability
    filename = request.args.get('filename')
    with open(filename, 'r') as file:
        return file.read()

@app.route('/login', methods=['POST'])
def login():
    # Insecure cookie setting
    username = request.form.get('username')
    password = request.form.get('password')

    if password == HARDCODED_PASSWORD:
        response = "Login successful"
        # Insecure cookie (no httpOnly, no secure flag)
        return response

    return "Login failed"

if __name__ == '__main__':
    # Running with debug=True in production is a security risk
    app.run(debug=True, host='0.0.0.0')
