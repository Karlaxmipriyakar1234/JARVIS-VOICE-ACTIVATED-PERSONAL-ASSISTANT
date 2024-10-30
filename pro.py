import pyttsx3
import speech_recognition as sr
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import wikipedia
import pygame
import os
import webbrowser

# Initialize the TTS engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)#it is a python inbuild library for find current date and time
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your personal assistant mam. Please tell me how may I help you")

def recognize_speech(prompt):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt)
        print(prompt)
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        text = r.recognize_google(audio, language='en-in')
        print(f"You said: {text}")
        return text
    except sr.RequestError:
        speak("API unavailable")
        print("API unavailable")
    except sr.UnknownValueError:
        speak("Unable to recognize speech")
        print("Unable to recognize speech")
    except Exception as e:
        speak(f"Error: {e}")
        print(f"Error: {e}")
    return None

def send_email(to_email, subject, body):
    from_email = "your_email@gmail.com"
    password = "your_password"  # Use environment variables or a secure method to handle credentials

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        speak("Email sent successfully!")
        print("Email sent successfully!")
    except Exception as e:
        speak(f"Failed to send email: {e}")  
        print(f"Failed to send email: {e}")

def search_wikipedia(query):
    try:
        speak(f"Searching Wikipedia for {query}")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    except Exception as e:
        speak("Sorry, I couldn't find any results for your query")
        print(f"Error: {e}")

def play_music(file_path):
    if not os.path.exists(file_path):
        speak("Sorry, the music file does not exist.")
        print("Music file does not exist.")
        return

    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    speak("Playing music")
    while pygame.mixer.music.get_busy():
        continue

def calculator():
    speak("Welcome to the calculator. Please say the first number")
    num1 = recognize_speech("Please say the first number")
    if num1 is None:
        speak("Error recognizing speech for the first number")
        return

    operator = recognize_speech("Please say the operator (plus, minus, times, divided by)")
    if operator is None:
        speak("Error recognizing speech for the operator")
        return

    num2 = recognize_speech("Please say the second number")
    if num2 is None:
        speak("Error recognizing speech for the second number")
        return

    try:
        num1 = int(num1)
        num2 = int(num2)
    except ValueError:
        speak("Could not convert speech to an integer")
        return

    if operator == 'plus':
        result = num1 + num2
    elif operator == 'minus':
        result = num1 - num2
    elif operator == 'times':
        result = num1 * num2
    elif operator == 'divided by':
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Division by zero is not allowed"
    else:
        result = "Invalid operator"

    speak(f"The result is {result}")

if __name__ == "__main__":
    
    
    wishMe()

    while True:
        command = recognize_speech("Please say the command")
        if command:
            command = command.lower()
            
            if "send email" in command:
                to_email = recognize_speech("Please say the recipient's email address")
                if to_email:
                    subject = recognize_speech("Please say the subject of the email")
                    if subject:
                        body = recognize_speech("Please say the body of the email")
                        if body:
                            send_email(to_email, subject, body)
                        else:
                            speak("Failed to get the email body.")
                    else:
                        speak("Failed to get the email subject.")
                else:
                    speak("Failed to get the recipient's email address.")
                    
            elif "wikipedia" in command:
                query = recognize_speech("Please say the topic you want to search on Wikipedia")
                if query:
                    search_wikipedia(query)
                else:
                    speak("Failed to get the search query")
            
            elif "play music" in command:
                music_path = "path/to/your/music/file.mp3"  # Replace with the path to your music file
                play_music(music_path)
            
            elif "search on youtube" in command:
                speak("What do you want to search on YouTube?")
                query = recognize_speech("What do you want to search on YouTube?")
                if query:
                    search_url = f"https://www.youtube.com/results?search_query={'+'.join(query.split())}"
                    webbrowser.open(search_url)
                else:
                    speak("Failed to get the search query")
                    
            elif "search on google" in command:
                speak("What do you want to search on Google?")
                query = recognize_speech("What do you want to search on Google?")
                if query:
                    search_url = f"https://www.google.com/search?q={'+'.join(query.split())}"
                    webbrowser.open(search_url)
                else:
                    speak("Failed to get the search query")
                    
            elif "calculator" in command:
                calculator()
                    
            elif "what is your name" in command:
                speak("My name is Task Master and I am Laxmi's personal assistant.")  
            elif "hello" in command:
                speak("Hello mam, how are you?")
            elif "i am fine" in command:
                speak("That is great, mam.") 
            elif "how are you" in command:
                speak("Perfect, mam.") 
            elif "thank you" in command:
                speak("You are welcome, mam.")                       
            elif "who made you" in command:
                speak("I have been created by Laxmipriya.")  
            elif "change your name" in command:
                speak("What would you like to call me?") 
                assname = recognize_speech("What would you like to call me?")
                if assname:
                    speak(f"Thanks for naming me {assname}")
                else:
                    speak("Failed to get the name")
                
            elif "exit" in command:
                speak("Thanks for giving your time.") 
                exit() 
                
            else:
                speak("I can only help with sending emails, searching Wikipedia, playing music, and searching on YouTube right now.")
        else:
            speak("Failed to recognize the command.")
