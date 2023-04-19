from scraper_peviitor import Scraper, loadingData, Rules
import uuid

url = "https://www.biofarm.ro/cariere/job-uri-disponibile"

scraper = Scraper(url)
rules = Rules(scraper)

jobs= rules.getTag("main", {"class": "site-main"}).find("ul").find_all("li")

finalJobs = list()

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("a").text.strip()
    job_link = job.find("a").get("href")
    company = "Biofarm"
    country = "Romania"
    city = "Romania"

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city
    })

    print(job_title + " -> " + city)

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Biofarm")