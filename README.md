# Emotion Recognizer

We have built a Machine Learning model that has the ability to recognize emotions through audio. We have used Librosa to extract the features of the audio file, inlcuding MFCC, chroma and mel information. 

We have used Scikit Learn MLPClassfier in order to train the model using the RAVDESS dataset of audio recordings and their sentiments.

This model is an example of supervised learning wherein we have used some data for training and rest of the data for testing the model. 

The model has an accuracy of 96.56 % in terms of recognizing sentiments of the test data we have provided. 

We have pickled this model for the flask backend to use. 

## Flask Backend

We have used a Flask backend that takes in a simple GET and POST request. 

For the POST request, our API essentially receives an audio file. We have used SpeechRecognition module to convert this into a .wav file and save it locally. Then we extract the audio features and use the model to give it's prediction. 

It is able to return the result to the caller within 1 sec and is extremely efficient. 