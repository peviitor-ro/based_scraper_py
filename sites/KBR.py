from scraper_peviitor import Scraper, loadingData
import uuid
import json

apiUrl = "https://kbr.wd5.myworkdayjobs.com/wday/cxs/kbr/KBR_Careers/jobs"

company = {"company": "KBR"}
finalJobs = list()

scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets":{"locationHierarchy1":["7d7dca02efe30103cd2815e9f401c80a"]},"limit":20,"offset":0,"searchText":""}

scraper.session.headers.update(headers)

numberOfJobs = scraper.post(apiUrl, json=data).json().get("total")

iteration = [i for i in range(0, numberOfJobs, 20)]

for num in iteration:
    data["offset"] = num
    jobs = scraper.post(apiUrl, json=data).json().get("jobPostings")
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.get("title")
        job_link = "https://kbr.wd5.myworkdayjobs.com/en-US/KBR_Careers" + job.get("externalPath")
        city = job.get("locationsText").split(",")[0]

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city
        })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://kbr.wd5.myworkdayjobs.com/KBR_Careers/assets/logo"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))