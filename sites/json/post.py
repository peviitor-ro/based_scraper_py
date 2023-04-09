import os
import json
import time
from scraper_peviitor import loadingData

path = os.path.dirname(os.path.abspath(__file__))
apikey = os.environ.get('apikey')

for site in os.listdir(path):
    if site.endswith(".json"):
        with open(os.path.join(path, site), 'r') as f:
            data = json.load(f)
            company = data[0]["company"]
            loadingData(data, apikey, company)
            time.sleep(2)

