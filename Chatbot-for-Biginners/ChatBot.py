
#install packages
# pip install "chatterbot==1.0.0"
# pip install pytz
#      OR
# pip install -r requirements.txt

# import required packages
import socket
import threading
import sys
import json
import re
import requests
import pyttsx3
import openai
import speech_recognition as sr
import datetime
import webbrowser
import chatgpt
import os
import wikipedia 
from os import getcwd
from email.message import EmailMessage
import ssl
import smtplib

openai.api_key = "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" # or use the method we defined earlier




def generate_responseoo(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()



def process_responseoo(response):
    response = re.sub('[^0-9a-zA-Z\n\.\?,!]+', ' ', response)
    response = re.sub('[\n]+', '\n', response)
    response = response.strip()
    return response



email_sender="m.a.belkouri@gmail.com"   
email_password="psqemhvxddwxgiov"

pp=0
pp=int(pp)
email_receiver="mohamedali.belkouri@smartqualitygate.com"   
subject="dont forget subscribe"
body="""
this is a message when a chatbot didin't understand a predined qustion
"""


# create ChatBot
# Train ChatBot with English language corpus
# you can train with different language
# or with your custom .yam file
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
    
    
        return json.load(bot_responses)
    


# Greeting from chat bot

response_data = load_json(getcwd()+r"\bot.json")

def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = [] 
    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]
        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1
        # Amount of required words should match the required score
        if required_score == len(required_words):
            # print(required_score == len(required_words))
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)
        # Debugging: Find the best phrase
        # print(response_score, response["user_input"])
    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    
    work = input_string
    
    
        
    #print(message_not_found)
    #speak(message_not_found)
    
         #receiveThread = threading.Thread(target = receive, args = (sock, True))
         #receiveThread.start()
         #Send data to server
         #str.encode is used to turn the string message into bytes so it can be sent across the network
         
         #sock.send(str.encode("hi"))
         #sock.send(str.encode(message_not_found))
    
    # Check if input is empty
    work=input_string
    if input_string == "":
        return "Please type something so we can chat :("
    if "raiss" in work:
        #speak("Searching wikipedia...")
        best_response = work.replace("raiss", "")
        
        best_response = generate_responseoo(work)
        best_response = process_responseoo(response)
        
        print(best_response)
        
  
    #return results 
    # If there is no good response, return a random one.
    if best_response != 0:  
        print(response_data[response_index]["bot_response"])
#        speak(response_data[response_index]["bot_response"])
    if best_response == 0:
          #Send data to server
         #str.encode is used to turn the string message into bytes so it can be sent across the network
          
          requests.post(
		"https://api.mailgun.net/v3/sandbox3f9c2c0d22534d0ea632230284730d23.mailgun.org/messages",
		auth=("api", "e617652fd4ae0e2db119a5cf7a136230-81bd92f8-af782858"),
		data={"from": "mbelkouri392@gmail.com",
			"to": "Mohamed Ali Belkouri <m.a.belkouri@gmail.com>",
			"subject": "Hello, client didin't understand a response from the rais chatbot ",
			"text": "hello , there is a client with a certain id , he didi'nt understand  (a response from rais chatbot) , so he needs to talk to the support team (us)"})

# keep communicating with ChatBot
while True:
    # take user input/query
    query = input(">>>")
    # response from ChatBot
    # put query on Statement format to avoid runtime alert messages
    # Statement(text=query, search_text=query)
    print(get_response(query))
