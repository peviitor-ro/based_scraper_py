from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import re
import json

scraper = Scraper()
rules = Rules(scraper)
regex  = re.compile(r"search-results-(.*?)-bodyEl")

pageNumber = 1
foundedJobs = True

company = {"company": "ElectronicArts"}
finalJobs = list()

while foundedJobs:
    url = f"https://ea.gr8people.com/jobs?page={pageNumber}&geo_location=ChIJw3aJlSb_sUARlLEEqJJP74Q"

    doom = scraper.post(url).text
    scraper.soup = doom
    
    elementId = re.findall(regex, doom)[0]
    jobsContainer = rules.getTag("tbody", {"id": f"search-results-{elementId}-bodyEl"})
    jobs = jobsContainer.find_all("tr")

    foundedJobs = len(jobs) > 0

    for job in jobs:
        id = str(uuid.uuid4())
        job_title = job.find_all("td")[1].text.strip()
        job_link = job.find("a").get("href")

        finalJobs.append(
            {
                "id": id,
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": "Romania",
            })

    pageNumber += 1

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))