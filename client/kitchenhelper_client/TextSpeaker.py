import pyttsx3
import threading

class TextSpeaker:
    def __init__(self, window):
        self.window = window
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 100)     # setting up new voice rate
        self.thread = threading.Thread(target=self.sayAndBlock, args=('hello',), daemon=True)
        self.thread.start()
        
    def say(self, text):
        if self.thread.is_alive():
            self.thread.join()
        self.thread = threading.Thread(target=self.sayAndBlock, args=(text,), daemon=True)
        self.thread.start()

    def sayAndBlock(self, text):
        self.engine.say(text)
        self.engine.runAndWait()