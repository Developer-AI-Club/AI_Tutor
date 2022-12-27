import speech_recognition as sr
from t2t_model import *
import time 
# import wikipedia
# wikipedia.set_lang('en')

while True:
    r = sr.Recognizer()
    
    with sr.Microphone() as mic:
        
        audio = r.listen(mic)

        try:      
            print("Say something or quit for stop!")  
            text = r.recognize_google(audio)
            text = text.lower()
            if "stop talking" in text:
                print("You:", text)
                print("Bot: I hope to see you soon !")
                break
            print(f"You say: {text} ")
           
            results = model.predict([bag_of_words(text, words)])
            results_index = np.argmax(results)
            tag = labels[results_index]
            
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
        
            print("Bot: ",random.choice(responses))
           
            
        except sr.UnknownValueError:
            print("You were trying to be funny ")
            # r = sr.Recognizer()
            time.sleep(2)
            # continue