from kitchenhelper_client.Singleton import Singleton
class BaseState(metaclass=Singleton):
    """
    Base state class - class is a Sigleton that sould remeber its state
    """
    def __init__(self, window):
        self.window = window

    def keyPressEvent(self, e):
        """
        Fuction will take of keboard actions in a state
        """
        pass

    def enter(self):
        """
        Actions to perform when entering a state
        """
        pass
    
    def leave(self):
        """
        Actions to perform when leaving a state 
        """
        pass