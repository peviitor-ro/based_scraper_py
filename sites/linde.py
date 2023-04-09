from scraper_peviitor import Scraper, Rules, loadingData, ScraperSelenium
from selenium.webdriver import Chrome

import time
import uuid
import json
import os

#Folosim ScraperSelenium deoarece joburile sunt incarcate prin AJAX
scraper = ScraperSelenium("https://linde.csod.com/ux/ats/careersite/20/home?c=linde&country=ro")
scraper.get()

time.sleep(5)

#Luam doom-ul
dom = scraper.getDom()

#Setam un nou scraper
scraper = Scraper()
scraper.soup = dom
rules = Rules(scraper)

#Luam toate joburile
jobs = rules.getTags('div', {'class': 'p-panel'})

j = set()

#Pentru fiecare job, luam titlul, link-ul si orasul si le adaugam intr-un set pentru a nu avea duplicate
for job in jobs:
    try:
        job_title = job.find('a', {"data-tag": "displayJobTitle"}).text
        job_link = "https://linde.csod.com" + job.find('a', {"data-tag": "displayJobTitle"})['href']
        city = job.find('p', {"data-tag": "displayJobLocation"}).text

        j.add((job_title, job_link, city))
    except:
        pass

finalJobs = list()

#Pentru fiecare job, cream un dictionar cu datele jobului si il adaugam intr-o lista
for job in j:
    id = uuid.uuid4()
    job_title = job[0]
    job_link = job[1]
    company = "Linde"
    country = "Romania"
    try:
        city = job[2].split(",")[0]
    except:
        city = "Romania"

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city
    })

#Afisam numarul de joburi gasite
print("Jobs found: " + str(len(finalJobs)))

#Salvam joburile in fisierul linde.json
with open("json/linde.json", "w") as f:
    json.dump(finalJobs, f, indent=4)

#Incarcam joburile in baza de date
apikey = os.environ.get("apikey")
loadingData(finalJobs, apikey, "Linde")