from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import time
import json 
import os

#Cream o instanta a clasei Scraper
url = "https://www.medlife.ro/cariere/lista-joburi"
scraper = Scraper(url)
rules = Rules(scraper)

#Luam numarul total de joburi
totalJobs = int(rules.getTag("div", {"class":"title-header-listing"}).find("p").text.split(" ")[0])

pageNumbers = [*range(0, totalJobs, 7 )]

finalJobs = list()

#Iteram prin fiecare pagina
for page in range(len(pageNumbers)):
    #Setam url-ul paginii
    pageurl = url + "/s/page/" + str(page)
    scraper.url = pageurl

    #Luam elementele de pe pagina
    elements = rules.getTags("div", {"class":"mc-hand-hover"})
    
    #Iteram prin fiecare element si luam informatiile
    for element in elements:
        id = uuid.uuid4()
        job_title = element.find("div", {"class":"card-title-joburi-detalii"}).find_all("div")[0].text
        job_link = element["onclick"].split("'")[1]
        company = "Medlife"
        country = "Romania"
        city = element.find("div", {"class":"detaii-job"}).find_all("div")[0].text.strip()
        print(job_title + " " + city)

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })

    time.sleep(3)

#Afisam numarul total de joburi
print(len(finalJobs))

#Salvam datele in fisierul medlife.json
with open("json/medlife.json", "w") as f:
    json.dump(finalJobs, f, indent=4)

apikey = os.environ.get("apikey")