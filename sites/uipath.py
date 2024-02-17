from scraper_peviitor import Scraper
from utils import show_jobs, translate_city, publish, publish_logo
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
    if not county:

        city = [
            translate_city(location.get("city"))
            for location in job.get("additional_locations")
        ]
        county = [get_county(city) for city in city]
    remote = []

    if job.get("location_type") == "ANY":
        remote.append("Remote")

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
            "remote": remote,
        }
    )


publish(4, company.get("company"), finalJobs, "APIKEY")

publish_logo(
    company.get("company"),
    "https://cms.jibecdn.com/prod/uipath/assets/HEADER-NAV_LOGO-en-us-1663079214804.svg",
)
show_jobs(finalJobs)
