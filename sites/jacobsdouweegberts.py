from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty
import requests
from bs4 import BeautifulSoup


_counties = GetCounty()
url = "https://careers-ro.jdepeets.com/job-search/"

company = {"company": "Jacobsdouweegberts"}
finaljobs = []

headers = {"Accept-Language": "en-GB,en;q=0.9"}

response = requests.get(url, headers=headers, timeout=20)
soup = BeautifulSoup(response.text, "html.parser")
jobs = soup.select("div.article[data-job-id]")

for job in jobs:
    job_title = job.select_one("span.job-name-value").get_text(" ", strip=True)
    job_link = "https://careers-ro.jdepeets.com" + job.select_one("a.btn").get("href")
    city = translate_city(job.select_one("span.city-value").get_text(" ", strip=True))
    county = ["Bucuresti"] if city == "Bucuresti" or city == "Bucharest" else _counties.get_county(city)
    if city == "Bucharest":
        city = "Bucuresti"

    finaljobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": city,
            "county": county,
            "company": company.get("company"),
        }
    )

publish_or_update(finaljobs)

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/JDE_Peet%27s_box_logo.svg/1024px-JDE_Peet%27s_box_logo.svg.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
