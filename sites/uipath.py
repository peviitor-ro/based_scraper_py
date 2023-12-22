from scraper_peviitor import Scraper, loadingData
from utils import show_jobs, translate_city
from getCounty import get_county

apiUrl = "https://careers.uipath.com/api/jobs?location=romania&stretch=50&stretchUnit=MILES&page=1&limit=100&country=Romania&sortBy=relevance&descending=false&internal=false"

scraper = Scraper(apiUrl)

jobs = scraper.getJson().get("jobs")

company = {"company": "UiPath"}
finalJobs = list()

for job in jobs:
    job = job.get("data")

    job_title = job.get("title")
    job_link = job.get("meta_data").get("canonical_url")
    city = translate_city(job.get("city"))
    county = get_county(city)
    remote = []

    if job.get("location_type") == "ANY":
        remote.append("Remote")

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city,
        "county": county,
        "remote": remote,
    })


loadingData(finalJobs, company.get("company"))   
show_jobs(finalJobs)