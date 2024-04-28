from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs
from getCounty import GetCounty

_counties = GetCounty()
company = "Selgros"
url = "https://mingle.ro/api/boards/careers-page/jobs?company=selgros&page=0&pageSize=1000"

scraper = Scraper()
scraper.get_from_url(url, "JSON")

acurate_city = {
    "Iasi": {"city": "Iasi", "county": "Iasi"},
}

jobs = []

for job in scraper.markup["data"]["results"]:
    try:
        locations = job["locations"]
        cities = []
        counties = []
        for city in locations:
            if "Bucuresti" in city["label"]:
                if "Bucuresti" not in cities:
                    cities.append("Bucuresti")
                    counties.append("Bucuresti")
            else:

                county = _counties.get_county(city["label"])

                if county and county not in counties:
                    cities.append(city["label"])
                    counties.extend(county)
                else:
                    county = _counties.get_county(city["label"].replace(" ", "-"))
                    if county and county not in counties:
                        cities.append(city["label"].replace(" ", "-"))
                        counties.extend(county)
        jobs.append(
            create_job(
                job_title=job["title"],
                job_link="https://selgros.mingle.ro/ro/embed/apply/" + job["uid"],
                city=cities,
                country="Romania",
                company=company,
                county=counties,
            )
        )
    except Exception as e:
        pass

publish_or_update(jobs)

publish_logo(
    company,
    "https://www.selgros.ro/themes/contrib/garnet/dist/assets/branding/logo-selgros.svg",
)
show_jobs(jobs)
