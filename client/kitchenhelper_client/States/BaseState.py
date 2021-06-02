from kitchenhelper_client.Singleton import Singleton
class BaseState(metaclass=Singleton):
    def __init__(self, window):
        self.window = window

    def keyPressEvent(self, e):
        pass

    def enter(self):
        pass
    
    def leave(self):
        pass