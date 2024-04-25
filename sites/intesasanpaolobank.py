from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()
url = "https://www.intesasanpaolobank.ro/en/persoane-fizice/Our-World/cariere.html"

company = {"company": "IntesaSanpaoloBank"}
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url)


jobs = scraper.find_all("article", {"class": "careersItem"})

for job in jobs:
    job_title = job.find("h2").text.strip()
    job_link = "https://www.intesasanpaolobank.ro" + job.find("a").get("href")
    locations = job.find("p").text.split("/")

    remote = ["Remote" for location in locations if "remote" in location.lower()]

    cities = [remove_diacritics(location.strip()) for location in locations]
    counties = []

    for city in cities:
        county = _counties.get_county(city)
        if county:
            counties.extend(county)

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": cities,
            "county": counties,
            "remote": remote,
        }
    )

publish_or_update(finalJobs)

logoUrl = "https://www.epromsystem.com/wp-content/uploads/2021/09/Clienti-INTESASP-epromsystem.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
