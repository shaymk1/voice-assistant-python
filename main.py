from fileinput import filename
from typing import Mapping
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import nltk


recognizer = speech_recognition.Recognizer()
nltk.download('omw-1.4')
speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ['meditation', 'breakfast', 'shower', 'drive to work']


def create_note():
    global recognizer
    speaker.say('what do you want to write onto your note?')
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say('choose a file name')
                speaker.runAndWait()
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

            with open(f"{filename}.txt", 'w') as f:
                f.write(note)
                done = True
                speaker.say(f'i successfully created the note{filename}')
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say('i am sorry i did not get that!Please try again!')
            speaker.runAndWait()


def add_todo():
    global recognizer
    speaker.say("what to do do you want to add?")
    speaker.runAndWait()

    done = False
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()
                todo_list.append(item)

                done = True

                speaker.say("i have added new item to the to dolist")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say('i am sorry i did not get that!Please try again!')
            speaker.runAndWait()


def show_todos():
    speaker.say('the items on your todo list are the following:')
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say('Hello, what can i do for you!')
    speaker.runAndWait()


def stop():
    speaker.say('Bye-Bye!')
    speaker.runAndWait()
    sys.exit(0)


mappings = {

    "greetings": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "exit": stop
}


assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()
assistant.save_model()
assistant.load_model()

while True:
    try:

        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
        speaker.say('i am sorry i did not get that!Please try again!')
        speaker.runAndWait()
