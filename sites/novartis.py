from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, translate_city, show_jobs
from getCounty import GetCounty

_counties = GetCounty()
url = "https://www.novartis.com/ro-ro/cariere/cauta-un-job?search_api_fulltext=&country%5B0%5D=LOC_RO&early_talent=All&page=0"

company = {"company": "Novartis"}
finaljobs = list()

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find("table", {"class": "views-table"}).find("tbody").find_all("tr")
page = 0

while True:
    try:
        for job in jobs:
            job_title = job.find("a").text.strip()
            job_link = "https://www.novartis.com" + job.find("a").get("href")
            city = translate_city(
                job.find(
                    "td", {"class": "views-field-field-job-work-location"}
                ).text.strip()
            )
            county = _counties.get_county(city)

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

        page += 1
        scraper.get_from_url(
            "https://www.novartis.com/ro-ro/cariere/cauta-un-job?search_api_fulltext=&country%5B0%5D=LOC_RO&early_talent=All&page="
            + str(page)
        )

        jobs = (
            scraper.find("table", {"class": "views-table"}).find("tbody").find_all("tr")
        )
    except:
        break

publish_or_update(finaljobs)

logoUrl = "https://www.novartis.com/ro-ro/themes/custom/nvs_arctic/logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
