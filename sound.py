from random import sample
import librosa as lb
import numpy as np
import soundfile as sf
import os, glob, pickle
import pickle

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

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

focussed_emotional_labels = ['calm', 'happy', 'fearful', 'disgust']
def audio_features(file_name, mfcc, chroma, mel):
    print(file_name)
    with sf.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype = "float32")
        sample_rate = sound_file.samplerate
        result = np.array([])
        if mfcc:
            mfccs = np.mean(lb.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            stft = np.abs(lb.stft(X))
            chroma = np.mean(lb.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(lb.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
            result = np.hstack((result, mel))
    return result
        
def loading_audio_data(test_size=0.2):
    x,y = [],[]
    for file in glob.glob("./data/Actor_*/*.wav"):
        # print(file)
        file_name = os.path.basename(file)
        emotion = emotional_labels[file_name.split("-")[2]]
        if emotion not in focussed_emotional_labels:
            continue
        feature = audio_features(file, mfcc=True, chroma=True, mel=True)
        x.append(feature)
        y.append(emotion)
    return train_test_split(np.array(x), y, test_size=test_size, random_state=101)

def main():
    X_train, X_test, y_train, y_test = loading_audio_data(test_size=0.25)
    # print(f'Features extracted: {X_train.shape[1]}')
    model = MLPClassifier(alpha=0.01, batch_size=256, epsilon=1e-08, 
                        hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=500)
    model.fit(X_train,y_train)

    filename = 'finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))

    y_pred = model.predict(X_test)
    print(f'Accuracy: {accuracy_score(y_test, y_pred) * 100}%')
    print(classification_report(y_true=y_test, y_pred=y_pred))

if __name__ == '__main__':
    main()