import subprocess
import json
import requests
from currency_converter import CurrencyConverter
import datetime

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

    return data

def eurusd_change():
    c = CurrencyConverter()
    return c.convert(1, 'EUR', 'USD')