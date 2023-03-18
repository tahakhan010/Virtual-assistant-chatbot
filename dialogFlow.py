# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 04:36:00 2021

@author: M Taha khan
"""

from gtts import gTTS
from playsound import playsound

import os, subprocess, random, re
from datetime import date

from PyQt5 import QtGui

import dialogflow
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private-key.json'

DIALOGFLOW_PROJECT_ID = 'sarah-sdrf'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'MAX'

from threading import Thread

from reminder import createReminder
session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)


def checkDialogFlowOutput(ui, writtenBool, speechIfExists):
    writtenText = ""
    if(writtenBool == True):
        writtenText = ui.chat.text()
    else: writtenText = speechIfExists
    if(writtenText == ""):
        return
    if(writtenBool == True):
        ui.chat.clear()
    history = ui.history
    history.append("You: " + writtenText)
    thread = Thread(target = checkIfLocalOutputOrDialogFlow, args=(ui, writtenText))
    thread.start()
    
def checkIfLocalOutputOrDialogFlow(ui, writtenText):
    localList = ["reminder", "remind", "notepad", "note", "notes"]
    foundIndex = -1
    
    for i, word in enumerate(localList):
        if word in writtenText.lower():
            foundIndex = i
    
    if foundIndex == -1:
        getDialogFlowOutput(ui, writtenText)
    else:
        if foundIndex == 0 or foundIndex == 1 : checkAndCreateReminder(ui, writtenText)
        elif foundIndex == 2 or foundIndex == 3 or foundIndex == 4 : openNotepad(ui)

    
def getDialogFlowOutput(ui, writtenText):
    text_input = dialogflow.types.TextInput(text=writtenText, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    text = response.query_result.fulfillment_text.strip()
    if text != "":
        writeAndSay(ui, response.query_result.fulfillment_text)
    
def checkAndCreateReminder(ui, writtenText):
    num = re.findall(r'\d+', writtenText)
    if not num:
        writeAndSay(ui, "Please provide seconds or minutes with Reminder")
        return
    else:
        sayOkay(ui)
        createReminder(writtenText, int(num[0]))
    
def openNotepad(ui):
    sayOkay(ui)
    print("Opening notepad....")
    today = date.today()
    dateToday = today.strftime("%b-%d-%Y")
    subprocess.Popen(["notepad", "Notepad_" + dateToday + ".txt"])
    
def sayOkay(ui):
    okayWords = ["Okay!", "Sure!", "Alright!", "As you say!", "Done!"]
    writeAndSay(ui, random.choice(okayWords))
    
def writeAndSay(ui, text):
    ui.history.append("Sarah: " + text)
    ui.history.moveCursor(QtGui.QTextCursor.End)
    try:
        ui.makeSay()
        if '<a' in text:
            text = text.split('<')[0]
            ui.history.clearHistory()
        tts = gTTS(text=text, lang="en")
        tts.save("1.mp3")
        playsound("1.mp3")
        os.remove("1.mp3")
        
        print("speaking")
    except PermissionError:
        print("idle")
        ui.makeIdle()
        ui.mic.stop()
        return
    print("idle")
    ui.makeIdle()
    ui.mic.stop()
    ui.history.moveCursor(QtGui.QTextCursor.End)
