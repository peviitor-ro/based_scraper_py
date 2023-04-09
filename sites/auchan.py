from scraper_peviitor import Scraper, ScraperSelenium, Rules, loadingData
from selenium.webdriver.common.by import By


import os
import time
import uuid
import json 

#Folosim ScraperSelenium pentru a putea naviga pe pagini
scraper = ScraperSelenium("https://cariere.auchan.ro/?_ga=2.139478582.44265217.1594377481-1024065221.1578324695/")
scraper.get()

#Asteptam sa se incarce pagina
firstPage = scraper.find_element(By.CSS_SELECTOR, "ul.k-pager-numbers > li > span")

#Restul paginilor
pages = scraper.find_elements(By.CSS_SELECTOR, "ul.k-pager-numbers > li > a")

print(len(pages))

finaljobs = list()

#Folosim Scraper pentru a putea extrage datele de pe pagina
#Extragem dom-ul
dom = scraper.getDom()
#Cream un nou scraper
pageScraper = Scraper()
#Setam dom-ul pe noul scraper
pageScraper.soup = dom
#Cream un nou set de reguli
rules = Rules(pageScraper)

#Extragem elementul tbody
bodyElement = rules.getTag("tbody", {"role": "rowgroup"})
#Setam dom-ul pe noul scraper
pageScraper.soup = str(bodyElement)

#Extragem toate elementele tr
elements = rules.getTags("tr", {"role": "row"})
#Pentru fiecare element tr extragem datele
for element in elements:
    id = uuid.uuid4()
    job_title = element.find("a").text
    job_link = "https://cariere.auchan.ro/" + element.find("a")["href"]
    company = "Auchan"
    country = "Romania"
    city = element.find_all("td")[2].text

    print(job_title + " " + city)
    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city
    })
    
#Pentru restul paginilor
for page in range(len(pages)):
    #Asteptam sa se incarce pagina
    #Scrollam pana la pagina
    scraper.driver.execute_script("arguments[0].scrollIntoView();", pages[page])
    #Click pe pagina
    scraper.click(pages[page])
    #extragem elementele a
    pages = scraper.find_elements(By.CSS_SELECTOR, "ul.k-pager-numbers > li > a")
    #extragem dom-ul
    dom = scraper.getDom()
    #Cream un nou scraper
    pageScraper = Scraper()
    #Setam dom-ul pe noul scraper
    pageScraper.soup = dom
    #Cream un nou set de reguli
    rules = Rules(pageScraper)

    #Extragem elementul tbody
    bodyElement = rules.getTag("tbody", {"role": "rowgroup"})
    #Setam dom-ul pe noul scraper
    pageScraper.soup = str(bodyElement)

    #Extragem toate elementele tr
    elements = rules.getTags("tr", {"role": "row"})

    #Pentru fiecare element tr extragem datele
    for element in elements:
        id = uuid.uuid4()
        job_title = element.find("a").text
        job_link = "https://cariere.auchan.ro/" + element.find("a")["href"]
        company = "Auchan"
        country = "Romania"
        city = element.find_all("td")[2].text

        print(job_title + " " + city)
        finaljobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })

    time.sleep(3)

#Afisam numarul total de joburi
print(len(finaljobs))

#Salvam datele in fisierul auchan.json
with open("json/auchan.json", "w") as f:
    json.dump(finaljobs, f, indent=4)

apikey = os.environ.get("apikey")

loadingData(finaljobs, apikey, "Auchan")