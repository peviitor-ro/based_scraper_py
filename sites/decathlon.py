from scraper_peviitor import Scraper, loadingData

import uuid
#Folosesc selenium deoarece joburile sunt incarcate prin ajax
scraper = Scraper('https://apply.workable.com//api/v1/widget/accounts/404273')
jobs = scraper.getJson().get('jobs')

finalJobs = list()

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get('title')
    job_link = job.get('url')
    company = "Decathlon"
    country = "Romania"
    city = job.get('city')
    
    print(job_title + " -> " + city)

    country = "Romania"
    finalJobs.append({
        'id': str(uuid.uuid4()),
        'job_title': job_title,
        'job_link': job_link,
        'company': company,
        'country': country,
        'city': city
    })


#Afisa numarul de joburi
print("Total jobs: " + str(len(finalJobs)))

#Incarc joburile in baza de date
loadingData(finalJobs, 'Decathlon')