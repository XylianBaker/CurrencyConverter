# model for currency conversion to convert from a local file or from an api
# locally it converts from the file conversions.json
# api uses an api key
# Authors: Jan Kammellander
# Date: 21.11.2022 Version: 1.0

import json
from typing import List

import requests


# This class converts a value from one currency to another
class CurrencyConverter:
    def __init__(self, source: str):
        """
        This function takes a string as an argument and assigns it to the variable source

        :param source: The source of the currency
        :type source: str
        """
        self.to_currency = None
        self.current_currency = None
        self.value = None
        self.source = source

    def set_value(self, value: float):
        """
        This function sets the value

        :param value: The value
        :type value: float
        """
        self.value = value

    def set_current_currency(self, current_currency: str):
        """
        This function sets the current currency

        :param current_currency: The current currency
        :type current_currency: str
        """
        self.current_currency = current_currency

    def set_to_currency(self, to_currency: list):
        """
        This function sets the currencies to convert to

        :param to_currency: The currencies to convert to
        :type to_currency: list
        """
        self.to_currency = to_currency

    def convert(self) -> list:
        pass

    def get_currencies(self) -> list:
        """
        This function returns the currencies

        :return: The currencies
        :rtype: list
        """
        pass

    def __str__(self):
        pass


# This class is a subclass of the CurrencyConverter class, and it
# converts the value from the current currency to the to_currency.
class CurrencyConverterFile(CurrencyConverter):
    _conversion_dict: dict

    def __init__(self, source: str):
        """
        This function loads the conversion file and creates a dictionary of currencies

        :param source: The source of the data. This can be a URL or a file path
        :type source: str
        """
        super().__init__(source)
        self._conversion_dict = self.load_conversion_file()
        self.currencies = self.get_currencies()

    def load_conversion_file(self) -> dict:
        """
        This function loads the conversion file and returns the json file as a dictionary

        :return: The dictionary from the json file
        :rtype: dict
        """
        with open(self.source, "r") as f:
            return json.load(f)

    def convert(self) -> list:
        """
        It takes the value of the currency to be converted, the currency it is currently in, and the currency it is to be
        converted to, and returns the converted value, the currency it is now in, and the conversion rate
        :return: A list of tuples.
        """
        to_currency = [currency.lower() for currency in self.to_currency]
        # converted_amounts = [(self.value, self.current_currency)]
        converted_amounts = []
        for currency in to_currency:
            converted_amounts.append(
                (self._conversion_dict[currency]["rate"] * self.value, currency,
                 self._conversion_dict[currency]["rate"]))
            if currency == to_currency[-1]:
                converted_amounts.append(self._conversion_dict[currency]["date"])
        return converted_amounts

    def get_currencies(self) -> list:
        """
        This function returns a list of all the currencies that are supported by the currency converter
        :return: A list of the keys in the dictionary, sorted alphabetically.
        """
        return sorted([key.upper() for key in self._conversion_dict.keys()])

    def __str__(self):
        """
        It converts the value of the object into the currencies specified in the list of currencies and returns a list of
        tuples containing the converted value, the currency and the exchange rate
        :return: The return value is a string.
        """
        converted_amounts = self.convert()
        out = f"<b>{self.value} {self.current_currency.upper()}</b> entsprechen <br/><ul>"
        for converted_amount in converted_amounts:
            if converted_amount == converted_amounts[-1]:
                out += f"</ul><br/>Stand: {converted_amount}"
            else:
                out += f"<li><b>{converted_amount[0]} {converted_amount[1].upper()}</b> (Kurs: {converted_amount[2]})</li>"
        return out


# It takes in a value, a current currency, and a to currency, and returns a list of the response from the API
class CurrencyConverterAPI(CurrencyConverter):
    def __init__(self, source: str):
        """
        The function __init__() is a constructor that initializes the class CurrencyRates. It takes one argument, source,
        which is a string. The function calls the super() method, which is a built-in function that finds the superclass of
        the class and calls its constructor. The function then calls the get_currencies() method, which is a method of the
        superclass, and assigns the return value to the instance variable currencies.

        :param source: The source of the data
        :type source: str
        """
        super().__init__(source)
        self.currencies = self.get_currencies()

    def get_response(self, to_currency: str) -> list:
        """
        It takes the current currency and value of the object and converts it to the currency specified by the user

        :param to_currency: The currency you want to convert to
        :type to_currency: str
        :return: A list of dictionaries
        """
        base_url = "https://api.apilayer.com/exchangerates_data/convert"
        payload = {
            "to": to_currency,
            "from": self.current_currency,
            "amount": self.value
        }
        headers = {
            "apikey": self.source
        }
        response = requests.get(base_url, params=payload, headers=headers)
        response = response.json()
        return response

    def convert(self) -> list:
        """
        It takes the value and currency of the object, and converts it to the currencies specified in the to_currency list
        :return: A list of tuples.
        """
        converted_amounts = []
        for currency in self.to_currency:
            response = self.get_response(currency)
            converted_amounts.append((response["result"], currency, response["info"]["rate"],))
            # last response append is the time of the conversion
            if currency == self.to_currency[-1]:
                converted_amounts.append(response["date"])
        return converted_amounts

    def get_currencies(self) -> list:
        """
        It makes a GET request to the API endpoint, and returns a list of all the currencies that the API supports
        :return: A list of currencies
        """
        url = "https://api.apilayer.com/exchangerates_data/symbols"
        payload = {}
        headers = {
            "apikey": self.source
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        return sorted([key.upper() for key in response["symbols"].keys()])

    def __str__(self):
        """
        It converts the value of the object into the currencies specified in the list of currencies and returns a list of
        tuples containing the converted value, the currency and the exchange rate
        :return: The return value is a string.
        """
        converted_amounts = self.convert()
        out = f"<b>{self.value} {self.current_currency.upper()}</b> entsprechen <br/><ul>"
        for converted_amount in converted_amounts:
            if converted_amount == converted_amounts[-1]:
                out += f"</ul><br/>Stand: {converted_amount}"
            else:
                out += f"<li><b>{converted_amount[0]} {converted_amount[1].upper()}</b> (Kurs: {converted_amount[2]})</li>"
        return out


if __name__ == '__main__':
    # converter = CurrencyConverter("conversion_rates.json")
    converter = CurrencyConverterAPI("gqcj9s0B9RnMLkjXlMEcHoozSFE2842G")
    converter.value = 1000
    converter.current_currency = "usd"
    converter.to_currency = ["eur", "gbp"]
    print(converter)
