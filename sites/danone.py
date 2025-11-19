from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city, get_jobtype
from getCounty import GetCounty

_counties = GetCounty()
url = "https://careers.danone.com/content/corp/global/career-rebrand/global/en/jobs.results.html?10000_group.propertyvalues.property=jcr%3Acontent%2Fdata%2Fmaster%2Fcountry&10000_group.propertyvalues.operation=equals&10000_group.propertyvalues.66_values=Romania&10004_group.propertyvalues.property=jcr%3Acontent%2Fdata%2Fmaster%2Fcountry&10004_group.propertyvalues.operation=equals&10004_group.propertyvalues.66_values=Romania&layout=teaserList&p.offset=0&p.limit=12"

company = {"company": "Danone"}


scraper = Scraper()

scraper.get_from_url(url)


jobs = scraper.find_all("div", {"class": "dn-jobdetails__job-card"})


finalJobs = []

while jobs:
    for job in jobs:
        job_title = job.find("h3", {"class": "job-card__title"}).text.strip()
        job_url = "https://careers.danone.com" + job.find("a")["href"].strip()
        location = job.find("h4", {"class": "job-card__city"}).text.strip()
        city = translate_city(location.split(",")[0].strip())
        county = _counties.get_county(city)
        remote = get_jobtype(
            job.find("h4", {"class": "job-card__workFromHome"}).text.strip()
        )

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_url,
                "city": city,
                "country": "Romania",
                "county": county,
                "company": company.get("company"),
                "remote": remote,
            }
        )
    scraper.get_from_url(
        f"https://careers.danone.com/content/corp/global/career-rebrand/global/en/jobs.results.html?10000_group.propertyvalues.property=jcr%3Acontent%2Fdata%2Fmaster%2Fcountry&10000_group.propertyvalues.operation=equals&10000_group.propertyvalues.66_values=Romania&10004_group.propertyvalues.property=jcr%3Acontent%2Fdata%2Fmaster%2Fcountry&10004_group.propertyvalues.operation=equals&10004_group.propertyvalues.66_values=Romania&layout=teaserList&p.offset={len(finalJobs)}&p.limit=12"
    )
    jobs = scraper.find_all("div", {"class": "dn-jobdetails__job-card"})


publish_or_update(finalJobs)

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/1/13/DANONE_LOGO_VERTICAL.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
