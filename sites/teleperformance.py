from scraper_peviitor import Scraper
from utils import publish, publish_logo, show_jobs, translate_city
from getCounty import get_county

apiUrl = "https://www.teleperformance.com/Umbraco/Api/Careers/GetCareersBase?node=13761&country=Romania&pageSize=100"

company = {"company": "Teleperformance"}

scraper = Scraper(apiUrl)
jobs = scraper.getJson().get("resultado")

finalJobs = [
    {
        "job_title": job.get("title"),
        "job_link": job.get("url"),
        "company": company.get("company"),
        "country": "Romania",
        "city": translate_city(job.get("location")),
        "county": get_county(translate_city(job.get("location"))),
    }
    for job in jobs
]

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = "https://www.teleperformance.com/media/yn5lcxbl/tp-main-logo-svg.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
