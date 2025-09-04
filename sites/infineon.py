from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city, get_jobtype
from getCounty import GetCounty

_counties = GetCounty()

start = 0
num = 10

url = f"https://jobs.infineon.com/api/apply/v2/jobs?domain=infineon.com&start={start}&num={num}&location=Romania&pid=563808958979269&domain=infineon.com&sort_by=relevance&triggerGoButton=false"

company = {"company": "Infineon"}
finaljobs = list()

scraper = Scraper()

scraper.get_from_url(url=url,type= "JSON", verify=False)
jobs = scraper.markup.get("positions")

while len(jobs) > 0:
    for job in jobs:
        job_title = job.get("name")
        job_link = job.get("canonicalPositionUrl")
        city = translate_city(job.get("location").split(" ")[0].strip())
        county = _counties.get_county(city)
        remote = get_jobtype(job.get("work_location_option"))

        finaljobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": city,
            "county": county,
            "company": company.get("company"),
            "remote": remote
        })

    start += 10
    url = f"https://jobs.infineon.com/api/apply/v2/jobs?domain=infineon.com&start={start}&num={num}&location=Romania&pid=563808958979269&domain=infineon.com&sort_by=relevance&triggerGoButton=false"
    scraper.get_from_url(url=url,type= "JSON", verify=False)
    jobs = scraper.markup.get("positions")

publish_or_update(finaljobs)

logoUrl = "https://www.infineon.com/frontend/release_2023-03/dist/resources/img/logo-mobile-en.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
