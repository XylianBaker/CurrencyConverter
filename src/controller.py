# Controller for the qt gui for the currency converter
# controller has a init, def and reset function
# Authors: Jan Kammellander
# Date: 21.11.2022 Version: 1.0
from PyQt6.QtWidgets import QApplication

from src import view
from src.model import CurrencyConverterFile, CurrencyConverterAPI


class Controller:
    def __init__(self):
        """
        The function __init__() is a constructor that initializes the model and view objects
        """
        # Initialize the model
        self.model_api = CurrencyConverterAPI("gqcj9s0B9RnMLkjXlMEcHoozSFE2842G")
        self.model_file = CurrencyConverterFile("../data/conversions.json")
        # Initialize the view
        self.view = view.View(self)
        self.view.show()
        self.view.set_currencies(self.model_api.get_currencies())
        self.view.set_current_currency(self.model_api.get_currencies())

    def change(self):
        """
        It changes the current currency and currencies in the view
        """
        # Get the input from the view
        api = self.view.get_api()
        # clear the current currency and currencies in the view
        self.view.clear_current_currency()
        self.view.clear_currencies()
        # Set the current currency and currencies in the view
        if api:
            self.view.set_current_currency(self.model_api.get_currencies())
            self.view.set_currencies(self.model_api.get_currencies())
        else:
            self.view.set_current_currency(self.model_file.get_currencies())
            self.view.set_currencies(self.model_file.get_currencies())

    def execute(self):
        """
        It executes the conversion and sets the current_currency and currencies either by api or file depending on
        the api checkbox in the view
        also print the happening event in the statusbar
        """
        # Get the input from the view
        value = self.view.get_input()
        current_currency = self.view.get_current_currency()
        to_currency = self.view.get_currencies()
        api = self.view.get_api()

        # Set the value, current currency, and currencies to convert to in the model
        if api:
            self.model_api.set_value(value)
            self.model_api.set_current_currency(current_currency)
            self.model_api.set_to_currency(to_currency)
            self.view.set_current_currency(self.model_api.get_currencies())
            self.view.set_currencies(self.model_api.get_currencies())
            # Convert the currencies
            result = self.model_api.__str__()
        else:
            self.model_file.set_value(value)
            self.model_file.set_current_currency(current_currency)
            self.model_file.set_to_currency(to_currency)
            self.view.set_current_currency(self.model_file.get_currencies())
            self.view.set_currencies(self.model_file.get_currencies())
            # Convert the currencies
            result = self.model_file.__str__()

        # Set the result in the view
        self.view.set_output(result)
        # Set the statusbar in the view
        self.view.set_text_statusbar("Umrechnung ausgeführt")

    def reset(self):
        """
        It resets the view and sets the statusbar text
        """
        # Reset the view
        self.view.reset()
        # Set the statusbar in the view
        self.view.set_text_statusbar("Zurückgesetzt")


# A main function that initializes the controller and the app.
if __name__ == '__main__':
    app = QApplication([])
    controller = Controller()
    app.exec()
