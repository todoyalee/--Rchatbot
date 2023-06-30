import socket
from flask import Flask, jsonify, request,render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import threading
import sys
import json
import re
import random
import pyttsx3
import requests
import openai
import speech_recognition as sr
import datetime
import webbrowser
import chatgpt
import os
import wikipedia 
from os import getcwd
from email.message import EmailMessage


import mysql.connector
b=1
mysql=mysql.connector.connect(

    host="localhost",
    user="root",
    passwd="",
    database="mightguy",
)

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


email_sender="m.a.belkouri@gmail.com"   
email_password="psqemhvxddwxgiov"
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
    
    
        return json.load(bot_responses)




def process_responseoo(response):
    response = re.sub('[^0-9a-zA-Z\n\.\?,!]+', ' ', response)
    response = re.sub('[\n]+', '\n', response)
    response = response.strip()
    return response




pp=0
pp=int(pp)
email_receiver="mohamedali.belkouri@smartqualitygate.com"   
subject="dont forget subscribe"
body="""
this is a message when a chatbot didin't understand a predined qustion
"""
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


# Store JSON data
response_data = load_json("bot.json")


def get_response(input_string,id):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []
    #r=random.randint(99999,999999999999999)
          #Send data to server
         #str.encode is used to turn the string message into bytes so it can be sent across the network
        
    #mycursor=mysql.cursor()
    #mycursor.execute("insert into QUESTIONS(id ,question) values(%s,%s)" ,(r,input_string))
         
    #mysql.commit()

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
    work=input_string

    # Check if input is empty
    if input_string == "":
        return "Please type something so we can chat :("+'\U0001F62D'


    # If there is no good response, return a random one.
    if best_response != 0:
     #aa='\U0001F603'
     #bb='\U0001F60E'
     #cc='\U0001F44D'
     #ee='\U0001F60D'
     #dd='\U0001F44E'
     #ff='\U0001F602'
     #gg='\U0001F60A'
     #kk='\U0001F600'
     #tablee=[aa,bb,cc,dd,ee,ff,gg,kk]
     #rr=random.randint(0,8)
     #return response_data[response_index]["bot_response"]+tablee[rr]
     return response_data[response_index]["bot_response"]
  
     #r=random.randint(99999,999999999999999)
     #mycursor=mysql.cursor()
     #mycursor.execute("insert into QUESTIONS2(id ,question) values(%s,%s)" ,(r,input_string))
     #mysql.commit()
     

          #Send data to server
         #str.encode is used to turn the string message into bytes so it can be sent across the network
          
    if best_response == 0:
          smile_emoji = '\U0001F600'
          r=random.randint(1,10000)
          #Send data to server
         #str.encode is used to turn the string message into bytes so it can be sent across the network
        
          mycursor=mysql.cursor()
          mycursor.execute("insert into QUESTIONS(id ,question) values(%s,%s)" ,(r,input_string))
         
          mysql.commit()
          
          
          requests.post(
		"https://api.mailgun.net/v3/sandbox3f9c2c0d22534d0ea632230284730d23.mailgun.org/messages",
		auth=("api", "e617652fd4ae0e2db119a5cf7a136230-81bd92f8-af782858"),
		data={"from": "mbelkouri392@gmail.com",
			"to": "Mohamed Ali Belkouri <m.a.belkouri@gmail.com>",
			"subject":"Hello, client "+id+" didin't understand a response from the rais chatbot and his question is : \n"+input_string,
			"text": "hello , there is a client with a certain id , he didi'nt understand  (a response from rais chatbot) , so he needs to talk to the support team (us)"})
          return(" i didin't understnad your question but support team will contact u to answear it"+smile_emoji)
    
    #return random_responses.random_string()
    


import base64    
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/get',methods=['POST'])
#@app.route('/get')
def get_bot_response():
    message=json.loads(request.get_data().decode('utf-8'))




    #request feha data lkoul ,url ,header,all the request bdara bkoul chy
    userText = message.get('msg')
    id = message.get('id')
    print(get_response(userText,id))
    return { "msg":str(get_response(userText,id)) }
    
    
    
    #print (str(get_response(userText)))
    



if __name__ == "__main__":
    app.run()

    