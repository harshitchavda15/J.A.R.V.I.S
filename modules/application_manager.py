import subprocess  
import modules.text_to_speech as speak

apps={
    "notepad":"notepad.exe",
    "calculator":"calc.exe",
    "chrome":"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
}

def open_application(app_name):
    if app_name in apps:
        subprocess.Popen(apps[app_name])
        speak(f"Opening {app_name}")
    else:
        speak(f"Application {app_name} not found")