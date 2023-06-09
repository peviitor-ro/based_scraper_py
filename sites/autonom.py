from scraper_peviitor import Scraper, Rules, loadingData
import uuid 
import json

url = "https://www.autonom.ro/cariere"

scraper = Scraper(url)
rules = Rules(scraper)

#Obtinem toate joburile
jobs = rules.getTags('a', {'class': 'box-listing-job'})

company = {"company": "Autonom"}
finalJobs = list()

#Pentru fiecare job, extragem datele si le adaugam in lista finalJobs
for job in jobs:
    id = uuid.uuid4()
    job_title = job.find('p', {"class":"nume-listing-job"}).text
    job_link = job['href']
    city = job.find_all('span', {"class":"locatie-job"})

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city[0].text,
    })

#Afisam numarul de joburi
print(json.dumps(finalJobs, indent=4))

#Incarcam datele in baza de date
loadingData(finalJobs, company.get("company"))