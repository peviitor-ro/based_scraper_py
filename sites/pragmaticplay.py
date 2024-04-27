from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()
url = "https://jobs.jobvite.com/pragmaticplay"

company = {"company": "PragmaticPlay"}
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find_all("tr")

for job in jobs:
    try:
        country = (
            job.find("td", {"class": "jv-job-list-location"}).text.split(",")[1].strip()
        )
    except:
        country = None

    if country == "Romania":
        job_title = job.find("td", {"class": "jv-job-list-name"}).text.strip()
        job_link = "https://jobs.jobvite.com" + job.find("a").get("href")
        city = translate_city(
            job.find("td", {"class": "jv-job-list-location"}).text.split(",")[0].strip()
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

publish_or_update(finalJobs)

logoUrl = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpPW3wkzEqzustHI4sHkexU14oanfsBQrtjMVDMXdT&s"
publish_logo(company.get("company"), logoUrl)
show_jobs(finalJobs)
