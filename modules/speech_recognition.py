import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer

# ✅ Update this path to match your extracted model location
MODEL_PATH = r"C:\Users\HP\OneDrive\Desktop\jarvis\models\vosk-model-en-us-0.42-gigaspeech"

def recognize_speech():
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        raise Exception(f"Vosk model not found at {MODEL_PATH}. Please check the path!")

    # Load Vosk model
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    # Initialize microphone
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Listening... Speak now!")

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        
        if recognizer.AcceptWaveform(data):  # If a full sentence is recognized
            result = json.loads(recognizer.Result())  # Convert JSON to dictionary
            text = result.get("text", "")  # Get the recognized text

            if text:
                print(f"You said: {text}")
                return text  # Return recognized speech as text

# Test the function
if __name__ == "__main__":
    command = recognize_speech()
    print("Final output:", command)
