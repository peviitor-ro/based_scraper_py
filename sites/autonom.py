from urllib.parse import urljoin

from scraper.Scraper import Scraper
from getCounty import GetCounty, remove_diacritics
from utils import publish_or_update, publish_logo, show_jobs

_counties = GetCounty()
url = "https://www.autonom.ro/cariere"
alternate_url = "https://www.autonom.com/cariere"
ejobs_url = "https://www.ejobs.ro/company/autonom/28906"

company = {"company": "Autonom"}
acurate_city = {"Iasi": {"city": "Iasi", "county": "Iasi"}}


def get_county(city):
    if city in acurate_city:
        return acurate_city[city]["county"]

    county_result = _counties.get_county(city)
    return county_result[0] if county_result else None


def scrape_autonom(source_url):
    scraper = Scraper()
    scraper.get_from_url(source_url, verify=False)

    jobs = scraper.find_all("a", {"class": "box-listing-job"})
    jobs_list = []

    for job in jobs:
        job_title = job.find("p", {"class": "nume-listing-job"}).text
        job_link = job["href"].strip()

        locations = job.find_all("span", {"class": "locatie-job"})
        cities = [remove_diacritics(city.text) for city in locations]

        for city in cities:
            jobs_list.append(
                {
                    "job_title": job_title,
                    "job_link": job_link,
                    "company": company.get("company"),
                    "country": "Romania",
                    "city": city,
                    "county": get_county(city),
                }
            )

    return jobs_list


def scrape_ejobs():
    scraper = Scraper()
    scraper.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    }
    scraper.get_from_url(ejobs_url)

    jobs_list = []

    for card in scraper.select(".job-card-wrapper"):
        title_elem = card.select_one(".job-card-content-middle__title")
        link_elem = card.select_one(".job-card-content-middle__title a")
        if not title_elem or not link_elem:
            continue

        job_title = title_elem.get_text(" ", strip=True)
        job_link = urljoin("https://www.ejobs.ro", link_elem.get("href", ""))

        location = ""
        for info in card.select(".job-card-content-middle__info"):
            if "job-card-content-middle__info--darker" not in info.get("class", []):
                location = info.get_text(" ", strip=True)
                break

        cities = [
            remove_diacritics(city.strip())
            for city in location.split(",")
            if city.strip()
        ] or [""]

        for city in cities:
            jobs_list.append(
                {
                    "job_title": job_title,
                    "job_link": job_link,
                    "company": company.get("company"),
                    "country": "Romania",
                    "city": city,
                    "county": get_county(city) if city else None,
                }
            )

    return jobs_list


finalJobs = scrape_autonom(url)

if not finalJobs:
    finalJobs = scrape_autonom(alternate_url)

if not finalJobs:
    finalJobs = scrape_ejobs()

seen = set()
unique_jobs = []
for job in finalJobs:
    key = (job["job_title"], job["job_link"], job["city"])
    if key not in seen:
        seen.add(key)
        unique_jobs.append(job)

finalJobs = unique_jobs

publish_or_update(finalJobs)

logoUrl = "https://www.autonom.ro/assets/uploads/autonom_logo-high-res.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
