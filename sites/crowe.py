from scraper.Scraper import Scraper
from utils import show_jobs, translate_city, publish_or_update, publish_logo
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()

url = (
    "https://mingle.ro/api/boards/careers-page/jobs?company=crowe&page=0&pageSize=1000"
)
scraper = Scraper()
scraper.get_from_url(url, "JSON")

company = "Crowe"
jobs = list()

jobs_elements = scraper.markup.get("data").get("results")

for job in jobs_elements:
    job_title = job.get("title")
    job_link = "https://crowe.mingle.ro/en/apply/" + job.get("uid")
    cities = []
    counties = []

    if job.get("locations"):
        for location in job.get("locations"):
            city = translate_city(remove_diacritics(location.get("label")))
            county = _counties.get_county(city)

            if not county:
                city = city.replace(" ", "-")
                county = _counties.get_county(city)

            if county:
                cities.append(city)
                counties.extend(county)
    else:
        cities = ["Bucuresti", "Timisoara", "Cluj-Napoca"]
        counties = ["Bucuresti", "Timis", "Cluj"]

    jobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": "Romania",
            "city": list(set(cities)),
            "county": list(set(counties)),
        }
    )


publish_or_update(jobs)

logoUrl = "https://i.ytimg.com/vi/dTmm3WNIpnc/maxresdefault.jpg"
publish_logo(company, logoUrl)
show_jobs(jobs)
