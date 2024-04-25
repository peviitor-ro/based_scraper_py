from scraper.Scraper import Scraper
from utils import (
    translate_city,
    acurate_city_and_county,
    create_job,
    show_jobs,
    publish_logo,
    publish_or_update,
)
from getCounty import GetCounty

url = "https://cariere.mega-image.ro/api/vacancy/?options%5Bsort_order%5D=desc&sort=created&sortDir=DESC&pageSize=1000"
_counties = GetCounty()

scraper = Scraper()
scraper.set_headers({"Content-Type": "application/json"})
scraper.get_from_url(url, type="JSON")

pageNumber = 1

jobs = scraper.markup.get("vacancies")

company = {"company": "MegaImage"}
finalJobs = list()

acurate_city = acurate_city_and_county(
    iasi={"city": "Iasi", "county": "Iasi"},
    municipiul_bucuresti={"city": "Bucuresti", "county": "Bucuresti"},
    stefanestii_de_jos={"city": "Stefanestii de Jos", "county": "Ilfov"},
    cluj_napoca={"city": "Cluj-Napoca", "county": "Cluj"},
)


for job in jobs:
    job_title = job.get("title")
    job_link = (
        "https://cariere.mega-image.ro/post-vacant/"
        + str(job.get("id"))
        + "/"
        + job.get("slug")
    )

    job_element = create_job(
        job_title=job_title,
        job_link=job_link,
        company=company.get("company"),
        country="Romania",
    )

    city = translate_city(job.get("city").title())

    if acurate_city.get(city.replace(" ", "_").replace("-", "_").lower()):
        job_element["city"] = acurate_city.get(
            city.replace(" ", "_").replace("-", "_").lower()
        ).get("city")
        job_element["county"] = acurate_city.get(
            city.replace(" ", "_").replace("-", "_").lower()
        ).get("county")
    else:
        job_element["city"] = city
        job_element["county"] = _counties.get_county(city)

    finalJobs.append(job_element)

publish_or_update(finalJobs)

logo_url = "https://cariere.mega-image.ro/uploads/MEGA%20IMAGE%20LOGO.png"
publish_logo(company.get("company"), logo_url)
show_jobs(finalJobs)
