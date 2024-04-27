from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty
from math import ceil

_counties = GetCounty()
url = "https://ptc.eightfold.ai/api/apply/v2/jobs?domain=ptc.com&start=0&location=Bucharest%2C%20Romania&domain=ptc.com&sort_by=relevance"

company = {"company": "PTC"}
finalJobs = list()

scraper = Scraper()

scraper.get_from_url(url, "JSON")

pages = ceil(scraper.markup.get("count") / 10)

for page in range(pages):
    scraper.get_from_url(url.replace("start=0", "start=" + str(page * 10)), "JSON")
    jobs = scraper.markup.get("positions")
    for job in jobs:
        job_title = job.get("name")
        job_link = "https://ptc.eightfold.ai/careers?pid=" + str(job.get("id")) + "&domain=ptc.com&sort_by=relevance"
        city = translate_city(job.get("location").split(",")[0])
        county = _counties.get_county(city) or []
        
        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": city,
            "county": county,
            "company": company.get("company")
        })
publish_or_update(finalJobs)

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/PTC_logo.svg/1280px-PTC_logo.svg.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
