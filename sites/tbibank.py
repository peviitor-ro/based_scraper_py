from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://tbibank.ro/cariere/"

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("div", {"class": "card-career"})

company = {"company": "TBIBank"}
finalJobs = list()

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("div", {"class": "card-career__header"}).text.strip()
    job_link = job.find("a", {"class": "card-career__link"}).get("href")
    city = job.find("div", {"class": "card-career__countries"}).text.strip()

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city
    })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))


