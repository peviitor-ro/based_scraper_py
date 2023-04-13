from scraper_peviitor import Scraper, ScraperSelenium, Rules, loadingData

import json
import uuid

#url-ul paginii
url = "https://careers.allianz.com/tile-search-results?q=&locationsearch=Romania&searchby=location&d=15&"
#Numarul de rezultate de pe pagina
numberOfResults = 0

finaljobs = list()

#Cream un nou scraper
scraper = Scraper()
#Cream un nou obiect Rules
rules = Rules(scraper)

#Luam toate joburile

#Definim o variabila de iteratie
iteration = True

while iteration:
    #Setam url-ul paginii
    scraper.url = url + f"startrow={numberOfResults}"
    #Luam toate joburile
    elements = rules.getTags("li", {"class": "job-tile"})
    #Pentru fiecare job luam titlul, linkul, compania, tara si orasul
    for element in elements:
        id = uuid.uuid4()
        job_title = element.find("a").text.strip()
        job_link = "https://careers.allianz.com" + element.find("a").get("href")
        company = "Allianz"
        country = "Romania"
        city = "Romania"

        job = {
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city,
        }
        print(job_title + " -> " + city)

        #Verificam daca jobul exista deja in lista
        for j in finaljobs:
            if j["job_title"] == job_title and j["job_link"] == job_link:
                #Daca exista oprim iteratia
                iteration = False
                break
        
        #Daca nu exista il adaugam in lista
        if iteration:
            finaljobs.append(job)
    #Incrementam numarul de rezultate
    numberOfResults += 25

#Afisam numarul de total de joburi
print("Total jobs: " + str(len(finaljobs)))

#Incarcam datele in baza de date
loadingData(finaljobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Allianz")