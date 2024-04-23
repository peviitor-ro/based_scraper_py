from scraper.Scraper import Scraper
import re
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty

_counties = GetCounty()
scraper = Scraper()
regex = re.compile(r"search-results-(.*?)-bodyEl")

pageNumber = 1
foundedJobs = True

company = {"company": "ElectronicArts"}
finalJobs = list()

while foundedJobs:
    url = f"https://ea.gr8people.com/jobs?page={pageNumber}&geo_location=ChIJw3aJlSb_sUARlLEEqJJP74Q"

    doom = scraper.post(url, {}).text
    scraper.__init__(doom, "html.parser")

    elementId = re.findall(regex, doom)[0]
    jobsContainer = scraper.find("tbody", {"id": f"search-results-{elementId}-bodyEl"})
    jobs = jobsContainer.find_all("tr")

    foundedJobs = len(jobs) > 0

    for job in jobs:
        job_title = job.find_all("td")[1].text.strip()
        job_link = job.find("a").get("href")
        city = translate_city(job.find_all("td")[3].text.strip().split(",")[0])
        remote = ""

        county = _counties.get_county(city)

        if not county:
            city = ""
            county = ""
            remote = "Remote"

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
                "remote": remote,
            }
        )
    pageNumber += 1

publish_or_update(finalJobs)

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/0/0d/Electronic-Arts-Logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
