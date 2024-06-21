from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()
apiUrl = "https://www.teleperformance.com/Umbraco/Api/Careers/GetCareersBase?node=13761&country=Romania&pageSize=100"

company = {"company": "Teleperformance"}

scraper = Scraper()
scraper.set_headers({
    "Content-Type": "application/json",
})
scraper.get_from_url(apiUrl, "JSON")

finalJobs = [
    {
        "job_title": job.get("title"),
        "job_link": job.get("url"),
        "company": company.get("company"),
        "country": "Romania",
        "city": translate_city(job.get("location")),
        "county": _counties.get_county(translate_city(job.get("location"))),
    }
    for job in scraper.markup.get("resultado")
]

publish_or_update(finalJobs)

logoUrl = "https://www.teleperformance.com/media/yn5lcxbl/tp-main-logo-svg.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
