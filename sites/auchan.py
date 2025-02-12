from scraper.Scraper import Scraper
from utils import (
    create_job,
    publish_or_update,
    publish_logo,
    show_jobs,
    translate_city,
    acurate_city_and_county,
)
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()

company = "Auchan"
url = "https://cariere.auchan.ro/jobs?per_page=1000"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
}
scraper = Scraper()
scraper.set_headers(headers)
scraper.get_from_url(url)

jobs = list()
jobs_elements = scraper.find_all("a", class_="job")

acurate_city = acurate_city_and_county(
    Iasi={"city": "Iasi", "county": "Iasi"},
    Galati={"city": "Galati", "county": "Galati"},
)

for job in jobs_elements:
    try:
        city = translate_city(
            remove_diacritics(job.find("div", class_="js-job-oras").text.strip())
        )
    except Exception:
        city = ""
        
    county = ""

    if city in acurate_city.keys():
        city = acurate_city[city]["city"]
        county = acurate_city[city]["county"]
    else:
        county = _counties.get_county(city)

    jobs.append(
        create_job(
            job_title=job.find("div", class_="job-title").text,
            job_link=job["href"],
            company=company,
            country="Romania",
            city=city,
            county=county,
        )
    )

publish_or_update(jobs)
publish_logo(
    company,
    "https://res.cloudinary.com/smartdreamers/image/upload/v1685443347/company_logos/82780f0401d4b4b2097c8f79d13fa468.svg",
)
show_jobs(jobs)
