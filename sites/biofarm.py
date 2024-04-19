from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()

company = "Biofarm"
url = "https://mingle.ro/api/boards/careers-page/jobs?company=biofarm&page=0&pageSize=1000&sort="

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = []

for job in scraper.markup["data"]["results"]:
    if job["locations"]:
        job_title = job["title"]
        job_link = "https://biofarm.mingle.ro/ro/embed/apply/" + job["uid"]
        city = translate_city(job["locations"][0]["label"])
        county = _counties.get_county(city)

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

publish_logo(company, "https://www.biofarm.ro/wp-content/uploads/2019/10/logo.png")
show_jobs(jobs)
