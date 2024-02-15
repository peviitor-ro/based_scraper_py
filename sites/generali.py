from scraper.Scraper import Scraper
from utils import publish, publish_logo, create_job, show_jobs, translate_city
from getCounty import get_county
from math import ceil

# Cream o instanta a clasei Scraper
url = "https://join.generalicee.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=RO&optionsFacetsDD_city=&optionsFacetsDD_customfield3=&optionsFacetsDD_customfield4=&optionsFacetsDD_customfield2"
scraper = Scraper()
scraper.get_from_url(url)

company = "Generali"
jobs = list()

totalJobs = (
    scraper.find("span", {"class": "paginationLabel"}).text.strip().split(" ")[-1]
)

pages = ceil(int(totalJobs) / 10)

for page in range(pages):
    jobsElements = (
        scraper.find("table", {"id": "searchresults"}).find("tbody").find_all("tr")
    )
    for job in jobsElements:
        job_title = job.find("a").text.strip()
        job_link = "https://join.generalicee.com" + job.find("a")["href"]
        job_location = (
            job.find("span", {"class": "jobLocation"}).text.strip().split(",")
        )
        job_city = translate_city(job_location[0].strip())
        job_county = get_county(job_city)
        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=company,
                country="Romania",
                city=job_city,
                county=job_county,
            )
        )

    scraper.get_from_url(f"{url}&start={page * 10}")


publish(4, company, jobs, "APIKEY")

publish_logo(company, "https://www.generali.ro/wp-content/uploads/2022/06/logo.svg")
show_jobs(jobs)
