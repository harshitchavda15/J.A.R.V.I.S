import os
import datetime
import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import webbrowser
import requests
import asyncio
import pyjokes
import pygetwindow as gw
import pyautogui
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

app=Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)

async def speak(text):
    print(f"FRIDAY: {text}")
    engine.say(text)
    engine.runAndWait()

async def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You: {command}")        
            return command
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            await speak("Sorry, I am having trouble connecting to the internet.")
            return None
        except sr.WaitTimeoutError:
            return None

def get_greeting():
    """Returns a greeting based on the system time."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning, Boss!"
    elif 12 <= hour < 18:
        return "Good afternoon, Boss!"
    else:
        return "Good evening, Boss!"

async def open_application(app_name):
    print(f"Opening application: {app_name}")
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "vscode": "C:\\Users\\HP\\OneDrive\\Desktop\\Visual Studio Code.lnk",
        "excel":"EXCEL.exe",
        "word":"WINWORD.exe",
        "powerpoint":"POWERPNT.EXE",
    }
    if app_name in apps:
        os.startfile(apps[app_name])
        await speak(f"Opening {app_name}")
    else:
        await speak("Application not found.")

async def search_web(query):
    print(f"Searching Google for: {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")
    await speak("Here is what I found on Google.")

async def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    print(f"Current time: {now}")
    await speak(f"The current time is {now}")

async def tell_date():
    today = datetime.date.today().strftime("%B %d, %Y")
    print(f"Today's date: {today}")
    await speak(f"Today's date is {today}")

async def get_wikipedia_summary(topic):
    print(f"Searching Wikipedia for: '{topic}'")  # Debugging print
    try:
        summary = wikipedia.summary(topic, sentences=2)
        print(f"Wikipedia Summary: {summary}")  # Debugging print
        await speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"DisambiguationError: {e.options}")  # Debugging print
        await speak(f"There are multiple topics. Did you mean {', '.join(e.options[:5])}?")
    except wikipedia.exceptions.PageError:
        print("PageError: No information found.")  # Debugging print
        search_results = wikipedia.search(topic)
        if search_results:
            print(f"Trying related search: {search_results[0]}")  # Debugging print
            summary = wikipedia.summary(search_results[0], sentences=2)
            await speak(summary)
        else:
            await speak("Still no results found.")
            
async def get_weather(city="Ahmedabad"):
    print(f"Fetching weather for: {city}")
    api_key = "006c26dd9077b540af59c2f6a18d3389"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()
        
    if data.get("cod") == 200:
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        await speak(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")
    else:
        await speak(f"Error fetching weather: {data.get('message', 'Unknown error')}")  # Show actual error message

async def control_system(action):
    print(f"System control action: {action}")
    if action == "shutdown":
        os.system("shutdown /s /t 1")
    elif action == "restart":
        os.system("shutdown /r /t 1")
    elif action == "log off":
        os.system("shutdown /l")
    elif action == "sleep":
        os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
    elif action == "lock":
        os.system("rundll32.exe user32.dll,LockWorkStation")
    await speak(f"System {action} in progress.")

async def play_youtube(video):
    print(f"Playing YouTube video: {video}")
    pywhatkit.playonyt(video)
    await speak(f"Playing {video} on YouTube.")

async def tell_joke():
    joke = pyjokes.get_joke()
    print(f"Joke: {joke}")
    await speak(joke)

async def take_screenshot():
    filename="screenshot.png"
    screenshot=pyautogui.screenshot()
    screenshot.save(filename)
    print(f'Screenshot saved as {filename}')
    await speak("Screenshot taken.")

def get_active_window():
    try:
        win = gw.getActiveWindow()
        if win:
            print(f"Active window: {win.title}")
            return win
        else:
            print("No active window found.")
            return None
    except Exception as e:
        print(f"Error getting window: {e}")
        return None

def minimize_active_window():
    win = get_active_window()
    if win:
        win.minimize()
        print("Window minimized.")

def maximize_active_window():
    win = get_active_window()
    if win:
        win.maximize()
        print("Window maximized.")
   
async def run_friday():
    greeting = get_greeting()
    await speak(f"{greeting}")
    while True:
        command = await recognize_speech()
        if command:
            print(f"Command received: {command}")
            if "open" in command:
                app_name = command.replace("open", "").strip()
                await open_application(app_name)
            elif "search" in command:
                query = command.replace("search", "").strip()
                await search_web(query)
            elif "time" in command:
                await tell_time()
            elif "date" in command:
                await tell_date()
            elif "wikipedia" in command:
                topic = command.replace("wikipedia", "").strip()
                await get_wikipedia_summary(topic)
            elif "weather" in command:
                city = command.replace("weather", "").strip()
                await get_weather(city)
            elif "shutdown" in command:
                await control_system("shutdown")
            elif "restart" in command:
                await control_system("restart")
            elif "log off" in command:
                await control_system("log off")
            elif "sleep" in command:
                await control_system("sleep")
            elif "lock" in command:
                await control_system("lock")    
            elif "play" in command:
                video = command.replace("play", "").strip()
                await play_youtube(video)
            elif "joke" in command:
                await tell_joke()
            elif "screenshot" in command:
                await take_screenshot()
            elif "minimise window" or "minimise the window" in command:
                 minimize_active_window()
            elif "maximise window" or "maximise the window" in command:
                  maximize_active_window()
            elif "exit" in command or "quit" in command:
                await speak("Goodbye Boss.")
                break
            else:
                await speak("Sorry Boss, I didn't get that.")
if __name__ == "__main__":
    asyncio.run(run_friday())
