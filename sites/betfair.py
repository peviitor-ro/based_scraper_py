from scraper_peviitor import Scraper, Rules, loadingData

import uuid

url = "https://www.betfairromania.ro/find-a-job/?search=&country=Romania&pagesize=1000#results"

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("div", {"class": "card-job"})

finalJobs = list()

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("h2", {"class":"card-title"}).text.strip()
    job_link = "https://www.betfairromania.ro" + job.find("a").get("href")
    company = "Betfair"
    country = "Romania"
    city = job.find("li").text.split("-")[-1].strip()

    print(job_title + " -> " + city)

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city
    })

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Betfair")