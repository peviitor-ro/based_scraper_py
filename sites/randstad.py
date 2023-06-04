from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json
import re

url = "https://www.randstad.ro/locuri-de-munca/lucreaza-la-randstad/"

company = {"company": "Randstad"}
finalJobs = list()

scraper = Scraper(url)

pattern = re.compile(r"const data = {(.*?)};", re.DOTALL)

data = re.search(pattern, scraper.soup.prettify()).group(1)
jobs = json.loads("{" + data + "}").get("ecommerce").get("impressions")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("job_title")
    job_link = "https://www.randstad.ro" + job.get("url")
    city = job.get("city")

    print(job_title + " -> " + city)
    
    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city
    })

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/1/10/Randstad_Logo.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))