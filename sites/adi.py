from scraper_peviitor import Scraper, loadingData
import uuid
import json

apiUrl = "https://analogdevices.wd1.myworkdayjobs.com/wday/cxs/analogdevices/External/jobs"

company = {"company": "ADI"}
finalJobs = list()

scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets":{},"limit":20,"offset":0,"searchText":"Romania"}

scraper.session.headers.update(headers)

numberOfJobs = scraper.post(apiUrl, json=data).json().get("total")

iteration = [i for i in range(0, numberOfJobs, 20)]

for num in iteration:
    data["offset"] = num
    jobs = scraper.post(apiUrl, json=data).json().get("jobPostings")
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.get("title")
        job_link = "https://analogdevices.wd1.myworkdayjobs.com/en-US/External" + job.get("externalPath")
        city = job.get("locationsText").split(",")

        if len(city) > 1:
            city = city[1]
        else:
            city = "Romania"

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

logoUrl = "https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-original-577x577/s3/072011/analog-logo.ai_.png?itok=RM5-oQ34"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))