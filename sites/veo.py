from scraper.Scraper import Scraper
from utils import (
    translate_city,
    publish_or_update,
    publish_logo,
    show_jobs,
)
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()

url = "https://www.ejobs.ro/company/veo/161798"
page = 1

company = "VEO"
final_jobs = []

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find("ul", class_="companies-show-jobs__items").find_all(
    "div", class_="job-card"
)
while jobs:
    for job in jobs:
        job_title = job.find(
            "h2", class_="job-card-content-middle__title").text.strip()
        job_url = job.find(
            "h2", class_="job-card-content-middle__title").find("a")["href"]
        job_url = "https://www.ejobs.ro" + job_url

        locations = job.find(
            "div", class_="job-card-content-middle__info").text.strip().split(",") if job.find("div", class_="job-card-content-middle__info") else []

        locations.extend(
            job.find("span", class_="PartialList__Rest").get("title").split(
                ",") if job.find("span", class_="PartialList__Rest") else []
        )

        cities = []
        counties = []

        for location in locations:
            city = translate_city(remove_diacritics(
                location.replace("și alte  orașe", "").strip()))
            county = _counties.get_county(city) or []

            cities.append(city)
            counties.extend(county)

        final_jobs.append(
            {
                "job_title": job_title,
                "job_link": job_url,
                "city": cities,
                "county": list(set(counties)),
                "country": "Romania",
                "company": company,
            }
        )
    page += 1
    scraper.get_from_url(url + "/" + str(page))

    try:
        jobs = scraper.find("ul", class_="companies-show-jobs__items").find_all(
            "div", class_="job-card"
        )
    except AttributeError:
        break
        

publish_or_update(final_jobs)

publish_logo(company, "https://content.ejobs.ro/img/logos/1/161798.png")
show_jobs(final_jobs)
