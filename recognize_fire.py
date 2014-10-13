import pyaudio
import speech_recognition as sr
from twilio.rest import TwilioRestClient
from init import *
import random
r = sr.Recognizer()
response=""
count=0
while "fire" not in response and "help" not in response and "911" not in response and count<5:
    with sr.Microphone() as source:                # use the default microphone as the audio source
        audio = r.listen(source)                   # listen for the first phrase and extract it into audio data
    try:
        response=r.recognize(audio)    # recognize speech using Google Speech Recognition
        print(response)
    except LookupError:                            # speech is unintelligible
        print("Could not understand audio")
    count+=1

def generate_sequence(): 
    adjectives=["grand", "baby", "musical", "quiet", "quick", "good"]
    colors=["red","blue","green","purple","orange","cyan","pink", "amber", "gray"]
    nouns=["paper", "desk", "plant", "cereal", "monkey", "car", "window", "diamond", "street", "water", "icon"]
    url=""
    url+=random.choice(adjectives)+"-"
    url+=random.choice(colors)+"-"
    url+=random.choice(nouns)
    with app.app_context():
        g.db=connect_db()
        add_to_db(url)
    return url;

response=generate_sequence()
# Find these values at https://twilio.com/user/account
account_sid = "AC653afa392f0405d63291b6caa60d275d"
auth_token = "41584e5b461e673b46cc328893a4cc75"
client = TwilioRestClient(account_sid, auth_token)
 
message = client.messages.create(to="+18478637628", from_="+17472221936",
                                     body="fire fire fire!!!\n222 W Merchandise Mart Plz\n12th Fl 1871\nvisit localhost:5000/%s to see more info."%response)