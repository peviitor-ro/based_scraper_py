from scraper_peviitor import Scraper, Rules, loadingData, ScraperSelenium
from selenium.webdriver import Chrome

import json
import time
import uuid
import os

#Folosim ScraperSelenium deoaarece joburile sunt incarcate prin AJAX
scraper = ScraperSelenium("https://careers.fedex.com/express-eu/jobs?lang=ro-RO&location=România&woe=12&stretch=10&stretchUnit=MILES&page=1&limit=100")
scraper.get()

time.sleep(5)

#Folosim Scraper pentru a extrage codul HTML
dom = scraper.getDom()

#Setam un nou scraper pentru a extrage joburile
scraper = Scraper()
scraper.soup = dom
rules = Rules(scraper)

#Extragem joburile
jobs = rules.getTags("a", {"class": "job-title-link"})

finaljobs = list()

#Iteram prin joburi si le adaugam in lista finaljobs
for job in jobs:
    id = uuid.uuid4()
    job_title = job.text
    job_link = "https://careers.fedex.com" + job.get("href")
    company = "FedEx"
    country = "Romania"
    city = "Romania"

    print(job_title + " " + city)

    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city,
    })

#Afisam numarul de joburi
print("Total jobs: " + str(len(finaljobs)))

#Salvam joburile in fisierul json/fedex.json
with open("json/fedex.json", "w") as f:
    json.dump(finaljobs, f, indent=4)

#Incarcam joburile in baza de date
apikey = os.environ.get("apikey")
loadingData(finaljobs, apikey, "FedEx")

