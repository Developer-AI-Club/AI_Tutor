# import os

# import numpy as np
# import tensorflow as tf
# import yaml
# from tensorflow_tts.utils.utils import CONFIG_FILE_NAME, MODEL_FILE_NAME
# from


# class BaseModel(tf.keras.Model):
#     def set_config(self, config):
#         self.config = config

#     def save_pretrained(self, saved_path):
#         """Save config and weights to file"""
#         os.makedirs(saved_path, exist_ok=True)
#         self.config.save_pretrained(saved_path)
#         self.save_weights(os.path.join(saved_path, MODEL_FILE_NAME))
import os
import time

import playsound

import speech_recognition as sr
from gtts import gTTS

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said =r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: "+ str(e))
        
    return said

speak("hello Hieu")
text= get_audio()
if "hello " in text:
    speak("hello, how are you ?")

if "what is your name" in text:
    speak ("My name is Kubo")

