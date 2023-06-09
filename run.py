from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtGui import QMovie
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import pyttsx3 # python text to speech
import speech_recognition as sr
import os
import time
import webbrowser
import sounddevice
from scipy.io.wavfile import write

import pywhatkit
import speech_recognition as sr
import pyttsx3  # python text to speech
import datetime
import wikipedia
import pyjokes
import os
import webbrowser
import numpy as np
import cv2
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc#A FourCC ("four-character code") is a sequence of four bytes (typically ASCII) used to uniquely identify data formats.


flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)

engine = pyttsx3.init('sapi5')#Microsoft Speech API (SAPI5) is the technology for voice recognition and synthesis provided by Microsoft
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)# 0 for male,1 for female
engine.setProperty('rate',180)
# engine=pyttsx3.init(): The init function is the main function, we have to use this function every time. This function initializes the connection and creates an engine and we can perform all the things on the engine created by the .init() function
# engine.say(text): This function will convert the text to speech (text is the input from the user)
# engine.runAndWait(): This function will make the speech audible in the system, if you don't write this command then the speech will not be audible to you.
# engine.setProperty(): This method sets different properties of the model.
# engine.getProperty(): This method is used to get the details with the help of this function.
# voice: If we want the Voices and ascent of the model, we can get it with the help of the voice method.
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)#for current date and time
    if hour>=0 and hour <12:
        speak("Good morning,I am your alexa how can i help you?")
    elif hour>=12 and hour<17:
        speak("Good Afternoon,I am your alexa how can i help you?")
    else:
        speak("Good evening,I am your alexa how can i help you?")
#Widgets are small parts on web applications that allow user input
class mainT(QThread):#To communicate between the main thread and the worker threads, you use signals and slots i.e QThread
    def __init__(self):
        super(mainT,self).__init__()
    
    def run(self):
        self.Alexa()
    
    def STT(self):
        R = sr.Recognizer()# Creating a recognizer who can recognize voice
        with sr.Microphone() as source:
            print("Listening...........")# used for indication that our assistant is listening
            R.adjust_for_ambient_noise(source,duration=1)#used to calibrate the recognizer for changing noise conditions each time the recognize_speech is called
            #anaylses audio source for 1 second
            audio = R.listen(source)# using microphone as source and then calling speech recognizer to listen to this source and thus we can use functions which speech recognizer uses to convert voice to  text
        try:
            print("Recog......")
            text = R.recognize_google(audio,language='en-in') # Using google API ,pass the voice to google and it will give text
            print(">> ",text)
        except Exception:
            speak("Sorry! can you Speak Again")
            return "None"
        text = text.lower()
        return text

    def Alexa(self):
        wish()
        while True:
            self.query = self.STT()
            if 'close' in self.query:
                speak("Good bye")
                sys.exit()
            elif ("open my mail" in self.query) or ("gmail" in self.query) or ("check my email" in self.query):
                    search_term = self.query.split("for")[-1]
                    url = "https://mail.google.com/mail/u/0/#inbox"
                    webbrowser.get().open(url)
                    speak("here you can check your gmail")

            elif "record" in self.query:
                    speak("Recording")
                    fps = 44100 #frequency of audio
                    duration = 10
                    print('Recording')
                    rec = sounddevice.rec(int(duration * fps), samplerate=fps, channels=2)#sound coming from or going to a single point
                    sounddevice.wait()
                    print('Done')
                    speak("Recording done")
                    write('recording.wav', fps, rec)

            elif "capture" in self.query:
                speak("Capturing your video")
                webcam = cv2.VideoCapture(0)
                video = VideoWriter('webcam.avi', VideoWriter_fourcc(*'MP42'), 25.0, (640, 480))#25:frame rate,(640,480):(width,height)
                while True:
                    #get the frame from webcam
                # stream_ok checks webcam is working or not
                    stream_ok, frame = webcam.read()
                    if stream_ok:
                        #display current frame
                        cv2.imshow('webcam', frame)
                        video.write(frame)
                    if cv2.waitKey(1) & 0xFF == 27:#to tell the computer that the representation is in hexadecimal:0xFF
                        break
                #clean ups
                cv2.destroyAllWindows()
                webcam.release()
                video.release


            elif 'open google' in self.query:
                webbrowser.open('www.google.co.in')
                speak("opening google")
            elif 'open youtube' in self.query:
                speak("opening youtube")
                webbrowser.open("www.youtube.com")
            elif "play" in self.query or "open" in self.query:
                speak("playing on youtube")
                song = self.query.replace('play', '')
                
                pywhatkit.playonyt(song)

            elif 'search' in self.query or 'what' in self.query or 'who' in self.query or "how" in self.query:
                speak("Searching on Google")
                if 'who' in self.query:
                    try:
                        person = self.query.replace('who is', '')
                        info = wikipedia.summary(person, 1)  # 1 denotes the number of lines
                        
                    except Exception as e:
                        pass

                self.query = self.query.replace("search", "")
                self.query = self.query.replace("play", "")
                pywhatkit.search(self.query)

            elif "time" in self.query:
                time = datetime.datetime.now().strftime("%I:%M:%p")  # to get the current time in string format
            # %H for hour %M for minute %p for AM or PM
                speak("The time is " + time)

            elif 'wikipedia' in self.query:  # if wikipedia found in thecommand then this block will be executed
                speak('Searching Wikipedia...')
                try:
                    self.query = self.query.replace("wikipedia", "")
                    results = wikipedia.summary(self.query, sentences=2)
                    speak("According to Wikipedia")
                    speak(results)
                except Exception as e:
                    pywhatkit.search(self.query)


            elif 'joke' in self.query:
                speak(pyjokes.get_joke())

            elif ("+" in self.query) or ("-" in self.query) or ("multiply " in self.query) or ("divide" in self.query) or ("power" in self.query):
                opr = self.query.split()[1]
                if opr == '+':
                    try:
                        speak(int(self.query.split()[0]) + int(self.query.split()[2]))
                        print(int(self.query.split()[0]) + int(self.query.split()[2]))
                    except Exception as e:
                        speak("Operator or operand not recognized")
                elif opr == '-':
                    try:
                        speak(int(self.query.split()[0]) - int(self.query.split()[2]))
                        print(int(self.query.split()[0]) - int(self.query.split()[2]))
                    except Exception as e:
                        speak("Operator or operand not recognized")
                elif opr == 'multiply' or opr=="x":
                    try:
                        speak(int(self.query.split()[0]) * int(self.query.split()[2]))
                        print(int(self.query.split()[0]) * int(self.query.split()[2]))
                    except Exception as e:
                        speak("Operator or operand not recognized")

                elif opr == 'divide':
                    try:
                    
                        speak(int(self.query.split()[0]) / int(self.query.split()[2]))
                        print(int(self.query.split()[0]) / int(self.query.split()[2]))
                    except Exception as e:
                        speak("Operator or operand not recognized")

                elif opr == 'power':
                    try:
                        speak(int(self.query.split()[0]) ** int(self.query.split()[2]))
                        print(int(self.query.split()[0]) ** int(self.query.split()[2]))
                    except Exception as e:
                        speak("Operator or operand not recognized")
                

                
                else:
                    speak("Wrong Operator")

FROM_MAIN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"./scifi.ui"))

class Main(QMainWindow,FROM_MAIN):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)  #For loading all the graphics
        self.setFixedSize(1920,1080)
        self.label_7 = QLabel
        self.exitB.setStyleSheet("background-image:url(./lib/exit - Copy.png);\n"
        "border:none;")
        self.exitB.clicked.connect(self.close)#adding action to the button
        self.setWindowFlags(flags)
        Assistant = mainT()
        self.label_7 = QMovie("./lib/gifloader.gif", QByteArray(), self)#QMovie is a class for playing movies, but it can also play (animated) gifs.
        self.label_7.setCacheMode(QMovie.CacheAll)
        self.label_4.setMovie(self.label_7)
        self.label_7.start()

        self.ts = time.strftime("%A, %d %B")

        Assistant.start()
        self.label.setPixmap(QPixmap("./lib/tuse.png"))
        self.label_5.setText("<font size=8 color='white'>"+self.ts+"</font>")
        self.label_5.setFont(QFont(QFont('Acens',8)))


app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
exit(app.exec_())#Qt applications are event-based. When you call the exec() method, it starts an event loop and creates a thread that is referred to as the main thread.