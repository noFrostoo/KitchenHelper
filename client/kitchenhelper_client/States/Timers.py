from kitchenhelper_client import States 
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtWidgets import (
  QMessageBox
)
from kitchenhelper_client.pythonUi.AddTimerDialog import AddTimerDialog
from time import sleep
from kitchenhelper_client.pythonUi.ListenDialog import ListenDialog 
from word2number import w2n

class Timers(States.BaseState.BaseState):
    def __init__(self, window):
        self.window = window
        self.updeter = Updater(window, None)
        self.selectedId = -1
        self.id = -1
        self.updateTimersList = False
        self.updeter.updateSelectedTimerSignal.connect(self.updateMainArea)
        self.updeter.updateTimerListSignal.connect(self.updateTimerList)
        self.window.timers.timerTimeout.connect(self.timerTimeout)

    def enter(self):
        self.updeter.start()
        self.showTimers()
        self.showSelectedTimerOrInfo()

    def showSelectedTimerOrInfo(self):
        if self.updeter.hasTimer():
            self.showSelectedTimer()
        else:
            self.showInfo()

    def showSelectedTimer(self):
        self.window.mainArea.setCurrentIndex(0)
        self.updeter.startUpdatingTimer()

    def leave(self):
        self.updeter.stopUpdating()
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
        elif e.key() == Qt.Key_Plus:
            self.addTimer()
        elif e.key() == Qt.Key_Minus:
            self.removeTimer()
        elif e.key() == Qt.Key_Period:
            self.window.changeState(States.VoiceCommand.VoiceCommand)
            self.window.List.clear()
        elif e.key() == Qt.Key_Slash:
            self.startTimer()
        elif e.key() == Qt.Key_Asterisk:
            if self.updeter.isRunning():
                self.pauseTimer()
            else:
                self.stopTimer()
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
            f"<p>Wrong key {e.key()}</p>"
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
            self.startTimerListUpdating()

    def startTimerListUpdating(self):
        self.window.List.clear()
        self.updeter.startUpdatingList()

    def showSelectedTimer(self):
        self.window.mainArea.setCurrentIndex(0)
        self.updeter.startUpdatingTimer()
    
    def selectTimer(self, id):
        self.updeter.changeTimer(self.window.timers.getTimer(id))
        self.selectedId = id
        self.id = 0
        self.idSize = 0
        self.window.statusbar.showMessage(f"timer selected {id}")

    def selectTimerVoice(self):
        dialog = ListenDialog(self.window, 'Listing to timer id...')
        if dialog.exec():
            timerID = self.minutes = w2n.word_to_num(dialog.getText())
            print(f"text from speech recognition: {timerID}")
            self.selectTimer(timerID)
        else:
            QMessageBox.critical(
            self.window,
            "Error",
            f"<p>{dialog.getError()}, timer not selected</p>"
            )

    def pauseTimer(self):
        self.window.timers.pauseTimer(self.selectedId)
        self.updeter.stopUpdatingTimer()

    def stopTimer(self):
        self.window.timers.stopTimer(self.selectedId)
        self.updeter.stopUpdatingTimer()
    
    def startTimer(self):
        self.window.timers.startTimer(self.selectedId)
        self.updeter.startUpdatingTimer()
        self.updeter.startUpdatingList()
    
    def addToId(self, number):
        self.id += self.idSize * 10 + number
        self.idSize += 1
        self.window.statusbar.showMessage(f'Timer id: {self.id}')
        
    def addTimer(self):
        addTimerDialog = AddTimerDialog(self.window)
        if addTimerDialog.exec():
            timerTitle = addTimerDialog.getTitle()
            print(f"text from speech recognition: {timerTitle}")
            time = addTimerDialog.getTime()
            print(f"time from dialog: {time}")
            self.selectedId = self.window.timers.addTimer(time, timerTitle)
            self.updeter.changeTimer(self.window.timers.getTimer(self.selectedId))
            self.showSelectedTimerOrInfo()
            self.showTimers()
        else:
            QMessageBox.critical(
            self.window,
            "Error",
            f"<p>{addTimerDialog.getError()}</p>"
            )    
    
    def removeTimer(self):
        self.window.timers.removeTimer(self.selectedId)
        if self.window.timers.count() == 0:
            self.updeter.stopUpdatingList()
    
    def updateMainArea(self, timer, fullTime):
        remainingTime = timer['timer'].remainingTime()
        progresBarValue = ((fullTime - remainingTime)/fullTime)*100
        self.window.timerProgressBar.setValue(progresBarValue)
        remainingTimeText = formatTime(remainingTime)
        self.window.remainingTimeText.setText(remainingTimeText)

    def updateTimerList(self):
        self.window.List.clear()
        timers = self.window.timers.getTimers()
        for timer in timers.values():
            remainingTimeText = formatTime(timer['timer'].remainingTime())
            self.window.List.addItem(f'Id: {timer["id"]}, Title:{timer["title"]}, {remainingTimeText}')

    def timerTimeout(self, timer):
        self.selectedId

class Updater(QThread):
    updateSelectedTimerSignal = pyqtSignal(object, int)
    updateTimerListSignal = pyqtSignal()

    def __init__(self, window, timer):
        super().__init__(window)
        self.window = window
        self.ifRun = False
        self.updateSelectedTimer = False
        self.updateList = False
        self.timer = timer
        
    def changeTimer(self, newTimer):
        print(f"new timer change {newTimer}")
        self.timer = newTimer
        self.fullTime = newTimer['time']
        self.window.timerTitleLabel.setText(newTimer['title'])
    
    def startUpdatingTimer(self):
        self.updateSelectedTimer = True

    def startUpdatingList(self):
        self.updateList = True

    def run(self):
        self.ifRun = True
        while self.ifRun:
            if self.hasTimer() and self.updateSelectedTimer:
                self.updateSelectedTimerSignal.emit(self.timer, self.fullTime)
            if self.updateList:
                self.updateTimerListSignal.emit()
            sleep(1)
    
    def stopUpdating(self):
        self.ifRun = False

    def stopUpdatingTimer(self):
        self.updateSelectedTimer = False 

    def stopUpdatingList(self):
        self.updateList = False
    
    def hasTimer(self):
        return self.timer is not None
    
def formatTime(ms):
    s=ms/1000
    m,s=divmod(s,60)
    h,m=divmod(m,60)
    d,h=divmod(h,24)
    return f"{h:02}:{m:02}:{s:02}"


class NoTimerSelected(Exception):
    pass