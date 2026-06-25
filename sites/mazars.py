from scraper.Scraper import Scraper
import json
import html
from utils import (
    translate_city,
    publish_or_update,
    publish_logo,
    show_jobs,
)
from getCounty import GetCounty

_counties = GetCounty()
url = "https://careers-ro.forvismazars.com/wp-json/wp/v2/job-offer"

company = {"company": "Mazars"}
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = scraper.markup

for job in jobs:
    job_title = html.unescape(job["title"]["rendered"])
    job_link = job["link"]

    loc_class = [c for c in job["class_list"] if c.startswith("location-")]
    city_name = loc_class[0].replace("location-", "") if loc_class else ""
    city_name = city_name.replace("-", " ").title()
    city = [translate_city(city_name)]

    if not city[0]:
        city = ["Bucuresti", "Cluj-Napoca"]

    counties = []

    for c in city:
        county = _counties.get_county(c) or []
        counties.extend(county)

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": city,
            "county": counties,
            "company": company.get("company"),
        }
    )

publish_or_update(finalJobs)

logoUrl = "https://www.mazarscareers.com/ro/wp-content/themes/mazars-2020/assets/images/mazars-logo.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
