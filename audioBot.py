import speech_recognition as sr
import tflearn
from Train import *

while True:
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say Something: ")
        audio = r.listen(source)

        def outText():
            for tg in data["intents"]:
                if tg["tag"] == labels[np.argmax(model.predict([bag_words(say, words)]))]:
                    responses = tg['responses']
                    print(random.choice(responses))
        try:
            say = r.recognize_google(audio)
            print("Text: " + say)
            if say == "quit":
                break

            outText()
        except sr.UnknownValueError:
            print("Can not recognize")

