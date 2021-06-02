import speech_recognition as sr
from kitchenhelper_client.Singleton import Singleton


class VoiceInterpreter(metaclass=Singleton):
    def __init__(self):
        self.r = sr.Recognizer()

    def listenAndRecognize(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.r.listen(source)
        self.text = self.r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + self.text)
        return self.text
        
    def getText(self):
        return self.text
    
    def getError(self):
        return self.error
    
    def recognize(self, audio):
        self.text = self.r.recognize_google(audio)
        return self.text
    
    def listen(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.r.listen(source)
        return audio



        # except sr.UnknownValueError:
        #     print("Google Speech Recognition could not understand audio")
        #     self.error = "Google Speech Recognition could not understand audio"
        # except sr.RequestError as e:
        #     print("Could not request results from Google Speech Recognition service; {0}".format(e))
        #     self.error = "Could not request results from Google Speech Recognition service; {0}".format(e)
