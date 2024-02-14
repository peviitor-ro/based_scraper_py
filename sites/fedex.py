from scraper_peviitor import Scraper
from utils import translate_city, publish, publish_logo, show_jobs
from getCounty import get_county

# Folosim ScraperSelenium deoaarece joburile sunt incarcate prin AJAX
url = "https://careers.fedex.com/api/jobs?lang=ro-RO&location=Rom%25C3%25A2nia&woe=12&stretch=10&stretchUnit=MILES&page=1&limit=100&sortBy=relevance&descending=false&internal=false&brand=FedEx%20Express%20EU"
scraper = Scraper(url)

jobs = scraper.getJson().get("jobs")

company = {"company": "FedEx"}
finaljobs = list()

# Iteram prin joburi si le adaugam in lista finaljobs
for job in jobs:
    obj = job.get("data")
    job_title = obj.get("title")
    job_link = obj.get("meta_data").get("canonical_url")
    city = translate_city(obj.get("city"))

    if city == "Judetul Cluj":
        city = "Cluj-Napoca"

    county = get_county(city)

    finaljobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
        }
    )

publish(4, company.get("company"), finaljobs, "Grasum_Key")

logoUrl = "https://1000logos.net/wp-content/uploads/2021/04/Fedex-logo-500x281.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
