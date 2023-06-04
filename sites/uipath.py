from scraper_peviitor import Scraper, loadingData
import uuid

apiUrl = "https://careers.uipath.com/api/jobs?location=Romania&stretch=10&stretchUnit=MILES&page=1&limit=100&sortBy=relevance&descending=false&internal=false"

scraper = Scraper(apiUrl)

jobs = scraper.getJson().get("jobs")

finalJobs = list()

for job in jobs:
    job = job.get("data")
    country_code = job.get("country_code")
    if country_code == "RO":
        id = uuid.uuid4()
        job_title = job.get("title")
        job_link = job.get("meta_data").get("canonical_url")
        company = "UiPath"
        country = "Romania"
        city = job.get("city")

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

loadingData(finalJobs, "UiPath")