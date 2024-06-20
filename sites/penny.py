from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty

_counties = GetCounty()
url = "https://cariere.penny.ro/joburi/"
scraper = Scraper()
scraper.get_from_url(url)

pageNum = 1

jobs = scraper.find_all("div", {"class": "job_position"})

company = {"company": "Penny"}
finalJobs = list()

while jobs:
    for job in jobs:
        job_title = job.find("span", {"itemprop": "title"}).text.strip()
        job_link = job.find("a", {"itemprop": "url"}).get("href")

        try:
            city = (
                job.find("span", {"itemprop": "addressLocality"})
                .text.strip()
                .replace("-", " ")
                .title()
                .replace("De", "de")
            )
        except:
            city = ""

        if "Sector" in city:
            city = city.split("Sector")[0].strip()

        county = _counties.get_county(city) or []

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

    pageNum += 1
    scraper.get_from_url(url + f"page/{pageNum}/")
    jobs = scraper.find_all("div", {"class": "job_position"})

publish_or_update(finalJobs)

logo_url = "https://cariere.penny.ro/wp-content/themes/penny_cariere/img/logo.jpg"
publish_logo(company.get("company"), logo_url)
show_jobs(finalJobs)
