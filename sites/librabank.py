from scraper.Scraper import Scraper
from utils import translate_city, acurate_city_and_county, publish_logo, publish_or_update, show_jobs
from getCounty import GetCounty
import re
import requests


def remove_words(text, words):
    for word in words:
        text = text.replace(word, "")
    return text


acurate_city = acurate_city_and_county(
    Iasi={
        "city": "Iasi",
        "county": "Iasi"
    }
)

url = "https://www.librabank.ro/Cariere"

_counties = GetCounty()
scraper = Scraper()
scraper.get_from_url(url, timeout=30, verify=False)

jobContainer = scraper.find_all("div", {"class": "jobListing"})
jobs = list(jobContainer)[0].find_all("div", {"class": "card-body"})

company = {"company": "LibraBank"}
finalJobs = list()


def get_salary(job_link):
    text = requests.get(job_link, timeout=20).text
    match = re.search(
        r"intervalul de\s*([0-9\.]+)\s*lei\s*brut\s*si\s*([0-9\.]+)\s*lei\s*brut",
        text,
        re.IGNORECASE,
    )

    if not match:
        return None, None, None

    salary_min = int(match.group(1).replace(".", ""))
    salary_max = int(match.group(2).replace(".", ""))
    return salary_min, salary_max, "RON"

for job in jobs:
    job_title = job.find("a").text.strip()
    job_link = "https://www.librabank.ro" + job.find("a").get("href")
    salary_min, salary_max, salary_currency = get_salary(job_link)

    location = remove_words(
        job_title.split(" - ")[-1].strip(), ["Sucursala", "Sucursale"]
    ).strip()
    city = ""
    county = ""
    accurate_location = acurate_city.get(location)

    if accurate_location:
        city = accurate_location["city"]
        county = accurate_location["county"]
    else:
        city = translate_city(location)
        county = _counties.get_county(city)

        if not county:
            city = "Bucuresti"
            county = "Bucuresti"

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city,
        "county": county,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "salary_currency": salary_currency,
    })

publish_or_update(finalJobs)

logo_url = "https://www.librabank.ro/imagini/logo-libra.svg"
publish_logo(company.get("company"), logo_url)
show_jobs(finalJobs)
