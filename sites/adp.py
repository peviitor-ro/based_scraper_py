from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty, remove_diacritics
import json
import re

_counties = GetCounty()

url = "https://jobsapi-google.m-cloud.io/api/job/search?callback=jobsCallback&pageSize=100&companyName=companies%2Fc3f83ef5-c5b8-4d56-9c79-66f4052c4c4a&languageCode%5B%5D=en&customAttributeFilter=country%3D%22RO%22&orderBy=relevance%20desc"

company = {"company": "ADP"}
finalJobs = list()

headers = {"Content-Type": "application/json"}

scraper = Scraper()
scraper.set_headers(headers)

scraper.get_from_url(url, "HTML")
pattern = re.compile(r"jobsCallback\({(.*?)}\)", re.DOTALL)

data = re.search(pattern, scraper.text).group(1)
jobs = json.loads("{" + data + "}").get("searchResults")

# show_jobs(jobs)

for job in jobs:
    job_title = job.get("job").get("title")
    job_link = "https://jobs.adp.com/en/jobs/" + job.get("job").get("ref")
    locations = job.get("job").get("google_locations")

    cities = [
        translate_city(remove_diacritics(location.get("city")))
        for location in locations
        if location.get("country") == "RO"
    ]
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
        }
    )

publish_or_update(finalJobs)
logoUrl = "https://cdn-static.findly.com/wp-content/uploads/sites/794/2019/03/NewADP-redlogo.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)

