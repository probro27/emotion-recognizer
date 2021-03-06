from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
import os
import sound
import speech_recognition as sr
import pickle
import soundfile as sf
from werkzeug.utils import secure_filename
import connectSpotify

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
        
        print(request.files)
        if "file" not in request.files:
            return jsonify({"error": "No file in request"}), 400
        
        file = request.files['file']
        print(type(file))
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            print(type(audioFile))
            with audioFile as source:
                data = recognizer.record(source)
            with open("audio.wav", "wb") as f:
                f.write(data.get_wav_data())
            data_features = sound.audio_features("audio.wav", mfcc=True, chroma=True, mel=True)
            model = pickle.load(open("finalized_model.sav", "rb"))
            prediction = model.predict([data_features])
            os.environ["MOOD"] = str(prediction[0])
            username = request.form['username']
            token = connectSpotify.connect(username)
            sp = connectSpotify.authenticate()
            top_tracks_uri = connectSpotify.aggregate_top_tracks(sp, connectSpotify.aggregate_top_artists(sp))
            selected_tracks = connectSpotify.select_tracks(sp, top_tracks_uri)
            playlist_uri = connectSpotify.create_playlist(sp, selected_tracks)
            print(sp)
            print(prediction)
        return jsonify({"result": prediction[0], "uri": playlist_uri}), 200
    elif request.method == 'GET':
        return "Hello World!"   

if __name__ == '__main__':
    app.run(debug=True)