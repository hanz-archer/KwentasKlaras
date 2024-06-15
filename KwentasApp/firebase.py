
from django.shortcuts import render, redirect
import pyrebase

# Initialize Firebase app
firebase_config = {
    "apiKey":"AIzaSyBrm2OZhgEi5UF0hTr36t-X8CJ7jffc_z8",
    "authDomain": "test-24ea0.firebaseapp.com",
    "databaseURL": "https://test-24ea0-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "test-24ea0",
    "storageBucket": "test-24ea0.appspot.com",
    "messagingSenderId":"811829331453",
    "appId": "1:811829331453:web:12930831feba2f3a098594",
    "measurementId": "G-5EQ2SMHDSY"
}

firebase = pyrebase.initialize_app(firebase_config)
database = firebase.database()

