from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://careers-ro.jacobsdouweegberts.com/job-search/"

company = {"company": "JacobsDouweEgberts"}   
finaljobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("li", {"class": "app-smartRecruiterSearchResult-list__item"})

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("span", { "class":"job-name"}).text.strip()
    job_link = "https://careers-ro.jacobsdouweegberts.com" + job.find("a").get("href")
    city = job.find("span", { "class":"job-city"}).text.strip()

    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": city,
        "company": company.get("company")
    })

print(json.dumps(finaljobs, indent=4))

loadingData(finaljobs, company.get("company"))

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/JDE_Peet%27s_box_logo.svg/1024px-JDE_Peet%27s_box_logo.svg.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))