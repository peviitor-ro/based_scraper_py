from scraper.Scraper import Scraper
from utils import publish, publish_logo, create_job, show_jobs, translate_city
from getCounty import get_county
from urllib.parse import quote

url = "https://careers.veeam.com/api/vacancy"

company = "Veeam"
jobs = []

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs_elements = scraper.markup

for job in jobs_elements:
    job_title = job["title"]
    job_link = "https://careers.veeam.com/vacancies/sales/" + quote(job["routeAlias"])
    cities = [
        translate_city(location["city"])
        for location in job["location"]
        if location["country"] == "Romania"
    ]
    counties = [get_county(translate_city(city)) for city in cities]
    if cities and counties:

        jobObj = create_job(
            job_title=job_title,
            job_link=job_link,
            company=company,
            country="Romania",
            city=cities,
            county=counties,
        )

        jobs.append(jobObj)


publish(4, company, jobs, "APIKEY")

publish_logo(company, "https://img.veeam.com/careers/logo/veeam/veeam_logo_bg.svg")
show_jobs(jobs)
