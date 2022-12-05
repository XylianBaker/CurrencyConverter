# View for the qt gui for the file gui.ui for the currency converter
# input for the value of the current currency is a double spin boy
# selection of the current currency is a combo box
# checkbox to convert from the api or from the local file
# Selection of the currency to convert to is a list widget
# output is a list view
# Authors: Jan Kammellander
# Date: 21.11.2022 Version: 1.0
from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt6.QtWidgets import *
from PyQt6 import uic

from src.controller import Controller


class View(QMainWindow):
    # A type hinting for the variables.
    input: QDoubleSpinBox
    current_currency: QComboBox
    api: QCheckBox
    currencies: QListWidget
    output: QTextBrowser

    def __init__(self, c: Controller):
        """
        The function loads the GUI from the file gui.ui, connects the buttons to the controller's execute and reset
        functions, and displays the GUI

        :param c: Controller
        :type c: controller
        """
        super().__init__()
        uic.loadUi("../data/gui.ui", self)
        self.api.stateChanged.connect(c.change)
        self.pB_execute.clicked.connect(c.execute)
        self.pB_reset.clicked.connect(c.reset)
        self.output.setReadOnly(True)

    def reset(self) -> None:
        """
        This function resets the input, current_currency, api, currencies, and output.
        """
        self.input.setValue(0)
        self.current_currency.setCurrentIndex(0)
        self.api.setChecked(False)
        self.currencies.clear()
        self.output.clear()

    def set_text_statusbar(self, text: str) -> None:
        """
        This function sets the text of the statusbar to the text passed in as a parameter

        :param text: The text to be displayed in the status bar
        :type text: str
        """
        self.statusbar.showMessage(text)

    def get_input(self) -> float:
        """
        This function returns the value of the input variable
        :return: The value of the input.
        """
        return self.input.value()

    def get_current_currency(self) -> str:
        """
        It returns the current currency that is selected in the dropdown menu
        :return: The current currency that is selected in the dropdown menu.
        """
        return self.current_currency.currentText()

    def get_api(self) -> bool:
        """
        This function returns a boolean value that indicates whether the checkbox is checked or not
        :return: The value of the checkbox.
        """
        return self.api.isChecked()

    def get_currencies(self) -> list:
        """
        It returns a list of the selected items in the currencies list
        :return: A list of strings.
        """
        items = self.currencies.selectedItems()
        return [item.text() for item in items]

    def set_currencies(self, currencies: list) -> None:
        """
        This function takes a list of currencies as an argument and adds them to the currencies list

        :param currencies: A list of currencies
        :type currencies: list
        """
        self.currencies.addItems(currencies)

    def set_current_currency(self, currencies: list) -> None:
        """
        This function takes a list of currencies as an argument and adds them to the current_currency list

        :param currencies: A list of currencies
        :type currencies: list
        """
        self.current_currency.addItems(currencies)

    def set_output(self, conversions: str) -> None:
        """
        This function takes a string as an argument and sets the output to the string

        :param conversions: The string to be displayed in the output
        :type conversions: str
        """
        self.output.setText(conversions)

    def clear_current_currency(self):
        """
        This function clears the current_currency list
        """
        self.current_currency.clear()

    def clear_currencies(self):
        """
        This function clears the currencies list
        """
        self.currencies.clear()


# The main function of the program. It creates an instance of the QApplication class and executes the
# program.
if __name__ == '__main__':
    app = QApplication([])
    view = View(Controller())
    view.show()
    app.exec()
