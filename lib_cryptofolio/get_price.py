import subprocess
import json
import requests
import datetime
from currency_converter import CurrencyConverter

def coingecko_data(it=1,file_path=None):
    if file_path is not None:
        # Open the file in read mode
        with open(file_path, "r") as file:
            # Load the JSON data
            data = json.load(file)
    else:
        data=[]
        for i in range(it):
            # Define the curl command as a list of arguments
            curl_command = [
                'curl',
                '-X', 'GET',
                'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=250&page='+str(i)+'&sparkline=false&price_change_percentage=1h%2C24h%2C7d%2C30d%2C1y&locale=en'
            ]
            try:
                # Execute the curl command
                result = subprocess.run(curl_command, capture_output=True, text=True, check=True)

                # Parse JSON response
                data = data + json.loads(result.stdout)
            except subprocess.CalledProcessError as e:
                print("Error executing curl command:", e)
        # add crypto not found
        curl_command = [
                'curl',
                '-X', 'GET',        
                'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=orion-protocol%2Cdigibyte%2Cswissborg&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d%2C30d&locale=en'
        ]
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        data = data + json.loads(result.stdout)
        
    return data

def eurusd_change():
    c = CurrencyConverter()
    return c.convert(1, 'EUR', 'USD')

def get_price(coin_id,data):
    symbol_list = [d['symbol'] for d in data]
    return data[symbol_list.index(coin_id.lower())]['current_price']