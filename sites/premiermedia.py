from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty

_counties = GetCounty()
company = "premiermedia"
url = "https://jobs.workable.com/api/v1/jobs?location=Romania&query=Premier+Media"

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = scraper.markup.get("jobs")
final_jobs = []

while True:
    for job in jobs:
        job_title = job["title"]
        job_link = job["url"]
        remote = job["workplace"].replace("_", "-")
        city = translate_city(job["location"]["city"]) 

        if city:
            county = _counties.get_county(city)
        else:
            county = []

        final_jobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "remote": remote,
                "country": "Romania",
                "company": company,
                "city": city,
                "county": county,
            }
        )
    if not scraper.markup.get("nextPageToken"):
        break
    
    scraper.get_from_url(url + "&pageToken=" + scraper.markup.get("nextPageToken"), "JSON")
    jobs = scraper.markup.get("jobs")

publish_or_update(final_jobs)

logourl = "https://workablehr.s3.amazonaws.com/uploads/account/logo/581049/logo"
publish_logo(company, logourl)

show_jobs(final_jobs)
