from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
import os

app = Flask(__name__)
CORS(app)

# Get and post request for audio
@app.route('/api/audio', methods=['GET', 'POST'])
def audio():
    if request.method == 'POST':
        length = request.content_length
        content_type = request.content_type
        data = request.data
        return f"Content-Length: {length}\nContent-Type: {content_type}\n\n{data}"
    elif request.method == 'GET':
        return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)