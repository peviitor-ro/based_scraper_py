from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://magnaelectronicsromania.teamtailor.com/jobs?page="

company = {"company": "MagnaElectronics"}
finalJobs = list()

scraper = Scraper()
rules = Rules(scraper)
page = 1

while True:
    scraper.url = url + str(page)
    jobs = []

    try:
        jobs = rules.getTag("div", {"id": "jobs"}).find("div",{"class":"mx-auto text-lg block-max-w--md"}).find_all("li")
    except:
        break

    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("span", {"class": "text-block-base-link"}).text.strip()
        job_link = job.find("a").get("href")
        city = job.find("div", {"class": "mt-1 text-md"}).find_all("span")[2].text.split(",")[0].strip()

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city
        })

    page += 1

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/6901fc63-3786-4d8b-8230-aa1bcd971324/original.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))
