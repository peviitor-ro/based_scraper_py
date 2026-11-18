import requests
from bs4 import BeautifulSoup
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()

url = "https://jobs.adp.com/en/jobs/xml/?rss=true"

company = {"company": "ADP"}
finalJobs = list()

response = requests.get(url, timeout=60)
response.raise_for_status()
soup = BeautifulSoup(response.text, "xml")

for job in soup.find_all("job"):
    country = job.find("country")
    if not country or country.get_text(strip=True) != "Romania":
        continue

    job_title = job.find("title").get_text(strip=True)
    job_link = job.find("url").get_text(strip=True)
    cities = [
        translate_city(remove_diacritics(location.get_text(strip=True)))
        for location in job.find_all("city")
        if location.get_text(strip=True)
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

