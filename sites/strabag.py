from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://jobboerse.strabag.at/inc/jobsuche_2022.php"

company = {"company": "Strabag"}
finaljobs = list()

scraper = Scraper()
rules = Rules(scraper)

data = {
    "MIME Type":"application/x-www-form-urlencoded; charset=UTF-8",
# "morejobs":0
"search":"Romania",
"radius":50,
"language":"RO",
"status":1
}

response = scraper.post(url, data=data)

scraper.soup = response.text

jobs = rules.getTags("div", {"class": "row datenSatz dunkelGrau"})

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("div", {"class": "row"}).find_all("div")[0].text.strip()
    job_link = job.find("a").get("href")
    country = "Romania"
    city = "Romania"
    company = "Strabag"

    print(job_title + " -> " + city)
    
    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city
    })

print("Total jobs: " + str(len(finaljobs)))

loadingData(finaljobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Strabag")

logoUrl = "https://jobboerse.strabag.at/img/strabag-logo-300px.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":"Strabag",
        "logo":logoUrl
    }
]))