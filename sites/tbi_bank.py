from scraper_peviitor import Scraper, Rules, loadingData
import uuid

url = "https://tbibank.ro/cariere/"

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("div", {"class": "card-career"})

finalJobs = list()

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("div", {"class": "card-career__header"}).text.strip()
    job_link = job.find("a", {"class": "card-career__link"}).get("href")
    company = "TBIBank"
    country = "Romania"
    city = job.find("div", {"class": "card-career__countries"}).text.strip()

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

loadingData(finalJobs, "TBIBank")


