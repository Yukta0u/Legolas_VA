import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
import subprocess
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import time
import pyjokes
import requests
import pyautogui
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import smtplib


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices');
# print(voices[0].id)
engine.setProperty('voices', voices[len(voices) - 1].id)

#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

#For Fetching Weather 

# Fetch weather using OpenWeatherMap API
def get_weather(city):
    api_key = "6a3e637501b657139998f0183d5e5e1b"  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(base_url).json()
        if response["cod"] == 200:
            city_name = response["name"]
            temperature = response["main"]["temp"]
            weather_description = response["weather"][0]["description"]
            humidity = response["main"]["humidity"]
            wind_speed = response["wind"]["speed"]

            # Speaking weather details
            speak(f"The weather in {city_name} is as follows:")
            speak(f"Temperature: {temperature} degrees Celsius")
            speak(f"Condition: {weather_description}")
            speak(f"Humidity: {humidity} percent")
            speak(f"Wind Speed: {wind_speed} meters per second")
        else:
            speak("Sorry, I couldn't find the weather details for the specified location.")
    except Exception as e:
        speak("An error occurred while fetching the weather information. Please try again later.")

#To Play and Stop music

music_process = None  # To store the music process

def play_music():
        music_dir = r"C:\Users\mda15\Music\Songs"
        songs = os.listdir(music_dir)
        # rd = random.choice(songs)
        for song in songs:
            if song.endswith('.mp3'):
                os.startfile(os.path.join(music_dir, song))
        
def stop_music():
    """Stop music by closing the Media Player window."""
    speak("Stopping music...")
    try:
        # Locate Media Player by title
        media_player_window = pyautogui.getWindowsWithTitle("Media Player")[0]
        media_player_window.close()  # Close the window
        speak("Music has been stopped.")
    except IndexError:
        speak("No active Media Player window found.")

#To convert voice into text
def  takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)  # Calibrate for background noise.
        try:
            audio = r.listen(source,timeout=30,phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Timeout occurred while listening.")
            speak("I couldn't hear anything. Please try again.")
            return "none"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")

    except Exception as e:
        speak("Say that again please...")
        return "none"
    return query

#to wish
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour <= 12:
        speak(f"good morning, its {tt}")
    elif hour >= 12 and hour <= 18:
        speak(f"good afternoon, its {tt}")
    else:
        speak(f"good evening, its {tt}")
    speak("i am Legolas. please tell me how Should I assist you today")

  
#to send email
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('mda15299@gmail.com', 'tranquile@6')
    server.sendmail('mda15299@gmail.com', to, content)
    server.close()
 
 
 

#for news updates
def news():
    api_key = 'b0f73319ea464637b7a60284e349ddab'
    main_url = f'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={api_key}'

    main_page = requests.get(main_url).json()
    # print(main_page)
    articles = main_page["articles"]
    # print(articles)
    head = []
    day=["first","second","third","fourth","fifth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        # print(f"today's {day[i]} news is: ", head[i])
        speak(f"today's {day[i]} news is: {head[i]}")



if __name__ == "__main__": #main program
    wish()
    while True:
    # if 1:

        query = takecommand().lower()

        #logic building for tasks

        if "open notepad" in query:
            npath = "C:\\Windows\\System32\\notepad.exe"
            os.startfile(npath)
            
            
        elif 'hi' in query or 'hello' in query:
            speak("Hello , how may I help you?")
        
        elif "open adobe" in query:
            apath = r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"
            os.startfile(apath)

        elif "open command prompt" in query:
            os.system("start cmd")

        # elif "open camera" in query:  // Original Code
        #     cap = cv2.VideoCapture(0)
        #     while True:
        #         ret, img = cap.read()
        #         cv2.imshow('webcam', img)
        #         k = cv2.waitKey(1)
        #         if k==27:
        #             break;
        #     cap.release()
        #     cv2.destroyAllWindows()

        # elif "play music" in query:
        #     music_dir = r"C:\Users\mda15\Music\Songs"
        #     songs = os.listdir(music_dir)
        #     # rd = random.choice(songs)
        #     for song in songs:
        #         if song.endswith('.mp3'):
        #             os.startfile(os.path.join(music_dir, song))
        
        # Example usage based on query:

        if "play music" in query:
            play_music()
        elif "stop music" in query:
            stop_music()
        
        #For Fetching weather
        elif "give weather" in query:
            speak("Please tell me the name of the city.")
            city = takecommand().lower()
            if city != "none":
                get_weather(city)
            else:
                speak("I couldn't understand the city name.")

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"your IP address is {ip}")
        # Modified To Open Wikipedia
        # elif "show wikipedia" in query:
        #     webbrowser.open("www.wikipedia.com")
        #To Search on wikipedia     Commented Code
        # elif "what is" in query:
        #     speak("searching wikipedia....")
        #     query = query.replace("What is","")
        #     results = wikipedia.summary(query, sentences=2)
        #     speak("According to wikipedia")
        #     speak(results)    
        
        #Added Code
        elif "what is" in query.lower():
            speak("Searching Wikipedia...")
            query = query.lower().replace("what is", "").strip()
            if query:
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    speak(results)
                except Exception as e:
                    speak("Sorry, I couldn't find any information on that.")
            else:
                speak("Please provide a valid query.")

        
        # elif "open youtube" in query:
        #     webbrowser.open("www.youtube.com")
        elif "open youtube" in query:
            speak("What should I search on YouTube?")
            search_query = takecommand().lower()
            if search_query != "none":
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}")
                speak(f"Searching for {search_query} on YouTube.")
            else:
                speak("Search query not received. Opening YouTube homepage.")
                webbrowser.open("https://www.youtube.com")
                
        #To Open Calculator      
        elif "open calculator" in query:
           speak("Opening Calculator.")
           os.system("calc")

        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")

        elif "open stackoverflow" in query:
            webbrowser.open("www.stackoverflow.com")
        
        #Modified Open-Google
        elif "open google" in query:
            speak("What should I search on Google?")
            cm = takecommand().lower()
            if cm:  # Ensure the command is not empty
                webbrowser.open(f"https://www.google.com/search?q={cm}")
            else:
                speak("I couldn't understand. Please try again.")
              
        elif "open wikipedia" in query:
            speak("What should I search on Wikipedia?")
            cm = takecommand().lower()
            webbrowser.open(f"https://en.wikipedia.org/wiki/{cm.replace(' ', '_')}")
        # elif "send whatsapp message" in query:
        #     kit.sendwhatmsg("+91_To_number_you_want_to_send", "this is testing protocol",4,13)
        #     time.sleep(120)
        #     speak("message has been sent")
        
        #Modified to close Browser
        
        #1 Chrome
        elif 'close chrome' in query or 'lose chrome' in query:
            speak("Closing Chrome...")
            os.system("taskkill /f /im chrome.exe")

        #2 Edge
        elif 'close edge' in query or 'lose edge' in query:
            speak("Closing Microsoft Edge...")
            os.system("taskkill /f /im msedge.exe")


        elif "song on youtube" in query:
            kit.playonyt("Thunder")
        
        #Old Timer Code     
        # elif 'timer' in query or 'stopwatch' in query:
        #     speak("For how many minutes?")
        #     timing = takecommand()
        #     timing =timing.replace('minutes', '')
        #     timing = timing.replace('minute', '')
        #     timing = timing.replace('for', '')
        #     timing = float(timing)
        #     timing = timing * 60
        #     speak(f'I will remind you in {timing} seconds')

        #     time.sleep(timing)
        #     speak('Your time has been finished sir')
        #  modified
        elif 'set timer' in query or 'stopwatch' in query:
            speak("For how much time? You can specify minutes or seconds.")
            timing = takecommand()  # Example input: "5 minutes" or "30 seconds"
            try:
        # Normalize the input to lowercase and clean it up
                timing = timing.lower()
        
        # Handle minutes
                if 'minute' in timing:
                    timing = timing.replace('minutes', '').replace('minute', '').replace('for', '').strip()
                    timing_in_seconds = float(timing) * 60  # Convert minutes to seconds
        
        # Handle seconds
                elif 'second' in timing:
                    timing = timing.replace('seconds', '').replace('second', '').replace('for', '').strip()
                    timing_in_seconds = float(timing)  # Already in seconds
        
        # If no unit is mentioned, assume seconds
                else:
                    timing_in_seconds = float(timing)
        
        # Notify the user and start the timer
                
                speak(f'I will remind you in {timing_in_seconds} seconds.')
                time.sleep(timing_in_seconds)
                speak('Your time has finished, sir.')
            except ValueError:
        # Handle cases where the input is not a valid number
                speak("Sorry, I couldn't understand the time duration. Please try again.")   
                
                     
        # elif "email to me" in query: 
            #try:
                #speak("what should i say?")
                #content = takecommand().lower()
                #to = "mohger15201@gmail.com"
                #sendEmail(to,content)
                #speak("Email has been sent to Rashmi")

            #except Exception as e:
                #print(e)
                #speak("sorry Ma'am, i am not able to sent this mail")
                
              

        elif "ok thanks" in query:
         speak("thanks for using me, have a good day.")
         sys.exit()
            


#to close any application
        elif "close notepad" in query:
         speak("okay, closing notepad")
         os.system("taskkill /f /im notepad.exe")

#to set an alarm
        elif "set alarm" in query:
           nn = int(datetime.datetime.now().hour)
           if nn==22: 
                music_dir = 'E:\\music'
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))
#to find a joke
        elif "tell me a joke" in query:
         joke = pyjokes.get_joke()
         speak(joke)

        elif "shut down the system" in query:
         os.system("shutdown /s /t 5")

        elif "restart the system" in query:
         os.system("shutdown /r /t 5")

        elif "sleep the system" in query:
         os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")



###########################################################################################################################################
###########################################################################################################################################



        elif 'switch the' in query:
           pyautogui.keyDown("alt")
           pyautogui.press("tab")
           time.sleep(1)
           pyautogui.keyUp("alt")
                   

        elif "give news" in query:
           speak("please wait,fetching the latest news")
           news()


        elif "email to Rashmi" in query:
           speak("Ma'am what should i say")
           query = takecommand().lower()
           if "send a file" in query:
                email = 'your@gmail.com' # Your email
                password = 'your_pass' # Your email account password
                send_to_email = 'To_person@gmail.com' # Whom you are sending the message to
                speak("okay Ma'am, what is the subject for this email")
                query = takecommand().lower()
                subject = query   # The Subject in the email
                speak("and Ma'am, what is the message for this email")
                query2 = takecommand().lower()
                message = query2  # The message in the email
                speak("Ma'am please enter the correct path of the file into the shell")
                file_location = input("please enter the path here")    # The File attachment in the email

                speak("please wait,i am sending email now")

                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = send_to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(message, 'plain'))

                # Setup the attachment
                filename = os.path.basename(file_location)
                attachment = open(file_location, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                # Attach the attachment to the MIMEMultipart object
                msg.attach(part)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email, password)
                text = msg.as_string()
                server.sendmail(email, send_to_email, text)
                server.quit()
                speak("email has been sent to Rashmi")

else:                
                email = 'your@gmail.com' # Your email
                password = 'your_pass' # Your email account password
                send_to_email = 'To_person@gmail.com' # Whom you are sending the message to
                message = query # The message in the emai

                server = smtplib.SMTP('smtp.gmail.com', 587) # Connect to the server
                server.starttls() # Use TLS
                server.login(email, password) # Login to the email server
                server.sendmail(email, send_to_email , message) # Send the email
                server.quit() # Logout of the email server
                speak("email has been sent to Rashmi")
            

        # speak("Ma'am, do you have any other work")
#### To Close the Voice-Assistant ####

