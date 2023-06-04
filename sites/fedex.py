from scraper_peviitor import Scraper, loadingData

import uuid

#Folosim ScraperSelenium deoaarece joburile sunt incarcate prin AJAX
url = 'https://careers.fedex.com/api/jobs?lang=ro-RO&location=Rom%25C3%25A2nia&woe=12&stretch=10&stretchUnit=MILES&page=1&limit=100&sortBy=relevance&descending=false&internal=false&brand=FedEx%20Express%20EU'
scraper = Scraper(url)

jobs = scraper.getJson().get('jobs')

finaljobs = list()

#Iteram prin joburi si le adaugam in lista finaljobs
for job in jobs:
    obj = job.get('data')
    id = uuid.uuid4()
    job_title = obj.get('title')
    job_link = obj.get('meta_data').get('canonical_url')
    company = "FedEx"
    country = "Romania"
    city = obj.get("city")

    print(job_title + " -> " + city)

    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city,
    })

#Afisam numarul de joburi
print("Total jobs: " + str(len(finaljobs)))

#Incarcam joburile in baza de date
loadingData(finaljobs, "FedEx")

