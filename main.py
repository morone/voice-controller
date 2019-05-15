# !/usr/bin/env python3

import random
import time
import sys
import speech_recognition as sr

import pyttsx3
import requests

engine = pyttsx3.init()

def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def actions(word):
    if word == 'goodbye':
        print('Killing process, bye bye!')
        engine.say('Killing process, bye bye!')
        sys.exit()
    if word == 'post':
        requests.post("www.google.com", data='')


if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        print('Listening ...')
        command = recognize_speech_from_mic(recognizer, microphone)

        if command["error"]:
            print("ERROR: {}".format(command["error"]))

        try:
            print('-> {0}'.format(command["transcription"]))
            actions(command["transcription"])
        except sr.UnknownValueError:
            print("Could not understand audio")
            engine.say("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        finally:
            engine.runAndWait()
