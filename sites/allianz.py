from scraper_peviitor import Scraper, ScraperSelenium, Rules, loadingData
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os 
import time
import uuid
import json

#Folosim ScraperSelenium pentru ca siteul incarca elementele prin AJAX
url = "https://careers.allianz.com/en_US.html/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_department=&optionsFacetsDD_shifttype=&optionsFacetsDD_customfield3=&optionsFacetsDD_customfield2=&optionsFacetsDD_facility=&optionsFacetsDD_customfield4=&inputSearchValue=Romania&quatFlag=false"
scraper = ScraperSelenium(url)
scraper.get()

#Asteptam sa se incarce cookie-ul
scraper.wait(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))

#Acceptam cookie-ul
cookieBtn = scraper.find_element(By.ID, "onetrust-accept-btn-handler")
scraper.click(cookieBtn)

finaljobs = list()

#Asteptam sa se incarce elementele
while True:
    #Luam DOM-ul
    dom = scraper.getDom()

    #Cream un nou scraper
    pageScraper = Scraper()
    #Setam DOM-ul
    pageScraper.soup = dom
    #Cream un nou obiect Rules
    rules = Rules(pageScraper)

    #Luam toate joburile
    elements = rules.getTags("tbody")

    #Pentru fiecare job luam titlul, linkul, compania, tara si orasul
    for element in elements:
        id = uuid.uuid4()
        job_title = element.find("a").text
        job_link = "https://careers.allianz.com" + element.find("a")["href"]
        company = "Allianz"
        country = "Romania"
        city = "Romania"

        print(element.find("a").text)

        finaljobs.append(
            {
                "id": str(id),
                "job_title": job_title,
                "job_link": job_link,
                "company": company,
                "country": country,
                "city": city,
            }
        )

    #Cautam butonul de next
    nextPage = scraper.find_element(By.CLASS_NAME, "nx-pagination__link--next")
    #Scrollam pana la buton
    scraper.driver.execute_script("arguments[0].scrollIntoView();", nextPage)

    #Daca butonul este disabled inseamna ca nu mai avem pagini
    if "is-disabled" in nextPage.get_attribute("class"):
        break

    #Daca nu este disabled, apasam pe el
    scraper.click(nextPage)
    time.sleep(3)

#Afisam numarul de total de joburi
print(len(finaljobs))

#Salvam joburile in fisierul allianz.json
with open("json/allianz.json", "w") as f:
    json.dump(finaljobs, f, indent=4)

apikey = os.environ.get("apikey")

loadingData(finaljobs, apikey, "Allianz")