from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://jobs.intel.com/en/search-jobs/Romania/599/2/798549/46/25/50/2"

company = {"company": "Intel"}
finalJobs = list()

scraper = Scraper()
scraper.session.headers.update({
    "Accept-Language": "en-GB,en;q=0.9",
})

scraper.url = url
rules = Rules(scraper)

jobs = rules.getTag("section", {"id": "search-results-list"}).findAll("li")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("h2").text.strip()
    job_link = "https://jobs.intel.com" + job.find("a").get("href")

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": "Romania"
    })

print(finalJobs)

loadingData(finalJobs, company.get("company"))

logoUrl = "https://tbcdn.talentbrew.com/company/599/gst-v1_0/img/logo/logo-intel-blue.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))