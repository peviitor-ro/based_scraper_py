from scraper.Scraper import Scraper
from utils import (publish, publish_logo, show_jobs)

url = "https://www.brd.ro/cariere"

#Cream o instanta a clasei Scraper
scraper = Scraper()
scraper.get_from_url(url, verify=False)

#Un set pentru a nu avea duplicate
company = {"company": "BRD"}
j = set()

#Cautam elementele care contin joburile 
elements = scraper.find_all("a", {"class": "category-card-link"})

#Pentru fiecare categorie, extragem titlul si link-ul 
#Le adaugam intr-un set pentru a nu avea duplicate
for element in elements:
    #setam link-ul paginii
    jobCategory = "https://www.brd.ro" + element["href"]
    scraper.get_from_url(jobCategory, verify=False)

    #Cautam elementele care contin joburile
    jobs = scraper.find_all("div", {"class": "card"})

    for job in jobs:
        #Pentru fiecare job, extragem titlul si link-ul
        title = job.find("div", {"class": "card-header"}).text
        link = "https://www.brd.ro" + job.find("a")["href"]

        j.add((title, link))
finalJobs = list()

#Pentru fiecare job din set, extragem titlul si link-ul 
#Celelalte date le setam manual deoarce nu sunt afisate pe site
for job in j:
    job_title = job[0]
    job_link = job[1]

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": "Romania",
        }
    )

for version in [1,4]:
    publish(version, company, finalJobs, 'APIKEY')

# publish_logo(company, "https://www.brd.ro/assets/images/logo-brd.svg")
show_jobs(finalJobs)