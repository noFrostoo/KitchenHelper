from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QObject
import threading
from PyQt5.QtWidgets import (
  QMessageBox
)
from time import sleep

class Timers(QObject):
    timerTimeout = pyqtSignal(object)

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.timers = {}
        self.nextId = 0
        self.nextTimerToGoOff = NextTimerToGoOff(window, self.timers)
        self.ifUpdateTimerList = False
        self.UpdateNextTimerToGoOffLookupThread = None
        self.window.TimerText.setText(f'<h2 style="text-align:center">No Timer Active</h2>')
        self.nextTimerToGoOff.update.connect(self.updateNextTimertoGoOff)

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
        if self.nextTimerToGoOff.isRunning() and self.nextTimerToGoOff.isNextTimerToGoOff(id):
            self.nextTimerToGoOff.findNextTimerToGoOff()

    def pauseTimer(self, id):
        remainingTime = self.timers[id]['timer'].remainingTime()
        self.timers[id]['timer'].stop()
        self.timers[id]['remainingTime'] = remainingTime
        self.nextTimerToGoOff.findNextTimerToGoOff()
        if self.nextTimerToGoOff.isRunning() and self.nextTimerToGoOff.isNextTimerToGoOff(id):
            self.nextTimerToGoOff.findNextTimerToGoOff()

    def startTimer(self, id):
        self.timers[id]['timer'].start(self.timers[id]['time'])
        self.nextTimerToGoOff.findNextTimerToGoOff()
        if not self.nextTimerToGoOff.isRunning():
            self.nextTimerToGoOff.start()

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
        QMessageBox.critical(
        self.window,
        "TIMER TIMEOUT",
        f"<p>{self.nextTimerToGoOff.timer['title']} has timed out</p>"
        )
        self.removeTimer(self.nextTimerToGoOff.timer['id'])
        self.nextTimerToGoOff.findNextTimerToGoOff()

    def getTimer(self, id):
        return self.timers[id]
    
    def getTimers(self):
        return self.timers
    
    def updateNextTimertoGoOff(self, timer):
        time = timer['timer'].remainingTime()
        self.window.TimerText.setText(f'<h2 style="text-align:center">Time: {time}</h2>')


class NextTimerToGoOff(QThread):
    update = pyqtSignal(object)
    
    def __init__(self, window, Timers):
        super().__init__(window)
        self.window = window
        self.Timers = Timers
        self.ifRun = False
        self.timer = None
        

    def run(self):
        self.ifRun = True
        while self.ifRun:
            self.update.emit(self.timer)
            sleep(1)
    
    def stop(self):
        self.ifRun = False
    
    def findNextTimerToGoOff(self):
        changed = False
        minTime = 900000000000000
        nextTimerId = -1
        for timer in self.Timers.values():
            if timer['timer'].isActive() and timer['timer'].remainingTime() < minTime:
                nextTimerId = timer['id']
                changed = True
        if not changed:
            self.stop()
            return
        self.timer = self.Timers[nextTimerId]
    
    def isNextTimerToGoOff(self, id):
        return self.timer['id'] == id

    
