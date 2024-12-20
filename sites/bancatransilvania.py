from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()
company = "BANCATRANSILVANIA"
url = "https://cariere.bancatransilvania.ro/hrscapi/api/CareersSite/jobOpenings?currentPage=1&itemsPerPage=1000"

jobs = []

scraper = Scraper()
scraper.get_from_url(url, "JSON")

response = scraper.markup.get("jobOpenings")

for job in response:
    job_title = job.get("title")
    job_link = (
        "https://cariere.bancatransilvania.ro/joburi-disponibile/"
        + job.get("postSlug")
    )
    country = "Romania"
    locations = job.get("locations")

    cities = []
    counties = []

    for location in locations:
        try:
            city = translate_city(
                remove_diacritics(location.get(
                    "name").title().replace(" ", "-"))
            )
            county = _counties.get_county(city)

            if not county:
                city = remove_diacritics(
                    location.get("address").split(",")[
                        0].strip().replace(" ", "-")
                )
                county = _counties.get_county(city)

            cities.append(city)
            counties.extend(county)
        except Exception as e:
            cities = []
            counties = []

    jobs.append(
        create_job(
            job_title=job_title,
            job_link=job_link,
            company=company,
            country=country,
            city=cities,
            county=list(set(counties)),
        )
    )

publish_or_update(jobs)
publish_logo(
    company,
    "https://www.bancatransilvania.ro/themes/bancatransilvania/assets/images/logos/bt-cariere.svg",
)

show_jobs(jobs)
