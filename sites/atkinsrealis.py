from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()
company = "atkinsrealis"
url = "https://careers.atkinsrealis.com/jobs?options=,6477&page="
page = 1

scraper = Scraper()
scraper.set_headers(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 91.0.4472.124 Safari/537.36",
    }
)

scraper.get_from_url(url + str(page), verify=False)

jobs = []
jobs_elements = scraper.find("div", class_="attrax-list-widget__lists").find_all(
    "div", class_="attrax-vacancy-tile")

while True:
    for job in jobs_elements:

        job_title = job.find(
            "a", class_="attrax-vacancy-tile__title").text.strip()
        job_link = (
            "https://careers.atkinsrealis.com"
            + job.find("a", class_="attrax-vacancy-tile__title")["href"]
        )
        city = translate_city(
            job.find(
                "div", class_="attrax-vacancy-tile__option-location-valueset"
            ).text.strip()
        )

        county = _counties.get_county(city) or []

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                city=city,
                county=county,
                company=company,
                country="Romania",
            )
        )

    page += 1
    scraper.get_from_url(url + str(page), verify=False)
    try:
        jobs_elements = scraper.find(
            "div", class_="attrax-list-widget__lists"
        ).find_all("div", class_="attrax-vacancy-tile")
    except AttributeError:
        break

publish_or_update(jobs)

publish_logo(
    company,
    "https://attraxcdnprod1-freshed3dgayb7c3.z01.azurefd.net/1481103/1e2dbbdd-b55c-47cb-941b-4ecd47e8f5ef/2023.17000.541/Blob/img/snc-logo.png",
)
show_jobs(jobs)
