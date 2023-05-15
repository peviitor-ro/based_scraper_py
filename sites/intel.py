from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://jobs.intel.com/en/search-jobs/Romania/599/2/798549/46/25/50/2"

company = {"company": "Intel"}
finalJobs = list()

scraper = Scraper()
scraper.session.headers.update({
    "Accept-Language": "en-GB,en;q=0.9",
})

scraper.url = url
rules = Rules(scraper)


jobs = rules.getTag("section", {"id": "search-results-list"}).findAll("li")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("h2").text.strip()
    job_link = "https://jobs.intel.com" + job.find("a").get("href")
    city = "Romania"

    print(job_title + " -> " + city)
    print(job_link)

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city
    })

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", company.get("company"))

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Intel_logo_%282006-2020%29.svg/800px-Intel_logo_%282006-2020%29.svg.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))