from scraper.Scraper import Scraper
from utils import (
    translate_city,
    acurate_city_and_county,
    publish_or_update,
    publish_logo,
    show_jobs,
)
from getCounty import GetCounty, remove_diacritics
from math import ceil

_counties = GetCounty()

url = "https://careers.eon.com/romania/go/Toate-joburile-din-Romania/3727401?utm_source=pagina-cariere-ro"
scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find("span", {"class": "paginationLabel"}).find_all("b")[1]
step = 25

totalJobs = ceil(int(jobs.text) / step)

company = {"company": "Eon"}
finalJobs = list()

acurate_city = acurate_city_and_county(
    Iasi={"city": "Iasi", "county": "Iasi"},
    Targu_Mures={"city": "Targu-Mures", "county": "Mures"},
)

# Pentru fiecare pagina, luam joburile si le adaugam in lista finalJobs
for page in range(totalJobs):
    pageurl = f"https://careers.eon.com/romania/go/Toate-joburile-din-Romania/3727401/{page * step}/?q=&sortColumn=referencedate&sortDirection=desc"
    scraper.get_from_url(pageurl)

    jobs = scraper.find_all("tr", {"class": "data-row"})

    for job in jobs:
        job_title = job.find("a").text
        job_link = "https://careers.eon.com" + job.find("a")["href"]
        city = translate_city(
            remove_diacritics(
                job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()
            )
        )

        job = {
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "company": company.get("company"),
        }

        if acurate_city.get(city.replace(" ", "_")):
            county = acurate_city.get(city.replace(" ", "_")).get("county")
            city = acurate_city.get(city.replace(" ", "_")).get("city")

            job["city"] = city
            job["county"] = county

        elif "Remote" in city:
            job["remote"] = ["Remote"]
            job["city"] = ""
            job["county"] = ""

        else:
            county = _counties.get_county(city)
            if not county:
                city = city.replace(" ", "-")
                county = _counties.get_county(city.replace(" ", "-"))
            job["city"] = city
            job["county"] = county

        finalJobs.append(job)

publish_or_update(finalJobs)

logoUrl = "https://www.eon-romania.ro/content/dam/eon/eon-romania-ro/logo/header_M.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
