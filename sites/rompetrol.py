from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty, remove_diacritics
from math import ceil

_counties = GetCounty()
url = "https://careers.rompetrol.com/search/?q=&locationsearch=Romania"
scraper = Scraper(url)
scraper.get_from_url(url)

jobs = int(scraper.find("span", {"class": "paginationLabel"}).find_all("b")[1].text)

queryList = ceil(jobs / 25)

company = {"company": "Rompetrol"}
finaljobs = list()

for query in range(queryList):
    url = (
        "https://careers.rompetrol.com/search/?q=&locationsearch=Romania&startrow="
        + str(query * 25)
    )
    scraper.get_from_url(url)

    jobs = scraper.find_all("tr", {"class": "data-row"})

    for job in jobs:
        job_title = job.find("a").text
        job_link = "https://careers.rompetrol.com" + job.find("a")["href"]
        city = translate_city(
            job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()
        )
        county = _counties.get_county(city) or []

        finaljobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
            }
        )
publish_or_update(finaljobs)

logo_url = "https://www.rompetrol.com/upload/photos/rompetrol_2961.png"
publish_logo(company.get("company"), logo_url)
show_jobs(finaljobs)
