from scraper_peviitor import Scraper, loadingData
import uuid
import json

#Folosim ScraperSelenium deoaarece joburile sunt incarcate prin AJAX
url = 'https://careers.fedex.com/api/jobs?lang=ro-RO&location=Rom%25C3%25A2nia&woe=12&stretch=10&stretchUnit=MILES&page=1&limit=100&sortBy=relevance&descending=false&internal=false&brand=FedEx%20Express%20EU'
scraper = Scraper(url)

jobs = scraper.getJson().get('jobs')

company = {"company": "FedEx"}
finaljobs = list()

#Iteram prin joburi si le adaugam in lista finaljobs
for job in jobs:
    obj = job.get('data')
    id = uuid.uuid4()
    job_title = obj.get('title')
    job_link = obj.get('meta_data').get('canonical_url')
    city = obj.get("city")

    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city,
    })

#Afisam numarul de joburi
print(json.dumps(finaljobs, indent=4))

#Incarcam joburile in baza de date
loadingData(finaljobs, company.get("company"))