

from django.shortcuts import render, redirect
import pyrebase

# Initialize Firebase app
firebase_config = {
    "apiKey":"AIzaSyBQTMX4Rgrpj8DTDuOBgO4g0n9GRePLYzQ",
    "authDomain":"kwentasklaras-c7847.firebaseapp.com",
    "databaseURL":"https://kwentasklaras-c7847-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "kwentasklaras-c7847",
    "storageBucket": "kwentasklaras-c7847.appspot.com",
    "messagingSenderId":"818882186137",
    "appId": "1:818882186137:web:b8d00a65c29f9cae98e108",
    "measurementId":"G-K8RYM6CFCX"
}

firebase = pyrebase.initialize_app(firebase_config)
database = firebase.database()



