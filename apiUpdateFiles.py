import requests

url = "https://api.laurentiumarian.ro/scraper/based_scraper_py/"

r = requests.post(url, data = {"update": "true"})

response = r.json()

if response.get("succes"):
    print(response.get("succes"))
else:
    print(response.get("error"))