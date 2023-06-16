from scraper_peviitor import Scraper, loadingData
import uuid

#Folosesc selenium deoarece joburile sunt incarcate prin ajax
scraper = Scraper('https://apply.workable.com//api/v1/widget/accounts/404273')
jobs = scraper.getJson().get('jobs')

company = {"company": "Decathlon"}
finalJobs = list()

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get('title')
    job_link = job.get('url')
    city = job.get('city')

    finalJobs.append({
        'id': str(uuid.uuid4()),
        'job_title': job_title,
        'job_link': job_link,
        'company': company.get('company'),
        'country': 'Romania',
        'city': city
    })


#Afisa numarul de joburi
print(finalJobs)

#Incarc joburile in baza de date
loadingData(finalJobs, company.get("company"))