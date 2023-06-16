from scraper_peviitor import Scraper, loadingData
import uuid
import json

url = "https://www.infineon.com/search/jobs/jobs"

company = {"company": "Infineon"}
finaljobs = list()

data = {
    "term": "",
    "offset":0,
    "max_results":100,
    "lang":"en",
    "country":"Romania"
}

scraper = Scraper()
scraper.session.headers.update(
    {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
)

response = scraper.post(url = url, data = data)

jobs = response.json().get("pages").get("items")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("title")
    job_link = "https://www.infineon.com" + job.get("detail_page_url")
    city = job.get("location")[0]
    
    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": city,
        "company": company.get("company")
    })

print(finaljobs)

loadingData(finaljobs, company.get("company"))

logoUrl = "https://www.infineon.com/frontend/release_2023-03/dist/resources/img/logo-mobile-en.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))