import os
import fnmatch
from modules.text_to_speech import speak

def search_files(directory, filename):
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, f"*{filename}*"):
                results.append(os.path.join(root, file))
    
    if results:
        speak(f"Found {len(results)} results.")
        for result in results[:5]:  # Limit to 5 results
            print(result)
    else:
        speak("No files found.")
