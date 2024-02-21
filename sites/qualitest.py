from scraper.Scraper import Scraper
from utils import show_jobs, publish, publish_logo, translate_city

company = "qualitest"
url = "https://jobs.workable.com/api/v1/companies/piDJ4xBDdP6LcySpBX7LvY"

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = scraper.markup.get("jobs")
final_jobs = []

while scraper.markup.get("nextPageToken"):

    for job in jobs:
        job_title = job["title"]
        job_link = job["url"]
        remote = job["workplace"].replace("_", "-")

        if job["location"]["countryName"] == "Romania":
            final_jobs.append(
                {
                    "job_title": job_title,
                    "job_link": job_link,
                    "remote": remote,
                    "country": "Romania",
                    "company": company,
                    "city": (
                        translate_city(job["location"]["city"])
                        if job["location"]["city"]
                        else []
                    ),
                    "county": (
                        translate_city(
                            job["location"]["subregion"].replace("County", "").strip()
                        )
                        if job["location"]["subregion"]
                        else []
                    ),
                }
            )
    scraper.get_from_url(
        url + "?pageToken=" + scraper.markup.get("nextPageToken"), "JSON"
    )
    jobs = scraper.markup.get("jobs")

publish(4, company, final_jobs, "APIKEY")

logourl = "https://static.otta.com/uploads/images/company-logos/12608-VWKbfxnEMQpPk5I5aK7oBSr36vMu7zE5VwQkcV6-KE4.png"
publish_logo(company, logourl)

show_jobs(final_jobs)
