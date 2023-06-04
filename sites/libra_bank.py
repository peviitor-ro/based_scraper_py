from scraper_peviitor import Scraper, Rules, loadingData
import uuid

url = "https://www.librabank.ro/Cariere"

scraper = Scraper(url)
rules = Rules(scraper)

jobContainer = rules.getTags("div", {"class": "jobListing"})
jobs = list(jobContainer)[0].find_all("div", {"class": "card-body"})

finalJobs = list()

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("a").text.strip()
    job_link = "https://www.librabank.ro" + job.find("a").get("href")
    company = "LibraBank"
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

loadingData(finalJobs, "LibraBank")
