import socket
from flask import Flask, jsonify, request, render_template
import threading
import sys
import json
import re
import random
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import webbrowser
from textblob import TextBlob

import os
import wikipedia  # 👈 CHANGED: kept for fallback
from os import getcwd
from email.message import EmailMessage
import mysql.connector
import base64
from flask_cors import CORS
from flask_cors import cross_origin
from transformers import pipeline
from textblob import TextBlob
from transformers import pipeline
# Initialize the emotion detection pipeline
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
from flask import Flask, jsonify, request, render_template
import torch

import random
import re
import requests
from transformers import pipeline
from textblob import TextBlob
import mysql.connector
import spacy
from sentence_transformers import SentenceTransformer, util
import wikipedia
# Initialize the emotion detection model
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")


nlp = spacy.load("en_core_web_sm")

semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
def preprocess_text(text):
    doc = nlp(text.lower())
    return [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]


def get_best_semantic_match(user_input, response_data):
    user_embedding = semantic_model.encode(user_input, convert_to_tensor=True)
    best_score = -1
    best_response = None

    for response in response_data:
        for phrase in response["user_input"]:
            phrase_embedding = semantic_model.encode(phrase, convert_to_tensor=True)
            score = util.pytorch_cos_sim(user_embedding, phrase_embedding).item()
            if score > best_score:
                best_score = score
                best_response = response["bot_response"]

    return best_response if best_score > 0.5 else None



# Connect to MySQL (adjust according to your configuration)
mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mightguy"
)


def make_decision(emotion, sentiment_score, input_string):
    decision = None

    # Emotion-based decision-makings
    if emotion == 'anger':
        decision = "I sense you're frustrated. How about I escalate this to support?"
    elif emotion == 'sadness':
        decision = "It seems like you're feeling down. Let me know how I can assist you better."
    elif emotion == 'joy':
        decision = "I'm happy to see you're in a good mood! How can I help you further?"
    elif emotion == 'fear':
        decision = "Don't worry, I'm here to assist you. How can I make things easier?"
    elif emotion == 'surprise':
        decision = "Looks like you're surprised! What's going on?"
    else:
        decision = "It seems you're feeling something. Let me know if I can help."

    # Sentiment-based decision-making (based on polarity of the input)
    if sentiment_score < 0:
        decision = "I noticed that you're feeling negative. Do you want to talk about it?"

    # Keyword-based decision (For example, "urgent" or "help")
    if "urgent" in input_string.lower():
        decision = "This seems urgent. I'll prioritize your request immediately."

    return decision
def detect_emotion(text):
    emotion = emotion_pipeline(text)
    detected_emotion = emotion[0]['label']
    print(f"Detected emotion for '{text}': {detected_emotion}")
    return detected_emotion


def send_simple_message(user_input, detected_emotion):
    # API_KEY should be stored securely in environment variables
    api_key = os.getenv('API_KEY', 'a8461a92232c3c2d294b196f3ae580a4-17c877d7-067b5a7f')  # Make sure to set your API key in environment variables

    # The email data
    return requests.post(
        "https://api.mailgun.net/v3/sandbox0af3c74f770748b6b9d614ff4ef41f9b.mailgun.org/messages",
        auth=("api", api_key),
        data={
            "from": "Mailgun Sandbox <postmaster@sandbox0af3c74f770748b6b9d614ff4ef41f9b.mailgun.org>",
            "to": "dali <m.a.belkouri@gmail.com>",  # Replace with the recipient's email
            "subject": "Emotion Detected in User Message",
            "text": f"The user typed: '{user_input}'\nEmotion Detected: {detected_emotion}"
        })

# Sentiment analysis function
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity


def load_json(file):
    with open(file, encoding="utf-8") as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


# Store JSON data
response_data = load_json("bot.json")


# Response generation function based on emotion
def get_response(input_string, id):
    detected_emotion = detect_emotion(input_string)

    # Send the detected emotion via email
    response = send_simple_message(input_string, detected_emotion)
    
    # Analyze Sentiment (for additional feedback)
    sentiment_score = analyze_sentiment(input_string)
    bot_response = "Hello, how can I assist you today?"

    # Split the message into individual words and check for predefined responses
    #split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    split_message = preprocess_text(input_string)

    score_list = []

    # Logic for predefined responses (this part is similar to your original code)
   # response_data = [
    #    {"user_input": ["help", "support"], "bot_response": "I'm here to help! What do you need?"}
        # Add more responses here as needed
    #]
    decision = make_decision(detected_emotion, sentiment_score, input_string)

    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["user_input"]

        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        if required_score == len(required_words):
            for word in split_message:
                if word in response["user_input"]:
                    response_score += 1

        score_list.append(response_score)

    best_response = max(score_list)
    response_index = score_list.index(best_response)

    if input_string == "":
        return "Please type something so we can chat :(" + '\U0001F62D'

    if best_response != 0:
        return response_data[response_index]["bot_response"]
    
    semantic_response = get_best_semantic_match(input_string, response_data)
    if semantic_response:
        return semantic_response

    
    # Add emotion-based response
    bot_response += f" [Emotion Detected: {detected_emotion}]"
    bot_response += " " + decision

    # Customize bot response based on the detected emotion
    #if detected_emotion == 'joy':
     #   bot_response = "I'm so happy to hear you're feeling joyful! 😊 " + bot_response
    #elif detected_emotion == 'anger':
     #   bot_response = "It seems like you're upset. How can I help? 😞 " + bot_response
    #elif detected_emotion == 'fear':
        #bot_response = "Don't worry, I'm here to assist you! 💪 " + bot_response
    #elif detected_emotion == 'sadness':
        #bot_response = "I'm sorry you're feeling down. I'm here for you! 💙 " + bot_response
    #elif detected_emotion == 'surprise':
        #bot_response = "Wow! It sounds like you're surprised. What happened? 😲 " + bot_response
    #else:
     #   bot_response = "I see you're feeling something. How can I assist you further? 😊" + bot_response

    # Add a fallback (e.g., using Wikipedia for general questions)
    keywords = ["what is", "who is", "tell me about", "define", "explain"]
    if any(kw in input_string.lower() for kw in keywords):
        try:
            topic = input_string.lower()
            for kw in keywords:
                topic = topic.replace(kw, "")
            topic = topic.strip()
            summary = wikipedia.summary(topic, sentences=5)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Your question is ambiguous. Did you mean: {', '.join(e.options[:3])}?"
        except wikipedia.exceptions.PageError:
            return "Sorry, I couldn't find anything about that topic on Wikipedia."
        except Exception as e:
            return "There was a problem finding info from Wikipedia."

    # If no response found, save question and notify support
    smile_emoji = '\U0001F600'
    r = random.randint(1, 10000)
    mycursor = mysql.cursor()
    mycursor.execute("INSERT INTO QUESTIONS(id ,question) VALUES(%s,%s)", (r, input_string))
    mysql.commit()

    requests.post(
        "https://api.mailgun.net/v3/sandbox3f9c2c0d22534d0ea632230284730d23.mailgun.org/messages",
        auth=("api", "e617652fd4ae0e2db119a5cf7a136230-81bd92f8-af782858"),
        data={
            "from": "mbelkouri392@gmail.com",
            "to": "Mohamed Ali Belkouri <m.a.belkouri@gmail.com>",
            "subject": f"Client {id} didn't understand a response",
            "text": f"The question was: {input_string}"
        })
    bot_response += f" {decision}"

    #return "I didn't understand your question, but the support team will contact you " + smile_emoji
    return bot_response



# Flask App
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/get', methods=['POST'])
@cross_origin()  # 👈 Allow cross-origin

def get_bot_response():
    message = json.loads(request.get_data().decode('utf-8'))
    userText = message.get('msg')
    id = message.get('id')
    return { "msg": str(get_response(userText, id)) }

if __name__ == "__main__":
    app.run()
    CORS(app)