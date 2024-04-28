from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty

_counties = GetCounty()
company = "sapfioneer"
url = "https://jobs.workable.com/api/v1/jobs?location=Romania&query=sap+fioneer"

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = scraper.markup.get("jobs")
final_jobs = []

while scraper.markup.get("nextPageToken"):

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
    scraper.get_from_url(
        url + "&pageToken=" + scraper.markup.get("nextPageToken"), "JSON"
    )
    jobs = scraper.markup.get("jobs")

publish_or_update(final_jobs)

logourl = "https://workablehr.s3.amazonaws.com/uploads/account/logo/562664/logo"
publish_logo(company, logourl)

show_jobs(final_jobs)
