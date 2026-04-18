import requests
from bs4 import BeautifulSoup
from utils import publish_or_update, publish_logo, show_jobs, create_job, translate_city
from getCounty import GetCounty

_counties = GetCounty()
company = "Lenovo"
feed_url = "https://jobs.lenovo.com/en_US/careers/SearchJobs/Romania/feed/?jobRecordsPerPage=50"

feed = requests.get(feed_url, timeout=30).text
soup = BeautifulSoup(feed, "xml")

jobs = []

for item in soup.find_all("item"):
    job_title = item.find("title").text.strip()
    job_link = item.find("link").text.strip()

    try:
        detail_html = requests.get(job_link, timeout=30).text
        detail_soup = BeautifulSoup(detail_html, "html.parser")
    except Exception:
        continue

    labels = detail_soup.select(".article__content__view__field__label")
    values = detail_soup.select(".article__content__view__field__value")
    details = {
        label.get_text(" ", strip=True): value.get_text(" ", strip=True)
        for label, value in zip(labels, values)
    }

    country = details.get("Country/Region:") or details.get("Country/Region")
    if country != "Romania":
        continue

    city = translate_city((details.get("City:") or details.get("City") or "Bucharest").strip())
    if city == "Bucharest":
        city = "Bucuresti"
    county = _counties.get_county(city) or ["Bucuresti"]

    jobs.append(
        create_job(
            job_title=job_title,
            job_link=job_link,
            company=company,
            country="Romania",
            city=city,
            county=county,
        )
    )

publish_or_update(jobs)
publish_logo(
    company,
    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Lenovo_logo_2015.svg/512px-Lenovo_logo_2015.svg.png",
)
show_jobs(jobs)
