from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty, remove_diacritics
from math import ceil

_counties = GetCounty()
url = "https://www.medlife.ro/cariere/lista-joburi"
scraper = Scraper()
scraper.get_from_url(url)

totalJobs = int(
    scraper.find("div", {"class": "title-header-listing"}).find("p").text.split(" ")[0]
)

pageNumbers = ceil(totalJobs / 7)

company = {"company": "Medlife"}
finalJobs = list()

elements = scraper.find_all("div", {"class": "mc-hand-hover"})

for page in range(pageNumbers):
    for element in elements:
        job_title = (
            element.find("div", {"class": "card-title-joburi-detalii"})
            .find_all("div")[0]
            .text
        )
        job_link = element["onclick"].split("'")[1]
        city = translate_city(
            remove_diacritics(
                element.find("div", {"class": "detaii-job"})
                .find_all("div")[0]
                .text.strip()
            )
        )
        county = _counties.get_county(city)

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
            }
        )
    pageurl = url + "/s/page/" + str(page)
    scraper.get_from_url(pageurl)
    elements = scraper.find_all("div", {"class": "mc-hand-hover"})

publish_or_update(finalJobs)

logo_url = "https://www.medlife.ro/cariere/sites/all/themes/cariere_medlife/images/logo-medlife.png"
publish_logo(company.get("company"), logo_url)
show_jobs(finalJobs)
