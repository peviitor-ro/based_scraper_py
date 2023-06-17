from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://www.betfairromania.ro/find-a-job/?search=&country=Romania&pagesize=1000#results"

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("div", {"class": "card-job"})

company = {"company": "Betfair"}
finalJobs = list()

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("h2", {"class":"card-title"}).text.strip()
    job_link = "https://www.betfairromania.ro" + job.find("a").get("href")
    city = job.find("li").text.split("-")[-1].strip()

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