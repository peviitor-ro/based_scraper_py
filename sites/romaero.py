from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://romaero.com/cariere/locuri-de-munca-romaero/"

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTag("table", {"id": "myTable"}).find("tbody").find_all("tr")

company = {"company": "Romaero"}
finalJobs = list()

for job in jobs:
    try:
        id = uuid.uuid4()
        try:
            job_title = job.find("strong").text.strip()
        except:
            job_title = job.find("b").text.strip()
        job_link = job.find("a").get("href")

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": "Romania"
        })
    except:
        pass

print(json.dumps(finalJobs, indent=4))
print(len(finalJobs))

loadingData(finalJobs, company.get("company"))