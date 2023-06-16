from scraper_peviitor import Scraper, loadingData, Rules
import uuid
import json

url = "https://careers.smartrecruiters.com/PublicisGroupe?search=Romania"

company = {"company": "PublicisGroupe"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("li", {"class": "job"})

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("h4", {"class":"job-title"}).text.strip()
    job_link = job.find("a").get("href")
    city = job.find("p", {"class": "job-desc"}).find("span").text.split(",")[0].strip()

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": city,
        "company": company.get("company")
    })

print(finalJobs)

loadingData(finalJobs, company.get("company"))

logoUrl = "https://c.smartrecruiters.com/sr-company-logo-prod-aws-dc1/58822766e4b0680b1154ae69/huge?r=s3&_1533642429153"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))