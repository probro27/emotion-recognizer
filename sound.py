from random import sample
import librosa as lb
import numpy as np
import soundfile as sf
import os, glob, pickle

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

emotional_labels = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

focused_emotional_labels = ['happy', 'sad', 'angry']

def audio_features(file_path, mfcc, chroma, mel):
    with sf.SoundFile(file_path) as sound_file:
        audio = sound_file.read(dtype='float32')
        sample_rate = sound_file.samplerate
        if chroma:
            stft = np.abs(lb.stft(audio))
            result = np.array([])
        if mfcc:
            mfcc = np.mean(lb.feature.mfcc(y = audio,sr = sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfcc))
        if chroma:
            chroma = np.mean(lb.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(lb.feature.melspectrogram(audio, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))
        return result