
import json
import os
import time
import requests
from dotenv import load_dotenv

class CurrencyExchanger:
    def __init__(self):
        
        def verify_rates_are_up_to_date():
            current_time = time.time()
            currency_timestamp = currency_data['timestamp']
            
            # Check if the currency rates are older than 1 day
            if current_time - currency_timestamp > 86400:
                return False
            return True
        
        def update_currency_rates():
            try:
                load_dotenv("../.env")
                api_url = os.getenv("EXCHANGE_API_URL")
                
                response = requests.get(api_url)
                currency_data = response.json()
                
                # Update the currency_data dictionary with the new data
                with open('currency_rates.json', 'w') as f:
                    json.dump(currency_data, f)
                return currency_data
            except:
                raise ValueError("Failed to retrieve the latest currency exchange rates.")
        
        # Load the JSON data from the currency_rates.json file
        with open('currency_rates.json', 'r') as f:
            currency_data = json.load(f)
            
        if not verify_rates_are_up_to_date():
            currency_data = update_currency_rates()

        # Extract the rates dictionary from the JSON data
        self.rates = currency_data['rates']
    
    def exchange(self, amount, from_currency, to_currency):
        # Check if input and output currencies are in the rates dictionary
        if from_currency not in self.rates or to_currency not in self.rates:
            raise ValueError("Currency not found in the exchange rates list.")

        # Conversion based on the input currency being the base currency (EUR)
        if from_currency == 'EUR':
            converted_amount = amount * self.rates[to_currency]
        elif to_currency == 'EUR':
            converted_amount = amount / self.rates[from_currency]
        else:
            # Convert the amount to EUR first, then to the target currency
            amount_in_eur = amount / self.rates[from_currency]
            converted_amount = amount_in_eur * self.rates[to_currency]
        
        return converted_amount
    