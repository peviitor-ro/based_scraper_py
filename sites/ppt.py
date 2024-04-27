from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty, remove_diacritics
from scraper.Scraper import Scraper

_counties = GetCounty()


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url)

    locations = scraper.find("meta", {"data-hid": "cXenseParse:b19-ejobs_city"})[
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

job_elements = scraper.find("main", class_="CDInner__Main").find_all(
    "div", class_="JobCard"
)

final_jobs = []

for job in job_elements:
    job_title = job.find("h2", class_="JCContentMiddle__Title").text.strip()
    job_url = job.find("h2", class_="JCContentMiddle__Title").find("a")["href"]
    job_url = "https://www.ejobs.ro" + job_url

    locations = job.find("div", class_="JCContentMiddle__Info").text.strip().split(",")

    if "și alte" in locations[-1]:
        cities, counties = get_aditional_city(job_url)
    else:
        cities = []
        counties = []

        for location in locations:
            city = translate_city(remove_diacritics(location.strip()))
            county = _counties.get_county(city) or []

            if not county:
                city = city.replace(" ", "-")
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
