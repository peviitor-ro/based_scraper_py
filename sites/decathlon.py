from scraper_peviitor import Scraper, Rules, ScraperSelenium, loadingData
from selenium import webdriver

import uuid
import time
import os

#Folosesc selenium deoarece joburile sunt incarcate prin ajax
scraper = ScraperSelenium('https://cariere-decathlon.ro')
scraper.get()

#Iau dom-ul randat de browser
dom = scraper.getDom()


scraper = Scraper()
#incarc dom-ul in scraper
scraper.soup = dom

#Folosesc clasa Rules pentru a extrage joburile
rules = Rules(scraper)

#Iau toate h3-urile cu clasa whr-title
elements = rules.getTags('h3', {'class': 'whr-title'})

finalJobs = list()
idx = 0

#Pentru fiecare h3 extrag titlul si linkul
for elemen in elements:
    link = elemen.find('a')
    title = link.text

    #Deschid link-ul jobului in browser
    scraper.url = link['href']

    #Iau locatia jobului
    city = rules.getTag('span', {'data-ui': 'job-location'})

    try:
        location = city.text.split(',')[0]
    except:
        location = "Romania"
    
    print(title + " -> " + location)

    country = "Romania"
    finalJobs.append({
        'id': str(uuid.uuid4()),
        'job_title': title,
        'job_link': link['href'],
        'company': 'Decathlon',
        'country': country,
        'city': location,
    })

    time.sleep(3)

#Incarc joburile in baza de date
loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", 'Decathlon')