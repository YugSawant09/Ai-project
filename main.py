import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import datetime
import os
from modules.data_processing import log_query_csv, log_query_json

# Initialize recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            log_query_csv(command)
            log_query_json(command)
            return command
        except sr.UnknownValueError:
            return "Sorry, I didn't understand."
        except sr.RequestError:
            return "Could not request results, check your internet connection."

# Function to process commands
def process_command(command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    elif "date" in command:
        today_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today's date is {today_date}")
    elif "search" in command:
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}")
    elif "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia: {summary}")
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results, please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("No Wikipedia page found for this query.")
    elif "open notepad" in command:
        os.system("notepad.exe")
        speak("Opening Notepad")
    elif "history" in command:
        from modules.data_processing import get_query_history
        print(get_query_history())
        speak("Showing your last 10 queries.")
    elif "exit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I didn't understand that. Can you say it again?")

# Main loop
if __name__ == "__main__":
    speak("Hello, I am your AI assistant with Big Data capabilities. How can I help you?")
    while True:
        command = recognize_speech()
        process_command(command)
