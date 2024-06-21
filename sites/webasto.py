from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty

_counties = GetCounty()

url = "https://jobs.webasto.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=RO&optionsFacetsDD_location=&optionsFacetsDD_dept=&optionsFacetsDD_shifttype="

company = {"company": "Webasto"}
finaljobs = list()

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find("table", {"id": "searchresults"}).find(
    "tbody").find_all("tr")

for job in jobs:
    job_title = job.find("a").text.strip()
    job_link = "https://jobs.webasto.com" + job.find("a").get("href")
    city = translate_city(
        job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()
    )
    county = _counties.get_county(city)
    
    finaljobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city,
        "county": county,
    })

publish_or_update(finaljobs)

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/8/81/Webasto_20xx_logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
