import face_recognition
import cv2
import numpy as np
from dialogFlow import writeAndSay

import pytesseract

from PIL import Image
import re

global video_capture
video_capture = None
global notDetected
global ocrDetect
ocrDetect = True

    # Load multiple images and recognize
    
Taha_image = face_recognition.load_image_file("Taha.png")
Taha_face_encoding = face_recognition.face_encodings(Taha_image)[0]
    
    
    # Create arrays of known face encodings and their names
known_face_encodings = [Taha_face_encoding]
known_face_names = ["Taha"]
unknown_face = "Unknown"
    
def startCamera(ui):
    print("Starting camera......")
    global video_capture
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    global notDetected
    notDetected = True
    count = 0
    
    while notDetected:
        count = count + 1
        if ocrDetect:
            detectOCR(count, ui)
        else:
            startFaceDetection(known_face_encodings, known_face_names, ui)
            
def startFaceDetection(known_face_encodings, known_face_names, ui):
    face_encodings = []
    
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    
    # Find all the faces and face encodings in the current frame of video
    face_encodings = face_recognition.face_encodings(rgb_small_frame)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = unknown_face

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            global notDetected
            notDetected = False

        face_names.append(name)

    length = len(face_names)
    text = ""
    
    if length == 1:
        if face_names[0] == unknown_face:
            text = "I could not recognize who is in the camera."
        else:
            text =  "Hi " + ','.join(face_names) + " I can see you now!"
    elif length > 1:
        if unknown_face in face_names:
            face_names.remove(unknown_face)
            text = "Hi " + ', '.join(face_names) + " I can see you now!"
            text = text + " Although I see 1 more who I do not recognize."
        else:
            text = "Hi " + ', '.join(face_names) + " I can see you all!"
    
    speakAndStopCamera(ui, text)

        
def detectOCR(count, ui):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    try:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        gray = cv2.bitwise_not(img_bin)
        
        kernel = np.ones((2, 1), np.uint8)
        img1 = cv2.erode(gray, kernel, iterations=1)
        img1 = cv2.dilate(img1, kernel, iterations=1)
        
        text = pytesseract.image_to_string(Image.fromarray(img1))
        modText = ' '.join(text.split())
        if modText == "":
            if count > 10:
                modText = "I could not read anything"
        else:
            modText = "I could read '" + modText + "'"
    except Exception:
        ui.camera.setStyleSheet("background-color : light gray")
        ui.camera.setChecked(False)
        global notDetected
        notDetected = False
        stopCamera()
        return
    if modText != "":
        speakAndStopCamera(ui, modText)
    
def speakAndStopCamera(ui, text):
    if text != "" and text.strip() != "":
        writeAndSay(ui, text)
        ui.camera.setStyleSheet("background-color : light gray")
        ui.camera.setChecked(False)
        stopCamera()

def stopCamera():
    global notDetected
    notDetected = False
    global video_capture
    if video_capture:
        print("Stopping camera......")
        video_capture.release()
    cv2.destroyAllWindows()