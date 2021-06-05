from typing import Optional
from PyQt5.QtCore import Qt

from kitchenhelper_client.MainWindow import MainWindow
from kitchenhelper_client.States.Idle import Idle
from kitchenhelper_client.States.BaseState import BaseState

class Recipes(BaseState):
    def __init__(self, window: MainWindow):
        super().__init__(window)
        self.currentIndex = None

    def enter(self):
        self.window.mainArea.setCurrentIndex(1)
        self.recipes = self.window.dataStore.getAllRecipes()

        for i, recipe in enumerate(self.recipes):
            self.window.List.addItem(f'{i}: {recipe.title}')
    
    def leave(self):
        self.window.List.clear()

    def keyPressEvent(self, e):
        num_keys = [Qt.Key.Key_0, Qt.Key.Key_1, Qt.Key.Key_2, Qt.Key.Key_3, Qt.Key.Key_4,
                    Qt.Key.Key_5, Qt.Key.Key_6, Qt.Key.Key_7, Qt.Key.Key_8, Qt.Key.Key_9]

        index = num_keys.index(e.key())

        if index != -1:
            self.currentIndex = index

        elif self.currentIndex is not None:
            if e.key() == Qt.Key.Key_Up:
                self.currentIndex -= 1
            elif e.key() == Qt.Key.Key_Down:
                self.currentIndex += 1

        elif e.key() == Qt.Key.Key_Escape:
            self.window.List.clear()
            self.window.changeState(Idle)
    
    def selectRecipe(self, index: Optional[int]):
        if index is None:
            self.window.List.setCurrentRow(-1)
            self.showInfo()

        elif 0 <= index < len(self.recipes):
            self.window.List.setCurrentRow(index)
            self.displayRecipe(index)

    def displayRecipe(self, index):
        recipe = self.recipes[index]
        text = []

        if recipe.image is not None:
            text.append(f'<img src="{recipe.image}"></img>')
        
        text.append(f'<h1>{recipe.title}</h1>')

        if recipe.total_time is not None:
            text.append(f'<p>Time: {recipe.total_time}</p>')

        if recipe.yields is not None:
            text.append(f'<p>Yields: {recipe.yields}</p>')

        if recipe.ingredients is not None:
            text.append('<p>Ingredients:</p><ul>')
            for ingr in recipe.ingredients:
                text.append(f'<li>{ingr}</li>')
            text.append('</ul>')

        if recipe.instructions is not None:
            text.append(f'<p>{recipe.instructions}</p>')

        if recipe.nutrients is not None:
            text.append('<p>Nutrients:</p><ul>')
            for nutrient in recipe.nutrients:
                text.append(f'<li>{nutrient}</li>')
            text.append('</ul>')

        self.window.TextArea.setText(''.join(text))

    def showInfo(self):
        self.window.TextArea.setText(
            '<h1>Recipes</h1>'
            '<p>You can view a previously used recipe using number (0-9) or arrow keys</p>'
            '<p>You can also search for a new recipe by saying "Get a recipe for" and then a name of a dish</p>'
        )
