from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://www.librabank.ro/Cariere"

scraper = Scraper(url)
rules = Rules(scraper)

jobContainer = rules.getTags("div", {"class": "jobListing"})
jobs = list(jobContainer)[0].find_all("div", {"class": "card-body"})

company = {"company": "LibraBank"}
finalJobs = list()

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("a").text.strip()
    job_link = "https://www.librabank.ro" + job.find("a").get("href")

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": "Romania"
    })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))