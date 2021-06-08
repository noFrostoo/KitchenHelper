from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from kitchenhelper_client import States
from kitchenhelper_client.pythonUi.ListenDialog import ListenDialog


class Recipes(States.BaseState.BaseState):
    def __init__(self, window):
        super().__init__(window)
        self.currentIndex = None

    def enter(self):
        self.window.mainArea.setCurrentIndex(1)
        self.window.List.clear()
        self.recipes = self.window.dataStore.getAllRecipes()

        for i, recipe in enumerate(self.recipes):
            self.window.List.addItem(f'{i}: {recipe.title}')

        self.selectRecipe()
    
    def leave(self):
        self.window.List.clear()

    def keyPressEvent(self, e):
        num_keys = [Qt.Key.Key_0, Qt.Key.Key_1, Qt.Key.Key_2, Qt.Key.Key_3, Qt.Key.Key_4,
                    Qt.Key.Key_5, Qt.Key.Key_6, Qt.Key.Key_7, Qt.Key.Key_8, Qt.Key.Key_9]

        try:
            self.currentIndex = num_keys.index(e.key())
        except ValueError:
            pass

        if self.currentIndex is not None:
            if e.key() == Qt.Key.Key_Up:
                self.currentIndex -= 1
            elif e.key() == Qt.Key.Key_Down:
                self.currentIndex += 1

        if e.key() == Qt.Key.Key_R:
            self.listenToDish()
        elif e.key() == Qt.Key.Key_Escape:
            self.window.List.clear()
            self.window.changeState(States.Idle.Idle)
            return
        elif e.key() == Qt.Key_Comma:
            self.window.List.clear()
            self.window.changeState(States.VoiceCommand.VoiceCommand)
            return

        self.selectRecipe()
    
    def selectRecipe(self):
        if self.currentIndex is None:
            self.window.List.setCurrentRow(-1)
            self.showInfo()

        elif 0 <= self.currentIndex < len(self.recipes):
            self.window.List.setCurrentRow(self.currentIndex)
            self.displayRecipe(self.currentIndex)

    def displayRecipe(self, index):
        recipe = self.recipes[index]
        text = []

        if recipe.image:
            img = self.window.dataStore.getImage(recipe.image)
            if img is not None:
                text.append(f'<img src="{str(img)}" height="400"></img>')
        
        text.append(f'<h1>{recipe.title}</h1>')

        if recipe.total_time:
            text.append(f'<p><b>Time:</b> {recipe.total_time}</p>')

        if recipe.yields:
            text.append(f'<p><b>Yields:</b> {recipe.yields}</p>')

        if recipe.ingredients:
            text.append('<p><b>Ingredients:</b></p><ul>')
            for ingr in recipe.ingredients:
                text.append(f'<li>{ingr}</li>')
            text.append('</ul>')

        if recipe.instructions:
            text.append(f'<p><b>Instructions:</b></p><p>{recipe.instructions}</p>')

        if recipe.nutrients:
            text.append('<p><b>Nutrients:</b></p><ul>')
            for nutr, value in recipe.nutrients.items():
                text.append(f'<li>{nutr}: {value}</li>')
            text.append('</ul>')

        self.window.TextArea.setText(''.join(text))

    def showInfo(self):
        self.window.TextArea.setText(
            '<h1>Recipes</h1>'
            '<p>You can view a previously used recipe using number (0-9) or arrow keys.</p>'
            '<p>You can search for a new recipe by using the "Get a recipe" voice command and then saying a name of a dish.</p>'
            '<p>You can also use the <i>R</i> key to trigger recipe search while on this page.</p>'
            '<p>Press <i>Esc</i> to exit to the main menu.</p>'
            '<p>You can activate voice command by clicking comma(,)</p>'
        )

    def listenToDish(self):
        dialog = ListenDialog(self.window)

        if dialog.exec():
            dish = dialog.getText()
            recipe = self.window.dataStore.getRecipe(dish)

            if recipe is None:
                QMessageBox.critical(
                    self.window,
                    'Recipe not found',
                    f'Could not find recipe for "{dish}"'
                )
                return
            
            self.enter()
            self.currentIndex = 0
            self.selectRecipe()
        else:
            QMessageBox.critical(
                self.window,
                'Error',
                f'{dialog.getError()}'
            )
