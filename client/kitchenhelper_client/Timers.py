from PyQt5.QtCore import Qt, QTimer
import threading
from PyQt5.QtWidgets import (
  QMessageBox
)
class Timers:
    def __init__(self, window):
        self.window = window
        self.timers = {}
        self.nextId = 0
        self.nextTimerToGoOff = NextTimerToGoOff(window, self.timers)
        self.ifUpdateTimerList = False
        self.UpdateNextTimerToGoOffLookupThread = None
        self.window.TimerText.setText(f'<h1 style="text-align:center">No Timer Active</h1>')

    def addTimer(self, time, title):
        id = self.nextId
        timer = {
            'id': self.nextId,
            'title': title,
            'timer': QTimer(),
            'time': time,
            'remainingTime': time
        }
        timer['timer'].timeout.connect(self.timerTimeOut)
        self.timers[self.nextId] = timer
        self.nextId += 1
        return id

    def removeTimer(self, id):
        self.timers[id]['timer'].stop()
        self.timers.pop(id, None)
        self.nextTimerToGoOff.findNextTimerToGoOff()

    def stopTimer(self, id):
        self.timers[id]['timer'].stop()
        self.timers[id]['remainingTime'] = 0
        self.nextTimerToGoOff.findNextTimerToGoOff()

    def pauseTimer(self, id):
        remainingTime = self.timers[id]['timer'].remainingTime()
        self.timers[id]['timer'].stop()
        self.timers[id]['remainingTime'] = remainingTime
        self.nextTimerToGoOff.findNextTimerToGoOff()

    def startTimer(self, id):
        self.timers[id]['timer'].start(self.timers[id]['time'])
        self.nextTimerToGoOff.findNextTimerToGoOff()

    def getTimerInfo(self, id):
        remainingTime = self.timers[id]['timer'].remainingTime()
        self.timers[id]['remainingTime'] = remainingTime
        return {
            'title': self.timers[id]['title'],
            'remainingTime': remainingTime,
            'timeFull': self.timers[id]['time']
            }

    def count(self):
        return len(self.timers.keys())

    
    def timerTimeOut(self):
        self.nextTimerToGoOff.timerTimeOut()
        
    def getTimer(self, id):
        return self.timers[id]
    
    def getTimers(self):
        return self.timers


class NextTimerToGoOff(threading.Thread):
    def __init__(self, window, Timers):
        threading.Thread.__init__(self)
        self.window = window
        self.Timers = Timers
        self.ifRun = False
        self.timer = None

    def run(self):
        self.ifRun = True
        while self.ifRun:
            time = self.timer['timer'].remainingTime()
            self.window.TimerText.setText(f'<h1 style="text-align:center">Time remaining: {time}</h1>')
    
    def stop(self):
        self.ifRun = False
    
    def findNextTimerToGoOff(self):
        minTime = 9000000000000000000000000
        nextTimerId = -1
        for timer in self.Timers.values():
            if timer['timer'].remainingTime() < minTime:
                nextTimerId = timer['id']
        self.timer = self.Timers[nextTimerId]
    
    def timerTimeOut(self):
        QMessageBox.critical(
        self.window,
        "TIMER TIMEOUT",
        f"<p>{self.timer['title']} has timed out</p>"
        )
        self.findNextTimerToGoOff()
    
