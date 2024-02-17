from scraper.Scraper import Scraper
from utils import show_jobs, publish, publish_logo, translate_city
from getCounty import get_county

company = "sapfioneer"
url = "https://jobs.workable.com/api/v1/companies/7gpSy323CcsUQ2Reb7x87t"

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
            city = translate_city(job["location"]["city"])
            county = get_county(city)

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
        url + "?pageToken=" + scraper.markup.get("nextPageToken"), "JSON"
    )
    jobs = scraper.markup.get("jobs")

publish(4, company, final_jobs, "APIKEY")

logourl = "https://workablehr.s3.amazonaws.com/uploads/account/logo/562664/logo"
publish_logo(company, logourl)

show_jobs(final_jobs)
