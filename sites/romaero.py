from scraper_peviitor import Scraper, Rules, loadingData
import uuid
url = "https://romaero.com/cariere/locuri-de-munca-romaero/"

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("tr")

company = {"company": "Romaero"}
finalJobs = list()

for job in jobs:
    try:
        id = uuid.uuid4()
        job_title = job.find("strong").text.strip()
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

print(finalJobs)

loadingData(finalJobs, company.get("company"))