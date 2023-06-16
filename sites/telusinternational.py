from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://jobs.telusinternational.com/en_US/careers/Romania?source=TI+website&amp%3Btags=telus_main_website&listFilterMode=1&2947=5170&2947_format=4626"

company = {"company": "TelusInternational"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("li", {"class": "listSingleColumnItem"})

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("h3").text.strip()
    job_link = job.find("h3").find("a").get("href")

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": "Romania"
    })

print(finalJobs)

loadingData(finalJobs, company.get("company"))

logoUrl = "https://jobs.telusinternational.com/portal/11/images/logo_telus-international_header-v2.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))