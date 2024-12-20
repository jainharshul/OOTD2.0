'''// Import the functions you need from the SDKs you need

import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyD3FuW6RemgH-Nc9ksE3RMUw989MoSIVuI",
  authDomain: "ootd2-493ef.firebaseapp.com",
  projectId: "ootd2-493ef",
  storageBucket: "ootd2-493ef.firebasestorage.app",
  messagingSenderId: "658206910414",
  appId: "1:658206910414:web:a65537f978d27a447dad9f",
  measurementId: "G-47RCDRVDN6"
};
'''

import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path to your Firebase private key
firebase_key_path = os.getenv("FIREBASE_KEY_PATH")

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(cred)

# Get Firestore database
db = firestore.client()
