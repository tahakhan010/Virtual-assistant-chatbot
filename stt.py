# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 00:10:54 2021

@author: M Taha khan
"""

import speech_recognition as sr
from threading import Thread

from dialogFlow import checkDialogFlowOutput

response = {
    "success": False,
    "error": None,
    "transcription": None
}

def runMicUsingThread(ui):
    parallelThread = Thread(target = recognize_speech_from_mic, args=[ui])
    parallelThread.start()
 

def recognize_speech_from_mic(ui):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=1)
    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit = 4)
    except sr.WaitTimeoutError:
        print("Speech timed Out")
        ui.mic.stop()
        return checkDialogFlowOutput(ui, False, "(Speech Recog. timed out!)")
    
    # set up the response object
    response = {
        "success": False,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
        response["success"] = True
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["success"] = False
        response["error"] = "Unable to recognize speech"
    if(response["success"] == True):
        checkDialogFlowOutput(ui, False, response["transcription"])
    else:
        checkDialogFlowOutput(ui, False, "(inaudible speech)")
    ui.mic.stop()