from scraper_peviitor import Scraper, Rules, loadingData
import uuid

url = "https://www.brd.ro/cariere"

#Cream o instanta a clasei Scraper
scraper = Scraper(url)
rules = Rules(scraper)

#Un set pentru a nu avea duplicate
company = {"company": "BRD"}
j = set()

#Cautam elementele care contin joburile 
elements = rules.getTags("div", {"class": "category-card"})

#Pentru fiecare categorie, extragem titlul si link-ul 
#Le adaugam intr-un set pentru a nu avea duplicate
for element in elements:
    #setam link-ul paginii
    jobCategory = "https://www.brd.ro" + element.find("a")["href"]
    scraper.url = jobCategory

    #Cautam elementele care contin joburile
    jobs = rules.getTags("div", {"class": "card"})

    for job in jobs:
        #Pentru fiecare job, extragem titlul si link-ul
        title = job.find("div", {"class": "card-header"}).text
        link = "https://www.brd.ro" + job.find("a")["href"]

        j.add((title, link))
finalJobs = list()

#Pentru fiecare job din set, extragem titlul si link-ul 
#Celelalte date le setam manual deoarce nu sunt afisate pe site
for job in j:
    id = uuid.uuid4()
    job_title = job[0]
    job_link = job[1]

    finalJobs.append(
        {
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": "Romania",
        }
    )
#Afisam numarul total de joburi gasite
print(finalJobs)

#Salvam datele in baza de date
loadingData(finalJobs, company.get("company"))