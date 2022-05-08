from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
import os
import sound
import speech_recognition as sr

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, World!'})

# Get and post request for audio
@app.route('/api/audio', methods=['GET', 'POST'])
def audio():
    print("Request received")
    if request.method == 'POST':
        print("POST request received")
        length = request.content_length
        content_type = request.content_type
        
        if "file" not in request.files:
            return jsonify({"error": "No file in request"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            with open("audio.wav", "wb") as f:
                f.write(data.get_wav_data())
            
            data_features = sound.audio_features("audio.wav", mfcc=True, chroma=True, mel=True)
            model = sound.main()
            prediction = model.predict([data_features])
            print(prediction)
        return jsonify({"result": prediction[0]}), 200
    elif request.method == 'GET':
        return "Hello World!"   

if __name__ == '__main__':
    app.run(debug=True)