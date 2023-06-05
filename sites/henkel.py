from scraper_peviitor import Scraper, loadingData
import uuid
import json

url = "https://www.henkel.ro/ajax/collection/ro/1338824-1338824/queryresults/asJson?Career_Level_18682=&Functional_Area_18674=&Digital_1030670=&Locations_279384=Europe&Europe_877522=ROU&search_filter=&startIndex=0&loadCount=10&ignoreDefaultFilterTags=true"

company = {"company": "Henkel"}
finaljobs = list()

scraper = Scraper(url)

jobs = scraper.getJson().get("results")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("title")
    job_link = "https://www.henkel.ro" + job.get("link")
    city = ""

    try:
        city = job.get("location").split(",")[1].strip()
    except:
        city = "Romania"

    print(job_title + " -> " + city)
    
    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "company": company.get("company"),
        "city": city
    })

print("Total jobs: " + str(len(finaljobs)))

loadingData(finaljobs, company.get("company"))

logoUrl = "https://www.henkel.ro/resource/blob/737324/1129f40d0df611e51758a0d35e6cab78/data/henkel-logo-standalone-svg.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":"Ericsson",
        "logo":logoUrl
    }
]))


