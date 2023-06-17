from scraper_peviitor import Scraper, loadingData
import uuid
import json

url = "https://ptc.eightfold.ai/api/apply/v2/jobs?domain=ptc.com&start=0&location=Bucharest%2C%20Romania&domain=ptc.com&sort_by=relevance"

company = {"company": "PTC"}
finalJobs = list()

scraper = Scraper(url)

totalJobs = scraper.getJson().get("count")

pages = [*range(0, totalJobs, 10)]

for page in pages:
    scraper.url = url.replace("start=0", "start=" + str(page))
    jobs = scraper.getJson().get("positions")
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.get("name")
        job_link = "https://ptc.eightfold.ai/careers?pid=" + str(job.get("id")) + "&domain=ptc.com&sort_by=relevance"
        city = job.get("location").split(",")[0]
        
        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": city,
            "company": company.get("company")
        })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/PTC_logo.svg/1280px-PTC_logo.svg.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))