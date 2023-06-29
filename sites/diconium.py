from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://jobs.diconium.com/en/category/data-ai/59954e8a-f49e-5d4a-b37b-6177b94e1bb4"

company = {"company": "Diconium"}
finalJobs = list()

d = []

scraper = Scraper(url)
rules = Rules(scraper)

linkJobs = rules.getTag("div", {"class": "hasCategories"}).find_all("a")

for link in linkJobs:
    data = json.loads(link.get("data-offerids"))
    if data:
        
        d.append({
            "offerIds": data, "categoryId": link.get("data-id"), "page":1
        })


url = "https://jobs.diconium.com/en/api/filter/offers-content-category/diconium-jobs-en"

for data in d:
    response = scraper.post(url, json.dumps(data))
    html = response.json().get("html")
    scraper.soup = html

    jobs = scraper.soup.findAll("a", {"class": "shont item"})

    for job in jobs:
        location = job.find("div", {"class": "p cityNames"}).text.strip()

        if location == "Bucharest":
            id = uuid.uuid4()
            job_title = job.find("div", {"class":"h3"}).text.strip()
            job_link = job.get("href")
            city = location

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

logoUrl = "https://jobs.diconium.com/en/uploads/1623/settings/companies/diconium-jobs-en-96-6059ae9f8dd12.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))