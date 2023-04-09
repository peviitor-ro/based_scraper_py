from scraper_peviitor import Scraper, ScraperSelenium, Rules, loadingData
from selenium.webdriver.common.by import By

import time
import uuid
import json
import os


#Folosim ScraperSelenium deoarece numarul de joburi este incarcat prin AJAX
scraper = ScraperSelenium("https://careers.eon.com/romania/go/Toate-joburile-din-Romania/3727401?utm_source=pagina-cariere-ro")
scraper.get()

time.sleep(5)

#Luam numarul total de joburi
jobs = scraper.find_elements(By.CSS_SELECTOR, "span.paginationLabel > b")[1]
step = 25

#Calculam numarul de pagini
totalJobs = [*range(0, int(jobs.text), step)]

finalJobs = list()

#Pentru fiecare pagina, luam joburile si le adaugam in lista finalJobs
for page in totalJobs:
    pageurl = f"https://careers.eon.com/romania/go/Toate-joburile-din-Romania/3727401/{page}/?q=&sortColumn=referencedate&sortDirection=desc"
    pageScaper = Scraper(pageurl)
    rules = Rules(pageScaper)

    jobs = rules.getTags("tr", {"class": "data-row"})

    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("a").text
        job_link = "https://careers.eon.com" + job.find("a")["href"]
        company = "Eon"
        country = "Romania"
        city = job.find("span", {"class": "jobLocation"}).text.split(",")[0]
        print(job_title + " " + city.strip())

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city.strip(),
        })
    time.sleep(3)

#Afisam numarul de joburi extrase
print(len(finalJobs))

#Salvam joburile in fisierul eon.json
with open("json/eon.json", "w") as f:
    json.dump(finalJobs, f, indent=4)

#Incarcam joburile in baza de date
apikey = os.environ.get("apikey")

loadingData(finalJobs, apikey, "Eon")