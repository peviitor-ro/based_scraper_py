from scraper_peviitor import ScraperSelenium, Scraper, Rules, loadingData
from selenium.webdriver.common.by import By

import os 
import json
import time
import uuid

#Folosim selenium deoarece anchorele cu nu au atributul href
scraper = ScraperSelenium("https://medicover.mingle.ro/en/apply")
scraper.get()

#Caut toate anchorele cu clasa btn-apply
anchors = scraper.find_elements(By.CLASS_NAME, "btn-apply")

#Instantiez un nou scraper pentru a extrage datele de pe pagina jobului
anchorPageScraper = Scraper()
rules = Rules(anchorPageScraper)

finalJobs = list()
idx = 0

while idx < len(anchors):
    #Scroll pana la ancorela curenta si apoi fac click pe ea
    anchor = anchors[idx]
    scraper.driver.execute_script("arguments[0].scrollIntoView();", anchor)
    time.sleep(1)
    scraper.click(anchor)

    time.sleep(1)
    #Incarc dom-ul paginii jobului in scraper
    anchorPageScraper.soup = scraper.getDom()

    #Extrag datele de pe pagina jobului
    id = uuid.uuid4()
    job_title = rules.getTag("title").text
    job_link = scraper.driver.current_url
    company = "Medicover"
    country = "Romania"
    cities = []
    
    #Caut div-ul cu clasa py-2 d-flex flex-nowrap si extrag orasele
    try:
        city = rules.getTag("div", {"class": "py-2 d-flex flex-nowrap"}).text
        if "," in city:
            cities = city.split(",")
        else:
            cities.append(city)
    except:
        cities = ["Romania"]

    #Adaug joburile in lista finala
    for city in cities:
        finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city.strip()
    })
        
    #Afisez jobul curent
    print(job_title + " " + city)
    
    #Inapoi la pagina principala
    scraper.driver.back()
    time.sleep(1)

    #Caut toate ancorele din nou
    anchors = scraper.find_elements(By.CLASS_NAME, "btn-apply")
    idx += 1

#Numarul de joburi gasite
print(len(finalJobs))

#Salvez joburile in fisierul medicover.json
with open("json/medicover.json", "w") as f:
    json.dump(finalJobs, f, indent=4)


apikey = os.environ.get("apikey")

loadingData(finalJobs, apikey, "Medicover")


