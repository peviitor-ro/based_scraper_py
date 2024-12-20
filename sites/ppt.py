from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty, remove_diacritics
from scraper.Scraper import Scraper

_counties = GetCounty()


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url)

    locations = scraper.find("meta", {"data-hid": "jobs-show-main-summaries__summary-value jobs-show-main-summaries__summary-location"})[
        "content"
    ].split(",")

    cities = []
    counties = list()

    for location in locations:
        city = translate_city(remove_diacritics(location.strip()))
        county = _counties.get_county(city) or []

        if not county:
            city = location.replace(" ", "-")
            county = _counties.get_county(city)

        cities.append(city)
        counties.extend(county)

    return cities, counties


url = "https://www.ejobs.ro/company/preturi-pentru-tine/194591"
company = "PPT"

scraper = Scraper()
scraper.get_from_url(url)

job_elements = scraper.find("ul", class_="companies-show-jobs__items").find_all(
    "div", class_="job-card"
)

final_jobs = []

for job in job_elements:
    job_title = job.find(
        "h2", class_="job-card-content-middle__title").text.strip()
    job_url = job.find(
        "h2", class_="job-card-content-middle__title").find("a")["href"]
    job_url = "https://www.ejobs.ro" + job_url

    locations = job.find(
        "div", class_="job-card-content-middle__info").text.strip().split(",") if job.find("div", class_="job-card-content-middle__info") else []

    locations.extend(
        job.find("span", class_="PartialList__Rest").get("title").split(
            ",") if job.find("span", class_="PartialList__Rest") else []
    )

    cities = []
    counties = []

    for location in locations:
        city = translate_city(remove_diacritics(
            location.replace("și alte  orașe", "").strip()))
        county = _counties.get_county(city) or []

        cities.append(city)
        counties.extend(county)

    final_jobs.append(
        {
            "job_title": job_title,
            "job_link": job_url,
            "city": cities,
            "county": list(set(counties)),
            "country": "Romania",
            "company": company,
        }
    )


publish_or_update(final_jobs)
publish_logo(company, "https://content.ejobs.ro/img/logos/1/194591.png")

show_jobs(final_jobs)
