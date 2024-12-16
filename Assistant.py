import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser 
import os 
import smtplib
import subprocess
import psutil 
import pywhatkit as kit
import pyaudio

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voice', voices[0].id)

calculator_process = None

def play_on_youtube(query):
    search_query = query.replace("play", "").strip()
    kit.playonyt(search_query)
    
def play_song_on_youtube(query):
    song_name = query.replace("play song", "").strip()
    speak(f'Playing {song_name} on Youtube...')
    kit.playonyt(song_name)  

def open_calculator():
    global calculator_process
    calculator_process = subprocess.Popen(["calc.exe"])
    
def close_calculator():
    global calculator_process
    if calculator_process is not None:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'Calculator.exe' or proc.info['name'] == 'calc.exe':
                proc.terminate()
                proc.wait()
                print("Calculator closed")
                break
            calculator_process = None
    else:
        print("Calculator is not running.")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
        
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
        
    else:
        speak("Good Evening")
        
    speak("I am Jarvis Sir. Please tell me how may I help you")

def takeCommand():
    #it takes microphone input from the user and returns string output
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)
                          
    try:    
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        
    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query

def translate(): 
    speak('Which language do you want to translate from?')
    source_language = takeCommand().lower()
    speak('Which language do you want to translate to?')
    target_language = takeCommand().lower()
    
    speak('What text do you want to translate?')
    text_to_translate = takeCommand()
    
    url = f"https://translate.google.com/translate_a/single?client=gtx&sl={source_language}&tl={target_language}&dt=t&q={text_to_translate}"
    response = response.get(url)
    data = response.json()
    translated_text = data[0][0][0]
    
    speak(f"The translated text is: {translated_text}") 
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()
            
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            
        if 'open youtube' in query:
            webbrowser.open("youtube.com")
            
        elif 'search youtube' in query: 
            speak('What do you want to search on Youtube?')
            search_query = input("Enter search query: ")
            kit.playonyt(search_query)
        
        elif 'play song' in query:
            play_song_on_youtube(query)

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open microsoft edge' in query:
            webbrowser.open("microsoftedge.com")
            
        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorit Songs2'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
            
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            
        elif 'open code' in query:
            codePath = "C:\\Users\\gncs\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
            
        elif 'open calculator' in query:
            open_calculator()
            
        elif 'close calculator' in query:      
            close_calculator()
            
        elif 'email to Jack' in query: #try pull request of the remark
            try:
                speak("What Should I say?")
                content = takeCommand()
                to = "anshkumar5008@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry My friend Ansh Bro. I am not able  to send  this email")
        
speak()
 


