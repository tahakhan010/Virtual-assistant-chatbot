# -*- coding: utf-8 -*-
"""
Created on Wed May 19 18:14:30 2021

@author: M Taha khan
"""

import time
from win10toast import ToastNotifier

def createReminder(writtenText, num):
    if "minute" in writtenText:
        timerMinutes(num)
    else:
        timerSeconds(num)
        

def showError():
    try:
        notifier = ToastNotifier()
        notifier.show_toast(f"Notification","Reminder could not be created.",duration=5, threaded=True)
    except AttributeError as error:
        print("Notifications already exist")


def timerMinutes(minutes):
    minutes = int(minutes)
    notifier = ToastNotifier()
    try:
        notifier.show_toast("Reminder",f"System will remind you in exactly {minutes} minutes..",duration = 5, threaded=True)
        time.sleep(minutes * 60)
        notifier.show_toast(f"Reminder","Reminder created by Sarah",duration=15, threaded=True)
    except AttributeError as error:
        showError()
    
def timerSeconds(seconds):
    minutes = int(seconds)
    notifier = ToastNotifier()
    try:
        notifier.show_toast("Reminder",f"System will remind you in exactly {seconds} seconds..",duration = 5, threaded=True)
        time.sleep(seconds)
        notifier.show_toast(f"Reminder","Reminder created by Sarah",duration=15, threaded=True)
    except AttributeError as error:
        showError()