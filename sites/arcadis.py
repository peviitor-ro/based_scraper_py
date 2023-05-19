from scraper_peviitor import Scraper, loadingData
import uuid
import json
import re

url = "https://careers.arcadis.com/search-results?qkstate=Romania"

company = {"company": "Arcadis"}
finalJobs = list()

scraper = Scraper()
response = scraper.session.get(url)

pattern = re.compile(r"phApp.ddo = {(.*?)};", re.DOTALL)

data = re.search(pattern, response.text).group(1)
jobs = json.loads("{" + data + "}").get("eagerLoadRefineSearch").get("data").get("jobs")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("title")
    job_link = job.get("applyUrl")
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

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", company.get("company"))

logoUrl = "https://cdn.phenompeople.com/CareerConnectResources/ARCAGLOBAL/images/MicrosoftTeams-image32-1620211091518.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))