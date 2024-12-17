from utils import publish_or_update, publish_logo, show_jobs, translate_city, acurate_city_and_county
from getCounty import GetCounty, remove_diacritics
from scraper.Scraper import Scraper

_counties = GetCounty()

url = "https://api.ejobs.ro/companies/317733?jobsPageSize=1000"
company = "SKILLD"

scraper = Scraper()
scraper.get_from_url(url, 'JSON')

final_jobs = []

for job in scraper.markup["jobs"]:
    title = job["title"]
    job_url = 'https://www.ejobs.ro/user/locuri-de-munca/' + \
        job["slug"] + '/' + str(job["id"])
    locations = job["locations"]
    counties = []

    try:
        cities = [
            remove_diacritics(
                translate_city(location["address"])).replace(", Romania", "")
            for location in locations
        ]

        for city in cities:
            county = _counties.get_county(city)
            if county:
                counties += county

    except Exception as e:
        cities = []

    final_jobs.append(
        {
            "job_title": title,
            "job_link": job_url,
            "country": "Romania",
            "company": company,
            "city": cities,
            "county": counties,
        }
    )

publish_or_update(final_jobs)

publish_logo(company, "https://content.ejobs.ro/img/logos/3/317733.png")
show_jobs(final_jobs)
