from scraper_peviitor import Scraper, Rules, loadingData
import time
import uuid
import json
import os

url = "https://www.brd.ro/cariere"

#Cream o instanta a clasei Scraper
scraper = Scraper(url)
rules = Rules(scraper)

#Un set pentru a nu avea duplicate
j = set()

#Cautam elementele care contin joburile 
elements = rules.getTags("div", {"class": "category-card"})

#Pentru fiecare categorie, extragem titlul si link-ul 
#Le adaugam intr-un set pentru a nu avea duplicate
for element in elements:
    #setam link-ul paginii
    jobCategory = "https://www.brd.ro" + element.find("a")["href"]
    scraper.url = jobCategory

    time.sleep(2)

    #Cautam elementele care contin joburile
    jobs = rules.getTags("div", {"class": "card"})

    for job in jobs:
        #Pentru fiecare job, extragem titlul si link-ul
        title = job.find("div", {"class": "card-header"}).text
        link = "https://www.brd.ro" + job.find("a")["href"]

        j.add(
            (
                title,
                link,
            )
        )
finalJobs = list()

#Pentru fiecare job din set, extragem titlul si link-ul 
#Celelalte date le setam manual deoarce nu sunt afisate pe site
for job in j:
    id = uuid.uuid4()
    job_title = job[0]
    job_link = job[1]
    company = "BRD"
    country = "Romania"
    city = "Romania"

    finalJobs.append(
        {
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city,
        }
    )
    print(job_title + " " + city)

#Afisam numarul total de joburi gasite
print(len(finalJobs))

#Salvam joburile in fisierul brd.json
with open("json/brd.json", "w") as f:
    json.dump(finalJobs, f, indent=4)

apikey = os.environ.get("apikey")

loadingData(finalJobs, apikey, "BRD")