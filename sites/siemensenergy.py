from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty
from math import ceil

_counties = GetCounty()
url = "https://jobs.siemens-energy.com/en_US/jobs/Jobs/?29454=964547&29454_format=11381&listFilterMode=1&folderRecordsPerPage=20&folderOffset=0"

company = {"company": "SiemensEnergy"}
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url)

totalJobs = int(
    scraper.find("div", {"class": "list-controls__text__legend"})
    .text.split("of")[1]
    .replace("results", "")
    .strip()
)

pages = ceil(totalJobs / 20)

for page in range(pages):
    url = (
        "https://jobs.siemens-energy.com/en_US/jobs/Jobs/?29454=964547&29454_format=11381&listFilterMode=1&folderRecordsPerPage=20&folderOffset="
        + str(page * 20)
    )
    scraper.get_from_url(url)

    jobs = scraper.find_all("details", {"class": "article--result--container"})

    for job in jobs:
        locations = (
            job.find("div", {"class": "article__content"}).find("p").text.split(",")
        )
        country = locations[0].split(":")[-1].strip()
        if len(country.split("|")) == 1 and country.split("|")[0].strip() == "Romania":
            job_title = (
                job.find("div", {"class": "article__header__text"}).find("a").text.strip()
            )
            job_link = job.find("div", {"class": "article__header__text"}).find("a")["href"]

            city = translate_city(locations[2].strip())
            county = _counties.get_county(city) or []

            job = {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
            }

            finalJobs.append(job)

publish_or_update(finalJobs)

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Siemens_Energy_logo.svg/799px-Siemens_Energy_logo.svg.png?20200823090225"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
