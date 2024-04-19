from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs

url = "https://www.brd.ro/cariere"

scraper = Scraper()
scraper.get_from_url(url, verify=False)

company = "BRD"
j = set()

elements = scraper.find_all("a", {"class": "category-card-link"})

for element in elements:
    jobCategory = "https://www.brd.ro" + element["href"]
    scraper.get_from_url(jobCategory, verify=False)

    jobs = scraper.find_all("div", {"class": "card"})
    category = element.text.strip()

    for job in jobs:
        title = job.find("div", {"class": "card-header"}).text
        link = "https://www.brd.ro" + job.find("a")["href"]

        j.add((title, link, category))
finalJobs = list()

for job in j:
    job_title = job[0]
    job_link = job[1]
    category = job[2]

    job_element = {
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": "Romania",
        "city": "All",
        "county": "All",
    }

    if category == "IT":
        job_element["remote"] = "Hybrid"

    finalJobs.append(job_element)


publish_or_update(finalJobs)
publish_logo(company, "https://www.brd.ro/sites/all/themes/brd/img/logo-mic.png")
show_jobs(finalJobs)
