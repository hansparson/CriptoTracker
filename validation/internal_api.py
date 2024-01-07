
import os
import traceback
import requests
import json

class InternalApi(object):
    def __init__(self, params='', headers='', payload='', list_coins=None):
        self.headers = headers
        self.payload = payload
        self.params = params
        self.coincap_url = os.getenv("COINCAP_URL")
        self.list_coins = list_coins

    
    def coincap_get_asset(self):
        try:
            end_point = 'v2/assets' 
            url = '{}/{}'.format(self.coincap_url, end_point)
            asset_crypto = requests.get(url,timeout=int(os.getenv("REQUEST_TIMOUT"))).json()
            print(asset_crypto)
            # Filtered data
            filtered_data = [entry for entry in asset_crypto['data'] if entry['id'] in self.list_coins]

            # Create a new dictionary with required keys
            result = []
            for entry in filtered_data:
                result.append({
                    "id": entry["id"],
                    "rank": entry["rank"],
                    "symbol": entry["symbol"],
                    "name": entry["name"],
                    "priceUsd": entry["priceUsd"],
                    "priceIdr": "{}".format(float(entry["priceUsd"]) * 15503.35)
                })

            # Convert the result to JSON
            result_json = json.dumps(result, indent=4)
            
            return True, json.loads(result_json)
        
        except:
            print(traceback.format_exc())
            return False, "TIMEOUT"