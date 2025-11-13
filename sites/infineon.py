from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()

start = 0
url = f"https://jobs.infineon.com/api/pcsx/search?domain=infineon.com&query=&location=Romania&start={start}&sort_by=distance&"

company = {"company": "Infineon"}
finaljobs = list()

scraper = Scraper()

scraper.get_from_url(url=url,type= "JSON", verify=False)
jobs = scraper.markup.get("data").get("positions")

while len(jobs) > 0:
    for job in jobs:
        job_title = job.get("name")
        job_link = "https://jobs.infineon.com" + job.get("positionUrl")
        city = [
            translate_city(location.split(",")[0])
            for location in job.get("standardizedLocations", [])
        ]
        county = [
            c for city_name in city for c in _counties.get_county(city_name) or []
        ]
        remote = [
            type.lower() for type in job.get("efcustomTextWorkplaceType", [])
        ]

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
    url = f"https://jobs.infineon.com/api/pcsx/search?domain=infineon.com&query=&location=Romania&start={start}&sort_by=distance&"
    scraper.get_from_url(url=url,type= "JSON", verify=False)
    jobs = scraper.markup.get("data").get("positions")

publish_or_update(finaljobs)

logoUrl = "https://www.infineon.com/frontend/release_2023-03/dist/resources/img/logo-mobile-en.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
