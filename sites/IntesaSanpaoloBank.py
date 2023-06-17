from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://www.intesasanpaolobank.ro/en/persoane-fizice/Our-World/cariere.html"

company = {"company": "IntesaSanpaoloBank"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("article", {"class": "careersItem"})

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("h2").text.strip()
    job_link = "https://www.intesasanpaolobank.ro" + job.find("a").get("href")
    city = job.find("p").text.strip()
    
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

logoUrl = "https://www.epromsystem.com/wp-content/uploads/2021/09/Clienti-INTESASP-epromsystem.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))