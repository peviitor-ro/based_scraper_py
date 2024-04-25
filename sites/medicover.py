from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()
url = "https://mingle.ro/api/boards/careers-page/jobs?company=medicover&page=0&pageSize=1000&sort="

scraper = Scraper()
scraper.set_headers({"Content-Type": "application/json"})
scraper.get_from_url(url, type="JSON")

company = {"company": "Medicover"}
finalJobs = list()

for job in scraper.markup.get("data").get("results"):
    job_title = job.get("title")
    job_link = "https://medicover.mingle.ro/en/apply/" + job.get("uid")
    cities = [
        translate_city(city.get("label")) for city in job.get("locations")
    ] or []

    counties = []
    for city in cities:
        county = _counties.get_county(city) or []
        counties.extend(county)

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": cities,
        "county": counties,
    })

publish_or_update(finalJobs)

logo_url = "https://upload.wikimedia.org/wikipedia/commons/d/d7/Logo-medicover.png"
publish_logo(company.get("company"), logo_url)
show_jobs(finalJobs)
