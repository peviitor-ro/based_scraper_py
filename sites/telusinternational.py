from scraper.Scraper import Scraper
from utils import (publish, publish_logo, show_jobs)


url = "https://jobs.telusinternational.com/en_US/careers/Romania?source=TI+website&amp%3Btags=telus_main_website&listFilterMode=1&2947=5170&2947_format=4626"

company = "TelusInternational"
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url, verify=False)

jobs = scraper.find_all("li", {"class": "listSingleColumnItem"})

for job in jobs:
    job_title = job.find("h3").text.strip()
    job_link = job.find("h3").find("a").get("href")

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": "Romania",
        "city": "Bucuresti",
        "county": "Bucuresti"
    })

for version in [1,4]:
    publish(version, company, finalJobs, 'APIKEY')
publish_logo(company, "https://jobs.telusinternational.com/portal/11/images/logo_telus-international_header-v2.svg")
show_jobs(finalJobs)
