from getCounty import GetCounty
from utils import translate_city, publish_logo, publish_or_update, show_jobs
import requests
from bs4 import BeautifulSoup


_counties = GetCounty()
url = "https://www.inetum.com/global/en/careers/jobs.html?f%5B0%5D=region%3A1068"

company = {"company": "Inetum"}
finalJobs = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

response = requests.get(url, headers=headers, timeout=20)
soup = BeautifulSoup(response.text, "html.parser")
jobs = soup.select('div.cmp-teaser.joboverviewlist__item[data-job-opening-country="Romania"]')

for job in jobs:
    job_title = job.select_one("h2.cmp-teaser__title").get_text(" ", strip=True)
    job_link = "https://www.inetum.com" + job.select_one("a.cmp-teaser__link").get("href")
    location_text = job.select_one("div.cmp-teaser__location").get_text(" ", strip=True)
    city = translate_city(location_text.split("-")[-1].strip())
    county = ["Bucuresti"] if city == "Bucharest" or city == "Bucuresti" else _counties.get_county(city)
    if city == "Bucharest":
        city = "Bucuresti"

    remote = []
    if job.get("data-job-opening-remote") == "Yes":
        remote.append("remote")
    if "hybrid" in job_title.lower():
        remote.append("hybrid")

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
            "remote": remote,
        }
    )


publish_or_update(finalJobs)

logoUrl = "https://vtlogo.com/wp-content/uploads/2021/05/inetum-vector-logo-small.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
