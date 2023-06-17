from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://cariere.penny.ro/joburi/"
scraper = Scraper(url)
rules = Rules(scraper)

#Setam pagina pe care vrem sa o extragem
pageNum = 1 

#Cautam elementele care contin joburile si locatiile
jobs = rules.getTags("div", {"class": "job_position"})

company = {"company": "Penny"}
finalJobs = list()

#Pentru fiecare job, extragem titlul, link-ul, compania, tara si orasul
while jobs:
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("span", {"itemprop": "title"}).text.strip()
        job_link = job.find("a", {"itemprop": "url"}).get("href")

        try: 
            city = job.find("span", {"itemprop": "addressLocality"}).text.strip()
        except:
            city = "Romania"

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city
        })
    #Setam pagina urmatoare
    pageNum += 1
    #Setam link-ul paginii
    scraper.url = url + f"page/{pageNum}/"
    #Cautam elementele care contin joburile si locatiile
    jobs = rules.getTags("div", {"class": "job_position"})

#Afisam numarul total de joburi gasite
print(json.dumps(finalJobs, indent=4))

#Incarcam datele in baza de date
loadingData(finalJobs, company.get("company"))