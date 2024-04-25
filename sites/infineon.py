from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()
url = "https://www.infineon.com/search/jobs/jobs"

company = {"company": "Infineon"}
finaljobs = list()

data = {
    "term": "",
    "offset":0,
    "max_results":100,
    "lang":"en",
    "country":"Romania"
}

scraper = Scraper()
scraper.set_headers(
    {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
)

response = scraper.post(url = url, data = data)

jobs = response.json().get("pages").get("items")

for job in jobs:
    job_title = job.get("title")
    job_link = "https://www.infineon.com" + job.get("detail_page_url")
    city = translate_city(job.get("location")[0])
    county = _counties.get_county(city)
    
    finaljobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": city,
        "county": county,
        "company": company.get("company")
    })

publish_or_update(finaljobs)

logoUrl = "https://www.infineon.com/frontend/release_2023-03/dist/resources/img/logo-mobile-en.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)