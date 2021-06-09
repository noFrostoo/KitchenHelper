import pyttsx3
import threading

class TextSpeaker:
    def __init__(self, window):
        self.window = window
        self.engine = pyttsx3.init()
        self.queue = []
        self.ifRun = True
        self.engine.setProperty('rate', 100)     # setting up new voice rate
        self.thread = threading.Thread(target=self.__waitAndSayLoop, daemon=True)
        self.thread.start()
        
    def say(self, text):
        """
        This funcionc is not blocking, it adds text to qeueu and returns
        """
        self.queue.append(text)
    
    def finish(self):
        self.ifRun = False
        self.thread.join()

    def __waitAndSayLoop(self):
        while self.ifRun:
            if len(self.queue) != 0:
                text = self.queue.pop(0)
                self.engine.say(text)
                self.engine.runAndWait()