from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()
company = "BANCATRANSILVANIA"
url = "https://api.ejobs.ro/companies/8092"

jobs = []

scraper = Scraper()
scraper.get_from_url(url, "JSON")

response = scraper.markup.get("jobs")


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url)

    locations = scraper.find("meta", {"data-hid": "cXenseParse:b19-ejobs_city"})[
        "content"
    ].split(",")

    cities = [translate_city(remove_diacritics(location)) for location in locations]
    counties = []

    for city in cities:
        county = _counties.get_county(city)
        counties.extend(county or [])

    return cities, counties


for job in response:
    job_title = job.get("title")
    job_link = (
        "https://www.ejobs.ro/user/locuri-de-munca/"
        + job.get("slug")
        + "/"
        + str(job.get("id"))
    )
    country = "Romania"
    locations = job.get("locations")

    cities = []
    counties = []

    for location in locations:
        try:
            city = translate_city(
                remove_diacritics(location.get("address").split(",")[0].strip())
            )
            county = _counties.get_county(city)

            if not county:
                city = remove_diacritics(
                    location.get("address").split(",")[0].strip().replace(" ", "-")
                )
                county = _counties.get_county(city)

            cities.append(city)
            counties.extend(county)
        except Exception as e:
            cities = []
            counties = []

    if not cities:
        cities, counties = get_aditional_city(job_link)

    jobs.append(
        create_job(
            job_title=job_title,
            job_link=job_link,
            company=company,
            country=country,
            city=cities,
            county=counties,
        )
    )


publish_or_update(jobs)
publish_logo(
    company,
    "https://www.bancatransilvania.ro/themes/bancatransilvania/assets/images/logos/bt-cariere.svg",
)

show_jobs(jobs)
