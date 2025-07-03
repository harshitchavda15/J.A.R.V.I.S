from tkinter import *
from tkinter.scrolledtext import ScrolledText
import asyncio
import threading
from friday_core import recognize_speech, speak, process_command  # Adjust name as needed

class FridayGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FRIDAY Assistant")
        self.root.geometry("600x400")

        self.output_box = ScrolledText(root, wrap=WORD, font=("Helvetica", 12))
        self.output_box.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.input_entry = Entry(root, font=("Helvetica", 12))
        self.input_entry.pack(padx=10, pady=(0, 10), fill=X)
        self.input_entry.bind("<Return>", self.handle_text_command)

        self.listen_button = Button(root, text="🎙️ Start Listening", command=self.start_listening)
        self.listen_button.pack(pady=5)

    def log(self, message):
        self.output_box.insert(END, message + "\n")
        self.output_box.see(END)

    def handle_text_command(self, event=None):
        command = self.input_entry.get().strip()
        self.input_entry.delete(0, END)
        self.log(f"You: {command}")
        threading.Thread(target=self.async_command, args=(command,)).start()

    def start_listening(self):
        threading.Thread(target=self.listen_loop).start()

    def listen_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.listen_and_respond())

    async def listen_and_respond(self):
        command = await recognize_speech()
        if command:
            self.log(f"You (mic): {command}")
            await process_command(command, respond=self.log)
        else:
            self.log("FRIDAY: I didn't catch that.")

    def async_command(self, command):
        asyncio.run(process_command(command, respond=self.log))

if __name__ == "__main__":
    root = Tk()
    app = FridayGUI(root)
    root.mainloop()
