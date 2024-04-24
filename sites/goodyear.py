from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from math import ceil
from getCounty import GetCounty

_counties = GetCounty()
company = "GoodYear"
url = "https://jobs.goodyear.com/search/?createNewAlert=false&q=&locationsearch=Romania"

scraper = Scraper()
scraper.get_from_url(url)

totalJobs = int(
    scraper.find("span", class_="paginationLabel").find_all("b")[-1].text.strip()
)

pages = ceil(totalJobs / 25)

jobs = []

for page in range(1, pages + 1):

    jobs_elements = (
        scraper.find("table", id="searchresults").find("tbody").find_all("tr")
    )

    for job in jobs_elements:
        job_link = "https://jobs.goodyear.com" + job.find("a")["href"]
        job_title = job.find("a").text.strip()
        job_location = translate_city(job.find("span", class_="jobLocation").text.split(",")[0].title().strip())

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                city=job_location,
                county = _counties.get_county(job_location),
                country="Romania",
                company=company,
            )
        )

    scraper.get_from_url(url + f"&startrow={page * 25}")


publish_or_update(jobs)

publish_logo(
    company, "https://rmkcdn.successfactors.com/38b5d3dd/ef930ba2-97c9-4abc-a14a-e.png"
)
show_jobs(jobs)
