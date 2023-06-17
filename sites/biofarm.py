from scraper_peviitor import Scraper, loadingData, Rules
import uuid
import json

url = "https://www.biofarm.ro/cariere/job-uri-disponibile"

scraper = Scraper(url)
rules = Rules(scraper)

jobs= rules.getTag("main", {"class": "site-main"}).find("ul").find_all("li")

company = {"company": "Biofarm"}
finalJobs = list()

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("a").text.strip()
    job_link = job.find("a").get("href")

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