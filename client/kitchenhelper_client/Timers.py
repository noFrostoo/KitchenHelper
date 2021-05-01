from PyQt5.QtCore import Qt, QTimer

class Timers:
    def __init__(self, window):
        self.window = window
        self.timers = {}
        self.nextId = 0

    def addTimer(self, time, title):
        timer = {
            'title': title,
            'timer': QTimer(),
            'time': time,
            'remainingTime': time
        }
        timer['timer'].timeout.connect(self.timerTimeOut)
        self.timers[self.nextId] = timer

    def removeTimer(self, id):
        pass

    def stopTimer(self, id):
        pass

    def pauseTimer(self, id):
        pass

    def startTimer(self, id):
        pass
    
    def getTimerInfo(self, id):
        pass

    def count(self):
        pass
    
    def updateTimersQuickLookup(self):
        pass

    def updateTimersList(self):
        pass

    def showTimers(self):
        pass
    
    def timerTimeOut(self):
        pass

