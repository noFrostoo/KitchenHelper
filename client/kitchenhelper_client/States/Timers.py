from kitchenhelper_client import States 
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
  QMessageBox
)
import threading

class Timers(States.BaseState.BaseState):
    def __init__(self, window):
        self.window = window
        self.selectedTimer = SelectedTimer(window, None)
        self.timersListUpdater = TimersListUpdater(window)
        self.selectedId = -1
        self.updateTimersList = False

    def enter(self):
        self.showTimers()
        if self.selectedTimer.hasTimer():
            self.showInfo()
        else:
            self.showTimer()

    def leave(self):
        self.selectedTimer.stopUpdating()
        self.timersListUpdater.stopUpdating()
        self.window.List.clear()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_0:
            self.addToId(0)
        elif e.key() == Qt.Key_1:
            self.addToId(1)
        elif e.key() == Qt.Key_2:
            self.addToId(2)
        elif e.key() == Qt.Key_3:
            self.addToId(3)
        elif e.key() == Qt.Key_4:
            self.addToId(4)
        elif e.key() == Qt.Key_5:
            self.addToId(5)
        elif e.key() == Qt.Key_6:
            self.addToId(6)
        elif e.key() == Qt.Key_7:
            self.addToId(7)
        elif e.key() == Qt.Key_8:
            self.addToId(8)
        elif e.key() == Qt.Key_9:
            self.addToId(9)
        elif e.key() == Qt.Key_Enter:
            self.selectTimer(self.id)
            self.showSelectedTimer()
        elif e.key() == Qt.Key_Escape:
            self.window.changeState(States.Idle.Idle)
            self.window.List.clear()
        else:
            QMessageBox.critical(
            self.window,
            "Error",
            "<p>Wrong key</p>"
            )
    
    def showInfo(self):
        self.window.mainArea.setCurrentIndex(1)
        self.window.TextArea.setText('<h1> Welcome to Stopwatches Page</h1>'
                                '<p> You see this info because you have no Stopwatches</p>'
                                '<p> You can add Stopwatche by pressing + key</p>'
                                '<p> You can remove Stopwatche by pressing - and then entering Stopwatche number </p>'
                                '<p> You can look at pause/start by entering id and then pressing enter </p>'
                                '<p> You can go back by pressing escape key</p>'
                                '<p> Available voice commands: </p>')
    
    def showTimers(self):
        if self.window.timers.count() == 0:
            self.window.List.addItem(f'no active timers')
        else:
            self.updateTimersList()

    def updateTimersList(self):
        self.window.List.clear()
        self.timersListUpdater.run()

    def showSelectedTimer(self):
        self.window.mainArea.setCurrentIndex(0)
        self.selectedTimer.start()
    
    def selectTimer(self, id):
        self.selectedTimer.changeTimer(self.window.timers.getTimer(id))
        self.selectedId = id
        self.id = 0
        self.idSize = 0

    def pauseTimer(self):
        self.window.timers.pauseTimer(self.selectedId)

    def stopTimer(self):
        self.window.timers.stopTimer(self.selectedId)
    
    def startTimer(self):
        self.window.timers.startTimer(self.selectedId)
    
    def addToId(self, number):
        self.id += self.idSize * 10 + number
        self.idSize += 1
        self.window.statusbar.showMessage(f'Timer id: {self.id}')

    

class SelectedTimer(threading.Thread):
    def __init__(self, window, timer):
        threading.Thread.__init__(self)
        self.window = window
        self.ifRun = False
        self.timer = timer
        self.fullTime = timer['time']
        self.clockScale = window.timerClock.upperBound()


    def changeTimer(self, newTimer):
        self.timer = newTimer
    
    def run(self):
        self.ifRun = True
        while self.ifRun:
            self.update()

    def update(self):
        remainingTime = self.timer['timer'].remainingTime()
        progresBarValue = (remainingTime/self.fullTime)*100
        clockValue = (remainingTime/self.fullTime)*self.clockScale
        self.window.timerClock.upperBound(clockValue)
        self.window.timerProgressBar.setValue(progresBarValue)
        remainingTimeText = formatTime(remainingTime)
        self.window.remainingTimeText.setText(remainingTimeText)
    
    def stopUpdating(self):
        self.ifRun = False


    def hasTimer(self):
        return self.timer is not None


class TimersListUpdater(threading.Thread):
    def __init__(self, window):
        threading.Thread.__init__(self)
        self.window = window
        self.ifRun = False

    def run(self):
        self.ifRun = True
        while self.ifRun():
            self.window.List.clear()
            self.updateList()
    
    def updateList(self):
        timers = self.window.timers.getTimers()
        for timer in timers.values():
            remainingTimeText = formatTime(timer['timer'].remainingTime())
            self.window.List.addItem(f'Id: {timer["id"]}, {remainingTimeText}')

    def stopUpdating(self):
        self.ifRun = False

def formatTime(ms):
    s=ms/1000
    m,s=divmod(s,60)
    h,m=divmod(m,60)
    d,h=divmod(h,24)
    return f"{d}:{h}:{m}:{s}"